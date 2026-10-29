# 变更与修复记录（时间倒序）

> 按日期倒序；包含脚本修复、参数调整、内核版本升级等

## 2026-10-29 第三窗口：自检「配额」错报修复（身份取数统一到凭据文件）

- **本窗口未跑验证**：`Docs/summary.json` 四内核 `partial=false`、`sampled` 均已到 2500 上限
  （2502/2503/2506/2503），`exhausted=false` 是取样上限的稳态（同 10-28 口径），
  第一窗口 23:08 已测完 → 跳过续跑，未重测任何节点，只做自检 + 修复 + 发布
- **修 info（错报，有证据）**：自检连续三天写「GitHub 配额 core 60/60、search 10/10（匿名）」，
  与采集实际身份不符。两处缺陷叠加：
  - `check_quota()` 判身份只看 `os.environ["GITHUB_TOKEN"]`，**没走** `load_github_token()`
    的凭据文件查找链 → 本机环境变量为空、token 在文件里，于是天天判成匿名
  - `github_api("/rate_limit")` **没传 token** → 查到的是匿名桶，`limit=60` 被当成「采集可用额度」
  - 先证伪：用 `load_github_token()` + 带 token 直查得 `core 5000/5000、search 30/30`
    （`ghp_…x6hY`，打码），与 60/60 差两个数量级 → 是报告错，不是采集缺配额
  - `health_check.py`：统一 `c.load_github_token()` 取身份 + token 传入 `rate_limit` +
    `c.token_desc()` 打码显示；新增「带 token 失败 → 退回匿名查一次」分支，
    用于区分**凭据过期**（报 warn 并注明配额是匿名桶）与**网络问题**
  - 回归三分支：真实 token → 5000/5000；伪造 token → warn + `HTTP 401` 回退说明；
    无凭据 → 60/60 匿名（与原行为一致）。整轮复跑 0 严重 / 5 告警，告警集合与修复前一致
  - 详见 `Docs/known-issues.md` 第 45 条
- **数据复核**（第一窗口产出）：原始 117984 → 唯一 10177 → TCP 可达 3918 → 发布 3912；
  分流 3438/3347/3870/3706；四核可用 30/105/72/50（可用率 1.2%/4.2%/2.9%/2.0%）
- **自检 0 critical / 5 warn**：三条「可用率异常低」与 `crashgfw` 那条（第二窗口已加受限重试，
  生效于下次采集）属已知水位，镜像失效 10/13 属环境
- **无回归核对**：singbox 失败原因 `reset` 1860/2503（74%），10-28 为 1812/2509（72%），
  同一指纹，不是本次引入

## 2026-10-29 第二窗口：外部订阅链接加一次受限重试（瞬时抖动会整仓归零）

- **本窗口未跑验证**：`Docs/summary.json` 四内核 `partial=false`、`sampled` 均已达上限
  （2502/2503/2506/2503），第一窗口 23:08 就测完，按规则跳过续跑，只做自检 + 修复 + 发布
- **修 warn（有证据）**：自检报「1 个高贡献仓库本次 0 条：`crashgfw/free-airport-nodes`
  （历史 1050 条，部分链接下载失败）」。日志显示 10 条链接 9 条失败（URLError ×2 + 超时 ×1 …）
  - 归因：9 条节点链接全在同一域名 `ndxy.fn0821.xyz/nodes/<hex>`；**窗口内单点复现 0.3~0.8s 全部 200、
    每条 8860B、正常解出 30 个节点**（IPv6 不通、IPv4 正常）→ 下载侧瞬时不可达，不是解析缺陷、
    也不是 URL 拼错（第 43 条那种）
  - 佐证：当天 19 条下载失败里 `URLError` 6 / `429` 4 / `503` 3 / `404` 3 / `403` 2 / `超时` 1，
    **13 条属瞬时类**，只有 3 条 404 是真上游失效
  - `collect_nodes.py`：新增 `RETRYABLE_HTTP={408,425,429,500,502,503,504}` 与
    `_retryable_fetch_error()`；`fetch_url_text()` 把原逻辑收成 `once()`，瞬时失败**整链再走一次**（只 1 次），
    429 尊重 `Retry-After` 封顶 3s。**404/410 与「超时」明确不重试**（前者是第 42 条成果，
    后者会把单仓 90s 预算翻倍）
  - 回归 4 例：正常 0.3~0.8s 不变 / 连接重置 2.50s（确实重试）/ 404 0.48s 不重试 /
    超时 2.01s 只等一次；整仓回归 10 条链接 9 条 OK（第 10 条是分类网页，非订阅）
  - 生效从下次采集（2026-10-30 22:00）开始，本窗口不采集
- **数据**（第一窗口产出，本窗口复核）：原始 117984 → 唯一 10177 → TCP 可达 3918 → 发布 3912；
  分流 3438/3347/3870/3706；四核可用 30/105/72/50
- **自检 0 critical / 5 warn**：三条「可用率异常低」（1.2%/2.9%/2.0%）为免费源正常水位，
  镜像失效 10/13 属环境，`crashgfw` 那条即上面已修
- **新观察（不改代码）**：`MAX_README_LINKS=10` 使该仓库 17 条订阅链接只跟随前 10 条，
  未跟随的 7 条记入 `Docs/review_logs.md`，等有产出率数据再决定是否放宽

## 2026-10-29 第一窗口：80 个仓库首次全部扫完，四内核全部测完（无代码改动）

- **采集参数微调（非代码）**：`--time-budget 3000`（默认 2400）。10-28 首窗口在 52/80 撞预算，
  本窗口给到 50 分钟，80 个仓库全部扫完（35 分钟），代价是验证预算压到 2635s，
  实测四内核各 ~450s 够用。**这是本窗口唯一的口径变化**
- **内核检查**：`[uplink] 通道就绪` 仅 1 次（v2ray @ 202.50.253.81:19999），`--check-kernels`
  复用成功；v2ray 5.53.0 / clash 1.19.33 / singbox 1.14.4 均为最新；
  **xray 上游已发 26.10.29（本地 26.10.21）**，能力指纹 13 项接受 / 0 拒绝，与基线完全一致，
  **判定为纯版本号前进、不影响节点处理逻辑，本窗口不升级**（升级会改变验证侧二进制，
  想升可在后续窗口用 `check_kernels.py --update` 单独做并复跑一轮验证）
- **10-28 修复生效验证**：`sakha1370/OpenRay` 22457 条、`SoliSpirit/v2ray-configs` 22017 条、
  `barry-far/V2ray-Config` 18507 条（10-28 这几个都是 0 或部分失败），`refs/heads` 修复确认落地
- **数据**：原始 117984 → 唯一 10177 → TCP 可达 3918（38.5%，中位 23ms 起）→ 发布 3912；
  分流 3438/3347/3870/3706
- **验证**：四核 2502/2503/2506/2503 全部测完，`partial=false`，未被 `--time-budget` 截断；
  可用 30/105/72/50
- **自检 0 critical / 5 warn**：三条「可用率异常低」（v2ray 1.2% / clash 2.9% / singbox 2.0%）
  与 10-28 同水位（1.3% / 3.7% / 2.9%），属免费源正常波动；镜像失效 11/13 属环境；
  `crashgfw/free-airport-nodes` 0 条为上游部分链接失效。**本轮不改代码**
- **新观察（不改代码，证据不足）**：`sinavm/SVM` 单仓库吃掉约 9 分钟、9 个链接最终 0 条。
  已用 API 查该仓库根目录，`config.txt` 仅 0.03MB、其余 json 均 <0.01MB，
  **「大文件超时」的猜测被否定**；按 0.03MB 小文件 × 9 链接 ≈ 60s/链接 反推，
  时间花在逐链接的多通道回退上而非体积。根因待抓单点复现，记入 `Docs/review_logs.md`

## 2026-10-28 第三窗口：修掉「refs/heads 链接被解析坏」——每天白丢约 2 万条候选节点

- **本窗口未跑验证**：`Docs/summary.json` 四内核 `partial=false`（v2ray 2118 / xray 2159 /
  clash 2508 / singbox 2509 均已达排序前 2500 的取样上限），前两窗口已测试完，按规则跳过续跑，
  只做自检与发布
- **修 critical（真根因）**：自检 1 critical「14/51 个仓库下载失败（27%）」。
  复现 4 个仓库 8 条链接全 404，打印 README 原文后确认**是我们自己拼错了 URL**：
  GitHub 给出的 `raw.githubusercontent.com/<o>/<r>/refs/heads/main/<path>` 被解析成
  `heads/main/<path>`（ref 还被记成 `refs`），拼出来的地址必然 404
  - `collect_nodes.py`：新增 `_split_raw_parts()`，三条 raw 形状分支
    （raw.githubusercontent / gitmirror+kgithub / githack）统一按 `refs/heads|tags` 拆 ref 与路径
  - 端到端回归：`SoliSpirit/v2ray-configs` 0 → **10980 条**、`cbusifabcap/daily_free_vpn` 0 → 7674、
    `whoahaow/rjsxrd` 0 → 2293、`free18/v2ray` 0 → 350、`crashgfw/free-airport-nodes` 0 → 150
- **修归因（warn 方向错）**：仓库节点数为 0 但部分链接下载失败时，日志原来写
  「0 条（文件已下载但解析不到节点）」，把排查引向「格式覆盖」。现写
  「0 条（3/10 个链接下载失败，其余已下载但解析不到节点）」；
  `health_check.py` 新增 `pfail` 桶，不再把这类算进「解析不到节点」，避免误触发「解析能力 critical」
- **更正第 42 条结论**：上一窗口把这批 404 归因为「上游路径失效」，实际至少 5 个仓库是我们自己的
  解析 bug，已在第 42 条末尾更正、并在第 43 条完整记录
- **数据未变**：本窗口不采集，发布的仍是 22:00 那轮的 2744 条（修复从下一次采集生效）
- 详见 `Docs/known-issues.md` 第 43 条

## 2026-10-28 第二窗口：下载失败带原因标签 + 404 快速失败 + 趋势改按采集总量比较

- **本窗口未跑验证**：首窗口已把四内核全部测完（`partial=false` + 各内核 `sampled` 达上限），
  按规则跳过续跑，只做自检与发布
- **修 critical 归因**：自检报「14/51 个仓库下载失败（27%）」，日志里却只有「下载失败」没有原因。
  抽样单点复现 `SoliSpirit/v2ray-configs`、`ts-sf/fly` 均为 **HTTP 404**（上游改了路径），
  不是通道截断
  - `collect_nodes.py`：新增 `err_tag()`，README 链接失败明细记成 `clash:下载失败(HTTP 404)`，
    仓库级记成 `- repo：下载失败（HTTP 404）`
  - `collect_nodes.py`：`fetch_url_text` 遇 **404/410 立即放弃剩余镜像**（镜像只做转发，
    原站 404 时必然全 404）。单条死链 37s → **1.0s**（14 条 ≈ 省 5 分钟，直接缓解第 41 条的预算截断）
  - `health_check.py`：失败仓库里 ≥60% 是 404/410 时降级 warn 并标注「上游路径失效」，
    其余仍报 critical（无标签的历史日志走原分支）
  - 回归：仓库级 -1 判定由 `endswith` 改 `in`（否则带后缀后会被误判成「解析不到节点」）
- **修趋势误报**：`今日 2744 条 vs 中位数 13021 条（降幅 >60%）` 是口径错位——
  采集侧 10-28 起默认丢弃 TCP 不可达节点，`uniq` 变成过滤后量，历史日志是过滤前量。
  今日实为 **6931 采集 / 2744 发布**。采集日志新增
  `- TCP 过滤：丢弃不可达 N 条（采集总量 M 条），保留 K 条`，
  `health_check.collected_of()` 统一按采集总量比较（自检结论 6 warn → 5 warn）
- **数据订正**：给今天的采集日志条目补上该行（4187 丢弃 / 6931 总量，取自当日采集日志）
- 详见 `Docs/known-issues.md` 第 42 条

## 2026-10-28 首窗口：四内核全部测完（吞吐提升见效），采集被 40 分钟预算截断到 52/80

- **验证侧达标**：`--test-timeout 3 / --workers 24 / --retry 0` 全部生效，四内核在 34 分钟预算内
  **全部测完**（v2ray 2118、xray 2159、clash 2508、singbox 2509，均 exhausted），
  分别可用 27 / 127 / 93 / 72。这是 10-25 起第一次在单个窗口内测完四个内核
- **采集侧被护栏截断**：80 个候选只走到 52 个就触发
  `[warn] 已达采集时间预算`（默认 `--time-budget 2400`），唯一节点 6931 条、TCP 可达 2744 条；
  前一日分别是 16629 / 6859。原因与处理见 known-issues 第 41 条
- **未改代码**：本次唯一的 critical（14/51 仓库下载失败）与 warn（镜像失效 10/13）
  都归因于「死链仓库 + 镜像环境」，属既定护栏与环境波动；
  候选改法（同仓库连续 2 个链接全挂即短路）留待单点回归后再落，观察项写入 `Docs/review_logs.md`
- **内核**：四内核均为最新（v2ray 5.53.0 / xray 26.10.21 / mihomo 1.19.33 / sing-box 1.14.4），
  能力指纹无变化；`[uplink] 通道就绪` 全程只出现一次（v2ray @ 202.50.253.81:19999），复用正常
- **发布**：commit `eb1f040` → origin/master 成功（自建 v2ray 代理推送）

## 2026-10-28 只采集 TCP 可达节点 + 验证侧 3s 超时 / 24 并发 / 不复测（吞吐 ×4）

- **问题**：三窗口接力仍测不完四内核（10-27 整晚 75 分钟只测 7321 个，clash/singbox 各 800 左右）。
  此前一直在砍测试量（3000→1000→600）掩盖症状，没量过单节点成本
- **实测定位**：内核启动只要 ~390ms（不是瓶颈）；可用节点 HTTP 耗时 p50 1.39s / p90 1.87s / max 2.24s；
  失败节点 p50 2.78s 且几乎全顶到 12s 超时；12 并发 1.3 节点/s、24 并发 4.9~5.7 节点/s。
  三条叠加：12s 超时 × retry 1 次 × 12 并发
- **改动**
  - `collect_nodes.py`：**默认只发布 TCP 可达节点**（`--keep-dead` 关闭）。16620 → ~6800 条，
    订阅从 5~6MB 降到 2MB 上下；`--drop-dead` 保留为兼容参数；探测全不可达时回退保留全部，不写空
  - `test_nodes.py`：`--test-timeout` 12 → **3.0**（误杀率实测 2.5%）、`--retry` 1 → **0**（且超时类永不重试）、
    `--workers` 12 → **24**、`--tcp-workers` 64 → **256**、`--tcp-timeout` 2.0 → **1.5**
  - `layout.py`：`FULL_BELOW`/`MAX_TEST` 3000 → **2500**（4 核 ≈ 29 分钟，总时长 ~72 分钟）
  - `test_nodes.py`：预算被预筛吃光且一个内核都没跑时，强制给第一个内核 180s（避免整晚空产物）
  - `test_nodes.py`：修 `--out` 与采集目录不同时 `repo_quality.json` 写入 `FileNotFoundError` 崩溃
- **验证**：600 个节点单点回归 106s（5.66 节点/s）、44 个可用，产物/汇总/池写入正常
- 详见 `Docs/known-issues.md` 第 40 条

## 2026-10-27 自检不再误删 `review_logs.md` 里手写的「窗口」小节

- **问题**：第三窗口跑完 `health_check.py --date 2026-10-27` 后，`Docs/review_logs.md` 中
  「## 2026-10-27 第二窗口（23:45 起跑…）」整段消失，只剩脚本生成的「自检摘要」；
  退出码照样 0，不比对文件内容根本发现不了（已从 git 恢复内容）
- **根因**：`layout.upsert_section` 默认日报模式按 `startswith("## <日期>")` 判重，
  手写小节标题同样以日期开头 → 被当成同一天旧摘要覆盖。日报（summary/report）标题带时间，
  只能前缀匹配，所以不能全局改成精确匹配
- **改动**：`health_check.py` 写 `review_logs.md` 时传 `match_heading=True`，
  只替换「同日期 + 同标题=自检摘要」的小节，手写小节不再受影响；日报类行为不变
- **验证**：连续两次 `health_check.py --date 2026-10-27`（`--skip-network` 与完整各一次），
  小节顺序稳定为「自检摘要 / 第三窗口 / 第二窗口 / 10-26 / 10-25」，自动摘要始终只一条
- 详见 `Docs/known-issues.md` 第 39 条

## 2026-10-27 `--fair-budget`：内核顺序跑时，别让第一个内核吃光整窗预算

- **问题**：首窗口把 2321s 全花在 v2ray（1584/3005），日志三行「xray/clash/singbox：墙钟预算已用满，
  跳过该内核」——三个内核的 `available_*` 还是前一天的旧文件，对它们来说当天零产出。
  根因是 `for core in cores:` 顺序跑、而 deadline 是整轮的；实测吞吐 0.62 个/秒，
  四内核全量 5.4 小时 > 一夜三窗口 4 小时，顺序跑必然让后面的内核饿死
- **改动**：`test_nodes.py` 新增 `--fair-budget`（默认关，需配合 `--time-budget`）：
  每个内核开始前重算「剩余墙钟 ÷ 尚未开始的内核数」作为它的 deadline，
  前面内核提前测完的空档自动被后面吸收。**取样口径不变**，`--full-below`/`--max-test` 仍是 3000
- **实测**（第二窗口 3900s）：v2ray 576 个（7 可用）、xray 624（65）、clash 792（75）、singbox 840（68），
  四个内核当天全部有数据（61/65/75/68），代价是四个内核都 `partial=true` 而非某一个 `exhausted`
- **观察**：v2ray 排序尾部可用率仅 1.2%（头部 3.4%），「前 3000」对 v2ray 过量；
  按要求不压测试量，只记进 `Docs/review_logs.md`
- 详见 `Docs/known-issues.md` 第 38 条；`Skills/free-nodes-collector/SKILL.md` 已同步（参数表 + 第 7 条 + 运行示例）

## 2026-10-27 一夜跑三个窗口：`--resume-tested` 让验证接力不重测、不冲掉当日可用

- **背景**：平台 90 分钟硬上限改不掉，一个窗口测不完四个内核。改为 22:00 采集+验证 →
  23:45 续跑 → 01:30 再续跑，每个窗口都能把已测结果落盘并发布
- **`--resume-tested`（默认关）**：跳过本日已测过的 `host:port`（`nodes/tested_state.json`
  按日期自动重置），只测排序里的下一批候选；否则第二个窗口从头部重测，90 分钟全是重复劳动
- **当日可用并回**：续跑时把前面窗口已验证可用的节点并回 `available_<core>.*` 与汇总。
  实测踩到过：第二轮测 96 个全不可用，第一轮的 20 个可用节点被覆盖清零
- **汇总累积**：`Docs/summary.*` 合并同一天前序窗口的内核结果，换个 `--cores` 跑不会把
  别的内核从汇总里抹掉。`tested` 记本日累计、`partial` 只针对本窗口
- **口径**：路径助手 `layout.tested_state_path()` 新增（路径单一事实来源不变）；
  `summary.json` 补 `policy` 字段，合并后「轮次」列不再退化成数字
- 详见 `Docs/known-issues.md` 第 37 条；`Skills/free-nodes-collector/SKILL.md` 已同步

## 2026-10-27 验证侧不再拍脑袋限测试量：增量落盘 + `--time-budget`（用户要求「不要设限」）

- **删掉自定的 35 分钟降级规则**：那条「超过 35 分钟就 `--max-test 600`」是我们自己写在 prompt 里的，
  实测吞吐对不上（600 个/内核要 40 分钟），已作废；测试量不再设人为上限
- **平台 90 分钟硬上限留下，但不再是致命伤**：`test_nodes.py` 原先只在四核全跑完后才写
  `summary.*` 与 `pool_state.json`，被强杀等于白干。现在**每个内核结束立即增量落盘**，
  被砍最多丢当前内核
- **新增 `--time-budget`（默认 0 = 不限）**：主动收尾用，到期停止提交新节点、跳过未开始的内核，
  汇总里标注「本轮未跑完（主动收尾，不是失败）」，下次 `--cores <剩余>` 补跑；
  `summary.json` 新增 `sampled` / `partial` 字段
- **顺手修两个自己引入的坑**：`Executor.map` 一次性吃空迭代器（预算检查失效，改按块提交）；
  `for c in ...` 覆盖了模块别名 `c`（`collect_nodes`）导致汇总写入抛 AttributeError
- 详见 `Docs/known-issues.md` 第 36 条

## 2026-10-26 README 反引号/加粗裸链接被吸进 URL 导致 404（已修复）

- **问题**：`URL_RE` 的排除字符集没有反引号和星号，中文 README 常见的
  `` `https://...` ``（行内代码）与 `**https://...**`（加粗）写法会把装饰符带进 URL 尾部，
  下载必然 404。本次采集命中 2 例（`ts-sf/fly` 的 `clash`、`tglaoshiji/nodeshare` 的 `freenode`），
  日志里表现为「README 声明的链接全部下载失败」
- **改动**：`collect_nodes.py` 的 `URL_RE` 排除集加 `` ` ``/`*`/`|`；
  `_strip_url_tail()` 的 rstrip 集合同步扩充
- **验证**：单点回归 `ts-sf/fly` README，链接目标由 `.../main/clash`` ` ``（404）
  变为干净的 `.../main/clash`，并正确识别为 `kernel=clash` 订阅
- 详见 `Docs/known-issues.md` 第 35 条

## 2026-10-26 上行通道前移 + 推送不探测本机端口 + known-issues 合并（用户三点要求）

- **第 1 步就自建代理**：`check_kernels.py` 原先完全没有代理能力（`latest_release(proxy=...)`
  参数留着没人传），查 `api.github.com` 只能指望直连。现在默认 `--uplink auto`：
  用已验证节点建通道 → 查版本 → 结束关闭（独立运行无残留）
- **代理只建一次**：`check_kernels` 拆出 `run_check() -> (rc, uplink_mod, handle)`，
  `collect_nodes.py --check-kernels` 在同一进程里先跑检查、再接管该通道采集。
  原因：本机 job 限制会在命令结束时回收 detached 子进程（`CREATE_BREAKAWAY_FROM_JOB`
  被拒 WinError 5），跨进程复用只能尽力而为 → 详见 known-issues 第 34 条
- **版本查询必须带 token**：走免费节点代理时出口 IP 与他人共享，匿名配额（60/时）
  几乎必然 403（实测四核全被限流），`latest_release` 现在带 `Authorization`
- **推送不探测本机端口**（用户要求）：`publish_free_nodes.py --proxy auto` 删掉
  `PROXY_CANDIDATES` / `detect_proxy()`，直接用已验证节点自建（先尝试接管登记在案的通道）；
  `--proxy http://...` 仍可指定现成代理
- **known-issues 合并为一个文件**（用户要求）：`Docs/known-issues.md`（人工知识库）与
  `Docs/known_issues.md`（自检表格）名字只差一个连字符、内容还会互相抄串。现合并为单文件：
  上方编号知识库，末尾「自检发现」区块（条目用 `### 日期 标题`，`layout.append_issue`
  独立插入、不碰知识库条目、幂等去重、最多 30 条）
- 顺手修：`collect_nodes.py` 空结果时 `uniq[0]` 抛 `IndexError`（预算过短 / 来源全失败时整轮失败）

## 2026-10-25 内核检查与升级

- v2ray 新增支持：hysteria2/-/tls、vless/tcp/vision（可考虑放宽 layout.CAPS）
- xray 新增支持：hysteria2/-/tls（可考虑放宽 layout.CAPS）

## 2026-10-25 扩大仓库池 + token 接入 + README 按内核/日期取数

- **token 接入**（用户提供）：新增 `load_github_token()` 查找链
  `--token` → `GITHUB_TOKEN`/`GH_TOKEN` 环境变量 → 本地凭据文件
  `~/.workbuddy/data/free-nodes-tools/github_token.txt`（权限 600，不在仓库内，
  `.gitignore` 另加 `github_token.txt` 兜底）。实测配额 **核心 5000/时、搜索 30/分**
  （匿名是 60/时、10/分）。日志只打印 `前4…后4` 打码形式
- **仓库池扩大**：
  - `SEARCH_QUERIES` 10 组 → **26 组**，补上按内核（mihomo/xray）、按协议
    （hysteria2/tuic/reality/vmess/trojan/ss）、中文（免费机场/节点分享/订阅链接）、
    日更型（daily free nodes）四类
  - `search_repos()` 支持翻页：每页 100 条 × `--search-pages`（默认 2）
  - 限速按身份自适应：带 token 2.2s/请求，匿名 6.5s
  - `--max-repos` 30 → **80**，`--max-seeds` 15 → **30**
  - 阶段 2 时间窗从「前一天」放宽到 `--search-days`（默认前 **3** 天）
  - `seed_repos.json` 上限 80 → **300** 个仓库
- **README 按内核分类**：新增 `KERNEL_LINK_HINTS`，从文件名 → 目录名 → 链接文字 → 域名
  逐级识别 v2ray/xray/clash/singbox。识别出的节点写入对应内核文件时**豁免 CAPS 预筛**
  （作者已声明格式，CAPS 的保守规则可能把真能用的判死）
- **README 按日期筛选**：新增 `DATE_TOKEN_RE` / `DATE_HEADING_RE`，两种写法都认——
  链接自带日期（`.../2026-10-25/all.txt`、`Nodes-20261025.txt`）和有日期小标题
  （`### 2026-10-25` 下的链接，回溯 4000 字符取最近标题）。只取当天
  （`--readme-date-tolerance` 默认 0）。**整份 README 没提日期 → 全部保留**，
  否则非日更仓库会被一刀砍死。因日期跳过记 `-4` 状态，与「未声明链接」区分
- **补 sing-box 反解**（`singbox_to_uri()`）：旧代码对 `kind=singbox` 直接返回空串，
  导致 sing-box JSON 订阅的节点进不了 `nodes_uris.txt` 主清单 → **完全不参与可用性验证**。
  现覆盖 ss/trojan/vless/vmess/hysteria2/tuic 六种，其余返回 None

**验证结果**（隔离目录试跑，12 分 48 秒，不污染正式产物）：
- 搜索：26 组关键词 × 1 页 = 26 次请求，去重 **396** 个仓库（阶段 1）；
  阶段 2 放宽至 2026-10-22 起，去重 **689** 个仓库
- 日期筛选真实命中：`VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy` 有 **17 个链接
  因日期不是当天被跳过**，保留 10 个当天链接采到 255 条
- 主清单 7189 条 → v2ray 6841 / xray 7110 / clash 7167 / singbox 6953
- sing-box 反解：6 种协议往返一致（server/port 不变）；四内核原生校验
  vless(reality/ws)/vmess 全接受、hysteria2 只有 clash/singbox 能构造（符合能力边界）；
  端到端验证 sing-box 来源节点能进主清单与四个 sub 文件

## 2026-10-25 md 日志去重粒度修正

- **问题**：`upsert_section()` 按「日期前缀」删旧小节，同一天写第二条不同主题时，
  会把当天先写入的记录整段抹掉（本次差点丢掉「布局重构与内核检查」整节，已用 git 恢复）
- **改动**：加 `match_heading` 开关——`report/summary/health_check` 仍按日期替换（当天一份结论），
  `changelog/known_issue` 改为按「日期 + 标题」替换（一天多事件并存）

## 2026-10-25 修复仓库质量分倒挂

- **改了什么**：`collect_nodes.quality_score()`
  - 可用率 ≤0 或 `avg_latency` 为空时直接 `return rate*70`（延迟项 0），不再把「无数据」当满分
  - 延迟归零点 1500ms → 5000ms（`100 - latency/50`），让 30 分权重真正起作用
- **回填结果**（16 个仓库）：

  | 仓库 | 可用率 | 旧分 | 新分 |
  |---|---|---|---|
  | snakem982/proxypool | 61.9% | 43.3 | **63.8** |
  | Pawdroid/Free-servers | 65.0% | 45.5 | 54.9 |
  | 0xRadikal/Free-v2ray-Configs | 11.4% | 8.0 | 29.0 |
  | Epodonios/v2ray-configs | 2.6% | 13.9 | 26.4 |
  | igareck/vpn-configs-for-russia | 33.3% | 23.3 | 23.3 |
  | MatinGhanbari 等 5 个 0% 仓库 | 0.0% | 30.0 | **0.0** |

- **验证**：排序恢复单调（可用高的分高、0 可用的垫底）；`repo_sort_key` 未改动，
  采集优先级行为不变（仍按 `avail_rate`）
- 记录：`references/known-issues.md` 第 19 条；`SKILL.md` 质量分公式说明同步更新

## 2026-10-25 布局重构与内核检查

### 输出布局重构：扁平 + 单文件制

- **动机**：每内核产出 `pool_<core>.txt` / `_list.txt` / `.json` 三件套，验证后再产出
  `available_<core>.txt` / `_list.txt` / `_clash.yaml` / `_singbox.json` 四件套，大半是冗余
- **改动**：
  - 节点文件统一为 `v2ray_sub.txt` / `xray_sub.txt` / `clash_sub.yaml` / `singbox_sub.json`，
    一内核一文件、只写该客户端能直接导入的格式；`nodes_uris.txt` 作为内部主清单（全量明文 URI）
  - 可用清单统一为 `available_v2ray.txt` / `available_xray.txt` / `available_clash.yaml` /
    `available_singbox.json`，取消跨内核格式转换（xray 的 REALITY 节点转成 clash 配置不保真）
  - 池统一为 `pool/pool_<core>.<ext>` 四个文件 + 一份共享 `pool/pool_state.json`（只存元数据）
  - 全部平铺在 `free-nodes/` 根目录，**不再按日期建子目录**（过期节点没有意义）
  - 新增 `layout.py` 集中定义命名/格式/能力矩阵/路径，`collect_nodes`、`test_nodes`、`pool`、
    `uplink`、`health_check`、`check_kernels` 全部改为依赖它，不再各自硬编码文件名

### 四内核能力分流（layout.CAPS）

- v2ray 与 xray 共用同一份源订阅，但按「代理协议 / 传输层 / REALITY / flow」分流：
  带 REALITY、VLESS flow、xhttp 的节点只进 `xray_sub.txt`（v2fly 不支持，写进去会让整份配置导入失败）
- clash 额外收 ssr / hysteria2 / tuic，singbox 额外收 hysteria2 / tuic，各自缺 kcp/quic 的差异也按矩阵过滤
- 本日实测分流结果：主清单 6632 条 → v2ray 5633 / xray 6419 / clash 6615 / singbox 6529

### 内核命名归一

- 对外统一 `v2ray` / `xray` / `clash` / `singbox`；`mihomo`、`meta` → `clash`，`v2fly` → `v2ray`，
  `sing-box`、`sb` → `singbox`。此前同一个 mihomo 内核既有 `pool_mihomo.txt` 又有 `pool_clash.yaml`，
  两份内容一样、名字不同

### md 日志改为时间倒序累积

- `report.md` / `summary.md` / `health_check.md` / `known_issue.md` / `changelog.md` /
  `collection_log.md` / `review_log.md` 统一由 `layout.upsert_section()` 写入：
  新小节插到顶部，同一天重跑**替换**当天小节（不会堆叠重复），超过 30 个小节从尾部丢弃

### 新增 check_kernels.py（内核版本 + 能力漂移检查）

- 比对本地二进制版本与 GitHub 最新 release（XTLS/Xray-core、v2fly/v2ray-core、
  MetaCubeX/mihomo、SagerNet/sing-box）
- 用「协议 × 传输层 × 加密方式」样本跑内核原生校验，比对 accepted 集合与 `kernel_state.json` 基线
- 本日实测：v2ray 5.53.0 / xray 26.10.21 / clash(mihomo) 1.19.33 / singbox 1.14.4 均为最新，
  能力指纹 10/12/14/14 项与基线一致

### 修复：自检误判与计数偏差（3 处）

1. **`health_check.read_sub_stats()` 只认 base64** → 传进去的是明文 `nodes_uris.txt`，
   base64 解码得到乱码、过滤后 0 行，自检报「本次采集到 0 条节点」critical（实际 6632 条）。
   改为先看明文里有没有 `://`，没有再尝试 base64 解码
2. **sing-box 计数比汇总多 1** → `available_singbox.json` 里除了节点还有一个内置
   `{"type":"direct"}` 出站，被当成节点计入。改为排除 `direct/block/dns/selector/urltest/tor`
3. **v2ray 版本查询 404** → `v2fly/v2fly-core` 这个仓库名调 `/releases/latest` 返回 404，
   正确的仓库是 `v2fly/v2ray-core`（tag `v5.53.0`）

验证：修复后自检从「1 critical / 2 warn」降到「0 critical / 1 warn」，剩下一项是镜像失效（见 known_issue）。
