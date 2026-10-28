#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""layout.py — 统一输出布局 / 内核能力矩阵 / 时间倒序的 md 日志

四内核（对外名，固定顺序）：v2ray → xray → clash → singbox

目录结构（2026-10-25 起，根目录只放 README 与 CHANGELOGS，其余按用途分三个子目录 + Skills）：
节点文件一律不分日期——过期节点没有意义，每次运行覆盖更新：

    <root>/
      README.md                 目录说明（人手写，脚本不覆盖）
      CHANGELOGS.md             修复/变更记录（按日期倒序累积）
      nodes/                    「生成的节点信息」全部在这里
        v2ray_sub.txt            采集：v2ray 内核可用的节点（base64 订阅）
        xray_sub.txt             采集：xray 内核可用的节点（base64 订阅）
        clash_sub.yaml           采集：clash/mihomo 可用节点（clash 配置）
        singbox_sub.json         采集：sing-box 可用节点（sing-box outbounds）
        available_v2ray.txt      验证通过（base64 订阅，可直接导入 v2rayN/v2rayNG）
        available_xray.txt       验证通过（base64 订阅）
        available_clash.yaml     验证通过（clash 配置）
        available_singbox.json   验证通过（sing-box 配置）
        nodes_uris.txt           内部主清单：全部唯一节点 URI（验证阶段的输入，按内核能力过滤）
        nodes_meta.json          节点元数据：TCP 延迟 + 来源仓库
        pool/pool_v2ray.txt      可用节点池（各内核 1 个文件，格式同上）
        pool/pool_xray.txt
        pool/pool_clash.yaml
        pool/pool_singbox.json
        pool/pool_state.json     池元数据（首见/最近通过/通过次数/最佳延迟），四内核共用
      Docs/                     「跟文档相关的文件」全部在这里
        protocol.md             四内核解析规范与实测校准报告
        proxy.md                自建代理与节点测试链路说明
        known-issues.md         踩坑知识库（现象/根因/修复/教训）+ 末尾「自检发现」区块（脚本自动写）
        sources.md              种子仓库来源说明
        tools-setup.md          内核二进制部署/升级方法
        report.md               采集报告       ┐
        summary.md              验证汇总       │ 都是「按日期倒序」累积：
        summary.json            验证最新快照   │ 新条目插到顶部，同一天重跑替换当天小节，
        health_check.md         自检报告       │ 最多保留 MAX_SECTIONS 个小节
        health_check.json       自检最新快照   │
        collection_logs.md      采集日志       │
        review_logs.md          自检摘要       ┘
      src/                      「脚本文件」+ 采集配置/状态（全链路脚本的唯一事实来源）
        collect_nodes.py / test_nodes.py / layout.py / pool.py / uplink.py …
        seed_repos.json         动态仓库清单（采集优先级 + 质量分）
        repo_quality.json       仓库质量历史
        kernel_state.json       内核版本与能力指纹基线
      Skills/                   技能定义（SKILL.md；脚本与文档分别见 src/ 与 Docs/）
      .workbuddy/memory/        项目记忆（MEMORY.md + 每日日志，纳入 git 跟踪）

内核能力矩阵（CAPS）：采集时按「代理协议 + 传输层 + 加密/REALITY + flow」把同一个订阅链接
里的节点分流到四个内核各自的文件；验证阶段再用真实内核作为最终裁判。
矩阵只用于「预筛明显不可能的节点」（比如 v2fly 不支持 REALITY），宁可放宽也不要漏掉真能用的。
"""

import base64
import json
import os
import re
import shutil
import sys
import urllib.parse
from datetime import datetime

# ---------------------------------------------------------------- 内核

CORES = ["v2ray", "xray", "clash", "singbox"]

# 别名 → 对外名（历史数据、命令行参数里可能用 mihomo/sing-box 等叫法）
ALIASES = {
    "mihomo": "clash", "meta": "clash", "clash-meta": "clash", "clashmeta": "clash",
    "v2fly": "v2ray", "v2ray-core": "v2ray", "xray-core": "xray",
    "sing-box": "singbox", "sing_box": "singbox", "sb": "singbox",
}

# 内核程序：子目录 + 可执行文件名（clash 对应的是 mihomo 内核）
CORE_BIN = {
    "v2ray": ("v2ray", "v2ray.exe"),
    "xray": ("xray", "xray.exe"),
    "clash": ("mihomo", "mihomo.exe"),
    "singbox": ("singbox", "sing-box.exe"),
}

# 每个内核只出一种「自己客户端能直接导入」的格式，不再重复生成别的格式
CORE_FMT = {"v2ray": "base64", "xray": "base64", "clash": "clash", "singbox": "singbox"}

SUB_FILE = {"v2ray": "v2ray_sub.txt", "xray": "xray_sub.txt",
            "clash": "clash_sub.yaml", "singbox": "singbox_sub.json"}
AVAIL_FILE = {"v2ray": "available_v2ray.txt", "xray": "available_xray.txt",
              "clash": "available_clash.yaml", "singbox": "available_singbox.json"}
POOL_FILE = {"v2ray": "pool_v2ray.txt", "xray": "pool_xray.txt",
             "clash": "pool_clash.yaml", "singbox": "pool_singbox.json"}

URIS_FILE = "nodes_uris.txt"       # 内部主清单
META_FILE = "nodes_meta.json"
STATE_FILE = "pool_state.json"
TESTED_STATE_FILE = "tested_state.json"   # 当日已测节点记录（多窗口续跑用，按日期自动重置）

# 子目录：根目录只留 README.md 与 CHANGELOGS.md（2026-10-25 布局调整）
NODES_DIR = "nodes"                # 生成的节点信息（订阅/可用清单/主清单/元数据/池）
DOCS_DIR = "Docs"                  # 文档（规范、报告、汇总、自检、日志）
SRC_DIR = "src"                    # 脚本 + 采集配置/状态
SKILLS_DIR = "Skills"              # 技能定义（SKILL.md）

# md 日志（全部时间倒序，放 Docs/；CHANGELOG_MD 例外，按用户要求留根目录）
REPORT_MD = "report.md"
SUMMARY_MD = "summary.md"
SUMMARY_JSON = "summary.json"
HEALTH_MD = "health_check.md"
HEALTH_JSON = "health_check.json"
ISSUE_MD = "known-issues.md"           # 单一文件：踩坑知识库（人工编号条目）+ 末尾「自检发现」区块
# 自检发现的问题写在同一个文件的末尾区块里（2026-10-26 合并：原先 known-issues.md 与
# known_issues.md 并存，名字只差一个连字符，实际内容还会互相抄串，极易混淆）
SELF_CHECK_TITLE = "## 自检发现（health_check 自动维护，按日期倒序）"
SELF_CHECK_MAX = 30
REVIEW_LOG_MD = "review_logs.md"
COLLECTION_LOG_MD = "collection_logs.md"
CHANGELOG_MD = "CHANGELOGS.md"     # 根目录（用户明确要求保留在 free-nodes/ 根下）
SEED_FILE = "seed_repos.json"      # src/：动态仓库清单
REPO_QUALITY_FILE = "repo_quality.json"   # src/：仓库质量历史
KERNEL_STATE_FILE = "kernel_state.json"   # src/：内核版本与能力指纹基线
MAX_SECTIONS = 30

# 全量测试策略默认值（2026-10-25 起，用户要求：晚间时间空闲，候选不多就全测；
# 上限最初笔误为 30000，用户当晚纠正为 3000）。
# 某内核候选数 ≤ FULL_BELOW → 全部测试；超过 → 只测排序前 MAX_TEST 个。
# 取值集中在 layout.py：test_nodes.py 与 collect_nodes.py 的命令行默认值都读它。
#
# 2026-10-28 下调到 2500：单次自动化只有 90 分钟，采集本身要 ~36 分钟，
# 验证侧实测吞吐 4.9~5.7 节点/s（24~32 并发、3s 超时、不复测）。
# 4 内核 × 3000 = 12000 个要 35~41 分钟，加上采集/自检/发布就压到 90 分钟红线；
# 2500 只要 29~34 分钟，总时长 ~72 分钟，留出真正可靠的余量。
# 另外采集侧默认已只发布 TCP 可达节点，单核候选本身就从 5~6 千降到 3 千上下。
FULL_BELOW = 2500
MAX_TEST = 2500

# ---------------------------------------------------------------- 能力矩阵

# URI 里 type= 的取值 → 规范名。
# h2 是 HTTP/2 传输的另一种写法（v2ray/xray 的 network 名是 http），
# splithttp 是 Xray 对 xhttp 的旧写法，两者内核侧等价。
NET_ALIAS = {
    "": "tcp", "none": "tcp", "tcp": "tcp", "raw": "tcp",
    "ws": "ws", "websocket": "ws", "grpc": "grpc", "gun": "grpc",
    "http": "http", "h2": "http", "h2c": "http",
    "kcp": "kcp", "mkcp": "kcp", "quic": "quic",
    "httpupgrade": "httpupgrade",
    "xhttp": "xhttp", "splithttp": "xhttp",
}

# 所有已知传输（不在表里的新写法按「未知」处理：预筛放行，转换器兜底跳过）
ALL_NETS = {"tcp", "ws", "grpc", "http", "kcp", "quic", "httpupgrade", "xhttp"}

# Shadowsocks 加密方式分组（2022 系列的口令必须是定长 base64 密钥）
SS_AEAD = {"aes-128-gcm", "aes-256-gcm", "chacha20-ietf-poly1305",
           "aead_aes_128_gcm", "aead_aes_256_gcm", "aead_chacha20_poly1305"}
SS_2022 = {"2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm",
           "2022-blake3-chacha20-poly1305"}

# 各内核能力矩阵。核对基线（2026-10-25，全部为本机实测的内核自校验结果）：
#   v2ray  5.53.0    tcp/kcp/ws/http(h2)/quic/grpc；无 reality、无 httpupgrade/xhttp/splithttp
#   xray   26.10.21  tcp/kcp/ws/grpc/httpupgrade/xhttp；HTTP、QUIC 传输已移除，VLESS/Trojan 必须 TLS；
#                    hysteria2 自 v26.1.23 引入（协议名是 "hysteria"+version:2，非 "hysteria2"，
#                    二进制含 HysteriaClientConfig/ServerConfig/ salamander/udphop/obfs，实测确认）
#   clash  1.19.33   tcp/ws/http/h2/grpc/xhttp；无 kcp/quic/httpupgrade
#   singbox 1.14.4   tcp/ws/http/grpc/httpupgrade/quic(TLS)；无 xhttp
# 详细字段与参数规范见 references/protocol.md；内核升级后由 check_kernels.py 能力指纹复核。
CAPS = {
    "v2ray": {
        # v2fly 5.x 支持 hysteria2（代理层+传输层双 hysteria2，密码在 hy2Settings，
        # 2026-10-25 官方文档 hy2.md + E2E 实测确认）；不支持 tuic、REALITY
        "protocols": {"vmess", "vless", "trojan", "ss", "hysteria2"},
        "reality": False,   # v2fly 不支持 REALITY（见 known-issues 第 4 条）
        "flow": True,       # v2fly 5.x 已支持 xtls-rprx-vision
        "nets": {"tcp", "kcp", "ws", "http", "quic", "grpc"},
        "ss_ciphers": SS_AEAD | {"none"},
        "ss_plugins": set(),          # v2fly 不支持 ss 插件（obfs / v2ray-plugin）
        "tls_required": set(),
    },
    "xray": {
        # Xray 26.x 起支持 hysteria2（v26.1.23 引入）：协议名 "hysteria" + settings.version=2，
        # 出站 address/port 平铺在 settings，认证密码在传输层 hysteriaSettings.auth；
        # 2026-10-25 二进制 + infra/conf/hysteria.go 源码 + xray run -test 实测确认，
        # 客户端能拨号并完成到服务端的 TLS 握手（详见 known-issues 第 27 条）。
        "protocols": {"vmess", "vless", "trojan", "ss", "hysteria2"},
        "reality": True,
        "flow": True,
        "nets": {"tcp", "kcp", "ws", "grpc", "httpupgrade", "xhttp"},
        "ss_ciphers": SS_AEAD | SS_2022,
        "ss_plugins": set(),          # Xray 也没有 ss 插件
        "tls_required": {"vless", "trojan"},   # 26.x 起禁止无 TLS 的 VLESS / Trojan
    },
    "clash": {
        "protocols": {"vmess", "vless", "trojan", "ss", "ssr", "hysteria2", "tuic"},
        "reality": True,
        "flow": True,
        "nets": {"tcp", "ws", "http", "h2", "grpc", "xhttp"},
        "ss_ciphers": None,           # mihomo 仍支持 CFB/rc4 等旧流加密，不做白名单
        "ss_plugins": {"obfs", "v2ray-plugin"},
        "tls_required": set(),
    },
    "singbox": {
        "protocols": {"vmess", "vless", "trojan", "ss", "hysteria2", "tuic"},
        "reality": True,
        "flow": True,
        "nets": {"tcp", "ws", "http", "grpc", "httpupgrade", "quic"},
        "ss_ciphers": None,           # 出站仍支持旧流加密（服务端入站已移除，实测确认）
        "ss_plugins": {"obfs", "v2ray-plugin"},   # 配置里写 obfs-local，见 protocol.md
        "tls_required": set(),
    },
}

SCHEME_ALIAS = {"hy2": "hysteria2", "shadowsocks": "ss", "ssr": "ssr"}


def canon_net(raw):
    """URI 的 type= 参数 → 规范传输名；未知返回空串。"""
    key = (raw or "").strip().lower()
    if key in NET_ALIAS:
        return NET_ALIAS[key]
    return key if key in ALL_NETS else ""


def canon(core):
    """把内核名/别名统一成对外名；未知名字原样返回（调用方可自行报错）。"""
    c = (core or "").strip().lower()
    return ALIASES.get(c, c)


def parse_cores(text, default=None):
    """把 "v2ray,xray,clash,singbox" 解析成规范名列表（去重保序）。"""
    seen, out = set(), []
    for part in (text or "").split(","):
        c = canon(part)
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out or list(default or CORES)


def _query(uri):
    try:
        return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(uri).query))
    except ValueError:
        return {}


def uri_proto(uri):
    """取 URI 的协议名（统一 hy2→hysteria2 等别名）。"""
    scheme = uri.split("://", 1)[0].lower() if "://" in uri else ""
    return SCHEME_ALIAS.get(scheme, scheme)


def b64d(text):
    """宽容的 base64 解码（标准/URL 安全、有无填充都试），失败返回空串。"""
    s = (text or "").strip().replace("-", "+").replace("_", "/")
    if not s:
        return ""
    s += "=" * (-len(s) % 4)
    for fn in (base64.b64decode, base64.urlsafe_b64decode):
        try:
            return fn(s).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            continue
    return ""


def split_plugin(spec):
    """ss 的 plugin 参数（如 obfs-local;obfs=http;obfs-host=a.com）→ (名字, 选项字典, 原始选项串)。"""
    raw = (spec or "").strip()
    if not raw:
        return "", {}, ""
    parts = [p for p in raw.split(";") if p]
    name = canon_plugin(parts[0])
    opts, kv = {}, []
    for p in parts[1:]:
        k, _, v = p.partition("=")
        opts[k.strip().lower()] = v.strip()
        kv.append(p.strip())
    return name, opts, ";".join(kv)


# 各家对同一个插件叫法不同：mihomo 叫 obfs，sing-box 叫 obfs-local，URI 里两种都有人写。
PLUGIN_ALIAS = {"obfs-local": "obfs", "obfslocal": "obfs", "simple-obfs": "obfs",
                "obfs": "obfs", "v2ray-plugin": "v2ray-plugin",
                "v2rayplugin": "v2ray-plugin", "v2ray_plugin": "v2ray-plugin",
                "shadow-tls": "shadow-tls", "shadowtls": "shadow-tls"}


def canon_plugin(name):
    key = (name or "").strip().lower()
    return PLUGIN_ALIAS.get(key, key)


def ss_2022_key_ok(cipher, password):
    """2022 系列的口令必须是 16/32 字节的 base64 密钥，否则内核直接拒绝配置。"""
    need = 16 if "128" in cipher else 32
    raw = b64d(password)
    if not raw:
        return False
    # b64d 返回 str，按字节长度判断需要重新解码成 bytes
    try:
        blob = base64.b64decode((password or "").strip().replace("-", "+").replace("_", "/")
                                + "=" * (-len(password or "") % 4))
    except Exception:  # noqa: BLE001
        return False
    return len(blob) == need


def _ss_cred(uri):
    """从 ss:// 链接里取 (method, password)；支持 SIP002 的全部四种写法。"""
    body = uri[5:].split("#")[0]
    query = ""
    if "?" in body:
        body, _, query = body.partition("?")
    if "@" in body:
        cred = body.rsplit("@", 1)[0]
        cred = b64d(cred) or cred
    else:
        full = b64d(body)
        cred = full.rpartition("@")[0] if "@" in full else full
    method, _, pwd = cred.partition(":")
    if not pwd:
        method, pwd = "aes-256-gcm", cred
    plugin = ""
    for k, v in urllib.parse.parse_qsl(query):
        if k.lower() == "plugin":
            plugin = urllib.parse.unquote(v)
    return method.strip().lower(), pwd, plugin


def node_facts(uri):
    """抽出「协议 / 传输 / 安全层 / 加密方式 / 插件」——能力预筛的唯一事实来源。

    采集分流、转换器、验证取样三处都调它，保证判断标准一致；
    链接畸形时返回空 proto，调用方按「不确定」放行。
    """
    facts = {"proto": "", "net": "tcp", "security": "", "flow": "",
             "cipher": "", "plugin": "", "host": "", "port": 0, "pbk": ""}
    uri = (uri or "").strip()
    if "://" not in uri:
        return facts
    facts["proto"] = uri_proto(uri)
    low = uri.lower()
    try:
        if low.startswith("vmess://"):
            d = json.loads(b64d(uri[8:].split("#")[0]) or "{}")
            facts["net"] = canon_net(d.get("net")) or "tcp"
            if str(d.get("tls", "")).lower() in ("tls", "true", "1"):
                facts["security"] = "tls"
            facts["cipher"] = str(d.get("scy") or "").lower()
            facts["host"] = str(d.get("add") or "")
            facts["port"] = int(d.get("port") or 0)
            facts["pbk"] = str(d.get("pbk") or "")
            return facts
        if low.startswith("ss://"):
            method, _pwd, plugin = _ss_cred(uri)
            facts["cipher"] = method
            facts["plugin"] = split_plugin(plugin)[0]
            return facts
        if low.startswith("ssr://"):
            raw = b64d(uri[6:])
            head = raw.split("/", 1)[0].split(":")
            if len(head) >= 4:
                facts["cipher"] = head[3].lower()
            return facts
        u = urllib.parse.urlsplit(uri)
        q = _query(uri)
        facts["net"] = canon_net(q.get("type")) or "tcp"
        facts["security"] = (q.get("security") or "").lower()
        facts["flow"] = q.get("flow") or ""
        facts["host"] = u.hostname or ""
        facts["port"] = u.port or 0
        facts["pbk"] = q.get("pbk") or ""
        if facts["proto"] in ("hysteria2", "tuic") and not facts["security"]:
            facts["security"] = "tls"      # 这两个协议底层就是 QUIC + TLS
    except Exception:  # noqa: BLE001
        return {"proto": "", "net": "tcp", "security": "", "flow": "",
                "cipher": "", "plugin": "", "host": "", "port": 0}
    return facts


def supports(core, uri):
    """该内核是否能处理这个节点（协议 / 传输 / 加密 / 插件 / 安全层 五层预筛）。

    判定全部来自本机内核实测过的能力（见 CAPS 注释），只排除**确定不支持**的组合；
    拿不准的（未知传输、畸形链接）一律放行，由真机验证做最终裁判。
    """
    exp = CAPS.get(canon(core))
    if not exp:
        return True
    f = node_facts(uri)
    proto = f["proto"]
    if not proto:
        return True
    if proto not in exp["protocols"]:
        return False

    net = f["net"]
    if net in ALL_NETS and net not in exp["nets"]:
        return False
    if net not in ALL_NETS:
        return True          # 未知传输：交给转换器/实测判断

    if proto == "ss":
        ciphers = exp.get("ss_ciphers")
        cipher = (f["cipher"] or "").lower()
        if ciphers is not None and cipher and cipher not in ciphers:
            return False
        if cipher in SS_2022:
            _m, pwd, _p = _ss_cred(uri)
            if not ss_2022_key_ok(cipher, pwd):
                return False
        plugin = (f["plugin"] or "").lower()
        if plugin and plugin not in (exp.get("ss_plugins") or set()):
            return False

    if f["security"] == "reality":
        if not exp["reality"]:
            return False
        # REALITY 公钥必须是 32 字节 base64url（43 字符）；残缺公钥内核会直接拒绝配置
        if len(f.get("pbk") or "") != 43:
            return False
    if f["flow"] and not exp["flow"]:
        return False
    if proto in (exp.get("tls_required") or ()) and f["security"] not in ("tls", "reality"):
        return False
    return True


def filter_uris(core, uris):
    return [u for u in uris if supports(core, u)]


# ---------------------------------------------------------------- 路径

def nodes_dir(root):
    return os.path.join(root, NODES_DIR)


def docs_dir(root):
    return os.path.join(root, DOCS_DIR)


def src_dir(root):
    return os.path.join(root, SRC_DIR)


def sub_path(root, core):
    return os.path.join(root, NODES_DIR, SUB_FILE[canon(core)])


def avail_path(root, core):
    return os.path.join(root, NODES_DIR, AVAIL_FILE[canon(core)])


def pool_dir(root):
    return os.path.join(root, NODES_DIR, "pool")


def pool_path(root, core):
    return os.path.join(pool_dir(root), POOL_FILE[canon(core)])


def pool_state_path(root):
    return os.path.join(pool_dir(root), STATE_FILE)


def tested_state_path(root):
    """当日已测记录放在 nodes/ 下（与池目录分开：池是跨天资产，这份是当天进度）。"""
    return os.path.join(root, NODES_DIR, TESTED_STATE_FILE)


def uris_path(root):
    return os.path.join(root, NODES_DIR, URIS_FILE)


def meta_path(root):
    return os.path.join(root, NODES_DIR, META_FILE)


def report_path(root):
    return os.path.join(root, DOCS_DIR, REPORT_MD)


def summary_path(root):
    return os.path.join(root, DOCS_DIR, SUMMARY_MD)


def summary_json_path(root):
    return os.path.join(root, DOCS_DIR, SUMMARY_JSON)


def health_path(root):
    return os.path.join(root, DOCS_DIR, HEALTH_MD)


def health_json_path(root):
    return os.path.join(root, DOCS_DIR, HEALTH_JSON)


def issue_path(root):
    return os.path.join(root, DOCS_DIR, ISSUE_MD)


def review_log_path(root):
    return os.path.join(root, DOCS_DIR, REVIEW_LOG_MD)


def collection_log_path(root):
    return os.path.join(root, DOCS_DIR, COLLECTION_LOG_MD)


def changelog_path(root):
    # CHANGELOGS.md 按用户要求留在根目录（与 README.md 一起）
    return os.path.join(root, CHANGELOG_MD)


def seed_file_path(root):
    return os.path.join(root, SRC_DIR, SEED_FILE)


def repo_quality_path(root):
    return os.path.join(root, SRC_DIR, REPO_QUALITY_FILE)


def kernel_state_path(root):
    return os.path.join(root, SRC_DIR, KERNEL_STATE_FILE)


# 一次性迁移：旧扁平布局（文件平铺在 root 下）→ 新布局（nodes/Docs/src）。
# 只搬「确定属于哪一类」的已知文件名，已在正确位置的不动；返回 {旧路径: 新路径}。
_LEGACY_MAP = {}
for _c in CORES:
    _LEGACY_MAP[SUB_FILE[_c]] = (NODES_DIR, SUB_FILE[_c])
    _LEGACY_MAP[AVAIL_FILE[_c]] = (NODES_DIR, AVAIL_FILE[_c])
    _LEGACY_MAP[POOL_FILE[_c]] = (NODES_DIR, os.path.join("pool", POOL_FILE[_c]))
_LEGACY_MAP.update({
    URIS_FILE: (NODES_DIR, URIS_FILE),
    META_FILE: (NODES_DIR, META_FILE),
    STATE_FILE: (NODES_DIR, os.path.join("pool", STATE_FILE)),
    REPORT_MD: (DOCS_DIR, REPORT_MD),
    SUMMARY_MD: (DOCS_DIR, SUMMARY_MD),
    SUMMARY_JSON: (DOCS_DIR, SUMMARY_JSON),
    HEALTH_MD: (DOCS_DIR, HEALTH_MD),
    HEALTH_JSON: (DOCS_DIR, HEALTH_JSON),
    ISSUE_MD: (DOCS_DIR, ISSUE_MD),
    REVIEW_LOG_MD: (DOCS_DIR, REVIEW_LOG_MD),
    COLLECTION_LOG_MD: (DOCS_DIR, COLLECTION_LOG_MD),
    SEED_FILE: (SRC_DIR, SEED_FILE),
    REPO_QUALITY_FILE: (SRC_DIR, REPO_QUALITY_FILE),
    KERNEL_STATE_FILE: (SRC_DIR, KERNEL_STATE_FILE),
    # 2026-10-25 复数规范化之前的旧名（一次性迁移兼容，存量树里可能还有）
    "known_issue.md": (DOCS_DIR, ISSUE_MD),
    "collection_log.md": (DOCS_DIR, COLLECTION_LOG_MD),
    "review_log.md": (DOCS_DIR, REVIEW_LOG_MD),
})


def migrate_legacy_flat(root):
    """把旧扁平布局的文件搬进 nodes/Docs/src（幂等；已就位的不动）。

    旧布局里 pool/ 是目录、changelog.md 已由调用方单独 git mv 成根目录 CHANGELOGS.md。
    """
    moved = {}
    for name, (subdir, newname) in _LEGACY_MAP.items():
        old = os.path.join(root, name)
        new = os.path.join(root, subdir, newname)
        if os.path.isfile(old) and not os.path.exists(new):
            os.makedirs(os.path.dirname(new), exist_ok=True)
            shutil.move(old, new)
            moved[old] = new
    # 旧 pool/ 目录整体搬到 nodes/pool（新位置不存在时才搬）
    old_pool, new_pool = os.path.join(root, "pool"), pool_dir(root)
    if os.path.isdir(old_pool) and not os.path.exists(new_pool):
        os.makedirs(new_pool, exist_ok=True)
        for f in os.listdir(old_pool):
            src = os.path.join(old_pool, f)
            if os.path.isfile(src):
                shutil.move(src, os.path.join(new_pool, f))
                moved[src] = os.path.join(new_pool, f)
    return moved


def is_legacy_date_dir(path):
    """判断是否是历史遗留的日期目录（迁移时清理用）。"""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", os.path.basename(path.rstrip("\\/"))))


# ---------------------------------------------------------------- 订阅文件读写

def _b64(text):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def node_list_text(uris):
    uris = [u for u in (uris or []) if u]
    return "\n".join(uris) + ("\n" if uris else "")


def clash_config(proxies):
    names = [p.get("name", "") for p in proxies]
    return {
        "mixed-port": 7890, "allow-lan": False, "mode": "rule", "log-level": "info",
        "proxies": proxies,
        "proxy-groups": [{"name": "PROXY", "type": "select",
                          "proxies": names[:300] + ["DIRECT"]}],
        "rules": ["MATCH,PROXY"],
    }


def singbox_config(outbounds):
    return {"log": {"level": "info"},
            "outbounds": list(outbounds) + [{"type": "direct", "tag": "direct"}]}


def write_core_file(path, core, uris=None, proxies=None, outbounds=None):
    """按内核的原生格式写文件，返回 (路径, 节点数)。"""
    fmt = CORE_FMT[canon(core)]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if fmt == "base64":
        text = node_list_text(uris)
        with open(path, "w", encoding="utf-8") as f:
            f.write(_b64(text))
        n = len([u for u in (uris or []) if u])
    elif fmt == "clash":
        proxies = [p for p in (proxies or []) if p.get("name")]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(clash_config(proxies), f, ensure_ascii=False, indent=1)
        n = len(proxies)
    else:
        outbounds = [o for o in (outbounds or []) if o.get("tag")]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(singbox_config(outbounds), f, ensure_ascii=False, indent=1)
        n = len(outbounds)
    return path, n


def read_uris_file(path):
    """读内部主清单（明文，一行一个 URI）。"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return [ln.strip() for ln in f if "://" in ln]


def write_uris_file(path, uris):
    with open(path, "w", encoding="utf-8") as f:
        f.write(node_list_text(uris))
    return path, len([u for u in (uris or []) if u])


# ---------------------------------------------------------------- md 日志（时间倒序）

_H2 = re.compile(r"^##\s+(.*)$")


def _split_doc(text):
    """拆成 (头部行列表, [(小节标题行, 小节正文行列表), ...])。"""
    head, sections, cur = [], [], None
    for line in text.splitlines():
        if _H2.match(line):
            cur = ([line], [])
            sections.append(cur)
        elif cur is None:
            head.append(line)
        else:
            cur[1].append(line)
    return head, sections


def upsert_section(path, date_str, heading="", body="", doc_title=None,
                   intro="", max_sections=MAX_SECTIONS, match_heading=False):
    """把「## <date> <heading>」小节插到文件顶部（时间倒序）。

    - match_heading=False（默认，用于日报类）：**同一天**的小节整段替换，
      避免重跑产生重复——report/summary/health_check 都是「当天一份结论」
    - match_heading=True（用于事件类）：只替换「同一天 + 同一标题」的小节，
      同一天的不同事件各自保留——changelog/known_issue 一天可能有多条变更，
      按日期替换会把当天先写入的记录整段抹掉
    - 超出 max_sections 的旧小节从尾部丢弃
    - 文件不存在时新建，首行是 doc_title
    """
    text = ""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            text = ""
    head, sections = _split_doc(text)
    if not head or not any(ln.startswith("# ") for ln in head):
        head = [f"# {doc_title or os.path.basename(path)}", ""]
        if intro:
            head += [f"> {intro}", ""]
    new_title = f"## {date_str} {heading}".rstrip()
    new_body = body.rstrip("\n").splitlines()
    # 需要替换的老小节：日报类按日期匹配，事件类按「日期 + 标题」匹配
    if match_heading:
        drop = lambda t: " ".join(t[0].split()) == " ".join(new_title.split())  # noqa: E731
    else:
        drop = lambda t: t[0].startswith(f"## {date_str}")  # noqa: E731
    sections = [(t, b) for t, b in sections if not drop(t)]
    sections.insert(0, ([new_title, ""], new_body))
    if max_sections and len(sections) > max_sections:
        sections = sections[:max_sections]

    out = [ln for ln in head]
    while out and not out[-1].strip():
        out.pop()
    out.append("")
    for title, body_lines in sections:
        out.extend(title)
        out.extend(body_lines)
        while out and not out[-1].strip():
            out.pop()
        out.append("")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip("\n") + "\n")
    return path


def append_changelog(root, date_str, heading, body):
    """修复/变更记录（含内核升级）统一入口。

    一天可以有多条不同主题的变更，所以按「日期 + 标题」去重（match_heading=True），
    同一天再写不同标题不会抹掉先前的记录。
    文件按用户要求放在根目录：<root>/CHANGELOGS.md。
    """
    return upsert_section(changelog_path(root), date_str, heading, body,
                          doc_title="变更与修复记录（时间倒序）",
                          intro="按日期倒序；包含脚本修复、参数调整、内核版本升级等",
                          match_heading=True)


def _split_self_check(text):
    """把 known-issues.md 拆成 (区块标题之前的行, 「自检发现」区块内的小节列表)。

    小节用三级标题 `### <日期> <标题>`，与知识库的二级标题 `## N.` 天然分开，
    所以写入自检记录永远不会挤掉知识库条目（这是合并两个文件时最关键的一点）。
    """
    lines = text.splitlines()
    idx = next((i for i, ln in enumerate(lines)
                if ln.strip().startswith("## 自检发现")), None)
    if idx is None:
        return lines, []
    head = lines[:idx + 1]
    sections = []
    cur_title, cur_body = None, []
    for ln in lines[idx + 1:]:
        if ln.startswith("### "):
            if cur_title is not None:
                sections.append((cur_title, cur_body))
            cur_title, cur_body = ln, []
        elif cur_title is not None:
            cur_body.append(ln)
    if cur_title is not None:
        sections.append((cur_title, cur_body))
    return head, sections


def append_issue(root, date_str, heading, body):
    """自检发现的问题 → Docs/known-issues.md 末尾的「自检发现」区块。

    与踩坑知识库同文件（用户要求合并，避免两个近似文件名混淆），但区块独立：
    只在该区块内按「日期 + 标题」替换，按 SELF_CHECK_MAX 截断，绝不触碰上面的知识库条目。
    """
    path = issue_path(root)
    text = ""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            text = ""
    first = text.splitlines()[0] if text.strip() else ""
    if not first.startswith("# "):
        # 文件不存在（或没有一级标题）：建骨架，知识库部分留空由人工补
        text = ("# 免费节点采集 — 已知问题与踩坑记录\n\n"
                "> 两类内容：① 踩坑知识库（人工维护，编号条目，每条含现象/根因/修复/教训）；\n"
                "> ② 自检发现的问题（`health_check.py` 自动写入文件末尾「自检发现」区块，按日期倒序）。\n\n"
                + SELF_CHECK_TITLE + "\n")

    head, sections = _split_self_check(text)
    if not any(ln.strip().startswith("## 自检发现") for ln in head):
        # 老文件（合并前的知识库）没有这个区块标题，先补上再写条目
        head = head + ["", SELF_CHECK_TITLE]
    new_title = f"### {date_str} {heading}".rstrip()
    new_body = body.rstrip("\n").splitlines()
    sections = [(t, b) for t, b in sections
                if " ".join(t.split()) != " ".join(new_title.split())]
    sections.insert(0, (new_title, new_body))
    if SELF_CHECK_MAX and len(sections) > SELF_CHECK_MAX:
        sections = sections[:SELF_CHECK_MAX]

    out = [ln.rstrip() for ln in head]
    while out and not out[-1].strip():
        out.pop()
    out.append("")
    for title, body_lines in sections:
        out.append(title)
        out.append("")
        for ln in body_lines:
            out.append(ln.rstrip())
        while out and not out[-1].strip():
            out.pop()
        out.append("")

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip("\n") + "\n")
    return path


def now_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ---------------------------------------------------------------- CLI

def _main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="md 日志工具：按日期倒序追加/替换小节")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, help_text in (("log", "写任意 md 日志"),
                            ("changelog", "写根目录 CHANGELOGS.md（修复/变更）"),
                            ("issue", "写 Docs/known-issues.md 的「自检发现」区块（问题）")):
        p = sub.add_parser(name, help=help_text)
        if name == "log":
            p.add_argument("--file", required=True, help="目标 md 文件路径")
            p.add_argument("--doc-title", default=None, help="文件首行标题（新建时用）")
        p.add_argument("--root", default=".", help="输出根目录（changelog/issue 用）")
        p.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                       help="日期 YYYY-MM-DD，默认今天")
        p.add_argument("--heading", default="", help="小节标题（跟在日期后面）")
        p.add_argument("--body", default="", help="小节正文；用 - 表示从 stdin 读")
    a = ap.parse_args(argv)

    body = sys.stdin.read() if a.body == "-" else a.body
    if a.cmd == "log":
        upsert_section(a.file, a.date, a.heading, body, doc_title=a.doc_title)
        print(f"[done] 已写入 {a.file}（{a.date}）")
    elif a.cmd == "changelog":
        print("[done]", append_changelog(a.root, a.date, a.heading, body))
    else:
        print("[done]", append_issue(a.root, a.date, a.heading, body))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
