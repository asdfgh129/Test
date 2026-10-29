# 项目长期记忆

## 免费节点每日采集（自动化 a3d7bb22-948c-4326-b344-f4c5535ddcd0，每天 22:00）

- 产出目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes\` —— **三分层布局，不分日期**
  （根目录只留 `README.md` + `CHANGELOGS.md`；`nodes/` 订阅+available+nodes_uris/nodes_meta+pool/；
  `Docs/` 全部文档与报告（protocol/proxy/sources/tools-setup + `known-issues.md` **单文件**：
  上方踩坑知识库 + 末尾「自检发现」区块；collection_logs/review_logs 复数日志 +
  report/summary/health_check）；
  `src/` **采集/验证/发布全链路脚本的唯一事实来源**（12 文件：9 脚本 + publish_free_nodes.py
  + seed_repos/repo_quality/kernel_state json）；`Skills/free-nodes-collector/SKILL.md` 技能定义；
  `.workbuddy/memory/` 项目记忆（已纳入 git 跟踪）。过期节点没有意义，禁止再建 YYYY-MM-DD 子目录）
- 发布脚本：`free-nodes/src/publish_free_nodes.py`（只暂存 free-nodes，绝不 `git add -A`；
  `--workspace` 默认脚本上溯三级（src → free-nodes → 仓库根）；`--skill-scripts` 默认即自身所在目录；
  push 失败写 `.git/free-nodes-pending-push.json`，下次补推）
- 技能 junction 兼容层（2026-10-25 建）：`~/.workbuddy/skills/free-nodes-collector/` 的
  `scripts` 是指向 `free-nodes/src` 的目录 junction、`references` 指向 `free-nodes/Docs`，
  SKILL.md 是仓库版副本。**真实内容只在仓库里，改完即生效，零同步**；
  该目录仅为仍引用旧路径的定时任务 prompt 提供路径兼容，技能列表已不再发现它（代价可接受）
- 内核在 `~/.workbuddy/data/free-nodes-tools/bin`（查找顺序：环境变量 → 该目录 → 已失效的 legacy 路径）
- 采集策略：`--readme-only`（只跟随 README 声明的订阅链接，不扫仓库目录）
- **README 订阅链接按内核 + 按日期取数**（用户明确要求）：
  - 识别链接归属内核（v2ray/xray/clash/singbox），命中后该链接节点保证进对应内核文件
  - README 按日期分列订阅时**只取当天**（`--readme-date-tolerance 0`）；
    整份 README 没提日期的按通用订阅全部保留
- **采集只发 TCP 可达节点（2026-10-28 用户要求，已设为默认）**：采集末尾 TCP 握手探测，
  `tcp_latency` 为 null 的整条丢弃（`--keep-dead` 可关闭，`--drop-dead` 降为兼容参数）。
  实测 16620 条里仅 ~6800 条可达，订阅从 5~6MB 降到 2MB；探测全不可达时回退保留全部，不写空
- 验证策略（2026-10-28 起）：**每内核候选 ≤2500 全部实测，>2500 只测排序前 2500 个**
  （`--full-below 2500 --max-test 2500`，常量 FULL_BELOW/MAX_TEST 集中在 layout.py，两值相同；
  曾为 3000，2026-10-28 下调，理由见下条吞吐实测）；
  排序 = 协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序；
  summary 里 `exhausted=true` 表示候选已全部测完，此时不要再加测试量、也不要放宽探测地址。
  旧模式（`--no-full-test` 回退「可用数 <10 沿序追加，上限 limit×5、预算 1800s」）仅供对比
- **验证侧三个口径（2026-10-28 实测定位后定死，别凭感觉改回去）**：
  `--test-timeout 3`（可用节点 HTTP 耗时 p50 1.39s/p90 1.87s/max 2.24s，3s 只误杀 2.5%）、
  `--retry 0`（3s 判失败的 117 个里放宽到 12s 仅 2 个变可用 = 1.7%，代价是吞吐腰斩；
  且 `reason=="timeout"` 在代码层面永不重试）、`--workers 24`（12 并发 1.3 节点/s、
  24 并发 4.9~5.7，瓶颈是网络等待不是 CPU）；TCP 预筛 256 并发 / 1.5s
  （64 并发跑 16620 个要 8 分钟，会把 `--time-budget` 吃光、四个内核全被跳过）
- **时间限制的真相（2026-10-27 用户追问后核实）**：
  - 平台对单次自动化运行有 **90 分钟强制取消**（`[CANCELLED] Run timed out`，
    10-25 22:00 起跑、23:30 被砍）——**不是我们定的，任务内部改不掉，automation 也没有超时字段**
  - 曾经写在 prompt 里的「超过 35 分钟就 `--max-test 600`」是**我们自己拍的数字**，
    2026-10-27 已删除。用户明确要求「不要设限」：`--max-test` 一律给当前全量上限（现为 2500），
    不按固定测试量降级
  - 正确做法：**测试量不设人为上限**，靠 `test_nodes.py --time-budget N`（默认 0=不限）
    在平台强杀前主动收尾——到期停止提交新节点、跳过未开始的内核，已测结果立即落盘，
    `summary.md` 标「本轮未跑完（主动收尾，不是失败）」，`summary.json` 有 `sampled/partial`
  - **增量落盘**：每内核测完立即写 `available_*`/`Docs/summary.*`/仓库质量/`pool_state.json`，
    被强杀最多丢当前内核（此前只在四核全跑完后才写，被砍等于整晚白干）
- **一夜三窗口接力（2026-10-27 用户拍板「90 分钟跑不完就跑第 2 个、第 3 个」）**：
  - 22:00 主任务（采集+验证）→ 23:45 第二窗口 → 01:30 第三窗口，后两个**只续跑验证、不采集**
  - 自动化 id：主 `a3d7bb22-…` / 第二 `a4c4ae9d-9d70-4395-b78d-63a0a131e62d` /
    第三 `19f100fb-c01d-4d31-9a1e-76444fbf51ad`
  - **进度记录默认开**：`test_nodes.py` 无条件写 `nodes/tested_state.json`
    （`{date, cores:{core:[host:port]}}`，路径助手 `layout.tested_state_path()`），
    日期不符视为空。所以主窗口不用加任何参数，后两窗口才加 `--resume-tested`
  - **`--resume-tested` 三件事**：跳过本日已测的 `host:port`（否则第二窗口从排序头部重测，
    90 分钟全打水漂）；把每窗口已测写回；**把前面窗口已验证可用的节点并回** available 与汇总
    （不并回会被冲掉——实测第二轮测 96 个全不可用，第一轮 20 个可用清零）
  - 汇总累积：`Docs/summary.*` 会合并同一天前序窗口的内核结果，换 `--cores` 不会抹掉别的内核；
    `tested` 记**本日累计**、`partial` 只针对**本窗口**，「本轮未跑完」只列本窗口真跑过的内核
  - 第三窗口跨零点，`--date` 必须取 `Docs/summary.json` 的 `date`（采集日），不能用 `date +%F`
  - 三窗口都要在验证前 `taskkill` 残留内核（前窗口被强杀会留 xray/v2ray/mihomo/sing-box 占端口）
- 仓库池：26 组关键词 × 2 页（100 条/页）× 三级扩量，`src/seed_repos.json` 上限 300 个
- **自动化 prompt 已可自助更新**（2026-10-27 起 `automation_update` 工具可用，
  id `a3d7bb22-948c-4326-b344-f4c5535ddcd0`）：已把 35 分钟/600 那条换成 `--time-budget` 规则，
  并把 known-issues 第 34/35/36 条写进第 4 步
- **`test_nodes.py` 两个易踩的坑**：① `ThreadPoolExecutor.map` 会一次性吃空迭代器，
  写在生成器里的时间检查形同虚设，必须按块提交；② 模块顶层有 `as c`/`as lay` 别名，
  函数内禁止用 `c`、`lay` 当循环变量（会把 `c.quality_score` 变成字符串属性错误）

## 四内核协议能力（2026-10-25 实测校准，详见 Docs/protocol.md）

- 能力矩阵 `layout.CAPS` 是唯一事实来源（test_nodes 分流与 uplink 的 `_cores_for` 都读它）
- **能力判定三原则**（用户两次质疑后沉淀）：① grep 二进制**文件本身**
  （`xray.exe | grep` 扫的是进程 stdout，必漏检，必须 `grep -a` 文件）；
  ② 协议名不能按字面猜（Xray 的 Hysteria2 叫 `hysteria` + `version:2`，名字里没有 "2"）；
  ③ config check 过 ≠ 装填对 ≠ 支持，必须 E2E 实测兜底
- hysteria2 四内核均支持（v2fly 5.x 全系、Xray ≥ v26.1.23）：v2ray 用
  `protocol:hysteria2` + 传输层 `hy2Settings.password`；xray 用 `protocol:hysteria`
  + `settings.version:2`（address/port 平铺）+ 传输层 `hysteriaSettings.auth`；
  xray 另支持 salamander 混淆与 udphop 端口跳跃
- xray hysteria2 回环 E2E 未过（回环服务端 SNI 选证书怪象），**真实节点未端到端验证**：
  线上若仅 xray 失败而其他内核可用，优先怀疑 xray 侧配置/兼容，别急着判节点不可达
- 变更协议能力时的固定同步链：layout.CAPS → test_nodes 转换器 → protocol_check 用例 →
  protocol.md（仅 `Docs/protocol.md` 一份，仓库内即唯一副本）→ `Skills/free-nodes-collector/SKILL.md` → known-issues

## GitHub token（凭据，勿泄露）

- 存放：`C:\Users\bemin\.workbuddy\data\free-nodes-tools\github_token.txt`（权限 600，
  **不在 git 仓库内**；`.gitignore` 已加 `github_token.txt` 兜底）
- 查找链：`--token` → `GITHUB_TOKEN`/`GH_TOKEN` 环境变量 → 上述文件
- 配额：带 token 核心 5000/时、搜索 30/分；匿名只有 60/时、10/分
- **日志与汇报只允许打印打码形式（前 4…后 4），任何情况下不得输出完整 token**

## 网络环境事实（重要）

- `github.com:443` 曾长期被阻断（连接重置）；`api.github.com`、`codeload.github.com` 可直连；
  `raw.githubusercontent.com` 不可直连，靠镜像（gh-proxy.com / gh-proxy.org / gh.monlor.com 等，失效率高）
- 因此 GitHub 采集与 push 都走 **自建代理**：`scripts/uplink.py` 用池内已验证节点起内核
  （clash→singbox→xray→v2ray 轮换），探测 `https://github.com/` 或
  `https://api.github.com/rate_limit` 拿 2xx 才算通；四内核全不通才直连
- 通道是全局 opener，所以**搜索 API 与节点下载都走它**，不只是下载
- 池为空时无候选节点可起代理（首次运行），会降级直连 —— 属物理限制，不是故障
- 推送探测只认 `https://github.com/`（api 通不代表能 push）

## 上行通道生命周期（2026-10-26 用户三点要求落地）

- **第 1 步就建代理**：`check_kernels.py` 查 `api.github.com` 前先自建通道（`--uplink auto`），
  否则直连不通时版本检查必然失败。走免费节点代理时出口 IP 与他人共享，
  **匿名配额 60/时 几乎必然 403，查版本必须带 token**（`latest_release` 已加 Authorization）
- **代理只建一次 = 同进程合并**：`collect_nodes.py --check-kernels` 内部调
  `check_kernels.run_check()`，把返回的通道 handle 直接交给采集。
  **不能依赖「子进程活过父进程」**：本机 job 在命令结束时回收 detached 子进程，
  `CREATE_BREAKAWAY_FROM_JOB` 被拒 WinError 5（详见 known-issues 第 34 条）；
  `runtime/uplink_session.json` + pid/探活只是尽力而为的交接
- **推送**：`publish_free_nodes.py --proxy auto` **不探测本机代理端口**（用户明确要求），
  直接自建；`--proxy <url>` 才用指定代理。注意 `auto` 必须先清空 GIT_PROXY，
  否则 git 会把字面量 "auto" 当代理地址（踩过：`Could not resolve proxy: auto`）
- **known-issues 只有一个文件**：`Docs/known-issues.md`。知识库条目用 `## N.`，
  自检条目用 `### 日期 标题` 且只在末尾「自检发现」区块内增删——
  绝不能让 `upsert_section` 那套「插顶部 + 截断 30 条」作用在知识库上（会挤掉旧条目）

## 仓库约定

- git 身份：`bemin <xiaoxuefeng@msn.com>`（仓库级配置）
- 仓库里同时有用户的 C++ 项目（`Test/`、`Test.sln`），自动化只允许路径限定的 add
- `free-nodes/.gitattributes` 用 `* -text` 防止 autocrlf 改写订阅文件
- **路径单一事实来源 = `free-nodes/src/layout.py`**（sub_path/avail_path/pool_path/uris_path/
  meta_path/report_path/summary_path/health_path/issue_path/seed_file_path 等助手），
  全脚本禁止硬编码 join；改目录布局只改 layout.py + `migrate_legacy_flat()`
- **路径助手的返回值不许二次加工**（known-issues 第 32/33 条的血泪）：
  `dirname(lay.pool_dir(root))` 在旧平铺布局下是对的，三分层后拼出 `nodes/nodes/pool`；
  调用方要么直接传 `root`、要么直接用助手给的最终路径，禁止「助手路径 + 自己再取父目录/再拼一层」
- 改布局后的固定自检两条：① `grep -rn "_dir_of\|_path_of\|dirname(lay\." src/` 扫旧标识符与二次加工；
  ② 长任务收工后抽查「产物路径 + mtime + 关键计数」——静默错位不报错、退出码照样 0，
  只有比对时间戳和节点数才看得出来
- 补救错写的数据用**合并**（`pool.merge` 按 `host:port` 去重、累加 `ok_count`），
  别图省事直接覆盖，否则历史累积节点就没了
- md 日志去重粒度：`Docs/report`/`Docs/summary`/`Docs/health_check` 按**日期**替换；
  根 `CHANGELOGS.md`/`Docs/known_issues.md` 按**日期+标题**替换（一天多事件并存）
- 仓库根 `.workbuddy` 是指向 `free-nodes/.workbuddy` 的 junction（宿主 memory 系统固定读
  `Test/.workbuddy/memory/`，靠它不断链）；`.gitignore` 用根锚定 `/.workbuddy/`，
  所以只有 free-nodes/.workbuddy 入库；`__pycache__/`、`*.pyc` 已全局忽略
- 调试产物（hysteria2 回环测试的 `_san_*.pem`、`tmp_xray_hy2_*.py`）在
  `~/.workbuddy/data/free-nodes-tools/debug/`，**绝不入公开仓库**
- **看到 404 先怀疑自己拼的 URL**（known-issues 第 43 条）：GitHub「复制链接」给的是
  `raw.githubusercontent.com/<o>/<r>/refs/heads/main/<path>`，解析漏掉 `refs/heads`
  就变成 `heads/main/...`、ref 记成 `refs`，拼出来的地址必然 404。
  代价是每天白丢约 2 万条候选，还会被自检报成「上游路径失效」——判断上游是否真失效，
  最短路径是把 README 原文打出来和我们的请求地址比对
- 仓库「0 条」有两种归因，别混：`下载失败`/`部分链接下载失败` 是通道与路径问题，
  只有「已下载但解析不到节点」才是格式覆盖问题（`health_check` 用 `pfail` 桶分开计）
