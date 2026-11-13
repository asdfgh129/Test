#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo_pool.py — 仓库地址池 + 仓库质量评分（2026-11-11 用户需求）

背景：以前「仓库清单」只是采集的副产物（src/seed_repos.json 里谁贡献过节点就记一条），
既没有入池/出池的生命周期，也没有统一的评分口径，取哪个仓库采多少全凭当时的临时规则。
现在把它提升为**正经的地址池**：

  1. 每天搜索命中的仓库全部入池（`mark_seen`），并记录 GitHub 的 `pushed_at`；
  2. **5 天没更新就出池**（`evict_stale`），出池后不再采集，被再次搜索命中会复活；
  3. 池内每个仓库有 0-100 的质量分（`score_entry`），采集顺序与单仓配额都由分数决定；
  4. 每天把「去重后的产量归属」与「实测可用率」写回池（`update_yield` / `update_quality`）。

文件仍是 `src/seed_repos.json`（历史名字保留，免得同时维护两份清单造成漂移），
但内部结构升到 version 2，v1 的 `repos` 会被 `migrate()` 原地升级。

评分口径（用户 2026-11-11 拍板：可用率 40 / 产量 25 / 新鲜度 20 / 延迟 15）：

    score = 100 × (0.40·可用率 + 0.25·产量 + 0.20·新鲜度 + 0.15·延迟) × 惩罚

  - 可用率：窗口内 sum(ok)/sum(tested)，样本 <20 时向先验 0.25 收缩
    （`(ok + 0.25·20) / (tested + 20)`），防止「3 条样本碰巧通了」的仓库拿满分；
  - 产量：近 7 天**去重后归属**的日均条数，log 缩放、3000 条/天封顶。
    归属按「同一条节点被 N 个仓库同时给出 ⇒ 每个仓库记 1/N」，否则搬运型聚合站
    靠原始条数就能霸榜，而它并没有创造供给（2026-11-10 实测最大仓库单日 2.1 万条，
    其中绝大多数是别家也有的重复节点）；
  - 新鲜度：max(0, 1 − push_days/5)，与「5 天出池」同一把尺子；
  - 延迟：max(0, 1 − 平均可用延迟/5000)；
  - 惩罚：连续 3 天「样本≥20 却 0 可用」×0.3；下载失败率 >50% ×0.7。

配额（`quota`）：分数 ≥60 → 10 链接 / 90s；30~60 → 6 链接 / 60s；<30 → 3 链接 / 40s；
从未实测过的新仓库按中档并保底一次完整采样（否则新仓库永远拿不到样本、永远 0 分）。
"""

import json
import math
import os
from datetime import date, datetime, timedelta

VERSION = 2

STALE_DAYS = 5              # 这么久没 push 就出池（用户口径）
EVICT_KEEP_DAYS = 90        # 出池记录保留天数（复盘用，不参与采集）
MAX_ACTIVE = 400            # 池内 active 仓库上限（按分数截断）
MAX_EVICTED = 300           # 出池记录保留条数上限

SCORE_W = {"rate": 0.40, "yield": 0.25, "fresh": 0.20, "lat": 0.15}
PRIOR_RATE = 0.25           # 未实测仓库的中性可用率先验
PRIOR_TESTS = 20            # 收缩样本量：样本少于它时向先验靠
YIELD_CAP = 3000.0          # 产量项封顶（条/天）
LAT_ZERO_MS = 5000.0        # 延迟项归零点
DEAD_STREAK_DAYS = 3        # 连续这么多天「有样本但 0 可用」→ 惩罚
FAIL_RATIO_PENALTY = 0.5    # 下载失败率超过它 → 惩罚
PENALTY_DEAD = 0.3
PENALTY_FAIL = 0.7

QUALITY_WINDOW = 5          # 实测窗口（known-issues 第 53 条）
YIELD_WINDOW = 14           # 产量窗口（天）

# 配额分档：(分数下限, README 链接上限, 单仓预算秒)
QUOTA_TIERS = [(60.0, 10, 90), (30.0, 6, 60), (0.0, 3, 40)]
QUOTA_NEW = (6, 60)         # 从未实测过的新仓库


# ---------------------------------------------------------------- 基础

def _as_date(value, default=None):
    """把 'YYYY-MM-DD' / 'YYYY-MM-DDTHH:MM:SSZ' / date 统一成 date。"""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value or "").strip()
    if len(text) >= 10:
        try:
            return date.fromisoformat(text[:10])
        except ValueError:
            return default
    return default


def _today(day=None):
    return _as_date(day, date.today()) or date.today()


def _empty_entry(full_name):
    return {"full_name": full_name, "stars": 0, "contributed": 0,
            "first_seen": "", "last_seen": "", "last_push": "", "last_collected": "",
            "state": "active", "evicted_at": "", "evict_reason": "",
            "yield_days": [], "quality_history": []}


def _empty_pool():
    return {"version": VERSION, "updated": "", "repos": []}


def load(path):
    """读池；v1（只有 full_name/stars/contributed/last_collected）会被原地升级。"""
    if not path or not os.path.exists(path):
        return _empty_pool()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return _empty_pool()
    if not isinstance(data, dict):
        return _empty_pool()
    data.setdefault("repos", [])
    data.setdefault("updated", "")
    if int(data.get("version") or 1) < VERSION:
        migrated = migrate(data)
        data["version"] = VERSION
        data["_migrated"] = migrated
    return data


def migrate(pool):
    """v1 → v2：补齐生命周期与窗口字段，不丢历史统计。返回升级条目数。"""
    n = 0
    for r in pool.get("repos", []):
        if not r.get("full_name"):
            continue
        base = _empty_entry(r["full_name"])
        for k, v in base.items():
            r.setdefault(k, v)
        # v1 的 last_collected 是「最后一次真的采过它」的日期，可当作 last_seen 的近似
        if not r.get("last_seen") and r.get("last_collected"):
            r["last_seen"] = r["last_collected"]
        if not r.get("first_seen") and r.get("last_collected"):
            r["first_seen"] = r["last_collected"]
        # v1 的 tested/ok/avail_rate 是窗口汇总，转成一条 quality_history 样本
        if r.get("tested") and not r.get("quality_history"):
            r["quality_history"] = [{"date": r.get("last_tested") or r.get("last_collected") or "",
                                     "tested": int(r.get("tested") or 0),
                                     "ok": int(r.get("ok") or 0),
                                     "rate": round(float(r.get("avail_rate") or 0), 3),
                                     "latency": r.get("avg_latency")}]
        r["state"] = r.get("state") or "active"
        n += 1
    return n


def save(path, pool, date_str):
    """按状态与分数裁剪后落盘（active 上限 400、出池记录 300 条）。"""
    today = _today(date_str)
    repos = [r for r in pool.get("repos", []) if r.get("full_name")]
    for r in repos:
        r["push_days"] = staleness(r, today)
        r.setdefault("state", "active")

    active = [r for r in repos if r.get("state") == "active"]
    evicted = [r for r in repos if r.get("state") != "active"]
    active.sort(key=lambda r: (-(r.get("score") or 0), r["full_name"]))
    # 出池记录按出池时间倒序，太久远的丢掉（只留复盘价值，不参与采集）
    evicted.sort(key=lambda r: (r.get("evicted_at") or "", r["full_name"]), reverse=True)
    evicted = [r for r in evicted
               if (_as_date(r.get("evicted_at"), today) or today) >= today - timedelta(days=EVICT_KEEP_DAYS)]
    if len(active) > MAX_ACTIVE:
        print(f"[info] 仓库池 active 条目 {len(active)} 超过上限 {MAX_ACTIVE}，按分数截断")
        active = active[:MAX_ACTIVE]
    evicted = evicted[:MAX_EVICTED]

    pool["repos"] = active + evicted
    pool["version"] = VERSION
    pool["updated"] = str(date_str)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pool, f, ensure_ascii=False, indent=1)
        return path
    except OSError as e:
        print(f"[warn] 仓库池写入失败: {e}")
        return None


# ---------------------------------------------------------------- 进出池

def find(pool, full_name):
    for r in pool.get("repos", []):
        if r.get("full_name") == full_name:
            return r
    return None


def ensure(pool, full_name, stars=0):
    r = find(pool, full_name)
    if r is None:
        r = _empty_entry(full_name)
        r["stars"] = int(stars or 0)
        pool.setdefault("repos", []).append(r)
    return r


def mark_seen(pool, full_name, stars=0, pushed_at="", date_str=""):
    """搜索命中：入池 / 刷新 pushed_at / 记录最近一次见到它的日期。

    被出池过的仓库在这里复活（state 回到 active）——它又更新了就说明还活着。
    """
    r = ensure(pool, full_name, stars)
    r["stars"] = max(int(r.get("stars") or 0), int(stars or 0))
    r["last_seen"] = str(date_str)
    if pushed_at:
        apply_push(r, pushed_at)
    if r.get("state") != "active":
        print(f"[info] 仓库复池：{full_name}（最近 push {r.get('last_push') or '未知'}）")
        r["state"] = "active"
        r["evicted_at"] = ""
        r["evict_reason"] = ""
    return r


def apply_push(entry, pushed_at):
    """写入 GitHub 的 pushed_at（只前进不后退，搜索接口偶尔会给出更旧的缓存值）。"""
    new = _as_date(pushed_at)
    if not new:
        return
    old = _as_date(entry.get("last_push"))
    if old and new < old:
        return
    entry["last_push"] = new.isoformat()


def staleness(entry, today=None):
    """距最近一次 push 的天数；不知道 pushed_at 时返回 None。"""
    pushed = _as_date(entry.get("last_push"))
    if not pushed:
        return None
    return max(0, (_today(today) - pushed).days)


def needs_verify(entry, today=None, days=STALE_DAYS):
    """是否要在出池前用 API 复核一次 pushed_at（快到期的才查，控制配额）。"""
    if entry.get("state") != "active":
        return False
    d = staleness(entry, today)
    return d is not None and d >= days - 1


def evict_stale(pool, today=None, days=STALE_DAYS):
    """把 5 天没更新的仓库移出池（state=evicted，记录保留）。返回出池名单。"""
    today = _today(today)
    gone = []
    for r in pool.get("repos", []):
        if r.get("state") != "active":
            continue
        d = staleness(r, today)
        if d is None:
            # 完全不知道 push 时间的（v1 迁移来的老条目）不下杀手，靠 last_seen 兜底：
            # 连续 5 天没在任何搜索结果里见到，才认为它已经停更
            seen = _as_date(r.get("last_seen"))
            d = (today - seen).days if seen else None
            if d is None or d <= days:
                continue
            r["evict_reason"] = "unknown_push"
        else:
            if d <= days:
                continue
            r["evict_reason"] = "stale5"
        r["state"] = "evicted"
        r["evicted_at"] = today.isoformat()
        gone.append(r["full_name"])
    return gone


# ---------------------------------------------------------------- 评分

def _rate_part(entry):
    """可用率项（0~1），带贝叶斯收缩。"""
    tested = int(entry.get("tested") or 0)
    ok = int(entry.get("ok") or 0)
    if tested <= 0:
        return PRIOR_RATE, {"tested": 0, "ok": 0, "raw": None}
    raw = ok / tested
    shrunk = (ok + PRIOR_RATE * PRIOR_TESTS) / (tested + PRIOR_TESTS)
    return shrunk, {"tested": tested, "ok": ok, "raw": round(raw, 4)}


def _yield_part(entry, today):
    """产量项（0~1）：近 7 天去重归属的日均条数，log 缩放。"""
    today = _today(today)
    start = today - timedelta(days=7)
    total = 0.0
    for d in entry.get("yield_days") or []:
        day = _as_date(d.get("date"))
        if day and day > start:
            total += float(d.get("uniq") or 0)
    daily = total / 7.0
    part = 0.0 if daily <= 0 else min(1.0, math.log10(1 + daily) / math.log10(1 + YIELD_CAP))
    return part, {"daily": round(daily, 1), "uniq_7d": round(total, 1)}


def _fresh_part(entry, today):
    d = staleness(entry, today)
    if d is None:
        return 0.5, {"push_days": None}
    return max(0.0, 1.0 - d / float(STALE_DAYS)), {"push_days": d}


def _lat_part(entry):
    lat = entry.get("avg_latency")
    if not lat:
        return 0.0, {"avg_latency": None}
    return max(0.0, 1.0 - float(lat) / LAT_ZERO_MS), {"avg_latency": lat}


def _dead_streak(entry):
    """末尾连续多少天「样本≥PRIOR_TESTS 但 0 可用」。"""
    streak = 0
    for h in reversed(entry.get("quality_history") or []):
        if int(h.get("tested") or 0) < PRIOR_TESTS:
            break
        if int(h.get("ok") or 0) > 0:
            break
        streak += 1
    return streak


def _fail_ratio(entry):
    raw = fails = 0
    for d in (entry.get("yield_days") or [])[-7:]:
        raw += int(d.get("raw") or 0)
        fails += int(d.get("fail") or 0)
    if raw + fails <= 0:
        return 0.0
    return fails / float(raw + fails)


def score_entry(entry, today=None):
    """算总分与分项，写回 entry（score/score_parts），返回分项字典。"""
    rate, rate_info = _rate_part(entry)
    yld, yield_info = _yield_part(entry, today)
    fresh, fresh_info = _fresh_part(entry, today)
    lat, lat_info = _lat_part(entry)

    penalty = 1.0
    reasons = []
    streak = _dead_streak(entry)
    if streak >= DEAD_STREAK_DAYS:
        penalty *= PENALTY_DEAD
        reasons.append(f"连续{streak}天0可用")
    fr = _fail_ratio(entry)
    if fr > FAIL_RATIO_PENALTY:
        penalty *= PENALTY_FAIL
        reasons.append(f"下载失败率{fr * 100:.0f}%")

    total = 100.0 * (SCORE_W["rate"] * rate + SCORE_W["yield"] * yld
                     + SCORE_W["fresh"] * fresh + SCORE_W["lat"] * lat) * penalty
    parts = {"rate": round(rate, 4), "yield": round(yld, 4),
             "fresh": round(fresh, 4), "lat": round(lat, 4),
             "penalty": round(penalty, 3), "penalty_reasons": reasons,
             "rate_info": rate_info, "yield_info": yield_info,
             "fresh_info": fresh_info, "lat_info": lat_info}
    entry["score"] = round(total, 1)
    entry["score_parts"] = parts
    return parts


def refresh(pool, today=None):
    """给池内所有 active 仓库重算分数，按分数降序返回。"""
    out = []
    for r in pool.get("repos", []):
        if r.get("state") != "active":
            continue
        score_entry(r, today)
        out.append(r)
    out.sort(key=lambda r: (-(r.get("score") or 0), r.get("full_name") or ""))
    return out


def active_repos(pool, today=None, limit=None):
    """按分数降序取 active 仓库（采集清单）。"""
    ordered = refresh(pool, today)
    return ordered[:limit] if limit else ordered


def quota(entry, today=None):
    """单仓配额：(README 链接上限, 时间预算秒)。分数越高给的越多。"""
    if not int(entry.get("tested") or 0):
        links, budget = QUOTA_NEW
        return links, budget, "new"
    score = float(entry.get("score") or 0)
    for floor, links, budget in QUOTA_TIERS:
        if score >= floor:
            return links, budget, f"score{floor:.0f}+"
    return QUOTA_TIERS[-1][1], QUOTA_TIERS[-1][2], "low"


# ---------------------------------------------------------------- 回写统计

def update_quality(pool, per_repo, date_str, window=QUALITY_WINDOW):
    """把四内核实测结果按仓库滚动汇总（口径同 known-issues 第 53 条）。

    per_repo: {repo: {"tested": n, "ok": m, "latency_sum": ms, "latency_n": k}}
    用 sum(tested)/sum(ok) 汇总而不是可用率平均：样本多的那次自然权重大。
    """
    for repo, st in (per_repo or {}).items():
        tested, ok = int(st.get("tested") or 0), int(st.get("ok") or 0)
        if not tested:
            continue
        entry = ensure(pool, repo)
        avg_lat = round(st["latency_sum"] / st["latency_n"]) if st.get("latency_n") else None
        hist = list(entry.get("quality_history") or [])
        sample = {"date": str(date_str), "tested": tested, "ok": ok,
                  "rate": round(ok / tested, 3), "latency": avg_lat}
        if hist and hist[-1].get("date") == sample["date"]:
            hist[-1] = sample          # 同日多内核各写一次，后者覆盖前者
        else:
            hist.append(sample)
        hist = hist[-window:]
        tot_t, tot_ok = 0, 0
        for h in hist:
            h_tested = int(h.get("tested") or 0)
            h_ok = int(h.get("ok") or 0) if "ok" in h else int(round(float(h.get("rate") or 0) * h_tested))
            tot_t += h_tested
            tot_ok += h_ok
        entry["quality_history"] = hist
        entry["tested"], entry["ok"] = tot_t, tot_ok
        entry["avail_rate"] = round(tot_ok / tot_t, 3) if tot_t else 0
        entry["avg_latency"] = avg_lat
        entry["last_tested"] = str(date_str)
        # 兼容字段：沿用旧公式（可用率 70 + 延迟 30），health_check 仍在读
        entry["quality"] = legacy_quality(entry["avail_rate"], avg_lat)
    return pool


def update_yield(pool, per_repo, date_str, fail=None):
    """把「去重后的产量归属」写回池。

    per_repo: {repo: {"raw": 原始条数, "uniq": 归属条数（已按 1/N 拆分）}}
    fail:     {repo: 下载失败链接数}
    """
    fail = fail or {}
    for repo, st in (per_repo or {}).items():
        entry = ensure(pool, repo)
        days = [d for d in (entry.get("yield_days") or [])
                if _as_date(d.get("date")) and _as_date(d.get("date")) > _today(date_str) - timedelta(days=YIELD_WINDOW)]
        rec = {"date": str(date_str), "raw": int(st.get("raw") or 0),
               "uniq": round(float(st.get("uniq") or 0), 3),
               "fail": int(fail.get(repo) or 0)}
        if days and days[-1].get("date") == rec["date"]:
            days[-1] = rec
        else:
            days.append(rec)
        entry["yield_days"] = days[-YIELD_WINDOW:]
        entry["contributed"] = int(entry.get("contributed") or 0) + rec["raw"]
        entry["last_collected"] = str(date_str)
    return pool


def legacy_quality(avail_rate, avg_latency):
    """旧公式（可用率 70 分 + 延迟 30 分，5000ms 归零），仅为兼容 health_check 保留。"""
    rate = max(0.0, min(1.0, float(avail_rate or 0)))
    if rate <= 0 or avg_latency is None:
        return round(rate * 70, 1)
    lat = max(0.0, 100.0 - float(avg_latency) / 50.0)
    return round(rate * 70 + lat * 0.3, 1)


def summary(pool, today=None):
    """池状态摘要（写日志/汇报用）。"""
    today = _today(today)
    acted = [r for r in pool.get("repos", []) if r.get("state") == "active"]
    fresh = 0
    for r in acted:
        d = staleness(r, today)
        if d is not None and d <= 1:      # 注意 0 是合法值（今天 push 过），不能写成 `or`
            fresh += 1
    tested = [r for r in acted if int(r.get("tested") or 0) > 0]
    ev = [r for r in pool.get("repos", []) if r.get("state") != "active"]
    scores = sorted((float(r.get("score") or 0) for r in tested), reverse=True)
    return {"active": len(acted), "evicted": len(ev), "pushed_today": fresh,
            "tested": len(tested),
            "score_max": scores[0] if scores else None,
            "score_median": scores[len(scores) // 2] if scores else None,
            "score_min": scores[-1] if scores else None}


def priority_hint(pool, today=None, n=8):
    """「质量优先顺序」的可读快照（写进采集日志）。"""
    rows = active_repos(pool, today, limit=n)
    return "、".join(
        f"{r['full_name']}(分{r.get('score')}/可用率{(float(r.get('avail_rate') or 0)) * 100:.0f}%"
        f"/push{(r.get('push_days') if r.get('push_days') is not None else '?')}天前)"
        for r in rows)
