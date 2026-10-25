#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""protocol_check.py — 节点处理规范 × 内核实际能力的一致性自检

回答一个问题：**我们生成的配置，是否还在内核当前版本的正确用法内？**

做三件事（全部只读，不联网）：

1. 样本矩阵：每种「协议 × 传输 × 安全层 × 插件」组合，先用转换器生成配置，
   再交给内核自己的校验命令（v2ray `test -c`、xray `-test -config`、
   mihomo `-t -f`、sing-box `check -c`）。预期支持却生成失败 / 校验不过 → 退出码 1。
2. 参数保真：传输层参数不能被静默丢弃。生成出来的配置里 network/transport 必须
   与 URI 声明的一致，否则节点会因为「退化成 tcp」而连接失败（历史 bug，
   见 references/known-issues.md）。
3. 加密方式矩阵：ss 各加密方式逐个试内核，和 layout.CAPS 的 ss_ciphers 白名单比对。

用法：
    python protocol_check.py                 # 全量自检
    python protocol_check.py --verbose       # 打印每个用例的内核报错
    python protocol_check.py --core xray     # 只查一个内核
    python protocol_check.py --tools <bin>   # 指定内核目录

退出码：0 全部一致；1 有不一致（需要更新转换器或 layout.CAPS）；2 环境问题（内核缺失）
"""

import argparse
import base64
import json
import os
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import collect_nodes as c  # noqa: E402
import layout as lay  # noqa: E402
import test_nodes as t  # noqa: E402

UUID = "11111111-1111-1111-1111-111111111111"
PBK = "jNXHt1yRo0vDuchQlIP6Z0ZvjT3KtzVI-T4E7RoLJS0"   # 32 字节 base64url，43 字符
KEY32 = base64.b64encode(b"0123456789abcdef0123456789abcdef").decode()
# 预期支持情况（True=该内核应当能生成并通过校验；False=应当判定为不支持）
SKIP, OK = False, True


def _vmess(**kw):
    d = {"v": "2", "ps": "t", "add": "example.com", "port": "443", "id": UUID, "aid": "0",
         "scy": "auto", "net": "tcp", "type": "none", "host": "", "path": "", "tls": "", "sni": ""}
    d.update(kw)
    return "vmess://" + base64.b64encode(json.dumps(d).encode()).decode()


def _ss(method, pwd, query=""):
    blob = base64.b64encode(f"{method}:{pwd}".encode()).decode().rstrip("=")
    return f"ss://{blob}@example.com:8388{query}#ss"


# name, uri, {core: 预期}
CASES = [
    ("vmess tcp", _vmess(), {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("vmess ws+tls", _vmess(net="ws", host="a.com", path="/ws", tls="tls", sni="a.com"),
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("vmess grpc+tls", _vmess(net="grpc", path="gs", tls="tls", sni="a.com"),
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("vmess h2+tls", _vmess(net="h2", host="a.com", path="/h", tls="tls", sni="a.com"),
     {"v2ray": OK, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("vmess httpupgrade+tls", _vmess(net="httpupgrade", host="a.com", path="/u", tls="tls", sni="a.com"),
     {"v2ray": SKIP, "xray": OK, "clash": SKIP, "singbox": OK}),
    ("vmess xhttp+tls", _vmess(net="xhttp", host="a.com", path="/x", tls="tls", sni="a.com"),
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": SKIP}),
    ("vmess kcp", _vmess(net="kcp"), {"v2ray": OK, "xray": OK, "clash": SKIP, "singbox": SKIP}),
    ("vmess quic", _vmess(net="quic"), {"v2ray": OK, "xray": SKIP, "clash": SKIP, "singbox": SKIP}),
    ("vless tcp 明传", f"vless://{UUID}@example.com:80?encryption=none&type=tcp#v",
     {"v2ray": OK, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("vless reality+flow",
     f"vless://{UUID}@example.com:443?encryption=none&security=reality&sni=www.microsoft.com"
     f"&fp=chrome&pbk={PBK}&sid=ab&type=tcp&flow=xtls-rprx-vision#v",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": OK}),
    ("vless reality 坏公钥",
     f"vless://{UUID}@example.com:443?security=reality&pbk=short&sni=a.com#v",
     {"v2ray": SKIP, "xray": SKIP, "clash": SKIP, "singbox": SKIP}),
    ("vless ws+tls", f"vless://{UUID}@example.com:443?security=tls&sni=a.com&type=ws&path=%2Fws&host=a.com#v",
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("vless grpc+tls", f"vless://{UUID}@example.com:443?security=tls&sni=a.com&type=grpc&serviceName=g#v",
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("vless http(h2)+tls", f"vless://{UUID}@example.com:443?security=tls&sni=a.com&type=http&path=%2Fh&host=a.com#v",
     {"v2ray": OK, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("vless splithttp", f"vless://{UUID}@example.com:443?security=tls&sni=a.com&type=splithttp&path=%2Fs#v",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": SKIP}),
    ("vless kcp", f"vless://{UUID}@example.com:443?security=tls&sni=a.com&type=kcp#v",
     {"v2ray": OK, "xray": OK, "clash": SKIP, "singbox": SKIP}),
    ("trojan 无 security", "trojan://pw@example.com:443?sni=a.com#t",
     {"v2ray": OK, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("trojan ws+tls", "trojan://pw@example.com:443?security=tls&sni=a.com&type=ws&path=%2Fws&host=a.com#t",
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("trojan+reality", f"trojan://pw@example.com:443?security=reality&pbk={PBK}&sid=ab&sni=a.com#t",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": OK}),
    ("ss aes-256-gcm", _ss("aes-256-gcm", "pwd"), {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("ss aes-256-cfb", _ss("aes-256-cfb", "pwd"), {"v2ray": SKIP, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("ss plugin obfs", _ss("aes-256-gcm", "pwd", "?plugin=obfs-local%3Bobfs%3Dhttp%3Bobfs-host%3Dbing.com"),
     {"v2ray": SKIP, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("ss plugin v2ray-plugin",
     _ss("aes-256-gcm", "pwd", "?plugin=v2ray-plugin%3Bmode%3Dwebsocket%3Bhost%3Da.com%3Bpath%3D%2Fws"),
     {"v2ray": SKIP, "xray": SKIP, "clash": OK, "singbox": OK}),
    ("ss2022 合法密钥", f"ss://{base64.b64encode(('2022-blake3-aes-256-gcm:' + KEY32).encode()).decode()}@example.com:8388#s",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": OK}),
    ("ss2022 非法密钥", f"ss://{base64.b64encode(b'2022-blake3-aes-256-gcm:short').decode()}@example.com:8388#s",
     {"v2ray": SKIP, "xray": SKIP, "clash": SKIP, "singbox": SKIP}),
    ("hysteria2", "hysteria2://pwd@example.com:443?sni=a.com&insecure=1#h",
     {"v2ray": OK, "xray": OK, "clash": OK, "singbox": OK}),
    ("hysteria2+obfs", "hysteria2://pwd@example.com:443?sni=a.com&obfs=salamander&obfs-password=x#h",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": OK}),
    ("hysteria2+mport", "hysteria2://pwd@example.com:443?sni=a.com&mport=443-8443#h",
     {"v2ray": SKIP, "xray": OK, "clash": OK, "singbox": OK}),
    ("tuic v5", f"tuic://{UUID}:pwd@example.com:443?sni=a.com&congestion_control=bbr&alpn=h3&udp_relay_mode=native#tu",
     {"v2ray": SKIP, "xray": SKIP, "clash": OK, "singbox": OK}),
]

# ss 加密方式：白名单（layout.CAPS）必须与内核实际接受情况一致
SS_CIPHERS = ["aes-128-gcm", "aes-256-gcm", "chacha20-ietf-poly1305", "xchacha20-ietf-poly1305",
              "aes-256-cfb", "chacha20-ietf", "rc4-md5", "none"]


def core_net(core, uri):
    """该内核配置里应当出现的传输名；tcp 返回 None。"""
    facts = lay.node_facts(uri)
    raw = ""
    low = uri.lower()
    if low.startswith("vmess://"):
        raw = (json.loads(lay.b64d(uri[8:].split("#")[0]) or "{}").get("net") or "tcp").lower()
    elif "://" in uri and not low.startswith("ss"):
        raw = (c._q(uri).get("type") or "tcp").lower()  # noqa: SLF001
    net = facts["net"]
    if net in ("", "tcp"):
        return None
    if core == "clash":
        return "h2" if raw == "h2" else net
    if core == "singbox":
        return "http" if net == "http" else net
    return net


def actual_net(core, cfg):
    if core in ("v2ray", "xray"):
        return ((cfg.get("outbounds") or [{}])[0].get("streamSettings") or {}).get("network")
    if core == "clash":
        return (cfg.get("proxies") or [{}])[0].get("network")
    return ((cfg.get("outbounds") or [{}])[0].get("transport") or {}).get("type")


def check_case(core, name, uri, expect, exe, verbose):
    cfg = t.build_config(core, uri, 39990)
    if cfg is None:
        return (expect is SKIP), ("应生成配置却判为不支持" if expect else "")
    if expect is SKIP:
        return False, "预期不支持，却生成了配置（会被误测）"
    net = core_net(core, uri)
    got = actual_net(core, cfg)
    if net and got != net:
        return False, f"传输参数丢失：期望 {net}，实际 {got or 'tcp'}"
    tmp = tempfile.mkdtemp(prefix="pc_")
    path = os.path.join(tmp, "config.yaml" if core == "clash" else "config.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False)
    ok, out = t.check_config(core, exe, path)
    if ok:
        return True, ""
    last = (out or "").strip().splitlines()
    return False, (last[-1][:140] if last else "内核校验失败")


def check_ciphers(core, exe, verbose):
    """ss 加密方式：内核接受与否，和 CAPS 白名单是否一致。"""
    caps = lay.CAPS[lay.canon(core)].get("ss_ciphers")
    bad = []
    for m in SS_CIPHERS:
        uri = _ss(m, "pwd")
        cfg = t.build_config(core, uri, 39990)
        allowed = caps is None or m in caps
        if cfg is None:
            if allowed:
                bad.append(f"{m}: 白名单允许但转换器拒绝")
            continue
        if not allowed:
            bad.append(f"{m}: 白名单拒绝但转换器仍生成")
            continue
        tmp = tempfile.mkdtemp(prefix="pc_")
        path = os.path.join(tmp, "config.yaml" if core == "clash" else "config.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        ok, out = t.check_config(core, exe, path)
        if not ok:
            last = (out or "").strip().splitlines()
            bad.append(f"{m}: 内核拒绝（{last[-1][:80] if last else ''}）")
    return bad


def main():
    ap = argparse.ArgumentParser(description="协议处理规范 × 内核能力一致性自检")
    ap.add_argument("--tools", default=t.DEFAULT_TOOLS, help="内核 bin 目录")
    ap.add_argument("--core", default=None, help="只查一个内核")
    ap.add_argument("--verbose", action="store_true", help="打印每条失败的内核报错")
    args = ap.parse_args()

    cores = [lay.canon(args.core)] if args.core else list(lay.CORES)
    missing = [x for x in cores if not os.path.exists(
        os.path.join(args.tools, lay.CORE_BIN[x][0], lay.CORE_BIN[x][1]))]
    if missing:
        print(f"[error] 缺少内核：{', '.join(missing)}（先跑 check_kernels.py --update）",
              file=sys.stderr)
        return 2

    print("== 版本基线 ==")
    for core in cores:
        spec = t.CORES[core]
        exe = os.path.join(args.tools, spec["dir"], spec["exe"])
        ver = t._run(exe, ["version"] if core != "clash" else ["-v"])[1].strip().splitlines()
        print(f"  {core:<8} {ver[0][:70] if ver else '(未知版本)'}")
        t.detect_core_features(core, exe)

    failures = 0
    print("\n== 样本矩阵 ==")
    for core in cores:
        exe = os.path.join(args.tools, t.CORES[core]["dir"], t.CORES[core]["exe"])
        ok_n = skip_n = 0
        for name, uri, expect in CASES:
            want = expect.get(core, SKIP)
            good, why = check_case(core, name, uri, want, exe, args.verbose)
            if want:
                ok_n += 1
            else:
                skip_n += 1
            if not good:
                failures += 1
                print(f"  [FAIL] {core:<8} {name:<24} {why}")
        print(f"  {core:<8} 通过（支持 {ok_n} / 预期不支持 {skip_n}）")

    print("\n== ss 加密方式 ==")
    for core in cores:
        exe = os.path.join(args.tools, t.CORES[core]["dir"], t.CORES[core]["exe"])
        bad = check_ciphers(core, exe, args.verbose)
        if bad:
            failures += len(bad)
            for b in bad:
                print(f"  [FAIL] {core:<8} {b}")
        else:
            print(f"  {core:<8} 白名单与内核一致")

    print()
    if failures:
        print(f"[FAIL] {failures} 项不一致：转换器或 layout.CAPS 需要跟进（见 references/protocol.md）")
        return 1
    print("[OK] 配置生成、参数保真、加密方式与四个内核当前版本完全一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
