#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_kernels.py — 内核版本更新 + 节点处理能力变化检查

每天验证前跑一次，回答两个问题：

1. **内核有没有新版本**：查各上游 GitHub 的最新 release，和本地二进制比对。
   `--update` 时会自动下载替换（Windows amd64），并把改动写进 changelog.md。

2. **内核支持的东西有没有变**：用「一个协议 × 一种传输 × 一种加密」的样本配置，
   让内核自己做配置校验（xray/v2ray `-test`、mihomo `-t`、sing-box `check`），
   得到该内核当前真正接受的组合集合（能力指纹）。和上次的指纹对比：
   - 以前能接受、现在不接受了 → 说明本机的节点处理逻辑可能过时，记 known_issue.md
   - 新增了能接受的组合 → 记 changelog.md，并提示可以放宽 layout.CAPS

用法：
    python check_kernels.py --root <输出根目录>              # 只检查，不改任何东西
    python check_kernels.py --root <输出根目录> --update      # 有新版就下载替换
    python check_kernels.py --skip-network                   # 只做本地能力指纹

退出码：0 = 一切正常；1 = 有新版可用 / 能力有变化；2 = 检查本身失败
"""

import argparse
import base64
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import collect_nodes as c  # noqa: E402
import layout as lay  # noqa: E402
import test_nodes as t  # noqa: E402

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# 上游仓库与版本命令；配置校验命令见 test_nodes.CHECK_CMDS（会自动适配版本差异）
REPOS = {
    "xray": {"repo": "XTLS/Xray-core", "version_args": ["version"],
             "asset": ("windows", "64")},
    # 注意：v2fly 的 release 在 v2fly/v2ray-core，v2fly/v2fly-core 这个仓库名
    # 调 /releases/latest 会返回 404（2026-10-25 实测）
    "v2ray": {"repo": "v2fly/v2ray-core", "version_args": ["-version"],
              "asset": ("windows", "64")},
    "clash": {"repo": "MetaCubeX/mihomo", "version_args": ["-v"],
              "asset": ("windows", "amd64")},
    "singbox": {"repo": "SagerNet/sing-box", "version_args": ["version"],
                "asset": ("windows", "amd64")},
}

UUID = "11111111-1111-1111-1111-111111111111"
# REALITY 的 publicKey 必须是 32 字节 base64url（43 字符），随便编会让内核报 invalid public_key
REALITY_PBK = "jNXHt1yRo0vDuchQlIP6Z0ZvjT3KtzVI-T4E7RoLJS0"
STATE_FILE = "kernel_state.json"


def log(msg):
    print(msg, flush=True)


def tools_dir():
    env = os.environ.get("FREE_NODES_TOOLS")
    if env and os.path.isdir(env):
        return env
    legacy = os.path.join(os.path.dirname(SCRIPT_DIR), "tools", "bin")
    if os.path.isdir(legacy):
        return legacy
    return os.path.join(os.path.expanduser("~"), ".workbuddy", "data",
                        "free-nodes-tools", "bin")


def exe_of(core, tools):
    sub, exe = lay.CORE_BIN[lay.canon(core)]
    return os.path.join(tools, sub, exe)


# ---------------------------------------------------------------- 版本

def run(exe, args, timeout=20):
    try:
        p = subprocess.run([exe, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout,
                           creationflags=CREATE_NO_WINDOW)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except OSError as e:
        return 127, str(e)


def local_version(core, tools):
    exe = exe_of(core, tools)
    if not os.path.exists(exe):
        return None, ""
    args = REPOS[core]["version_args"]
    code, out = run(exe, args)
    if code != 0 or not out.strip():
        # 兜底：换个写法再来一次（各内核的版本命令历史上变过）
        alt = ["version"] if args != ["version"] else ["-v"]
        code, out = run(exe, alt)
    return parse_version(out), out.strip().splitlines()[0] if out.strip() else ""


def parse_version(text):
    m = re.search(r"\bv?(\d+\.\d+(?:\.\d+)?(?:[-.\w]*)?)", text or "")
    return m.group(1) if m else None


def ver_key(v):
    """把版本号变成可比较的元组（1.8.24 → (1,8,24)）。"""
    if not v:
        return ()
    parts = re.findall(r"\d+", v)
    return tuple(int(x) for x in parts[:3])


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "free-nodes-collector"})
    with urllib.request.urlopen(req, timeout=timeout, context=c._NOVERIFY_CTX) as r:  # noqa: SLF001
        return json.loads(r.read().decode("utf-8", "replace"))


def latest_release(core, proxy=None):
    url = f"https://api.github.com/repos/{REPOS[core]['repo']}/releases/latest"
    try:
        d = http_json(url)
    except Exception as e:  # noqa: BLE001
        return None, f"查询失败：{str(e)[:80]}"
    tag = d.get("tag_name") or d.get("name") or ""
    return {"version": parse_version(tag) or tag, "tag": tag,
            "assets": [(a.get("name", ""), a.get("browser_download_url", ""))
                       for a in d.get("assets", [])]}, ""


def pick_asset(core, assets):
    want = REPOS[core]["asset"]
    cands = []
    for name, url in assets:
        low = name.lower()
        if not low.endswith(".zip") or want[0] not in low or want[1] not in low:
            continue
        if "arm" in low or "386" in low:   # 只装 amd64
            continue
        cands.append((len(low), name, url))
    if not cands:
        return None, None
    cands.sort()
    return cands[0][1], cands[0][2]


def download(url, dest, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "free-nodes-collector"})
    with urllib.request.urlopen(req, timeout=timeout, context=c._NOVERIFY_CTX) as r, \
            open(dest, "wb") as f:  # noqa: SLF001
        shutil.copyfileobj(r, f)
    return dest


def install_from_zip(core, zip_path, tools):
    sub, exe_name = lay.CORE_BIN[lay.canon(core)]
    target_dir = os.path.join(tools, sub)
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        member = None
        for n in z.namelist():
            if os.path.basename(n).lower() == exe_name.lower():
                member = n
                break
        if not member:
            return None, "压缩包里没有 " + exe_name
        tmp_exe = os.path.join(target_dir, exe_name + ".new")
        with z.open(member) as src, open(tmp_exe, "wb") as dst:
            shutil.copyfileobj(src, dst)
    target = os.path.join(target_dir, exe_name)
    if os.path.exists(target):
        try:
            shutil.copy2(target, target + ".bak")
        except OSError:
            pass
    os.replace(tmp_exe, target)
    return target, ""


# ---------------------------------------------------------------- 能力指纹

def sample_uris(core):
    """构造该内核「应该支持」的样本节点：协议 × 传输 × 加密 组合。"""
    core = lay.canon(core)
    caps = lay.CAPS[core]
    samples = []
    transports = [x for x in ("tcp", "ws", "grpc") if x in caps["nets"]]

    for net in transports:
        q = f"type={net}&security=tls&sni=example.com"
        if net == "ws":
            q += "&path=%2Fws&host=example.com"
        if net == "grpc":
            q += "&serviceName=gs"
        if "vless" in caps["protocols"]:
            samples.append(("vless", net, "tls",
                            f"vless://{UUID}@example.com:443?{q}#t-{net}"))
        if "trojan" in caps["protocols"]:
            samples.append(("trojan", net, "tls",
                            f"trojan://pw@example.com:443?{q}#t-{net}"))
        if "vmess" in caps["protocols"]:
            samples.append(("vmess", net, "tls", _vmess_uri(net)))
    if "ss" in caps["protocols"]:
        samples.append(("ss", "-", "-",
                        "ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@example.com:8388#ss"))
    if caps["reality"]:
        samples.append(("vless", "tcp", "reality",
                        f"vless://{UUID}@example.com:443?security=reality&pbk={REALITY_PBK}"
                        f"&sid=01&fp=chrome&sni=example.com&type=tcp#reality"))
    if caps["flow"]:
        samples.append(("vless", "tcp", "vision",
                        f"vless://{UUID}@example.com:443?security=tls&type=tcp"
                        f"&flow=xtls-rprx-vision&sni=example.com#vision"))
    if "hysteria2" in caps["protocols"]:
        samples.append(("hysteria2", "-", "tls",
                        "hysteria2://pw@example.com:443?sni=example.com&insecure=1#hy2"))
    if "tuic" in caps["protocols"]:
        samples.append(("tuic", "-", "tls",
                        f"tuic://{UUID}:pw@example.com:443?sni=example.com&congestion_control=bbr#tuic"))
    return samples


def _vmess_uri(net="tcp"):
    """生成一条 vmess 样本 URI（vmess 用 base64 JSON 表示）。"""
    obj = {"v": "2", "ps": f"t-{net}", "add": "example.com", "port": "443",
           "id": UUID, "aid": "0", "net": net, "type": "none",
           "host": "example.com", "path": "/ws", "tls": "tls"}
    raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    return "vmess://" + base64.b64encode(raw).decode("ascii")


def probe_capabilities(core, tools):
    """让内核自己校验样本配置，返回 (accepted, rejected, err)。标签如 vless/ws/tls。"""
    core = lay.canon(core)
    exe = exe_of(core, tools)
    if not os.path.exists(exe):
        return None, None, "内核不存在"
    t.detect_core_features(core, exe)   # 先按该内核版本调整 TLS 写法
    accepted, rejected = set(), set()
    allocator = t.PortAllocator(31000)
    kind = lay.CORE_FMT[core]

    for proto, net, sec, uri in sample_uris(core):
        label = f"{proto}/{net}/{sec}"
        port = allocator.get()
        tmpdir = tempfile.mkdtemp(prefix="knl-")
        path = os.path.join(tmpdir, "cfg.yaml" if kind == "clash" else "cfg.json")
        try:
            cfg = t.build_config(core, uri, port)
            if not cfg:
                rejected.add(label)
                continue
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=1)
            ok, out = t.check_config(core, exe, path)
            if ok:
                accepted.add(label)
            else:
                rejected.add(label)
                first = (out or "").strip().splitlines()
                log(f"[info] {core} {label} 未被接受：{first[-1][:110] if first else ''}")
        except Exception as e:  # noqa: BLE001
            rejected.add(label)
            log(f"[warn] {core} 样本 {label} 生成/校验异常：{str(e)[:80]}")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    return accepted, rejected, ""


def load_state(root):
    path = lay.kernel_state_path(root)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(root, state):
    path = lay.kernel_state_path(root)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=1)
    except OSError as e:
        log(f"[warn] 内核状态写入失败：{e}")


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="内核版本与能力变化检查")
    ap.add_argument("--root", default="free-nodes", help="输出根目录（写 changelog/known_issue）")
    ap.add_argument("--tools", default=None, help="内核 bin 目录")
    ap.add_argument("--update", action="store_true", help="有新版本就自动下载替换")
    ap.add_argument("--skip-network", action="store_true", help="不查上游版本（只做本地能力指纹）")
    ap.add_argument("--date", default=None, help="日期标记 YYYY-MM-DD")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    tools = args.tools or tools_dir()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    state = load_state(root)
    state.setdefault("cores", {})
    changed, notes = [], []
    need = False

    for core in lay.CORES:
        info = REPOS[core]
        exe = exe_of(core, tools)
        local_v, local_line = local_version(core, tools)
        log(f"[{core}] 本地：{local_line or '未安装'}"
            + (f"（版本 {local_v}）" if local_v else ""))

        # 1) 版本检查
        if not args.skip_network:
            latest, err = latest_release(core)
            if err:
                notes.append(f"{core} 版本查询失败：{err}")
                log(f"[{core}] {err}")
            elif latest:
                newer = ver_key(latest["version"]) > ver_key(local_v or "")
                log(f"[{core}] 上游最新：{latest['version']}"
                    + ("（有新版）" if newer else "（已是最新）"))
                if newer:
                    need = True
                    name, url = pick_asset(core, latest["assets"])
                    if not args.update:
                        notes.append(f"{core} 有新版本 {latest['version']}（本地 {local_v}），"
                                     f"可用 --update 自动升级")
                    elif not url:
                        notes.append(f"{core} 新版 {latest['version']} 没找到 Windows amd64 资产")
                    else:
                        log(f"[{core}] 下载 {name} …")
                        try:
                            with tempfile.TemporaryDirectory() as td:
                                zp = download(url, os.path.join(td, name))
                                target, err2 = install_from_zip(core, zp, tools)
                            if err2:
                                notes.append(f"{core} 升级失败：{err2}")
                            else:
                                new_v, new_line = local_version(core, tools)
                                changed.append(f"{core} 内核升级 {local_v} → {new_v}"
                                               f"（{new_line}）")
                                log(f"[{core}] 已升级到 {new_v}")
                        except Exception as e:  # noqa: BLE001
                            notes.append(f"{core} 下载/安装失败：{str(e)[:100]}")
                            log(f"[{core}] 下载失败：{str(e)[:100]}")

        # 2) 能力指纹
        accepted, rejected, err = probe_capabilities(core, tools)
        if accepted is None:
            log(f"[{core}] 跳过能力检查：{err}")
            continue
        prev = state["cores"].get(core) or {}
        prev_acc = set(prev.get("accepted") or [])
        now_v, _ = local_version(core, tools)
        state["cores"][core] = {"version": now_v, "checked": date_str,
                                "accepted": sorted(accepted),
                                "rejected": sorted(rejected)}
        log(f"[{core}] 能力指纹：接受 {len(accepted)} 项、拒绝 {len(rejected)} 项"
            + (f"（上次 {len(prev_acc)} 项）" if prev_acc else "（首次建立基线）"))
        if prev_acc:
            lost = sorted(prev_acc - accepted)
            gained = sorted(accepted - prev_acc)
            if lost:
                need = True
                notes.append(f"{core} 不再接受：{'、'.join(lost)}"
                             "（内核行为变了，需要更新节点处理逻辑 / layout.CAPS）")
            if gained:
                changed.append(f"{core} 新增支持：{'、'.join(gained)}（可考虑放宽 layout.CAPS）")
        expected = {f"{p}/{n}/{s}" for p, n, s, _u in sample_uris(core)}
        unexpected = sorted(expected - accepted)
        if unexpected:
            notes.append(f"{core} 本应支持却被拒绝：{'、'.join(unexpected[:6])}"
                         "（配置生成可能不兼容该内核版本，见 known-issues 第 4 条）")

    save_state(root, state)

    # 3) 落盘：changelog + known_issue
    # 标题固定（不带分钟）：同一天多跑几次只保留最新一份，不会堆出一串碎片小节
    if changed:
        lay.append_changelog(root, date_str, "内核检查与升级",
                             "\n".join(f"- {x}" for x in changed))
    if notes:
        lay.append_issue(root, date_str, "内核检查发现",
                         "\n".join(f"- {x}" for x in notes))

    log("")
    if changed:
        log("[done] 已更新：\n  - " + "\n  - ".join(changed))
    if notes:
        log("[warn] 需要关注：\n  - " + "\n  - ".join(notes))
    if not changed and not notes:
        log("[done] 内核均为最新，能力指纹无变化")
    return 1 if need else 0


if __name__ == "__main__":
    sys.exit(main())
