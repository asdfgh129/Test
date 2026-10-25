#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""uplink.py — 用已采集/已验证的免费节点自建本地代理，作为访问 GitHub 的上行通道。

背景：部分网络环境里 api.github.com / codeload.github.com 可直连，但 github.com:443
被重置，导致 git push 与网页采集全部失败。既然本机本来就有四个代理内核和一堆已实测
可用的节点，最自然的做法是：拿一个可用节点，起一个本地代理内核，让 GitHub 流量走它。

对外接口：
    up = uplink.start(pool_dir=..., extra_dirs=[...])   # 起一个可用上行通道，失败返回 None
    uplink.set_proxy_env(up.url)                        # 让 urllib / git 走它
    uplink.stop(up)                                     # 用完必须停掉，避免占用端口干扰验证

    mode, up = uplink.ensure(...)                       # 代理 → 直连 → 等待重试 的完整兜底链

候选节点来源（按可靠性排序）：
1. nodes/pool/pool_<core>.<ext> —— 历史上实测通过的节点（ok_count 高、best_latency 低优先）
2. nodes/available_<core>.<ext> —— 最近实测通过
3. nodes/nodes_uris.txt —— 还没验证过的原始节点，兜底
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import collect_nodes as c  # noqa: E402
import layout as lay  # noqa: E402
import test_nodes as t  # noqa: E402

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# 内核尝试顺序：clash(mihomo) / sing-box 协议覆盖最全，先把它们用掉
CORE_ORDER = ["clash", "singbox", "xray", "v2ray"]

# 判定「这条上行通道真的能到 GitHub」的探测地址。
# github.com 是 git push 的实际目标（git smart http 就走它），api.github.com 用来确认 API 也通。
DEFAULT_PROBES = ["https://github.com/", "https://api.github.com/rate_limit"]

DEFAULT_TOOLS = t.DEFAULT_TOOLS


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------- 候选节点

def _read_uri_list(path):
    """读取明文 URI 列表或 base64 订阅。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read().strip()
    except OSError:
        return []
    if "://" not in text:
        decoded = c.try_b64decode(text)
        if decoded:
            text = decoded
    return [ln.strip() for ln in text.splitlines() if "://" in ln]


def _pool_nodes(root, per_core):
    """池内节点：按 (通过次数降序, 最佳延迟升序) 取前 N 个，带上来源内核。"""
    out = []
    if not root:
        return out
    try:
        import pool as node_pool
        nodes = node_pool.all_uris(root)
    except Exception as e:  # noqa: BLE001
        log(f"[uplink] 读取节点池失败：{e}")
        return out
    used = {}
    for n in nodes:
        core = lay.canon(n.get("core") or "")
        if used.get(core, 0) >= per_core:
            continue
        used[core] = used.get(core, 0) + 1
        out.append({"uri": n["uri"], "proto": n.get("proto", ""), "host": "", "port": 0,
                    "core_hint": core, "ok_count": n.get("ok_count", 0),
                    "best_latency": n.get("latency"),
                    "source": f"pool/{core}"})
    return out


def _dir_nodes(root, cores, per_dir=8):
    """已发布的可用清单优先（每个内核 1 个文件），内部主清单兜底。

    clash / sing-box 的清单是 yaml/json，反解 URI 不划算，它们的节点由池状态覆盖。
    """
    out = []
    if not root:
        return out
    for core in cores:
        core = lay.canon(core)
        f = lay.avail_path(root, core)
        if lay.CORE_FMT.get(core) != "base64" or not os.path.exists(f):
            continue
        for uri in _read_uri_list(f)[:per_dir]:
            out.append({"uri": uri, "proto": "", "host": "", "port": 0,
                        "core_hint": core, "ok_count": 0, "best_latency": None,
                        "source": f"available_{core}"})
    for uri in lay.read_uris_file(lay.uris_path(root))[:per_dir]:
        out.append({"uri": uri, "proto": "", "host": "", "port": 0,
                    "core_hint": "", "ok_count": 0, "best_latency": None,
                    "source": "nodes_uris"})
    return out


def candidates(root=None, cores=None, per_core=10, limit=40):
    """汇总候选节点，按 URI 去重，池内高质量节点排最前。"""
    cores = [lay.canon(x) for x in (cores or CORE_ORDER)]
    seen, out = set(), []
    for n in _pool_nodes(root, per_core) + _dir_nodes(root, cores):
        uri = n["uri"].strip()
        if not uri or uri in seen:
            continue
        parsed = c.parse_uri_hostport(uri)
        if parsed:
            n["proto"], n["host"], n["port"] = parsed
        seen.add(uri)
        out.append(n)
        if len(out) >= limit:
            break
    return out


def _cores_for(node):
    """节点该用哪些内核实测：池来源内核优先，其余按协议兼容性排序。"""
    proto = (node.get("proto") or "").lower()
    order = []
    if node.get("core_hint"):
        order.append(lay.canon(node["core_hint"]))
    for core in CORE_ORDER:
        if core in order:
            continue
        if proto and proto not in t.CORES[core]["protocols"]:
            continue
        order.append(core)
    return order


# ---------------------------------------------------------------- 起停内核

class Uplink:
    """一个正在运行的本地代理通道。"""

    def __init__(self, port, core, uri, proc, tmpdir):
        self.port = port
        self.core = core
        self.uri = uri
        self.proc = proc
        self.tmpdir = tmpdir

    @property
    def url(self):
        return f"http://127.0.0.1:{self.port}"

    def describe(self):
        parsed = c.parse_uri_hostport(self.uri) or ("", "", 0)
        return f"{self.core} @ {parsed[1]}:{parsed[2]}（本地 {self.url}）"


def _free_port(start=26000):
    for port in range(start, start + 500):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return 0


def _probe(port, urls, timeout):
    """逐个探测：能拿到 2xx 才算这条通道可用。"""
    for url in urls:
        ok, latency, code, _err = t.http_via_proxy(port, url, timeout)
        if ok:
            return True, url, latency
    return False, "", 0


def build_one(core, uri, tools_dir=None, probes=None, probe_timeout=15,
              startup_timeout=6):
    """用单个节点起一个内核，探测通过则返回 Uplink（保持运行），否则清理并返回 None。"""
    tools_dir = tools_dir or DEFAULT_TOOLS
    probes = probes or DEFAULT_PROBES
    spec = t.CORES.get(core)
    if not spec:
        return None
    exe = os.path.join(tools_dir, spec["dir"], spec["exe"])
    if not os.path.exists(exe):
        return None
    port = _free_port()
    if not port:
        return None
    cfg = t.build_config(core, uri, port)
    if not cfg:
        return None
    tmpdir = tempfile.mkdtemp(prefix=f"up_{core}_")
    ext = ".yaml" if spec["kind"] == "yaml" else ".json"
    cfg_path = os.path.join(tmpdir, "config" + ext)
    proc = None
    try:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        proc = subprocess.Popen(
            ([exe, "-d", tmpdir, "-f", cfg_path] if core == "mihomo"
             else [exe] + spec["args"] + [cfg_path]),
            cwd=tmpdir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
        )
        if not t.wait_port(port, startup_timeout):
            raise RuntimeError("内核启动超时")
        ok, url, latency = _probe(port, probes, probe_timeout)
        if not ok:
            raise RuntimeError("探测失败")
        up = Uplink(port, core, uri, proc, tmpdir)
        log(f"[uplink] 通道就绪：{up.describe()}，{url} {round(latency)}ms")
        return up
    except Exception as e:  # noqa: BLE001
        if proc is not None:
            try:
                proc.kill()
                proc.wait(timeout=3)
            except Exception:  # noqa: BLE001
                pass
        _cleanup(tmpdir)
        log(f"[uplink] {core} 起核失败：{str(e)[:60]}")
        return None


def _cleanup(tmpdir):
    if not tmpdir:
        return
    try:
        for name in os.listdir(tmpdir):
            p = os.path.join(tmpdir, name)
            try:
                os.remove(p)
            except OSError:
                pass
        os.rmdir(tmpdir)
    except OSError:
        pass


def stop(up):
    """停掉上行通道（采集/推送结束后必须调用，避免端口与内核残留）。"""
    if not up:
        return
    try:
        up.proc.kill()
        up.proc.wait(timeout=3)
    except Exception:  # noqa: BLE001
        pass
    _cleanup(up.tmpdir)
    log(f"[uplink] 已停止通道 {up.core}（{up.url}）")


def start(root=None, cores=None, tools_dir=None, probes=None,
          max_candidates=40, probe_timeout=15, startup_timeout=6, prefilter=True,
          skip=()):
    """按候选顺序逐条起核试连，第一个通的就用它。全部失败返回 None。

    skip：本轮已经试过的节点 URI 集合（推送阶段「通了但 git 还是失败」时要换一批节点）。
    """
    cand = candidates(root=root, cores=cores, limit=max_candidates + len(skip))
    if skip:
        cand = [n for n in cand if n["uri"] not in skip]
    cand = cand[:max_candidates] if max_candidates else cand
    if not cand:
        log("[uplink] 没有可用候选节点（池与近期清单都为空，或候选都已试过）")
        return None
    log(f"[uplink] 候选节点 {len(cand)} 个，开始逐条试连 GitHub …")

    # TCP 预筛：连服务器都连不上的直接跳过，省掉起核的 2-6 秒
    if prefilter:
        alive = []
        for n in cand:
            if n.get("host") and n.get("port"):
                if c.tcp_latency_ms(n["host"], n["port"], 2.0) is None:
                    continue
            alive.append(n)
        if alive:
            log(f"[uplink] TCP 预筛后剩 {len(alive)} 个候选")
            cand = alive

    tried = 0
    for node in cand:
        for core in _cores_for(node):
            tried += 1
            up = build_one(core, node["uri"], tools_dir, probes, probe_timeout, startup_timeout)
            if up:
                log(f"[uplink] 第 {tried} 次尝试命中（来源 {node.get('source', '?')}）")
                return up
            if tried >= max_candidates:
                return None
    log(f"[uplink] {tried} 次尝试全部失败，未能建立可用通道")
    return None


# ---------------------------------------------------------------- 环境接入

_ENV_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy")


def set_proxy_env(url):
    """让 urllib / requests / git 默认走这个代理；url 为空则清空代理变量。"""
    for k in _ENV_KEYS:
        if url:
            os.environ[k] = url
        else:
            os.environ.pop(k, None)


def install_opener(url):
    """把全局 opener 换成带代理的（collect_nodes 里带 context 的调用另有 env 兜底）。"""
    if url:
        handler = urllib.request.ProxyHandler({"http": url, "https": url})
    else:
        handler = urllib.request.ProxyHandler({})  # 空字典 = 强制直连，忽略 env
    urllib.request.install_opener(urllib.request.build_opener(handler))


def direct_ok(probes=None, timeout=12):
    """直连能否访问 GitHub（临时屏蔽代理环境变量后实测），任一探测地址通即算通。"""
    probes = probes or DEFAULT_PROBES
    saved = {k: os.environ.get(k) for k in _ENV_KEYS}
    set_proxy_env("")
    old_opener = urllib.request._opener  # noqa: SLF001
    passed, failed = [], []
    try:
        install_opener("")
        for url in probes:
            ok = False
            try:
                with urllib.request.urlopen(url, timeout=timeout,
                                            context=c._NOVERIFY_CTX) as resp:  # noqa: SLF001
                    ok = 200 <= resp.status < 400
            except urllib.error.HTTPError as e:
                ok = 200 <= e.code < 400
            except Exception:  # noqa: BLE001
                ok = False
            (passed if ok else failed).append(url)
        if passed:
            log(f"[uplink] 直连可达：{'、'.join(passed)}")
        if failed:
            log(f"[uplink] 直连不可达：{'、'.join(failed)}"
                + ("（采集可继续，但 git push 需要能到 github.com，建议保留自建代理）"
                   if any("github.com/" in u for u in failed) else ""))
        return bool(passed)
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
        urllib.request._opener = old_opener  # noqa: SLF001


# ---------------------------------------------------------------- 兜底链

def ensure(root=None, cores=None, tools_dir=None, probes=None,
           retries=2, retry_wait=600, allow_direct=True, max_candidates=40, skip=()):
    """建立上行通道：先自建代理 → 代理不可用则直连 → 直连也不通就等 retry_wait 秒重试。

    root：扁平输出根目录（池 + 已发布的可用清单都在这里），用来自选候选节点。
    返回 (mode, uplink)：mode ∈ {"proxy", "direct", "none"}；mode=proxy 时 uplink 非空，
    调用方用完后必须 uplink.stop(up)。
    """
    for attempt in range(retries + 1):
        if attempt:
            log(f"[uplink] 等待 {retry_wait} 秒后重试（第 {attempt}/{retries} 次重试）…")
            time.sleep(retry_wait)
        up = start(root=root, cores=cores,
                   tools_dir=tools_dir, probes=probes, max_candidates=max_candidates,
                   skip=skip)
        if up:
            set_proxy_env(up.url)
            install_opener(up.url)
            return "proxy", up
        if allow_direct and direct_ok(probes):
            log("[uplink] 代理不可用，但 GitHub 可直连，改用直连")
            set_proxy_env("")
            install_opener("")
            return "direct", None
        log("[uplink] 代理与直连都不可用")
    set_proxy_env("")
    install_opener("")
    return "none", None


if __name__ == "__main__":
    # 自测：尝试建立一条上行通道，成功后打印并立刻停掉
    ap_args = sys.argv[1:]
    root = ap_args[0] if ap_args else None
    up = start(root=root)
    if up:
        log(f"[selftest] 通道可用：{up.url}")
        stop(up)
        sys.exit(0)
    log("[selftest] 未能建立通道")
    sys.exit(1)
