#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pool.py — 按内核的跨天「可用节点池」

布局（与验证产物同一套命名，见 layout.py）：
    <root>/pool/pool_v2ray.txt        base64 订阅
    <root>/pool/pool_xray.txt         base64 订阅
    <root>/pool/pool_clash.yaml       clash 配置
    <root>/pool/pool_singbox.json     sing-box 配置
    <root>/pool/pool_state.json       四内核共用的元数据（首见/最近通过/通过次数/最佳延迟）

设计要点：
- 每个内核**只对外 1 个池文件**（客户端能直接导入），不再同时写 txt/json/list 三份
- 元数据集中放在 pool_state.json：这是「复测优先级 / 淘汰策略」的依据，不是节点列表的复制
- 节点身份用 host:port，同一服务器换参数不会重复入池
- 每次实测通过的刷新 last_ok / ok_count / best_latency；连续多天未通过则淘汰
- 池内节点每天参与复测（少量配额），仍然可用的直接复用，避免「一天没采到就全丢」
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as lay

VERSION = 2
DEFAULT_DAYS = 14          # 超过这么多天没再验证通过就淘汰
DEFAULT_MAX = 3000         # 单内核池上限
DEFAULT_RETEST = 40        # 每内核每天复测的池内节点数

LEGACY_PREFIX = "pool_"     # 旧版的 pool_<core>.json / .txt / _list.txt


def node_key(host, port):
    return f"{host}:{port}"


# ---------------------------------------------------------------- 共享状态

def _empty_state():
    return {"version": VERSION, "updated": "", "cores": {}}


def load_state(root):
    """读共享状态；顺便把旧版「每内核一个 json」迁移进来（只迁移，不删除旧文件）。"""
    state = _empty_state()
    path = lay.pool_state_path(root)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                got = json.load(f)
            if isinstance(got, dict) and isinstance(got.get("cores"), dict):
                state.update(got)
        except (OSError, ValueError):
            pass
    # 迁移旧数据（池目录 = nodes/pool，见 layout.pool_dir）
    pdir = lay.pool_dir(root)
    for fname in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if not (fname.startswith(LEGACY_PREFIX) and fname.endswith(".json")):
            continue
        core = lay.canon(fname[len(LEGACY_PREFIX):-5])
        if core in lay.CORES and core not in state["cores"]:
            try:
                with open(os.path.join(pdir, fname), "r", encoding="utf-8") as f:
                    old = json.load(f)
                if isinstance(old, dict) and isinstance(old.get("nodes"), list):
                    state["cores"][core] = {"nodes": old["nodes"],
                                            "updated": old.get("updated", "")}
                    print(f"[info] 已从旧格式迁移节点池：{fname} → pool_state.json（{core}）")
            except (OSError, ValueError):
                continue
    return state


def save_state(root, state, date_str):
    state["version"] = VERSION
    state["updated"] = date_str
    path = lay.pool_state_path(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=1)
        return path
    except OSError as e:
        print(f"[warn] 节点池状态写入失败: {e}", file=sys.stderr)
        return None


def load(state, core):
    """取某内核的池（结构 {"core","nodes"}）。"""
    core = lay.canon(core)
    got = (state.get("cores") or {}).get(core) or {}
    return {"core": core, "version": VERSION,
            "updated": got.get("updated", ""),
            "nodes": list(got.get("nodes") or [])}


# ---------------------------------------------------------------- 合并 / 淘汰

def merge(pool, results, date_str):
    """把本次实测可用的节点并入池。返回 (新增数, 更新数)。"""
    idx = {n.get("key"): n for n in pool.get("nodes", []) if n.get("key")}
    added = updated = 0
    for r in results:
        host, port = r.get("host"), int(r.get("port") or 0)
        if not host or not port:
            continue
        k = node_key(host, port)
        lat = r.get("latency")
        lat = int(lat) if isinstance(lat, (int, float)) and lat > 0 else None
        entry = idx.get(k)
        if entry is None:
            entry = {
                "key": k, "host": host, "port": port,
                "uri": r.get("uri", ""), "proto": r.get("proto", ""),
                "repo": r.get("repo", ""),
                "first_seen": date_str, "last_ok": date_str,
                "ok_count": 1, "best_latency": lat, "last_latency": lat,
            }
            pool.setdefault("nodes", []).append(entry)
            idx[k] = entry
            added += 1
        else:
            entry["uri"] = r.get("uri") or entry.get("uri", "")
            entry["proto"] = r.get("proto") or entry.get("proto", "")
            entry["repo"] = r.get("repo") or entry.get("repo", "")
            entry["last_ok"] = date_str
            entry["ok_count"] = int(entry.get("ok_count") or 0) + 1
            entry["last_latency"] = lat
            if lat is not None:
                best = entry.get("best_latency")
                entry["best_latency"] = lat if best is None else min(best, lat)
            updated += 1
    return added, updated


def prune(pool, today, days=DEFAULT_DAYS, max_nodes=DEFAULT_MAX):
    """淘汰太久没验证通过的节点，并按「通过次数 + 延迟」截断到上限。"""
    from datetime import datetime, timedelta
    try:
        cutoff = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=days)).strftime("%Y-%m-%d")
    except ValueError:
        cutoff = ""
    before = len(pool.get("nodes", []))
    keep = [n for n in pool.get("nodes", [])
            if n.get("key") and n.get("uri") and (n.get("last_ok") or "") >= cutoff]
    keep.sort(key=lambda n: (-(n.get("ok_count") or 0),
                             1 if n.get("best_latency") is None else 0,
                             n.get("best_latency") or 0))
    truncated = 0
    if max_nodes and len(keep) > max_nodes:
        truncated = len(keep) - max_nodes
        keep = keep[:max_nodes]
    pool["nodes"] = keep
    return before - len(keep) - truncated, truncated


# ---------------------------------------------------------------- 写池文件

def _write_pool_file(root, core, uris):
    """按内核原生格式写池文件：v2ray/xray → base64；clash → yaml；singbox → json。"""
    core = lay.canon(core)
    path = lay.pool_path(root, core)
    uris = [u for u in uris if u]
    if lay.CORE_FMT[core] == "base64":
        return lay.write_core_file(path, core, uris=uris)

    import collect_nodes as c  # 延迟导入：复用 URI→clash/sing-box 的转换
    if lay.CORE_FMT[core] == "clash":
        items, names = [], []
        for u in uris:
            try:
                p = c.uri_to_clash(u, "")
            except Exception:  # noqa: BLE001
                p = None
            if not p:
                continue
            items.append(p)
            names.append(c._frag(u) or f"{p.get('server')}:{p.get('port')}")
        for p, nm in zip(items, c.unique_names(names)):
            p["name"] = nm
        return lay.write_core_file(path, core, proxies=items)

    items = []
    for u in uris:
        try:
            ob = c.uri_to_singbox(u, c._frag(u) or "")
        except Exception:  # noqa: BLE001
            ob = None
        if ob:
            items.append(ob)
    for ob, nm in zip(items, c.unique_names([o.get("tag", "") for o in items])):
        ob["tag"] = nm
    return lay.write_core_file(path, core, outbounds=items)


def save(root, core, pool, date_str, state=None):
    """写该内核的池文件 + 更新共享状态。返回 {"path","count","state"}。"""
    core = lay.canon(core)
    os.makedirs(lay.pool_dir(root), exist_ok=True)
    uris = [n["uri"] for n in pool.get("nodes", []) if n.get("uri")]
    try:
        path, n = _write_pool_file(root, core, uris)
    except Exception as e:  # noqa: BLE001 — 单个内核写失败不应中断整轮采集
        print(f"[warn] 节点池写入失败（{core}）: {e}", file=sys.stderr)
        return {"path": None, "count": 0}
    if state is not None:
        state.setdefault("cores", {})[core] = {"updated": date_str,
                                              "nodes": list(pool.get("nodes", []))}
    return {"path": path, "count": n}


# ---------------------------------------------------------------- 查询

def retest_candidates(pool, exclude_keys, limit):
    """挑出池里今天还没测过的节点做复测（低延迟优先）。"""
    if limit <= 0:
        return []
    cand = [n for n in pool.get("nodes", [])
            if n.get("key") not in exclude_keys and n.get("uri")]
    cand.sort(key=lambda n: (1 if n.get("best_latency") is None else 0,
                             n.get("best_latency") or 0))
    out = []
    for n in cand[:limit]:
        out.append({"uri": n["uri"], "proto": n.get("proto", ""),
                    "host": n.get("host"), "port": n.get("port"),
                    "repo": n.get("repo", ""), "latency": n.get("best_latency"),
                    "from_pool": True})
    return out


def all_uris(root, cores=None):
    """池里全部节点 URI（自建代理选候选用），按「通过次数多、延迟低」排序。"""
    state = load_state(root)
    cores = cores or lay.CORES
    cand = []
    for core in cores:
        pool = load(state, core)
        for n in pool.get("nodes", []):
            if n.get("uri"):
                cand.append({"uri": n["uri"], "core": core,
                             "ok_count": int(n.get("ok_count") or 0),
                             "latency": n.get("best_latency"),
                             "proto": n.get("proto", "")})
    cand.sort(key=lambda x: (-x["ok_count"],
                             1 if x["latency"] is None else 0,
                             x["latency"] or 0))
    seen, out = set(), []
    for c in cand:
        if c["uri"] in seen:
            continue
        seen.add(c["uri"])
        out.append(c)
    return out


def summary_lines(root, cores, notes=None):
    """生成池汇总的 markdown 表格行（供 summary.md 使用）。"""
    state = load_state(root)
    lines = ["| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |", "|---|---|---|---|---|"]
    for core in cores:
        core = lay.canon(core)
        if core not in lay.CORES:
            continue
        pool = load(state, core)
        note = (notes or {}).get(core) or {}
        lines.append(f"| {core} | {len(pool.get('nodes', []))} | {note.get('added', 0)} | "
                     f"{note.get('updated', 0)} | `pool/{lay.POOL_FILE[core]}` |")
    return lines
