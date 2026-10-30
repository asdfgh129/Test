---
name: free-nodes-collector
description: GitHub 免费节点每日采集与自检。用于每天跟踪 v2ray/xray/clash/sing-box 免费节点仓库的当日更新：读 README 跟随订阅链接、两级去重、按四内核能力分流成 4 个订阅文件、TCP 延迟排序、四内核实测可用性、跨天可用节点池、内核版本与能力漂移检查、采集后自检。触发词：收集今天的免费节点、更新节点订阅、采集 GitHub 免费节点、合并去重节点、检查采集是否有问题、免费节点每日任务。
agent_created: true
---

# free-nodes-collector — GitHub 免费节点每日采集

采集 GitHub 上有更新的免费节点仓库，合并、两级去重，**按四内核各自能力分流**，输出可直接导入客户端的订阅文件。链路：读 README → 按仓库质量排序采集 → TCP 延迟排序 → 跨天可用节点池 → 四内核实测 → 自检。

**产物不分日期**，按 `nodes/`（节点产物）、`Docs/`（文档与日志）、`src/`（脚本与采集状态）、`Skills/`（技能定义）四层存放；根目录只留 `README.md` 与 `CHANGELOGS.md`，每次运行覆盖更新。免费节点过期就没意义，留历史日期目录只会制造「看起来有、其实已死」的误导。

## 核心工作流

**三步：采集 → 验证 → 自检。**

内核检查必须和采集**在同一进程里跑**（`--check-kernels`）：内核检查要连 `api.github.com`，直连不通时得先自建代理，而内核子进程会随父进程退出被回收（本机 job 限制），**分步执行时前一步建的通道活不到下一步**。合并成一条命令后通道只建一次，日志里 `[uplink] 通道就绪` 只应出现一次；出现两次说明没复用，记进汇报。分步执行仍可用，每步会先尝试接管已登记通道，接管不到才自建（约 10~30 秒）。

```bash
# 1+2. 内核检查 + 采集（一条命令，代理只建一次；不加 --test，验证单独跑）
python <free-nodes>/src/collect_nodes.py --out <输出根目录> --readme-only --check-kernels \
  --max-repos 80 --search-pages 2 --search-days 3 --readme-date-tolerance 0

# 2b. 四内核可用性验证（全量策略；--time-budget 见下方「硬约束」）
python <free-nodes>/src/test_nodes.py --input <输出根目录> --cores v2ray,xray,clash,singbox \
  --full-below 3000 --max-test 3000 --time-budget <剩余秒数>

# 3. 自检：只诊断、不改动，输出待修复清单
python <free-nodes>/src/health_check.py --dir <输出根目录>

# 5. 发布（只暂存 free-nodes，不碰仓库里其他项目）
python <free-nodes>/src/publish_free_nodes.py --proxy auto --date <date +%F 的输出>
```

**参数名陷阱（踩过）**：`test_nodes.py` 用 `--full-below` / `--max-test` / `--time-budget`（**不带** `--test-` 前缀）；`--test-full-below` / `--test-max-test` 是 `collect_nodes.py` 的透传名，传给 `test_nodes.py` 会直接报错退出。

**退出码**：`health_check.py` 0 健康 / 1 有告警 / 2 有严重问题。`collect_nodes.py` 0 正常 / 3 本次采到 0 条但**保留旧结果**（不写空文件，查配额与网络后重跑）。`test_nodes.py` 非 0 不要整轮重跑，先看日志——已测结果通常已落盘。

**纯 Python 标准库实现，无需安装任何依赖。**

## 硬约束（平台行为，任务内部改不掉）

| 约束 | 数值 | 正确应对 |
|---|---|---|
| 单次运行墙钟上限 | **90 分钟**（超时报 `[CANCELLED] Run timed out`） | 传 `--time-budget` 主动收尾，不要压缩测试量 |
| `--time-budget` 取值 | `5400 - 已用秒数 - 600`（给自检+发布留 10 分钟） | 先 `date +%s` 记开始时刻再算 |
| 多窗口续跑 | 22:00 采集+验证 / 23:45 续跑 / 01:30 再续跑 | 后续窗口加 `--resume-tested`，**首窗口绝对不能加** |
| 内核顺序跑，首个内核吃光预算 | 实测首窗口 v2ray 吃满 2321s，其余三内核零数据 | 第二/第三窗口加 `--fair-budget` 均分墙钟 |
| 增量落盘 | 每内核测完立即写 available / summary / 池 | 被强杀只丢当前内核，不会新旧混排 |

**测试量不设人为上限**：`--max-test` 一律给 3000（全量策略上限）。不要因为「怕超时」自行降到 1000 或 600——那些数字是拍脑袋估的，与实测吞吐对不上，压了反而白少测一批。

## 关键口径（结论，理由见参考文件）

- **探测地址用裸域 HTTPS**：默认 `https://gstatic.com/generate_204`。不能带 `www`（会命中国内缓存节点、直连就返回 204、毫无区分度），不能用明文 HTTP（可被篡改、且触发宿主明文确认弹窗打断自动化），必须走代理。
- **超时 3s、并发 24**：实测单节点 p50=1.39s / p90=1.87s，3s 只误杀 2.5%；复测收益仅 1.7% 而吞吐腰斩，故 `--retry` 默认 0。
- **只发布 TCP 可达节点**：`tcp_latency = null` 的整条丢弃（`--keep-dead` 可保留）。实测 16620 条里仅约 6800 条可达，留在订阅里只撑大文件还拖慢验证。
- **Cloudflare 前置节点整体降权**：握手 10-40ms 但回源多是死的，排在真实可达节点之后、不可达之前（否则采样 200 个只通 0-3 个）。
- **验证不跟随重定向**：3xx 直接判不可用，只认 2xx。跟着跳等于替节点访问陌生域名，既暴露本机 IP 也可能触发网络拦截弹窗。
- **每内核可用数个位数到十几个是免费节点的正常水位**，不要为数字好看换回 `www.gstatic.com` 或明文 HTTP。

## 产物

| 位置 | 内容 |
|---|---|
| `nodes/*_sub.*` | 四内核订阅：`v2ray_sub.txt` / `xray_sub.txt`（base64）、`clash_sub.yaml`、`singbox_sub.json` |
| `nodes/nodes_uris.txt` / `nodes_meta.json` | 全量唯一节点主清单 / 每节点延迟 + 来源仓库（验证取样与仓库质量依据） |
| `nodes/available_*` | 验证后的可用清单，与上面四件一一对应 |
| `nodes/pool/` | 每内核一个池文件 + 共用 `pool_state.json`（跨天累积，可直接导入） |
| `nodes/tested_state.json` | 本日已测进度，供后续窗口 `--resume-tested` 续跑 |
| `Docs/` | `report.md`、`summary.md/.json`、`health_check.md/.json`、`known-issues.md`（知识库 + 末尾自检区块）、`collection_logs.md`、`review_logs.md`、`protocol.md`、`proxy.md`、`sources.md`、`tools-setup.md` |
| 根目录 | `CHANGELOGS.md`（按日期倒序，同天同标题替换） |
| `.workbuddy/memory/` | 项目记忆，纳入 git 跟踪 |

`collect_nodes.py` 一条命令自动串完：搜索当天更新仓库 → 读 README 取订阅链接 → 挑候选文件 → 下载解析 → 两级去重 → TCP 延迟探测排序 → 按四内核能力分流写出 4 个订阅文件 + 节点元数据 + 报告。

完整文件清单见 `references/09-outputs.md`。

## 运行后必做

0. 跑 `health_check.py`，有 critical/warn 按下方修复闭环处理
1. 读 `Docs/report.md`、`collection_logs.md`、`summary.md`、`health_check.md` 的**第一小节**（时间倒序，最新在最前）汇报
2. 提示用户：免费节点时效极短，当天导入当天用；只要低延迟精品直接导入 `nodes/pool/pool_<core>.<ext>`
3. 结果为 0 条时查网络与 GitHub 限额（匿名搜索 10 次/分、核心 60 次/时），建议配 token 重试

**配额一行的读法**：`health_check` 的「GitHub 配额剩余」现在带身份标注——
`（已配置 token ghp_…x6hY）` 表示走的是凭据文件里的 token（核心 5000/时），
`（匿名）` 表示没有任何凭据（60/时）。**`limit` 字段就是身份的指纹**：60 = 匿名桶、5000 = token 桶，
两者混杂说明取数身份和干活身份不一致（第 45 条就是这么被抓到的）。
身份判断一律调 `collect_nodes.load_github_token()`，不要在别处再写 `os.environ.get("GITHUB_TOKEN")`。

## 故障排查（修复闭环）

1. 读 `Docs/health_check.md` 的待办清单，取最靠前的 critical
2. 对照 `Docs/known-issues.md` 找同类症状（多数问题那里已有答案，条目按编号，第 31/36/37/38 条与多窗口、超时、预算均分相关）
3. 抓 **1 个失败样本**（仓库 / URI / 内核）单独复现，不要靠猜
4. 改脚本并用该样本单点回归；解析类问题重跑采集，验证类重跑 `test_nodes.py`
5. 再跑 `health_check.py`，确认 finding 消失且未引入新问题
6. 记录：`Docs/known-issues.md` 上方知识库按编号追加（现象/根因/修复/教训）、根 `CHANGELOGS.md` 按日期倒序写小节、观察项写 `Docs/review_logs.md`；行为有变化同步更新本文件
7. 提交推送（只暂存 free-nodes）

只改有证据支撑的地方。成片 `config` 是转换器有 Bug，成片 `unsupported` 是能力矩阵要对齐内核，都不代表节点质量下降。

**失败归因与数字口径（2026-10-28 起）**：
- 采集日志里 `- repo：下载失败（HTTP 404）`：**先怀疑自己拼的 URL，再怀疑上游**。
  GitHub「复制链接」给的是 `raw.githubusercontent.com/<o>/<r>/refs/heads/main/<path>`，
  解析漏掉 `refs/heads` 就会拼出 `heads/main/...` → 必然 404（known-issues 第 43 条，一天白丢约 2 万条候选）。
  确认上游是否真失效，最短路径是把 README 原文打出来和我们的请求地址比对。
  不带括号的是老日志，要自己抓样本确认。自检对「失败仓库里 ≥60% 是 404/410」降级为 warn（第 42 条）
- 采集日志里 `- repo：0 条（3/10 个链接下载失败，其余已下载但解析不到节点）`：原因是**下载**不是解析，
  自检把它计入 `pfail` 桶，不要按「解析能力不足」去改格式覆盖
- **「下载成功但 0 条」先看正文有没有 `#` 订阅头**（第 47 条）：`#profile-title` / `#subscription-userinfo`
  挡在 sing-box JSON 前面会让 `json.loads` 直接失败、兜底当纯文本抽 URI → 必然 0 条。
  `_strip_leading_comments()` 已处理；若又见 0 条，先打正文前 200 字符确认格式，别再往「文件太大/网络慢」上猜
- **仓库质量闸门只按「实测 ≥20 且可用 0 个」跳过**（第 46 条）：不要恢复「可用率 < 2% 也跳」的判据，
  大仓库可用率天生 0.5%~1.3%，按率切会把每天 18% 的可用节点砍掉
- **外部订阅链接已带一次重试（2026-10-29 起，第 44 条）**：`URLError`（连接重置/拒绝/DNS 抖动）、
  `429`、`5xx` 会整链再走一次（429 尊重 `Retry-After`，封顶 3s）；**`404/410` 与「超时」不重试**
  （前者是死链快失败的成果，后者会翻倍单仓 90s 预算）。所以日志里还出现 `下载失败(URLError)`
  = 已经重试过一次仍然失败，属真不可达，不要再怀疑重试次数不够
- 看节点量一律看采集日志的 `- TCP 过滤：丢弃不可达 N 条（采集总量 M 条），保留 K 条`：
  **M 才是和历史可比的口径**，K 是发布量（10-28 起默认只发 TCP 可达节点），拿 K 跟历史比会误判减产

## 参考文件索引（按需读，不要一次全读）

细节都在 `Skills/free-nodes-collector/references/` 下。**一律按下面的绝对路径读**，不要按 `references/xxx.md` 相对路径解析——宿主技能目录 `~/.workbuddy/skills/free-nodes-collector/` 里的 `references` 软链指向 `Docs/`，相对解析会找错地方。只在遇到对应场景时读：

根路径：`C:\Users\bemin\WorkBuddy\Test\free-nodes\Skills\free-nodes-collector\references\`

| 什么时候读 | 文件 |
|---|---|
| 要调参数、查某个开关的默认值与含义 | `01-params.md` |
| README 一条链接都没识别到 / 候选文件挑错 / 下载老失败 | `02-collect-internals.md` |
| 想理解仓库质量分怎么算、延迟排序为何这样排、池怎么复用淘汰 | `03-quality-and-pool.md` |
| 某内核「全死」、要改能力矩阵、内核升级要查漂移 | `04-core-caps.md` |
| 验证口径、失败分层、取样排序、协议回归、重定向弹窗 | `05-verify.md` |
| GitHub 直连不通、代理建不起来、推送失败 | `06-uplink-publish.md` |
| 自检各项触发条件与完整修复闭环 | `07-healthcheck.md` |
| 节点数不足要扩量、去重规则、搜索关键词与黑名单 | `08-expansion.md` |
| 产物文件全表与目录职责 | `09-outputs.md` |
