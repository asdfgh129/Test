# 第二窗口（23:45）执行记录

## 2026-10-27（首晚执行）

- 起点：首窗口已测 v2ray 1584 个（54 可用），xray/clash/singbox 因预算耗尽被跳过
- **修复**：`test_nodes.py` 新增 `--fair-budget` —— 内核顺序跑时按剩余内核数均分墙钟，
  避免第一个内核吃光预算（详见 known-issues #38、CHANGELOGS 同日条目、SKILL.md 参数表+第 7 条）
- 本窗口命令：`test_nodes.py --resume-tested --time-budget 3900 --fair-budget`
  （3900 而非 4800：准备+预筛已花掉约 10 分钟，按平台 90 分钟硬上限反推）
- 结果：四内核全部拿到当天数据 61/65/75/68（v2ray 576 测、xray 624、clash 792、singbox 840），
  全部 partial=true、exhausted=false
- 自检 0 critical / 2 warn（v2ray 累计可用率 2.8% 属排序尾部效应；镜像失效 10/13 为环境）
- 踩坑：`health_check.py` 跨零点默认写次日小节 → 必须显式 `--date <采集日>`（已入 SKILL.md）
- 发布：commit fe98b19 推送成功（v2ray @ 202.50.253.81:19999）
- **下一窗口要点**：继续 `--resume-tested --fair-budget`；`--date` 仍取 `Docs/summary.json` 的
  `2026-10-27`（采集日），自检也要带同一个 `--date`

## 2026-10-28（第二晚，本窗口没跑验证）

- **判断依据**：`Docs/summary.json` 四内核 `partial=false`，`sampled` 已达 2500 上限
  （2118/2159/2508/2509），首窗口 23:15 就测完了 → 按规则跳过续跑，只做自检+修复+发布
- **修 1（critical 归因）**：自检报「14/51 仓库下载失败（27%）」，日志却只有「下载失败」无原因。
  抽 2 个样本单点复现均为 **HTTP 404**（上游改路径），404 还会把镜像链全试完（单条 23~37s）
  - `collect_nodes.py`：`err_tag()` 出标签；日志记 `下载失败(HTTP 404)`；`fetch_url_text` 遇 404/410 立即 break
  - `health_check.py`：失败仓库 ≥60% 是 404/410 → 降级 warn（「上游路径失效」），无标签仍报 critical
  - 回归：404 样本 37s → **1.0s**，正常链接 6.6s 不受影响；合成日志三例全过
- **修 2（趋势误报）**：`今日 2744 vs 中位数 13021` 是口径错位（uniq 从采集总量变成了 TCP 过滤后发布量）。
  采集日志新增 `- TCP 过滤：…（采集总量 M 条）`，`health_check.collected_of()` 统一按 M 比较；
  今日日志已按 4187/6931 补行订正。自检 warn 6 → 5
- 自检结论：1 critical（本次采集早于标签机制，无法归因）/ 5 warn，其余为既定水位与环境
- 发布：commit `42a3315` → origin/master 成功（v2ray @ 202.50.253.81:19999）
- **给后续窗口的要点**：
  - 判断是否需要续跑只看 `Docs/summary.json` 的 `partial`，`exhausted=false` 但 sampled 已到 2500 属正常
  - 读采集日志时，「下载失败（HTTP 404）」= 上游路径失效，别去调镜像；节点量比对一律看「采集总量」
  - 本窗口追加的项目日志（`free-nodes/.workbuddy/memory/2026-10-28.md`）在发布之后写的，
    属未提交状态，下次发布自动带上
