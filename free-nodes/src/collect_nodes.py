#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_nodes.py — 每日免费节点采集合并脚本（纯标准库，无第三方依赖）

流程：
1. 通过 GitHub Search API 查找当天（最近 24h）有更新的 v2ray/clash/singbox 相关仓库
2. 抓取仓库根目录中的候选节点订阅文件（.txt/.yaml/.yml/.json/.list/.log）
3. 提取节点：URI 链接（vmess/vless/trojan/ss/ssr/hysteria2/tuic）、clash proxies、sing-box outbounds
4. 两级去重：先按完整链接去重，再按 服务器地址:端口 去重
5. 按四个内核（v2ray / xray / clash / singbox）各自支持的协议、传输层、加密方式分流，输出：
   - nodes/v2ray_sub.txt    v2ray 可处理的节点（base64 订阅）
   - nodes/xray_sub.txt     xray 可处理的节点（base64 订阅，与 v2ray 同源订阅，按 xray 能力多保留 REALITY/flow 节点）
   - nodes/clash_sub.yaml   clash/mihomo 可用节点（clash 配置）
   - nodes/singbox_sub.json sing-box 可用节点（sing-box outbounds）
   - nodes/nodes_uris.txt   内部主清单（全部唯一 URI，供验证阶段按内核能力取样）
   - nodes/nodes_meta.json  节点元数据（TCP 延迟 + 来源仓库）
   - Docs/report.md         采集报告（按日期倒序累积）
   - Docs/collection_logs.md 采集日志（按日期倒序累积）
   - src/seed_repos.json    动态仓库清单（贡献数 + 质量分，采集优先级依据）

用法：
    python collect_nodes.py [--out 输出目录] [--token GITHUB_TOKEN] [--max-repos 25] [--min-stars 0]

环境变量：GITHUB_TOKEN 可选，提供后可突破 GitHub 匿名 API 限额。
"""

import argparse
import atexit
import base64
import binascii
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# uplink 内部反向 import 本模块，必须延迟导入（放在 main() 里），否则循环导入
import layout as lay  # 统一布局：四内核命名/文件格式/能力矩阵/md 日志（无反向依赖）

# ---------------------------------------------------------------- SSL 上下文（三级回退）
# 受管 Python 可能缺少 CA 证书库：certifi → Windows 证书存储 → 不校验（带警告）


def _build_ssl_context():
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    try:
        ctx = ssl.create_default_context()
        loaded = 0
        for store in ("CA", "ROOT"):
            for cert, _enc, _trust in ssl.enum_certificates(store):
                ctx.load_verify_locations(cadata=ssl.DER_cert_to_PEM_cert(cert))
                loaded += 1
        if loaded:
            return ctx
    except Exception:  # noqa: BLE001
        pass
    return ssl.create_default_context()


_SSL_CTX = _build_ssl_context()
_NOVERIFY_CTX = ssl._create_unverified_context()
_SSL_WARNED = [False]


class EmptyBody(Exception):
    """HTTP 200 但正文 0 字节。

    2026-10-30 实测：gh-proxy 镜像与 jsDelivr 的 fastly/gcore 边缘对
    `free-nodes/clashfree/clash20261030.yml`（688KB，真实存在）都返回 200 + 0 字节，
    而 testingcf 边缘能给出完整内容。旧代码把空正文当成功，于是整仓「下载成功但
    解析不到节点」——历史 324 条的仓库连续归零，日志里还看不出是通道问题。
    """


def _build_direct_opener(ctx):
    """强制直连的 opener（显式空 ProxyHandler，忽略 HTTP(S)_PROXY 环境变量）。"""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}),
                                       urllib.request.HTTPSHandler(context=ctx))


_DIRECT_OPENER = _build_direct_opener(_SSL_CTX)
_DIRECT_OPENER_NOVERIFY = _build_direct_opener(_NOVERIFY_CTX)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) free-nodes-collector/1.0"
API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"

# GitHub token 的本地凭据文件（放在用户数据目录，**绝不在 git 仓库里**）
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "data",
                          "free-nodes-tools", "github_token.txt")


def load_github_token(cli_token=None):
    """token 优先级：--token > GITHUB_TOKEN/GH_TOKEN 环境变量 > 本地凭据文件。

    匿名额度是核心 60 次/时、搜索 10 次/分；带 token 分别升到 5000 次/时、30 次/分，
    这直接决定了能扫多少个仓库，所以把这个查找链写进脚本，不要求每次手敲 --token。
    任何情况下都不打印 token 本身。
    """
    if cli_token and cli_token.strip():
        return cli_token.strip()
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            val = f.read().strip()
        if val and not val.startswith("#"):
            return val
    except OSError:
        pass
    return None


def token_desc(token):
    """把 token 打码成前 4 + 后 4，用于日志确认「用的是哪个身份」而不泄露。"""
    if not token:
        return "匿名"
    return f"{token[:4]}…{token[-4:]}" if len(token) > 10 else "***"


# raw 加速镜像前缀候选池（raw 无法直连时按序尝试，前缀 + 完整 raw URL 的拼接方式）
# 可通过环境变量 FREE_NODES_MIRRORS 覆盖（逗号分隔，留空表示禁用）
# 注意：这些公共代理的存活率极低且随网络环境剧烈变化（实测同一批域名在不同出口下
# 可用数从 1/11 到 7/11 不等），所以这里是**候选池**而不是可信清单——真正决定
# 下载用哪些的是每轮运行的探活结果（refresh_mirror_state）。
DEFAULT_MIRROR_PREFIXES = [
    "https://gh-proxy.com/",
    "https://gh-proxy.org/",
    "https://gh.monlor.com/",
    "https://ghfast.top/",
    "https://ghproxy.net/",
    "https://gh-proxy.net/",
    "https://hub.gitmirror.com/",
    "https://gh.llkk.cc/",
    "https://gitdl.cn/",
    "https://ghproxy.cc/",
    "https://ghp.ci/",
    "https://ghps.cc/",
    "https://raw.gitmirror.com/",
]

# 备用候选：默认不进下载链，只在探活后「主清单存活镜像 < 2 个」时补测一次。
# 主清单会成批烂掉——2026-10-24 实测 13 个候选只剩 1 个活，其余多数直接 DNS 解析失败；
# 这里只放「域名能解析、当前被墙/限流/403」的站点：出口网络变化时有救回机会，
# 已确认 DNS 不存在的域名不收（补测纯属浪费 12s 超时）。
MIRROR_SPARE_CANDIDATES = [
    "https://github.moeyy.xyz/",
    "https://mirror.ghproxy.com/",
    "https://ghfast.xyz/",
    "https://ghproxy.imciel.com/",
    "https://gitproxy.click/",
    "https://ghproxy.1888866.xyz/",
    "https://gh.imbx.workers.dev/",
    "https://gh.nxnow.top/",
    "https://gh.yylh.xyz/",
    "https://ghproxy.liuzhicong.com/",
    "https://ghproxy.crazypeace.workers.dev/",
    "https://gh.h233.eu.org/",
    "https://gh-proxy.moyu.im/",
]

# jsDelivr 边缘节点：大文件回退链的主通道。
# 不能写死单个域名——cdn.jsdelivr.net 在部分网络被 DNS/SNI 阻断，
# 而同一套内容的 fastly / gcore 节点仍然可用（实测 cdn 挂、fastly+gcore 通）。
JSDELIVR_HOSTS = [
    "fastly.jsdelivr.net",
    "gcore.jsdelivr.net",
    "cdn.jsdelivr.net",
    "testingcf.jsdelivr.net",
]

# 通道探测状态（镜像 + jsDelivr 边缘节点，每轮运行自动刷新）
MIRROR_STATE_FILE = os.path.join(
    os.path.expanduser("~"), ".workbuddy", "data", "free-nodes-tools", "mirrors_state.json"
)
MIRROR_PROBE_FILE = "https://raw.githubusercontent.com/octocat/Hello-World/master/README"
CDN_PROBE_TMPL = "https://{host}/gh/octocat/Hello-World@master/README"
# 探活结果的有效期；超过则认为网络环境可能已变，重新全量探测
CHANNEL_STATE_TTL = 24 * 3600


def _base_mirrors():
    env = os.environ.get("FREE_NODES_MIRRORS")
    if env is not None:
        return [m.strip().rstrip("/") + "/" for m in env.split(",") if m.strip()]
    return list(DEFAULT_MIRROR_PREFIXES)


def _load_channel_state():
    """读取未过期的探活结果；不存在或已过期返回 None（调用方按"未探测"处理）。"""
    try:
        with open(MIRROR_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if time.time() - float(state.get("checked_ts") or 0) > CHANNEL_STATE_TTL:
            return None
        return state
    except (OSError, ValueError, TypeError):
        return None


def get_mirror_prefixes():
    """**下载用**镜像前缀：只返回探活通过的。

    探活过但全挂时返回空列表——继续拿死镜像逐个重试，会让每个下载失败的文件
    多空等 N×timeout 秒（实测 5 个死镜像 × 20s ≈ 100s/文件），比直接走
    raw 直连 + jsDelivr 糟糕得多。未探测过时才退回全量候选池。
    备用候选（MIRROR_SPARE_CANDIDATES）探活通过后同样可用，所以白名单要一并放行。
    """
    base = _base_mirrors()
    if not base:
        return []
    state = _load_channel_state()
    if state is None:
        return base
    allowed = set(base) | set(MIRROR_SPARE_CANDIDATES)
    return [m for m in state.get("alive", []) if m in allowed]


def get_cdn_hosts(fallback=True):
    """jsDelivr 边缘节点，探活通过的排前面。

    与镜像不同，这里**保留**探活失败的节点兜底（fallback=True）：
    jsDelivr 探活本身有抖动（同一批节点实测能在 1/4 和 3/4 之间波动），
    而四节点内容完全相同、单个成本低，全判死会让大文件通道直接断掉。
    只有前面全都不行时才会走到保底节点。
    """
    state = _load_channel_state()
    if state is None:
        return list(JSDELIVR_HOSTS)
    alive = [h for h in state.get("cdn_alive", []) if h in JSDELIVR_HOSTS]
    if not fallback:
        return alive
    return alive + [h for h in JSDELIVR_HOSTS if h not in alive]


def raw_alive():
    """raw 直连是否可用：True/False，未探测过返回 None（当作未知，先试一次）。"""
    state = _load_channel_state()
    if state is None or "raw_alive" not in state:
        return None
    return bool(state["raw_alive"])


def refresh_mirror_state(timeout=12):
    """并发探测 raw 镜像与 jsDelivr 边缘节点，结果落盘供下载链使用。"""
    base = _base_mirrors()
    alive, dead = [], []
    cdn_alive, cdn_dead = [], []

    def _probe_mirror(prefix):
        try:
            text = http_get_text(prefix + MIRROR_PROBE_FILE, retries=0, timeout=timeout)
            return prefix, "Hello World" in text
        except Exception:  # noqa: BLE001
            return prefix, False

    def _probe_cdn(host):
        try:
            text = http_get_text(CDN_PROBE_TMPL.format(host=host), retries=0, timeout=timeout)
            return host, "Hello World" in text
        except Exception:  # noqa: BLE001
            return host, False

    if base:
        with ThreadPoolExecutor(min(8, len(base))) as ex:
            for prefix, ok in ex.map(_probe_mirror, base):
                (alive if ok else dead).append(prefix)
    # 主清单存活不足 2 个 → 补测备用候选（主清单成批死亡是常态，见 MIRROR_SPARE_CANDIDATES）
    spare_alive = []
    if base and len(alive) < 2:
        spares = [m for m in MIRROR_SPARE_CANDIDATES if m not in base]
        if spares:
            with ThreadPoolExecutor(min(8, len(spares))) as ex:
                for prefix, ok in ex.map(_probe_mirror, spares):
                    if ok and prefix not in alive:
                        alive.append(prefix)
                        spare_alive.append(prefix)
    if spare_alive:
        print(f"[info] 主清单存活镜像不足 2 个，已从备用候选救回 {len(spare_alive)} 个："
              f"{'、'.join(spare_alive)}")
    with ThreadPoolExecutor(min(4, len(JSDELIVR_HOSTS))) as ex:
        for host, ok in ex.map(_probe_cdn, JSDELIVR_HOSTS):
            (cdn_alive if ok else cdn_dead).append(host)

    # raw 直连也测一次：已知不通时把镜像前置，省掉每个文件的 TLS 失败等待
    raw_ok = False
    try:
        raw_ok = "Hello World" in http_get_text(MIRROR_PROBE_FILE, retries=0, timeout=timeout)
    except Exception:  # noqa: BLE001
        raw_ok = False

    try:
        os.makedirs(os.path.dirname(MIRROR_STATE_FILE), exist_ok=True)
        with open(MIRROR_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"alive": alive, "dead": dead,
                       "cdn_alive": cdn_alive, "cdn_dead": cdn_dead,
                       "raw_alive": raw_ok,
                       "checked_ts": time.time(),
                       "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M")},
                      f, ensure_ascii=False, indent=1)
    except OSError:
        pass

    print(f"[info] 下载通道：raw 直连 {'可用' if raw_ok else '不可用'}；"
          f"镜像 {len(alive)}/{len(base)}"
          + (f"（{'、'.join(alive)}）" if alive else "（无，仅走 raw/CDN）")
          + f"；jsDelivr {len(cdn_alive)}/{len(JSDELIVR_HOSTS)}"
          + (f"（{'、'.join(cdn_alive)}）" if cdn_alive else "（无）"))
    return alive, dead


# 搜索关键词：覆盖 v2ray / clash / sing-box 生态与中文节点仓库
SEARCH_QUERIES = [
    # ── 综合聚合仓库 ──
    "v2ray free nodes",
    "v2ray configs",
    "vmess vless trojan",
    "free proxy nodes",
    "proxy subscription",
    "free subscription nodes",
    # ── 按内核命名（README 里通常直接给该内核的订阅链接）──
    "clash subscription",
    "clash config",
    "mihomo config",
    "sing-box config",
    "singbox nodes",
    "xray configs",
    "xray vless reality",
    # ── 按协议命名（新协议仓库基本只按协议起名，不搜会整类漏掉）──
    "hysteria2 nodes",
    "tuic vless",
    "vless reality",
    "vmess subscription",
    "trojan subscription",
    "shadowsocks subscription",
    # ── 中文仓库 ──
    "节点 订阅",
    "免费节点",
    "免费机场",
    "节点分享",
    "订阅链接",
    # ── 日更型仓库（每天自动产出当天订阅）──
    "daily free nodes",
    "daily v2ray",
]

# 默认种子仓库（长期活跃、star 高、更新频繁的主流聚合仓库）
# 运行后脚本会动态维护 seed_repos.json（记录各仓库贡献的节点数），节点不足时优先补充采集
DEFAULT_SEED_REPOS = [
    "barry-far/V2ray-Configs",
    "Epodonios/v2ray-configs",
    "mahdibland/V2RayAggregator",
    "peasoft/NoMoreWalls",
    "Au1rxx/free-vpn-subscriptions",
]

# 用于排除明显不是节点仓库的路径
BLACKLIST_REPO_PATTERNS = re.compile(
    r"(tutorial|docs?|wiki|awesome|list$|track|client|app|gui|windows|android|ios|"
    r"macos|linux|docker|script|tool|manager|panel|core$|kernel|-src$|"
    # 面板 / 客户端 / 订阅转换器类项目：不是节点源，扫了只会浪费配额
    r"sub-?store|subconverter|3x-?ui|x-?ui|clash-?verge|v2raya|nekoray|nekobox|"
    r"hiddify|v2rayng|shadowrocket|clash-?for|proxy-?client)",
    re.IGNORECASE,
)

CANDIDATE_EXT = {".txt", ".yaml", ".yml", ".json", ".list", ".log"}
CANDIDATE_NAME_HINTS = re.compile(
    r"(sub|node|config|clash|v2ray|sing|proxy|all|merge|mix|proxy|free|aggregat|combo|mini|lite|"
    r"节点|订阅|配置|机场|免费|代理)",
    re.IGNORECASE,
)

# 无扩展名的订阅文件：这类在真实仓库里很常见（ts-sf/fly 的 clash 与 v2、
# 各种 proxypool 产出的 configs），文件名本身就是格式声明，靠扩展名筛会整仓漏掉。
BARE_SUB_NAMES = re.compile(
    r"^(clash|clashx|mihomo|v2|v2ray|vmess|vless|trojan|ss|ssr|hysteria2?|tuic|"
    r"sing-?box|sub|subs|subscribe|subscription|nodes?|servers?|configs?|"
    r"proxies|proxy|all|mixed?|merged?|total|combined|free|list|outputs?)$",
    re.IGNORECASE,
)

SKIP_FILE_PATTERNS = re.compile(
    r"(readme|license|\.gitignore|country|asn|geosite|geoip|rule|block|direct|ads|cn$|"
    r"white|black|cidr|ip-?list|allowlist|bypass|"          # 分流/白名单类，不是节点列表
    r"scrapy|nohup|access\.log|error\.log|debug\.log|"       # 爬虫/运行日志（.log 在候选扩展名里）
    r"golangci|docker-compose|^package\.json|^requirements|pre-commit|composer\.|"
    r"tsconfig|eslint|Makefile|\.github|workflow|\.svg$|\.png$)",
    re.IGNORECASE,
)

# 根目录无候选文件时，最多再扫描这么多个疑似订阅子目录（控制 API 配额消耗）
MAX_SUBDIR_SCAN = 2
SUBDIR_HINTS = re.compile(
    r"^(sub|subs|subscri\w*|nodes?|configs?|outputs?|dist|data|source|src|clash|"
    r"sing-?box|v2ray|all|public|result|release|txt|yaml|list)$",
    re.IGNORECASE,
)
# 中文 / 内核名目录（Mihomo内核系、Sing-box内核系、节点订阅、免费机场…）。
# 这类目录名普遍带后缀，锚定正则穷举不了，只能按"包含"匹配。
SUBDIR_HINTS_LOOSE = re.compile(
    r"(mihomo|sing-?box|xray|hysteria2?|tuic|vmess|vless|trojan|shadowrocket|"
    r"内核|节点|订阅|配置|机场|免费|代理|翻墙|科学上网)",
    re.IGNORECASE,
)


def is_subdir_hint(name):
    """目录名是否像订阅目录（英文锚定匹配 + 中文/内核名包含匹配）。"""
    name = (name or "").strip()
    return bool(SUBDIR_HINTS.match(name) or SUBDIR_HINTS_LOOSE.search(name))
# 大文件（>2MB）走镜像极易被截断，优先用 jsDelivr 分块 CDN
LARGE_FILE_BYTES = 2 * 1024 * 1024

# ---------------------------------------------------------------- README 订阅链接
# 大量仓库把订阅文件路径/外链写在 README 里（「Clash 订阅」「sing-box 配置」等），
# 只靠文件名猜会漏掉这些核心产物，因此每个仓库都先读 README 再挑文件。
README_NAME_RE = re.compile(r"^readme(?:[._-].*)?$", re.IGNORECASE)
README_PREFER = ("readme.md", "readme_cn.md", "readme-zh.md", "readme.zh-cn.md", "readme.markdown")
MAX_README_LINKS = 10         # 单个仓库最多跟随的 README 订阅链接数（按内核+日期筛过后）

# ── 按内核识别订阅链接 ──
# 很多仓库在 README 里分内核列出订阅（「Clash 订阅」「sing-box 配置」「V2ray 订阅」），
# 认出来之后有两个用处：① 日志里能说清每个内核各采了多少；
# ② 仓库作者既然声明「这是 clash 订阅」，该链接里的节点就**保证**能进 clash 文件，
#    可以豁免 layout.CAPS 的保守预筛（CAPS 宁可漏也不肯放宽，容易把真能用的判死）。
# 顺序有讲究：sing-box 先判，避免被 clash 的宽泛规则抢走
KERNEL_LINK_HINTS = [
    ("singbox", re.compile(r"sing[-_ ]?box|singbox", re.IGNORECASE)),
    ("clash", re.compile(r"clash|mihomo", re.IGNORECASE)),
    ("xray", re.compile(r"x[-_ ]?ray", re.IGNORECASE)),
    ("v2ray", re.compile(r"v2ray|v2fly|v2rayng|v2rayn", re.IGNORECASE)),
]

# ── 按日期识别订阅链接 ──
# 日更型仓库常见两种写法：
#   ① 链接本身带日期：.../2026-10-25/all.txt、.../20261025/clash.yaml、Nodes-2026-10-25.txt
#   ② 用小标题分节：### 2026-10-25 下面才列当天的链接（链接自己没有日期）
# 两种都要认。只认 4 位年份的完整日期，不猜 "1025" 这类缩写（误伤率太高）。
DATE_TOKEN_RE = re.compile(r"(20\d{2})[-_/.年]?(\d{1,2})[-_/.月]?(\d{1,2})")
DATE_HEADING_RE = re.compile(
    r"^[ \t]{0,3}#{1,6}[^\n]{0,80}?(20\d{2})[-_/.年]?(\d{1,2})[-_/.月]?(\d{1,2})", re.MULTILINE)

MD_LINK_RE = re.compile(r"\[([^\]\n]{0,80})\]\(\s*(https?://[^)\s]+)\s*\)")
HREF_LINK_RE = re.compile(r"""href=["'](https?://[^"'\s]+)["']""", re.IGNORECASE)
# 排除字符里必须有反引号与星号：中文 README 极爱用 `裸链接`（行内代码）和 **加粗链接**，
# 这两种装饰符不在排除集里就会被吸进 URL 尾部，拼出一个 404 的地址（见 known-issues 第 35 条）。
URL_RE = re.compile(r"https?://[^\s\)\]\"'<>`*|，。；、]+")
# clash/sing-box 的一键导入链接，真正的订阅地址在 ?url= 里
IMPORT_LINK_RE = re.compile(r"(?:clash(?:meta|-meta)?|sing-?box)://[^\s\)\]\"'<>，。；、]+",
                            re.IGNORECASE)
SUB_URL_EXT = {".txt", ".yaml", ".yml", ".json", ".list", ".conf", ".log"}
# README 中明显不是订阅链接的地址（徽章/图片/仓库主页/文档站）
BAD_LINK_RE = re.compile(
    r"(shields\.io|badge|\.png|\.jpe?g|\.gif|\.svg|\.ico|/issues|/pull/|/releases|/wiki|"
    r"/stargazers|/actions|/graphs|/network|/commits|/blame|/tree/|/discussions|/forks|"
    r"/watchers|/topics/|star-history|jsdelivr\.com/package|\.github\.io|"
    r"t\.me|telegram|discord|youtube|twitter|x\.com|/sponsors|/settings|"
    r"github\.com/[^/]+/[^/?#]+/?$)",
    re.IGNORECASE,
)
# 无扩展名的订阅接口需要更强的特征才放行（否则 ?repos=/…Walls 之类网页会被误收）
SUB_URL_STRONG_HINT = re.compile(r"(sub|clash|v2ray|sing-?box|node)", re.IGNORECASE)

URI_RE = re.compile(
    r"(?:vmess|vless|trojan|ss|ssr|hysteria2?|hy2|tuic)://[^\s\"'<>\\)\]]+",
    re.IGNORECASE,
)
B64_CHUNK_RE = re.compile(r"[A-Za-z0-9+/=_\-]{100,}")


# ---------------------------------------------------------------- HTTP

def _urlopen(req, timeout, ctx, direct):
    """统一的 open：direct=True 走不带代理的 opener，False 尊重环境里的代理设置。"""
    if direct:
        opener = _DIRECT_OPENER if ctx is _SSL_CTX else _DIRECT_OPENER_NOVERIFY
        return opener.open(req, timeout=timeout)
    return urllib.request.urlopen(req, timeout=timeout, context=ctx)


def http_get(url, token=None, timeout=20, retries=2, direct=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    if token and "api.github.com" in url:
        req.add_header("Authorization", "Bearer " + token)
    last_err = None
    for i in range(retries + 1):
        try:
            with _urlopen(req, timeout, _SSL_CTX, direct) as resp:
                body = resp.read()
            # 200 但 0 字节：镜像/CDN 边缘缓存未命中时的典型表现，必须当失败处理，
            # 否则上层会以为「文件下载成功、只是没有节点」，链条后面的好通道再也不会被尝试
            if not body:
                raise EmptyBody(f"200 空响应（{len(url)}B url …{url[-40:]}）")
            return body
        except EmptyBody as e:
            last_err = e
        except urllib.error.URLError as e:
            # 证书链无法校验（常见于沙箱/代理环境）：降级为不校验后重试一次
            if isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError) or \
                    "CERTIFICATE_VERIFY_FAILED" in str(getattr(e, "reason", "")):
                if not _SSL_WARNED[0]:
                    print("[warn] HTTPS 证书校验失败，已降级为不校验（沙箱/代理环境常见）", file=sys.stderr)
                    _SSL_WARNED[0] = True
                with _urlopen(req, timeout, _NOVERIFY_CTX, direct) as resp:
                    body = resp.read()
                if not body:
                    raise EmptyBody(f"200 空响应（url …{url[-40:]}）")
                return body
            last_err = e
        except Exception as e:  # noqa: BLE001
            last_err = e
        if i < retries:
            time.sleep(1.5 * (i + 1))
    raise last_err


def http_get_text(url, token=None, timeout=20, retries=2, direct=False):
    return http_get(url, token, timeout, retries=retries,
                    direct=direct).decode("utf-8", errors="replace")


def _quote_api_path(path):
    """把 API 路径里的非 ASCII 字符转义，同时保留分隔符与查询串。

    中文节点仓库常用中文目录/文件名（Xray内核系、节点订阅.txt），不转义时
    urllib 会在发请求前抛 UnicodeEncodeError，上层把异常当成"仓库没有文件"，
    整个仓库被静默跳过。
    """
    if "?" in path:
        head, _, query = path.partition("?")
    else:
        head, query = path, ""
    head = urllib.parse.quote(head, safe="/:@!$&'()*+,;=_~-.")
    return f"{head}?{query}" if query else head


def github_api(path, token=None):
    data = http_get(API_BASE + _quote_api_path(path), token)
    return json.loads(data.decode("utf-8", errors="replace"))


# ---------------------------------------------------------------- 仓库发现

def search_repos(token, max_repos, min_stars, since_iso, pages=2):
    """搜索 since_iso 之后有更新的仓库：多关键词 × 多页，按更新时间排序，去重合并。

    为什么要翻页：单个关键词按 `sort=updated` 取前 100 条基本被几个日更大仓库占满，
    真正的中小仓库全在第二页之后。带 token 时搜索限额 30 次/分（匿名只有 10 次/分），
    所以间隔按身份动态调整——匿名 6.5s，带 token 2.2s。
    """
    repos = {}
    pages = max(1, pages)
    gap = 2.2 if token else 6.5
    calls = 0
    for kw in SEARCH_QUERIES:
        for page in range(1, pages + 1):
            q = f"{kw} pushed:>={since_iso} stars:>={min_stars}"
            url = ("/search/repositories?q=" + urllib.parse.quote(q)
                   + f"&sort=updated&order=desc&per_page=100&page={page}")
            calls += 1
            try:
                data = github_api(url, token)
            except Exception as e:  # noqa: BLE001
                print(f"[warn] 搜索失败（{kw} 第 {page} 页）: {e}", file=sys.stderr)
                break
            items = data.get("items", [])
            for item in items:
                full = item.get("full_name", "")
                if not full or full in repos:
                    continue
                if BLACKLIST_REPO_PATTERNS.search(full.split("/")[-1]):
                    continue
                repos[full] = {
                    "full_name": full,
                    "stars": item.get("stargazers_count", 0),
                    "pushed_at": item.get("pushed_at", ""),
                    "desc": item.get("description") or "",
                }
            if len(items) < 100:      # 该关键词已经到底，不必翻下一页
                break
            time.sleep(gap)           # 翻页之间也要限速
        time.sleep(gap)
    print(f"[info] 搜索完成：{len(SEARCH_QUERIES)} 组关键词 × {pages} 页 = {calls} 次请求，"
          f"去重后 {len(repos)} 个仓库")
    ranked = sorted(repos.values(), key=lambda r: (r["stars"], r["pushed_at"]), reverse=True)
    return ranked[:max_repos]


def _score_entry(name, size):
    """给候选文件打分：名称强相关 + 体积适中优先（大文件经镜像极易截断）。"""
    score = 0
    if CANDIDATE_NAME_HINTS.search(name):
        score += 100
    if re.search(r"(sub|all|total|merge|mix|best|node|free|combo)", name, re.IGNORECASE):
        score += 50
    if size <= LARGE_FILE_BYTES:
        score += 30
    else:
        score -= 20
    if size < 512:
        score -= 40  # 几百字节的多半是占位/说明文件
    return score


def _normalize_entry(ent):
    """把 GitHub contents 条目或 jsDelivr 文件条目统一成 {path,name,size,type}。"""
    path = (ent.get("path") or ent.get("name") or "").lstrip("/")
    if not path:
        return None
    return {"path": path, "name": ent.get("name") or os.path.basename(path),
            "size": int(ent.get("size") or 0), "type": ent.get("type", "file")}


def list_repo_files(repo_full, token, force_api=False):
    """列出仓库全部文件（扁平路径）。

    **优先 jsDelivr data API（不消耗 GitHub 核心配额）**，失败才回落 contents API。
    匿名 GitHub 配额只有 60 次/小时，列目录曾是最大消耗项——这是每日采集卡住的主因。
    注意 jsDelivr 可能是旧快照（文件名与 HEAD 不一致），下载全失败时用 force_api=True 重新核对。
    """
    for branch in (() if force_api else ("main", "master")):
        url = f"https://data.jsdelivr.com/v1/packages/gh/{repo_full}@{branch}?structure=flat"
        try:
            data = json.loads(http_get_text(url, retries=0, timeout=20))
        except Exception:  # noqa: BLE001
            continue
        files = data.get("files") or []
        items = [x for x in (_normalize_entry({"path": f.get("name"), "size": f.get("size")})
                             for f in files) if x]
        if items:
            return items
    # 回落：GitHub contents API（根目录；force_api 时再补 1-2 个子目录，消耗配额）
    try:
        entries = github_api(f"/repos/{repo_full}/contents/", token)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] 列目录失败（{repo_full}）: {e}", file=sys.stderr)
        return []
    if not isinstance(entries, list):
        return []
    items = [x for x in (_normalize_entry(e) for e in entries) if x]
    if force_api:
        dirs = [e for e in entries if e.get("type") == "dir"
                and is_subdir_hint(e.get("name"))]
        for d in dirs[:MAX_SUBDIR_SCAN]:
            try:
                sub = github_api(f"/repos/{repo_full}/contents/{d.get('path')}", token)
            except Exception:  # noqa: BLE001
                continue
            if isinstance(sub, list):
                items += [x for x in (_normalize_entry(e) for e in sub)
                          if x and x.get("type") == "file"]
    return items


def _pick_from(items, limit=3, root_only=False):
    """从（已规范化的）文件列表里挑候选订阅文件。"""
    picked = []
    for it in items:
        if it["type"] != "file":
            continue
        depth = it["path"].count("/")
        if root_only and depth:
            continue
        size, name = it["size"], it["name"]
        if size <= 0 or size > 8 * 1024 * 1024:
            continue
        if SKIP_FILE_PATTERNS.search(name):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in CANDIDATE_EXT:
            # 无扩展名的裸文件：只有名字整体像订阅（clash / v2 / configs）才收，
            # 且体积要够大——几百字节的裸文件多半是脚本或标记文件
            if ext or not BARE_SUB_NAMES.match(name) or size < 4096:
                continue
        picked.append({**it, "score": _score_entry(name, size)})
    picked.sort(key=lambda x: -x["score"])
    return picked[:limit]


def pick_candidate_files(repo_full, token, items=None):
    """挑选候选订阅文件：根目录优先；根目录没货时用子目录（Subscriptions/、source/ 等）。

    很多聚合仓库把订阅放在子目录里，只看根目录会直接判定「无可候选文件」。
    items 可传入已列好的文件树，避免同一仓库重复列目录（省配额 + 省时间）。
    """
    items = items if items is not None else list_repo_files(repo_full, token)
    if not items:
        return []
    picked = _pick_from(items, limit=3, root_only=True)
    if picked:
        return picked

    # 子目录兜底：允许任意深度（sub/raw/01.yaml 这类两层布局很常见），
    # 但顶层目录必须命中订阅目录提示词，避免去扫 src/ docs/ tools/
    subs = [it for it in items
            if it["path"].count("/") >= 1
            and is_subdir_hint(it["path"].split("/")[0])]
    got = _pick_from(subs, limit=2)
    if got:
        print(f"[info] {repo_full} 根目录无候选文件，改用子目录 {os.path.dirname(got[0]['path'])}/")
        return got

    # 若文件树来自 contents API，目录下的文件根本没被列出来（type=dir 且无子项），
    # 这时需要真正进目录扫一次。只有存在命中提示词的目录才付这份配额。
    hinted_dirs = [it for it in items
                   if it["type"] == "dir" and is_subdir_hint(it["name"])]
    if hinted_dirs:
        deeper = list_repo_files(repo_full, token, force_api=True)
        if deeper and deeper is not items:
            retry = _pick_from([it for it in deeper
                                if it["path"].count("/") >= 1
                                and is_subdir_hint(it["path"].split("/")[0])], limit=2)
            if retry:
                print(f"[info] {repo_full} 根目录无候选文件，进目录扫描后取 "
                      f"{os.path.dirname(retry[0]['path'])}/")
                return retry
    return got


# ---------------------------------------------------------------- README 订阅链接读取

def find_readme(items):
    """在文件树里找 README（根目录优先，兼容 README_CN.md / readme.rst 等）。"""
    cands = [it for it in items
             if it["type"] == "file" and it["path"].count("/") == 0
             and README_NAME_RE.match(it["name"])]
    if not cands:
        return None
    cands.sort(key=lambda it: (it["name"].lower() not in README_PREFER,
                               len(it["name"])))
    return cands[0]


def _strip_url_tail(url):
    # 反引号/星号/竖线来自 markdown 装饰（行内代码、加粗、表格分隔），一律剥掉
    return url.rstrip(".,;:，。；、)]}>'\"`*|")


def _split_raw_parts(parts):
    """`owner/repo/<ref|refs/heads/<ref>>/<path>` → (rel_path, ref)。

    `parts[2] == "refs"` 时把 `refs/heads/main` 整段当成引用、路径从 parts[5:] 起；
    否则 parts[2] 就是引用本身。GitHub 页面「复制链接」给出的就是 refs 形态
    （2026-10 起 README 里非常普遍），不认它就会拼出 `heads/main/xxx` 这种必 404 的路径。
    """
    if len(parts) >= 5 and parts[2] == "refs" and parts[3] in ("heads", "tags"):
        return "/".join(parts[5:]), parts[4]
    return "/".join(parts[3:]), parts[2]


def _repo_path_from_url(url, repo_full):
    """判断链接是否指向某个 GitHub 仓库内的文件，返回 (repo, rel_path, branch) 或 None。"""
    # 这里必须用**全量候选池**而不是 get_mirror_prefixes()：
    # 归一化的目的是识别链接指向哪个仓库文件，与镜像当前是否存活无关，
    # 用可用清单会让失效镜像的链接认不出来，导致同一文件被重复下载。
    for m in _base_mirrors():
        if url.lower().startswith(m.lower()):
            return _repo_path_from_url(url[len(m):], repo_full)
    try:
        u = urllib.parse.urlsplit(url)
    except ValueError:
        return None
    host = u.netloc.lower().split(":")[0]
    parts = [p for p in urllib.parse.unquote(u.path).split("/") if p]
    if host == "raw.githubusercontent.com" and len(parts) >= 3:
        rel, ref = _split_raw_parts(parts)
        return "/".join(parts[:2]), rel, ref
    if host in ("raw.gitmirror.com", "raw.kgithub.com") and len(parts) >= 4:
        rel, ref = _split_raw_parts(parts)
        return "/".join(parts[:2]), rel, ref
    # raw.githack.com / rawcdn.githack.com：README 里常见的另一层 CDN
    if host in ("raw.githack.com", "rawcdn.githack.com") and len(parts) >= 4:
        rel, ref = _split_raw_parts(parts)
        return "/".join(parts[:2]), rel, ref
    if host in ("github.com", "www.github.com") and len(parts) >= 5 and parts[2] in ("raw", "blob"):
        repo = "/".join(parts[:2])
        rest = parts[3:]
        if rest and rest[0] == "refs" and len(rest) >= 3:
            return repo, "/".join(rest[3:]), rest[2]
        return repo, "/".join(rest[1:]), rest[0]
    if host in JSDELIVR_HOSTS and len(parts) >= 4 and parts[0] == "gh":
        # /gh/<owner>/<repo>@<ref>/<path>
        repo_ref = parts[2]
        repo = f"{parts[1]}/{repo_ref.split('@')[0]}"
        ref = repo_ref.split('@', 1)[1] if "@" in repo_ref else "main"
        return repo, "/".join(parts[3:]), ref
    return None


def detect_kernel_hint(*texts):
    """从链接路径 / 文件名 / 链接文字里认出它属于哪个内核；认不出返回 None（通用）。"""
    for core, rx in KERNEL_LINK_HINTS:
        for t in texts:
            if t and rx.search(t):
                return core
    return None


def parse_date_token(*texts):
    """从若干段文本里找第一个合法日期（YYYY-MM-DD），找不到返回 None。"""
    for t in texts:
        if not t:
            continue
        for m in DATE_TOKEN_RE.finditer(t):
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if not (1 <= mo <= 12 and 1 <= d <= 31):
                continue
            try:
                return date(y, mo, d)
            except ValueError:   # 2 月 30 日之类的非法日期
                continue
    return None


def classify_readme_link(url, repo_full, link_text=""):
    """把 README 里的链接分类：(kind, target, kernel)。kernel 为 None 表示通用订阅。"""
    url = _strip_url_tail(url)
    if not url or BAD_LINK_RE.search(url):
        return None
    # clash://install-config?url=<订阅地址> 这类导入链接，取出真正的订阅地址
    url_kernel = detect_kernel_hint(url)
    if url.lower().startswith(("clash://", "clashmeta://", "clash-meta://", "sing-box://")):
        scheme = url.split("://", 1)[0].lower()
        url_kernel = detect_kernel_hint(scheme)
        inner = _q(url).get("url") or ""
        url = urllib.parse.unquote(_strip_url_tail(inner))
        if not url.startswith("http"):
            return None
    got = _repo_path_from_url(url, repo_full)
    if got:
        repo, rel, branch = got
        if not rel or rel.endswith("/"):
            return None
        base = os.path.basename(rel).lower()
        if re.search(r"(example|template|sample|demo)", base):
            return None  # 示例配置，不是真实订阅
        ext = os.path.splitext(rel)[1].lower()
        if ext not in CANDIDATE_EXT:
            return None
        # 内核判定顺序：文件名 → 目录名 → 链接文字（最贴近内容的优先）
        kernel = (detect_kernel_hint(base) or detect_kernel_hint(rel)
                  or url_kernel or detect_kernel_hint(link_text))
        if repo.lower() == repo_full.lower():
            return ("repo_path", rel, kernel)
        # 别的仓库的 blob 页面是 HTML，换成 raw 地址（镜像回退链照样生效）
        raw = f"https://raw.githubusercontent.com/{repo}/{branch or 'main'}/{rel}"
        return ("url", raw, kernel)
    try:
        u = urllib.parse.urlsplit(url)
    except ValueError:
        return None
    q = dict(urllib.parse.parse_qsl(u.query or ""))
    # 订阅转换器接口（sub?target=...&url=...）：源多半还是本仓库文件，走它既慢又重复
    if q.get("target") and q.get("url"):
        return None
    path = urllib.parse.unquote(u.path or "")
    if not path or path == "/":
        return None
    # 以 "/" 结尾 = 目录/分类/文章页，不可能是订阅文件本体。
    # 2026-10-31 归因：crashgfw/free-airport-nodes 的 `v2raya.net/categories/free-nodes/`
    # 靠 SUB_URL_STRONG_HINT 里的 "node" 混进了链接清单，占了 MAX_README_LINKS 的 1 个名额，
    # 下载回来是 HTML（解析 0 条），日志里却记成「1/10 链接下载成功」；
    # shaoyouvip/free 的 `blog.zrf.me/p/GUI-for-Clash/` 同理。
    # 订阅接口（/api/v1/client/sub?token=…）不会以 "/" 收尾，所以这条规则不会误伤真实订阅。
    if path.endswith("/"):
        return None
    ext = os.path.splitext(path)[1].lower()
    kernel = (detect_kernel_hint(path) or url_kernel or detect_kernel_hint(link_text)
              or detect_kernel_hint(u.netloc))
    if ext in SUB_URL_EXT:
        return ("url", url, kernel)
    # 无扩展名的订阅接口（如 /api/v1/client/sub?token=xxx）：必须有 sub/clash/node 等强特征
    if ext == "" and SUB_URL_STRONG_HINT.search(path + "?" + (u.query or "")):
        return ("url", url, kernel)
    return None


def extract_readme_links(text, repo_full, today=None, tolerance=0):
    """从 README 抽出订阅链接，并按「内核 + 日期」筛选。

    返回 (links, stats)：
      links  每项 {"kind","target","kernel","day"}（kernel 为 None = 通用订阅）
      stats  {"candidates","kept","date_skipped","dates_seen","kernels"}

    日期规则（用户策略：只取当天）：
      - 链接自身带日期（.../2026-10-25/all.txt）或有日期小标题（### 2026-10-25）作为上下文
      - 只有落在 [today - tolerance, today] 内的才保留；tolerance 默认 0 = 严格只要当天
      - 整份 README 完全没提日期 → 视为通用订阅，全部保留（否则会把非日更仓库全砍掉）
    """
    hits = []  # (位置, 原始链接, 链接文字)
    for rx, link_grp, text_grp in ((MD_LINK_RE, 2, 1), (HREF_LINK_RE, 1, None),
                                   (IMPORT_LINK_RE, 0, None), (URL_RE, 0, None)):
        for m in rx.finditer(text):
            label = ""
            if text_grp is not None:
                try:
                    label = m.group(text_grp) or ""
                except IndexError:
                    label = ""
            hits.append((m.start(link_grp), m.group(link_grp), label))
    hits.sort(key=lambda x: x[0])

    # 日期上下文：README 里所有「带日期的标题」位置
    date_marks = []
    for m in DATE_HEADING_RE.finditer(text):
        d = parse_date_token(m.group(0))
        if d:
            date_marks.append((m.start(), d))
    date_marks.sort()

    def ctx_date(pos):
        """链接所属的日期上下文：最近的带日期标题（超过 4000 字视为不属于该节）。"""
        cur = None
        for p, d in date_marks:
            if p > pos:
                break
            if pos - p <= 4000:
                cur = d
        return cur

    today = today or date.today()
    low = today - timedelta(days=max(0, int(tolerance)))
    found, seen = [], set()
    stats = {"candidates": len(hits), "kept": 0, "date_skipped": 0,
             "dates_seen": {}, "kernels": {}}
    for pos, raw, label in hits:
        got = classify_readme_link(raw, repo_full, label)
        if not got:
            continue
        kind, target, kernel = got
        # 日期优先看链接本身，其次看它所在的日期标题
        day = parse_date_token(raw) or ctx_date(pos)
        if day is not None:
            stats["dates_seen"][day.isoformat()] = stats["dates_seen"].get(day.isoformat(), 0) + 1
            if not (low <= day <= today):
                stats["date_skipped"] += 1
                continue
        # 同一文件常被 README 用 raw / 多个 CDN 域名重复列出，按「仓库+路径」归一去重，
        # 否则一个 list.txt 会被下载 4 次（既拖慢采集，也把链接配额浪费在副本上）
        if kind == "repo_path":
            ident = f"{repo_full.lower()}::{target.lower()}"
        else:
            rp = _repo_path_from_url(target, repo_full)
            ident = f"{rp[0].lower()}::{rp[1].lower()}" if rp else target
        if ident in seen:
            continue
        seen.add(ident)
        found.append({"kind": kind, "target": target, "kernel": kernel,
                      "day": day.isoformat() if day else None})
        stats["kernels"][kernel or "any"] = stats["kernels"].get(kernel or "any", 0) + 1
    stats["kept"] = len(found[:MAX_README_LINKS])
    return found[:MAX_README_LINKS], stats


def err_tag(e):
    """把下载异常压成短标签，供日志区分「404 路径失效」与「超时/网络」两类失败。

    之前所有失败都只记「下载失败」，自检报出的「下载通道 critical」因此无法归因：
    实采一次抽样复现（2026-10-28）证明多数是 README 声明的路径已 404，
    与镜像/通道无关，属上游改动。
    """
    if isinstance(e, EmptyBody):
        return "空响应"
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code}"
    reason = getattr(e, "reason", None)
    if isinstance(e, (TimeoutError, socket.timeout)) or \
            isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(e):
        return "超时"
    return type(e).__name__


# 可重试的瞬时失败：限流与临时不可用。404/410 属上游路径失效，重试毫无意义。
RETRYABLE_HTTP = {408, 425, 429, 500, 502, 503, 504}

# 外链走哪条路：非 GitHub 域名直连优先（通道只为 github 而建，见 fetch_url_text 说明）
GITHUB_HOSTS = {"github.com", "api.github.com", "raw.githubusercontent.com",
                "codeload.github.com", "objects.githubusercontent.com"}
DIRECT_TIMEOUT = 8            # 外部站点直连的超时上限：先快速失败，再交给通道
_HOST_DIRECT_BAD = set()      # 直连试过并失败的 host，本进程内不再走直连（省 8s/条）


def _is_github_url(url):
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return host in GITHUB_HOSTS or host.endswith(".githubusercontent.com") \
        or host.endswith(".github.com")


def _retryable_fetch_error(e):
    """判断一次外部链接下载失败是否值得再试一次。

    2026-10-29 实采归因：当天 19 条下载失败里 URLError 6、HTTP 429 4、HTTP 503 3，
    共 13 条属瞬时类；单点复现证明同一批链接随后 0.3~0.8s 全部成功、内容也能正常解析，
    说明失败发生在下载侧而不是解析侧。crashgfw/free-airport-nodes 的 10 条链接全在
    同一个订阅域名上，一次抖动就让这个历史千条的仓库整仓归零。

    **超时不重试**：外部订阅站点慢时再来一轮 15s 只会把单仓 90s 时间预算翻倍，
    宁可记失败等下一天（吞吐优先，同 known-issues 第 40 条口径）。
    **空响应不重试**：所有通道都已经试过一轮，再走一遍只是把每条链接的耗时翻倍。
    """
    if isinstance(e, EmptyBody):
        return False
    if isinstance(e, urllib.error.HTTPError):
        return e.code in RETRYABLE_HTTP
    reason = getattr(e, "reason", None)
    if isinstance(e, (TimeoutError, socket.timeout)) or \
            isinstance(reason, (TimeoutError, socket.timeout)) or "timed out" in str(e):
        return False
    return True


def fetch_url_text(url, timeout=15):
    """下载任意 URL 的文本；raw.githubusercontent 走镜像回退链。

    超时比仓库内文件短——README 里声明的外部订阅地址不可控，
    一个慢站就能拖住整个仓库的采集。

    404/410 立刻放弃剩余镜像：镜像只是转发原站内容，原站 404 时其余镜像必然也是 404，
    逐个试完只是白等（实测一条死链走完镜像链要 23~37 秒，14 条就是 5 分钟以上）。

    瞬时类失败（连接重置/拒绝/DNS 抖动/429/5xx）整条链再走一次，只重试一次，
    429 时尊重 Retry-After 但封顶 3s。

    **外部站点直连优先、通道兜底**（2026-10-30 修复）：上行通道只为翻 github 那堵墙而建，
    把它当成所有外链的默认出口是个错误假设。实测同一个免费订阅站
    `ndxy.fn0821.xyz`（crashgfw/free-airport-nodes 的 9 条链接全在这个域）：
    直连 5/5 成功 0.3~2.7s，经通道 5/5 失败（SSL: UNEXPECTED_EOF，10~15s），
    该仓库连续两晚整仓归零（历史 1050 条）。
    现在改为：非 GitHub 域名先直连（超时压到 DIRECT_TIMEOUT），失败再走通道；
    并按域名记住哪条路通（同域链接往往一批，避免逐条重复试错）。
    """
    attempts = [url]
    if "raw.githubusercontent.com/" in url:
        for m in get_mirror_prefixes():
            attempts.append(m + url)

    host = (urllib.parse.urlparse(url).hostname or "").lower()
    external = bool(host) and not _is_github_url(url)
    direct_legs = [(u, True, min(DIRECT_TIMEOUT, timeout)) for u in attempts]
    proxy_legs = [(u, False, timeout) for u in attempts]
    if not external:
        plan = proxy_legs
    elif host in _HOST_DIRECT_BAD:
        plan = proxy_legs + direct_legs
    else:
        plan = direct_legs + proxy_legs

    def once():
        last_err = None
        for u, direct, tmo in plan:
            try:
                return http_get_text(u, retries=0, timeout=tmo, direct=direct)
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code in (404, 410):
                    break
            except Exception as e:  # noqa: BLE001
                last_err = e
                if direct:
                    # 直连失败的主机不再走直连：同域链接往往十几条，
                    # 每条都白等一个 DIRECT_TIMEOUT 会把单仓 90s 预算吃光
                    _HOST_DIRECT_BAD.add(host)
        raise last_err

    try:
        return once()
    except Exception as e:  # noqa: BLE001
        if not _retryable_fetch_error(e):
            raise
        wait = 1.0
        if isinstance(e, urllib.error.HTTPError):
            try:
                wait = min(float(e.headers.get("Retry-After") or 2.0), 3.0)
            except (TypeError, ValueError, AttributeError):
                wait = 2.0
        time.sleep(wait)
        return once()


def collect_from_readme(repo_full, items, token, records, budget=90, workers=4,
                        date_tolerance=0):
    """读 README → 跟随它声明的订阅链接 → 提取节点。

    返回 (链接数, 节点数, 明细, 链接统计)。这是很多仓库唯一暴露真实订阅文件的地方
    （文件名不带 sub/node 关键字，靠目录扫描根本挑不出来）。

    链接按「内核 + 日期」预筛（见 extract_readme_links），并发下载
    （外部订阅站点不可控，串行时一个慢站就能拖住整个仓库），整体再套时间预算。
    """
    readme = find_readme(items)
    if not readme:
        return 0, 0, [], {}
    try:
        text = fetch_repo_file_text(repo_full, readme["path"], token, size=readme.get("size", 0))
    except Exception as e:  # noqa: BLE001
        print(f"[warn] README 下载失败 {repo_full}/{readme['path']}: {e}", file=sys.stderr)
        return 0, 0, [], {}
    links, lstats = extract_readme_links(text, repo_full, tolerance=date_tolerance)
    if not links:
        return 0, 0, [], lstats
    deadline = time.time() + budget
    lock = threading.Lock()
    detail = []

    def work(link):
        kind, target = link["kind"], link["target"]
        if time.time() > deadline:
            return None
        label = (os.path.basename(target) if kind == "repo_path"
                 else (os.path.basename(urllib.parse.urlsplit(target).path) or target[-32:]))
        try:
            if kind == "repo_path":
                t = fetch_repo_file_text(repo_full, target, token)
                src = f"{repo_full}/{target}"
            else:
                t = fetch_url_text(target)
                src = f"{repo_full}/README→{urllib.parse.urlsplit(target).netloc}"
        except Exception as e:  # noqa: BLE001
            with lock:
                # 带上失败原因标签：404（上游路径失效）与超时/网络要分开看，
                # 前者属上游改动、无需修，后者才可能是镜像/通道问题
                detail.append((label, None, err_tag(e)))
            return None
        local = []
        n = extract_text_into(t, src, repo_full, local, os.path.splitext(target)[1],
                              kernel=link.get("kernel"))
        with lock:
            records.extend(local)
            detail.append((label, n, ""))
        return n

    total = 0
    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(links)))) as ex:
        for n in ex.map(work, links):
            total += n or 0
    detail_lines = [f"{lab}:{f'下载失败({tag})' if n is None else n}"
                    for lab, n, tag in detail]
    return len(links), total, detail_lines, lstats


# ---------------------------------------------------------------- 节点提取

def try_b64decode(s):
    s = s.strip().replace("-", "+").replace("_", "/")
    s += "=" * (-len(s) % 4)
    try:
        return base64.b64decode(s).decode("utf-8", errors="replace")
    except (binascii.Error, ValueError):
        return None


def extract_uris(text):
    uris = []
    for m in URI_RE.finditer(text):
        uri = m.group(0).rstrip(".,;，。；")
        if uri.lower().startswith("ss://") and len(uri) < 12:
            continue
        uris.append(uri)
    # base64 整段订阅：无 '://' 时尝试解码
    if "://" not in text:
        for m in B64_CHUNK_RE.finditer(text):
            decoded = try_b64decode(m.group(0))
            if decoded and "://" in decoded:
                uris.extend(extract_uris(decoded))
                break
    else:
        # 混合文本里也可能有 base64 订阅行
        for line in text.splitlines():
            line = line.strip()
            if "://" in line or len(line) < 100 or "=" not in line:
                continue
            decoded = try_b64decode(line)
            if decoded and "://" in decoded:
                uris.extend(extract_uris(decoded))
    return uris


def _ss_hostport(uri):
    """解析 ss:// 的多种变体，返回 (host, port) 或 None。

    支持：
      1. ss://base64(method:pass)@host:port#name     （SIP002 标准式）
      2. ss://method:pass@host:port#name             （明文 userinfo）
      3. ss://base64(method:pass@host:port)#name     （整段 base64，以前全部被丢弃）
      4. ss://base64(JSON{v,add,port,...})#name      （v2rayN JSON 变体）
    """
    body = uri[5:].split("#")[0]
    # 1/2：含 @ 时按标准式解析
    if "@" in body:
        hostpart = body.rsplit("@", 1)[1].split("?")[0].split("/")[0]
        if hostpart.startswith("["):
            try:
                return hostpart[1:hostpart.index("]")], int(hostpart.split("]:")[1])
            except (ValueError, IndexError):
                return None
        if ":" in hostpart:
            host, _, port = hostpart.rpartition(":")
            if host and port.isdigit():
                return host, int(port)
        return None

    # 3/4：不含 @ 时，整段 base64 再判断
    decoded = try_b64decode(body.split("?")[0])
    if not decoded:
        return None
    if decoded.lstrip().startswith("{"):
        try:
            data = json.loads(decoded)
            host, port = str(data.get("add") or ""), int(data.get("port") or 0)
            return (host, port) if host and port else None
        except (ValueError, TypeError):
            return None
    if "@" in decoded:
        hostpart = decoded.rsplit("@", 1)[1].split("/")[0]
        if hostpart.startswith("["):
            try:
                return hostpart[1:hostpart.index("]")], int(hostpart.split("]:")[1])
            except (ValueError, IndexError):
                return None
        if ":" in hostpart:
            host, _, port = hostpart.rpartition(":")
            if host and port.isdigit():
                return host, int(port)
    return None


def parse_uri_hostport(uri):
    """从 URI 中解析 (scheme, host, port)，vmess/ss/ssr 等特殊格式单独处理。"""
    low = uri.lower()
    try:
        if low.startswith("vmess://"):
            payload = uri[8:].split("#")[0]
            data = json.loads(try_b64decode(payload) or "{}")
            host, port = str(data.get("add", "")), int(data.get("port") or 0)
            return ("vmess", host.lower(), port) if host and port else None
        if low.startswith("ssr://"):
            data = try_b64decode(uri[6:]) or ""
            hostport = data.split("/")[0].split(":")
            if len(hostport) >= 2 and hostport[1].isdigit():
                return "ssr", hostport[0].lower(), int(hostport[1])
            return None
        if low.startswith("ss://"):
            hp = _ss_hostport(uri)
            if not hp:
                return None
            host, port = hp
            # 整段 base64 的 JSON 变体其实是 vmess 结构
            body = uri[5:].split("#")[0]
            if "@" not in body:
                decoded = try_b64decode(body.split("?")[0]) or ""
                if decoded.lstrip().startswith("{"):
                    return "vmess", host.lower(), port
            return "ss", host.lower(), port
        # 统一处理含 userinfo@host:port 的协议
        scheme = low.split("://")[0]
        rest = uri[len(scheme) + 3:]
        hostpart = rest.split("@", 1)[-1] if "@" in rest else rest
        hostpart = hostpart.split("#")[0].split("?")[0].split("/")[0]
        if hostpart.startswith("["):  # IPv6
            host = hostpart[1:hostpart.index("]")]
            port = int(hostpart.split("]:")[1].split(":")[0]) if "]:" in hostpart else 0
        else:
            parts = hostpart.rsplit(":", 1)
            host, port = parts[0], int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 0
        if host and port:
            return scheme, host.lower(), port
    except Exception:  # noqa: BLE001
        pass
    return None


def add_uri_record(records, uri, source):
    parsed = parse_uri_hostport(uri)
    if not parsed:  # 解析不出 host/port 的链接一律丢弃，避免污染订阅
        return
    records.append({"kind": "uri", "uri": uri, "parsed": parsed, "source": source})


def _q(url):
    """安全解析查询参数（畸形 URL 返回空字典）。"""
    try:
        return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    except ValueError:
        return {}


def _frag(url):
    """安全解析 # 片段（畸形 IPv6 等 URL 退化为手工截取）。"""
    try:
        frag = urllib.parse.urlsplit(url).fragment
    except ValueError:
        frag = url.split("#", 1)[1] if "#" in url else ""
    return urllib.parse.unquote(frag).strip() or ""


def _tls_params(q):
    """URI 里与 TLS 有关的参数（各内核字段名不同，这里只做归一）。"""
    alpn = (q.get("alpn") or "").replace(",", "/")
    return {
        "sni": q.get("sni") or q.get("peer") or "",
        "alpn": [a for a in alpn.split("/") if a],
        "fp": q.get("fp") or "",
        "insecure": str(q.get("allowInsecure") or q.get("insecure") or "0").lower()
                    in ("1", "true"),
    }


def _clash_net(p, q, raw_net):
    """把传输层写进 clash 代理字典；该内核不支持时返回 False（调用方丢弃该节点）。

    注意 type=http 与 type=h2 在 clash 侧是两种不同的实现（http-opts / h2-opts），
    不能合并：前者是 v2ray 的 HTTP 传输，后者是 HTTP/2。
    """
    net = lay.canon_net(raw_net)
    if not net or net == "tcp":
        return True
    path = q.get("path") or "/"
    host = q.get("host") or ""
    if net == "ws":
        wo = {"path": path}
        if host:
            wo["headers"] = {"Host": host}
        if q.get("ed"):
            try:
                wo["max-early-data"] = int(q["ed"])
                wo["early-data-header-name"] = "Sec-WebSocket-Protocol"
            except ValueError:
                pass
        p["network"] = "ws"
        p["ws-opts"] = wo
        return True
    if net == "grpc":
        p["network"] = "grpc"
        p["grpc-opts"] = {"grpc-service-name": q.get("serviceName") or q.get("path") or ""}
        return True
    if net == "http":
        if (raw_net or "").lower() == "h2":
            p["network"] = "h2"
            p["h2-opts"] = {"path": path}
            if host:
                p["h2-opts"]["host"] = [host]
        else:
            p["network"] = "http"
            opts = {"path": [path], "method": "GET"}
            if host:
                opts["headers"] = {"Host": [host]}
            p["http-opts"] = opts
        return True
    if net == "xhttp":
        p["network"] = "xhttp"
        xo = {"path": path, "mode": q.get("mode") or "auto"}
        if host:
            xo["host"] = host
        p["xhttp-opts"] = xo
        return True
    return False


def _clash_ss_plugin(p, q, plugin):
    """ss 的 plugin 参数 → mihomo 的 plugin / plugin-opts；不支持的插件返回 False。"""
    name, opts, raw = lay.split_plugin(plugin)
    if not name:
        return True
    if name == "obfs":
        mode = (opts.get("obfs") or opts.get("mode") or "http").lower()
        if mode not in ("http", "tls"):
            return False
        po = {"mode": mode}
        if opts.get("obfs-host"):
            po["host"] = opts["obfs-host"]
        p["plugin"] = "obfs"
        p["plugin-opts"] = po
        return True
    if name == "v2ray-plugin":
        mode = (opts.get("mode") or "websocket").lower()
        if mode not in ("websocket", "quic"):
            return False
        po = {"mode": mode}
        for k_src, k_dst in (("host", "host"), ("path", "path")):
            if opts.get(k_src):
                po[k_dst] = opts[k_src]
        if str(opts.get("tls", "")).lower() in ("1", "true"):
            po["tls"] = True
        if str(opts.get("mux", "")).lower() in ("1", "true"):
            po["mux"] = True
        p["plugin"] = "v2ray-plugin"
        p["plugin-opts"] = po
        return True
    return False


def _ssr_to_clash(uri, tag):
    """ssr:// → mihomo ssr 代理（协议/混淆/参数都是独立字段，不能当普通 ss 处理）。"""
    raw = lay.b64d(uri[6:].split("#")[0])
    if not raw:
        return None
    main, _, query = raw.partition("/?")
    main = main.rstrip("/")
    parts = main.rsplit(":", 5)          # host 可能是 IPv6，从右往左切
    if len(parts) < 6:
        return None
    host, port, protocol, method, obfs, pwd_b64 = parts
    if not host or not str(port).isdigit():
        return None
    qs = dict(urllib.parse.parse_qsl(query))
    p = {"name": tag, "type": "ssr", "server": host, "port": int(port),
         "cipher": method or "aes-256-cfb", "password": lay.b64d(pwd_b64) or pwd_b64,
         "obfs": obfs or "plain", "protocol": protocol or "origin", "udp": True}
    if qs.get("obfsparam"):
        p["obfs-param"] = lay.b64d(qs["obfsparam"]) or qs["obfsparam"]
    if qs.get("protoparam"):
        p["protocol-param"] = lay.b64d(qs["protoparam"]) or qs["protoparam"]
    return p


def _vmess_from_json(d, name):
    """把 v2rayN 的 vmess JSON 结构转成 clash 代理字典（vmess:// 与 ss:// JSON 变体共用）。"""
    if not isinstance(d, dict) or not d.get("add"):
        return None
    p = {
        "name": name or d.get("ps") or str(d["add"]),
        "type": "vmess", "server": d["add"], "port": int(d.get("port") or 443),
        "uuid": d.get("id", ""), "alterId": int(d.get("aid") or 0),
        "cipher": d.get("scy") or "auto", "udp": True,
    }
    # vmess 的 net 可能是 ws / grpc / h2 / http / httpupgrade / xhttp，不能一律当 tcp
    q = {"type": d.get("net") or "tcp", "path": d.get("path") or "",
         "host": d.get("host") or "", "serviceName": d.get("path") or "",
         "mode": d.get("mode") or "auto"}
    if not _clash_net(p, q, q["type"]):
        return None
    if str(d.get("tls", "")).lower() in ("tls", "true", "1"):
        p["tls"] = True
        if d.get("sni"):
            p["servername"] = d["sni"]
        elif d.get("host"):
            p["servername"] = d["host"]
        if d.get("alpn"):
            p["alpn"] = [a for a in str(d["alpn"]).replace(",", "/").split("/") if a]
        if d.get("fp"):
            p["client-fingerprint"] = d["fp"]
    return p


def uri_to_clash(uri, name):
    """把常见协议 URI 转成 mihomo 代理字典；不支持或畸形返回 None。

    字段名与语义对齐 mihomo 1.19.x（见 references/protocol.md）：
    trojan 恒为 TLS（URI 不写 security 也一样）；ss 支持 obfs / v2ray-plugin 插件；
    hysteria2 支持 obfs 与端口跳跃；tuic 支持 alpn / udp-relay-mode / congestion-controller。
    转换不了的组合返回 None，由调用方按「不支持」跳过——绝不静默退化成 tcp，
    否则节点会因为参数丢失而连不上，被误判成「不可达」。
    """
    low = uri.lower()
    try:
        if low.startswith("vmess://"):
            return _vmess_from_json(json.loads(try_b64decode(uri[8:].split("#")[0]) or "{}"), name)

        u = urllib.parse.urlsplit(uri)
        q = _q(uri)
        # user:pass 形式（tuic / hysteria2 常见）要把 password 拼回去，
        # 否则 uuid 被截断，配置生成直接失败
        userinfo = urllib.parse.unquote(u.username or "")
        if u.password:
            userinfo = f"{userinfo}:{urllib.parse.unquote(u.password)}"
        host, port = u.hostname, u.port or 443
        tag = _frag(uri) or f"{host}:{port}"
        tls = _tls_params(q)
        raw_net = (q.get("type") or "tcp").lower()

        if low.startswith("vless://"):
            if not userinfo:
                return None
            p = {"name": tag, "type": "vless", "server": host, "port": port,
                 "uuid": userinfo, "udp": True}
            if q.get("flow"):
                p["flow"] = q["flow"]
            if not _clash_net(p, q, raw_net):
                return None
            security = (q.get("security") or "").lower()
            if security in ("tls", "reality", "xtls"):
                p["tls"] = True
                if tls["sni"]:
                    p["servername"] = tls["sni"]
                if tls["alpn"]:
                    p["alpn"] = tls["alpn"]
                if tls["fp"]:
                    p["client-fingerprint"] = tls["fp"]
                if security == "reality":
                    pbk = q.get("pbk") or ""
                    if not pbk:              # 缺公钥的 REALITY 配置内核会直接拒绝
                        return None
                    p["reality-opts"] = {"public-key": pbk}
                    if q.get("sid"):
                        p["reality-opts"]["short-id"] = q["sid"]
                    p.setdefault("client-fingerprint", "chrome")
                if tls["insecure"]:
                    p["skip-cert-verify"] = True
            return p

        if low.startswith("trojan://"):
            if not userinfo:
                return None
            p = {"name": tag, "type": "trojan", "server": host, "port": port,
                 "password": userinfo, "udp": True, "tls": True}
            if tls["sni"]:
                p["sni"] = tls["sni"]
            if tls["alpn"]:
                p["alpn"] = tls["alpn"]
            if tls["fp"]:
                p["client-fingerprint"] = tls["fp"]
            if tls["insecure"]:
                p["skip-cert-verify"] = True
            if not _clash_net(p, q, raw_net):
                return None
            return p

        if low.startswith("ss://"):
            body = uri[5:].split("#")[0].split("?")[0]
            if "@" not in body:
                full = try_b64decode(body) or ""
                if full.lstrip().startswith("{"):
                    return _vmess_from_json(json.loads(full), tag)  # v2rayN JSON 变体
            method, pwd, plugin = lay._ss_cred(uri)  # noqa: SLF001
            hp = _ss_hostport(uri)
            if not hp:
                return None
            p = {"name": tag, "type": "ss", "server": hp[0], "port": hp[1],
                 "cipher": method or "aes-256-gcm", "password": pwd, "udp": True}
            if str(q.get("tfo") or "").lower() in ("1", "true"):
                p["tfo"] = True
            if plugin and not _clash_ss_plugin(p, q, plugin):
                return None
            return p

        if low.startswith("ssr://"):
            return _ssr_to_clash(uri, tag)

        if low.startswith(("hysteria2://", "hy2://")):
            if not userinfo:
                return None
            p = {"name": tag, "type": "hysteria2", "server": host, "port": port,
                 "password": userinfo, "udp": True}
            if tls["sni"]:
                p["sni"] = tls["sni"]
            if tls["alpn"]:
                p["alpn"] = tls["alpn"]
            if q.get("obfs"):
                p["obfs"] = q["obfs"]
                if q.get("obfs-password"):
                    p["obfs-password"] = q["obfs-password"]
            if q.get("mport"):               # 端口跳跃：443-8443 或 443:8443
                p["ports"] = q["mport"].replace(":", "-")
                if str(q.get("hop-interval") or "").isdigit():
                    p["hop-interval"] = int(q["hop-interval"])
            for k in ("up", "down"):
                if str(q.get(k) or "").isdigit():
                    p[k] = int(q[k])
            p["skip-cert-verify"] = tls["insecure"]
            return p

        if low.startswith("tuic://"):
            uuid, sep, pwd = userinfo.partition(":")
            if not sep or not uuid:          # 标准写法是 uuid:password，缺一不可
                return None
            p = {"name": tag, "type": "tuic", "server": host, "port": port,
                 "uuid": uuid, "password": pwd}
            if q.get("congestion_control"):
                p["congestion-controller"] = q["congestion_control"]
            if q.get("udp_relay_mode"):
                p["udp-relay-mode"] = q["udp_relay_mode"]
            if tls["alpn"]:
                p["alpn"] = tls["alpn"]
            if tls["sni"]:
                p["sni"] = tls["sni"]
            if str(q.get("disable_sni") or "").lower() in ("1", "true"):
                p["disable-sni"] = True
            if str(q.get("reduce_rtt") or "").lower() in ("1", "true"):
                p["reduce-rtt"] = True
            if tls["insecure"]:
                p["skip-cert-verify"] = True
            return p
    except Exception:  # noqa: BLE001
        return None
    return None


def _singbox_transport(q, raw_net):
    """传输层 → sing-box transport 对象；该内核不支持时返回 (None, False)。

    sing-box 1.14 只有 ws / grpc / http / httpupgrade / quic 五种；
    没有 xhttp（写了会 "unknown transport type: xhttp" 直接启动失败）。
    """
    net = lay.canon_net(raw_net)
    if not net or net == "tcp":
        return None, True
    path = q.get("path") or "/"
    host = q.get("host") or ""
    if net == "ws":
        tr = {"type": "ws", "path": path}
        if host:
            tr["headers"] = {"Host": host}
        if q.get("ed"):
            try:
                tr["max_early_data"] = int(q["ed"])
                tr["early_data_header_name"] = "Sec-WebSocket-Protocol"
            except ValueError:
                pass
        return tr, True
    if net == "grpc":
        return {"type": "grpc", "service_name": q.get("serviceName") or q.get("path") or ""}, True
    if net == "http":
        tr = {"type": "http", "path": path}
        if host:
            tr["host"] = [host]
        return tr, True
    if net == "httpupgrade":
        tr = {"type": "httpupgrade", "path": path}
        if host:
            tr["host"] = host
        return tr, True
    if net == "quic":
        return {"type": "quic"}, True
    return None, False


def _singbox_tls(q, server, force=False):
    """TLS 对象。force：trojan / hysteria2 / tuic 这类协议本体就跑在 TLS 上。"""
    security = (q.get("security") or "").lower()
    if not force and security not in ("tls", "reality", "xtls"):
        return None
    tls = _tls_params(q)
    t = {"enabled": True,
         "insecure": True,                      # 测试场景统一跳过证书校验
         "server_name": tls["sni"] or server}
    if tls["alpn"]:
        t["alpn"] = tls["alpn"]
    if security == "reality":
        pbk = q.get("pbk") or ""
        if not pbk:
            return None
        t["reality"] = {"enabled": True, "public_key": pbk}
        if q.get("sid"):
            t["reality"]["short_id"] = q["sid"]
        # REALITY 客户端必须走 uTLS，否则握手必失败
        t["utls"] = {"enabled": True, "fingerprint": tls["fp"] or "chrome"}
        t["insecure"] = False
    return t


def uri_to_singbox(uri, tag):
    """把常见协议 URI 转成 sing-box outbound；不支持或畸形返回 None。

    字段名对齐 sing-box 1.14.x（见 references/protocol.md）。特别注意：
    ss 插件写 plugin + plugin_opts（"obfs=http;obfs-host=x"），
    hysteria2 混淆写 obfs{type,password}、端口跳跃写 server_ports，
    tuic 写 udp_relay_mode / congestion_control + tls.alpn。
    """
    low = uri.lower()
    try:
        if low.startswith("vmess://"):
            d = json.loads(try_b64decode(uri[8:].split("#")[0]) or "{}")
            if not d.get("add"):
                return None
            ob = {"type": "vmess", "tag": tag, "server": d["add"],
                  "server_port": int(d.get("port") or 443),
                  "uuid": d.get("id", ""), "security": (d.get("scy") or "auto").lower(),
                  "alter_id": int(d.get("aid") or 0)}
            q = {"type": d.get("net") or "tcp", "path": d.get("path") or "",
                 "host": d.get("host") or "", "serviceName": d.get("path") or ""}
            tr, ok = _singbox_transport(q, q["type"])
            if not ok:
                return None
            if str(d.get("tls", "")).lower() in ("tls", "true", "1"):
                ob["tls"] = {"enabled": True, "insecure": True,
                             "server_name": d.get("sni") or d.get("host") or d["add"]}
                if d.get("alpn"):
                    ob["tls"]["alpn"] = [a for a in str(d["alpn"]).replace(",", "/").split("/") if a]
            if tr:
                if tr.get("type") == "quic" and not ob.get("tls"):
                    return None       # sing-box 的 QUIC 传输强制要求 TLS
                ob["transport"] = tr
            return ob

        u = urllib.parse.urlsplit(uri)
        q = _q(uri)
        # user:pass 形式（tuic / hysteria2 常见）要把 password 拼回去，
        # 否则 uuid 被截断，配置生成直接失败
        userinfo = urllib.parse.unquote(u.username or "")
        if u.password:
            userinfo = f"{userinfo}:{urllib.parse.unquote(u.password)}"
        host, port = u.hostname, u.port or 443
        raw_net = (q.get("type") or "tcp").lower()

        if low.startswith("vless://"):
            if not userinfo:
                return None
            ob = {"type": "vless", "tag": tag, "server": host, "server_port": port,
                  "uuid": userinfo}
            if q.get("flow"):
                ob["flow"] = q["flow"]
            t = _singbox_tls(q, host)
            if t:
                ob["tls"] = t
            elif (q.get("security") or "").lower() == "reality":
                return None
            tr, ok = _singbox_transport(q, raw_net)
            if not ok:
                return None
            if tr:
                if tr.get("type") == "quic" and not ob.get("tls"):
                    return None       # sing-box 的 QUIC 传输强制要求 TLS
                ob["transport"] = tr
            return ob

        if low.startswith("trojan://"):
            if not userinfo:
                return None
            ob = {"type": "trojan", "tag": tag, "server": host, "server_port": port,
                  "password": userinfo}
            t = _singbox_tls(q, host, force=True)
            if not t:
                return None
            ob["tls"] = t
            tr, ok = _singbox_transport(q, raw_net)
            if not ok:
                return None
            if tr:
                if tr.get("type") == "quic" and not ob.get("tls"):
                    return None       # sing-box 的 QUIC 传输强制要求 TLS
                ob["transport"] = tr
            return ob

        if low.startswith("ss://"):
            method, pwd, plugin = lay._ss_cred(uri)  # noqa: SLF001
            hp = _ss_hostport(uri)
            if not hp:
                return None
            ob = {"type": "shadowsocks", "tag": tag, "server": hp[0], "server_port": hp[1],
                  "method": method or "aes-256-gcm", "password": pwd}
            name, opts, raw = lay.split_plugin(plugin)
            if name:
                if name == "obfs":
                    ob["plugin"] = "obfs-local"
                    parts = [f"obfs={opts.get('obfs') or opts.get('mode') or 'http'}"]
                    if opts.get("obfs-host"):
                        parts.append(f"obfs-host={opts['obfs-host']}")
                    ob["plugin_opts"] = ";".join(parts)
                elif name == "v2ray-plugin":
                    ob["plugin"] = "v2ray-plugin"
                    ob["plugin_opts"] = raw or "mode=websocket"
                else:
                    return None
            return ob

        if low.startswith(("hysteria2://", "hy2://")):
            if not userinfo:
                return None
            ob = {"type": "hysteria2", "tag": tag, "server": host, "server_port": port,
                  "password": userinfo}
            if q.get("obfs"):
                ob["obfs"] = {"type": q["obfs"]}
                if q.get("obfs-password"):
                    ob["obfs"]["password"] = q["obfs-password"]
            if q.get("mport"):
                ob["server_ports"] = [q["mport"].replace("-", ":")]
                if str(q.get("hop-interval") or "").isdigit():
                    ob["hop_interval"] = f"{int(q['hop-interval'])}s"
            for k_src, k_dst in (("up", "up_mbps"), ("down", "down_mbps")):
                if str(q.get(k_src) or "").isdigit():
                    ob[k_dst] = int(q[k_src])
            t = _singbox_tls(q, host, force=True)
            if not t:
                return None
            ob["tls"] = t
            return ob

        if low.startswith("tuic://"):
            uuid, sep, pwd = userinfo.partition(":")
            if not sep or not uuid:
                return None
            ob = {"type": "tuic", "tag": tag, "server": host, "server_port": port,
                  "uuid": uuid, "password": pwd}
            if q.get("congestion_control"):
                ob["congestion_control"] = q["congestion_control"]
            if q.get("udp_relay_mode"):
                ob["udp_relay_mode"] = q["udp_relay_mode"]
            t = _singbox_tls(q, host, force=True)
            if not t:
                return None
            t.setdefault("alpn", ["h3"])         # tuic 走 QUIC，默认 ALPN 是 h3
            ob["tls"] = t
            return ob
    except Exception:  # noqa: BLE001
        return None
    return None


def extract_from_text(text, source, records):
    for uri in extract_uris(text):
        add_uri_record(records, uri, source)


def extract_from_json_obj(obj, source, records):
    """识别 sing-box 风格的 outbounds 或 JSON 数组节点。"""
    outbounds = None
    if isinstance(obj, dict):
        outbounds = obj.get("outbounds")
    elif isinstance(obj, list):
        outbounds = obj
    if not isinstance(outbounds, list):
        return False
    ok = 0
    for ob in outbounds:
        if not isinstance(ob, dict):
            continue
        typ = ob.get("type", "")
        if typ in ("direct", "block", "dns", "selector", "urltest") or not ob.get("server"):
            continue
        if typ in ("vmess", "vless", "trojan", "shadowsocks", "hysteria2", "tuic", "hysteria", "shadowtls"):
            records.append({"kind": "singbox", "outbound": ob, "parsed": None, "source": source})
            ok += 1
    return ok > 0


def _yaml_scalar(tok):
    """把 YAML 标量转成 Python 值（够用即可，不做完整规范实现）。"""
    tok = tok.strip()
    if not tok:
        return ""
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    low = tok.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    if re.fullmatch(r"-?\d+\.\d+", tok):
        return float(tok)
    if tok.startswith("[") and tok.endswith("]"):
        inner = tok[1:-1].strip()
        return [_yaml_scalar(x) for x in _split_flow(inner)] if inner else []
    if tok.startswith("{") and tok.endswith("}"):
        # 行内映射，如 reality-opts: {public-key: xxx, short-id: "yyy"}
        return _parse_flow_map(tok[1:-1])
    return tok


def _split_flow(body):
    """按顶层逗号切分，忽略引号与 {} [] 内的逗号。"""
    parts, buf, depth, quote = [], [], 0, None
    for ch in body:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "{[":
            depth += 1
            buf.append(ch)
        elif ch in "}]":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def _parse_flow_map(body):
    out = {}
    for part in _split_flow(body):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        out[k.strip().strip("\"'")] = _yaml_scalar(v)
    return out


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _parse_yaml_map(lines, idx, indent, seed):
    """解析 indent 缩进的 mapping 块，seed 为已解析的首个键值对。"""
    cur = seed
    while idx < len(lines):
        line = lines[idx]
        ind = _indent(line)
        if ind < indent:
            break
        s = line.strip()
        if s.startswith("- "):
            break
        if ind > indent:
            idx += 1
            continue
        k, sep, v = s.partition(":")
        if not sep:
            idx += 1
            continue
        key = k.strip().strip("\"'")
        if v.strip():
            cur[key] = _yaml_scalar(v)
            idx += 1
        else:
            nxt = idx + 1
            if nxt < len(lines) and _indent(lines[nxt]) > ind:
                child_indent = _indent(lines[nxt])
                if lines[nxt].strip().startswith("- "):
                    cur[key], idx = _parse_yaml_seq(lines, nxt, child_indent)
                else:
                    cur[key], idx = _parse_yaml_map(lines, nxt, child_indent, {})
            else:
                cur[key] = {}
                idx = nxt
    return cur, idx


def _parse_yaml_seq(lines, idx, indent):
    """解析 indent 缩进的 sequence 块（元素可为 flow map / 块状 mapping / 标量）。"""
    out = []
    while idx < len(lines):
        line = lines[idx]
        ind = _indent(line)
        if ind != indent or not line.strip().startswith("- "):
            break
        body = line.strip()[2:].strip()
        if not body:
            nxt = idx + 1
            if nxt < len(lines) and _indent(lines[nxt]) > ind:
                child_indent = _indent(lines[nxt])
                child, idx = (_parse_yaml_seq(lines, nxt, child_indent)
                              if lines[nxt].strip().startswith("- ")
                              else _parse_yaml_map(lines, nxt, child_indent, {}))
                out.append(child)
            else:
                out.append(None)
                idx = nxt
        elif body.startswith("{"):
            out.append(_parse_flow_map(body[1:].strip().rstrip("}").strip()))
            idx += 1
        elif re.match(r"^[\"'A-Za-z_][^:]*:", body):
            k, _, v = body.partition(":")
            key = k.strip().strip("\"'")
            seed = {key: _yaml_scalar(v) if v.strip() else {}}
            nxt = idx + 1
            if nxt < len(lines) and _indent(lines[nxt]) > ind:
                seed, idx = _parse_yaml_map(lines, nxt, _indent(lines[nxt]), seed)
            else:
                idx = nxt
            out.append(seed)
        else:
            out.append(_yaml_scalar(body))
            idx += 1
    return out, idx


def parse_clash_proxies_min(text):
    """纯标准库解析 clash 配置的 proxies 段（支持块状 `- name: x` 与 flow 式 `- {..}`）。

    没有 PyYAML 时用它兜底——之前完全解析不了块状 YAML，导致大量 clash 配置被丢弃。
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^proxies\s*:\s*$", line.rstrip()):
            start = i + 1
            break
    if start is None:
        return []

    block = []
    for line in lines[start:]:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if _indent(line) == 0 and re.match(r"^[A-Za-z_][\w-]*\s*:", line):
            break  # 回到顶层键，proxies 段结束
        block.append(line)
    if not block:
        return []

    first_indent = _indent(block[0])
    if block[0].strip().startswith("- "):
        items, _ = _parse_yaml_seq(block, 0, first_indent)
        return [p for p in items if isinstance(p, dict)]
    as_map, _ = _parse_yaml_map(block, 0, first_indent, {})
    for v in as_map.values():  # proxies 也可能是映射形式
        if isinstance(v, dict):
            return [v]
    return []


def try_parse_clash_yaml(text, source, records):
    """解析 clash YAML/JSON 的 proxies，尽力而为（PyYAML → 标准库迷你解析器 → JSON）。"""
    if "proxies:" not in text and '"proxies"' not in text:
        return False
    proxies = []
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            proxies = data.get("proxies") or []
    except ImportError:
        proxies = parse_clash_proxies_min(text)
        if not proxies:
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    proxies = data.get("proxies") or []
            except (ValueError, json.JSONDecodeError):
                proxies = []
    except Exception:  # noqa: BLE001
        return False

    ok = 0
    for p in proxies if isinstance(proxies, list) else []:
        if not isinstance(p, dict) or not p.get("server") or not p.get("port"):
            continue
        if p.get("type") in ("vmess", "vless", "trojan", "ss", "ssr", "hysteria2", "hysteria", "tuic"):
            records.append({"kind": "clash", "proxy": p, "parsed": None, "source": source})
            ok += 1
    return ok > 0


_QUOTA_CACHE = {"at": 0.0, "left": 999}


def quota_left_cached():
    """核心配额余量（缓存 60s，避免每个文件都查一次）。"""
    now = time.time()
    if now - _QUOTA_CACHE["at"] > 60:
        _QUOTA_CACHE["left"] = core_quota_remaining()
        _QUOTA_CACHE["at"] = now
    return _QUOTA_CACHE["left"]


def fetch_repo_file_text(repo_full, path, token, size=0):
    """按回退链下载文件内容：raw 直连 → raw 镜像代理（gh-proxy 等）→ jsDelivr CDN → GitHub contents API。

    大文件（>2MB）经镜像代理极易被截断（实测 3-5MB 文件几乎必挂），
    这类文件优先走 jsDelivr 分块 CDN，超时也放宽。

    **镜像与 CDN 走直连、不走上行通道**（2026-10-30 修复）：
    这两条腿存在的意义就是绕过 raw 被墙，它们本身是公网 CDN，直连即可；
    经通道反而多一跳，且行为取决于那个免费节点。实测 `free-nodes/clashfree`
    的 688KB 订阅：直连 testingcf 边缘 4s 拿到完整内容，而经通道时
    gh-proxy/jsDelivr 四个边缘**全部返回 200+0 字节**（旧代码把空正文当成功，
    仓库因此「下载成功但解析不到节点」整仓归零，历史 324 条）。
    raw 与 contents API 仍走通道——它们确实需要翻墙。
    """
    q = urllib.parse.quote(path)
    raw_url = f"{RAW_BASE}/{repo_full}/HEAD/{q}"
    mirrors = [m + raw_url for m in get_mirror_prefixes()]
    # 每个边缘节点都试 main / master 两个分支（按节点分组，避免在死节点上
    # 把两个分支都等一遍才换下一个可用节点）
    cdn = [f"https://{h}/gh/{repo_full}@{b}/{q}"
           for h in get_cdn_hosts() for b in ("main", "master")]
    large = size > LARGE_FILE_BYTES
    direct_legs = cdn + mirrors if large else mirrors + cdn
    attempts = [(u, True) for u in direct_legs]
    # raw 直连已知不通时放到最后：每个文件先撞一次 TLS 失败纯属浪费
    if raw_alive() is not False:
        attempts.insert(0, (raw_url, False))
    else:
        attempts.append((raw_url, False))
    timeout = 90 if large else 20
    last_err = None
    for url, direct in attempts:
        try:
            # 镜像/CDN 通道快速失败（不做重试），只有 contents API 保留重试
            return http_get_text(url, token, retries=0 if "api.github.com" not in url else 2,
                                 timeout=timeout, direct=direct)
        except Exception as e:  # noqa: BLE001
            last_err = e
    # 最后回退：contents API（消耗核心配额，返回 base64）
    # 配额紧张时跳过——它最贵也最不可靠，留着配额去列下一批仓库更值
    if quota_left_cached() <= 3:
        raise last_err
    try:
        # 这里传未转义的 path：github_api 内部统一做转义（传 q 会二次编码）
        data = github_api(f"/repos/{repo_full}/contents/{path}", token)
        content = data.get("content", "")
        if content:
            return base64.b64decode(content).decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        raise e from last_err
    raise last_err


def sniff_ext(text):
    """按内容推断订阅格式，用于没有扩展名的裸文件（clash / v2 / configs）。

    顺序有讲究：Clash 配置里同样散落着大量 URL 与 proxy 字样，必须先认 YAML
    结构，否则会被当纯 URI 列表解析，一条都出不来（实测把 clash 当文本解析得 0 条，
    按 yaml 解析得 200 条）。
    """
    head = text[:8192]
    if re.search(r"^\s*proxies\s*:", head, re.MULTILINE) or '"proxies"' in head:
        return ".yaml"
    if re.search(r"^\s*\"?outbounds\"?\s*:", head, re.MULTILINE) or '"outbounds"' in head:
        return ".json"
    stripped = head.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return ".json"
    return ""


def _strip_leading_comments(text):
    """剥掉 JSON 配置顶部那层 `#` 订阅头注释，否则 json.loads 必然失败。

    现在很多订阅站点（sinavm/SVM 等）把 sing-box 配置当成订阅分发，文件开头会塞
    `#profile-title` / `#subscription-userinfo` / `#announce` 这类头。文件名还叫 .json，
    正文确实是合法 sing-box 配置，但第一行起就是注释 → 解析器走文本兜底 → 0 条
    （2026-10-30 实测：9 个链接、700+ 节点全丢，known-issues 第 47 条）。

    只剥「首个非注释非空行之前」的那一段：正文里的 `#` 是 v2ray 分享链接的备注，
    也可能出现在 shell 片段里，不能全局删。
    """
    if not text or text.lstrip().startswith(("{", "[")):
        return text
    lines = text.splitlines()
    i = 0
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
        i += 1
    if 0 < i < len(lines):
        return "\n".join(lines[i:])
    return text


def extract_text_into(text, source, repo, records, ext="", kernel=None):
    """把一段文本按格式解析成节点记录，并给新记录打上来源仓库/内核标记。

    kernel：README 声明了这条链接属于哪个内核（"clash"/"xray"/…），
    写文件时据此豁免 layout.CAPS 的保守预筛——仓库作者既然标了「这是 clash 订阅」，
    这些节点就一定能进 clash 文件，不该被预筛判死。
    """
    before = len(records)
    ext = (ext or "").lower()
    if ext not in (".json", ".yaml", ".yml"):
        # 扩展名缺失或不是结构化格式时先嗅探内容，命中结构化格式就按结构化解析
        sniffed = sniff_ext(text)
        if sniffed:
            ext = sniffed
    if ext == ".json":
        # 订阅头注释（#profile-title …）挡在正文前面时 json.loads 必失败，先剥掉再解析
        body = _strip_leading_comments(text)
        try:
            obj = json.loads(body)
            if not extract_from_json_obj(obj, source, records):
                extract_from_text(text, source, records)
        except (ValueError, json.JSONDecodeError):
            extract_from_text(text, source, records)
    elif ext in (".yaml", ".yml"):
        if not try_parse_clash_yaml(text, source, records):
            extract_from_text(text, source, records)
    else:
        extract_from_text(text, source, records)
    for k in range(before, len(records)):
        records[k].setdefault("repo", repo)
        if kernel:
            records[k].setdefault("kernel", kernel)
    return len(records) - before


def fetch_and_extract(repo_full, path, token, records, size=0):
    """下载并提取单个文件。

    返回 (提取条数, 状态)，状态用于采集日志区分「下载失败」与「文件里没节点」——
    之前两者都记成 0 条，导致事后无法判断是网络问题还是解析能力不足。
    """
    try:
        text = fetch_repo_file_text(repo_full, path, token, size=size)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] 下载失败 {repo_full}/{path}: {e}", file=sys.stderr)
        return 0, "download_fail"
    n = extract_text_into(text, f"{repo_full}/{path}", repo_full, records,
                          os.path.splitext(path)[1])
    return n, ("ok" if n else "no_nodes")


# ---------------------------------------------------------------- 反向转换

def clash_to_uri(proxy):
    """把 clash 代理字典反解成标准分享链接，让 clash/sing-box 来源的节点也能进 v2ray 订阅。

    以前只写 URI 来源的节点，导致 clash 来源占多数时 v2ray_sub.txt 严重偏少。
    """
    try:
        typ = (proxy.get("type") or "").lower()
        server, port = proxy.get("server"), int(proxy.get("port") or 0)
        if not server or not port:
            return None
        name = urllib.parse.quote(str(proxy.get("name") or f"{server}:{port}"), safe="")
        net = (proxy.get("network") or "").lower()
        ws = proxy.get("ws-opts") or {}
        q = {}
        # 传输层：字段必须完整反解，丢一个参数就等于造了个连不上的链接
        if net == "ws":
            q["type"] = "ws"
            q["path"] = ws.get("path") or "/"
            host_hdr = (ws.get("headers") or {}).get("Host")
            if host_hdr:
                q["host"] = host_hdr
        elif net == "grpc":
            q["type"] = "grpc"
            q["serviceName"] = (proxy.get("grpc-opts") or {}).get("grpc-service-name", "")
        elif net == "h2":
            h2 = proxy.get("h2-opts") or {}
            q["type"] = "h2"
            q["path"] = h2.get("path") or "/"
            if h2.get("host"):
                q["host"] = (h2["host"] or [""])[0]
        elif net == "http":
            ho = proxy.get("http-opts") or {}
            q["type"] = "http"
            q["path"] = (ho.get("path") or ["/"])[0]
            hosts = (ho.get("headers") or {}).get("Host") or []
            if hosts:
                q["host"] = hosts[0]
        elif net == "xhttp":
            xo = proxy.get("xhttp-opts") or {}
            q["type"] = "xhttp"
            q["path"] = xo.get("path") or "/"
            if xo.get("host"):
                q["host"] = xo["host"]
            if xo.get("mode"):
                q["mode"] = xo["mode"]
        sni = proxy.get("servername") or proxy.get("sni") or ""
        reality = proxy.get("reality-opts") or {}
        if reality.get("public-key"):
            q.update({"security": "reality", "pbk": reality.get("public-key", ""),
                      "sid": reality.get("short-id", ""), "sni": sni,
                      "fp": proxy.get("client-fingerprint") or "chrome"})
        elif proxy.get("tls") or proxy.get("tls") is None and typ == "trojan":
            q["security"] = "tls"
            if sni:
                q["sni"] = sni
        if typ == "vless":
            if proxy.get("flow"):
                q["flow"] = proxy["flow"]
            qs = ("?" + urllib.parse.urlencode({k: v for k, v in q.items() if v})) if q else ""
            return f"vless://{proxy.get('uuid','')}@{server}:{port}{qs}#{name}"
        if typ == "vmess":
            d = {"v": "2", "ps": proxy.get("name", ""), "add": server, "port": str(port),
                 "id": proxy.get("uuid", ""), "aid": str(proxy.get("alterId", 0)),
                 "scy": proxy.get("cipher", "auto"), "net": net or "tcp",
                 "type": "none", "host": q.get("host", ""), "path": q.get("path", ""),
                 "tls": "tls" if q.get("security") in ("tls", "reality") else "",
                 "sni": sni}
            blob = base64.b64encode(json.dumps(d, ensure_ascii=False).encode()).decode()
            return f"vmess://{blob}"
        if typ == "trojan":
            q.setdefault("security", "tls")
            qs = "?" + urllib.parse.urlencode({k: v for k, v in q.items() if v})
            return f"trojan://{urllib.parse.quote(str(proxy.get('password','')))}@{server}:{port}{qs}#{name}"
        if typ == "ss":
            cred = f"{proxy.get('cipher','aes-256-gcm')}:{proxy.get('password','')}"
            blob = base64.b64encode(cred.encode()).decode().rstrip("=")
            extra = ""
            plugin = (proxy.get("plugin") or "").lower()
            po = proxy.get("plugin-opts") or {}
            if plugin == "obfs":
                parts = ["obfs-local", f"obfs={po.get('mode') or 'http'}"]
                if po.get("host"):
                    parts.append(f"obfs-host={po['host']}")
                extra = "?plugin=" + urllib.parse.quote(";".join(parts), safe="")
            elif plugin == "v2ray-plugin":
                parts = ["v2ray-plugin", f"mode={po.get('mode') or 'websocket'}"]
                for k in ("host", "path"):
                    if po.get(k):
                        parts.append(f"{k}={po[k]}")
                if po.get("tls"):
                    parts.append("tls")
                extra = "?plugin=" + urllib.parse.quote(";".join(parts), safe="")
            return f"ss://{blob}@{server}:{port}{extra}#{name}"
        if typ in ("hysteria2", "hysteria"):
            q2 = {}
            if sni:
                q2["sni"] = sni
            if proxy.get("skip-cert-verify"):
                q2["insecure"] = "1"
            if proxy.get("obfs"):
                q2["obfs"] = proxy["obfs"]
                if proxy.get("obfs-password"):
                    q2["obfs-password"] = proxy["obfs-password"]
            if proxy.get("ports"):
                q2["mport"] = str(proxy["ports"]).replace("-", ":")
            for k in ("up", "down"):
                if proxy.get(k):
                    q2[k] = str(proxy[k])
            qs = ("?" + urllib.parse.urlencode(q2)) if q2 else ""
            pwd = proxy.get("password") or proxy.get("auth") or ""
            return f"hysteria2://{urllib.parse.quote(str(pwd))}@{server}:{port}{qs}#{name}"
        if typ == "tuic":
            q2 = {}
            if sni:
                q2["sni"] = sni
            alpn = proxy.get("alpn")
            if isinstance(alpn, (list, tuple)):
                q2["alpn"] = "/".join(str(a) for a in alpn)
            elif alpn:
                q2["alpn"] = str(alpn)
            if proxy.get("udp-relay-mode"):
                q2["udp_relay_mode"] = proxy["udp-relay-mode"]
            if proxy.get("congestion-controller"):
                q2["congestion_control"] = proxy["congestion-controller"]
            if proxy.get("skip-cert-verify"):
                q2["allow_insecure"] = "1"
            qs = ("?" + urllib.parse.urlencode(q2)) if q2 else ""
            return (f"tuic://{proxy.get('uuid','')}:{urllib.parse.quote(str(proxy.get('password',''))) }"
                    f"@{server}:{port}{qs}#{name}")
    except Exception:  # noqa: BLE001
        return None
    return None


# ---------------------------------------------------------------- 去重与输出

def clash_to_singbox(proxy):
    """把 clash 代理字典转成 sing-box outbound，让 clash 来源的节点也出现在 sing-box 配置里。"""
    try:
        typ = (proxy.get("type") or "").lower()
        server, port = proxy.get("server"), int(proxy.get("port") or 0)
        if not server or not port:
            return None
        tag = str(proxy.get("name") or f"{server}:{port}")
        net = (proxy.get("network") or "").lower()
        ws = proxy.get("ws-opts") or {}
        transport = None
        if net == "ws":
            transport = {"type": "ws", "path": ws.get("path") or "/"}
            host_hdr = (ws.get("headers") or {}).get("Host")
            if host_hdr:
                transport["headers"] = {"Host": host_hdr}
        elif net == "grpc":
            transport = {"type": "grpc",
                         "service_name": (proxy.get("grpc-opts") or {}).get("grpc-service-name", "")}
        elif net == "h2":
            h2 = proxy.get("h2-opts") or {}
            transport = {"type": "http", "path": h2.get("path") or "/"}
            if h2.get("host"):
                transport["host"] = list(h2["host"])
        elif net == "http":
            ho = proxy.get("http-opts") or {}
            transport = {"type": "http", "path": (ho.get("path") or ["/"])[0]}
            hosts = (ho.get("headers") or {}).get("Host") or []
            if hosts:
                transport["host"] = list(hosts)
        elif net == "xhttp":
            return None     # sing-box 没有 xhttp 传输
        sni = proxy.get("servername") or proxy.get("sni") or ""
        reality = proxy.get("reality-opts") or {}
        tls = None
        if isinstance(reality, dict) and reality.get("public-key"):
            tls = {"enabled": True, "server_name": sni or server,
                   "utls": {"enabled": True,
                            "fingerprint": proxy.get("client-fingerprint") or "chrome"},
                   "reality": {"enabled": True, "public_key": reality.get("public-key", ""),
                               "short_id": reality.get("short-id", "")}}
        elif proxy.get("tls"):
            tls = {"enabled": True, "insecure": True, "server_name": sni or server}
        ob = {"tag": tag, "server": server, "server_port": port}
        if typ == "vless":
            ob.update({"type": "vless", "uuid": proxy.get("uuid", "")})
            if proxy.get("flow"):
                ob["flow"] = proxy["flow"]
        elif typ == "vmess":
            ob.update({"type": "vmess", "uuid": proxy.get("uuid", ""),
                       "security": proxy.get("cipher") or "auto",
                       "alter_id": int(proxy.get("alterId") or 0)})
        elif typ == "trojan":
            ob.update({"type": "trojan", "password": proxy.get("password", "")})
        elif typ == "ss":
            ob.update({"type": "shadowsocks", "method": proxy.get("cipher", "aes-256-gcm"),
                       "password": proxy.get("password", "")})
            plugin = (proxy.get("plugin") or "").lower()
            po = proxy.get("plugin-opts") or {}
            if plugin == "obfs":
                parts = [f"obfs={po.get('mode') or 'http'}"]
                if po.get("host"):
                    parts.append(f"obfs-host={po['host']}")
                ob["plugin"] = "obfs-local"
                ob["plugin_opts"] = ";".join(parts)
            elif plugin == "v2ray-plugin":
                parts = [f"mode={po.get('mode') or 'websocket'}"]
                for k in ("host", "path"):
                    if po.get(k):
                        parts.append(f"{k}={po[k]}")
                if po.get("tls"):
                    parts.append("tls")
                ob["plugin"] = "v2ray-plugin"
                ob["plugin_opts"] = ";".join(parts)
        elif typ in ("hysteria2", "hysteria"):
            ob.update({"type": "hysteria2", "password": proxy.get("password", "")})
            if proxy.get("obfs"):
                ob["obfs"] = {"type": proxy["obfs"]}
                if proxy.get("obfs-password"):
                    ob["obfs"]["password"] = proxy["obfs-password"]
            if proxy.get("ports"):
                ob["server_ports"] = [str(proxy["ports"]).replace("-", ":")]
            for k_src, k_dst in (("up", "up_mbps"), ("down", "down_mbps")):
                if proxy.get(k_src):
                    ob[k_dst] = int(proxy[k_src])
        elif typ == "tuic":
            ob.update({"type": "tuic", "uuid": proxy.get("uuid", ""),
                       "password": proxy.get("password", "")})
            if proxy.get("udp-relay-mode"):
                ob["udp_relay_mode"] = proxy["udp-relay-mode"]
            if proxy.get("congestion-controller"):
                ob["congestion_control"] = proxy["congestion-controller"]
            if tls and proxy.get("alpn"):
                tls["alpn"] = proxy["alpn"]
        else:
            return None
        if tls:
            ob["tls"] = tls
        if transport:
            ob["transport"] = transport
        return ob
    except Exception:  # noqa: BLE001
        return None

def record_hostport(record):
    """取记录对应的 (host, port)，三种来源格式统一处理。"""
    parsed = record.get("parsed")
    if parsed:
        return parsed[1], parsed[2]
    try:
        if record["kind"] == "clash":
            p = record["proxy"]
            return str(p.get("server", "")).lower(), int(p.get("port") or 0)
        if record["kind"] == "singbox":
            ob = record["outbound"]
            return str(ob.get("server", "")).lower(), int(ob.get("server_port") or 0)
    except (KeyError, ValueError, TypeError):
        return None
    return None


def dedupe(records):
    seen_uri, seen_hostport = set(), set()
    uniq, dropped = [], 0
    for r in records:
        uri_key = r["uri"] if r["kind"] == "uri" else None
        if uri_key:
            if uri_key in seen_uri:
                dropped += 1
                continue
            seen_uri.add(uri_key)
        hp = record_hostport(r)
        if hp and hp[1]:
            key = (hp[0], hp[1])
            if key in seen_hostport:
                dropped += 1
                continue
            seen_hostport.add(key)
        uniq.append(r)
    return uniq, dropped


# ---------------------------------------------------------------- TCP 延迟探测与排序

# Cloudflare 任播网段：这类入口 TCP 握手 10-40ms（就近接入边缘节点），但代理是否真的通
# 取决于回源配置——免费节点里大量是死的。只按 TCP 延迟排序会让它们霸占订阅最前面，
# 实测也证明它们可用率极低，因此排序时整体降权（排在真实节点之后、不可达节点之前）。
CF_NET_CIDRS = (
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22",
    "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32", "2405:b500::/32",
    "2405:8100::/32", "2a06:98c0::/29", "2c0f:f248::/32",
)
_CF_NETS = []


def is_cf_fronted(host):
    """判断 host 是否落在 Cloudflare 网段（域名无法离线判断，返回 False）。"""
    if not host:
        return False
    if not _CF_NETS:
        try:
            import ipaddress
            for cidr in CF_NET_CIDRS:
                try:
                    _CF_NETS.append(ipaddress.ip_network(cidr))
                except ValueError:
                    continue
        except ImportError:
            return False
    try:
        import ipaddress
        addr = ipaddress.ip_address(str(host))
    except ValueError:
        return False
    return any(addr in net for net in _CF_NETS)


def record_is_cf(record):
    hp = record_hostport(record)
    return is_cf_fronted(hp[0]) if hp else False


def tcp_latency_ms(host, port, timeout=1.5):
    """TCP 握手耗时（毫秒），不可达返回 None。用真实握手 RTT 作为延迟排序依据。"""
    if not host or not port:
        return None
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return int((time.perf_counter() - t0) * 1000)
    except (OSError, ValueError):
        return None


def probe_latencies(records, workers=128, timeout=1.5):
    """并发探测所有节点的 TCP 延迟，结果写回 record["tcp_latency"]（None=不可达）。

    同一 host:port 只探一次（聚合仓库里同一服务器常有几十条不同参数的节点）。
    """
    targets = {}
    for r in records:
        hp = record_hostport(r)
        if hp and hp[1]:
            targets.setdefault((hp[0], hp[1]), None)
    if not targets:
        return 0, 0
    print(f"[info] TCP 延迟探测：{len(targets)} 个服务器（并发 {workers}，超时 {timeout}s）…")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(tcp_latency_ms, host, port, timeout): (host, port)
                   for host, port in targets}
        for fut in as_completed(futures):
            targets[futures[fut]] = fut.result()
    reachable = sum(1 for v in targets.values() if v is not None)
    for r in records:
        hp = record_hostport(r)
        r["tcp_latency"] = targets.get((hp[0], hp[1])) if hp else None
    print(f"[info] TCP 延迟探测完成：可达 {reachable}/{len(targets)} 个服务器，耗时 {time.time()-t0:.0f}s")
    return reachable, len(targets)


def unique_names(names):
    used = {}
    out = []
    for n in names:
        n = (n or "").strip() or "node"
        if n in used:
            used[n] += 1
            n = f"{n} #{used[n]}"
        else:
            used[n] = 1
        out.append(n)
    return out


def singbox_to_uri(ob):
    """把 sing-box outbound 反解成标准分享链接，失败返回 None。

    以前这里直接返回空串（旧注释「sing-box 来源暂不反解」），后果比看起来严重：
    那些只提供 sing-box JSON 订阅的仓库，其节点既进不了 nodes_uris.txt 主清单，
    也就**不参与四内核可用性验证**——等于未经测试就发布，还进不了跨天池。
    README 按内核识别之后，`kernel=singbox` 的链接会更多，这个缺口必须补。
    覆盖 ss / trojan / vless / vmess / hysteria2 / tuic 六种；其余类型返回 None。
    """
    try:
        typ = (ob.get("type") or "").lower()
        server = ob.get("server")
        port = int(ob.get("server_port") or 0)
        if not server or not port:
            return None
        name = urllib.parse.quote(str(ob.get("tag") or f"{server}:{port}"), safe="")
        tls = ob.get("tls") or {}
        reality = tls.get("reality") or {}
        tr = ob.get("transport") or {}
        sni = tls.get("server_name") or ""
        insecure = bool(tls.get("insecure"))

        def tls_q():
            if not tls.get("enabled"):
                return {}
            q = {"security": "tls"}
            if sni:
                q["sni"] = sni
            if insecure:
                q["allowInsecure"] = "1"
            fp = (tls.get("utls") or {}).get("fingerprint")
            if fp:
                q["fp"] = fp
            if reality.get("enabled"):
                q["security"] = "reality"
                if reality.get("public_key"):
                    q["pbk"] = reality["public_key"]
                if reality.get("short_id"):
                    q["sid"] = reality["short_id"]
            return q

        def tr_q():
            t = (tr.get("type") or "").lower()
            if t == "ws":
                q = {"type": "ws", "path": tr.get("path") or "/"}
                host = (tr.get("headers") or {}).get("Host")
                if host:
                    q["host"] = host
                return q
            if t == "grpc":
                return {"type": "grpc", "serviceName": tr.get("service_name") or ""}
            if t in ("http", "h2"):
                q = {"type": "http", "path": tr.get("path") or "/"}
                hosts = tr.get("host") or []
                if isinstance(hosts, str):
                    hosts = [hosts]
                if hosts:
                    q["host"] = hosts[0]
                return q
            if t == "httpupgrade":
                q = {"type": "httpupgrade", "path": tr.get("path") or "/"}
                if tr.get("host"):
                    q["host"] = tr["host"]
                return q
            return {}

        if typ in ("shadowsocks", "ss"):
            cred = f"{ob.get('method') or 'aes-256-gcm'}:{ob.get('password') or ''}"
            blob = base64.b64encode(cred.encode()).decode().rstrip("=")
            extra = ""
            plugin = (ob.get("plugin") or "").lower()
            popts = ob.get("plugin_opts") or ""
            if plugin in ("obfs-local", "obfs"):
                extra = "?plugin=" + urllib.parse.quote("obfs-local;" + popts, safe="")
            elif plugin:
                extra = "?plugin=" + urllib.parse.quote(f"{plugin};{popts}", safe="")
            return f"ss://{blob}@{server}:{port}{extra}#{name}"
        if typ == "trojan":
            q = tls_q() or {"security": "tls"}
            q.update(tr_q())          # trojan 也能跑在 ws/grpc/httpupgrade 上
            qs = "?" + urllib.parse.urlencode({k: v for k, v in q.items() if v})
            pwd = urllib.parse.quote(str(ob.get("password") or ""))
            return f"trojan://{pwd}@{server}:{port}{qs}#{name}"
        if typ == "vless":
            q = {"encryption": "none"}
            q.update(tls_q())
            q.update(tr_q())
            if ob.get("flow"):
                q["flow"] = ob["flow"]
            qs = "?" + urllib.parse.urlencode({k: v for k, v in q.items() if v})
            return f"vless://{ob.get('uuid', '')}@{server}:{port}{qs}#{name}"
        if typ == "vmess":
            net = (tr.get("type") or "tcp").lower()
            d = {"v": "2", "ps": ob.get("tag") or f"{server}:{port}", "add": server,
                 "port": str(port), "id": ob.get("uuid", ""),
                 "aid": str(ob.get("alter_id") or 0), "scy": ob.get("security") or "auto",
                 "net": net, "type": "none",
                 "host": (tr.get("headers") or {}).get("Host") or sni,
                 "path": tr.get("path") or "",
                 "tls": "tls" if tls.get("enabled") else "", "sni": sni}
            blob = base64.b64encode(json.dumps(d, ensure_ascii=False).encode()).decode()
            return f"vmess://{blob}"
        if typ == "hysteria2":
            q = {}
            if sni:
                q["sni"] = sni
            if insecure:
                q["insecure"] = "1"
            obfs = ob.get("obfs")
            if isinstance(obfs, dict) and obfs.get("type"):
                q["obfs"] = obfs["type"]
                if obfs.get("password"):
                    q["obfs-password"] = obfs["password"]
            ports = ob.get("server_ports") or []
            if ports:
                q["mport"] = str(ports[0]).replace(":", "-")
            for k_src, k_dst in (("up_mbps", "up"), ("down_mbps", "down")):
                if ob.get(k_src):
                    q[k_dst] = str(ob[k_src])
            qs = ("?" + urllib.parse.urlencode(q)) if q else ""
            pwd = urllib.parse.quote(str(ob.get("password") or ""))
            return f"hysteria2://{pwd}@{server}:{port}{qs}#{name}"
        if typ == "tuic":
            q = {}
            if sni:
                q["sni"] = sni
            if ob.get("congestion_control"):
                q["congestion_control"] = ob["congestion_control"]
            if ob.get("udp_relay_mode"):
                q["udp_relay_mode"] = ob["udp_relay_mode"]
            alpn = tls.get("alpn") or []
            if alpn:
                q["alpn"] = "/".join(str(a) for a in alpn)
            if insecure:
                q["allow_insecure"] = "1"
            qs = ("?" + urllib.parse.urlencode(q)) if q else ""
            pwd = urllib.parse.quote(str(ob.get("password") or ""))
            return f"tuic://{ob.get('uuid', '')}:{pwd}@{server}:{port}{qs}#{name}"
    except (TypeError, ValueError, KeyError):
        return None
    return None


def record_uri(r):
    """把任意来源的记录还原成 URI（URI / clash / sing-box 三种来源都支持）。"""
    if r["kind"] == "uri":
        return r["uri"]
    if r["kind"] == "clash":
        try:
            return clash_to_uri(r["proxy"]) or ""
        except Exception:  # noqa: BLE001
            return ""
    if r["kind"] == "singbox":
        try:
            return singbox_to_uri(r["outbound"]) or ""
        except Exception:  # noqa: BLE001
            return ""
    return ""


def _hostport_of(proxy):
    return f"{proxy.get('server')}:{proxy.get('port')}"


def write_outputs(records, out_dir, date_str):
    """按四内核能力分流，各写一份「自己客户端能直接导入」的文件。

    同一个仓库订阅链接里的节点，按各内核支持的「代理协议 / 传输层 / 加密(REALITY) / flow」
    分流到 v2ray_sub.txt、xray_sub.txt、clash_sub.yaml、singbox_sub.json；
    另外写一份内部主清单 nodes_uris.txt（全部唯一 URI），验证阶段据此按内核能力取样。
    返回 {内核: {"path", "count"}}。
    """
    os.makedirs(out_dir, exist_ok=True)

    # 内部主清单：按记录顺序（已按 TCP 延迟升序）去重
    uris, seen = [], set()
    for r in records:
        u = record_uri(r)
        if u and u not in seen:
            seen.add(u)
            uris.append(u)
    lay.write_uris_file(lay.uris_path(out_dir), uris)

    # README 里明确声明了内核的链接（「Clash 订阅」「sing-box 配置」等），
    # 其节点按声明归入该内核并**豁免 CAPS 预筛**：作者已声明格式，CAPS 的保守规则
    # 可能把真能用的判死（宁可漏也不放宽是它原本的取舍）。
    declared = {}
    for r in records:
        k = r.get("kernel")
        if k in lay.CORES:
            u = record_uri(r)
            if u:
                declared.setdefault(k, set()).add(u)

    out = {}
    for core in lay.CORES:
        fmt = lay.CORE_FMT[core]
        if fmt == "base64":
            mine = lay.filter_uris(core, uris)
            extra = [u for u in uris if u in declared.get(core, ()) and u not in set(mine)]
            if extra:
                mine = mine + extra
                print(f"[info] {core}: {len(extra)} 条节点来自 README 声明的 {core} 订阅，"
                      f"豁免能力预筛")
            path, n = lay.write_core_file(lay.sub_path(out_dir, core), core, uris=mine)
        else:
            # clash / sing-box：优先用原始 proxy/outbound（保真），URI 来源再转换
            items, names, keys = [], [], set()
            allow = declared.get(core, set())
            for r in records:
                u = record_uri(r)
                if u and not lay.supports(core, u) and u not in allow:
                    continue
                if fmt == "clash":
                    if r["kind"] == "clash":
                        p = dict(r["proxy"])
                    else:
                        if not u:
                            continue
                        try:
                            p = uri_to_clash(u, "")
                        except Exception:  # noqa: BLE001
                            p = None
                    if not p or not p.get("server"):
                        continue
                    key = _hostport_of(p)
                    if key in keys:
                        continue
                    keys.add(key)
                    tag = (p.get("name") or "").strip()
                    if not tag or tag == "tmp":
                        tag = (_frag(u) if u else "") or key
                    items.append(p)
                else:
                    if r["kind"] == "singbox":
                        p = dict(r["outbound"])
                        key = f"{p.get('server')}:{p.get('server_port')}"
                    else:
                        if not u:
                            continue
                        try:
                            p = uri_to_singbox(u, "")
                        except Exception:  # noqa: BLE001
                            p = None
                        key = f"{p.get('server')}:{p.get('server_port')}" if p else ""
                    if not p or not key:
                        continue
                    if key in keys:
                        continue
                    keys.add(key)
                    tag = (p.get("tag") or "").strip()
                    if not tag or tag == "tmp":
                        tag = (_frag(u) if u else "") or key
                    items.append(p)
                names.append(tag)
            fixed = unique_names(names)
            for it, nm in zip(items, fixed):
                if fmt == "clash":
                    it["name"] = nm
                else:
                    it["tag"] = nm
            if fmt == "clash":
                path, n = lay.write_core_file(lay.sub_path(out_dir, core), core, proxies=items)
            else:
                path, n = lay.write_core_file(lay.sub_path(out_dir, core), core, outbounds=items)
        out[core] = {"path": path, "count": n}

    out["uris"] = len(uris)
    return out


def write_nodes_meta(out_dir, records, date_str, tcp_stats=None):
    """写出节点元数据（延迟 + 来源仓库），供验证阶段做「延迟优先取样」和「仓库质量考核」。"""
    nodes = []
    for r in records:
        hp = record_hostport(r)
        if not hp or not hp[1]:
            continue
        nodes.append({
            "key": f"{hp[0]}:{hp[1]}",
            "host": hp[0], "port": hp[1],
            "tcp_latency": r.get("tcp_latency"),
            "cf": record_is_cf(r),
            "repo": r.get("repo", ""),
            "source": r.get("source", ""),
        })
    lat = [n["tcp_latency"] for n in nodes if n.get("tcp_latency") is not None]
    buckets = {"<100ms": 0, "100-300ms": 0, "300-800ms": 0, ">800ms": 0, "不可达": 0}
    for n in nodes:
        v = n.get("tcp_latency")
        if v is None:
            buckets["不可达"] += 1
        elif v < 100:
            buckets["<100ms"] += 1
        elif v < 300:
            buckets["100-300ms"] += 1
        elif v < 800:
            buckets["300-800ms"] += 1
        else:
            buckets[">800ms"] += 1
    meta = {
        "date": date_str,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(nodes),
        "reachable": len(lat),
        "cf_fronted": sum(1 for n in nodes if n.get("cf")),
        "latency": {
            "min": min(lat) if lat else None,
            "median": sorted(lat)[len(lat) // 2] if lat else None,
            "max": max(lat) if lat else None,
            "buckets": buckets,
        },
        "tcp_probe": tcp_stats or {},
        "nodes": nodes,
    }
    path = lay.meta_path(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return path, meta


def run_probe_only(out_dir, date_str, args):
    """--probe-only：在「已采集」的候选清单上，只做本地 TCP 可达探测。

    为什么要有这个模式（2026-10-31）：采集搬到了 GitHub Actions（runner 直连 GitHub，
    不用自建上行代理、不依赖镜像、配额从匿名 60/时变成 token 5000/时），但**可达性必须
    回到本地网络判断**——免费节点的可达高度依赖出口位置，从 Azure 数据中心出口测出来的
    「可达/不可达」和你家宽带不是一回事（数据中心 IP 被大量节点封锁，会造成假阴性）。

    所以 CI 端用 --no-latency-sort 只做「下载 → 解析 → 去重 → 落盘」，产物与本地逐条相同；
    本地第一窗口先跑本模式：读 nodes/nodes_uris.txt → 探测 → 按 (不可达, CF 前置, 延迟) 排序
    → 只留可达 → 重写主清单 / 四份订阅 / 节点元数据。后续 test_nodes.py 原样接着跑。

    复用既有探测与写出函数，不复制格式转换逻辑；仓库/来源字段从上一步写下的元数据继承。
    """
    uris = lay.read_uris_file(lay.uris_path(out_dir))
    if not uris:
        print(f"[error] 未找到候选清单：{lay.uris_path(out_dir)}"
              f"（CI 采集是否已完成？）", file=sys.stderr)
        return 3

    # 上一段（CI）写下的元数据：仓库/来源在这里继承，探测结果用本地这份覆盖
    prev = {}
    meta_file = lay.meta_path(out_dir)
    if os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                for n in (json.load(f).get("nodes") or []):
                    if n.get("host") and n.get("port"):
                        prev[f"{n['host']}:{n['port']}"] = n
        except (OSError, ValueError) as e:
            print(f"[warn] 旧元数据读取失败，仓库字段将留空：{str(e)[:80]}")

    records, skipped = [], 0
    for u in uris:
        parsed = parse_uri_hostport(u)
        if not parsed:
            skipped += 1
            continue
        old = prev.get(f"{parsed[1]}:{parsed[2]}") or {}
        records.append({"kind": "uri", "uri": u, "parsed": parsed,
                        "repo": old.get("repo", ""), "source": old.get("source", "")})
    if not records:
        print("[error] 候选清单里没有可解析 host:port 的条目", file=sys.stderr)
        return 3
    print(f"[info] 候选清单 {len(uris)} 条，可解析 {len(records)} 条"
          + (f"（{skipped} 条解析不出 host:port，跳过）" if skipped else ""))

    reachable, probed = probe_latencies(records, args.latency_workers, args.latency_timeout)
    tcp_stats = {"workers": args.latency_workers, "timeout": args.latency_timeout,
                 "probed": probed, "reachable": reachable, "mode": "probe-only"}
    records.sort(key=lambda r: (r.get("tcp_latency") is None, record_is_cf(r),
                                r.get("tcp_latency") or 0))

    kept = records
    if not args.keep_dead:
        alive = [r for r in records if r.get("tcp_latency") is not None]
        if alive:
            print(f"[info] 只保留 TCP 可达节点：{len(records)} → {len(alive)} 条"
                  f"（丢弃不可达 {len(records) - len(alive)} 条）")
            kept = alive
        else:
            print("[warn] 本地探测全部不可达（本机网络异常？），保留全部候选写入，"
                  "避免本轮产物为空", file=sys.stderr)
    if args.keep_nodes and len(kept) > args.keep_nodes:
        print(f"[info] 按延迟截断：{len(kept)} → {args.keep_nodes} 条")
        kept = kept[:args.keep_nodes]

    out = write_outputs(kept, out_dir, date_str)
    write_nodes_meta(out_dir, kept, date_str, tcp_stats)
    cf_n = sum(1 for r in kept if record_is_cf(r))
    print(f"[done] 探测后产物已重写：主清单 {out.get('uris')} 条 URI（其中 CF 前置 {cf_n} 条已排末尾）"
          + "；" + "、".join(f"{k} {v['count']}" for k, v in out.items() if k != "uris"))
    return 0


def load_nodes_meta(input_dir):
    """读取 nodes/nodes_meta.json，返回 {"key": {...}}；缺失时返回空字典。"""
    path = lay.meta_path(input_dir)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}
    return {n["key"]: n for n in data.get("nodes", []) if n.get("key")}


def count_by_scheme(records):
    cnt = {}
    for r in records:
        if r["kind"] == "uri":
            s = r["parsed"][0] if r["parsed"] else "unknown"
        elif r["kind"] == "clash":
            s = r["proxy"].get("type", "unknown")
        else:
            s = r["outbound"].get("type", "unknown")
        if s == "shadowsocks":
            s = "ss"
        if s == "hy2":
            s = "hysteria2"
        cnt[s] = cnt.get(s, 0) + 1
    return dict(sorted(cnt.items(), key=lambda x: -x[1]))


def write_report(out_dir, date_str, repos, files_fetched, raw_count, uniq, dropped,
                 outputs, scheme_cnt, elapsed, meta=None, readme_stats=None,
                 seed_data=None, quality_order=None):
    path = lay.report_path(out_dir)
    repo_lines = "\n".join(
        f"| {r['full_name']} | ⭐{r['stars']} | {r['pushed_at'][:10]} |"
        for r in repos
    )
    src_counter = {}
    for r in uniq:
        src_counter[r["source"]] = src_counter.get(r["source"], 0) + 1
    src_lines = "\n".join(
        f"- `{k}`：{v} 个节点" for k, v in sorted(src_counter.items(), key=lambda x: -x[1])[:20]
    )

    # 延迟分布（采集阶段已按 TCP 握手延迟升序排好，低频节点排最后）
    lat_lines = "- 未做 TCP 延迟探测"
    if meta:
        b = meta.get("latency", {}).get("buckets", {})
        lat = meta.get("latency", {})
        lat_lines = "\n".join([
            f"- 可达服务器：**{meta.get('reachable', 0)}/{meta.get('total', 0)}**"
            f"（延迟中位数 {lat.get('median')}ms，最低 {lat.get('min')}ms）",
            f"- Cloudflare 前置节点：**{meta.get('cf_fronted', 0)}** 条"
            f"（TCP 握手快但代理多不通，已整体排在真实节点之后）",
            "",
            "| 延迟区间 | 节点数 |",
            "|---|---|",
            f"| <100ms | {b.get('<100ms', 0)} |",
            f"| 100-300ms | {b.get('100-300ms', 0)} |",
            f"| 300-800ms | {b.get('300-800ms', 0)} |",
            f"| >800ms | {b.get('>800ms', 0)} |",
            f"| 不可达（排在订阅末尾） | {b.get('不可达', 0)} |",
        ])

    # README 声明订阅链接的战果
    readme_lines = "- 无仓库在 README 中声明订阅链接"
    if readme_stats:
        hit = {k: v for k, v in readme_stats.items() if v.get("links")}
        if hit:
            rows = "\n".join(
                f"| {repo} | {st['links']} | {st.get('nodes', 0)} |"
                for repo, st in sorted(hit.items(), key=lambda kv: -kv[1].get("nodes", 0))[:15]
            )
            readme_lines = (f"共 **{len(hit)}** 个仓库在 README 里给出订阅链接，"
                            f"从中提取 **{sum(v.get('nodes', 0) for v in hit.values())}** 条节点。\n\n"
                            "| 仓库 | 声明链接数 | 提取节点数 |\n|---|---|---|\n" + rows)

    # 仓库质量排行（来自历史四内核实测）
    quality_lines = "- 暂无历史实测数据，本次验证后会自动建立质量评分"
    if seed_data:
        scored = [r for r in seed_data.get("repos", []) if r.get("tested")]
        scored.sort(key=lambda r: (-(r.get("quality") or 0), -(r.get("contributed") or 0)))
        if scored:
            rows = "\n".join(
                f"| {r['full_name']} | {r.get('quality')} | "
                f"{(r.get('avail_rate') or 0) * 100:.0f}%（{r.get('ok', 0)}/{r.get('tested', 0)}） | "
                f"{r.get('avg_latency') or '-'}ms | {r.get('contributed', 0)} |"
                for r in scored[:12]
            )
            quality_lines = ("| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |\n"
                             "|---|---|---|---|---|\n" + rows)

    perf_core = "、".join(f"{c} {outputs[c]['count']}" for c in lay.CORES if c in outputs)
    content = f"""### 概览

- 扫描仓库：**{len(repos)}** 个
- 抓取订阅文件：**{files_fetched}** 个
- 原始提取节点：**{raw_count}** 条
- 两级去重后（完整链接 + 服务器:端口）：**{len(uniq)}** 条（剔除重复 {dropped} 条）
- 各内核可处理节点数（按协议/传输/加密分流）：{perf_core}
- 耗时：{elapsed:.0f} 秒

### TCP 延迟分布

{lat_lines}

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

{readme_lines}

### 协议分布

| 协议 | 数量 |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in scheme_cnt.items()) + f"""

### 输出文件

- `v2ray_sub.txt`（{outputs.get('v2ray', {}).get('count', 0)} 条，base64 订阅）
- `xray_sub.txt`（{outputs.get('xray', {}).get('count', 0)} 条，base64 订阅）
- `clash_sub.yaml`（{outputs.get('clash', {}).get('count', 0)} 个代理）
- `singbox_sub.json`（{outputs.get('singbox', {}).get('count', 0)} 个 outbound）
- `nodes_uris.txt`（{outputs.get('uris', 0)} 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

{quality_lines}

{('- 本次采集优先级（质量从高到低）：' + quality_order) if quality_order else ''}

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
{repo_lines}

### 节点来源分布（去重后，前 20）

{src_lines or "- 无"}
"""
    # 时间倒序累积：同一天重跑会替换当天小节
    return lay.upsert_section(path, date_str, lay.now_stamp().split(" ")[1],
                              content,
                              doc_title="免费节点采集报告（时间倒序）",
                              intro="按日期倒序累积，最新一次运行在最上面")


# ---------------------------------------------------------------- 动态种子仓库清单

def load_seed_list(seed_file):
    """加载动态仓库清单（不存在则用内置默认）。返回 {full_name: stats}"""
    if os.path.exists(seed_file):
        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data.get("repos"):
                return data
        except (ValueError, json.JSONDecodeError, OSError):
            pass
    return {"repos": [{"full_name": n, "stars": 0, "contributed": 0, "last_collected": ""}
                      for n in DEFAULT_SEED_REPOS], "updated": ""}


def save_seed_list(seed_file, seed_data, date_str):
    """保存仓库清单：按贡献节点数与 star 排序，最多保留 300 个。

    上限从 80 提到 300：带 token 后每轮能扫几百个仓库，清单是「下次从哪补量」的
    唯一依据，截得太狠会把这次没见过效果的中小仓库永久丢掉。文件本身很小（每条一行 JSON）。
    """
    repos = [r for r in seed_data.get("repos", []) if r.get("full_name")]
    repos.sort(key=lambda r: (r.get("contributed", 0), r.get("stars", 0)), reverse=True)
    seed_data["repos"] = repos[:300]
    seed_data["updated"] = date_str
    try:
        os.makedirs(os.path.dirname(os.path.abspath(seed_file)), exist_ok=True)
        with open(seed_file, "w", encoding="utf-8") as f:
            json.dump(seed_data, f, ensure_ascii=False, indent=1)
    except OSError as e:
        print(f"[warn] 种子清单保存失败: {e}", file=sys.stderr)


def upsert_seed_stats(seed_data, repo_full, stars, contributed, date_str):
    """把本次采集贡献了节点的仓库写入/更新清单统计。"""
    for r in seed_data["repos"]:
        if r["full_name"] == repo_full:
            r["stars"] = max(r.get("stars", 0), stars)
            r["contributed"] = r.get("contributed", 0) + contributed
            r["last_collected"] = date_str
            return
    seed_data["repos"].append({"full_name": repo_full, "stars": stars,
                               "contributed": contributed, "last_collected": date_str})


# ---------------------------------------------------------------- 仓库质量考核

UNKNOWN_QUALITY = 50.0   # 未实测过的仓库给中等先验，避免被实测过的仓库完全压死
RATE_PRIOR = 0.25        # 未实测仓库在「采集/取样优先级」里的中性可用率


def quality_score(avail_rate, avg_latency):
    """仓库质量分（0-100）：可用率占 70 分，平均延迟占 30 分（5000ms 归零）。

    延迟项只在「确有可用节点」时计分：avg_latency 为空说明一个节点都没通过，
    没有任何延迟样本，此时延迟项必须记 0 —— 否则全死的仓库会因为「缺数据」
    反而拿满延迟分（历史 Bug：0% 可用率得 30 分，把 11% 可用率的 8 分压下去）。
    """
    rate = max(0.0, min(1.0, float(avail_rate or 0)))
    if rate <= 0 or avg_latency is None:
        return round(rate * 70, 1)
    # 免费节点实测延迟普遍 1500~7000ms，归零点取 5000ms；
    # 旧值 1500ms 会让延迟项对绝大多数仓库恒为 0，等于废掉这 30 分
    lat = max(0.0, 100.0 - float(avg_latency) / 50.0)
    return round(rate * 70 + lat * 0.3, 1)


def find_seed_entry(seed_data, repo_full):
    for r in seed_data.get("repos", []):
        if r["full_name"] == repo_full:
            return r
    return None


def repo_quality(seed_data, repo_full):
    """取仓库历史质量分；没实测过返回 None。"""
    entry = find_seed_entry(seed_data, repo_full)
    if not entry or not entry.get("tested"):
        return None
    return entry.get("quality")


def repo_sort_key(seed_data, repo_full):
    """采集优先级：实测可用率优先（未知走中性先验），其次历史贡献与 star。

    用可用率而不是总分：总分含延迟权重，会把「握手快但几乎全死」的仓库抬到前面。
    """
    entry = find_seed_entry(seed_data, repo_full) or {}
    rate = entry.get("avail_rate") if entry.get("tested") else None
    return (float(rate if rate is not None else RATE_PRIOR),
            int(entry.get("contributed", 0) or 0),
            int(entry.get("stars", 0) or 0))


def is_known_bad_repo(seed_data, repo_full, min_tests=20):
    """历史实测「一个可用都没有」的仓库，今天不必再浪费配额。

    唯一判据：实测 ≥20 个、可用 0 个（样本太少不跳，避免误杀新仓库）。

    刻意**不看可用率**：大仓库（OpenRay 2.2 万条、SoliSpirit 2.2 万条）的可用率
    天然只有 0.5%~1.3%，但绝对值有 20~27 个可用节点——按「可用率 < 2%」一刀切会把
    每天 18% 的可用节点（2026-10-29 实测 47/257）直接砍掉。可用率低不等于没价值，
    只有「绝对 0 个」才是真的白花配额（known-issues 第 46 条）。
    """
    entry = find_seed_entry(seed_data, repo_full)
    if not entry:
        return False
    tested = int(entry.get("tested") or 0)
    ok = int(entry.get("ok") or 0)
    return tested >= min_tests and ok == 0


def update_repo_quality(seed_file, per_repo, date_str, stars_map=None):
    """把验证结果按仓库汇总写入清单：可用率、平均延迟、质量分、历史走势。

    per_repo: {repo: {"tested": n, "ok": m, "latency_sum": ms, "latency_n": k}}
    由 test_nodes.py 在四内核实测后调用——这是仓库质量的唯一真实依据。
    """
    if not per_repo:
        return None
    seed_data = load_seed_list(seed_file)
    stars_map = stars_map or {}
    for repo, st in per_repo.items():
        entry = find_seed_entry(seed_data, repo)
        if not entry:
            entry = {"full_name": repo, "stars": stars_map.get(repo, 0),
                     "contributed": 0, "last_collected": ""}
            seed_data["repos"].append(entry)
        tested, ok = int(st.get("tested", 0)), int(st.get("ok", 0))
        if not tested:
            continue
        avg_lat = round(st["latency_sum"] / st["latency_n"]) if st.get("latency_n") else None
        entry["tested"] = tested
        entry["ok"] = ok
        entry["avail_rate"] = round(ok / tested, 3)
        entry["avg_latency"] = avg_lat
        entry["quality"] = quality_score(entry["avail_rate"], avg_lat)
        entry["last_tested"] = date_str
        hist = entry.get("quality_history") or []
        hist.append({"date": date_str, "rate": entry["avail_rate"],
                     "quality": entry["quality"], "tested": tested})
        entry["quality_history"] = hist[-7:]
    save_seed_list(seed_file, seed_data, date_str)
    return seed_data


def core_quota_remaining(token=None):
    """查询 GitHub 核心配额余量（此查询本身不计入配额）。"""
    try:
        data = github_api("/rate_limit", token)
        return int(data.get("resources", {}).get("core", {}).get("remaining", 60))
    except Exception:  # noqa: BLE001
        return 60


def collect_from_repos(repo_list, token, records, processed, contrib, counters, date_str,
                       per_repo_files=3, phase_log=None, seed_data=None,
                       readme_stats=None, skip_bad=True, reorder=True, deadline=None,
                       readme_only=False, date_tolerance=0, fail_reasons=None,
                       partial_fails=None):
    """对一批仓库执行「读 README → 列文件 → 下载 → 提取」。

    contrib 记录各仓库贡献的原始节点数；phase_log 记录 (仓库名, 节点数) 供采集日志使用
    （None=无候选文件，-1=下载失败，-2=历史质量过低跳过，-3=README 无订阅链接，
     -4=README 有链接但日期不是当天而跳过）。
    fail_reasons 记录 -1 的失败原因标签（HTTP 404 / 超时 / 网络异常名），
    没有它自检只能看到「下载失败」，无法区分上游路径失效与通道故障。
    partial_fails 记录 -1 之外、**部分链接下载失败**的仓库（"3/10 链接下载失败"）：
    这类仓库总节点数为 0，但原因是下载而不是解析，日志里标成「解析不到节点」会把排查带偏。
    seed_data 提供仓库质量分：quality 高的仓库先采，历史 0 可用的直接跳过。
    readme_only=True 时只跟随 README 里声明的订阅链接，不再按文件名猜目录（命中率更集中，
    也避免在无效仓库上白耗配额）；README 里没有链接的仓库直接跳过。
    """
    ordered = list(repo_list)
    if seed_data and reorder:
        # 质量优先；Python 排序稳定，同分仓库保持原有 star/更新时间顺序
        ordered.sort(key=lambda r: repo_sort_key(seed_data, r["full_name"]), reverse=True)
    for i, repo in enumerate(ordered, 1):
        full = repo["full_name"]
        if full in processed:
            continue
        if deadline and time.time() > deadline:
            print(f"[warn] 已达采集时间预算，剩余 {len(ordered) - i + 1} 个仓库留到下次；"
                  f"当前结果仍然完整可用（可用 --time-budget 调整上限）")
            break
        if skip_bad and seed_data and is_known_bad_repo(seed_data, full):
            entry = find_seed_entry(seed_data, full) or {}
            print(f"[info] ({i}/{len(ordered)}) {full} → 历史质量过低（实测 {entry.get('tested')} 个、"
                  f"可用 {entry.get('ok') or 0} 个），跳过以省配额")
            if phase_log is not None:
                phase_log.append((full, -2))
            processed.add(full)
            continue

        items = list_repo_files(full, token)
        readme_nodes = 0
        lstats = {}
        if items and (readme_stats is not None or readme_only):
            links, readme_nodes, detail, lstats = collect_from_readme(
                full, items, token, records, date_tolerance=date_tolerance)
            if readme_stats is not None:
                readme_stats[full] = {"links": links, "nodes": readme_nodes,
                                      "detail": detail, "stats": lstats}
            if links:
                day_note = ""
                if lstats.get("date_skipped"):
                    day_note = f"（另有 {lstats['date_skipped']} 个链接因日期不是当天跳过）"
                print(f"[info] ({i}/{len(ordered)}) {full} README 声明 {links} 个订阅链接"
                      f" → {readme_nodes} 条节点{day_note}（{'、'.join(detail[:4])}）")

        # README-only 模式：不再扫描仓库目录，README 没有订阅链接就跳过这个仓库
        if readme_only:
            if readme_nodes:
                counters["files"] += 1
                contrib[full] = contrib.get(full, 0) + readme_nodes
                if phase_log is not None:
                    phase_log.append((full, readme_nodes))
                print(f"[info] ({i}/{len(ordered)}) {full} → README 链接 {readme_nodes} 条节点")
            else:
                # 0 产出的原因必须分开记，否则日志会把「日期不符」误报成「没写链接」
                if not links and lstats.get("date_skipped"):
                    seen = "、".join(sorted(lstats.get("dates_seen") or {})[-3:])
                    kind, why = -4, (f"README 声明的 {lstats['date_skipped']} 个链接"
                                     f"日期不是当天（见到的日期：{seen or '未知'}），按策略跳过")
                elif links and detail and all("下载失败" in str(d) for d in detail):
                    # 注意：失败明细现在带原因后缀（`clash:下载失败(HTTP 404)`），
                    # 判断必须用 in 而不是 endswith，否则全部失败会被误归类成「解析不到节点」
                    tags = [m.group(1) for m in
                            (re.search(r"下载失败\(([^)]+)\)", str(d)) for d in detail) if m]
                    tag = max(set(tags), key=tags.count) if tags else ""
                    if tag and fail_reasons is not None:
                        fail_reasons[full] = tag
                    kind, why = -1, (f"README 声明的 {links} 个链接全部下载失败"
                                     + (f"（{tag}）" if tag else ""))
                elif links:
                    nfail = sum(1 for d in detail if "下载失败" in str(d))
                    if nfail and partial_fails is not None:
                        partial_fails[full] = f"{nfail}/{len(detail)} 个链接下载失败"
                    kind, why = 0, (
                        f"README 声明的 {links} 个链接部分下载失败（{nfail}/{len(detail)}），"
                        f"其余已下载但解析不到节点" if nfail
                        else f"README 声明的 {links} 个链接已下载但解析不到节点")
                else:
                    kind, why = -3, "README 未声明订阅链接"
                if phase_log is not None:
                    phase_log.append((full, kind))
                print(f"[info] ({i}/{len(ordered)}) {full} → {why}，跳过")
            processed.add(full)
            time.sleep(0.6)
            continue

        paths = pick_candidate_files(full, token, items=items)
        if not paths and not readme_nodes:
            if phase_log is not None:
                phase_log.append((full, None))
            processed.add(full)
            continue
        # README 已经拿到节点时少扫文件，把时间留给下一个仓库
        limit_files = max(1, per_repo_files - 1) if readme_nodes else per_repo_files
        got = readme_nodes
        statuses = ["README:ok"] if readme_nodes else []
        for p in paths[:limit_files]:
            n, st = fetch_and_extract(full, p["path"], token, records, size=p.get("size", 0))
            got += n
            statuses.append(f"{p['path']}:{st}")
        # 所有候选文件都没产出（下载失败或解析不到节点）→ 用 API 核对 HEAD 真实文件后重试一次
        # 典型场景：jsDelivr 列表是旧快照，给出的文件名在 HEAD 上已改名/不存在
        if got == 0 and statuses and all(not s.endswith(":ok") for s in statuses):
            items = list_repo_files(full, token, force_api=True)
            retry = _pick_from(items, limit=3, root_only=True)
            if not retry:
                subs = [it for it in items
                        if it["path"].count("/") == 1
                        and is_subdir_hint(it["path"].split("/")[0])]
                retry = _pick_from(subs, limit=2)
            for p in retry:
                if any(p["path"] == s.split(":")[0] for s in statuses):
                    continue
                n, st = fetch_and_extract(full, p["path"], token, records, size=p.get("size", 0))
                got += n
                statuses.append(f"{p['path']}:{st}")
        log_val = got
        if got:
            counters["files"] += 1
            contrib[full] = contrib.get(full, 0) + got
            print(f"[info] ({i}/{len(ordered)}) {full} → {got} 条节点（{'、'.join(statuses)}）")
        elif statuses and all(s.endswith("download_fail") for s in statuses):
            log_val = -1  # -1 = 下载失败（区别于 0 = 文件里没节点）
            print(f"[warn] ({i}/{len(ordered)}) {full} → 全部文件下载失败（{'、'.join(statuses)}）")
        else:
            print(f"[info] ({i}/{len(ordered)}) {full} → 文件已下载但无节点（{'、'.join(statuses)}）")
        if phase_log is not None:
            phase_log.append((full, log_val))
        processed.add(full)
        time.sleep(0.6)


def append_collection_log(log_file, date_str, phases, raw_count, uniq, dropped,
                          scheme_cnt, out_dir, target_reached, note="", readme_stats=None,
                          quality_hint=None, tcp_dead=0, fail_reasons=None,
                          partial_fails=None):
    """追加一条采集日志：日期、执行阶段、仓库明细（名称+节点数）、结果汇总。

    readme_stats 记录各仓库 README 声明的订阅链接与从中拿到的节点数（README 是很多仓库
    唯一的真实订阅入口）；quality_hint 记录本次按质量排序后的仓库优先级快照。
    """
    ts = datetime.now().strftime("%H:%M")
    lines = []
    phase_note = " → ".join(phases.keys())
    lines.append(f"- 执行阶段：{phase_note}{'' if target_reached else '（未达目标节点数）'}")
    if note:
        lines.append(f"- 备注：{note}")
    if quality_hint:
        lines.append(f"- 仓库优先级（质量分从高到低）：{quality_hint}")
    for phase_name, entries in phases.items():
        if not entries:
            continue
        lines.append(f"- {phase_name} 仓库明细（{len(entries)} 个）：")
        for full, got in entries:
            if got is None:
                lines.append(f"  - {full}：无可候选文件")
            elif got == -1:
                # 带原因后缀供自检归因；health_check 的解析是前缀匹配，后缀向后兼容
                reason = (fail_reasons or {}).get(full)
                lines.append(f"  - {full}：下载失败" + (f"（{reason}）" if reason else ""))
            elif got == -2:
                lines.append(f"  - {full}：质量过低跳过")
            elif got == -3:
                lines.append(f"  - {full}：README 未声明订阅链接，跳过（readme-only）")
            elif got == -4:
                lines.append(f"  - {full}：README 的链接日期不是当天，按策略跳过")
            elif got == 0:
                pf = (partial_fails or {}).get(full)
                lines.append(f"  - {full}：0 条（{pf}，其余已下载但解析不到节点）" if pf
                             else f"  - {full}：0 条（文件已下载但解析不到节点）")
            else:
                lines.append(f"  - {full}：{got} 条")
    if readme_stats:
        hit = {k: v for k, v in readme_stats.items() if v.get("links")}
        if hit:
            lines.append(f"- README 订阅链接（{len(hit)} 个仓库声明了链接）：")
            for repo, st in sorted(hit.items(), key=lambda kv: -kv[1].get("nodes", 0)):
                lines.append(f"  - {repo}：声明 {st['links']} 个 → 提取 {st.get('nodes', 0)} 条")
    scheme_str = " / ".join(f"{k} {v}" for k, v in scheme_cnt.items()) or "无"
    lines.append(f"- 结果：原始 {raw_count} 条 → 两级去重后 {uniq} 条（剔除 {dropped}）")
    if tcp_dead:
        # 单独记一行：自检的趋势对比要按「采集总量（过滤前）」比较，
        # 而 2026-10-28 之前的日志 uniq 本身就是过滤前的量（当时不过滤），
        # 不区分就会把「过滤后 2744 条」和「历史 13021 条」直接比，天天报降幅 >60%
        lines.append(f"- TCP 过滤：丢弃不可达 {tcp_dead} 条（采集总量 {uniq + tcp_dead} 条），"
                     f"保留 {uniq} 条")
    lines += [
        f"- 协议分布：{scheme_str}",
        f"- 输出目录：`{out_dir}`（nodes/ 下 v2ray_sub.txt / xray_sub.txt / clash_sub.yaml / "
        f"singbox_sub.json / nodes_uris.txt；Docs/ 下 report.md）",
    ]
    try:
        lay.upsert_section(log_file, date_str, ts, "\n".join(lines),
                           doc_title="免费节点采集日志（时间倒序）",
                           intro="每次运行一条，含执行阶段、仓库明细与结果；按日期倒序")
    except OSError as e:
        print(f"[warn] 采集日志写入失败: {e}", file=sys.stderr)


# ---------------------------------------------------------------- 主流程


def main():
    import uplink  # 延迟导入：uplink 反向依赖本模块

    ap = argparse.ArgumentParser(description="每日 GitHub 免费节点采集合并（自适应扩量 + 质量优先 + 延迟排序）")
    ap.add_argument("--out", default=None,
                    help="输出根目录（扁平存放，不分日期；默认 ./free-nodes）")
    ap.add_argument("--token", default=None,
                    help="GitHub Token（可选）。缺省时依次读 GITHUB_TOKEN/GH_TOKEN 环境变量、"
                         f"再读本地凭据文件 {TOKEN_FILE}；带 token 时核心配额 5000/时、搜索 30/分")
    ap.add_argument("--max-repos", type=int, default=80,
                    help="每个阶段最多扫描的新增仓库数（默认 80；带 token 时可放心放大）")
    ap.add_argument("--max-seeds", type=int, default=30,
                    help="节点不足时最多补充采集的种子仓库数（默认 30）")
    ap.add_argument("--search-pages", type=int, default=2,
                    help="每个关键词翻几页搜索结果（每页 100 条，默认 2 页；匿名限额下建议 1）")
    ap.add_argument("--search-days", type=int, default=3,
                    help="阶段2（节点不足时）的时间窗：放宽到前 N 天有更新的仓库（默认 3）")
    ap.add_argument("--readme-date-tolerance", type=int, default=0,
                    help="README 里按日期分列的订阅，允许取最近 N 天内的链接（默认 0=只要当天）")
    ap.add_argument("--target-nodes", type=int, default=1000, help="目标节点数，不足则逐级扩量")
    ap.add_argument("--min-stars", type=int, default=0, help="仓库最低 star 数")
    ap.add_argument("--seed-file", default=None, help="动态仓库清单路径（默认 <root>/src/seed_repos.json）")
    ap.add_argument("--test", action="store_true", help="采集完成后自动做节点可用性验证（调用 test_nodes.py）")
    ap.add_argument("--test-limit", type=int, default=200,
                    help="[限量模式] 每个内核单轮验证的节点数（初始取样量，也是扩量每轮的追加量）")
    ap.add_argument("--test-full-below", type=int, default=lay.FULL_BELOW,
                    help=f"[全量模式] 候选数不超过该值就全部验证（默认 {lay.FULL_BELOW}）")
    ap.add_argument("--test-max-test", type=int, default=lay.MAX_TEST,
                    help=f"[全量模式] 候选数超过 test-full-below 时，只验证排序前这么多（默认 {lay.MAX_TEST}）")
    ap.add_argument("--test-no-full-test", action="store_true",
                    help="关闭全量验证，回到 test-limit 初始取样 + 自适应扩量模式")
    ap.add_argument("--test-min-available", type=int, default=10,
                    help="[限量模式] 自适应扩量阈值：某内核可用数低于该值就继续追加测试（默认 10，0=关闭）")
    ap.add_argument("--test-limit-cap", type=int, default=0,
                    help="[限量模式] 单内核累计验证上限，0=自动（--test-limit 的 5 倍）")
    ap.add_argument("--test-workers", type=int, default=24,
                    help="单内核并发验证数（默认 24，与 test_nodes.py 一致；实测 12 并发只有 1.3 节点/s）")
    ap.add_argument("--test-cores", default="v2ray,xray,clash,singbox",
                    help="要验证的代理内核（默认 v2ray,xray,clash,singbox；clash 即 mihomo 内核）")
    ap.add_argument("--no-mirror-check", action="store_true",
                    help="跳过镜像探活（默认每轮运行探测一次并缓存排序结果）")
    ap.add_argument("--test-url",
                    default="https://gstatic.com/generate_204",
                    help="验证用测试地址。默认裸域 HTTPS（必须带 https，且不要加 www）："
                         "www.gstatic.com 在国内有缓存节点、直连即通，测不出出境能力；"
                         "裸域 gstatic.com 只有海外 IP，直连超时，能真实验证节点是否出境")
    ap.add_argument("--date", default=None, help="指定日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--no-latency-sort", action="store_true",
                    help="跳过 TCP 延迟探测与排序（省 1-2 分钟，但订阅不按延迟排序）")
    ap.add_argument("--latency-workers", type=int, default=128, help="延迟探测并发数")
    ap.add_argument("--latency-timeout", type=float, default=1.5, help="延迟探测超时（秒）")
    ap.add_argument("--keep-dead", action="store_true",
                    help="保留 TCP 不可达节点（排在订阅末尾）。**默认丢弃**：只发布 TCP 可达的节点，"
                         "订阅体积与后续验证量都不再含死节点（2026-10-28 用户要求）")
    ap.add_argument("--drop-dead", action="store_true",
                    help="（兼容保留；丢弃 TCP 不可达节点已是默认行为，传了也不报错）")
    ap.add_argument("--keep-nodes", type=int, default=0,
                    help="按延迟排序后只保留前 N 条（0 = 不截断）")
    ap.add_argument("--probe-only", action="store_true",
                    help="只对已有候选清单做本地 TCP 可达探测（采集已搬到 GitHub Actions 时用）："
                         "读 nodes/nodes_uris.txt → 探测 → 按延迟排序 → 只留 TCP 可达 → "
                         "重写主清单/四份订阅/节点元数据，后续 test_nodes.py 原样接着跑")
    ap.add_argument("--keep-bad-repos", action="store_true",
                    help="不跳过历史可用率为 0 的仓库（默认跳过以省配额）")
    ap.add_argument("--time-budget", type=int, default=2400,
                    help="采集阶段时间预算（秒，默认 2400=40 分钟；0=不限）")
    ap.add_argument("--pool-dir", default=None,
                    help="可用节点池目录（默认 <out父目录>/pool），验证阶段跨天累积复用")
    ap.add_argument("--readme-only", action="store_true",
                    help="只提取 README 中声明的订阅链接，不再扫描仓库目录；"
                         "README 没有订阅链接的仓库直接跳过")
    ap.add_argument("--uplink", default="auto",
                    help="GitHub 访问通道：auto=优先复用第 1 步已登记的自建代理，"
                         "没有则用已验证节点自建，不可用再直连，都不通则等待后重试；"
                         "direct=只用直连；也可直接给代理地址（如 http://127.0.0.1:7890）")
    ap.add_argument("--uplink-wait", type=int, default=600,
                    help="代理与直连都不通时，每次重试前等待的秒数（默认 600=10 分钟）")
    ap.add_argument("--uplink-retries", type=int, default=2,
                    help="代理与直连都不通时的重试次数（默认 2）")
    ap.add_argument("--uplink-max-candidates", type=int, default=40,
                    help="自建代理时最多尝试多少个候选节点")
    ap.add_argument("--check-kernels", action="store_true",
                    help="采集前先在**同一进程**里跑内核版本与能力检查，共用同一条自建代理通道。"
                         "本机执行环境会随父进程退出回收子进程，分步执行时第 1 步建的通道无法跨进程存活，"
                         "用这个开关可保证代理只建一次（第 1、2 步合一）")
    ap.add_argument("--check-kernels-update", action="store_true",
                    help="配合 --check-kernels：有新版本就下载升级内核")
    ap.add_argument("--check-kernels-skip-network", action="store_true",
                    help="配合 --check-kernels：不查上游版本（只做本地能力指纹）")
    args = ap.parse_args()
    args.token = load_github_token(args.token)

    tz = timezone(timedelta(hours=8))  # 东八区
    now = datetime.now(tz)
    date_str = args.date or now.strftime("%Y-%m-%d")
    today_iso = now.strftime("%Y-%m-%d")
    yesterday_iso = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    out_dir = os.path.abspath(args.out or "free-nodes")   # 扁平根目录，不再按日期建子目录
    seed_file = args.seed_file or lay.seed_file_path(out_dir)

    # ── 只做本地 TCP 可达探测（采集已在 CI 完成）：不碰网络下载、不建上行通道 ──
    if args.probe_only:
        sys.exit(run_probe_only(out_dir, date_str, args))

    # ── 可选：把内核检查跑在同一进程里，与采集共用一条上行通道 ──
    #    分步执行时，第 1 步起的代理子进程会随父进程退出被回收（本机 job 限制），
    #    所以「代理只建一次」靠这个开关实现（第 1、2 步合一）
    pre_uplink_handle = None
    if args.check_kernels:
        try:
            import check_kernels as ck  # noqa: PLC0415 — 延迟导入，避免顶层循环依赖
            rc_ck, _, pre_uplink_handle = ck.run_check(
                root=out_dir, update=args.check_kernels_update,
                skip_network=args.check_kernels_skip_network, date_str=date_str,
                uplink_arg=args.uplink, token=args.token)
            print(f"[info] 内核检查完成（退出码 {rc_ck}）"
                  + ("，采集沿用其建立的上行通道"
                     if pre_uplink_handle else "，未建立通道，采集阶段自行处理"))
        except Exception as e:  # noqa: BLE001
            print(f"[warn] 内核检查失败，继续采集：{str(e)[:120]}")

    # ── 上行通道：优先用已验证的节点自建代理访问 GitHub，其次直连，都不通就等 10 分钟重试 ──
    uplink_handle = pre_uplink_handle
    uplink_mode = "proxy" if pre_uplink_handle else "direct"
    if uplink_handle is None and args.uplink not in ("off", "direct"):
        if args.uplink == "auto":
            uplink_mode, uplink_handle = uplink.ensure(
                root=out_dir, retries=args.uplink_retries, retry_wait=args.uplink_wait,
                max_candidates=args.uplink_max_candidates)
        else:
            uplink.set_proxy_env(args.uplink)
            uplink.install_opener(args.uplink)
            uplink_mode = "proxy"
            print(f"[info] 上行通道：使用指定代理 {args.uplink}")
        if uplink_handle:
            atexit.register(uplink.stop, uplink_handle)   # 异常退出兜底；正常流程在采集结束时主动停
        print(f"[info] 上行通道：{uplink_mode}"
              + (f"（{uplink_handle.describe()}）" if uplink_handle else ""))

    # 镜像探活：可用前缀排前面，失效的沉底（否则每个文件都要在死镜像上空等超时）
    if not args.no_mirror_check:
        refresh_mirror_state()

    print(f"[info] 采集日期：{date_str}，目标节点数：{args.target_nodes}，输出目录：{out_dir}")
    print(f"[info] GitHub 身份：{token_desc(args.token)}"
          + (f"（核心配额 5000/时、搜索 30/分，每关键词翻 {args.search_pages} 页）"
             if args.token else "（匿名配额 60/时、搜索 10/分，仓库池会明显偏小）"))
    if args.readme_only:
        print("[info] 采集模式：README-only（只跟随 README 声明的订阅链接，不扫描仓库目录）")
    print(f"[info] 动态仓库清单：{seed_file}")
    t0 = time.time()
    deadline = (t0 + args.time_budget) if args.time_budget else None


    records, processed, contrib = [], set(), {}
    counters = {"files": 0}
    seed_data = load_seed_list(seed_file)
    readme_stats = {}
    log_file = lay.collection_log_path(out_dir)
    report_repos = []
    phases = {}  # 阶段名 → [(仓库名, 节点数或 None)]，供采集日志使用
    fail_reasons = {}  # 仓库名 → 失败原因标签（HTTP 404 / 超时 / …），写进采集日志供自检归因
    partial_fails = {}  # 仓库名 → "3/10 个链接下载失败"（总节点 0 但原因是下载，不是解析）

    def uniq_count():
        return len(dedupe(list(records))[0])

    def quota_left():
        left = core_quota_remaining(args.token)
        if left <= 5:
            print(f"[warn] GitHub 核心 API 配额仅剩 {left} 次，跳过本阶段（提供 --token 可提升限额）")
        return left

    def run_phase(name, repo_list, budget):
        """统一入口：质量优先排序 + README 优先 + 日志留痕。"""
        phases[name] = []
        collect_from_repos(repo_list[:budget], args.token, records, processed, contrib, counters,
                           date_str, phase_log=phases[name], seed_data=seed_data,
                           readme_stats=readme_stats, skip_bad=not args.keep_bad_repos,
                           deadline=deadline, readme_only=args.readme_only,
                           date_tolerance=args.readme_date_tolerance,
                           fail_reasons=fail_reasons, partial_fails=partial_fails)

    # 质量快照（写入日志，便于追溯「为什么先采这个仓库」）
    scored = [r for r in seed_data.get("repos", []) if r.get("tested")]
    scored.sort(key=lambda r: (-(r.get("avail_rate") or 0), -(r.get("contributed") or 0)))
    quality_hint = "、".join(
        f"{r['full_name']}(可用率{(r.get('avail_rate') or 0) * 100:.0f}%/质量{r.get('quality')})"
        for r in scored[:8])
    if quality_hint:
        print(f"[info] 质量优先顺序：{quality_hint}")

    # ── 阶段 1：当天有更新的仓库 ──
    repos_a = search_repos(args.token, args.max_repos, args.min_stars, today_iso,
                           pages=args.search_pages)
    print(f"[info] 阶段1（当天更新仓库）：发现 {len(repos_a)} 个候选")
    budget = max(0, quota_left() - 5)
    run_phase("阶段1·当天更新", repos_a, budget)
    report_repos.extend(repos_a)
    print(f"[info] 阶段1 完成，当前唯一节点：{uniq_count()} 条")

    # ── 阶段 2：仍不足 → 时间窗口放宽到前 N 天 + 扩大仓库数量 ──
    if uniq_count() < args.target_nodes:
        quota_left()
        wide_iso = (now - timedelta(days=max(1, args.search_days))).strftime("%Y-%m-%d")
        repos_b = search_repos(args.token, args.max_repos * 2, args.min_stars, wide_iso,
                              pages=args.search_pages)
        fresh = [r for r in repos_b if r["full_name"] not in processed]
        print(f"[info] 阶段2（放宽至前 {args.search_days} 天更新 {wide_iso} 起，"
              f"扩大仓库数）：新增候选 {len(fresh)} 个")
        budget = max(0, quota_left() - 5)
        run_phase(f"阶段2·放宽至前{args.search_days}天", fresh, budget)
        report_repos.extend(r for r in fresh if r["full_name"] not in {x["full_name"] for x in report_repos})
        print(f"[info] 阶段2 完成，当前唯一节点：{uniq_count()} 条")

    # ── 阶段 3：仍不足 → 补充采集动态清单中的主流种子仓库（按质量分排序）──
    if uniq_count() < args.target_nodes:
        quota_left()
        seed_repos = sorted(seed_data["repos"],
                            key=lambda r: (r.get("avail_rate") if r.get("tested") else RATE_PRIOR,
                                           r.get("contributed", 0), r.get("stars", 0)),
                            reverse=True)
        pending = []
        for r in seed_repos:
            if r["full_name"] in processed:
                continue
            pending.append(r)
            if len(pending) >= args.max_seeds:
                break
        print(f"[info] 阶段3（补充主流种子仓库，质量优先）：待采集 {len(pending)} 个")
        budget = max(0, quota_left() - 5)
        run_phase("阶段3·主流种子仓库", pending, budget)
        report_repos.extend({"full_name": r["full_name"], "stars": r.get("stars", 0),
                             "pushed_at": r.get("last_collected", "") or date_str}
                            for r in pending)
        print(f"[info] 阶段3 完成，当前唯一节点：{uniq_count()} 条")

    # ── 更新动态仓库清单 ──
    stars_map = {r["full_name"]: r.get("stars", 0) for r in report_repos}
    for full, got in contrib.items():
        upsert_seed_stats(seed_data, full, stars_map.get(full, 0), got, date_str)
    save_seed_list(seed_file, seed_data, date_str)
    print(f"[info] 动态仓库清单已更新（{len(seed_data['repos'])} 个仓库，本次贡献节点 {len(contrib)} 个仓库）")

    raw_count = len(records)
    uniq, dropped = dedupe(records)
    scheme_cnt = count_by_scheme(uniq)
    print(f"[info] 原始提取：{raw_count} 条 → 两级去重后：{len(uniq)} 条（剔除 {dropped} 条）")
    print(f"[info] 协议分布：{scheme_cnt}")
    if len(uniq) < args.target_nodes:
        print(f"[warn] 最终节点数 {len(uniq)} 未达目标 {args.target_nodes}，三级扩量均已执行；"
              f"建议提供 --token 提升配额后重试")

    # 保护：本次 0 条时不要覆盖目录里已有的有效结果（宁可保留上一次的，也不要写空）
    if not uniq:
        old_sub = lay.sub_path(out_dir, "v2ray")
        if os.path.exists(old_sub) and os.path.getsize(old_sub) > 0:
            print("[warn] 本次采集到 0 条节点，保留目录中已有的结果不覆盖"
                  "（检查配额/网络后重跑）", file=sys.stderr)
            append_collection_log(log_file, date_str, phases, raw_count, 0, dropped,
                                  scheme_cnt, os.path.abspath(out_dir), False,
                                  note="本次 0 条，已保留原有输出未覆盖",
                                  readme_stats=readme_stats, quality_hint=quality_hint,
                                  fail_reasons=fail_reasons, partial_fails=partial_fails)
            sys.exit(3)

    # ── TCP 延迟探测 + 升序排序（低延迟节点落在订阅最前面）──
    tcp_stats = {}
    dead_dropped = 0
    if not args.no_latency_sort:
        reachable, probed = probe_latencies(uniq, args.latency_workers, args.latency_timeout)
        tcp_stats = {"workers": args.latency_workers, "timeout": args.latency_timeout,
                     "probed": probed, "reachable": reachable}
        uniq.sort(key=lambda r: (r.get("tcp_latency") is None, record_is_cf(r),
                                 r.get("tcp_latency") or 0))
        cf_n = sum(1 for r in uniq if record_is_cf(r))
        if cf_n:
            print(f"[info] 其中 {cf_n} 条是 Cloudflare 前置节点：TCP 握手快但代理多不通，"
                  f"已整体排在真实节点之后（避免霸占订阅头部）")
        # 只发布 TCP 可达节点（默认）：TCP 都不通的节点不可能成为可用代理，
        # 留在订阅里只会把文件撑大（实测 16620 条里仅 6838 条可达），
        # 还会让后续验证把一半时间花在必然失败的节点上（2026-10-28 用户要求）。
        # 注意：--no-latency-sort 时没做过探测，tcp_latency 全是 None，此时绝不能过滤。
        if not args.keep_dead and not args.no_latency_sort:
            before = len(uniq)
            kept = [r for r in uniq if r.get("tcp_latency") is not None]
            if kept:
                dead_dropped = before - len(kept)
                uniq = kept
                print(f"[info] 已丢弃 TCP 不可达节点 {dead_dropped} 条，"
                      f"保留 {len(uniq)} 条（只发布 TCP 可达节点；--keep-dead 可关闭）")
            else:
                print("[warn] TCP 探测结果全部不可达（网络异常？），"
                      "保留全部节点写入，避免本轮产物为空", file=sys.stderr)
        if args.keep_nodes and len(uniq) > args.keep_nodes:
            print(f"[info] 按延迟排序后截断：{len(uniq)} → {args.keep_nodes} 条（只留低延迟节点）")
            uniq = uniq[:args.keep_nodes]
        if uniq:
            print(f"[info] 延迟排序完成，最快 {uniq[0].get('tcp_latency')}ms / "
                  f"末尾 {'不可达' if uniq[-1].get('tcp_latency') is None else str(uniq[-1].get('tcp_latency')) + 'ms'}")
        else:
            print("[warn] 本次没有任何节点通过解析（预算过短或全部来源失败），按空结果继续落盘")

    meta_path, meta = write_nodes_meta(out_dir, uniq, date_str, tcp_stats) if uniq else (None, None)
    out = write_outputs(uniq, out_dir, date_str)
    report = write_report(out_dir, date_str, report_repos, counters["files"],
                          raw_count, uniq, dropped, out, scheme_cnt, time.time() - t0,
                          meta=meta, readme_stats=readme_stats, seed_data=seed_data,
                          quality_order=quality_hint)
    append_collection_log(log_file, date_str, phases, raw_count, len(uniq), dropped,
                          scheme_cnt, os.path.abspath(out_dir), len(uniq) >= args.target_nodes,
                          readme_stats=readme_stats, quality_hint=quality_hint,
                          tcp_dead=dead_dropped, fail_reasons=fail_reasons,
                          partial_fails=partial_fails)
    print(f"[info] 采集日志已追加：{log_file}")
    print(f"[done] 报告：{report}")
    if meta_path:
        print(f"[done] 节点元数据：{meta_path}")
    print("[done] 输出：")
    for core in lay.CORES:
        info = out.get(core) or {}
        print(f"  - {os.path.basename(info.get('path', core))}：{info.get('count', 0)} 条")
    print(f"  - {lay.URIS_FILE}：{out.get('uris', 0)} 条（内部主清单）")

    # ── 采集结束：先停掉自建的上行代理，再进入四内核验证 ──
    # 验证阶段要独占本地端口并且必须测「节点本身」，留着代理既会干扰端口分配，
    # 也会让 urllib 的代理环境变量影响后续请求。
    if uplink_handle:
        uplink.stop(uplink_handle)
        uplink_handle = None
        uplink.set_proxy_env("")
        uplink.install_opener("")
        print("[info] 已停止上行通道（代理内核），接下来用四内核实测节点可用性")

    # ── 可选：自动验证节点可用性（含仓库质量考核 + 可用节点池）──
    if args.test:
        test_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_nodes.py")
        if args.test_no_full_test:
            policy_desc = (f"每内核单轮 {args.test_limit} 个，"
                           f"可用数 < {args.test_min_available} 自动扩量")
        else:
            policy_desc = (f"全量测试（候选 ≤ {args.test_full_below} 个全部验证；"
                           f"超过则取排序前 {args.test_max_test} 个）")
        print(f"[info] 开始节点可用性验证（内核：{args.test_cores}，{policy_desc}）…")
        cmd = [sys.executable, test_script,
               "--input", os.path.abspath(out_dir),
               "--out", os.path.abspath(out_dir),
               "--cores", args.test_cores,
               "--full-below", str(args.test_full_below),
               "--max-test", str(args.test_max_test),
               "--workers", str(args.test_workers),
               "--test-url", args.test_url,
               "--seed-file", seed_file,
               "--pool-dir", args.pool_dir or lay.pool_dir(out_dir)]
        if args.test_no_full_test:
            cmd += ["--no-full-test",
                    "--limit", str(args.test_limit),
                    "--min-available", str(args.test_min_available),
                    "--limit-cap", str(args.test_limit_cap)]
        rc = subprocess.call(cmd)
        if rc == 0:
            print("[done] 可用节点已写入 "
                  + "、".join(lay.AVAIL_FILE[c] for c in lay.parse_cores(args.test_cores)))
        else:
            print(f"[warn] 节点验证返回码 {rc}，可稍后单独运行 test_nodes.py", file=sys.stderr)


if __name__ == "__main__":
    main()
