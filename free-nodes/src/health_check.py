#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""free-nodes-collector 每日自检

采集 + 验证跑完后执行，机械地检查本次结果是否异常，输出可执行的改进建议。
不做任何修改动作，只做诊断——是否修复由调用方（自动化 agent）决定。

用法：
    python health_check.py --dir <输出根目录>
    python health_check.py --dir <输出根目录> --target-nodes 1000

输出（文档类全部在 Docs/ 子目录，md 日志按日期倒序累积）：
    Docs/health_check.md   人读报告（结论 + 指标 + 发现 + 建议动作）
    Docs/health_check.json 机读结果（最新一次）
    Docs/known-issues.md    末尾「自检发现」区块（按日期倒序，同一天重跑替换当天小节）
    Docs/review_logs.md     跨天摘要（按日期倒序）

退出码：0 = 健康，1 = 有告警，2 = 有严重问题
"""

import argparse
import base64
import glob
import json
import os
import re
import statistics
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import collect_nodes as c  # noqa: E402
import layout as lay  # noqa: E402
import pool as node_pool  # noqa: E402

# 内核可执行文件相对路径（统一用 layout.CORE_BIN，clash 对应 mihomo 内核）
CORE_BINS = dict(lay.CORE_BIN)

# 镜像探测用的固定小文件（稳定存在，几 KB）
PROBE_RAW = "https://raw.githubusercontent.com/octocat/Hello-World/master/README"


def default_tools_dir():
    return os.path.join(os.path.expanduser("~"), ".workbuddy", "data",
                        "free-nodes-tools", "bin")


def tools_dir():
    env = os.environ.get("FREE_NODES_TOOLS")
    if env:
        return env
    # 技能目录/tools/bin（旧布局）优先，否则用户数据目录
    legacy = os.path.join(os.path.dirname(SCRIPT_DIR), "tools", "bin")
    if os.path.isdir(legacy):
        return legacy
    return default_tools_dir()


# ---------------------------------------------------------------- 数据读取

def _lines_of_sub(path):
    """把订阅/清单文件还原成 URI 行列表。

    内部主清单 nodes_uris.txt 是**明文**，客户端订阅是 **base64**，
    两者都可能传进来。先看明文里有没有 `://`，没有再尝试 base64 解码。
    """
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    if "://" in raw:
        return [ln.strip() for ln in raw.splitlines() if "://" in ln]
    try:
        text = base64.b64decode(raw, validate=False).decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return []
    return [ln.strip() for ln in text.splitlines() if "://" in ln]


def read_sub_stats(path):
    """读取 URI 清单（明文或 base64），返回 (节点数, 协议分布, host 分布)。"""
    if not os.path.exists(path):
        return None
    uris = _lines_of_sub(path)
    schemes = Counter()
    hosts = Counter()
    for uri in uris:
        schemes[uri.split("://")[0].lower()] += 1
        parsed = c.parse_uri_hostport(uri)
        if parsed:
            hosts[parsed[1]] += 1
    return {"count": len(uris), "schemes": dict(schemes), "hosts": dict(hosts)}


# sing-box 的 outbounds 里除了节点还有 direct/block/dns/选择器等内置出站，
# 统计「节点数」时必须排除，否则永远比汇总多 1~2 个
_SINGBOX_NON_NODE = {"direct", "block", "dns", "selector", "urltest", "tor"}


def parse_collection_log(path):
    """解析 collection_logs.md，返回条目列表（按时间正序）。

    每条：{"header", "phases": {阶段名: {"declared", "repos": [(name, got, kind)]}},
           "raw", "uniq", "dropped"}
    kind: ok / zero（下载成功但无节点）/ fail（下载失败）/ nofile（无可候选文件）
    """
    if not os.path.exists(path):
        return []
    entries, cur = [], None
    phase = None
    for line in open(path, encoding="utf-8").read().splitlines():
        if line.startswith("## "):
            if cur:
                entries.append(cur)
            cur = {"header": line[3:].strip(), "phases": {}, "raw": None,
                   "uniq": None, "dropped": None, "readme_repos": 0, "readme_nodes": 0}
            phase = None
            continue
        if cur is None:
            continue
        m = re.match(r"^- (.+?) 仓库明细（(\d+) 个）", line.strip())
        if m:
            phase = m.group(1)
            cur["phases"][phase] = {"declared": int(m.group(2)), "repos": []}
            continue
        m = re.match(r"^\s+- (.+?)：(?:(\d+) 条|(无可候选文件|下载失败)|README 未声明订阅链接)", line)
        if m and phase:
            name = m.group(1).strip()
            if m.group(2) is not None:
                got = int(m.group(2))
                kind = "ok" if got > 0 else "zero"
            elif m.group(3) == "下载失败":
                got, kind = -1, "fail"
            elif m.group(3) == "无可候选文件":
                got, kind = None, "nofile"
            else:
                got, kind = None, "nolink"  # readme-only 模式下 README 没有订阅链接
            cur["phases"][phase]["repos"].append((name, got, kind))
            continue
        # README 声明链接明细：`  - repo：声明 3 个 → 提取 120 条`
        m = re.match(r"^\s+- (.+?)：声明 (\d+) 个 → 提取 (\d+) 条", line)
        if m:
            cur["readme_repos"] += 1
            cur["readme_nodes"] += int(m.group(3))
            continue
        m = re.search(r"原始 (\d+) 条.*?去重后 (\d+) 条（剔除 (\d+)）", line)
        if m:
            cur["raw"], cur["uniq"], cur["dropped"] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if cur:
        entries.append(cur)
    return entries


def read_summary(path):
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def read_core_file_count(path, core):
    """某个内核订阅/可用文件的节点数：base64 订阅 → 行数；clash → proxies 数；
    sing-box → outbounds 里**排除内置出站**后的数量。"""
    if not os.path.exists(path):
        return None
    if lay.CORE_FMT[lay.canon(core)] == "base64":
        st = read_sub_stats(path)
        return st["count"] if st else None
    data = read_json(path)
    if not isinstance(data, dict):
        return None
    if "proxies" in data:
        return len(data.get("proxies") or [])
    items = data.get("outbounds") or []
    return len([o for o in items if (o.get("type") or "") not in _SINGBOX_NON_NODE])


def summary_cores(summary):
    """summary.json 结构兼容：新版 {"date","cores":{...}}，旧版直接是 {core: st}。"""
    if not isinstance(summary, dict):
        return {}
    return summary.get("cores") if isinstance(summary.get("cores"), dict) else summary


def latest_entry(entries):
    """日志按日期倒序写在文件里，取最新一条要按 header 里的日期排，不能取末尾。"""
    if not entries:
        return None
    return max(entries, key=lambda e: e.get("header") or "")


def read_json(path):
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def parse_elapsed(report_path):
    if not os.path.exists(report_path):
        return None
    m = re.search(r"耗时：(\d+) 秒", open(report_path, encoding="utf-8").read())
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- 检查项

def check_outputs(find, root):
    """产物完整性：四内核各一个订阅文件 + 内部主清单 + 报告。"""
    uris_file = lay.uris_path(root)
    expect = [(uris_file, "内部主清单（验证输入）"), (lay.report_path(root), "采集报告")]
    expect += [(lay.sub_path(root, core), f"{core} 订阅") for core in lay.CORES]
    for path, desc in expect:
        if not os.path.exists(path):
            find("critical", "产物", f"缺少{desc} {os.path.relpath(path, root)}",
                 "采集未完成或输出被覆盖，需重跑采集")

    stats = read_sub_stats(uris_file)
    per_core = {core: read_core_file_count(lay.sub_path(root, core), core) for core in lay.CORES}
    shown = "、".join(f"{core} {v if v is not None else '-'}" for core, v in per_core.items())
    if stats:
        find("info", "产物", f"主清单 {stats['count']} 条；各内核订阅：{shown}", "")
        total = stats["count"]
        for core, n in per_core.items():
            if n == 0:
                find("warn", "产物", f"{core} 订阅文件为空（{lay.SUB_FILE[core]}）",
                     f"没有节点符合 {core} 的能力集合，检查 layout.CAPS 的能力矩阵是否过严，"
                     "或该内核支持的协议本次确实没采到")
            elif n is not None and n > total:
                find("warn", "产物", f"{core} 订阅节点数 {n} > 主清单 {total}",
                     "分流逻辑异常，检查 collect_nodes.write_outputs 的去重/过滤顺序")
    return stats, per_core


def check_scale(find, stats, target):
    n = stats["count"] if stats else 0
    if n == 0:
        find("critical", "规模", "本次采集到 0 条节点", "检查网络/镜像/GitHub 配额，重跑采集")
    elif n < target * 0.1:
        find("critical", "规模", f"节点数 {n} 远低于目标 {target}（<10%）", "大幅扩量：提高 --max-repos/--max-seeds，检查阶段 2/3 是否被配额门控跳过")
    elif n < target * 0.5:
        find("warn", "规模", f"节点数 {n} 低于目标 {target} 的一半", "扩量或补充种子仓库；如持续偏低，考虑放宽时间窗口")
    elif n < target:
        find("info", "规模", f"节点数 {n} 未达目标 {target}", "可选：提高 --max-repos 或补充清单仓库")
    else:
        find("info", "规模", f"节点数 {n} 达到目标 {target}", "")
    return n


def check_repo_yield(find, entries):
    """仓库产出率，并按失败类型给出针对性结论。

    三类失败原因完全不同，混在一起就无法定位：
      fail   = 拿到候选文件但下载失败（镜像截断/超时/大文件）
      zero   = 文件下载成功但解析不出节点（解析能力不足）
      nofile = 目录里没有可识别的候选文件（命名/子目录规则不足）
    """
    if not entries:
        find("warn", "仓库效率", "未找到采集日志，无法评估仓库产出率", "确认 collection_logs.md 是否正常写入")
        return
    last = latest_entry(entries)
    cnt = Counter()
    total = 0
    for ph in last["phases"].values():
        for _name, _got, kind in ph["repos"]:
            cnt[kind] += 1
            total += 1
    ok, zero, fail, nofile = cnt["ok"], cnt["zero"], cnt["fail"], cnt["nofile"]
    nolink = cnt["nolink"]          # readme-only 模式：README 没有订阅链接，主动跳过
    scanned = total - nolink
    rate = ok / scanned if scanned else 0
    detail = (f"扫描仓库 {total} 个：有产出 {ok}、解析不到节点 {zero}、"
              f"下载失败 {fail}、无候选文件 {nofile}"
              + (f"、README 无订阅链接跳过 {nolink}" if nolink else "")
              + f"（产出率 {rate:.0%}，按有尝试采集的 {scanned} 个计算）")
    if total < 5:
        find("info", "仓库效率", detail, "样本过少，暂不评估")
        return
    if rate >= 0.3:
        find("info", "仓库效率", detail, "")
    elif rate >= 0.1:
        find("warn", "仓库效率", detail, "产出率偏低，优先按下面细分的失败类型逐项处理")
    else:
        find("critical", "仓库效率", detail, "产出率极低，按下面细分的失败类型逐项处理")

    if total and fail / total > 0.25:
        find("critical", "下载通道", f"{fail}/{total} 个仓库的文件下载失败（{fail/total:.0%}）",
             "查 stderr 的 `下载失败` 行确认是超时还是截断；大文件（>2MB）应优先走 jsDelivr 并放宽超时，"
             "镜像列表用 health_check 的镜像探测结果剔除失效项")
    if total and zero / total > 0.35:
        find("critical", "解析能力", f"{zero}/{total} 个仓库下载成功但解析不出节点",
             "多半是格式没覆盖：检查 clash YAML（块状 proxies 需迷你解析器）、"
             "sing-box json 结构、以及新的 URI 变体；抓 1 个失败样本手工验证 extract 函数")
    if total and nofile / total > 0.35:
        find("warn", "文件识别", f"{nofile}/{total} 个仓库未识别到候选文件",
             "扩充候选文件名/扩展名规则，并对根目录无货的仓库扫描常见子目录"
             "（Subscriptions/、source/、output/ 等）")
    if nolink and nolink / total > 0.6:
        find("info", "README 采集",
             f"{nolink}/{total} 个仓库的 README 没有订阅链接，已被 readme-only 模式跳过",
             "这是 readme-only 的预期行为（不扫描仓库目录）；若节点数明显不够，"
             "可去掉 --readme-only 恢复目录扫描，或放宽 README 链接识别规则")


def check_seed_drop(find, entries, seed_file):
    """种子仓库掉线：历史贡献高但本次 0 条，通常是下载失败或解析退化。"""
    seed = read_json(seed_file)
    if not seed or not entries:
        return
    last = latest_entry(entries)
    today = {}
    kinds = {}
    for ph in last["phases"].values():
        for name, got, kind in ph["repos"]:
            today[name] = today.get(name, 0) + (got if isinstance(got, int) and got > 0 else 0)
            kinds[name] = kind
    dropped = []
    for r in seed.get("repos", []):
        name = r.get("full_name")
        contributed = r.get("contributed") or 0
        if contributed < 100 or name not in today:
            continue
        if today[name] == 0:
            dropped.append((name, contributed, kinds.get(name, "")))
    if dropped:
        dropped.sort(key=lambda x: -x[1])
        reason = {"fail": "下载失败", "zero": "解析不到节点", "nofile": "无候选文件",
                  "nolink": "README 无订阅链接"}
        names = "、".join(f"{n}(历史 {v} 条, {reason.get(k, k)})" for n, v, k in dropped[:5])
        find("warn", "来源稳定性", f"{len(dropped)} 个高贡献仓库本次 0 条：{names}",
             "按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，"
             "无候选文件查命名/子目录规则；都不是则属上游停更，无需处理")


def check_tests(find, root, summary, stats):
    """验证环节：是否执行、各内核可用率、可用文件与汇总是否一致。"""
    if summary is None:
        find("critical", "验证", "未找到 summary.json，可用性验证未执行或失败",
             "检查内核是否缺失、test_nodes.py 是否报错；补跑 test_nodes.py")
        return {}
    tools = tools_dir()
    for core, (sub, exe) in CORE_BINS.items():
        if not os.path.exists(os.path.join(tools, sub, exe)):
            find("warn", "验证", f"内核缺失：{core}（{os.path.join(tools, sub, exe)}）",
                 "重新下载该内核，或从验证列表移除该内核")
    rate_by_core = {}
    for core, st in summary_cores(summary).items():
        if st is None:
            find("warn", "验证", f"{core} 因内核缺失被跳过", "部署内核后可覆盖该内核协议")
            continue
        tested, ok = st.get("tested", 0), st.get("ok", 0)
        if tested == 0:
            find("critical", "验证", f"{core} 测试 0 个节点", "检查该内核协议匹配与 TCP 预筛结果")
            continue
        rate = ok / tested
        rate_by_core[core] = rate
        if ok == 0:
            find("critical", "验证", f"{core} 可用 0 个（测试 {tested} 个）",
                 "内核启动/配置生成可能全线失败：单独跑 1 个节点并打开内核日志定位"
                 "（常见原因：reality 缺 reality-opts/utls、TLS 证书校验未跳过、并发数据目录冲突）")
        elif rate < 0.03:
            find("warn", "验证", f"{core} 可用率异常低 {rate:.1%}（{ok}/{tested}）",
                 "同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。"
                 "注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准")
        elif ok < 10:
            if st.get("policy") == "full":
                # 全量模式：候选 ≤ full_below 已全部测完，或超过 max_test 被截断
                if st.get("exhausted"):
                    find("info", "验证",
                         f"{core} 仅 {ok} 个可用（候选 {st.get('cand')} 个已全部测完）",
                         "全量测试已无优化空间：免费节点本身失效严重，需要扩大采集来源"
                         "（提高 --target-nodes、补充高 star 种子仓库），继续堆测试量没有收益")
                else:
                    find("warn", "验证",
                         f"{core} 仅 {ok} 个可用（候选 {st.get('cand')} 个，"
                         f"已按上限 {st.get('cap')} 截断测试）",
                         "候选数超过 --max-test 被截断：确认是否要调大 --max-test；"
                         "若已全测仍这么少，属源池质量问题，不要堆测试量")
            else:
                rounds = st.get("rounds") or 1
                escaped = f"扩量 {rounds} 轮、共测 {tested} 个" if rounds > 1 else f"测试 {tested} 个"
                if st.get("exhausted"):
                    # 扩量已经把候选节点测完了还不足 10 个 → 验证环节已尽力，问题在源池
                    find("info", "验证",
                         f"{core} 仅 {ok} 个可用（{escaped}，候选 {st.get('cand')} 个已全部测完）",
                         "验证侧已无优化空间：免费节点本身失效严重，需要扩大采集来源"
                         "（提高 --target-nodes、补充高 star 种子仓库），继续堆测试量没有收益")
                else:
                    find("warn", "验证",
                         f"{core} 仅 {ok} 个可用（{escaped}，候选还没测完）",
                         "自适应扩量未达标但提前停了：多为触到 --test-limit-cap 或时间预算，"
                         "可调大 --test-limit-cap / --escalate-budget 后重跑 test_nodes.py")
        # 可用文件与 summary 一致性（每个内核只有 1 个文件，格式由内核决定）
        fname = lay.AVAIL_FILE[lay.canon(core)]
        f = lay.avail_path(root, core)
        if not os.path.exists(f):
            find("warn", "验证", f"{core} 缺少可用文件 {fname}", "确认 write_core_outputs 是否正常返回")
            continue
        got = read_core_file_count(f, core)
        if got is None:
            find("critical", "验证", f"{core} 的 {fname} 无法解析", "检查写出逻辑（base64 / json 是否损坏）")
        elif got != ok:
            find("warn", "验证", f"{core} 文件条数 {got} ≠ 汇总可用数 {ok}", "汇总与文件写出不一致，需排查")
    return rate_by_core


def check_source_concentration(find, stats):
    if not stats or not stats["count"]:
        return
    hosts = stats["hosts"]
    top, cnt = max(hosts.items(), key=lambda kv: kv[1])
    share = cnt / stats["count"]
    if len(hosts) >= 10 and share > 0.5:
        find("warn", "来源质量", f"单一服务器 {top} 占 {share:.0%}（{cnt}/{stats['count']}）",
             "节点来源过于集中，同源节点同时失效风险高；扩大关键词或提高仓库多样性")
    uniform = sum(1 for v in hosts.values() if v > 1)
    if stats["count"] > 50 and uniform == 0:
        find("info", "来源质量", "所有节点服务器地址互不相同", "来源分散正常")


def check_protocols(find, stats):
    if not stats:
        return
    have = stats["schemes"]
    missing = [p for p in ("vless", "vmess", "trojan", "ss") if p not in have]
    if missing:
        find("warn", "协议覆盖", f"本次缺少常见协议：{'、'.join(missing)}",
             "部分客户端只支持特定协议，若持续缺失需检查解析器是否漏掉该协议")
    if have and len(have) >= 1:
        top, cnt = max(have.items(), key=lambda kv: kv[1])
        if cnt / stats["count"] > 0.85:
            find("info", "协议覆盖", f"协议高度集中在 {top}（{cnt}/{stats['count']}）",
                 "可接受，但注意多数客户端对该协议的支持情况")


def check_mirrors(find):
    """下载通道可用性：raw 直连被墙时全靠镜像 + jsDelivr，两路都要有活的。"""
    base = c._base_mirrors()
    if not base:
        find("info", "下载通道", "镜像前缀列表为空（已禁用镜像）",
             "若 raw 直连经常失败，建议启用 gh-proxy.com")
        return
    alive, dead = c.refresh_mirror_state()
    cdn_alive = c.get_cdn_hosts(fallback=False)   # 报告要真实可用数，不能带兜底节点
    total_cdn = len(c.JSDELIVR_HOSTS)
    raw_ok = bool(c.raw_alive())

    if dead and not alive and not raw_ok:
        find("critical", "下载通道", f"镜像与 raw 直连全部不可用：{'、'.join(dead)}",
             "三条通道都没了，采集会大面积失败。换网络环境后重跑本检查，"
             "或通过 FREE_NODES_MIRRORS 指定可用代理")
    elif dead and not alive:
        find("info", "下载通道",
             f"镜像全部失效（{len(dead)} 个），raw 直连可用",
             "死镜像已从下载链剔除，raw 直连可承担下载；若后续 raw 也被墙则无退路")
    elif dead:
        find("warn", "下载通道",
             f"镜像失效 {len(dead)}/{len(base)}：{'、'.join(dead)}；可用：{'、'.join(alive)}",
             "失效项已从下载链剔除（不再逐个重试），本次不影响采集。"
             "若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选")
    else:
        find("info", "下载通道", f"镜像全部可用（{len(alive)} 个）", "")

    # jsDelivr 是大文件回退链的主通道，单独判定（cdn.jsdelivr.net 常被墙，
    # 但 fastly / gcore 通常仍可达，四节点全挂才需要报警）
    if not cdn_alive:
        find("warn", "下载通道", f"jsDelivr 边缘节点探活全失败（{total_cdn} 个）",
             "本轮下载仍会按保底顺序尝试这些节点（探活有抖动，不能直接判死），"
             "但若真实全挂，大文件（>2MB）只剩镜像代理，极易被截断；换网络后重跑确认")
    elif len(cdn_alive) < total_cdn:
        lost = [h for h in c.JSDELIVR_HOSTS if h not in cdn_alive]
        find("info", "下载通道",
             f"jsDelivr 可用 {len(cdn_alive)}/{total_cdn}：{'、'.join(cdn_alive)}"
             f"（不可达：{'、'.join(lost)}）", "")
    else:
        find("info", "下载通道", f"jsDelivr 四节点全部可用", "")


def check_quota(find):
    try:
        d = c.github_api("/rate_limit")
        core = d["resources"]["core"]
        search = d["resources"]["search"]
        token = bool(os.environ.get("GITHUB_TOKEN"))
        msg = (f"GitHub 配额剩余 core {core['remaining']}/{core['limit']}、"
               f"search {search['remaining']}/{search['limit']}（{'已配置 token' if token else '匿名'}）")
        if not token and core["remaining"] < 20:
            find("warn", "配额", msg, "匿名配额紧张，采集可能被截断；建议给自动化配置 GITHUB_TOKEN")
        else:
            find("info", "配额", msg, "" if core["remaining"] >= 20 else "配额偏低，注意阶段 2/3 可能被跳过")
    except Exception as e:  # noqa: BLE001
        find("warn", "配额", f"无法查询 GitHub 配额：{str(e)[:80]}", "检查网络；配额查询失败也意味着 API 调用可能不稳")


def check_trend(find, entries, today_uniq):
    latest = latest_entry(entries)
    hist = [e["uniq"] for e in entries if e is not latest and e.get("uniq")]
    if len(hist) < 2 or not today_uniq:
        return
    med = statistics.median(hist[-7:])
    if med and today_uniq < med * 0.4:
        find("warn", "趋势", f"今日 {today_uniq} 条，近几日中位数 {med:.0f} 条（降幅 >60%）",
             "对比近几日 collection_log，确认是上游整体减产还是本次采集/解析退化")


def check_elapsed(find, elapsed):
    if elapsed is None:
        return
    if elapsed > 2700:
        find("warn", "性能", f"采集耗时 {elapsed/60:.0f} 分钟（>45 分钟）",
             "多为镜像/CDN 慢速传输：调小超时、跳过超大文件、或减少每仓库候选文件数")
    elif elapsed > 1800:
        find("info", "性能", f"采集耗时 {elapsed/60:.0f} 分钟", "偏慢，可关注是否有大文件反复重试")


def check_dedupe(find, entries):
    if not entries:
        return
    last = latest_entry(entries)
    if last.get("raw") and last.get("dropped") is not None:
        ratio = last["dropped"] / last["raw"]
        if ratio > 0.95:
            find("info", "去重", f"去重剔除 {ratio:.0%}（{last['dropped']}/{last['raw']}）",
                 "重复度极高：说明多个仓库共享同一上游源，可减少同类仓库扫描以省配额")


def check_readme_harvest(find, entries):
    """README 订阅链接：本次有多少仓库声明了链接、从中拿到多少节点。

    README 是很多仓库唯一的真实订阅入口，这条链路断了会直接少掉一大块来源。
    """
    if not entries:
        return
    last = latest_entry(entries)
    declared = last.get("readme_repos") or 0
    nodes = last.get("readme_nodes") or 0
    scanned = sum(len(ph["repos"]) for ph in last["phases"].values())
    if not scanned:
        return
    if declared == 0:
        find("warn", "README 采集", f"扫描 {scanned} 个仓库，没有任何 README 被识别出订阅链接",
             "① 确认仓库 README 已抓到（看 stderr 是否有 README 下载失败）；"
             "② md_l 链接正则/he 分类规则可能过严，用 1 个已知仓库的 README 单点验证 "
             "collect_nodes.extract_readme_links")
    elif nodes == 0:
        find("warn", "README 采集", f"{declared} 个仓库声明了订阅链接，但一条节点都没提取出来",
             "链接能识别但内容解析失败：抓 1 个链接手工下载，确认是 HTML 页面还是真实订阅内容，"
             "必要时补 UA / 跟随重定向")
    elif declared / scanned < 0.05 and scanned >= 20:
        find("info", "README 采集", f"仅 {declared}/{scanned} 个仓库识别到 README 订阅链接",
             "比例偏低：检查链接分类是否漏掉子目录/相对路径写法")
    else:
        find("info", "README 采集", f"{declared} 个仓库的 README 声明了订阅链接，提取 {nodes} 条节点", "")


def check_latency(find, out_dir):
    """TCP 延迟探测与排序：文件是否生成、可达率、是否真的按延迟升序。"""
    path = lay.meta_path(out_dir)
    data = read_json(path)
    if not data:
        find("warn", "延迟排序", f"未找到 {os.path.relpath(path, out_dir)}，本次未做 TCP 延迟探测",
             "确认采集参数没有加 --no-latency-sort；该文件同时承载仓库归属，缺了会连带仓库质量考核失效")
        return None
    lat = data.get("latency") or {}
    total, reachable = data.get("total", 0), data.get("reachable", 0)
    buckets = lat.get("buckets") or {}
    if not total:
        return None
    share = reachable / total
    detail = (f"{reachable}/{total} 个服务器 TCP 可达（{share:.0%}），"
              f"延迟中位数 {lat.get('median')}ms，<100ms 共 {buckets.get('<100ms', 0)} 条")
    if reachable == 0:
        find("critical", "延迟排序", "所有节点 TCP 均不可达", "网络出口异常或节点集体失效，先确认本机连通性")
    elif share < 0.05:
        find("warn", "延迟排序", detail, "可达率极低属正常现象之一（免费节点失效快），"
             "但若持续 <5% 需确认探测参数（超时 1.5s 对高延迟线路偏严，可放宽到 2.5s）")
    else:
        find("info", "延迟排序", detail, "")

    cf = data.get("cf_fronted") or 0
    if cf:
        find("info", "延迟排序",
             f"{cf}/{total} 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后",
             "" if cf / total < 0.5 else "CF 前置占比过半：来源严重同质化，建议优先采非 CF 直连节点多的仓库")

    # 校验订阅真的按延迟升序（前 50 条里出现不可达说明排序没生效）
    meta_nodes = data.get("nodes") or []
    dead_in_head = sum(1 for n in meta_nodes[:50] if n.get("tcp_latency") is None)
    if dead_in_head > 10:
        find("warn", "延迟排序", f"订阅前 50 条里有 {dead_in_head} 条不可达节点",
             "排序应在写订阅前执行，检查 main() 中 probe_latencies → sort → write_outputs 的顺序")
    return {"reachable": reachable, "total": total, "median": lat.get("median")}


def check_pool(find, root):
    """可用节点池：每个内核 1 个池文件 + 1 个共享状态文件。"""
    pdir = lay.pool_dir(root)
    if not os.path.isdir(pdir):
        find("warn", "节点池", "未找到可用节点池目录 pool/",
             "验证阶段应写入 <root>/pool/pool_<core>.<ext>；确认 test_nodes.py 未加 --no-pool")
        return {}
    state = node_pool.load_state(root)
    info = {}
    for core in lay.CORES:
        n = len(node_pool.load(state, core).get("nodes") or [])
        info[core] = n
        if not os.path.exists(lay.pool_path(root, core)):
            find("warn", "节点池", f"{core} 缺少池文件 {lay.POOL_FILE[core]}",
                 "确认 pool.save 是否报错（权限/格式转换失败）")
        elif n == 0:
            find("warn", "节点池", f"{core} 节点池为空", "该内核当天无可用节点入池，检查验证环节")
    if not os.path.exists(lay.pool_state_path(root)):
        find("warn", "节点池", "缺少 pool_state.json（池元数据）",
             "复测优先级与淘汰策略依赖这份元数据；确认 pool.save_state 正常")
    if info:
        find("info", "节点池", "池内节点：" + "、".join(f"{k} {v}" for k, v in info.items()), "")
    return info


def check_repo_quality(find, seed_file):
    """仓库质量：是否已建立可用率评分，以及低质量仓库占比。"""
    seed = read_json(seed_file)
    if not seed:
        return {}
    repos = seed.get("repos", [])
    scored = [r for r in repos if r.get("tested")]
    if not scored:
        find("warn", "仓库质量", "仓库清单里没有任何实测可用率",
             "test_nodes.py 应在四内核实测后回写 quality/avail_rate；确认 --seed-file 指向正确且 nodes_meta.json 有 repo 字段")
        return {}
    bad = [r for r in scored if (r.get("ok") or 0) == 0 and (r.get("tested") or 0) >= 20]
    good = [r for r in scored if (r.get("avail_rate") or 0) >= 0.1]
    detail = (f"已评分 {len(scored)} 个仓库，可用率 >=10% 的 {len(good)} 个，"
              f"长期 0 可用 {len(bad)} 个（下次采集会自动跳过）")
    if bad and len(bad) / len(scored) > 0.5:
        find("warn", "仓库质量", detail,
             "过半仓库实测 0 可用：多为纯聚合转发站或已死源，建议提高 min-stars 或只用高质量清单仓库")
    else:
        find("info", "仓库质量", detail, "")
    return {r["full_name"]: r.get("quality") for r in scored[:10]}


# ---------------------------------------------------------------- 输出

def write_reports(root, findings, metrics, entries, args):
    level_rank = {"critical": 0, "warn": 1, "info": 2}
    findings = sorted(findings, key=lambda f: level_rank.get(f["level"], 3))
    n_crit = sum(1 for f in findings if f["level"] == "critical")
    n_warn = sum(1 for f in findings if f["level"] == "warn")
    if n_crit:
        verdict = f"发现 {n_crit} 个严重问题、{n_warn} 个告警，需要处理"
    elif n_warn:
        verdict = f"无严重问题，{n_warn} 个告警可优化"
    else:
        verdict = "本次运行健康，未发现需要处理的问题"

    now = datetime.now(timezone(timedelta(hours=8)))
    date_str = args.date or now.strftime("%Y-%m-%d")
    lines = [f"**结论：{verdict}**", "",
             "### 关键指标", "", "| 指标 | 值 |", "|---|---|"]
    for k, v in metrics.items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "### 发现与建议", ""]
    if not findings:
        lines.append("无。")
    else:
        for f in findings:
            icon = {"critical": "🔴", "warn": "🟡", "info": "🔵"}[f["level"]]
            lines.append(f"#### {icon} [{f['area']}] {f['title']}")
            lines.append("")
            if f.get("action"):
                lines.append(f"- 建议动作：{f['action']}")
            lines.append("")
    todo = [f for f in findings if f["level"] in ("critical", "warn") and f.get("action")]
    lines += ["### 待办清单（需人工或自动修复）", ""]
    if not todo:
        lines.append("无——本次无需修复。")
    else:
        for i, f in enumerate(todo, 1):
            lines.append(f"{i}. [{f['level']}] {f['title']} → {f['action']}")
    lines.append("")

    # health_check.md：按日期倒序累积（同一天重跑替换当天小节）
    md_path = lay.upsert_section(lay.health_path(root), date_str,
                                 now.strftime("%H:%M"), "\n".join(lines),
                                 doc_title="每日自检报告（时间倒序）",
                                 intro="按日期倒序累积，最新一次运行在最上面")
    json_path = lay.health_json_path(root)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"generated_at": now.isoformat(timespec="seconds"), "date": date_str,
                   "verdict": verdict, "metrics": metrics,
                   "findings": findings, "todo": todo}, fh, ensure_ascii=False, indent=1)

    # known-issues.md 末尾「自检发现」区块：自检发现的问题统一记在这里（按日期倒序）
    issue_lines = [f"**结论：{verdict}**", ""]
    if todo:
        issue_lines.append("| 级别 | 领域 | 问题 | 建议动作 |")
        issue_lines.append("|---|---|---|---|")
        for f in todo:
            issue_lines.append(f"| {f['level']} | {f['area']} | {f['title']} | {f['action']} |")
    else:
        issue_lines.append("本次自检未发现需要修复的问题。")
    watch = [f for f in findings if f["level"] == "info" and f.get("action")]
    if watch:
        issue_lines += ["", "待观察（info）："]
        issue_lines += [f"- [{f['area']}] {f['title']}" for f in watch]
    # 标题固定为「自检发现」：同一天重跑替换当天该节，不按分钟累积出一堆碎片小节
    lay.append_issue(root, date_str, "自检发现", "\n".join(issue_lines))

    # review_logs.md：跨天摘要（按日期倒序，一天一节 = 当天最后一次自检的结论）
    ok_metric = metrics.get("各内核可用")
    ok_txt = "/".join(str(v) for v in ok_metric.values()) if isinstance(ok_metric, dict) else "-"
    # match_heading=True：只替换「同日期 + 同标题」的自动摘要小节。
    # 之前用默认的「同日期」判重（startswith("## <date>")），会把同一天手写的
    # 「## 2026-10-27 第二窗口（…）」整段误删——手写小节标题同样以日期开头，
    # 被当成旧摘要覆盖（2026-10-27 第三窗口实测丢失，已从 git 恢复）。
    lay.upsert_section(lay.review_log_path(root), date_str, "自检摘要",
                       f"- 去重后节点：{metrics.get('去重后节点', '-')}"
                       f"（目标 {metrics.get('目标节点', '-')}）\n"
                       f"- 各内核可用：{ok_txt}\n"
                       f"- 结论：{verdict}；待修复 {len(todo)} 项",
                       doc_title="每日采集自检日志（时间倒序）",
                       intro="跨天摘要，按日期倒序",
                       match_heading=True)

    return md_path, json_path, n_crit, n_warn


def main():
    ap = argparse.ArgumentParser(description="采集结果自检：机械评估本次运行是否异常")
    ap.add_argument("--dir", default=None, help="输出根目录（默认 ./free-nodes）")
    ap.add_argument("--target-nodes", type=int, default=1000, help="目标节点数（与采集一致）")
    ap.add_argument("--date", default=None, help="日期标记 YYYY-MM-DD（默认今天）")
    ap.add_argument("--skip-network", action="store_true", help="跳过镜像/配额探测（离线快速模式）")
    args = ap.parse_args()

    tz = timezone(timedelta(hours=8))
    today = datetime.now(tz).strftime("%Y-%m-%d")
    root = os.path.abspath(args.dir or "free-nodes")
    args.date = args.date or today
    if not os.path.isdir(root):
        print(f"[error] 输出目录不存在：{root}", file=sys.stderr)
        sys.exit(2)

    findings = []

    def find(level, area, title, action=""):
        findings.append({"level": level, "area": area, "title": title, "action": action})

    log_path = lay.collection_log_path(root)
    seed_file = lay.seed_file_path(root)

    stats, per_core = check_outputs(find, root)
    n = check_scale(find, stats, args.target_nodes)
    entries = parse_collection_log(log_path)
    check_repo_yield(find, entries)
    check_seed_drop(find, entries, seed_file)
    check_readme_harvest(find, entries)
    latency = check_latency(find, root)
    check_repo_quality(find, seed_file)
    pool_sizes = check_pool(find, root)
    summary = read_summary(lay.summary_json_path(root))
    rate_by_core = check_tests(find, root, summary, stats)
    check_source_concentration(find, stats)
    check_protocols(find, stats)
    check_trend(find, entries, n)
    check_dedupe(find, entries)
    check_elapsed(find, parse_elapsed(lay.report_path(root)))
    if not args.skip_network:
        check_mirrors(find)
        check_quota(find)

    metrics = {
        "输出目录": root,
        "目标节点": args.target_nodes,
        "去重后节点": n,
        "各内核订阅": "、".join(f"{k} {v if v is not None else '-'}"
                          for k, v in (per_core or {}).items()) or "-",
        "协议分布": " / ".join(f"{k} {v}" for k, v in sorted((stats or {}).get("schemes", {}).items())) or "-",
        "TCP 可达": (f"{latency['reachable']}/{latency['total']}（中位数 {latency['median']}ms）"
                    if latency else "-"),
        "验证已执行": "是" if summary else "否",
        "各内核可用": ({core: f"{st.get('ok', 0)}/{st.get('tested', 0)}"
                    for core, st in summary_cores(summary).items() if st} or "-"),
        "可用节点池": ("、".join(f"{k} {v}" for k, v in pool_sizes.items()) or "-"),
    }
    md_path, json_path, n_crit, n_warn = write_reports(root, findings, metrics, entries, args)

    print(f"[info] 自检完成：严重 {n_crit} / 告警 {n_warn} / 建议 {len(findings) - n_crit - n_warn}")
    for f in [x for x in findings if x["level"] in ("critical", "warn")]:
        print(f"  [{f['level']}] [{f['area']}] {f['title']}")
    print(f"[done] 报告：{md_path}")
    print(f"[done] 机读：{json_path}")
    print(f"[done] 问题清单：{lay.issue_path(root)}")
    sys.exit(2 if n_crit else (1 if n_warn else 0))


if __name__ == "__main__":
    main()
