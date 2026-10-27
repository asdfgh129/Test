# 已知问题与修复档案

本文是**一个文件、两类内容**（2026-10-26 合并：此前 `known-issues.md` 与 `known_issues.md`
两个文件并存，名字只差一个连字符，实际内容还会互相抄串，极易混淆）：

1. **踩坑知识库**（本文上方，人工维护）：每条 = 症状 → 根因 → 修复方式（含关键代码位置）
2. **自检发现**（本文末尾区块，`health_check.py` 自动写入，按日期倒序）

自检报出的症状，先上来对照。**修复完任何一条，都要按编号把新发现追加到末尾（自检区块之前）。**

---

## 1. 节点数远低于目标，仓库明细大量「下载失败」

- **症状**：`[warn] xxx → 全部文件下载失败`，节点数骤降
- **根因**：`raw.githubusercontent.com` 直连被墙；镜像代理对 >2MB 文件几乎必然截断
- **修复**（`collect_nodes.py`）：
  - 四级回退：raw → 镜像前缀 → jsDelivr → contents API
  - `fetch_repo_file_text(..., size=)`：`size > LARGE_FILE_BYTES`(2MB) 时**优先 jsDelivr**，超时放宽到 90s
  - `_score_entry()`：候选文件打分时给 >2MB 的文件减分，优先挑体积适中的
  - `collect_from_repos()`：根目录文件全部下载失败时，回落扫描子目录里更小的文件

## 2. 仓库「无可候选文件」

- **根因**：订阅文件不在根目录，而在 `Subscriptions/`、`source/`、`output/`、`dist/` 等子目录
- **修复**：`SUBDIR_HINTS` + `MAX_SUBDIR_SCAN`（默认 2 个目录），`pick_candidate_files()` 在根目录无货时自动下钻一层
- **注意**：子目录扫描会多消耗 contents API 配额，只在根目录无货时才触发

## 3. 仓库「0 条（文件已下载但解析不到节点）」

- **根因**：环境没有 PyYAML，块状 YAML（`- name: xxx` 换行缩进式）的 clash 配置**整体解析失败**，
  旧实现只能勉强处理 flow 式 `- {name: xx}`，导致大量真实可用的 clash 配置被丢弃
- **修复**：`collect_nodes.parse_clash_proxies_min()` —— 纯标准库的 YAML 子集解析器
  （支持块状 mapping、sequence、嵌套 `ws-opts`/`reality-opts`、flow map、引号、布尔/数字）
- **验证窍门**：抓 1 个失败样本，直接调 `try_parse_clash_yaml(text, 'x')` 看返回条数

## 4. 某内核可用数为 0（内核启动即失败）

| 内核 | 症状 | 根因 | 修复位置 |
|---|---|---|---|
| mihomo | 全部 3ms 内失败 | 并发实例共用数据目录 → 会话冲突 | `test_nodes.py` 每个实例独立 `-d` |
| mihomo | 全部 TLS 报错 | 共享证书节点校验证书失败 | clash 配置加 `skip-cert-verify: true` |
| mihomo | reality 节点全挂 | 缺 `reality-opts` / `client-fingerprint` | `collect_nodes.uri_to_clash` |
| sing-box | 启动即 fatal | reality 必须开 uTLS | `collect_nodes.uri_to_singbox` 加 `tls.utls` |
| v2ray(v2fly) | 可用率很低（<10%） | 内核本身不支持 reality/xhttp（**正常现象**） | 无需修复，但需在汇报中说明 |

## 5. GitHub API 配额耗尽（每日采集卡住的主因）

- **症状**：`[warn] GitHub 核心 API 配额仅剩 N 次，跳过本阶段`；三个阶段全跳过，节点数 0
- **根因**：匿名核心配额只有 **60 次/小时**，而"列仓库目录"每仓库都要 1 次；30 个仓库 + 子目录扫描轻松超限
- **修复**：`list_repo_files()` **默认走 jsDelivr data API 列目录**
  （`https://data.jsdelivr.com/v1/packages/gh/<repo>@<branch>?structure=flat`，返回完整扁平文件树，**不消耗 GitHub 配额**）
  - jsDelivr 不可用时才回落 contents API（只列根目录）
  - 配额 ≤3 时跳过 contents API 下载兜底，把配额留给列目录
  - 实测：配额只剩 2 次时仍能采到 6400+ 节点
- **注意**：jsDelivr 列表可能是**旧快照**（如 `source/clash-meta-2.yaml` 在快照里叫 `clash-meta.yaml`）→
  某仓库文件全部下载失败时，用 `list_repo_files(..., force_api=True)` 重新核对 HEAD 再重试一次

## 5b. 采到 0 条却把已有结果覆盖成空

- **症状**：昨天/上午还有几千条，跑一次之后 `v2ray_sub.txt` 变成空文件
- **修复**：`main()` 里若 `uniq` 为空且目标目录已有非空订阅，**不写任何输出**，
  以退出码 `3` 结束并在采集日志里记「本次 0 条，已保留原有输出未覆盖」
- **配套**：定时任务看到退出码 3 时不要重试刷屏，先查配额/网络

## 6. 镜像前缀失效

- **症状**：`health_check` 报「镜像失效：https://...」
- **处理**：替换脚本顶部 `DEFAULT_MIRROR_PREFIXES`，候选：`gh-proxy.com`、`ghfast.top`、
  `ghproxy.net`、`hub.gitmirror.com`、`gh.llkk.cc`、`gitdl.cn`
- **必须验证**：改完后用 `health_check.py` 重跑镜像探测，确认至少有 1 个可用

## 6b. 镜像候选池成批烂掉，只剩 1 个可用（2026-10-24）

- **症状**：`health_check` 报「镜像失效 10/11」，只剩 `gh-proxy.com` 一个能通
- **根因（实测）**：不是脚本问题，是**这批公共代理域名在本机出口网络上大面积失效**，
  且失效形态以 **DNS 解析失败**为主（`getaddrinfo failed`），其次是 TCP 被重置/超时。
  同一批域名在别的网络可能仍然可用，所以 `DEFAULT_MIRROR_PREFIXES` 必须当**候选池**看，
  不能当可信清单
- **取证方法（不要凭感觉换域名）**：对候选逐个拉固定小文件
  `https://raw.githubusercontent.com/octocat/Hello-World/master/README`，
  判定条件 = `status 200` **且正文含 `Hello World`**（只判 200 不够：`ghproxy.cn`
  返回 200 但内容是落地页 HTML 400 字节，不是代理）；再拿**真实节点文件**复核内容完整性
  （本次用 `mahdibland/V2RayAggregator/Eternity.txt`，三个可用镜像均 33352 字节 / 199 条 URI，完全一致）
- **2026-10-24 批量探测结论**（54 个候选，可用 3 个）：
  - 可用：`gh-proxy.com`（原有）、`gh-proxy.org`（新增）、`gh.monlor.com`（新增）
  - DNS 解析失败：`ghp.ci`、`gitdl.cn`、`hub.gitmirror.com`、`raw.gitmirror.com`、
    `ghproxy.cfd`、`gitproxy.click`、`proxy.yaohud.cn`、`ghfile.geekbang.org` 等
  - 解析成功但连接被重置/超时：`ghfast.top`、`ghproxy.net`、`gh-proxy.net`、`gh.llkk.cc`、
    `ghproxy.cc`、`ghps.cc`、`github.moeyy.xyz`、`mirror.ghproxy.com`、`gh.nxnow.top`、`gh.yylh.xyz`
  - 返回 200 但不是代理（落地页/错误页）：`ghproxy.cn`、`gh.h233.eu.org`（403）、`gh-proxy.moyu.im`（436）
- **修复**：
  1. 把实测可用的 `gh-proxy.org`、`gh.monlor.com` 加进 `DEFAULT_MIRROR_PREFIXES`（1 → 3 个可用）
  2. 新增 `MIRROR_SPARE_CANDIDATES`：只在主清单**存活 <2 个**时补测，救回的节点并入 `alive` 并持久化；
     `get_mirror_prefixes()` 的白名单同时放行主清单与备用候选（只放行 `base` 会把救回的过滤掉）
  3. 备用池只收「域名能解析、当前被墙/限流」的站点——已确认 DNS 不存在的域名补测纯属浪费 12s 超时
- **注意**：备用池本次**实际救回 0 个**（备用域名当前也全死），机制有效性是用可控样本验证的：
  把主清单临时设为 `ghfast.top`（死）、备用设为 `gh-proxy.org`（活），日志出现
  「已从备用候选救回 1 个」且 `get_mirror_prefixes()` 返回该节点。**不要把「备用池存在」
  当成「备用池有货」**，存活数仍以每次探活结果为准
- **残留**：`health_check` 的「镜像失效 N/M」告警在公共代理大面积失效时无法消除，
  这是环境事实而非脚本缺陷；只要 `alive ≥2` 有冗余就不影响采集


## 7. 三种输出格式节点数不一致

- **症状**：`URI 98 / clash 86 / singbox 86`，差距 >15%
- **根因**：`uri_to_clash` / `uri_to_singbox` 不支持某些新协议参数，转换时被丢弃
- **处理**：拿丢失的 URI 样本逐字段对照（security/type/path/host/flow/pbk/sid/fp 等），补转换逻辑

## 8. 采集耗时异常（>45 分钟）

- **根因**：多为镜像/CDN 慢速传输或反复超时重试
- **处理**：确认大文件是否走 CDN；必要时降低每仓库候选文件数、跳过超大文件

## 9. README 里明明有订阅链接，却没采到（或少采）

- **症状**：`health_check` 报「扫描 N 个仓库，没有任何 README 被识别出订阅链接」，或 README 提取节点数为 0
- **根因**（按出现频率）：
  1. 链接是 `clash://install-config?url=<编码后的订阅地址>` 一键导入式 → 裸 URL 正则抓不到，必须先解 `?url=`
  2. 链接是 `github.com/x/y/blob/main/a.txt` → 直接下载得到 HTML，必须换写成 `raw.githubusercontent.com/...`
  3. 同一文件在 README 里写了 4 个 CDN 域名（cdn/fastly/testingcf/gcore.jsdelivr.net）→ 不归一会重复下载、浪费链接配额
  4. 分类过宽：`?repos=xxx/NoMoreWalls`、`peasoft.github.io/NWalls.html`、`jsdelivr.com/package/...`、`/forks` 被当成订阅链接
- **修复**（`collect_nodes.py`）：
  - `IMPORT_LINK_RE` 单独抓一键导入链接，`classify_readme_link()` 里用 `_q()` 取 `url` 参数
  - `_repo_path_from_url()` 统一识别 raw / github blob+raw / jsDelivr `/gh/<owner>/<repo>@<ref>/<path>`，跨仓库自动换 raw 地址
  - `extract_readme_links()` 用「仓库+路径」做身份归一去重，保留 README 中的原始顺序
  - 扩展名必须命中 `CANDIDATE_EXT`；无扩展名的订阅接口必须命中 `SUB_URL_STRONG_HINT`（sub/clash/v2ray/sing-box/node）
  - 过滤 `example/template/sample` 示例配置与 `BAD_LINK_RE` 里的一堆网页形态
- **验证窍门**：`python -c` 调 `extract_readme_links(text, repo)` 打印命中列表，再跑 `collect_from_readme()` 看节点数

## 9b. 延迟排序没生效 / 订阅头部全是死节点

- **症状**：`v2ray_sub.txt` 前几十条连不上；`health_check` 报「前 50 条里有 N 条不可达」
- **根因**：
  1. `probe_latencies()` 没跑（加了 `--no-latency-sort`，或 `--keep-nodes` 截断发生在排序之前）
  2. 排序写在了 `write_outputs()` 之后（顺序必须：去重 → 探测 → 排序 → 写文件）
- **修复**：`main()` 中严格按 `dedupe → probe_latencies → uniq.sort(key=(latency is None, latency)) → write_outputs`
- **注意**：`tcp_latency = None` 表示不可达，排序键必须把 None 放最后（`x.get("tcp_latency") is None` 作首要键）

## 9c. 仓库质量分一直不出现 / 一直是 0

- **症状**：`seed_repos.json` 里没有 `quality` 字段，或所有仓库都是 0 分
- **根因**：质量分靠「节点 → 来源仓库」的映射，映射断了两头都算不出账
  1. `nodes_meta.json` 缺 `repo` 字段（采集时没走 `extract_text_into()` 打标记）
  2. `test_nodes.py` 没传 `--seed-file`，回写到了别的目录
- **修复**：采集端 `extract_text_into()` 给新记录 `setdefault("repo", repo_full)`；
  验证端 `c.update_repo_quality(seed_file, repo_stats, date_str)` 按仓库累计 tested/ok/延迟
- **注意**：`is_known_bad_repo()` 只跳过「实测 ≥20 且可用 0 个」的仓库，样本太少不跳，避免误杀新仓库

## 9d. 节点池不增长 / 池里节点越来越少

- **症状**：`pool_<core>.json` 的 nodes 数量连续下降，或池文件根本不存在
- **根因**：
  1. `--no-pool` 被加上了
  2. `prune()` 的 `last_ok` 比 `--pool-days` 更早被清掉（日期格式必须是 `YYYY-MM-DD`，`date_str` 要前后一致）
  3. `--pool-retest 0` 导致池内节点从不复测，很快就全部过期
- **修复**：保持 `--pool-retest` ≥ 30；`date_str` 统一用东八区当天；池上限 `--pool-max` 别设太小（免费节点通过率低，2000-3000 合理）

---

## 9e. 延迟排序后实测可用率反而暴跌（0-3/200）

- **症状**：加了延迟排序/延迟优先取样后，四个内核可用数从十几个掉到个位数甚至 0
- **根因**：**Cloudflare 任播入口的 TCP 握手延迟极低（10-40ms），但代理根本不通**。
  免费节点里 CF 前置（104.16.0.0/13、172.64.0.0/13、162.158.0.0/15 等）占比很高，
  纯按 TCP 延迟排序/取样会让它们霸占头部，测的全是死节点
- **实测**（2026-10-24）：11755 条里 707 条 <60ms，其中 90% 是 CF；
  按延迟取前 200 测，xray 0/200、v2ray 1/200、mihomo 2/200、singbox 3/200
- **修复**：
  - `collect_nodes.is_cf_fronted()` + `CF_NET_CIDRS`：离线判定 CF 网段（含 IPv6）
  - 排序键改成 `(不可达, 是CF, 延迟)`：真实节点 → CF 前置 → 不可达
  - `test_nodes` 取样时桶内同样 `(是CF, 延迟)` 排序，CF 只做补位
  - `nodes_meta.json` 增加 `cf` 字段与 `cf_fronted` 统计，自检会提示 CF 占比
- **注意**：CF 前置节点不是全死（回源正常时能用），所以**降权而非丢弃**；不要直接过滤掉

## 9f. 仓库明明有节点文件，却判「无可候选文件」

- **症状**：采集日志里一批仓库写着「无可候选文件」，但打开仓库首页就能看到订阅文件
- **根因**（2026-10-24 复盘 11 个漏采仓库，四类全中）：
  1. **无扩展名订阅文件**：`ts-sf/fly` 的 `clash` 和 `v2`、各种 proxypool 的 `configs`——
     文件名本身就是格式声明，靠 `CANDIDATE_EXT` 筛会整仓漏掉
  2. **无扩展名文件按纯文本解析**：`clash` 是 YAML（200 条），当文本解析得 0 条
  3. **中文 / 内核名目录**：`IvanSolis1989/Smart-Config-Kit` 的 `Xray内核系`、`Sing-box内核系`，
     英文锚定正则匹配不到
  4. **子目录只认一层**：`ovmvo/FreeSub` 的订阅在 `sub/raw/01.yaml`（两层），一层过滤直接漏掉
  5. **`github_api` 不转义路径**：中文目录名触发 `UnicodeEncodeError`，被上层当成"没有文件"静默跳过
- **修复**（`collect_nodes.py`）：
  - `BARE_SUB_NAMES` 白名单收无扩展名裸文件（要求体积 ≥4KB，避免误收脚本/标记文件）
  - `sniff_ext()` 按内容嗅探格式：先认 `proxies:`（YAML），再认 `outbounds`/`{`/`[`（JSON），否则按纯 URI 文本
  - `SUBDIR_HINTS_LOOSE` + `is_subdir_hint()`：中文与内核名按"包含"匹配
  - `pick_candidate_files()` 子目录允许任意深度；文件树来自 contents API 且只有 `dir` 条目时，
    才额外付配额进目录扫（仅限命中提示词的目录）
  - `_quote_api_path()`：`github_api` 统一转义非 ASCII，查询串原样保留
    （注意：`fetch_repo_file_text` 的 contents 回退要传**未转义** path，传已 quote 的会二次编码）
  - `SKIP_FILE_PATTERNS` 补 `white|black|cidr|ip-list|allowlist|bypass`——
    否则 `whitelist-all.txt`、`cidrwhitelist.txt` 会被当节点文件抓下来
- **验证窍门**：
  ```bash
  python -c "import collect_nodes as c; print(c.pick_candidate_files('ts-sf/fly', None))"
  python -c "import collect_nodes as c; print(c.sniff_ext(open('clash').read()))"
  ```
- **不打算修的部分**：订阅藏在两层以上目录（`Mihomo内核系/OpenClash/xxx.yaml`）的仓库，
  递归扫描要烧大量 GitHub 配额（匿名 60/h），交给 README 链接通道解决；README 也没链接的直接放弃

## 9g. 镜像探活「可用 1 个」但采集仍奇慢

- **症状**：`镜像探活：可用 1/6` 之后，每个下载失败的文件都要等几十秒
- **根因**：`get_mirror_prefixes()` 返回「活的 + 死的」，死镜像排在后面照样被逐个尝试，
  5 个死镜像 × 20s 超时 ≈ 100s/文件
- **修复**：探活过就**只返回活的**（全死则返回空，退回 raw 直连 + jsDelivr）；
  未探活过才返回全量候选池
- **配套**：
  - `_repo_path_from_url()` 归一化链接时必须用 `_base_mirrors()`（全量候选），
    用可用清单会让失效镜像的链接认不出来 → 同一文件重复下载
  - raw 直连也纳入探活（`raw_alive()`），已知不通时排到最后，省掉每文件一次 TLS 失败
  - 公共镜像存活率随出口网络剧烈变化（同批域名实测 1/11 ~ 7/11），
    所以 `DEFAULT_MIRROR_PREFIXES` 是**候选池**而非可信清单

## 9h. 大文件回退链整体失效（jsDelivr 通道写死单域名）

- **症状**：>2MB 文件几乎全部下载失败或被截断
- **根因**：`fetch_repo_file_text()` 的 CDN 主通道写死 `cdn.jsdelivr.net`，
  该域名在部分网络被 DNS/SNI 阻断，而同一套内容的边缘节点仍然可用
- **实测**（2026-10-24 本机）：`cdn.jsdelivr.net` SSL EOF 失败，
  `fastly.` / `gcore.` / `testingcf.` 三个节点均 200
- **修复**：`JSDELIVR_HOSTS` 四节点全部探活，`get_cdn_hosts()` 只返回可用的；
  下载按「节点 × (main, master)」分组尝试，避免在死节点上把两个分支都等一遍
- **注意**：jsDelivr 有缓存，刚 push 的文件可能取到旧快照；
  下载全失败时用 `list_repo_files(force_api=True)` 重新核对文件名

## 10. 验证节点时被节点「劫持重定向」，访问了陌生第三方域名

- **症状**：运行采集/验证时，宿主系统弹出「是否允许访问 http://某陌生域名」的确认框；
  但在订阅产物、节点清单、仓库 README、脚本代码里**全都搜不到这个域名**
- **根因**：`test_nodes.py` 的 `http_via_proxy()` 用默认 `build_opener()`，
  它会**自动跟随 302/301**。验证时是拿节点的本地代理端口去请求
  `http://www.gstatic.com/generate_204`（明文 HTTP），
  节点若把这个请求重定向到任意站点，urllib 就替它访问了那个站点
- **为什么产物里查不到**：被访问的是**重定向目标**，不是节点本身。
  该域名永远不会出现在 `nodes_meta.json` / 节点池里——这是最容易让人误判为
  「不是我访问的」的陷阱
- **危害**：① 节点可把探测流量导流到任意站点（广告/统计/钓鱼），
  等于我们把本机 IP 暴露给第三方；② 明文 HTTP 跳转必然触发宿主的网络拦截弹窗，
  打断自动化流程
- **修复**：`_NoRedirect` 禁止跟随，3xx 直接判为不可用；判定从 `200<=code<400`
  收紧为 `200<=code<300`（`generate_204` 正常应返回 204，出现重定向本身即不可信）
- **验证手法**：本地起一个返回 302 的 server，确认 opener 抛 `HTTPError 302`
  且目标 server 只收到 1 次请求
- **排查这类「不明访问」的固定路径**（本次实战总结）：
  1. `~/.workbuddy/audit-log/<date>.jsonl` 搜域名 → 得到 `eventType: network.ask-matched/approved` 与 `toolCallId`
  2. `~/.workbuddy/logs/sandbox/<date>/*.log` 搜域名 → 得到 `decide_network`（host/port/scheme/reason）
     与 `拦截 HTTP: host:port`
  3. 据 `scheme=http` + `port=80` 判断是**明文 HTTP**（而非 TCP 探测，后者不走 HTTP 层）
  4. 据时间点对齐当刻在跑的任务；据 `ProcessExit.decisionRecords` 判断进程身份
- **注意**：`helpers`/日志会同时记录你自己排查命令里的关键词，统计命中时要排除这类自污染

## 11. 探测地址用 `www.gstatic.com` 导致「不出境也能通过」

- **症状**：验证出来的"可用节点"实际连不上境外网站；也可能表现为可用率虚高，
  但用户拿去用时大量节点打不开网页
- **根因**：默认探测地址曾是 `http://www.gstatic.com/generate_204`，而
  `www.gstatic.com` 解析到 `120.253.253.34`（国内 Google 缓存节点），
  **本机直连就返回 204 / 111ms** —— 这个地址根本没有区分度：
  - 国内中转节点：解析到国内缓存，直连即通 → 误判为"能翻墙"
  - 配了分流域名规则的节点：同样命中缓存 → 误判
  - 只支持 HTTP 转发、TLS 一塌糊涂的劣质节点：明文 204 通过 → 误判
- **对照实测**（同一批 6 个可用节点 × 4 种地址组合，均禁止跟随重定向）：

  | 地址 | 通过数 | 说明 |
  |---|---|---|
  | `http://www.gstatic.com/...` | 6/6 | 无区分度 |
  | `https://www.gstatic.com/...` | 6/6 | 仍无区分度（国内缓存同样支持 TLS）|
  | `http://gstatic.com/...` | 6/6 | 有区分度但仍走明文 |
  | `https://gstatic.com/...`（裸域 HTTPS）| **4/6** | 正确 |

  被淘汰的两个节点，`www+http` 都是 204，但 HTTPS 表现分别是「连接被重置」和
  「TLS 握手超时」——现代网页全走 HTTPS，这两个节点实际不可用，属于**假可用**
- **修复**：默认改为 `https://gstatic.com/generate_204`。三要素缺一不可：
  **裸域**（`gstatic.com` 只解析到海外 `142.250.196.195`，本机直连 10s 超时）+
  **HTTPS** + **走代理**
- **配套调整**：裸域要真出境，实测耗时 0.9～16.7s，原来的 `--test-timeout 8s`
  会误杀大量真实可用节点 → 默认提到 12s；并发 8 → 12 抵消变慢（总时长基本不变）
- **注意**：换探测地址时不要用 `www.` 前缀的 Google 域名，也不要用国内可达的
  `connectivitycheck.*` 系列（同样有国内节点）。判断标准很简单：
  **本机直连它必须失败**，否则测不出出境能力
- **顺带**：裸域 HTTPS 不会返回 3xx（实测 4/6 直接 204），所以 `_NoRedirect`
  不会误杀；但它仍需保留，因为节点可以把 HTTPS 请求 302 到 `http://` 站点

## 12. github.com 被重置，但 api.github.com 可直连

- **症状**：`git push` 报 `Failed to connect to github.com:443` / `Recv failure: Connection was reset`；
  但 `curl https://api.github.com/rate_limit` 返回 200，`codeload.github.com` 也能下载。
  采集靠 API + 镜像还能跑，推送完全不通
- **根因**：网络层对 `github.com` 这个域名（SNI）做了阻断，同一批 GitHub 域名里
  `api.` / `codeload.` 没被拦。换 IP、加重试都没用，因为不是 DNS 也不是限流
- **修复**：`scripts/uplink.py` —— 用**已实测可用的节点**起一个本地代理内核，让 GitHub 流量走它：
  - 候选顺序：`pool/pool_<core>.json`（ok_count 高、延迟低优先）→ 近 3 天
    `tested/<core>/available_<core>_list.txt` → 近 3 天 `v2ray_sub.txt`
  - 节点 × 内核（mihomo → singbox → xray → v2ray）逐条试，TCP 预筛掉不可达的，省起核开销
  - 探测地址 `https://github.com/`（**只有 2xx 才算通**；`api.github.com` 通了不代表能 push，
    两个地址要分开判）
  - 全失败才直连；直连也不通就等 `--uplink-wait`（默认 600s）重试
  - **代理必须在节点验证前停掉**：验证要独占端口，而且要测的是节点本身
- **推送侧**：`publish_free_nodes.py --proxy auto` 复用它，且「推不通就换节点、换内核，
  直到连通」（`--uplink-rounds`），全失败才回退直连重试
- **坑**：`urllib` 的默认 opener 在首次使用后缓存代理设置，光改环境变量可能不生效 ——
  脚本同时 `set_proxy_env()` + `install_opener()`，两条路都覆盖

## 13. README-only 模式的取舍

- **现象**：目录扫描（按文件名猜 `sub/node/clash` 等）在大量仓库上白耗配额：
  README 没有订阅链接的仓库里，根目录那堆 `*.txt` 多数是分流表/日志/白名单
- **决定**：`--readme-only` 只跟随 README 声明的订阅链接，README 无链接的仓库直接跳过
- **代价**：来源数量变少（很多仓库的真订阅文件就在根目录、但 README 没写），
  节点数可能不达 `--target-nodes`；自检的「仓库效率」会单独统计
  `README 无订阅链接跳过` 的数量（kind=`nolink`），且**不计入产出率分母**
- **何时恢复目录扫描**：节点数长期不足、或自检报「README 无订阅链接」占比 >60% 且
  池内节点在萎缩时，去掉 `--readme-only` 再跑

## 14. 每个内核可用数只有个位数（固定取样不够用）

- **现象**：`tested/summary.md` 里四个内核经常只有 3~8 个可用节点，池内也不涨
- **根因**：验证阶段原来固定按 `--limit`（默认 200）取样，测完就收工。免费节点单节点
  可用率本来就低（裸域 HTTPS 探测下常见 3%~10%），200 个样本期望就只有 6~20 个可用；
  碰上当天源质量差就直接跌到个位数。**候选池里还有大量没测过的节点，白白浪费**
- **改法**：`test_nodes.py` 加自适应扩量（`--min-available`，默认 10）
  - 取样顺序改为「先按协议轮流交错排出**全量**测试顺序」，初始取前 `--limit` 条
  - 某内核可用数 < `--min-available` 时，顺着同一顺序继续追加下一轮（每轮 `--limit` 条），
    不重复、不跳档，协议多样性也保持
  - 停止条件：达标 / 候选耗尽 / 触到 `--limit-cap`（默认 `limit*5`）/ 时间预算
    `--escalate-budget`（默认 1800s/内核）
  - `summary.md` / `summary.json` 增加扩量轮次、`cand`、`exhausted`，便于判断
    「是没测完」还是「候选全测完仍不足」
- **注意**：`exhausted=true` 且可用数仍 <10 时，**不要再加大测试量**（已经测完了），
  问题在源池质量，要扩大采集来源；健康检查对该情形降级为 info，只对「还没测完就停了」报 warn
- **不要**为了让数字好看放宽探测地址（见第 11 条）
- **回归测试注意**：单内核小样本跑 `test_nodes.py` 会把该内核的实测结果**覆盖**写进
  当天的 `seed_repos.json`（仓库质量分被拉偏），回归时请加 `--no-pool --seed-file <临时路径>`，
  或跑完 `git checkout -- free-nodes/seed_repos.json` 还原

## 15. 产物文件膨胀：池 3 件套 + 可用清单 4 件套（大半是冗余）

- **现象**：每内核产出 `pool_<core>.txt` + `pool_<core>_list.txt` + `pool_<core>.json` 三个池文件；
  验证后又产出 `available_<core>.txt` + `_list.txt` + `_clash.yaml` + `_singbox.json` 四个可用文件。
  用户直接问「这些各自什么用途？后两个应该没必要吧」
- **根因**：历史演进时每加一个消费方便新增一份派生文件，没人回收：
  - `_list.txt` = base64 订阅解码后的等价值，**纯冗余**
  - `available_<core>_clash.yaml` / `_singbox.json` = 把某内核的可用清单再转成别的内核格式。
    这在能力矩阵上**根本不成立**：xray 支持 REALITY / VLESS flow，转成 clash 配置要么丢字段
    要么报错；反过来 clash 的 ssr/hysteria2/tuic 也转不进 v2ray。转出来的文件是"看起来能用"的陷阱
  - `pool_<core>.json` 与池文件里的节点列表**存了两份同一数据**，改一份另一份就脏
- **改法**（单文件制 + 扁平布局）：
  - 采集：`nodes_uris.txt`（全量明文主清单）派生 4 个订阅文件
    `v2ray_sub.txt` / `xray_sub.txt` / `clash_sub.yaml` / `singbox_sub.json`，一内核一文件，
    只写该客户端能直接导入的格式
  - 验证：`available_v2ray.txt` / `available_xray.txt` / `available_clash.yaml` / `available_singbox.json`
  - 池：4 个池文件（格式同上）+ **1 份共享** `pool_state.json`（只有元数据，不存节点列表副本）
  - 全部平铺在同一个根目录，**不再按日期建子目录**（过期节点没有意义，留历史目录只会误导）
  - md 日志（`report.md` / `summary.md` / `health_check.md` / `known_issue.md` / `changelog.md` /
    `collection_log.md` / `review_log.md`）统一**时间倒序**累积，同一天重跑替换当天小节，
    超出 30 小节从尾部丢弃（`layout.upsert_section`）
- **命名归一**：对外只用 `v2ray` / `xray` / `clash` / `singbox`；`mihomo`/`meta` → `clash`，
  `v2fly` → `v2ray`，`sing-box`/`sb` → `singbox`（`layout.canon()`）。否则会出现
  `pool_mihomo.txt` 和 `pool_clash.yaml` 两份内容一样、名字不同的池文件

## 16. 内核升级后「所有节点全死」——其实是配置模板过期

同一个症状（某内核 0 可用 / 全样本"未被接受"）背后有两个独立的版本坑，都踩过：

- **Xray 26.x 移除 `tlsSettings.allowInsecure`**
  - 现象：`xray -test -config` 返回码 23，报
    `The feature "allowInsecure" has been removed and migrated to "pinnedPeerCertSha256"(pcs) and "verifyPeerCertByName"(vcn)`
  - 后果：所有带 TLS 的样本配置校验失败 → 看起来"节点全死了"，实际是模板过期
  - 改法：`detect_core_features()` 启动时用带 `allowInsecure` 的样本跑一次校验，被拒就
    后续配置不再写该字段（日志打印「该版本已移除 allowInsecure，TLS 配置改为严格校验证书」）
- **v2fly 5.x 改了配置校验命令**
  - 现象：`v2ray -test -config` 报 `flag provided but not defined: -test`，返回非 0
  - 后果：每个样本都被判"未被接受"，能力指纹全 0
  - 改法：`CHECK_CMDS` 候选链（`v2ray test -c` / `xray -test -config` / `mihomo -t -f` /
    `sing-box check -c`），`check_config()` 逐个试、成功即缓存该内核的命令
- **REALITY `publicKey` 必须是合法 32 字节 base64url**（43 字符），随便填 `aGVsbG8` 会让
  clash/singbox 报 `initialize outbound[0]: invalid public_key`——能力指纹会误判成"不支持 reality"
- **防复发**：`check_kernels.py` 每次比对「本地版本 vs GitHub 最新 release」+「能力指纹
  accepted 集合 vs 基线」，变了就往 `changelog.md` / `known_issue.md` 记一条，
  提醒同步 `layout.CAPS` 与转换逻辑

## 17. 迁移脚本把自己的新文件删了（通配符与新命名撞车）

- **现象**：`migrate_layout.py` 日志明明打印 `[pool] v2ray: 5 条 → pool_v2ray.txt`，
  跑完 `ls pool/` 却只剩 `pool_clash.yaml` + `pool_state.json`
- **根因**：清理旧文件的通配是 `pool_*.json` + `pool_*.txt`，而**新**池文件名恰好是
  `pool_v2ray.txt` / `pool_xray.txt` / `pool_singbox.json`——先写后删，自己把成果删了。
  `pool_clash.yaml` 因为扩展名不在通配里才幸存
- **改法**：清理前先建 `keep = {pool_state.json, *POOL_FILE.values()}` 白名单，命中的跳过；
  另外显式清理旧内核别名文件（`pool_mihomo.txt` / `pool_mihomo_list.txt`）
- **教训**：**"旧命名清理"和"新命名写入"共用同一目录时，必须用白名单而不是黑名单通配**。
  这类 bug 不会报错，只会安静地丢文件——迁移脚本跑完必须 `ls` 复核实际落盘，
  不能只看自己的日志（日志是"我以为我写了"）

## 18. 自检「自己算错」的三个坑（0 条节点 / 多 1 个 / 404）

扁平化改造后第一次跑自检，报出 1 critical + 2 warn，其中两项是自检自身的 bug：

- **critical「本次采集到 0 条节点」，实际有 6632 条**
  - 根因：`read_sub_stats()` 无脑 `base64.b64decode()`——它原本只处理客户端订阅。
    扁平化后传进去的是**明文** `nodes_uris.txt`，解码出来是乱码、按 `://` 过滤后 0 行
  - 改法：`_lines_of_sub()` 先看明文里有没有 `://`，没有再走 base64 解码。
    同一函数现在同时吃「明文主清单」和「base64 订阅」
- **warn「singbox 文件条数 53 ≠ 汇总可用数 52」**
  - 根因：`available_singbox.json` 的 `outbounds` 里除了 52 个节点，还有一个内置
    `{"type":"direct","tag":"direct"}`，被当成节点计入
  - 改法：`read_core_file_count()` 统计 sing-box 时排除
    `direct` / `block` / `dns` / `selector` / `urltest` / `tor` 这类内置出站
- **v2ray 版本查询 404**
  - 根因：`check_kernels.REPOS` 里写的是 `v2fly/v2fly-core`，这个仓库调
    `/releases/latest` 返回 404。v2fly 的发版仓库是 **`v2fly/v2ray-core`**（tag `v5.53.0`）
  - 改法：改仓库名；`parse_version()` 本来就会剥掉 tag 的 `v` 前缀，比较逻辑不用动
- **教训**：自检工具本身也会被布局变更打穿，而且**症状看起来像"采集挂了"**。
  遇到「自检报 0 条但产物文件明显有内容」，先怀疑统计函数读错格式，别急着重跑采集

## 19. 仓库质量分倒挂：全死的仓库反而拿 30 分

用户问「仓库地址的池维护规则」时翻 `seed_repos.json`，发现评分排序明显不合理：

| 仓库 | 可用率 | 均延迟 | 旧质量分 |
|---|---|---|---|
| `MatinGhanbari/v2ray-configs` | **0.0%**（164 测全死） | 无 | **30.0** |
| `Firmfox/Proxify` 等 5 个 | 0.0% | 无 | **30.0** |
| `0xRadikal/Free-v2ray-Configs` | **11.4%**（48/420 可用） | 1499ms | **8.0** |
| `snakem982/proxypool` | 61.9% | 1586ms | 43.3 |

一个节点都没通过的仓库，分数比真有 11% 可用率的仓库高 4 倍。

**两个叠加的根因**（`quality_score()`）：

1. **缺数据被当成满分**：`lat = 100.0 if not avg_latency else ...`
   —— `avg_latency` 为 `None` 是因为「没有任何节点通过 → 没有延迟样本」，
   这是**最差**的情况，却被赋予延迟项满分 30 分。应该记 0
2. **归零点太苛刻**：原文 `100 - latency/15` 意味着 1500ms 就归零。
   免费节点实测延迟普遍 1500~7000ms（实测库里 6 个有延迟的仓库有 4 个 ≥1500ms），
   延迟项对绝大多数仓库**恒为 0**，这 30 分权重等于废掉，可用率就成了唯一变量

**改法**：可用率 ≤0 或延迟缺失时直接 `return rate*70`（延迟项 0）；归零点放到 5000ms
（`100 - latency/50`）。回填后：0% → 0.0，11.4%@1499ms → 29.0，61.9%@1586ms → 63.8，
排序恢复正常。

**为什么没影响采集**：`repo_sort_key()` 用的是 `avail_rate` 而不是 `quality`
（原注释就写了「总分含延迟权重，会把握手快但几乎全死的仓库抬到前面」）。
所以这个 Bug 只污染 `report.md` 的排行和 `seed_repos.json` 的展示，采集优先级一直是安全的。
**但反过来提醒**：谁要是哪天把排序键改成 `quality`，就会立刻踩上这个坑。

**教训**：打分公式里凡是出现「默认值 / 缺省值」，都要问一句
「这个默认值代表最好还是最差？」——`not x` 这种写法在 `x` 为 `0` 或 `None` 时
会走进同一个分支，而这两个值的语义常常相反。

## 20. md 日志「同一天重跑替换」——对事件日志是错的

`upsert_section()` 原本按**日期前缀**删除旧小节（`t[0].startswith(f"## {date}")`），
这是为日报类文件（`report.md` / `summary.md` / `health_check.md`）设计的：
「当天重跑就该替换当天那份结论」。

但 `changelog.md` / `known_issue.md` 是**事件日志**——一天可以有好几条互不相干的记录。
本次往 changelog 补写「修复仓库质量分倒挂」时，把当天先写入的
「布局重构与内核检查」整节（58 行、6 个子节）**整段抹掉**了，只能用
`git checkout HEAD -- free-nodes/changelog.md` 恢复。

**改法**：`upsert_section(..., match_heading=True)` 只替换「同一天 + 同一标题」的小节；
`append_changelog()` / `append_issue()` 固定传 True，日报类保持默认 False。

**连带发现**：`health_check.py` 和 `check_kernels.py` 用 `now.strftime("%H:%M")` 当标题。
对按日期去重的日报无害（当天最后一个小节会替换前一个），但配合 `match_heading=True`
就变成「每跑一次新增一节」，一次排查跑三遍就堆三节。已全部改成固定标题
（`自检发现` / `自检摘要` / `内核检查与升级` / `内核检查发现`）。

**验证方法**：同一个命令连跑两次，`grep "^## " 文件` 的小节数必须不变。

**教训**：凡是「upsert（有则改、无则加）」逻辑，**去重键必须和业务语义一致**。
日报的去重键是「日期」，事件日志的去重键是「日期 + 事件标题」——用错键不会报错，
只会在某天悄悄吞掉数据，而且吞掉的往往是当天最有价值的那条。

## 21. README 按内核 / 按日期筛选的边界

用户要求「README 里一般会给出不同代理的订阅链接，直接按内核收集；有的还会分日期提供，就只取当天」。
实现见 `extract_readme_links()` / `classify_readme_link()`，几个必须守住的边界：

**内核识别（`KERNEL_LINK_HINTS`）**
- 判定顺序：文件名 → 目录名 → 链接文字 → 域名。最贴近内容的优先，
  因为 `.../clash/v2ray_sub.txt` 这种混合路径要以文件名为准
- `singbox` 必须排在 `clash` 之前判：`sing-box-clash` 这类命名会被 clash 的宽泛规则抢走
- 认不出就记 `None`（通用订阅），**不要瞎猜**——猜错会让节点被归到不支持它的内核
- 内核标记的作用是**豁免 `layout.CAPS` 预筛**，不是「只准进这个内核」。
  作者声明「这是 clash 订阅」，那这些节点一定能进 clash 文件，不该被 CAPS 判死；
  但它们同样可能被 v2ray/xray 支持，所以照常参与那些内核的分流，不能独占

**日期筛选**
- 两种写法都要认：① 链接自带（`.../2026-10-25/all.txt`、`Nodes-20261025.txt`）；
  ② 日期小标题给上下文（`### 2026-10-25` 下面列的链接自己没日期）
- 上下文只回溯 4000 字符且取「最近的带日期标题」：README 里 `## 2026-10-24 … ## 2026-10-25`
  两节时，10-25 节下的链接会正确归到 10-25，不会继承上面的 10-24
- **只认 4 位年份的完整日期**。`1025` / `10-25` 这类缩写一律不认——免费节点仓库里
  `1025` 出现在端口、UUID 片段、随机文件名里的概率太高，误杀成本远大于收益
- **整份 README 一个日期都没提 → 全部保留**。否则所有非日更仓库（占多数）会被一刀砍死
- 严格当天（`tolerance=0`）会让「凌晨跑、仓库当天还没更新」的日更仓库全军覆没。
  这属于运行时策略而不是代码 bug：用 `--readme-date-tolerance 1` 放宽，**不要改判定逻辑**

**日志必须区分三种 0 产出**（`phase_log` 的 kind）
- `-3` README 未声明订阅链接（没链接）
- `-4` README 有链接但日期不是当天（有链接，被策略跳过）
- `-1` / `0` 链接下载失败 / 下载了但解析不到节点

这里有个容易踩的空值陷阱：`if links and ...` 在 `links == 0` 时会直接落到
「未声明订阅链接」分支——而 `links == 0` 恰恰可能是「日期全被筛掉」造成的。
所以判断顺序必须**先查 `lstats["date_skipped"]`，再查 `links`**，否则日志会把
「按策略跳过」误报成「仓库没写链接」，进而误导下次去调采集逻辑。

**顺带补掉的老缺口：sing-box 来源不反解 URI**

`record_uri()` 里对 `kind=="singbox"` 一直返回空串（旧注释「sing-box 来源暂不反解」）。
在 README 按内核识别之前，这个缺口影响有限；识别之后 `kernel=singbox` 的链接变多，
后果就明显了：

- sing-box JSON 订阅里的节点**进不了 `nodes_uris.txt` 主清单**
- 主清单是 `test_nodes.py` 的取样来源 → 这些节点**根本不参与四内核可用性验证**
- 于是它们未经测试就写进 `available_singbox.json`，也进不了跨天池

补 `singbox_to_uri()` 覆盖 ss / trojan / vless / vmess / hysteria2 / tuic 六种，
其余类型返回 None。验证方式：
1. **往返一致性**：sing-box → URI → `uri_to_singbox()`，server/port 必须一致（6/6 通过）
2. **内核原生校验**：反解出的 URI 交给四个内核各自的配置校验命令，
   vless(reality/ws) 与 vmess 四内核全接受；hysteria2 只有 clash/singbox 能构造配置
   （v2ray/xray 的 `build_config` 返回 None，符合能力边界）
3. **端到端**：解析含 `{"type":"direct"}` 的 sing-box JSON → `write_outputs` →
   `nodes_uris.txt` 里有该节点，且四个 sub 文件都有它

注意 sing-box 里的 `direct`/`block`/`dns` 不是节点，解析阶段已经排除（同第 18 条第二个坑）。

**已知误判风险**（可接受，未修）
- URL 路径里出现 `2026xxxx` 形式的构建号会被当日期。若某仓库因此被整仓跳过，
  日志里会显示 `-4` 并带上「见到的日期」，能一眼看出来
- README 里若用 `10/25` 这种无年份写法，不会被识别为日期，链接按通用订阅保留（宁多不漏）

## 22. 传输层「静默退化」：不认识的 type 一律当 tcp（最大的一类假阴性）

**现象**：`type=xhttp / httpupgrade / kcp / quic / http / h2` 的节点，在对应内核上
全部「测不过」，可用率看起来正常，但用户反馈这些节点在客户端里其实是能用的。

**根因**：两个转换器都用了白名单 + 兜底：

```python
stream = {"network": net if net in ("tcp", "ws", "grpc", "http", "h2") else "tcp"}
```

vmess 的 `net`、`_ws_opts()` 只处理 `ws` / `grpc`，其余全部落回 `tcp`。
配置本身是「合法」的 —— 内核校验通过、进程能起、代理端口能监听，
所以它会一路走到「请求失败」，最后被记成**节点不可达**。
参数丢了 ≠ 节点死了，这是判定口径被污染最严重的一处。

**修复**：

1. 新增 `layout.canon_net()` 统一网络名（`h2`→`http`、`splithttp`→`xhttp`、`none`→`tcp`）。
2. 每个内核的传输能力写进 `layout.CAPS[core]["nets"]`，逐条来自内核实测：
   - v2ray 5.53：tcp/kcp/ws/http/quic/grpc（无 httpupgrade/xhttp）
   - xray 26.10：tcp/kcp/ws/grpc/httpupgrade/xhttp（HTTP、QUIC 传输已移除）
   - clash 1.19：tcp/ws/grpc/http/h2/xhttp
   - singbox 1.14：tcp/ws/grpc/http/httpupgrade/quic（无 xhttp）
3. 转换器改成**要么完整映射、要么返回 None**，禁止兜底成 tcp。
4. `protocol_check.py` 增加「参数保真」断言：生成出来的配置里 network/transport
   必须与 URI 声明一致，退化会直接报错。

**回归**：`protocol_check.py` 样本矩阵 29 组 × 4 内核全部一致；其中 `type=h2` 在
xray 上判为「不支持」（内核已移除该传输），而不是生成一份会失败的 tcp 配置。

## 23. Trojan 链接不写 security=tls，被当成明文 trojan

**现象**：形如 `trojan://pwd@host:443?sni=a.com#tag` 的节点（不带 `security=tls`）
在四个内核上都失败；带 `security=tls` 的同样节点却能用。

**根因**：`_stream_settings()` 只在 `security in ("tls","reality")` 时才补 TLS，
Trojan 协议本体必须跑在 TLS 上，链接里省略这个参数是常见写法。

**修复**：转换器里对 trojan 强制补 TLS（clash `tls: true`；v2ray/xray
`security: tls`；sing-box `tls.enabled: true`）。Xray 26 更进一步：
`trojan without TLS is prohibited unless the server address is a private IP`。

## 24. `tuic://uuid:password@host` 的口令被 URL 解析吃掉

**现象**：tuic 节点全部「配置生成失败」（旧日志里是「配置生成失败」直接跳过）。

**根因**：`urllib.parse.urlsplit("tuic://uuid:pwd@h:443")` 会把 `uuid` 放进 `.username`、
`pwd` 放进 `.password`。代码只取 `.username`，于是 `partition(":")` 拿不到分隔符，
`uuid` 有值、`password` 为空 → 转换器返回 None。

**修复**：三处转换器统一改成「有 `.password` 就拼回 `user:pass`」。

## 25. 「测不过」被一律记成不可用，配置错误和节点失效混在一起

**现象**：`summary.md` 只有一个「可用率」；某次内核升级后可用率骤降，无法判断是
节点变差了我们配错了。

**根因**：`test_one()` 把所有失败压成一句「请求失败」，内核 stderr 直接丢进 DEVNULL。

**修复**：

1. 失败后先跑内核 `check` 复核 —— 配置被拒记 `config`，不计入不可达。
2. 抓内核日志 + 客户端异常文本做归类（`tls / auth / refused / reset / timeout / config`）。
3. 网络类失败复测 1 次（`--retry`），两次都失败才定案。
4. `summary.md` 增加「不支持 / 配置错误 / 不可达」三列 + 「失败原因分布」表。

判定口径写进 `Docs/protocol.md` 第 4 节，包含每条原因的原文证据。
成片出现 `config` = 转换器有 Bug；成片 `unsupported` = 能力矩阵需要对齐内核；
只有 `tls / auth / refused / reset / timeout` 才是节点侧的证据。

## 26. v2ray 的 hysteria2 被误标为不支持（用户质疑后核实）

**现象**：protocol.md / SKILL.md / CAPS 都写「v2ray 不支持 hysteria2」，hysteria2
节点从不进 `v2ray_sub.txt`、测试阶段直接跳过。

**核实过程（2026-10-25）**：

1. 二进制检索：`v2ray.exe` 含 66 处 hysteria 字样（**此处对 xray 的结论是错的**，
>   当时用 `xray.exe | grep` 扫的是进程 stdout 而非二进制文件，漏检；xray 26.10.21
>   实际含 678 处 hysteria 字样，见第 27 条）
2. 配置校验：`protocol: "hysteria2"` 对 v2ray 5.53 通过且能启动；对 xray 26.10 被拒
3. 官方文档：v2fly 文档仓库 `docs/v5/config/proxy/hy2.md` + `stream/hy2.md` 白纸黑字
4. **端到端**：v2ray（hysteria2 代理层 + hysteria2 传输层 + `hy2Settings.password`）
   → sing-box hysteria2 服务端，HTTP 200 全通

**根因**：v2fly 的 hysteria2 装填方式特殊——代理层 `settings.servers` 只有
`address/port` 没有密码，密码在传输层 `hy2Settings.password`；且 v2fly 对未知
字段宽松（静默忽略不报错），早期只跑 config check 根本看不出问题，就当作不支持
写进了文档。另一个干扰源：v2rayN 等客户端宣传「支持 Hysteria2」指的是捆绑了
独立的 hysteria 官方内核，容易被误读成内核本体支持。

**修复**：

1. `layout.CAPS`：v2ray protocols 加 `hysteria2`
2. `test_nodes.uri_to_v2ray_outbound()`：hysteria2 分支按官方两层结构装填；
   带 `obfs` / `mport` 的节点判不支持（v2fly 静默忽略这些字段，违反「不静默降级」）
3. `protocol_check.py`：hysteria2 用例 v2ray 由 SKIP 改 OK；obfs / mport 保持 SKIP
4. 文档勘误（protocol.md §3.1 / §3.6 / §5）

**教训**：「config check 通过」≠「支持」≠「装填正确」。v2fly 不校验未知字段，
能力判定必须用端到端实测兜底；每个内核的协议支持清单应以其官方文档 + 实测为准，
不能凭社区直觉。（本条「Xray 系全都不支持 hysteria」的判断同样有误，已由第 27 条修正。）

---

## 27. Xray 的 hysteria2 也被误标为不支持（用户提示 v26.1.23 后核实）

**现象**：紧接第 26 条之后，protocol.md / SKILL.md / CAPS 仍写「xray 不支持
hysteria2」，hysteria2 节点从不进 `xray_sub.txt`、xray 测试阶段直接跳过。

**核实过程（2026-10-25，用户提供「Xray v26.1.23 引入 Hysteria2」线索后）**：

1. 二进制检索（**这次 grep 的是二进制文件本身**）：`xray.exe` 含 **678 处 hysteria**
   字样 + `HysteriaClientConfig` / `HysteriaServerConfig` / `HysteriaInboundValidator` /
   `salamander`(124) / `udphop`(66) / `obfs`——铁证
2. 官方源码（api.github.com 拉 `XTLS/Xray-core`）：`infra/conf/hysteria.go` 定义
   `HysteriaClientConfig`（version/address/port 平铺）；`proxy/hysteria/client.go`
   校验 `config.Server != nil`；`transport/internet/hysteria/dialer.go` 用
   `hysteriaSettings.auth` 发 `Hysteria-Auth` 头
3. 配置校验：`protocol: "hysteria"` + `settings.version:2` + `settings.address/port`
   （平铺）+ `streamSettings.network:"hysteria"` + `hysteriaSettings.version:2`
   → `xray run -test` 全过
4. 端到端：xray 客户端能拨号并完成到 xray hysteria2 服务端的 TLS 握手（日志见下）

**根因（双重误判）**：① 早先用 `xray.exe | grep hysteria` 扫的是**进程 stdout**
而非二进制文件，且当时以为没输出就是没有；② 不知道 Xray 把 Hysteria2 实现为
`protocol: "hysteria"` + `version: 2`（**协议名里没有 "2"**），按 `hysteria2` 去写
配置自然报 `unknown transport protocol: hysteria2` / `unknown config id`。

**修复**：

1. `layout.CAPS`：xray protocols 加 `hysteria2`
2. `test_nodes.uri_to_v2ray_outbound()`：新增 xray hysteria2 分支——
   `protocol:"hysteria"`、`settings:{version:2,address,port}`（平铺，**不是**
   `servers[]`/`server`，那两种会在拨号时 nil 指针 panic）、
   `streamSettings:{network:"hysteria", hysteriaSettings:{version:2,auth,up,down,
   [udphop]}, security:"tls", tlsSettings:{serverName,[verifyPeerCertByName]},
   [finalmask.udp=salamander]}`；insecure 节点用 `verifyPeerCertByName`（Xray 26
   已移除 `tlsSettings.allowInsecure`）
3. `protocol_check.py`：hysteria2 用例 xray 由 SKIP 改 OK
4. 文档勘误（protocol.md §3.1 / §3.6 / §5；本条修正第 26 条里关于 xray 的错误结论）

**遗留 / 边界**：

- 本机回环 E2E（xray 客户端 ↔ xray 服务端）卡在**服务端** TLS 报
  `CRYPTO_ERROR 0x170: tls: unrecognized name`——Go 服务端按 **DNS 名**匹配证书，
  测试证书 SAN 是 `IP:127.0.0.1,DNS:localhost`，客户端 SNI 无论填 `127.0.0.1` 还是
  `localhost` 服务端都不认（疑似 xray hysteria 服务端 SNI 选证书的怪癖）。这是
  **回环测试服务端**的问题，客户端配置本身正确（能拨号、能发起 TLS 握手）；对真实
  节点（证书匹配域名 + 正确 SNI）预期可用，但**尚未拿真实 hysteria2 节点端到端验证**
- 因此 xray 的 hysteria2 测试结论需与 v2ray/clash/singbox 交叉印证：若只有 xray
  失败而其他内核可用，优先怀疑 xray 侧配置/兼容，别急着判节点不可达

---

## 28. 输出根目录平铺 20+ 文件，找东西全靠猜（目录布局调整）

**现象**：`free-nodes/` 根目录长期平铺——4 个订阅 + 4 个可用清单 + `nodes_uris.txt` /
`nodes_meta.json` + `pool/` + 6 个报告类 md + 2 个 json + 3 个仓库状态文件 + `changelog.md`，
共 20+ 个条目混在一起。用户反馈「新建 nodes 目录存节点信息、Docs 目录存文档、src 目录存脚本」。

**处理（2026-10-25，当晚又按用户要求做了二次整合，见第 30 条）**：

1. 新布局：根目录只留 `README.md` + `CHANGELOGS.md`（changelog.md 更名）；
   `nodes/`（订阅 / available / nodes_uris / nodes_meta / pool/）；
   `Docs/`（protocol / proxy / known-issues / sources / tools-setup / report /
   summary±json / health_check±json / known_issues / collection_logs / review_logs）；
   `src/`（流水线脚本 + seed_repos / repo_quality / kernel_state）
2. `layout.py` 做**唯一事实来源**：所有脚本经 `lay.sub_path/avail_path/pool_path/
   uris_path/meta_path/report_path/summary_path/health_path/issue_path/seed_file_path`
   等助手取路径，改布局只改 layout.py 即全链路传播；硬编码 join 已全部清除
3. 仓库文件用 `git mv` 迁移（保历史）；`migrate_legacy_flat(root)` 提供幂等的一次性迁移

**教训**：路径常量散落在各脚本里，每加一个文件就要全局搜一遍 join。
收敛到 layout.py 的路径助手后，「调整目录结构」从改 N 个文件变成改一个文件。

---

## 29. 固定取样 200 个，晚上供给充足时白白浪费（全量测试策略）

**现象**：旧策略每内核单轮只测 `--limit`（200）个，可用数 <10 才逐级扩量。
夜里候选经常只有几百到两三千个，200 的取样既测不完也排不尽——
排序靠后的节点永远测不到，而它们的协议/仓库分布与头部并无本质差异。

**处理（2026-10-25，用户要求「未超过 3000 个就全测，超过只测 TCP 排序前 3000 个」；
注意上限最初笔误写成了 30000，当晚用户纠正为 3000）**：

1. `test_nodes.py` 新参数：`--full-below`（默认 3000）、`--max-test`（默认 3000）、
   `--no-full-test`（显式回退旧模式）
2. 取样逻辑：候选 ≤ `full_below` **全测**；超过则按既有排序
   （协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序）截取前 `max_test` 个
3. 扩量循环只在 `--no-full-test` 旧模式生效；全量模式单内核上限即 `--max-test`
4. `summary.json` 新增 `policy` 字段（`full` / `limited`），health_check 按策略
   给不同措辞（全量 + 候选测完 = info「已无优化空间」，不再误报「扩量未达标」）
5. `collect_nodes.py` 透传 `--test-full-below` / `--test-max-test` / `--test-no-full-test`

**教训**：「默认参数」要跟着真实供给调整：200 是早期供给紧张时代的遗产，
全量实测成本（每节点一次内核拨号 ≈ 6s，3000 个 ≈ 5 小时）在夜间空闲窗口可接受，
供给更多时就截断到上限——所以阈值本身要做成参数，而不是写死的策略。
另外用户随口报的数（「30000」）先落文档再实现时发现了笔误——**关键数字要在文档与
代码里逐处核对**，本次 30000→3000 的纠正涉及 layout.py 常量、三个脚本默认值、
SKILL/protocol/proxy/known-issues 五处文档与定时任务 prompt。

---

## 30. 技能目录 / 脚本 / 文档三处副本互相同步，改了总漏一边（目录整合）

**现象**：第 28 条布局调整后留下「同步」尾巴：技能在 `~/.workbuddy/skills/free-nodes-collector/`
（SKILL.md + references/ + scripts/），仓库里又有一份 `free-nodes/src/`（脚本同步副本）
与 `Docs/protocol.md` / `Docs/proxy.md`（文档副本）。每次改脚本要跑 `sync_src()` 拷贝、
改文档要记着两边同步——漏一次就两边漂移（本次就发现 `health_check.py` 的修复只在
技能侧、src 副本是旧的）。用户要求：「技能目录直接移到 freenodes/Skills 下，脚本直接用
src 目录的，references 文档直接用 Docs 目录的，不再进行不同目录间文件的同步」。

**处理（2026-10-25）**：

1. 技能迁入仓库：`~/.workbuddy/skills/free-nodes-collector/` → `free-nodes/Skills/free-nodes-collector/`
   （只留 SKILL.md；references/ 下的 known-issues / sources / tools-setup 全部并入 `Docs/`，
   protocol / proxy 的重复副本删除）
2. **`src/` 成为脚本唯一事实来源**：9 个流水线脚本 + `publish_free_nodes.py`
   （从 tools/ 迁入）直接住在仓库里，改脚本即改发布物；`sync_src()` 与
   `package_skill.py`（打包分发已无意义）一并删除
3. `publish_free_nodes.py` 相应改造：workspace 默认值改为「脚本上溯三级」
   （src → free-nodes → 仓库根），`--skill-scripts` 默认即自身所在目录
4. 文件名复数规范化：`known_issue.md`→`known_issues.md`、
   `collection_log.md`→`collection_logs.md`、`review_log.md`→`review_logs.md`
   （layout.py 路径助手单一修改 + git mv，全链路自动传播）
5. `Test/.workbuddy/memory/`（项目记忆）移入 `free-nodes/.workbuddy/memory/` 并纳入
   git 跟踪推送；`.gitignore` 的 `.workbuddy/` 改为根目录锚定 `/.workbuddy/`，
   仓库根的 junction 兼容宿主记忆系统的读取路径

**教训**：「同步两份」是假需求——真需求是「一份、可版本控制、可推送」。
技能住进仓库后，git 历史即分发链，`git clone` 即安装，同步动作归零。
代价是技能不再被 WorkBuddy 技能列表自动发现，定时任务与手工运行都改用
`free-nodes/src/` 绝对路径——对「脚本本来就走绝对路径」的自动化场景没有损失。

## 31. 定时任务 90 分钟超时，全量测试没跑完（夜间窗口不够）

**现象（2026-10-25 夜）**：22:00 的定时任务在 90 分钟窗口内失败
（`[CANCELLED] Run timed out`）。时间线：采集 43 分钟（22:01→22:44）→
任务发现旧技能目录被删、自行从 `src/`+`Docs/` 重建花了几分钟 → 补跑
`test_nodes.py` 全量测试 44 分钟被砍（23:30），健康检查与提交推送都没轮到，
当晚无发布。当晚 `nodes/available_*`、`Docs/summary.*` 停留在下午的旧产物。

**根因链**：① 晚间会话与定时任务并发改同一批文件（删旧技能目录、Docs 文件
复数改名），任务 22:45 起花时间自救；② 任务按旧 prompt 补跑测试时传了
`--limit 200`，但**全量模式下该参数被忽略**，实际按默认全量策略跑
（每内核候选 ≤3000 全测），44 分钟没跑完；③ 平台对单次自动化运行有
90 分钟硬上限，采集（30~45 分钟）+ 全量测试（50~70 分钟）+ 自检发布
（~7 分钟）本来就放不进一个窗口。

**处理**：
1. 当晚由主会话补跑：`src/test_nodes.py --full-below 3000 --max-test 3000`
   （**参数名坑**：`test_nodes.py` 用 `--full-below/--max-test`，
   `collect_nodes.py` 的透传参数才带 `--test-` 前缀；传错直接 exit 2）
2. 新版 prompt（`Docs/automation-prompt.md`）：采集不带内联测试 → 独立
   `test_nodes.py` 全量步 → 自检 → 发布；并写明时间预算与降级规则
   （时间紧就 `--max-test 1500` 减半，优先保证发布成功，别为多测而超时）
3. `~/.workbuddy/skills/free-nodes-collector/` 改为 junction 兼容层
   （scripts→src、references→Docs），旧 prompt 的路径持续有效、零同步

**教训**：
- 90 分钟是硬约束： nightly 流程要按「采集 → 测试 → 自检 → 发布」分步估时，
  测试量可降级，发布不能省（超时=整晚白干）
- 大改动（删目录、批量改名）尽量避开 22:00 任务窗口；万一撞上，任务当次
  可能失败，事后补跑即可，不要为此回滚已完成的重构
- 两套参数名（collect 透传带前缀 / test_nodes 不带）是长期易错点，
  prompt 与 SKILL.md 都要写全名并标注区别

## 32. 目录重构漏改函数名，写池崩溃害三个内核白等（已修复）

- **现象**：2026-10-25 夜间全量测试，v2ray 跑满 1000 个（可用 43、耗时 776s、`available_v2ray.txt`
  已落盘）后进程直接崩：`NameError: name 'pool_dir_of' is not defined`（`pool.py:201`）。
  后果是 **xray / clash / singbox 三个内核一个都没测**，且 `pool_state.json` 也没更新
- **根因**：目录布局重构（`pool/` 迁到 `nodes/pool/`）时，只把 `load_state()` 等处的
  路径改成了 `lay.pool_dir(root)`，**漏了 `save()` 里这一处** `os.makedirs(pool_dir_of(root))`。
  该函数名在重构前就不存在（应该是笔误残留），而它只在「每个内核测完写池」的分支被调用，
  **导入期和常规冒烟都碰不到**，所以直到 v2ray 跑完 13 分钟才炸
- **影响面判断**（重要）：`available_<core>.txt` 的写入在 `save()` **之前**，
  所以 v2ray 的 43 条结果没丢；丢的是池文件与共享状态 + 后续三个内核的全部测试
- **修复**：改为 `os.makedirs(lay.pool_dir(root), exist_ok=True)`；
  用 tempdir 调 `pool.save()` 冒烟，确认能写出 `nodes/pool/pool_v2ray.txt`
- **教训**：
  1. 「路径单一事实来源 = `layout.py`」这条约定只管住**新代码**，管不住历史函数名残留——
     改完必须全局 grep 旧标识符（`grep -rn "_dir_of\|_path_of" src/`），
     **「能导入」不等于「每条分支都能跑」**
  2. 崩溃发生在 per-core 循环内部：前面内核的成果已落盘、后面的跳过。补跑时要判断
     「已落盘的可用清单」与「池/状态」是否一致——不一致就整轮重跑，别只补跑缺失的内核，
     否则 available 与 pool 会长期对不上
  3. 长任务（单内核 10 分钟级）动手前先用小样本（`--max-test` 取几十）跑通**完整写盘链路**，
     别等真跑完才在最后一步炸

## 33. 池目录被拼成 nodes/nodes/pool（静默错位，比崩溃更危险）（已修复）

- **现象**：2026-10-26 补跑四核测试，日志一路正常（v2ray 32 / xray 37 / clash 43 / singbox 46、
  `[done] 可用节点池：…/nodes/pool`），退出码 0。但实际产物：
  - `nodes/available_*` 写在**正确位置**（`nodes/` 下）
  - 池文件却写到了 **`nodes/nodes/pool/`**（多一层），而 **`nodes/pool/` 仍是昨天 13:39 的旧数据**
- **根因**：`test_nodes.py:1067` 写成
  `pool_root = dirname(args.pool_dir or lay.pool_dir(root))`。
  旧平铺布局下 `pool_dir = <root>/pool`，`dirname` 得 `<root>` → 正确；
  三分层后 `lay.pool_dir()` 返回 `<root>/nodes/pool`，`dirname` 得 `<root>/nodes`，
  `pool.save()` 内部再拼一次 `nodes` → `<root>/nodes/nodes/pool`。
  `collect_nodes.py` 还会把 `lay.pool_dir(out_dir)` 透传给 `--pool-dir`，同样踩坑
- **为什么没人报错**：`os.makedirs` 会自己建目录，写入成功、返回值正常，
  日志照样打印「池内共 N 条」——**不崩、不红、退出码 0**，只能靠交叉核对发现
- **真实影响**（三条，都比"文件放错"本身更麻烦）：
  1. `pool_state.json` 停在昨天（节点数 27/43/56/54），`uplink` 自建代理读的是旧池
  2. 本轮池是**从空池起跑**的（加载的是新位置、尚不存在），历史累积节点没继承
  3. available 与 pool 长期对不上，越跑越偏
- **发现方式**：`find free-nodes -type f -newermt "2026-10-26 08:00"` 看今天到底改了哪些文件，
  再比对 `nodes/pool/pool_state.json` 的 `updated` 与 `cores` 节点数 ——
  **看时间戳和计数，比看日志可靠**
- **修复**：
  1. `pool_root` 语义回归「根」：不传 `--pool-dir` 时直接用 `root`，
     显式传池目录时才 `dirname`（接口语义不变，`collect_nodes` 透传链自然正确）
  2. 误写目录的数据**按 key 合并**回 `nodes/pool`（不是覆盖）：
     v2ray 27→48、xray 43→66、clash 56→85、singbox 54→84，历史节点一个没丢；
     随后删除 `nodes/nodes/`
- **教训**：
  1. **路径必须由 `layout` 一次性给全，调用方不许对助手返回值再 `dirname`/拼接**——
     「助手算路径 + 调用方二次加工」就是重构地雷，本条与第 32 条同源
  2. **静默错位比崩溃危险**：第 32 条崩在明处，13 分钟就暴露；本条一路绿灯，
     直到核对时间戳才发现。长任务收工后固定抽查：产物路径 + mtime + 关键计数
  3. 补救历史数据用**合并**（`pool.merge` 按 `host:port` 去重、累加 `ok_count`），
     不要图省事直接覆盖

## 34. 分步执行时「第 1 步建的代理」活不到第 2 步（环境限制，已绕开）

- **背景**：用户要求「内核检查那一步就自建代理保证连通，采集时直接用这条通道，不要重复搭建」。
  直觉做法是把通道信息落盘（`runtime/uplink_session.json`）、内核子进程 detached 启动，
  下一步读文件探活接管。
- **现象**：登记成功、pid 也拿到了，但**下一个进程一启动就发现 pid 已死**
  （`[uplink] 上次登记的通道进程已退出，准备重建`），复用 100% 失败
- **根因**（本机执行环境）：命令跑在一个 job object 里，结束时整个 job 关闭，
  `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` 会连带杀掉 detached 子进程；
  试图用 `CREATE_BREAKAWAY_FROM_JOB`(0x01000000) 脱离 job，直接被拒 `[WinError 5] 拒绝访问`
  （job 没开 breakaway 权限）。也就是说**这不是代码 bug，是环境不允许子进程活过父进程**
- **解决（绕开）**：把第 1、2 步合并到**同一进程**——`check_kernels.py` 拆出可复用的
  `run_check(...) -> (rc, uplink_mod, uplink_handle)`，`collect_nodes.py --check-kernels`
  直接调用它，把返回的通道 handle 传给采集逻辑。实测 `[uplink] 通道就绪` 只出现一次，
  采集期间不再试连节点
- **保留的能力**：跨进程「交接」仍然实现了（状态文件 + pid 存活校验 + 探活），
  环境允许时（例如普通桌面会话）能真的复用；分步执行时退化为重建（10~30 秒），不影响正确性
- **教训**：
  1. 任何「子进程要活过父进程」的设计，**先在目标环境实测存活**再动手写状态机
     （`Popen(detached)` 立刻返回 alive=True 不代表父进程退出后还活着）
  2. `CREATE_BREAKAWAY_FROM_JOB` 不是万能钥匙，job 没授权就是 WinError 5
  3. 与其和沙箱较劲，不如**把需要共享状态的两步放进同一进程**——最省事也最可靠

## 35. README 用反引号/加粗包裹的裸链接，尾随装饰符被吸进 URL 导致 404

- **现象**：采集日志里两条订阅链接名字带装饰符且一律「下载失败」：
  `ts-sf/fly` 的 `` clash` ``、`tglaoshiji/nodeshare` 的 `freenode**`。
  该仓库 README 明明声明了订阅链接，却被判成「声明的链接全部下载失败」，节点全丢
- **根因**：中文 README 极爱用行内代码 `` `https://...` `` 与 `**https://...**` 两种写法标记裸链接。
  `URL_RE` 的排除字符集只有 `空白 ) ] " ' < >` 与中文标点，**没有反引号和星号**，
  于是匹配到的 URL 尾部带上 `` ` `` 或 `**`；`_strip_url_tail()` 也没剥这两个字符。
  拼出来的地址必然 404，而日志里只显示「下载失败」，看起来像站点挂了
- **修复**：`URL_RE` 排除集加 `` ` ``、`*`、`|`；`_strip_url_tail()` 的 rstrip 集合同步加 `` ` ``、`*`、`|`
  （`|` 是 markdown 表格单元格分隔符，同理）
- **验证**：单点回归 `ts-sf/fly` —— 修复前 1 个链接目标为 `.../main/clash`` ` ``（404），
  修复后目标为干净的 `.../main/clash`，且被正确识别为 `kernel=clash` 的订阅
- **教训**：markdown 装饰符是 URL 抽取的**天然污染源**，排除集要按「README 实际怎么写」来列，
  不能只列「URL 语法里不可能出现的字符」；日志里出现带怪符号的文件名，先怀疑抽取而不是站点
- **遗留观察**：`ts-sf/fly` 的 README 把同一个文件写成「raw 直连 + `mirror.v2gh.com` 前缀」两行，
  无扩展名的 raw 形式（`/main/v2`、`/main/clash`）在 `repo_path` 分支因 `CANDIDATE_EXT` 不含空扩展名被丢弃，
  只有镜像前缀那一条能进采集；本次该镜像返回 403、raw 又被重置，故未能端到端取回节点

## 36. 「35 分钟必须降级 / 测试量 600」是我们自己拍的，平台只认 90 分钟硬上限

- **背景（用户 2026-10-27 追问）**：「35 分钟上限、90 分钟硬上限是我们自己定的吗？
  不是的话都可以放长，不要设限」
- **结论**：
  - **35 分钟 / `--max-test 600`**：**纯属我们自己写的启发式**，只存在于定时任务 prompt 里，
    没有任何平台或脚本依据。它按「每内核 600 个 ≈ 10 分钟」估的，实测吞吐根本对不上
    （2026-10-26 夜 v2ray 一个内核 600 个就跑了 40 分钟）→ 已删除，改为不设测试量上限
  - **90 分钟**：**不是我们定的**，是平台对单次自动化运行的强制取消（10-25 22:00 起跑、
    23:30 被砍，消息 `[CANCELLED] Run timed out`，正好 90 分钟，见第 31 条）。
    它在任务内部改不掉，`automation_update` 也没有超时字段 → 只能从「被砍时别丢数据」入手
- **真正的病根**：`test_nodes.py` 只在**四个内核全部跑完**后才写 `summary.*` 与 `pool_state.json`。
  一旦被强杀，前面几分钟到一小时的工作等于白干（2026-10-26 夜就是这样：v2ray 已落盘 52 条，
  但 summary 还是晨间的 32，多出一个「文件 52 ≠ 汇总 32」的假告警）
- **修复**：
  1. **增量落盘**：每个内核结束就把 `summary.md`/`summary.json`/仓库质量/`pool_state.json` 写一次
     （`lay.upsert_section` 按日期替换，同一天重复写是幂等的），被砍只丢「正在测的那个内核」
  2. **`--time-budget`（默认 0 = 不限）**：到期不再提交新节点、跳过未开始的内核，
     `summary.md` 明确标「本轮未跑完（主动收尾，不是失败）」，下次 `--cores <剩余>` 补跑。
     它的用途是**给发布留时间**，不是压测试量
  3. `summary.json` 增加 `sampled` / `partial` 字段，能区分「测完了就这么多」和「时间不够没测完」
- **修复过程中踩的两个坑（都已修）**：
  - `ThreadPoolExecutor.map(worker, gen)` 会**一次性把迭代器吃空**（内部先对所有入参 `submit`），
    写在生成器里的预算检查形同虚设，600 个照样全提交。改成按 `workers*2` 一块一块提交，
    每块之间重查表
  - `write_summary` 里我新加的 `for c in partial_cores:` 把模块别名 `c`（`import collect_nodes as c`）
    覆盖成字符串，导致下游 `c.quality_score(...)` 抛
    `AttributeError: 'str' object has no attribute 'quality_score'`，而且异常被 `| grep` 吃掉了。
    **教训：本模块顶层有 `as c`/`as lay` 别名，函数内禁止用 `c`、`lay` 当循环变量**
- **验证**：临时目录 `_tn_test`（复制真实 `nodes_uris.txt`/`nodes_meta.json`/订阅）跑两轮——
  ① 预算在 TCP 预筛阶段就用完 → 正确跳过内核并写出「未开始：v2ray」；
  ② 预算在测试中途用完 → `已提交 96/2260`、`partial=true`、汇总表 `截断（上限 600）` 与
  「中途截断：v2ray（96/2260）」都写对了
- **教训**：**「限时」要落在脚本里、写成可观测的收尾动作**，不要写成 prompt 里的固定数字。
  拍数字的结果是既没跑满窗口，又丢了一整轮的汇总

## 修复后的固定动作（缺一不可）

1. **单点回归**：用触发问题的样本（仓库 / 节点 URI）单独验证修复生效，不能只看整体数字
2. **重跑受影响环节**：解析类改动重跑采集；验证类改动重跑 `test_nodes.py`
3. **跑自检**：`health_check.py` 确认对应 finding 消失、且没引入新问题
4. **更新文档**：本文件追加条目；行为有变化时同步 `Skills/free-nodes-collector/SKILL.md`
5. **提交推送**：`src/publish_free_nodes.py --proxy auto`（脚本自身就在 src/ 里，无需同步/打包）
6. **写日志**：向用户说明「改了什么、为什么、验证结果」

## 自检发现（health_check 自动维护，按日期倒序）

### 2026-10-26 自检发现

**结论：无严重问题，1 个告警可优化**

| 级别 | 领域 | 问题 | 建议动作 |
|---|---|---|---|
| warn | 验证 | v2ray 文件条数 52 ≠ 汇总可用数 32 | 汇总与文件写出不一致，需排查 |

待观察（info）：
- [性能] 采集耗时 36 分钟

### 2026-10-25 自检发现


**结论：无严重问题，1 个告警可优化**

| 级别 | 领域 | 问题 | 建议动作 |
|---|---|---|---|
| warn | 下载通道 | 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ | 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选 |

待观察（info）：
- [性能] 采集耗时 43 分钟
