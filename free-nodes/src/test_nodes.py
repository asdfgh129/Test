#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_nodes.py — 分代理内核的节点可用性验证

流程：
1. 读取根目录 nodes/nodes_uris.txt（内部主清单），并按各内核订阅文件里**实际发布**的节点做交集
2. 第一级：TCP 连通性预筛（高并发，快速剔除服务器都不通的节点）。
   采集阶段已默认丢弃 TCP 不可达节点（collect_nodes.py 的 --keep-dead 可关闭），
   这里再筛一次是为了兜住「采集到验证之间新死的」节点
3. 第二级：按代理内核逐一实测（默认 3s 超时、24 并发；超时即判失败不再等）
   - v2ray   ：vmess / vless / trojan / ss / hysteria2（不支持 REALITY、不支持 vless flow）
   - xray    ：vmess / vless / trojan / ss / hysteria2（支持 REALITY / flow）
   - clash   ：vmess / vless / trojan / ss / ssr / hysteria2 / tuic（内核是 mihomo）
   - singbox ：vmess / vless / trojan / ss / hysteria2 / tuic
   为每个节点生成该内核的临时配置 → 启动内核 → 通过本地 HTTP 代理访问测试地址 → 判定可用
4. **全量测试策略（默认，晚间空闲时段）**：某内核候选数 ≤ --full-below（默认 3000）时
   **全部测试**；超过则只测排序前 --max-test（默认 3000）个。排序沿用「协议轮流交错 +
   仓库质量优先 + CF 前置排最后 + TCP 延迟升序」，TCP 不通的已在预筛阶段剔除。
   加 --no-full-test 可回到旧的「--limit 初始取样 + 可用数 < --min-available 自适应扩量」模式
5. 输出（根目录下分三个子目录，每个内核只有 1 个文件）：
   - nodes/available_v2ray.txt / nodes/available_xray.txt    base64 订阅
   - nodes/available_clash.yaml                              clash 配置
   - nodes/available_singbox.json                            sing-box 配置
   - Docs/summary.md（按日期倒序累积）/ Docs/summary.json（最新快照）
   - nodes/pool/pool_<core>.<ext> 池文件 + nodes/pool/pool_state.json 元数据

用法：
    python test_nodes.py --input <free-nodes 根目录>
    python test_nodes.py --input <根目录> --full-below 3000 --max-test 3000
    python test_nodes.py --input <根目录> --no-full-test --limit 200 --min-available 10
"""

import argparse
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect_nodes as c  # 复用解析与格式转换逻辑
import layout as lay  # 统一布局：四内核命名/能力矩阵/文件格式/md 日志
import pool as node_pool  # 按内核的跨天可用节点池

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 自适应扩量阈值（旧模式 --no-full-test）：单内核可用节点数低于这个值，就继续往后追加测试。
# 免费节点失效率高，固定取样常常只捞到个位数可用节点，靠扩量把候选池吃透。
MIN_AVAILABLE = 10

# 全量测试策略（默认，2026-10-25 起，用户要求：晚间时间空闲，尽量测全）：
# 某内核候选数 ≤ FULL_BELOW → 全部测试；> FULL_BELOW → 只测排序前 MAX_TEST 个。
# 排序 = 协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序（TCP 不通的已预筛剔除）。
# 默认值集中在 layout.py（collect_nodes 的命令行默认值也读它，保证一致）。
FULL_BELOW = lay.FULL_BELOW
MAX_TEST = lay.MAX_TEST


def _default_tools_dir():
    """内核目录查找顺序：环境变量 → 用户数据目录 → 技能内 tools/bin。"""
    env = os.environ.get("FREE_NODES_TOOLS")
    if env and os.path.isdir(env):
        return env
    user_data = os.path.join(os.path.expanduser("~"), ".workbuddy", "data", "free-nodes-tools", "bin")
    if os.path.isdir(user_data):
        return user_data
    return os.path.join(os.path.dirname(SCRIPT_DIR), "tools", "bin")


DEFAULT_TOOLS = _default_tools_dir()

# 内核能力实测缓存（core → {"allow_insecure": bool, "check_cmd": [...]}）
_CORE_FEATURES = {}

# 各内核「只校验配置、不联网」的命令；顺序即优先级，脚本会自动识别哪种写法被支持
CHECK_CMDS = {
    "v2ray": [["test", "-c"], ["-test", "-config"]],   # v2fly 5.x 改成 test -c
    "xray": [["-test", "-config"], ["test", "-c"]],
    "clash": [["-t", "-f"]],                            # mihomo
    "singbox": [["check", "-c"]],
}

PROBE_UUID = "11111111-1111-1111-1111-111111111111"


def _run(exe, args, timeout=25):
    try:
        p = subprocess.run([exe, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout,
                           creationflags=CREATE_NO_WINDOW)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except OSError as e:
        return 127, str(e)


def check_config(core, exe, path, timeout=25):
    """用内核自己的配置校验命令检查一份配置文件，返回 (ok, 输出)。

    各内核的写法随版本变过（v2fly 5.x 用 `test -c`，老版用 `-test -config`），
    这里按候选命令逐个试，认准一个后就缓存住。
    """
    core = lay.canon(core)
    feat = _CORE_FEATURES.setdefault(core, {})
    cands = list(CHECK_CMDS.get(core, []))
    if feat.get("check_cmd"):
        cands = [feat["check_cmd"]] + [x for x in cands if x != feat["check_cmd"]]
    last = ""
    for cmd in cands:
        code, out = _run(exe, [*cmd, path], timeout)
        last = out
        low = out.lower()
        if "flag provided but not defined" in low or "unknown command" in low:
            continue
        feat["check_cmd"] = cmd
        return code == 0, out
    return False, last


def detect_core_features(core, exe):
    """探测该内核当前是否还接受 tlsSettings.allowInsecure（Xray 26.x 起已移除）。

    写死版本判断太脆：这里直接用一条 TLS 样本配置让内核自己校验，结果缓存。
    """
    core = lay.canon(core)
    feat = _CORE_FEATURES.setdefault(core, {})
    if "allow_insecure" in feat:
        return feat
    if core not in ("xray", "v2ray") or not os.path.exists(exe):
        feat["allow_insecure"] = True
        return feat

    uri = f"vless://{PROBE_UUID}@example.com:443?security=tls&type=tcp&sni=example.com#probe"
    tmpdir = tempfile.mkdtemp(prefix="feat-")
    path = os.path.join(tmpdir, "cfg.json")
    try:
        cfg = build_config(core, uri, 39999, allow_insecure=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
        ok, out = check_config(core, exe, path)
        if ok:
            feat["allow_insecure"] = True
        elif "allowinsecure" in (out or "").lower() or "pinnedpeercertsha256" in (out or "").lower():
            feat["allow_insecure"] = False
            print(f"[info] {core}：该版本已移除 allowInsecure，TLS 配置改为严格校验证书")
        else:
            feat["allow_insecure"] = True   # 其它原因失败，先按原样
    except Exception as e:  # noqa: BLE001
        feat["allow_insecure"] = True
        print(f"[warn] {core} 能力探测失败（按默认处理）：{str(e)[:60]}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return feat

CORES = {
    "v2ray": {
        "dir": "v2ray", "exe": "v2ray.exe", "kind": "json", "args": ["run", "-c"],
        "protocols": lay.CAPS["v2ray"]["protocols"], "reality": lay.CAPS["v2ray"]["reality"],
    },
    "xray": {
        "dir": "xray", "exe": "xray.exe", "kind": "json", "args": ["run", "-c"],
        "protocols": lay.CAPS["xray"]["protocols"], "reality": lay.CAPS["xray"]["reality"],
    },
    "clash": {
        # 对外叫 clash，实际内核是 mihomo
        "dir": "mihomo", "exe": "mihomo.exe", "kind": "yaml", "args": ["-f"],
        "protocols": lay.CAPS["clash"]["protocols"], "reality": lay.CAPS["clash"]["reality"],
    },
    "singbox": {
        "dir": "singbox", "exe": "sing-box.exe", "kind": "json", "args": ["run", "-c"],
        "protocols": lay.CAPS["singbox"]["protocols"], "reality": lay.CAPS["singbox"]["reality"],
    },
    "mihomo": {  # 历史别名，等价于 clash
        "dir": "mihomo", "exe": "mihomo.exe", "kind": "yaml", "args": ["-f"],
        "protocols": lay.CAPS["clash"]["protocols"], "reality": lay.CAPS["clash"]["reality"],
    },
}

PROTO_NORMALIZE = {"hy2": "hysteria2", "hysteria": "hysteria2", "shadowsocks": "ss", "ssr": "ssr"}

# 未实测过的仓库在取样时的中性可用率先验：比多数免费聚合仓库（5%-20%）乐观，
# 但不至于压过实测 30%+ 的好仓库
RATE_PRIOR = 0.25


# ---------------------------------------------------------------- 工具

def load_sub_uris(sub_file):
    """读取 base64 订阅或明文 URI 列表。"""
    with open(sub_file, "r", encoding="utf-8", errors="replace") as f:
        text = f.read().strip()
    if "://" not in text:
        decoded = c.try_b64decode(text)
        if decoded:
            text = decoded
    return [ln.strip() for ln in text.splitlines() if "://" in ln]


def node_proto(uri):
    scheme = uri.split("://")[0].lower()
    return PROTO_NORMALIZE.get(scheme, scheme)


def load_core_keys(sub_file, core):
    """取出某个内核订阅文件里**实际发布**的节点 host:port 集合。

    验证时只测「发布出去的那些节点」，不给客户端用不到的东西浪费验证时间。
    文件不存在返回 None（表示不做交集，退回按能力矩阵取样）。
    """
    if not os.path.exists(sub_file):
        return None
    fmt = lay.CORE_FMT[lay.canon(core)]
    keys = set()
    try:
        if fmt == "base64":
            for uri in load_sub_uris(sub_file):
                parsed = c.parse_uri_hostport(uri)
                if parsed:
                    keys.add(f"{parsed[1]}:{parsed[2]}")
        else:
            with open(sub_file, "r", encoding="utf-8", errors="replace") as f:
                cfg = json.load(f)
            items = cfg.get("proxies") or cfg.get("outbounds") or []
            for it in items:
                host = it.get("server")
                port = it.get("port") or it.get("server_port")
                if host and port:
                    keys.add(f"{host}:{port}")
    except (OSError, ValueError):
        return None
    return keys


def tcp_alive(host, port, timeout):
    return c.tcp_latency_ms(host, port, timeout) is not None


def tcp_prefilter(nodes, workers, timeout):
    """TCP 预筛：顺带记录握手延迟，后面的取样与排序都用这份数据。"""
    alive = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(c.tcp_latency_ms, n["host"], n["port"], timeout): n for n in nodes}
        for fut in as_completed(futures):
            node = futures[fut]
            lat = fut.result()
            if lat is not None:
                node["tcp_latency"] = lat
                alive.append(node)
    return alive


class PortAllocator:
    """为并发测试分配互不冲突的本地端口。"""

    def __init__(self, start=23000):
        self._next = start
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            for _ in range(2000):
                port = self._next
                self._next += 1
                if self._next > 48000:
                    self._next = 23000
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.bind(("127.0.0.1", port))
                        return port
                    except OSError:
                        continue
            return 0


# ---------------------------------------------------------------- 配置生成

def _v2_stream(core, allow_reality, allow_insecure, net_raw, p, security, proto):
    """按内核版本拼 v2ray/xray 的 streamSettings；该内核没有这种传输则返回 None。

    参数 p：path / host / serviceName / mode / headerType / seed / quicSecurity /
            key / sni / alpn / fp / pbk / sid / insecure
    **绝不允许退化成 tcp**：以前未识别的传输会被静默当成 tcp，节点必然连不上，
    最后被误记成「不可达」——这正是要根除的假阴性来源。
    """
    caps = lay.CAPS[lay.canon(core)]
    net = lay.canon_net(net_raw)
    if not net or net not in caps["nets"]:
        return None
    stream = {"network": net}
    if net == "ws":
        ws = {"path": p.get("path") or "/"}
        if core == "xray":
            ws["host"] = p.get("host") or ""     # Xray 26 起 host 从 headers 迁到独立字段
        elif p.get("host"):
            ws["headers"] = {"Host": p["host"]}
        stream["wsSettings"] = ws
    elif net == "http":
        stream["httpSettings"] = {"path": p.get("path") or "/",
                                  "host": [p["host"]] if p.get("host") else []}
    elif net == "grpc":
        stream["grpcSettings"] = {"serviceName": p.get("serviceName") or ""}
    elif net == "kcp":
        kcp = {"mtu": 1350, "tti": 20, "congestion": False,
               "header": {"type": p.get("headerType") or "none"}}
        if p.get("seed"):
            kcp["seed"] = p["seed"]
        stream["kcpSettings"] = kcp
    elif net == "quic":
        stream["quicSettings"] = {"security": p.get("quicSecurity") or "none",
                                  "key": p.get("key") or "",
                                  "header": {"type": p.get("headerType") or "none"}}
    elif net == "httpupgrade":
        hu = {"path": p.get("path") or "/"}
        if p.get("host"):
            hu["host"] = p["host"]
        stream["httpupgradeSettings"] = hu
    elif net == "xhttp":
        xh = {"path": p.get("path") or "/",
              "mode": p.get("mode") or ("stream-one" if (net_raw or "").lower() == "splithttp"
                                        else "auto")}
        if p.get("host"):
            xh["host"] = p["host"]
        stream["xhttpSettings"] = xh

    security = (security or "").lower()
    if security == "reality":
        pbk = p.get("pbk") or ""
        # REALITY 公钥必须是 32 字节 base64url（43 字符），否则内核直接拒绝配置
        if not allow_reality or len(pbk) != 43:
            return None
        stream["security"] = "reality"
        rs = {"serverName": p.get("sni") or "",
              "publicKey": pbk,
              "shortId": p.get("sid") or "",
              "fingerprint": p.get("fp") or "chrome"}
        stream["realitySettings"] = {k: v for k, v in rs.items() if v != ""}
    elif security in ("tls", "xtls") or proto == "trojan":
        # trojan 协议本体永远跑在 TLS 上：URI 不写 security 也必须补 TLS
        stream["security"] = "tls"
        ts = {"serverName": p.get("sni") or p.get("host") or ""}
        if p.get("alpn"):
            ts["alpn"] = p["alpn"]
        if p.get("fp"):
            ts["fingerprint"] = p["fp"]
        if allow_insecure:
            ts["allowInsecure"] = True
        stream["tlsSettings"] = ts
    return stream


def _stream_settings(uri, core, allow_reality, allow_insecure=True):
    """URI → streamSettings（v2ray/xray）。不支持返回 None。"""
    c_core = lay.canon(core)
    q = c._q(uri)
    u = urllib.parse.urlsplit(uri)
    tls = c._tls_params(q)
    p = {
        "path": q.get("path") or "/",
        "host": q.get("host") or "",
        "serviceName": q.get("serviceName") or q.get("path") or "",
        "mode": q.get("mode") or "",
        "headerType": q.get("headerType") or "",
        "seed": q.get("seed") or "",
        "quicSecurity": q.get("quicSecurity") or "",
        "key": q.get("key") or "",
        "sni": tls["sni"] or (u.hostname or ""),
        "alpn": tls["alpn"],
        "fp": tls["fp"],
        "pbk": q.get("pbk") or "",
        "sid": q.get("sid") or "",
    }
    return _v2_stream(c_core, allow_reality, allow_insecure,
                      q.get("type") or "tcp", p, q.get("security") or "",
                      lay.uri_proto(uri))


def uri_to_v2ray_outbound(uri, core, allow_reality, allow_insecure=True):
    """URI → v2ray/xray outbound 对象；该内核不支持或参数不全返回 None。"""
    core = lay.canon(core)
    low = uri.lower()
    try:
        if low.startswith("vmess://"):
            d = json.loads(c.try_b64decode(uri[8:].split("#")[0]) or "{}")
            if not d.get("add"):
                return None
            alpn = str(d.get("alpn") or "").replace(",", "/")
            p = {"path": d.get("path") or "/", "host": d.get("host") or "",
                 "serviceName": d.get("path") or "", "mode": d.get("mode") or "",
                 "headerType": d.get("type") or "", "seed": d.get("seed") or "",
                 "quicSecurity": d.get("host") or "", "key": d.get("path") or "",
                 "sni": d.get("sni") or d.get("host") or d["add"],
                 "alpn": [a for a in alpn.split("/") if a], "fp": d.get("fp") or "",
                 "pbk": d.get("pbk") or "", "sid": d.get("sid") or ""}
            tls_flag = "tls" if str(d.get("tls", "")).lower() in ("tls", "true", "1") else ""
            stream = _v2_stream(core, allow_reality, allow_insecure,
                                d.get("net") or "tcp", p, tls_flag, "vmess")
            if stream is None:
                return None
            return {
                "protocol": "vmess",
                "settings": {"vnext": [{
                    "address": d["add"], "port": int(d.get("port") or 443),
                    "users": [{"id": d.get("id", ""), "alterId": int(d.get("aid") or 0),
                               "security": d.get("scy") or "auto"}],
                }]},
                "streamSettings": stream,
            }

        u = urllib.parse.urlsplit(uri)
        q = c._q(uri)
        user = urllib.parse.unquote(u.username or "")
        if u.password:      # trojan/vless 一般没有 password 段，tuic 有
            user = f"{user}:{urllib.parse.unquote(u.password)}"
        host, port = u.hostname, u.port or 443
        if not host:
            return None

        if low.startswith("vless://"):
            if not user:
                return None
            stream = _stream_settings(uri, core, allow_reality, allow_insecure)
            if stream is None:
                return None
            user_obj = {"id": user, "encryption": "none"}
            if q.get("flow"):
                user_obj["flow"] = q["flow"]
            return {
                "protocol": "vless",
                "settings": {"vnext": [{"address": host, "port": port, "users": [user_obj]}]},
                "streamSettings": stream,
            }
        if low.startswith("trojan://"):
            if not user:
                return None
            stream = _stream_settings(uri, core, allow_reality, allow_insecure)
            if stream is None:
                return None
            return {
                "protocol": "trojan",
                "settings": {"servers": [{"address": host, "port": port, "password": user}]},
                "streamSettings": stream,
            }
        if low.startswith("ss://"):
            method, pwd, plugin = lay._ss_cred(uri)  # noqa: SLF001
            if plugin:          # v2ray/xray 都没有 ss 插件，硬生成配置只会连不上
                return None
            hp = c._ss_hostport(uri)  # noqa: SLF001
            if not hp:
                return None
            return {
                "protocol": "shadowsocks",
                "settings": {"servers": [{"address": hp[0], "port": int(hp[1]),
                                          "method": method, "password": pwd}]},
            }
        if low.startswith(("hysteria2://", "hy2://")):
            # v2fly 5.x 与 Xray 26.x 都支持 hysteria2，但装填方式完全不同：
            # - v2fly（官方 hy2.md）：protocol "hysteria2"，settings.servers 仅 address/port，
            #   密码在传输层 hy2Settings.password；不支持 salamander / 端口跳跃（会静默忽略→判不支持）
            # - Xray（v26.1.23 引入，源码 infra/conf/hysteria.go）：protocol "hysteria" + version:2，
            #   address/port 平铺在 settings，密码在传输层 hysteriaSettings.auth；支持 salamander
            #   （streamSettings.finalmask.udp）与端口跳跃（hysteriaSettings.udphop）。
            #   2026-10-25 二进制 + 源码 + xray run -test + 客户端拨号到 TLS 握手实测确认。
            if core == "v2ray":
                if q.get("obfs") or q.get("mport"):
                    return None
                tls = {"serverName": q.get("sni") or host}
                if allow_insecure:
                    tls["allowInsecure"] = True
                return {
                    "protocol": "hysteria2",
                    "settings": {"servers": [{"address": host, "port": port}]},
                    "streamSettings": {"network": "hysteria2", "security": "tls",
                                       "tlsSettings": tls,
                                       "hy2Settings": {"password": user}},
                }
            if core == "xray":
                if not user:
                    return None
                hy2 = {"version": 2, "auth": user,
                       "up": f"{q.get('up') or q.get('upmbps') or 100}mbps",
                       "down": f"{q.get('down') or q.get('downmbps') or 500}mbps"}
                mport = q.get("mport")
                if mport:
                    hop_int = q.get("mport-hop-int") or q.get("mportHopInt") or 30
                    try:
                        hy2["udphop"] = {"port": mport, "interval": int(hop_int)}
                    except (TypeError, ValueError):
                        return None
                stream = {"network": "hysteria", "hysteriaSettings": hy2, "security": "tls"}
                sni = q.get("sni") or q.get("peer") or host
                tls = {"serverName": sni}
                if allow_insecure:
                    # Xray 26 已移除 tlsSettings.allowInsecure（迁到 pinnedPeerCertSha256 /
                    # verifyPeerCertByName）；hysteria2 节点多为自签/跳过校验，用 verifyPeerCertByName
                    # 以服务名校验对端证书（等价「证书名匹配即信、不校 CA」），覆盖大多数 insecure 节点。
                    tls["verifyPeerCertByName"] = sni
                stream["tlsSettings"] = tls
                obfs = q.get("obfs")
                if obfs:
                    if obfs != "salamander":
                        return None      # 未知 obfs：不静默降级
                    obfs_pwd = q.get("obfs-password")
                    if not obfs_pwd:
                        return None
                    stream["finalmask"] = {"udp": [{"type": "salamander",
                                                    "settings": {"password": obfs_pwd}}]}
                return {
                    "protocol": "hysteria",
                    "settings": {"version": 2, "address": host, "port": port},
                    "streamSettings": stream,
                }
            return None
    except Exception:  # noqa: BLE001
        return None
    return None


def build_config(core, uri, port, allow_insecure=None):
    """为指定内核生成单节点配置对象；不支持该节点返回 None。

    生成前先过一遍能力预筛（与采集分流同一套规则），保证「生成不出来」只意味着
    「这个内核不支持这种协议/传输/加密」，而不是参数丢了导致的假不可达。
    allow_insecure=None 时按该内核的实测能力决定（见 detect_core_features）：
    Xray 26.x 起 tlsSettings.allowInsecure 被移除，写了会直接启动失败。
    """
    core = lay.canon(core)   # clash 就是 mihomo 内核
    spec = CORES[core]
    if not lay.supports(core, uri):
        return None
    if allow_insecure is None:
        allow_insecure = _CORE_FEATURES.get(core, {}).get("allow_insecure", core != "xray")
    if core in ("xray", "v2ray"):
        ob = uri_to_v2ray_outbound(uri, core, spec["reality"], allow_insecure)
        if not ob:
            return None
        return {
            "log": {"loglevel": "error"},
            "inbounds": [{"tag": "http-in", "listen": "127.0.0.1", "port": port,
                          "protocol": "http", "settings": {"timeout": 0}}],
            "outbounds": [ob],
        }
    if core == "clash":
        proxy = c.uri_to_clash(uri, "test-node")
        if not proxy:
            return None
        # 测试场景统一跳过证书校验（免费节点常用共享证书，域名与实际不符）
        proxy["skip-cert-verify"] = True
        return {
            "mixed-port": port, "allow-lan": False, "mode": "rule", "log-level": "silent",
            "proxies": [proxy],
            "proxy-groups": [{"name": "P", "type": "select", "proxies": [proxy["name"]]}],
            "rules": ["MATCH,P"],
        }
    if core == "singbox":
        ob = c.uri_to_singbox(uri, "test-node")
        if not ob:
            return None
        return {
            "log": {"level": "error"},
            "inbounds": [{"type": "http", "tag": "http-in", "listen": "127.0.0.1",
                          "listen_port": port}],
            "outbounds": [ob],
        }
    return None


# ---------------------------------------------------------------- 单节点实测

def wait_port(port, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.4):
                return True
        except OSError:
            time.sleep(0.1)
    return False


# 验证用探测地址。三个条件同时满足才算合格：出境、加密、无跳转。
#
# 1) 必须走 HTTPS（不是明文 http://）：
#    - 明文 http:// 会触发宿主系统「所有明文 HTTP 需询问」的拦截弹窗（HttpIntercept），
#      每跑一轮验证就打扰用户一次；
#    - 明文请求可被节点/中间人随意篡改，"测试通过"不可信；
#    - HTTPS 要求节点具备 CONNECT 隧道能力，与真实翻墙场景一致。
# 2) 必须用**裸域** gstatic.com（不带 www）：
#    - www.gstatic.com 解析到 120.253.253.34（国内 Google 缓存节点），本机直连就返回 204/111ms，
#      毫无区分度——国内中转节点、甚至走直连规则的节点都会被判成"可用"；
#    - gstatic.com 裸域只解析到海外 IP（142.250.196.195），本机直连 10s 超时（实测），
#      只有真正把流量送出境外才可能拿到 204，这才是我们想测的东西。
# 3) 禁止跟随重定向（见 _NoRedirect）：generate_204 正常返回 204，
#    出现 3xx 本身就说明节点不可信。
#
# 实测代价（6 个可用节点 × 4 种组合）：裸域 HTTPS 4/6 通过、耗时 0.9~16.7s；
# 而 www + 明文 http 是 6/6 通过。多出来的那两个"通过"节点，
# 实际 HTTPS 表现是连接被重置 / TLS 握手超时——现在网页全走 HTTPS，它们等于不可用。
# 所以这里筛掉的不是误杀，而是假可用。
DEFAULT_TEST_URL = "https://gstatic.com/generate_204"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """禁止跟随重定向。

    节点可以把测试请求 302/301 到任意第三方域名。若跟随，就等于我们替这个
    节点去访问了那个域名——既是安全隐患（节点能把探测流量导向任意站点），
    也会触发宿主系统「明文 HTTP 连接需确认」的拦截弹窗。
    generate_204 的正常响应是 204，出现重定向本身就说明节点不可信或不可用。
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def http_via_proxy(port, test_url, timeout):
    """通过本地 HTTP 代理取测试地址，返回 (是否可用, 延迟ms, 状态码, 错误描述)。

    错误描述带回给失败分类：内核日志常常只有一行笼统报错，
    客户端侧的 "timed out / Connection reset / SSLError" 才是可用的证据。
    """
    proxy = f"http://127.0.0.1:{port}"
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": proxy, "https": proxy}),
        _NoRedirect,
    )
    t0 = time.time()
    try:
        with opener.open(test_url, timeout=timeout) as resp:
            resp.read(512)
            code = getattr(resp, "status", 0) or 200
        # 只认 2xx：3xx 已在 _NoRedirect 处被拦下，不会走到这里
        return (200 <= code < 300), (time.time() - t0) * 1000, code, ""
    except urllib.error.HTTPError as e:
        # 3xx 被 _NoRedirect 拦下后以 HTTPError 抛出：判为不可用，且不跟随
        return False, (time.time() - t0) * 1000, e.code, f"httperror {e.code}"
    except Exception as e:  # noqa: BLE001
        return False, (time.time() - t0) * 1000, 0, f"{type(e).__name__}: {e}"


# 失败原因 → 中文标签。区分「节点不可达」和「我们自己的配置/能力不支持」，
# 后者绝不能计入不可达，否则可用率会被系统性低估。
REASON_LABELS = {
    "unsupported": "该内核不支持（协议/传输/加密/插件）",
    "config": "配置被内核拒绝（参数不符）",
    "startup": "内核启动失败或超时",
    "tls": "TLS 握手失败（证书/协议不匹配）",
    "auth": "认证失败（口令/UUID 不符）",
    "refused": "连接被拒绝",
    "reset": "连接被重置",
    "timeout": "连接超时",
    "network": "网络层失败",
    "unknown": "未知原因",
}

# 内核日志里的关键字 → 失败类别（顺序有意义：先判配置类，再判网络类）
_LOG_RULES = [
    ("config", ("unknown cipher", "unsupported method", "unknown transport",
                "unknown field", "failed to build", "invalid key", "invalid config",
                "decode config", "unmarshal", "unknown protocol", "is prohibited",
                "has been removed", "not supported", "unsupported")),
    ("tls", ("certificate", "x509", "tls handshake", "handshake failure",
             "bad record mac", "no application protocol", "tls: ", "verify",
             "ssl: ", "sslerror")),
    ("auth", ("authentication", "invalid user", "invalid uuid", "invalid password",
              "unauthorized", "bad key", "invalid request", "auth fail")),
    ("refused", ("connection refused", "actively refused", "connectex")),
    ("reset", ("reset by peer", "connection reset", "broken pipe", "eof",
               "remote end closed", "remotedisconnected", "connection aborted",
               "connectionreseterror")),
    ("timeout", ("timeout", "timed out", "deadline exceeded", "no route")),
]


def classify_failure(log_text, note=""):
    """把内核日志 / 提示归类成失败原因。日志为空时按提示兜底。"""
    low = (log_text or "").lower()
    for reason, keys in _LOG_RULES:
        if any(k in low for k in keys):
            return reason
    if "启动超时" in (note or ""):
        return "startup"
    return "network"


def _read_log(path):
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", "replace")[-4000:]
    except OSError:
        return ""


def _once(core, uri, exe, allocator, test_url, test_timeout, startup_timeout):
    """跑一次「起内核 → 请求 → 收尾」，返回 (ok, latency, note, reason, log)。"""
    spec = CORES[core]
    port = allocator.get()
    if not port:
        return False, 0, "端口分配失败", "unknown", ""
    cfg = build_config(core, uri, port)
    if not cfg:
        return False, 0, "该内核无法表达该节点", "unsupported", ""
    tmpdir = tempfile.mkdtemp(prefix=f"nt_{core}_")
    ext = ".yaml" if spec["kind"] == "yaml" else ".json"
    cfg_path = os.path.join(tmpdir, "config" + ext)
    log_path = os.path.join(tmpdir, "kernel.log")
    logf = None
    try:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)   # JSON 也是合法 YAML
        logf = open(log_path, "ab")
        proc = subprocess.Popen(
            ([exe, "-d", tmpdir, "-f", cfg_path] if core == "clash"
             else [exe] + spec["args"] + [cfg_path]),
            cwd=tmpdir, stdout=logf, stderr=logf,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception as e:  # noqa: BLE001
        if logf:
            logf.close()
        shutil.rmtree(tmpdir, ignore_errors=True)
        return False, 0, f"启动失败: {str(e)[:40]}", "startup", ""

    try:
        deadline = time.time() + startup_timeout
        up = False
        while time.time() < deadline:
            if proc.poll() is not None:       # 内核自己退了（多半是配置被拒）
                break
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.3):
                    up = True
                    break
            except OSError:
                time.sleep(0.1)
        if not up:
            log = ""
            if logf:
                logf.close()
                logf = None
            log = _read_log(log_path)
            reason = "config" if proc.poll() is not None else "startup"
            ok, out = (False, "")
            if reason == "config":
                # 用内核自己的校验命令复核：确认是配置问题，而不是节点不通
                out = check_config(core, exe, cfg_path)[1]
            return False, 0, f"内核未就绪（{REASON_LABELS[reason]}）", reason, log + out

        ok, latency, code, err = http_via_proxy(port, test_url, test_timeout)
        if ok:
            return True, latency, f"HTTP {code}", "", ""
        if logf:
            logf.flush()
        log = _read_log(log_path)
        note = f"HTTP {code} 重定向(未跟随)" if 300 <= code < 400 else (
            f"HTTP {code}" if code else "请求失败")
        return False, latency, note, classify_failure(f"{log}\n{err}", note), log
    finally:
        try:
            proc.kill()
            proc.wait(timeout=3)
        except Exception:  # noqa: BLE001
            pass
        if logf:
            logf.close()
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_one(core, uri, exe, allocator, test_url, test_timeout, startup_timeout,
             retry=1):
    """启动内核实测单个节点，返回 (是否可用, 延迟ms, 说明, 原因)。

    判定链路（保证「测不过」= 真的用不了）：
    1. 能力不支持 / 配置被内核拒绝 → 原因标 unsupported / config，**不算不可达**；
    2. 请求失败 → 抓内核日志归类（tls / auth / refused / reset / timeout）；
    3. 网络类失败再复测一次（retry），两次都失败才判不可用，排除偶发抖动。
       **但 HTTP 超时类不重试**：3s 都没应答，再等 3s 只会同样超时（实测拿昨天可用节点
       做 12s 复测，28 个 3s 判失败的里只有 2 个变可用，都是 4~5s 的慢节点），
       而每次重试要多花一个完整超时的墙钟，是夜里跑不完的主要成本之一。
    """
    core = lay.canon(core)
    last = (False, 0, "未测试", "unknown")
    for attempt in range(max(0, retry) + 1):
        ok, latency, note, reason, _log = _once(core, uri, exe, allocator,
                                                test_url, test_timeout, startup_timeout)
        if ok:
            return ok, latency, note, ""
        last = (ok, latency, note, reason)
        if reason in ("unsupported", "config"):
            break           # 结构性失败，重试没有意义
        if reason == "timeout":
            break           # 超时重试几乎必然再超时，纯烧时间（见上面 docstring）
        if attempt < retry:
            time.sleep(0.3)
    return last


def _budget_limited(nodes, args, core):
    """按墙钟预算节流取样：到期后不再提交新节点，已在跑的自然收尾。

    为什么不直接杀进程：平台对单次自动化运行有 90 分钟硬上限（`[CANCELLED] Run timed out`，
    见 known-issues 第 31 条），被强杀时 summary/pool 都不会落盘，整晚白跑。
    自己看着表收尾，损失只有「没测到的那部分」，已测的一定留得下来。
    """
    deadline = getattr(args, "_deadline", None)
    for i, n in enumerate(nodes):
        if deadline and time.time() > deadline:
            print(f"[warn] {core}：已达墙钟预算，停止提交新节点（已提交 {i}/{len(nodes)} 个）")
            return
        yield n


def test_core(core, nodes, tools_dir, workers, args, allocator):
    """对一个内核并发实测一批节点，返回 (可用结果列表, 全部实测明细)。"""
    core = lay.canon(core)
    spec = CORES[core]
    exe = os.path.join(tools_dir, spec["dir"], spec["exe"])
    if not os.path.exists(exe):
        print(f"[warn] 未找到 {core} 内核：{exe}，跳过该内核", file=sys.stderr)
        return None, []
    results, tested = [], []
    lock = threading.Lock()
    t0 = time.time()

    def worker(node):
        ok, latency, note, reason = test_one(core, node["uri"], exe, allocator,
                                            args.test_url, args.test_timeout,
                                            args.startup_timeout, args.retry)
        with lock:
            tested.append({**node, "ok": ok, "reason": reason,
                           "latency": round(latency) if ok else None})
            if ok:
                results.append({**node, "latency": round(latency), "note": note})
        if ok:
            print(f"[ok] {core} {node['proto']:<9} {node['host']}:{node['port']} {round(latency)}ms")

    # 分批提交而不是 ex.map(worker, nodes)：ThreadPoolExecutor.map 会**一次性把迭代器吃空**
    # （内部先 `[submit(...) for args in zip(*iterables)]`），预算检查会被跳过、等于没限时。
    # 按 workers*2 一块提交，每块之间重查一次表，超时最多多跑一块。
    chunk = max(workers, workers * 2)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        batch = []
        for n in _budget_limited(nodes, args, core):
            batch.append(n)
            if len(batch) >= chunk:
                list(ex.map(worker, batch))
                batch = []
        if batch:
            list(ex.map(worker, batch))
    elapsed = time.time() - t0
    unsup = sum(1 for t in tested if t["reason"] == "unsupported")
    cfg_err = sum(1 for t in tested if t["reason"] == "config")
    if len(tested) < len(nodes):
        print(f"[warn] {core}：时间预算到期，只测了 {len(tested)}/{len(nodes)} 个节点"
              f"（未测的留给下一个运行窗口，不影响已测结果落盘）")
    print(f"[info] {core} 完成：测试 {len(tested)} 个，可用 {len(results)} 个，"
          f"不支持 {unsup} 个，配置错误 {cfg_err} 个，耗时 {elapsed:.0f}s")
    return results, tested


# ---------------------------------------------------------------- 输出

def write_core_outputs(core, results, out_dir):
    """写该内核的可用节点文件 —— 每个内核只出 1 个自己客户端能直接导入的文件。

    v2ray / xray       → available_<core>.txt（base64 订阅）
    clash              → available_clash.yaml（clash 配置）
    singbox            → available_singbox.json（sing-box outbounds）
    """
    core = lay.canon(core)
    uris = [r["uri"] for r in results]
    path = lay.avail_path(out_dir, core)

    if lay.CORE_FMT[core] == "base64":
        path, n = lay.write_core_file(path, core, uris=uris)
    elif lay.CORE_FMT[core] == "clash":
        proxies, names = [], []
        for r in results:
            try:
                p = c.uri_to_clash(r["uri"], "")
            except Exception:  # noqa: BLE001
                p = None
            if not p:
                continue
            tag = c._frag(r["uri"]) or f"{r['host']}:{r['port']}"
            proxies.append(p)
            names.append(tag)
        for p, nm in zip(proxies, c.unique_names(names)):
            p["name"] = nm
        path, n = lay.write_core_file(path, core, proxies=proxies)
    else:
        outbounds = []
        for r in results:
            tag = c._frag(r["uri"]) or f"{r['host']}:{r['port']}"
            try:
                ob = c.uri_to_singbox(r["uri"], tag)
            except Exception:  # noqa: BLE001
                ob = None
            if ob:
                outbounds.append(ob)
        for ob, nm in zip(outbounds, c.unique_names([o.get("tag", "") for o in outbounds])):
            ob["tag"] = nm
        path, n = lay.write_core_file(path, core, outbounds=outbounds)
    return {"path": path, "count": n}


def write_summary(root, stats, args, date_str, tcp_total, tcp_alive, elapsed,
                  pool_notes=None, repo_stats=None, budget_skipped=None,
                  resume_skipped=None, ran_cores=None):
    """写 Docs/summary.md（按日期倒序累积的小节）+ Docs/summary.json（最新一次快照）。"""
    if not args.no_full_test:
        policy_line = (f"- 测试策略：全量——候选 ≤ {args.full_below} 个全部测试；"
                       f"超过则只测排序前 {args.max_test} 个")
    elif not args.no_escalate:
        policy_line = (f"- 测试策略：限量——每内核单轮 {args.limit} 个；"
                       f"可用数 < {args.min_available} 时追加测试"
                       f"（单内核累计上限 {'自动' if args.limit_cap <= 0 else args.limit_cap}，"
                       f"时间预算 {args.escalate_budget}s）")
    else:
        policy_line = "- 测试策略：限量——只测初始取样（--no-escalate）"
    lines = [
        f"- 预筛：TCP 连通 {tcp_alive}/{tcp_total} 个节点",
        f"- 测试地址：`{args.test_url}`，并发 {args.workers}，超时 {args.test_timeout}s（超时即判失败，不再等）",
        policy_line,
        f"- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；"
        + (f"网络类失败复测 {args.retry} 次；" if args.retry else "不复测（实测复测收益 1.7%）；")
        + "「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）",
        f"- 总耗时：{elapsed/60:.1f} 分钟",
        "",
        "| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for core, st in stats.items():
        if st is None:
            lines.append(f"| {core} | - | - | - | - | - | - | - | 内核缺失，已跳过 |")
            continue
        unsup = st.get("unsupported", 0)
        cfg_err = st.get("config_err", 0)
        dead = st["tested"] - st["ok"] - unsup - cfg_err
        base = max(1, st["tested"] - unsup - cfg_err)
        rate = f"{st['ok']/base*100:.1f}%" if st["tested"] else "-"
        if st.get("policy") == "full":
            rt = "全量" if st.get("exhausted") else f"截断（上限 {st.get('cap')}）"
        else:
            rounds = st.get("rounds", 1)
            rt = str(rounds) if rounds <= 1 else f"{rounds}（候选{'已测完' if st.get('exhausted') else '未测完'}）"
        lines.append(f"| {core} | {st['tested']} | {st['ok']} | {rate} | {unsup} | {cfg_err} | "
                     f"{dead} | {rt} | `{lay.NODES_DIR}/{lay.AVAIL_FILE[lay.canon(core)]}` |")

    # 墙钟预算收尾的说明：这**不是失败**，是主动让路给平台硬上限
    # 只报「本窗口真的跑过」的内核：合并进来的前窗口结果不该被当成这轮的截断
    _ran = set(ran_cores) if ran_cores else None
    partial_cores = [_core for _core, _st in stats.items()
                     if _st and _st.get("partial") and (_ran is None or _core in _ran)]
    if budget_skipped or partial_cores or resume_skipped:
        notes = []
        if budget_skipped:
            notes.append(f"未开始：{'、'.join(budget_skipped)}")
        if resume_skipped:
            notes.append(f"本日候选已测完、本次跳过：{'、'.join(resume_skipped)}")
        # 变量名不能叫 c：本模块顶层 `import collect_nodes as c`，函数内再绑 c 会把
        # 下方仓库质量表里的 c.quality_score 变成「字符串没有该属性」（踩过，2026-10-27）
        for _pc in partial_cores:
            notes.append(f"中途截断：{_pc}（{stats[_pc]['tested']}/{stats[_pc].get('sampled', '?')}）")
        lines += ["", "> **本轮未跑完**（墙钟预算到期主动收尾或分窗口续跑，不是失败）："
                  + "；".join(notes) + "。已测结果全部有效且已落盘，"
                  "剩余部分下次运行用 `--cores` + `--resume-tested` 接着测。"]

    # 失败原因分布：用来判断「测不过」到底是节点死了还是我们配错了
    detail_rows = []
    for core, st in stats.items():
        if not st or not st.get("reasons"):
            continue
        for reason, n in sorted(st["reasons"].items(), key=lambda kv: -kv[1]):
            detail_rows.append((core, reason, n))
    if detail_rows:
        lines += ["", "### 失败原因分布", "",
                  "「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；"
                  "只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。", "",
                  "| 代理内核 | 原因 | 数量 |", "|---|---|---|"]
        for core, reason, n in detail_rows:
            lines.append(f"| {core} | {REASON_LABELS.get(reason, reason)} | {n} |")
        lines.append("")

    # 可用节点池
    if pool_notes is not None:
        lines += ["", "### 可用节点池（跨天累积）", "",
                  "每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，"
                  "连续多天未通过则淘汰。", ""]
        lines += node_pool.summary_lines(root, list(stats.keys()), pool_notes)
        lines += ["", f"池目录：`{lay.NODES_DIR}/pool`（`pool_<core>.<ext>` 可直接导入客户端；"
                      "`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）", ""]

    # 仓库质量
    if repo_stats:
        rows = sorted(((k, v) for k, v in repo_stats.items() if v["tested"]),
                      key=lambda kv: (-kv[1]["ok"] / kv[1]["tested"], -kv[1]["ok"]))
        lines += ["", "### 仓库节点可用率（本次实测）", "",
                  "可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。", "",
                  "| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |", "|---|---|---|---|---|---|"]
        for repo, st in rows[:25]:
            rate = st["ok"] / st["tested"] if st["tested"] else 0
            avg = round(st["latency_sum"] / st["latency_n"]) if st["latency_n"] else None
            lines.append(f"| {repo} | {st['tested']} | {st['ok']} | {rate*100:.0f}% | "
                         f"{avg if avg is not None else '-'}ms | {c.quality_score(rate, avg)} |")
        if len(rows) > 25:
            lines.append(f"| … | 共 {len(rows)} 个仓库 | | | | |")
        lines.append("")

    lines += ["", "### 各内核可用节点详情", ""]
    for core, st in stats.items():
        if st is None:
            continue
        lines.append(f"#### {core}（{st['ok']} 个可用）")
        lines.append("")
        if not st["results"]:
            lines.append("无可用节点。")
            lines.append("")
            continue
        lines.append("| 节点 | 协议 | 延迟 | 来源仓库 |")
        lines.append("|---|---|---|---|")
        for r in sorted(st["results"], key=lambda x: x["latency"])[:40]:
            lines.append(f"| `{r['host']}:{r['port']}` | {r['proto']} | {r['latency']}ms | "
                         f"{r.get('repo', '') or '-'} |")
        if len(st["results"]) > 40:
            lines.append(f"| … | 共 {len(st['results'])} 个 | | |")
        lines.append("")

    path = lay.upsert_section(lay.summary_path(root), date_str,
                              lay.now_stamp().split(" ")[1], "\n".join(lines),
                              doc_title="节点可用性验证汇总（时间倒序）",
                              intro="按日期倒序累积；同一天重跑会替换当天小节")
    with open(lay.summary_json_path(root), "w", encoding="utf-8") as f:
        json.dump({"date": date_str, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "cores": {core: (None if st is None else {
                       "tested": st["tested"], "ok": st["ok"],
                       "unsupported": st.get("unsupported", 0),
                       "config_error": st.get("config_err", 0),
                       "reasons": st.get("reasons", {}),
                       "rounds": st.get("rounds", 1),
                       "min_available": st.get("min_available"),
                       "cand": st.get("cand"),
                       "exhausted": st.get("exhausted"),
                       "cap": st.get("cap"),
                       "sampled": st.get("sampled"),
                       "partial": st.get("partial", False),
                       "policy": st.get("policy"),
                       "file": lay.AVAIL_FILE[lay.canon(core)],
                       "nodes": [{"host": r["host"], "port": r["port"], "proto": r["proto"],
                                  "latency": r["latency"], "repo": r.get("repo", "")}
                                 for r in st["results"]],
                   }) for core, st in stats.items()}}, f, ensure_ascii=False, indent=1)
    if repo_stats:
        # --out 与 --input 不同时（诊断/临时目录），目标 src/ 可能还不存在，
        # 直接 open 会 FileNotFoundError 把整轮汇总写崩（实测踩过）
        os.makedirs(os.path.dirname(lay.repo_quality_path(root)), exist_ok=True)
        with open(lay.repo_quality_path(root), "w", encoding="utf-8") as f:
            json.dump({k: {**v, "avail_rate": round(v["ok"] / v["tested"], 3) if v["tested"] else 0,
                           "avg_latency": round(v["latency_sum"] / v["latency_n"]) if v["latency_n"] else None,
                           "quality": c.quality_score(v["ok"] / v["tested"] if v["tested"] else 0,
                                                      round(v["latency_sum"] / v["latency_n"]) if v["latency_n"] else None)}
                       for k, v in repo_stats.items()}, f, ensure_ascii=False, indent=1)
    return path


# ------------------------------------------------- 多窗口续跑 / 汇总累积

def load_tested_state(path, date_str):
    """当日已测记录：{date, cores: {core: ["host:port", ...]}}。

    日期不符视为空——每天采集新节点，进度不该跨天继承。读坏了也当空，
    宁可多测一遍，也不能因为状态文件损坏把候选全跳过。
    """
    state = {"date": date_str, "cores": {}}
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return state
    except Exception as exc:
        print(f"[warn] 已测记录读取失败（按空处理）：{exc}", file=sys.stderr)
        return state
    if not isinstance(d, dict) or d.get("date") != date_str:
        return state
    cores = d.get("cores")
    if isinstance(cores, dict):
        state["cores"] = {k: v for k, v in cores.items() if isinstance(v, list)}
    return state


def save_tested_state(path, state):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception as exc:
        # 写不进去只影响下次续跑，不该中断验证
        print(f"[warn] 已测记录写入失败：{exc}", file=sys.stderr)


def load_prev_cores(path, date_str):
    """同一天前几个窗口已写入的 summary.json 内核快照。

    分窗口运行时每个窗口只测一部分内核，若直接覆盖 summary.json，
    先跑完的内核会从汇总里消失（自检会当成没验证）。所以同日期要累积。
    """
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return {}
    if not isinstance(d, dict) or d.get("date") != date_str:
        return {}
    cores = d.get("cores")
    return cores if isinstance(cores, dict) else {}


def prev_stat_to_stats(st):
    """把 summary.json 里的快照还原成 write_summary 认识的内部结构。"""
    if not isinstance(st, dict):
        return None
    d = dict(st)
    d["results"] = [{"host": n.get("host"), "port": n.get("port"), "proto": n.get("proto"),
                     "latency": n.get("latency"), "repo": n.get("repo", "")}
                    for n in (st.get("nodes") or []) if isinstance(n, dict)]
    d["config_err"] = st.get("config_error", 0)
    d["tested"] = st.get("tested", 0) or 0
    d["ok"] = st.get("ok", 0) or 0
    return d


def prev_ok_results(prev_cores, core, nodes):
    """把前面窗口写进 summary 的可用节点还原成结果条目。

    summary 只存 host/port/proto/latency/repo，不存 uri；这里用本次载入的
    节点清单按 host:port 反查 uri，供写订阅文件用。查不到就丢弃（宁可少一条，
    也不能写出残缺的配置）。
    """
    st = (prev_cores or {}).get(core) or {}
    uri_map = {f"{n['host']}:{n['port']}": n["uri"] for n in nodes}
    out = []
    for n in st.get("nodes") or []:
        if not isinstance(n, dict):
            continue
        uri = uri_map.get(f"{n.get('host')}:{n.get('port')}")
        if not uri:
            continue
        out.append({"host": n["host"], "port": n["port"], "proto": n.get("proto"),
                    "latency": n.get("latency"), "repo": n.get("repo", ""), "uri": uri})
    return out


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="分代理内核验证节点可用性")
    ap.add_argument("--input", required=True, help="采集输出根目录（含 nodes_uris.txt 与四个订阅文件）")
    ap.add_argument("--out", default=None, help="验证输出目录（默认与 --input 同一个根目录）")
    ap.add_argument("--tools", default=DEFAULT_TOOLS, help="内核 bin 目录（默认 技能目录/tools/bin）")
    ap.add_argument("--cores", default=",".join(lay.CORES),
                    help="要验证的内核，逗号分隔（默认 v2ray,xray,clash,singbox）")
    ap.add_argument("--limit", type=int, default=200,
                    help="[旧模式] 每个内核单轮测试的节点数（初始取样量，也是扩量时每轮的追加量）")
    ap.add_argument("--full-below", type=int, default=FULL_BELOW,
                    help=f"[全量模式] 候选数不超过该值就全部测试（默认 {FULL_BELOW}）")
    ap.add_argument("--max-test", type=int, default=MAX_TEST,
                    help=f"[全量模式] 候选数超过 full-below 时，只测排序前这么多（默认 {MAX_TEST}）")
    ap.add_argument("--no-full-test", action="store_true",
                    help="关闭全量测试策略，回到 --limit 初始取样 + 自适应扩量模式")
    ap.add_argument("--min-available", type=int, default=MIN_AVAILABLE,
                    help=f"[旧模式] 自适应扩量阈值：可用数低于该值就继续追加测试（默认 {MIN_AVAILABLE}，0=关闭）")
    ap.add_argument("--limit-cap", type=int, default=0,
                    help="单内核累计测试上限，0=自动（--limit 的 5 倍，且不低于 min-available 的 10 倍）")
    ap.add_argument("--escalate-budget", type=int, default=1800,
                    help="单内核扩量的时间预算（秒），0=不限；默认 1800")
    ap.add_argument("--time-budget", type=int, default=0,
                    help="整轮验证的墙钟时间预算（秒），0=不限（默认）。"
                         "到期后不再提交新节点、跳过尚未开始的内核，"
                         "但已测结果照常落盘——用于平台强杀前自己优雅收尾，见 known-issues 第 36 条")
    ap.add_argument("--fair-budget", action="store_true",
                    help="把整轮墙钟预算按「尚未开始的内核数」均分（须配合 --time-budget）。"
                         "避免排在前面的内核吃满预算、后面的内核一个节点都没测，见 known-issues 第 38 条")
    ap.add_argument("--no-escalate", action="store_true", help="关闭自适应扩量，只测初始取样")
    ap.add_argument("--workers", type=int, default=24,
                    help="单内核并发测试数（默认 24）。实测同一批节点：12 并发 1.3 节点/s、"
                         "24 并发 6.2 节点/s——瓶颈是网络等待不是 CPU，4 核机器也吃得下")
    ap.add_argument("--tcp-workers", type=int, default=256,
                    help="TCP 预筛并发数（默认 256）。这里是纯 TCP 握手、无进程开销，"
                         "实测 64 并发跑 16620 个节点要 8 分钟，直接把 --time-budget 吃光")
    ap.add_argument("--tcp-timeout", type=float, default=1.5,
                    help="TCP 预筛超时（秒，默认 1.5，与采集阶段的延迟探测一致）")
    ap.add_argument("--test-timeout", type=float, default=3.0,
                    help="HTTP 验证超时（秒，默认 3.0）。实测昨天已验证可用的 80 个节点："
                         "耗时 p50=1.39s / p90=1.87s / max=2.24s，3s 只误杀 2.5%%（2/80，"
                         "都是 4~5s 才返回的慢节点）；而 12s 下 3s 判失败的 28 个里只有这 2 个变可用。"
                         "超时就判失败、不再等——每个超时节点白等 12s 是夜间跑不完的主因")
    ap.add_argument("--startup-timeout", type=float, default=6.0, help="内核启动等待（秒）")
    ap.add_argument("--retry", type=int, default=0,
                    help="网络类失败后的复测次数（默认 0，不复测）。2026-10-28 实测：3s 判失败的"
                         " 117 个节点里，放宽到 12s 重测只有 2 个变可用（1.7%%，且都是 4~5s 慢节点），"
                         "而复测一次要多花一整个超时的墙钟、吞吐直接腰斩——不值")
    ap.add_argument("--test-url", default=DEFAULT_TEST_URL,
                    help=f"验证用测试地址（默认 {DEFAULT_TEST_URL}，HTTPS）")
    ap.add_argument("--seed-file", default=None,
                    help="仓库清单路径（默认 <root>/src/seed_repos.json），用于写入仓库质量分")
    ap.add_argument("--pool-dir", default=None,
                    help="可用节点池目录（默认 <root>/pool）")
    ap.add_argument("--pool-retest", type=int, default=node_pool.DEFAULT_RETEST,
                    help="每个内核每天额外复测的池内节点数（0=不复测）")
    ap.add_argument("--pool-days", type=int, default=node_pool.DEFAULT_DAYS,
                    help="池内节点连续多少天未通过则淘汰")
    ap.add_argument("--pool-max", type=int, default=node_pool.DEFAULT_MAX, help="单内核池上限")
    ap.add_argument("--no-pool", action="store_true", help="不读写可用节点池")
    ap.add_argument("--date", default=None, help="日期标记 YYYY-MM-DD（默认今天）")
    ap.add_argument("--resume-tested", action="store_true",
                    help="多窗口续跑：跳过本日已测过的节点、只测下一批候选，"
                         "并把本次已测记录写进 nodes/tested_state.json")
    args = ap.parse_args()

    t0 = time.time()
    root = os.path.abspath(args.input)          # free-nodes 根目录：nodes/Docs/src 三个子目录
    out_dir = os.path.abspath(args.out or root)
    date_str = args.date or time.strftime("%Y-%m-%d")
    seed_file = args.seed_file or lay.seed_file_path(root)
    # 池根目录 = free-nodes 根（layout 内部会再拼 nodes/pool）。
    # 旧平铺布局时这里写的是 dirname(lay.pool_dir(root))，三分层后那样会拼出
    # nodes/nodes/pool（双拼），见 known-issues 第 33 条
    pool_root = None if args.no_pool else os.path.abspath(
        os.path.dirname(args.pool_dir) if args.pool_dir else root)

    # 采集阶段写出的延迟/来源仓库元数据：延迟用来优先取样，仓库用来算可用率
    meta = c.load_nodes_meta(root)
    uris = lay.read_uris_file(lay.uris_path(root))
    if not uris:
        # 兜底：主清单缺失时，从各内核订阅文件里合并（base64 可直接解码）
        for core in lay.CORES:
            p = lay.sub_path(root, core)
            if os.path.exists(p) and lay.CORE_FMT[core] == "base64":
                uris.extend(load_sub_uris(p))
        uris = list(dict.fromkeys(uris))
    if not uris:
        print(f"[error] 未找到任何节点清单：{lay.uris_path(root)}", file=sys.stderr)
        sys.exit(1)
    nodes, seen = [], set()
    for uri in uris:
        if uri in seen:
            continue
        seen.add(uri)
        parsed = c.parse_uri_hostport(uri)
        if not parsed:
            continue
        proto, host, port = parsed
        info = meta.get(f"{host}:{port}") or {}
        nodes.append({"uri": uri, "proto": PROTO_NORMALIZE.get(proto, proto),
                      "host": host, "port": port,
                      "repo": info.get("repo", ""),
                      "tcp_latency": info.get("tcp_latency")})
    print(f"[info] 载入 {len(uris)} 条订阅，可解析节点 {len(nodes)} 个"
          f"（带仓库归属 {sum(1 for n in nodes if n['repo'])} 个）")

    print(f"[info] TCP 预筛中（并发 {args.tcp_workers}，超时 {args.tcp_timeout}s）…")
    alive = tcp_prefilter(nodes, args.tcp_workers, args.tcp_timeout)
    print(f"[info] TCP 预筛完成：{len(alive)}/{len(nodes)} 个服务器可达")

    os.makedirs(out_dir, exist_ok=True)
    allocator = PortAllocator()
    stats, pool_notes, repo_stats = {}, {}, {}
    cores = lay.parse_cores(args.cores)
    pool_state = node_pool.load_state(pool_root) if pool_root else None
    # 墙钟预算（0 = 不限）：平台对单次运行有 90 分钟硬上限，到点直接杀进程。
    # 与其被杀，不如自己看着表收尾——没测到的留给下个窗口，测到的必须落盘
    deadline = t0 + args.time_budget if args.time_budget > 0 else None
    args._deadline = deadline
    budget_skipped = []
    resume_skipped = []
    ran_cores = []
    # 本日已测进度：**一律记录**（每个窗口都写，下个窗口才有的可续）；
    # 但「跳过已测 / 并回旧可用」只在显式 --resume-tested 时生效，不改变默认取样行为
    resume = args.resume_tested
    tested_state_path = lay.tested_state_path(root)
    tested_state = load_tested_state(tested_state_path, date_str)
    if resume:
        done_cores = {k: len(v) for k, v in tested_state["cores"].items() if v}
        if done_cores:
            print(f"[info] 续跑模式：本日已测记录 {done_cores}"
                  f"（{os.path.basename(tested_state_path)}）")
    # 分窗口运行时（22:00/23:45/01:30 各一次），每个窗口只测一部分内核。
    # 汇总必须累积同一天前面窗口的结果，否则先跑完的内核会从 summary.json 里消失
    prev_cores = load_prev_cores(lay.summary_json_path(out_dir), date_str)

    def _merge_prev():
        added = []
        for _core, _st in prev_cores.items():
            if _core in stats:
                continue
            _ps = prev_stat_to_stats(_st)
            if _ps is not None:
                stats[_core] = _ps
                added.append(_core)
        return added
    if deadline:
        print(f"[info] 时间预算 {args.time_budget}s（{time.strftime('%H:%M:%S', time.localtime(deadline))} 到点收尾）")

    # 仓库质量：取样时优先高质量仓库的节点（用户诉求：优先采/先测质量高的仓库）。
    # 用「实测可用率」排序而不是总分——总分里延迟权重会把「快但几乎全死」的仓库抬上来。
    seed_data = c.load_seed_list(seed_file)
    rate_map = {r["full_name"]: (r.get("avail_rate") if r.get("tested") else RATE_PRIOR)
                for r in seed_data.get("repos", [])}

    for ci, core in enumerate(cores):
        if core not in CORES:
            print(f"[warn] 未知内核 {core}，跳过", file=sys.stderr)
            continue
        if deadline and time.time() > deadline:
            if not ran_cores:
                # 预筛 + 采样等准备阶段就把预算吃光时，若直接跳过全部内核，整晚产物为空。
                # 至少保证跑一个内核（实测 16620 个节点、64 并发预筛要 8 分钟，
                # 会吃掉 --time-budget 的大半——并发已提到 256，这里只是兜底）
                deadline = time.time() + 180
                args._deadline = deadline
                print(f"[warn] 预算已被预筛等准备阶段耗尽，至少给 {core} 180s 跑一轮"
                      f"（否则整晚没有新产物）")
            else:
                print(f"[warn] {core}：墙钟预算已用满，跳过该内核（已完成的内核照常落盘；"
                      f"下次运行可用 --cores {core} 单独补跑）")
                budget_skipped.append(core)
                continue
        spec = CORES[core]
        # 先探测该内核当前的能力（如是否还接受 allowInsecure），避免生成无效配置
        detect_core_features(core, os.path.join(args.tools, spec["dir"], spec["exe"]))
        # 只测「该内核订阅文件里真正发布出去的节点」：能力矩阵再兜一层预筛
        keys = load_core_keys(lay.sub_path(root, core), core)
        cand = [n for n in alive
                if n["proto"] in spec["protocols"]
                and lay.supports(core, n["uri"])
                and (keys is None or f"{n['host']}:{n['port']}" in keys)]
        if keys is not None:
            print(f"[info] {core}：订阅文件 {lay.SUB_FILE[core]} 里发布 {len(keys)} 个节点，"
                  f"TCP 可达 {len(cand)} 个")
        # 按协议分桶；桶内先按仓库质量分（高→低）、再真实节点优先、最后按 TCP 延迟升序。
        # 纯按延迟取前 N 会全是 CF 任播入口（握手 20ms、代理不通），实测可用率会塌到 0。
        buckets = {}
        for n in cand:
            buckets.setdefault(n["proto"], []).append(n)
        for arr in buckets.values():
            arr.sort(key=lambda x: (-rate_map.get(x.get("repo") or "", RATE_PRIOR),
                                    c.is_cf_fronted(x["host"]),
                                    x.get("tcp_latency") is None,
                                    x.get("tcp_latency") or 0))
        cf_cand = sum(1 for n in cand if c.is_cf_fronted(n["host"]))
        if cf_cand:
            print(f"[info] {core}：候选里 {cf_cand} 个是 Cloudflare 前置节点，取样时排在最后")
        sampled, idx = [], 0
        # 先按「协议轮流交错」排出全量测试顺序：既保证协议多样性，又不偏爱低延迟死节点。
        # 初始取样取这个顺序的前 N 条；扩量时顺着同一顺序继续往后取，不重复也不跳档。
        ordered = []
        while True:
            added = False
            for proto in sorted(buckets):
                if idx < len(buckets[proto]):
                    ordered.append(buckets[proto][idx])
                    added = True
            if not added:
                break
            idx += 1
        # ── 取样策略 ──
        # 全量模式（默认）：候选 ≤ full_below 全部测；超过只测排序前 max_test 个
        # （用户要求：晚间时间空闲，节点不多就全测；过多则按上面的顺序截断到 max_test）
        if args.no_full_test:
            sampled = ordered[:min(args.limit, len(ordered))]
        elif len(ordered) <= args.full_below:
            sampled = list(ordered)
        else:
            sampled = ordered[:args.max_test]
            print(f"[info] {core}：候选 {len(ordered)} 个超过全量阈值 {args.full_below}，"
                  f"按排序截取前 {len(sampled)} 个测试")

        # 续跑（--resume-tested）：跳过本日已测过的节点，接着测排序里的下一批候选。
        # 不加这个的话，第二个窗口会从排序头部重测一遍，把 90 分钟全花在重复劳动上
        if resume:
            done = set(tested_state["cores"].get(core) or [])
            if done:
                before = len(sampled)
                kept = [n for n in sampled if f"{n['host']}:{n['port']}" not in done]
                if kept:
                    sampled = kept
                    print(f"[info] {core}：续跑跳过本日已测 {before - len(kept)} 个，"
                          f"本轮测试 {len(kept)} 个")
                else:
                    print(f"[info] {core}：本日候选已全部测过（{before} 个），"
                          f"跳过该内核（available 文件保持不变）")
                    resume_skipped.append(core)
                    continue

        # 池内节点复测：前几天验证通过、今天新鲜列表里没有的，捞回来再试一次
        pool = node_pool.load(pool_state, core) if pool_state else {"nodes": []}
        pool_added = pool_updated = pool_dropped = 0
        if pool_state and args.pool_retest > 0:
            have = {f"{n['host']}:{n['port']}" for n in sampled}
            retest = node_pool.retest_candidates(pool, have, args.pool_retest)
            if retest:
                retest_alive = tcp_prefilter(retest, args.tcp_workers, args.tcp_timeout)
                sampled.extend(retest_alive)
                print(f"[info] {core}：池内复测 {len(retest)} 个（TCP 可达 {len(retest_alive)} 个）")

        print(f"[info] {core}：候选 {len(cand)} 个，本轮测试 {len(sampled)} 个")

        # ── 公平分配墙钟（--fair-budget）──
        # 顺序跑内核时，排在前面的内核会把整窗预算吃光，后面的内核一个节点都测不到
        # （2026-10-27 首窗口实测：v2ray 吃满 2321s，xray/clash/singbox 全部「预算已用满，跳过」，
        #  三个内核当天没有任何新数据，available_* 还是前一天的旧文件）。
        # 这里把「剩余墙钟」按「本内核 + 还很后面的内核数」均分：前一个内核提前测完留下的空档，
        # 会在下一个内核开始时被重新均分吸收，不会浪费。只改「谁先测多少时间」，
        # 不改 --full-below / --max-test 的取样口径（每个内核的取样上限仍是 3000）。
        if args.fair_budget and deadline:
            left = max(1, sum(1 for _c in cores[ci:] if _c in CORES))
            remain = deadline - time.time()
            if left > 1 and remain > 0:
                share = remain / left
                args._deadline = time.time() + share
                print(f"[info] {core}：公平分配墙钟 {share:.0f}s"
                      f"（剩余 {remain / 60:.0f} 分钟 ÷ {left} 个内核）")
            else:
                args._deadline = deadline
        results, tested = test_core(core, sampled, args.tools, args.workers, args, allocator)
        if results is None:
            stats[core] = None
            continue
        ran_cores.append(core)

        # ── 自适应扩量（仅旧模式 --no-full-test）：可用数不足就继续往后追加测试 ──
        # 免费节点失效快，固定取样常常只捞到个位数可用节点。只要可用数还不到
        # min_available，就按同一取样顺序追加下一批，直到达标 / 候选耗尽 / 触顶。
        # 全量模式下初始取样就是全部（或截断到 max_test），没有「再加一批」的意义。
        total_tested = len(sampled)
        esc_rounds = 0
        cursor = len(sampled)
        if args.no_full_test:
            cap = args.limit_cap if args.limit_cap > 0 else max(args.limit * 5,
                                                                args.min_available * 10)
        else:
            cap = args.max_test
        t_core = time.time()
        while (args.no_full_test and not args.no_escalate and args.min_available > 0
               and len(results) < args.min_available):
            if cursor >= len(ordered):
                if esc_rounds:
                    print(f"[info] {core}：候选已全部测完（{total_tested} 个），"
                          f"可用 {len(results)} 个，无更多节点可加")
                break
            if total_tested >= cap:
                print(f"[warn] {core}：已测 {total_tested} 个，达到单内核上限 {cap}，"
                      f"可用仅 {len(results)} 个，停止扩量（可用 --limit-cap 调整）")
                break
            if args.escalate_budget and time.time() - t_core > args.escalate_budget:
                print(f"[warn] {core}：扩量已用 {args.escalate_budget}s 时间预算，"
                      f"已测 {total_tested} 个、可用 {len(results)} 个，停止扩量")
                break
            step = min(args.limit, cap - total_tested, len(ordered) - cursor)
            batch = ordered[cursor:cursor + step]
            cursor += step
            esc_rounds += 1
            print(f"[info] {core}：可用 {len(results)} 个 < 目标 {args.min_available} 个，"
                  f"追加第 {esc_rounds} 轮测试 {len(batch)} 个"
                  f"（累计 {total_tested + len(batch)}/{cap}，候选剩余 {len(ordered) - cursor} 个）")
            r2, t2 = test_core(core, batch, args.tools, args.workers, args, allocator)
            if r2 is None:
                break
            results.extend(r2)
            tested.extend(t2)
            total_tested += len(batch)
        if esc_rounds and len(results) >= args.min_available:
            print(f"[info] {core}：扩量达标——累计测试 {total_tested} 个，可用 {len(results)} 个")

        # 续跑（--resume-tested）：把「本日前面窗口已验证可用」的节点并回来。
        # 否则第二个窗口只测到排序尾部的差节点，会把 available 文件覆盖成更少甚至 0 条
        # （实测踩过：第二轮测 96 个全不可用，20 个可用节点被冲掉）
        win_tested, win_ok = len(tested), len(results)
        prev_ok_added = 0
        if resume:
            prev_ok = prev_ok_results(prev_cores, core, nodes)
            if prev_ok:
                results.extend(prev_ok)
                prev_ok_added = len(prev_ok)

        # 同一 server:port 只保留一条（池复测、今日取样、前面窗口的结果可能重叠）
        uniq, seen_keys = [], set()
        for r in sorted(results, key=lambda x: x.get("latency") or 99999):
            k = f"{r['host']}:{r['port']}"
            if k in seen_keys:
                continue
            seen_keys.add(k)
            uniq.append(r)
        results = uniq
        if prev_ok_added:
            print(f"[info] {core}：并入本日前面窗口已可用 {prev_ok_added} 个"
                  f"→ 本日累计可用 {len(results)} 个")

        # 进度落盘（无条件）：本窗口测过哪些节点必须留住，否则下个窗口会从排序头部重测
        keyset = set(tested_state["cores"].get(core) or [])
        keyset.update(f"{t['host']}:{t['port']}" for t in tested)
        tested_state["cores"][core] = sorted(keyset)
        save_tested_state(tested_state_path, tested_state)
        print(f"[info] {core}：本日已测记录累计 {len(keyset)} 个"
              f"（{os.path.basename(tested_state_path)}）")

        # 仓库可用率：本次实测（含失败）按来源仓库汇总，作为质量考核依据
        for t in tested:
            repo = t.get("repo") or ""
            if not repo:
                continue
            st = repo_stats.setdefault(repo, {"tested": 0, "ok": 0,
                                              "latency_sum": 0, "latency_n": 0})
            st["tested"] += 1
            if t["ok"]:
                st["ok"] += 1
                lat = t.get("latency") or t.get("tcp_latency")
                if lat:
                    st["latency_sum"] += int(lat)
                    st["latency_n"] += 1

        outs = write_core_outputs(core, results, out_dir)
        reasons = {}
        for t in tested:
            if not t["ok"]:
                reasons[t.get("reason") or "unknown"] = reasons.get(t.get("reason") or "unknown", 0) + 1
        # 续跑模式下「测试量」按本日累计算（前面窗口 + 本窗口去重后），
        # 否则汇总里的可用率会把本窗口的小分母配上本日大分子
        cum_tested = len(tested)
        if resume:
            cum_tested = len(tested_state["cores"].get(core) or []) or cum_tested
        stats[core] = {"tested": cum_tested, "ok": len(results), "results": results,
                       "rounds": 1 + esc_rounds, "min_available": args.min_available,
                       "cand": len(cand), "exhausted": cursor >= len(ordered),
                       "cap": cap, "sampled": len(sampled),
                       "partial": len(tested) < len(sampled),
                       "policy": "limited" if args.no_full_test else "full",
                       "unsupported": reasons.get("unsupported", 0),
                       "config_err": reasons.get("config", 0),
                       "reasons": reasons}
        # 只有「过完能力预筛、配置合法、网络层仍失败」的才算真不可达。
        # 用本窗口的数字算：results 里含前面窗口并回来的节点，直接相减会出负数
        unreachable = win_tested - win_ok - reasons.get("unsupported", 0) \
            - reasons.get("config", 0)
        print(f"[info] {core} 可用清单已写入 {outs['path']}（{outs['count']} 个节点）；"
              f"判定不可达 {unreachable} 个（已扣除不支持/配置错误）")

        if pool_state is not None:
            pool_added, pool_updated = node_pool.merge(pool, results, date_str)
            pool_dropped, pool_trunc = node_pool.prune(pool, date_str,
                                                       args.pool_days, args.pool_max)
            saved = node_pool.save(pool_root, core, pool, date_str, pool_state)
            pool_notes[core] = {"added": pool_added, "updated": pool_updated,
                                "dropped": pool_dropped, "truncated": pool_trunc,
                                "count": (saved or {}).get("count", 0)}
            print(f"[info] {core} 可用池：新增 {pool_added} / 刷新 {pool_updated} / "
                  f"淘汰 {pool_dropped} → 池内共 {pool_notes[core]['count']} 条"
                  f"（{os.path.basename((saved or {}).get('path') or '')}）")

        # 增量落盘：每个内核一结束就把汇总、仓库质量、共享池状态写一次。
        # 万一这轮被平台强杀，已完成的内核不会白跑，也不会留下
        # 「一个内核是新结果、其余是旧结果但 summary 还是旧数字」的混合状态
        _merge_prev()
        write_summary(out_dir, stats, args, date_str, len(nodes), len(alive),
                      time.time() - t0, pool_notes=pool_notes,
                      repo_stats=repo_stats, budget_skipped=budget_skipped,
                      resume_skipped=resume_skipped, ran_cores=ran_cores)
        if pool_state is not None:
            node_pool.save_state(pool_root, pool_state, date_str)

    # 共享状态落盘（四内核共用一份 pool_state.json）
    if pool_state is not None:
        node_pool.save_state(pool_root, pool_state, date_str)

    # 仓库质量回写动态清单（下次采集按质量分排序、跳过长期 0 可用的仓库）
    if repo_stats:
        try:
            c.update_repo_quality(seed_file, repo_stats, date_str)
            ranked = sorted(repo_stats.items(),
                            key=lambda kv: -(kv[1]["ok"] / kv[1]["tested"] if kv[1]["tested"] else 0))
            print("[info] 仓库质量已写入 " + str(seed_file) + "："
                  + "、".join(f"{k.split('/')[-1]} {v['ok']}/{v['tested']}"
                              for k, v in ranked[:6]))
        except Exception as e:  # noqa: BLE001
            print(f"[warn] 仓库质量写入失败: {e}", file=sys.stderr)

    _merge_prev()
    summary = write_summary(out_dir, stats, args, date_str, len(nodes), len(alive),
                            time.time() - t0,
                            pool_notes=(pool_notes if pool_state is not None else None),
                            repo_stats=repo_stats, budget_skipped=budget_skipped,
                            resume_skipped=resume_skipped, ran_cores=ran_cores)
    print(f"[done] 汇总报告：{summary}")
    for core, st in stats.items():
        if st:
            print(f"[done] {core}: {st['ok']}/{st['tested']} 可用 → "
                  f"{lay.AVAIL_FILE[lay.canon(core)]}")
    if pool_state is not None:
        print(f"[done] 可用节点池：{lay.pool_dir(root)}（"
              + "、".join(f"{k} {v['count']}" for k, v in pool_notes.items()) + "）")


if __name__ == "__main__":
    main()
