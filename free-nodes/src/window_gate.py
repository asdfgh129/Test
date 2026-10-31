#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""window_gate.py — 判定今晚还需不需要再跑下一个验证窗口。

背景：本地验证原先固定跑 22:00 / 23:45 / 01:30 三个窗口接力（平台对单次自动化运行
有 90 分钟强制取消）。但如果第一窗口就把四个内核的候选测完了，后两窗口纯属空转：
白占机器，还会把 summary/日志再刷一遍。所以每个窗口收尾时用本脚本判定。

用法（每个窗口跑完都调一次）：

    python src/window_gate.py --input free-nodes

退出码：
    0 = 今晚已跑完，**不需要**下一个窗口
    1 = 还没跑完，下一个窗口继续；summary 缺失/日期不符等不确定情况也返回 1（宁可多跑）
    2 = 参数或文件错误

判定依据 Docs/summary.json（同一天多窗口的结果会累积合并）：
    - partial=true              → 没跑完（本窗口主动收尾或被强杀）
    - exhausted=true            → 跑完（候选全部测过）
    - tested >= min(cand, cap)  → 跑完（候选多于单轮上限时，测满上限就是既定口径）

注意：`partial` 只描述**本窗口**，`tested` 是本日累计，所以两者要分开看——
只看 partial 会把「第一窗被强杀、第二窗补完」误判成没跑完。
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as lay  # 统一布局，禁止在脚本里硬编码目录


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


def main():
    ap = argparse.ArgumentParser(description="判定今晚是否还要跑下一个验证窗口")
    ap.add_argument("--input", default=".", help="free-nodes 根目录（默认当前目录）")
    ap.add_argument("--date", default=None,
                    help="期望的采集日 YYYY-MM-DD；给了就校验 summary 是否属于这一天")
    ap.add_argument("--cores", default=",".join(lay.CORES),
                    help=f"参与判定的内核（默认 {','.join(lay.CORES)}）")
    args = ap.parse_args()

    root = os.path.abspath(args.input)
    cores = lay.parse_cores(args.cores, lay.CORES)
    path = lay.summary_json_path(root)
    if not os.path.exists(path):
        print(f"[gate] 没有 summary：{path}")
        print("GATE: continue（缺证据，按未跑完处理）")
        return 1

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        print(f"[gate] summary 读取失败：{str(e)[:120]}")
        print("GATE: continue（读取失败，按未跑完处理）")
        return 1

    date_str = str(data.get("date") or "")
    if not date_str:
        print("[gate] summary 里没有 date 字段")
        print("GATE: continue（日期缺失，按未跑完处理）")
        return 1
    if args.date and args.date != date_str:
        print(f"[gate] summary 日期 {date_str} 与期望 {args.date} 不符")
        print("GATE: continue（不是同一采集日，按未跑完处理）")
        return 1

    stats = data.get("cores") or {}
    print(f"[gate] 采集日 {date_str}（生成于 {data.get('generated_at', '-')}）")
    pending = []
    for core in cores:
        done, why = _core_done(stats.get(core))
        print(f"[gate]   {core:<8} {'完成' if done else '未完成'}：{why}")
        if not done:
            pending.append(core)

    if pending:
        print(f"GATE: continue（待补内核：{'、'.join(pending)}）")
        return 1
    print(f"GATE: done（{'、'.join(cores)} 今晚都已达既定口径，后续窗口不用跑）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
