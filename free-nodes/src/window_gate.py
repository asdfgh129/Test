#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""window_gate.py — 判定今晚还需不需要再跑下一个验证窗口 + 第 2/3 窗口自动开关。

背景：本地验证原先固定跑 22:00 / 23:45 / 01:30 三个窗口接力（平台对单次自动化运行
有 90 分钟强制取消）。但如果第一窗口就把四个内核的候选测完了，后两窗口纯属空转：
白占机器，还会把 summary/日志再刷一遍。所以每个窗口收尾时用本脚本判定。

三种用法（2026-11-14 起）：

    # 第一窗口（主窗口）收尾：跑闸门 + 记今晚结果 + 决策第 2/3 窗口开关
    python src/window_gate.py --input free-nodes --first-window

    # 第 2/3 窗口开工：开关 off 就直接跳过；on 才继续跑闸门
    python src/window_gate.py --input free-nodes --check-switch --window 2
    python src/window_gate.py --input free-nodes --check-switch --window 3 --date <采集日>

    # 一次性初始化：从 Docs/summary.md 回填最近 N 晚，按同一规则决策（不跑闸门）
    python src/window_gate.py --input free-nodes --backfill

    # 不带以上参数 = 第 2/3 窗口口径（兼容旧命令）：先读开关，off 直接 GATE: done；
    #                开关 on 才跑闸门。旧命令因此自动受开关约束，不用逐个改 prompt

退出码（沿用旧语义，主窗口/后续窗口都靠它判断）：
    0 = 今晚已跑完（或第 2/3 窗口已停用），**不需要**下一个窗口
    1 = 还没跑完，下一个窗口继续；summary 缺失/日期不符等不确定情况也返回 1（宁可多跑）
    2 = 参数或文件错误

判定依据 Docs/summary.json（同一天多窗口的结果会累积合并）：
    - partial=true              → 没跑完（本窗口主动收尾或被强杀）
    - exhausted=true            → 跑完（候选全部测过）
    - tested >= min(cand, cap)  → 跑完（候选多于单轮上限时，测满上限就是既定口径）

日期新鲜度（2026-11-13 新增）：summary 是**本地验证**的产物，本地某天没跑就一直是上次那天的。
不校验日期的话，只要本地连续几晚没跑（机器休眠、窗口没触发），闸门会一直拿旧 summary 回 done，
后续窗口全部空转、订阅也一直停在旧日期。所以在没给 --date 时按「今天」判断新鲜度：
    - summary 日期 == 今天            → 认可
    - summary 日期 == 昨天且当前时刻 < 06:00 → 认可（跨零点窗口，01:30 那次用的就是昨天）
    - 其他                            → 视为过期，按未跑完处理（GATE: continue）

## 第 2/3 窗口开关（用户口径 2026-11-14）

**开关只由第一窗口控制**：主窗口每晚收尾把结果写进 Docs/window_switch.json 并给出
SWITCH / SWITCH_ACTION 两行；第 2/3 窗口开工只读、不改开关。这样「要不要开后续窗口」
永远是一个地方决策、可审计、可复盘，不会出现三个窗口各自判断互相矛盾。

关闭条件：最近 STREAK_REQUIRED 个**有运行的夜晚**（不是连续日历日，机器离线那晚不算）
全部 GATE done 且验证耗时 ≤ MAX_ELAPSED_MIN 分钟。
立即开启条件（任一命中，当晚就让后两窗口待命）：
    - 今晚 GATE: continue（有 pending 内核 / partial / summary 缺失或过期）
    - 今晚验证耗时 > MAX_ELAPSED_MIN（说明窗口吃紧，随时可能不够用）
    - 开关 off 但主窗口已断档 ≥ STALE_DAYS 天（fail-safe，防止三个窗口全停没人恢复）

SWITCH_ACTION 是幂等的对齐指令，主窗口每晚都要照做一次：
    pause  → 把第 2/3 窗口的 automation 置为 PAUSED
    resume → 置为 ACTIVE（当夜 23:45 / 01:30 就能接手）
    keep   → 不用动平台配置

注意：`partial` 只描述**本窗口**，`tested` 是本日累计，所以两者要分开看——
只看 partial 会把「第一窗被强杀、第二窗补完」误判成没跑完。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as lay  # 统一布局，禁止在脚本里硬编码目录

# 跨零点窗口（01:30 那次）处理的是前一天的采集日，所以「昨天」只在凌晨时段被认可。
CROSS_MIDNIGHT_UNTIL_HOUR = 6

# ── 第 2/3 窗口开关口径（改这里就是改规则，别在别处散落常量）──
SWITCH_FILE = "window_switch.json"
STREAK_REQUIRED = 7           # 连续这么多晚「首窗独立跑完」才关掉后两窗口
MAX_ELAPSED_MIN = 50.0        # 单晚验证耗时超过它 = 窗口吃紧，即便 done 也不关
STALE_DAYS = 2                # 开关 off 且主窗口断档这么多天 → 自动恢复（fail-safe）
HISTORY_KEEP = 30             # history 保留晚数
BACKFILL_N = 7                # 一次性初始化时从 summary.md 回填几晚


def _date_fresh(summary_date, now=None):
    """summary 的日期是否够新（用于没显式给 --date 的场景）。

    返回 (是否新鲜, 说明)。规则见模块 docstring：今天内 / 凌晨时的昨天 才算新鲜。
    """
    now = now or datetime.now()
    try:
        d = datetime.strptime(summary_date, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return False, f"summary 日期无法解析：{summary_date!r}"
    today = now.date()
    if d == today:
        return True, "采集日为今天"
    if d == today - timedelta(days=1):
        if now.hour < CROSS_MIDNIGHT_UNTIL_HOUR:
            return True, "采集日为昨天（跨零点窗口）"
        return False, f"summary 停在昨天 {summary_date}，今天的本地验证还没跑"
    return False, f"summary 停在 {summary_date}，已过期 {(today - d).days} 天（本地验证没跑）"


def _core_done(st):
    """某个内核今晚是否已达既定口径。返回 (是否完成, 一句话原因)。"""
    if not st:
        return False, "未跑"
    cap = st.get("cap") or 0
    cand = st.get("cand") or 0
    tested = st.get("tested") or 0
    target = min(cand, cap) if cap else cand
    if st.get("partial"):
        return False, f"本窗口未跑完（已测 {tested}，候选 {cand}）"
    if st.get("exhausted"):
        return True, f"候选已全部测完（{tested}/{cand}）"
    if cap and tested >= target:
        return True, f"已测满单轮上限（{tested}/{target}）"
    return False, f"未跑完（已测 {tested}，还需 {max(target - tested, 0)} 个）"


def _gate_lines(data, cores, args, now=None):
    """原有闸门判定。返回 (退出码, 待打印的行, 待补内核列表, 采集日)。"""
    date_str = str(data.get("date") or "")
    if not date_str:
        return 1, ["[gate] summary 里没有 date 字段",
                   "GATE: continue（日期缺失，按未跑完处理）"], list(cores), date_str
    if args.date and args.date != date_str:
        return 1, [f"[gate] summary 日期 {date_str} 与期望 {args.date} 不符",
                   "GATE: continue（不是同一采集日，按未跑完处理）"], list(cores), date_str
    if not args.date:
        fresh, why = _date_fresh(date_str, now)
        if not fresh:
            return 1, [f"[gate] {why}",
                       "GATE: continue（summary 不是今天的，本地验证还没跑，按未跑完处理）"], list(cores), date_str

    stats = data.get("cores") or {}
    lines = [f"[gate] 采集日 {date_str}（生成于 {data.get('generated_at', '-')}）"]
    pending = []
    for core in cores:
        done, why = _core_done(stats.get(core))
        lines.append(f"[gate]   {core:<8} {'完成' if done else '未完成'}：{why}")
        if not done:
            pending.append(core)
    if pending:
        lines.append(f"GATE: continue（待补内核：{'、'.join(pending)}）")
        return 1, lines, pending, date_str
    lines.append(f"GATE: done（{'、'.join(cores)} 今晚都已达既定口径，后续窗口不用跑）")
    return 0, lines, pending, date_str


def _read_summary(root, args):
    """读 Docs/summary.json。返回 (data, 错误行列表)。"""
    path = lay.summary_json_path(root)
    if not os.path.exists(path):
        return None, [f"[gate] 没有 summary：{path}",
                      "GATE: continue（缺证据，按未跑完处理）"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), []
    except (OSError, ValueError) as e:
        return None, [f"[gate] summary 读取失败：{str(e)[:120]}",
                      "GATE: continue（读取失败，按未跑完处理）"]


# ───────────────────────── 开关状态文件 ─────────────────────────

def switch_path(root):
    return os.path.join(lay.docs_dir(root), SWITCH_FILE)


def load_switch(root):
    """读开关状态；文件不存在/损坏时默认 on（宁可多跑，绝不误停）。"""
    path = switch_path(root)
    state = {
        "version": 1,
        "followup_windows": "on",
        "updated_at": "",
        "reason": "初始状态：默认开启第 2/3 窗口",
        "streak_done": 0,
        "required_streak": STREAK_REQUIRED,
        "max_elapsed_min": MAX_ELAPSED_MIN,
        "history": [],
        "followup_used": [],
        "last_pause_at": None,
        "last_resume_at": None,
    }
    try:
        with open(path, "r", encoding="utf-8") as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            state.update(saved)
    except (OSError, ValueError):
        pass
    # 常量以脚本为准，避免旧文件里的过期阈值覆盖新规则
    state["required_streak"] = STREAK_REQUIRED
    state["max_elapsed_min"] = MAX_ELAPSED_MIN
    state.setdefault("history", [])
    state.setdefault("followup_used", [])
    return state


def save_switch(root, state):
    path = switch_path(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    state["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return path


def _elapsed_of(data, root, date_str):
    """取当晚验证耗时（分钟）。优先 summary.json 的 elapsed_min，回退解析 summary.md。"""
    v = data.get("elapsed_min") if isinstance(data, dict) else None
    if isinstance(v, (int, float)) and v > 0:
        return round(float(v), 1)
    try:
        with open(lay.summary_path(root), "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    for sec in re.split(r"(?m)^## ", text)[1:]:
        head = sec.splitlines()[0] if sec.splitlines() else ""
        if date_str and not head.startswith(date_str):
            continue
        m = re.search(r"总耗时：([\d.]+)\s*分钟", sec)
        return round(float(m.group(1)), 1) if m else None
    return None


def backfill_history(root, n=BACKFILL_N):
    """从 Docs/summary.md 回填最近 n 个有运行的夜晚（一次性初始化用）。

    只取「最终状态」：小节里出现「本轮未跑完」记 continue，否则记 done。
    第二/三窗口是否真的跑过验证由 followup_used 单独记录；初始化时按
    「当晚最终达标」处理，配合已核实的连续多晚后两窗口未跑验证记录使用。
    """
    try:
        with open(lay.summary_path(root), "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return []
    out = []
    for sec in re.split(r"(?m)^## ", text)[1:]:
        head = sec.splitlines()[0] if sec.splitlines() else ""
        m = re.match(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", head)
        if not m:
            continue
        mins = re.search(r"总耗时：([\d.]+)\s*分钟", sec)
        out.append({
            "date": m.group(1),
            "gate": "continue" if "本轮未跑完" in sec else "done",
            "elapsed_min": round(float(mins.group(1)), 1) if mins else None,
            "pending": [],
            "source": "backfill/summary.md",
        })
    out.sort(key=lambda x: x["date"])
    # 同一天多小节只留最后一个（summary.md 约定「同一天重跑会替换当天小节」）
    by_date = {}
    for e in out:
        by_date[e["date"]] = e
    return sorted(by_date.values(), key=lambda x: x["date"])[-n:]


def _upsert_history(history, entry):
    by_date = {e.get("date"): e for e in history if e.get("date")}
    by_date[entry["date"]] = entry
    return sorted(by_date.values(), key=lambda x: x["date"])[-HISTORY_KEEP:]


def _streak(history, n=STREAK_REQUIRED):
    """最近 n 个有运行的夜晚是否全部「跑完且不吃紧」。"""
    recent = history[-n:]
    all_done = len(recent) >= n and all(e.get("gate") == "done" for e in recent)
    all_fast = all((e.get("elapsed_min") is None or e["elapsed_min"] <= MAX_ELAPSED_MIN)
                   for e in recent)
    return recent, all_done, all_fast


def decide_switch(root, state, tonight=None, now=None):
    """核心决策。tonight=None 表示只按 history 复核（--backfill 用）。

    返回 (state, action, reason, switch_value)。action 是幂等的平台对齐指令。
    """
    now = now or datetime.now()
    today = now.date().isoformat()
    state = dict(state)
    if tonight:
        state["history"] = _upsert_history(state.get("history", []), tonight)
    history = state.get("history", [])
    recent, all_done, all_fast = _streak(history)

    danger = None
    if tonight and tonight.get("gate") != "done":
        danger = (f"今晚 GATE: continue"
                  + (f"（待补：{'、'.join(tonight.get('pending') or [])}）"
                     if tonight.get("pending") else "（summary 缺失/过期）"))
    elif tonight and tonight.get("elapsed_min") is not None and tonight["elapsed_min"] > MAX_ELAPSED_MIN:
        danger = f"今晚验证耗时 {tonight['elapsed_min']} 分钟 > {MAX_ELAPSED_MIN:.0f} 分钟上限，窗口吃紧"

    # fail-safe：开关 off 但主窗口已断档 → 自动恢复，避免「三个窗口全停、没人能重启」
    # 注意：只补充理由、不覆盖今晚的首要原因（否则「没跑完」会被「断档」盖掉）
    stale = False
    stale_note = ""
    if state.get("followup_windows") == "off":
        last = history[-1].get("date", "") if history else ""
        if not last:
            stale, stale_note = True, "且开关 off 无历史记录"
        else:
            try:
                gap = (now.date() - datetime.strptime(last, "%Y-%m-%d").date()).days
                stale = gap >= STALE_DAYS
                if stale:
                    stale_note = f"且开关 off 已断档 {gap} 天（最后记录 {last}）"
            except (TypeError, ValueError):
                stale, stale_note = True, f"且开关 off 的 history 日期无法解析（{last!r}）"
        if stale and not danger:
            danger = stale_note.lstrip("且") + "，自动恢复"
    if stale and stale_note and danger and "断档" not in danger:
        danger += "；" + stale_note.lstrip("且")

    if danger:
        value, action = "on", "resume"
        reason = danger + "；第 2/3 窗口保持/恢复启用"
        state["last_resume_at"] = f"{today} {now.strftime('%H:%M:%S')}"
    elif all_done and all_fast:
        value, action = "off", "pause"
        span = f"{recent[0]['date']}~{recent[-1]['date']}" if recent else "-"
        slow = max((e.get("elapsed_min") or 0) for e in recent)
        reason = (f"最近 {len(recent)} 个有运行的夜晚（{span}）首窗全部跑完、"
                  f"最长 {slow:.1f} 分钟（≤{MAX_ELAPSED_MIN:.0f}），后两窗口用不上")
        state["last_pause_at"] = f"{today} {now.strftime('%H:%M:%S')}"
    else:
        value = state.get("followup_windows", "on")
        action = "keep"
        n_done = sum(1 for e in recent if e.get("gate") == "done")
        reason = (f"维持 {value}：最近 {len(recent)} 晚跑完 {n_done} 晚"
                  f"（需 {STREAK_REQUIRED} 晚连续达标才停用，耗时达标={all_fast}）")

    state["followup_windows"] = value
    state["streak_done"] = sum(1 for e in history[-STREAK_REQUIRED:]
                               if e.get("gate") == "done")
    state["reason"] = reason
    state["stale_recovered"] = bool(stale)
    return state, action, reason, value


def _print_switch(state, action, reason, value, extra=None):
    print(f"SWITCH: {value}（{reason}）")
    print(f"SWITCH_ACTION: {action}")
    if extra:
        print(extra)


def followup_gate(root, args, cores, now):
    """第 2/3 窗口（含不带任何开关的默认调用）：先读开关，off 直接跳过。

    默认模式也走这里，是为了让**旧的闸门命令**在开关停用后自动生效——
    第二/三窗口的 prompt 不用改命令，也不会因为平台状态漂移而空转。
    """
    state = load_switch(root)
    if state.get("followup_windows") == "off":
        # fail-safe：主窗口连续断档就自动恢复，不能让三个窗口一起停摆
        fresh_state, action, reason, value = decide_switch(root, state, tonight=None, now=now)
        if value == "on":
            save_switch(root, fresh_state)
            print(f"[switch] {reason}")
            print("SWITCH_ACTION: resume（主窗口断档，后续窗口自动恢复；本窗口继续闸门判定）")
        else:
            why = state.get("reason") or "第 2/3 窗口已停用"
            if "初始状态" in why:
                why = "连续达标后已停用（详见 Docs/window_switch.json）"
            print(f"[switch] 第 {args.window or '?'} 窗口当前停用：{why}")
            print(f"SWITCH: off（{why}）")
            print("SWITCH_ACTION: keep")
            print("GATE: done（第 2/3 窗口已停用，本窗口跳过；今晚四内核由第一窗口跑完）")
            return 0
    # 开关 on（或刚被 fail-safe 恢复）→ 继续原有闸门判定
    data, err_lines = _read_summary(root, args)
    if data is None:
        for line in err_lines:
            print(line)
        return 1
    rc, lines, pending, date_str = _gate_lines(data, cores, args, now)
    for line in lines:
        print(line)
    if rc == 1 and args.window:
        st = load_switch(root)
        used = st.get("followup_used", [])
        used.append({"date": date_str or now.date().isoformat(),
                     "window": args.window, "gate": "continue", "pending": pending})
        st["followup_used"] = used[-HISTORY_KEEP:]
        save_switch(root, st)
    return rc


# ───────────────────────────── main ─────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="判定今晚是否还要跑下一个验证窗口 / 管理第 2/3 窗口开关")
    ap.add_argument("--input", default=".", help="free-nodes 根目录（默认当前目录）")
    ap.add_argument("--date", default=None,
                    help="期望的采集日 YYYY-MM-DD；给了就校验 summary 是否属于这一天")
    ap.add_argument("--cores", default=",".join(lay.CORES),
                    help=f"参与判定的内核（默认 {','.join(lay.CORES)}）")
    ap.add_argument("--first-window", action="store_true",
                    help="第一窗口收尾：跑闸门 + 记今晚结果 + 决策开关（开关只在这里改）")
    ap.add_argument("--check-switch", action="store_true",
                    help="第 2/3 窗口开工：开关 off 直接跳过；on 才继续跑闸门")
    ap.add_argument("--window", type=int, default=0, choices=(0, 2, 3),
                    help="配合 --check-switch 标明自己是第几窗口（只用于留痕）")
    ap.add_argument("--backfill", action="store_true",
                    help="一次性初始化：从 Docs/summary.md 回填最近 N 晚并决策，不跑闸门")
    args = ap.parse_args()
    if sum(bool(x) for x in (args.first_window, args.check_switch, args.backfill)) > 1:
        print("[gate] --first-window / --check-switch / --backfill 只能选一个", file=sys.stderr)
        return 2

    root = os.path.abspath(args.input)
    cores = lay.parse_cores(args.cores, lay.CORES)
    now = datetime.now()

    # ── 一次性初始化：只回填 + 决策，不看今晚实时闸门 ──
    if args.backfill:
        state = load_switch(root)
        if not state.get("history"):
            state["history"] = backfill_history(root)
        state, action, reason, value = decide_switch(root, state, tonight=None, now=now)
        save_switch(root, state)
        print(f"[switch] 已回填 {len(state['history'])} 晚记录（来源 Docs/summary.md）")
        _print_switch(state, action, reason, value,
                      f"[switch] 状态文件：{switch_path(root)}")
        return 0

    # ── 第 2/3 窗口（含默认调用）：只读开关，off 就跳过；on 才跑闸门 ──
    if not args.first_window:
        return followup_gate(root, args, cores, now)

    # ── 第一窗口：跑闸门（并收尾决策开关）──
    data, err_lines = _read_summary(root, args)
    if data is None:
        for line in err_lines:
            print(line)
        rc, date_str, pending, elapsed = 1, now.date().isoformat(), list(cores), None
    else:
        rc, lines, pending, date_str = _gate_lines(data, cores, args, now)
        for line in lines:
            print(line)
        elapsed = _elapsed_of(data, root, date_str) if data else None

    # ── 第一窗口收尾：记录今晚 + 决策开关（唯一改开关的地方）──
    state = load_switch(root)
    if not state.get("history"):
        state["history"] = backfill_history(root)
        print(f"[switch] 开关文件首次使用，已从 Docs/summary.md 回填 {len(state['history'])} 晚记录")
    # history 记的是「主窗口哪晚跑了」，用运行日而非 summary 的采集日：
    # summary 过期时 date_str 可能是几天前，用它会让 fail-safe 误判成主窗口断档
    tonight = {
        "date": now.date().isoformat(),
        "gate": "done" if rc == 0 else "continue",
        "elapsed_min": elapsed,
        "pending": pending,
        "summary_date": date_str,
        "source": "first_window",
    }
    state, action, reason, value = decide_switch(root, state, tonight=tonight, now=now)
    path = save_switch(root, state)
    _print_switch(state, action, reason, value, f"[switch] 状态文件：{path}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
