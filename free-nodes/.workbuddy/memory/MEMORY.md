# 项目长期记忆

## 免费节点每日采集（主窗口自动化 a3d7bb22-948c-4326-b344-f4c5535ddcd0，每天 22:00）

### 架构：采集在 CI，探测/验证在本地（2026-10-31 起）
- CI：仓库根 `.github/workflows/collect.yml`，北京 21:05（UTC `5 13 * * *`），只跑
  `--readme-only --no-latency-sort --uplink direct --time-budget 1500`（下载/解析/去重/落盘，不探测），
  提交 `nodes_uris` / `nodes_meta` / `Docs/` / `seed_repos` / `repo_quality` / `CHANGELOGS.md`，
  **不提交四份订阅文件**（那一刻含 TCP 死节点）。
- **探测必须本地**：runner 是 Azure 数据中心出口，封 ASN 的节点判死（假阴性）、海外通国内不通的判活
  （假阳性）。口径差异是有意的：`Docs/report.md`/`collection_logs.md` 是 CI 口径（含死节点），
  `nodes_uris.txt`/`nodes_meta.json` 是本地口径（只含可达）——数字不同不是 bug（known-issues 50）。
- 本地第一窗口顺序：`--sync-only` → `--probe-only` → `test_nodes.py` → health_check → publish → window_gate。
- **`--sync-only --proxy auto` 必须在 `--probe-only` 之前**（否则探昨天的清单）。只做 `fetch + merge --ff-only`，
  **绝不 rebase/reset/stash**（工作区有用户 C++ 改动）。失败重试要加 `--uplink-candidates 120`
  （默认 candidates 是确定性排序，原样重试等于同一批节点）。退出码 1 别空等，直接走兜底采集。
- 兜底采集（CI 未产出/同步失败）：`collect_nodes.py --readme-only --max-repos 80 --search-pages 2
  --search-days 3 --readme-date-tolerance 0 --drop-dead --check-kernels --time-budget 1500`；
  带 `--check-kernels` 就跳过独立内核检查步骤。
- **窗口闸门** `src/window_gate.py` 读 `Docs/summary.json` 四分支判定（partial / exhausted /
  tested≥min(cand,cap) / 内核漏跑），输出 `GATE: done|continue`（rc 0/1）。第二三窗口开工先跑，done 就结束。
  **第三窗口必须 `--date <采集日>`**（summary.date 是昨天，用 `date +%F` 会天天白跑）。

### 时间账与窗口接力
- 平台对单次运行有 **90 分钟强制取消**（`[CANCELLED] Run timed out`），任务内部改不掉。
  靠 `test_nodes.py --time-budget N` 主动收尾（到期不再提交新节点、跳过未开始内核、已测立即落盘，
  summary 标「本轮未跑完（主动收尾）」），**测试量不设人为上限**（`--max-test` 一律 2500）。
- 三窗口：22:00 主（探测+验证）→ 23:45 第二 → 01:30 第三；后两窗口先跑 gate，只续验证并加 `--resume-tested`
  （主窗口**不加**）。第三窗口跨零点必须取 summary 的采集日。
- `--resume-tested` 三件事：跳过本日已测 `host:port`；写回本窗口已测；**把前序窗口可用节点并回**
  available 与汇总（不并回会被冲掉，实测第二窗口把第一轮 20 个可用清零）。
- 进度记录默认开：`test_nodes.py` 无条件写 `nodes/tested_state.json`（`{date, cores:{core:[host:port]}}`）。
- 三窗口验证前都要 `taskkill` 残留内核（被强杀会留 xray/v2ray/mihomo/sing-box 占端口）。
- 时间账（全量 4×2500）：同步 ~1min + 内核检查 22s + 探测 ~3min + 验证 ~29min + 自检发布 ~7min ≈ 40min。

### 采集口径
- `--readme-only`：只跟随 README 声明的订阅链接，不扫仓库目录；链接按内核归属（v2ray/xray/clash/singbox），
  命中后保证进对应内核文件；README 按日期分列时只取当天（`--readme-date-tolerance 0`），没提日期按通用订阅保留。
- 只发 TCP 可达节点：`tcp_latency` 为 null 整条丢弃（`--keep-dead` 可关）；探测全不可达时回退保留全部并 warn
  （先查网络，别当「今天没节点」）。
- 仓库池：26 组关键词 × 2 页 × 三级扩量，`src/seed_repos.json` 上限 300。

### 验证口径（2026-10-28 实测定死，别凭感觉改）
- 每内核候选 ≤2500 全测，>2500 只测排序前 2500（`layout.FULL_BELOW/MAX_TEST`=2500，只能改 layout.py）。
  排序 = 协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序。`--limit/--min-available` 全量模式不生效。
- 参数名：`test_nodes.py --full-below/--max-test/--time-budget/--workers/--test-timeout/--retry`
  （`--test-full-below` 是 collect 的透传名，传给 test_nodes 直接报错）。
- `--test-timeout 3`（可用节点 p50 1.39s/p90 1.87s/max 2.24s，3s 仅误杀 2.5%）、`--retry 0`
  （117 个超时里放宽到 12s 只 2 个变可用=1.7%，吞吐腰斩；`reason=="timeout"` 代码层永不重试）、
  `--workers 24`（12 并发 1.3/s vs 24 并发 4.9~5.7/s，瓶颈是网络等待）；TCP 预筛 256 并发/1.5s。
- `--fair-budget` 必须加（内核顺序跑，不加第一个吃光预算，其余全跳过，known-issues 38）。
- 每内核可用数个位数到十几个是正常水位（探测要真出境+HTTPS）；不要为数字好看换 www.gstatic.com 或明文 http。
- `exhausted=true` = 候选已全测完，此时别加测试量、别放宽探测地址；可用数仍 <10 属源池质量问题。
- `test_nodes.py` 两个坑：① `ThreadPoolExecutor.map` 会吃空生成器，时间检查形同虚设，必须按块提交；
  ② 模块顶层有 `as c`/`as lay` 别名，函数内禁用 `c`/`lay` 当循环变量。

## 四内核协议能力（详见 Docs/protocol.md）
- `layout.CAPS` 是唯一事实来源（test_nodes 分流与 uplink `_cores_for` 都读它）。
- 判定三原则：① `grep -a` 二进制**文件本身**（`xray.exe | grep` 扫的是 stdout，必漏）；
  ② 协议名不能按字面猜（Xray 的 Hysteria2 = `hysteria` + `version:2`）；③ config check 过 ≠ 支持，必须 E2E 兜底。
- hysteria2 四内核均支持：v2ray `protocol:hysteria2` + `hy2Settings.password`；xray `protocol:hysteria`
  + `settings.version:2`（address/port 平铺）+ `hysteriaSettings.auth`，另支持 salamander 混淆与 udphop。
  xray hy2 回环 E2E 未过（真实节点未端到端验证）：线上仅 xray 失败先怀疑 xray 侧配置。
- 改协议能力的同步链：layout.CAPS → test_nodes 转换器 → protocol_check 用例 → Docs/protocol.md §7 →
  Skills/free-nodes-collector/SKILL.md → known-issues → 根 CHANGELOGS.md。

## 凭据与网络
- GitHub token：`C:\Users\bemin\.workbuddy\data\free-nodes-tools\github_token.txt`（600，不在仓库）；
  查找链 `--token` → `GITHUB_TOKEN`/`GH_TOKEN` → 该文件。配额 5000/时、搜索 30/分（匿名仅 60/时）。
  **任何日志/汇报只允许打码（前4…后4）**。CI 用仓库 Secrets 的 `FREE_NODES_TOKEN`（另一处配置）。
- `github.com:443` 被阻断；`api.github.com`、`codeload.github.com` 直连可；`raw.githubusercontent.com` 只能走镜像。
  → 采集下载与 push 都走自建通道；**只查 release 版本可用 `--uplink off` 直连**（实测 22s 跑完四内核）；
  `--update` 下载安装包必须 `--uplink auto`。
- 通道：`scripts/uplink.py` 用池内已验证节点起内核（clash→singbox→xray→v2ray 轮换），探 `https://github.com/`
  2xx 才算通；是全局 opener，搜索 API 与下载都走它；池空降级直连（物理限制）。
- **通道活不过父进程**：本机 job 结束即回收 detached 子进程（`CREATE_BREAKAWAY_FROM_JOB` WinError 5），
  所以「代理只建一次」只能靠同进程合并（`collect_nodes.py --check-kernels` 把 handle 传给采集）。
  换步骤顺序、合并进程都换不来通道复用（known-issues 34/51）。
- 推送 `--proxy auto` 不探测本机端口、直接自建；`auto` 前必须清空 GIT_PROXY（否则 git 把 "auto" 当代理地址）。
- 内核在 `~/.workbuddy/data/free-nodes-tools/bin`（环境变量 → 该目录 → legacy）。

## 仓库约定
- 布局：`free-nodes/` 三分层不分日期（根只留 README.md + CHANGELOGS.md；`nodes/` 订阅+available+nodes_uris/
  nodes_meta+pool/；`Docs/` 文档报告日志（`known-issues.md` 单文件：上方知识库 `## N.` + 末尾「自检发现」区块）；
  `src/` 全链路脚本唯一事实来源；`Skills/`；`.workbuddy/`）。**禁止建 YYYY-MM-DD 子目录**。
- 发布 `src/publish_free_nodes.py`：路径限定暂存 `free-nodes` + `.github/workflows`（CI 工作流不在 free-nodes 里，
  不带就永远上不了 GitHub），**绝不 `git add -A`**（仓库有用户 C++ 项目 Test/、Test.sln）；
  提交信息 `chore(free-nodes): 更新 <日期> 免费节点订阅`；push 失败写 `.git/free-nodes-pending-push.json` 下次补推。
- **路径单一事实来源 `src/layout.py`**（sub_path/avail_path/pool_path/uris_path/meta_path/... 助手，全脚本禁硬编码）；
  改布局只改 layout.py + `migrate_legacy_flat()`；**助手返回值不许二次加工**（`dirname(pool_dir)` 曾拼出 nodes/nodes/pool）。
  改布局后固定自检：`grep -rn "_dir_of\|_path_of\|dirname(lay\." src/` + 长任务收工比对「产物路径+mtime+计数」
  （静默错位不报错、退出码照样 0）。
- 补救错写数据用合并（`pool.merge` 按 host:port 去重、累加 ok_count），别直接覆盖。
- 日志去重：`Docs/report|summary|health_check` 按日期替换；`CHANGELOGS.md`/`known-issues` 自检区按「日期+标题」。
- `free-nodes/.gitattributes` = `* -text`；根 `.workbuddy` 是 junction 指向 `free-nodes/.workbuddy`
  （`.gitignore` 用根锚定 `/.workbuddy/`，只有 free-nodes 那份入库）；`__pycache__/`、`*.pyc` 全局忽略。
- 技能兼容层 `~/.workbuddy/skills/free-nodes-collector/`：scripts→`free-nodes/src`、references→`Docs` 的 junction，
  真实内容只在仓库，改完即生效，零同步。
- `known-issues.md` 只有一个文件：知识库条目 `## N.`，自检条目 `### 日期 标题` 只在末尾区块增删——
  绝不能让 `upsert_section`（插顶部+截断 30 条）作用在知识库上。
- 调试产物（`_san_*.pem`、`tmp_xray_hy2_*.py`）放 `~/.workbuddy/data/free-nodes-tools/debug/`，绝不入公开仓库。
- git 身份：`bemin <xiaoxuefeng@msn.com>`（仓库级）。

## 高频踩坑（详见 Docs/known-issues.md）
- **404 先怀疑自己拼的 URL**（43）：README 给的是 `/refs/heads/main/<path>`，漏掉 `refs/heads` 就 404，
  每天白丢约 2 万条。判上游是否真失效：打印 README 原文与请求地址比对。
- README 链接以 `/` 结尾 = 分类页/博客页，直接跳过（49），否则占掉 `MAX_README_LINKS=10` 配额。
  日志 `<名字>:0` 三义（空文件/HTML/格式未覆盖），别一律说「解析不到节点」。
- 判「上游为空」先查 `git/trees/HEAD?recursive=1` 的 `size`，别只看正文长度（0 字节可能是边缘缓存未命中）。
- 仓库「0 条」两归因：`下载失败`/`部分链接下载失败` = 通道/路径问题；只有「已下载但解析不到」才是格式问题。
- 静默减产类缺陷要盯：`is_known_bad_repo` 的次要判据曾把量源全跳过（46）、
  sing-box 配置顶部 `#profile-title` 让 `json.loads` 失败（47，已加 `_strip_leading_comments()`）、
  `update_repo_quality()` 用当日小样本覆盖历史大样本会把量源踢到队尾（待落地）。
