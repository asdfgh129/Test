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

## 2026-10-29（第三晚，本窗口没跑验证）

- **判断依据**：`Docs/summary.json` 四内核 `partial=false`、`sampled` 已达上限
  （2502/2503/2506/2503），首窗口 23:08 测完 → 跳过续跑，只做自检+修复+发布
- **修 1（warn 有证据）**：自检报 `crashgfw/free-airport-nodes` 0 条（历史 1050，部分链接下载失败）。
  归因不是解析也不是 URL 拼错：该仓库 9 条链接全在同一域名 `ndxy.fn0821.xyz/nodes/<hex>`，
  采集时整体不可达；窗口内单点复现 0.3~0.8s 全 200、每条 8860B、正常解出 30 节点。
  根因 = `fetch_url_text` 固定 `retries=0`，一次瞬时失败就整仓归零
  - `collect_nodes.py`：`RETRYABLE_HTTP={408,425,429,500,502,503,504}` + `_retryable_fetch_error()`；
    原逻辑收成 `once()`，瞬时失败整链再走一次（只 1 次，429 尊重 Retry-After 封顶 3s）
  - **404/410 与「超时」明确不重试**：前者是第 42 条死链快失败成果，后者会把单仓 90s 预算翻倍
  - 回归 4 例（正常/连接重置/404/超时）+ 整仓 10 链接回归全过
- 自检 0 critical / 5 warn；可用率 1.2%/2.9%/2.0% 与 10-28 同水位，镜像失效 10/13 属环境
- 发布：commit `ab6395d` → origin/master 成功（v2ray @ 202.50.253.81:19999）
- **给后续窗口的要点**：
  - 日志里出现 `下载失败(URLError)` 现在是「**已重试一次**仍失败」，别再怀疑重试次数不够
  - `MAX_README_LINKS=10` 会截断链接多的仓库（该仓库 17 条只跟 10 条），已知未改，
    要动先统计「被截断仓库的实际产出」，别直接放宽（会挤占单仓 90s 预算）
  - 该域名有 AAAA 但本机 IPv6 不通；若再出现「偶发全 URLError + IPv4 正常」，先查本机 IPv6 路由

## 2026-10-30（第四晚，本窗口没跑验证；修了两处采集侧缺陷）

- **判断依据**：`Docs/summary.json` 四内核 `partial=false`、`sampled` 到 2500 上限
  （2502/2505/2507/2506），首窗口 23:00 测完 → 跳过续跑
- **修 1（空正文当成功）**：gh-proxy/jsDelivr 边缘对 688KB 文件返回 `200 + 0 字节`，
  `http_get` 只看 `resp.read()` 不看长度 → 回退链第一跳就"成功"返回空串，
  日志变成「下载成功但解析不到节点」。第一窗口因此下错结论（"上游文件为空"）。
  加 `EmptyBody` + `err_tag` 的 `空响应` 标签，空响应不整链重试
- **修 2（外链默认走上行通道）**：通道只为翻 github 而建，却被当所有外链的默认出口。
  同一节点对 github 通、对 `ndxy.fn0821.xyz` TLS 掐断（5/5 失败，直连 5/5 成功）。
  非 GitHub 域名改直连优先 + 通道兜底；镜像/jsDelivr 腿固定直连
- 自检 0 critical / 5 warn；发布 commit `b9da0fc` → origin/master 成功
- **给后续窗口的要点**：
  - 看到 `下载失败(空响应)` = 所有通道都给空体，不是解析缺陷；别再判"上游为空"
  - 「下载成功但 0 条」的第一步永远是**量正文长度**，0 字节是通道问题
  - 直连优先引入的风险（透明劫持返回 200 HTML）已记 review_logs，出现再处理，别预先加嗅探
  - 本窗口跨零点，`--date` 用采集日 2026-10-30，不用 `date +%F`
  - `--out` 指向全新目录时 `write_nodes_meta` 会因缺 `nodes/` 子目录报 FileNotFoundError
    （冒烟时撞到，生产路径不受影响，未改）

## 2026-10-31（第五晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」（2506/2505/2507/2503，cap 2500），首窗口 23:01 已跑完
- 本窗口未占用验证资源、未重跑自检；只做尾巴清理
- 尾巴：`free-nodes/.workbuddy/memory/` 两个文件是第一窗口发布后写入的（无 pending-push.json、
  无 ahead 提交）→ 补一次 publish 收干净，commit `4fd578e` → origin/master 成功
  （v2ray @ 202.50.253.81:19999，通道第 1 次命中）
- 本日可用数：v2ray 54 / xray 122 / clash 60 / singbox 55（属正常水位）
- **给后续窗口的要点**：GATE: done 时先看 pending-push 与 `git status --short` 里 free-nodes 有无改动；
  本窗口写自动化 memory 又会产生同样的小尾巴，属正常，下次发布自动带上，不必反复补推

## 2026-11-01（第六晚：GATE: done，未跑验证，也没补推）

- 闸门退出码 0：四内核均「已测满单轮上限」2509/2506/2509/2506（cap 2500），summary 生成于 23:35
- 尾巴检查：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` 无输出；
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无补推动作，本窗口零 git 操作
- 本日可用数：v2ray 48 / xray 120 / clash 56 / singbox 63（正常水位）
- 结论：今晚首窗口一次跑完，第二窗口纯兜底空转，未占用验证资源
- **给后续窗口的要点**：`rev-list --left-right --count origin/master...HEAD` 比 git status 更能确认「已推送」，
  两处都干净就真的什么都不用做；本次没写 free-nodes 内任何文件（只写了本文件），下次发布才会带上这个尾巴

## 2026-11-02（第七晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」2507/2509/2508/2507（cap 2500），summary 生成于 22:47:27
- 本日可用（ok）：v2ray 26 / xray 53 / clash 47 / singbox 50；四内核 `partial=false`、`exhausted=false`
  （候选 4068/4088/4854/4685 远大于 2500，属「达 cap」而非「测完池子」，与既往一致）
- 尾巴检查：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` 无输出；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD 停在 b03ee67）
- 本窗口零验证、零自检、零修复；只写了本 memory 文件（它在 free-nodes/.workbuddy 下且**被 git 跟踪**），
  为免第三窗口看到脏工作区误判为「待补推」，主动 publish 一次收干净 → commit `340720c` 推送成功
  （xray @ 202.50.253.81:19999，首轮命中）；推后 `git status` 干净、ahead/behind = 0/0
- **给后续窗口的要点**：`free-nodes/.workbuddy/**` 是入库的（只有根 `/.workbuddy/` 被忽略），
  所以本自动化每次写 memory 都会产生一个真实改动；要么当次 publish 收掉，要么明确知道下次会带上

## 2026-11-03（第八晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」（2507/2509/2507/2506，cap 2500），summary 生成于 22:45:44
- 本日可用（ok）：v2ray 30 / xray 74 / clash 51 / singbox 46（正常水位）；四内核 `partial=false`、`exhausted=false`
  （候选 4049/4034/4814/4677 远大于 2500，属「达 cap」而非「测完池子」）
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD a33db82）；
  但 `git status --short -- free-nodes .github` 有两项：第一窗口 automation memory（M）+ `free-nodes/.workbuddy/memory/2026-11-03.md`（??）
- 按 11-02 的做法：先写本文件、再一次 publish 收干净（只暂存 free-nodes/.github，不碰用户 C++ 项目）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）
- **给后续窗口的要点**：闸门 done 时 `git status` 里出现 `.workbuddy/memory/**` 一般就是自动化自己写的尾巴，
  属预期；确认 `rev-list` 是 0/0 即可放心 publish，不会带出验证数据

## 2026-11-04（第九晚：GATE: done，未跑验证，零 git 操作）

- 闸门退出码 0：四内核均「已测满单轮上限」（2509/2508/2509/2507，cap 2500），summary 生成于 22:35:26
- 本日可用（ok）：v2ray 29 / xray 71 / clash 48 / singbox 56（正常水位）；四内核 `partial=false`、`exhausted=false`
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` 无输出；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD a4eeafd）
- 写本文件后又出现一项 `M free-nodes/.workbuddy/memory/automations/a4c4ae9d…/memory.md` → 按 11-02/11-03 做法
  publish 一次收干净，本窗口零验证、零自检、零修复
- **关键澄清（此前误判过两次）**：根 `.workbuddy` 是 junction → git 实际跟踪的是 `free-nodes/.workbuddy/**`，
  所以 `git check-ignore <根路径>` 会命中 `/.workbuddy/`、`git ls-files <根路径>` 会报 "not tracked"，
  **但 `git status` 报的是真实的 `free-nodes/.workbuddy/...` 路径且确实被跟踪**。
  → 判「要不要 publish」只认 `git status`，不要用 check-ignore/ls-files 的根路径结论反推为「没改动」

## 2026-11-05（第十晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」（2509/2510/2508/2507，cap 2500），summary 生成于 22:36:08
- 本日可用（ok）：v2ray 18 / xray 44 / clash 23 / singbox 26 —— 较 11-04 的 29/71/48/56 齐降约 40%，
  第一窗口已做四点取证（候选规模、失败分布、池复测、单核耗时）判为上游波动，未调参
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0（HEAD e387672）；
  `git status --short -- free-nodes .github` 有两项：第一窗口 automation memory（M）+ `2026-11-05.md`（??）
- 按 11-02 起的一贯做法：写完本文件后 publish 一次收干净；本窗口零验证、零自检、零修复
- **给后续窗口的要点**：可用数单日腰斩不必立刻怀疑代码——先看第一窗口日志里有没有做过取证；
  本日属上游波动（候选 3665/3811/4396/4262 与失败分布均正常），第三窗口若同样 GATE: done 直接跳过即可

## 2026-11-06（第十一晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」2509/2506/2508/2508（cap 2500），采集日 2026-11-06、summary 生成于 22:37:04
- 本日可用（ok）：v2ray 14 / xray 69 / clash 26 / singbox 21；四内核 `partial=false`、`exhausted=false`
  （候选规模远大于 2500，属「达 cap」而非「测完池子」）。v2ray 14 偏低但仍在 min_available(10) 之上，属源池波动
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0（HEAD 8b5fc53）；
  `git status --short -- free-nodes .github` 两项，均为自动化 memory 文件（第一窗口的 2026-11-06.md + 主窗口 a3d7bb22 memory）
- 按 11-02 起的一贯做法 publish 一次收干净 → commit `e809448` → origin/master 成功（v2ray @ 202.50.253.54:19999，第 1 次命中）；
  推后 status 干净、ahead/behind = 0/0、无 pending-push
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）
- **给后续窗口的要点**：GATE: done 时若 `git status` 里只有 `.workbuddy/memory/**`，就是自动化自己写的尾巴，
  publish 一次即可；本次 publish 既收了第一窗口的尾巴，也顺带把本文件纳入同一提交，无需二次补推

## 2026-11-07（第十二晚：GATE: done，未跑验证）

- 闸门退出码 0：四内核均「已测满单轮上限」2511/2507/2511/2508（cap 2500），采集日 2026-11-07、summary 生成于 22:35:57
- 本日可用（ok）：v2ray 31 / xray 78 / clash 24 / singbox 24（正常水位）；四内核 `partial=false`、`exhausted=false`
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0（HEAD 77cb4bb）；
  `git status --short -- free-nodes .github` 两项，均为自动化 memory（第一窗口的 2026-11-07.md + 主窗口 a3d7bb22 memory）
- 第一窗口本日已发两次（34fe3ec 28 文件 + 77cb4bb 观察补记），验证与自检均在首窗口完成，0 改动
- 本窗口零验证、零自检、零修复；只 publish 一次收掉 memory 尾巴（commit 哈希见当晚汇报）
- **给后续窗口的要点**：本文件故意不写自己的 commit 哈希（否则又会造出新尾巴）；
  哈希只在汇报里给。查历史提交用 `git log --oneline -- free-nodes/.workbuddy`

## 2026-11-08（第十三晚：GATE: done，未跑验证）

- 闸门退出码 0：v2ray「候选已全部测完」(2142/2131)、xray「候选已全部测完」(2499/2494)、
  clash「已测满单轮上限」(2511/2500)、singbox「已测满单轮上限」(2506/2500)；
  采集日 2026-11-08、summary 生成于 22:36:22
- 本日可用（ok）：v2ray 29 / xray 80 / clash 42 / singbox 45（正常水位）；四内核 `partial=false`
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD 4537be9）；`git status --short -- free-nodes .github` 两项，均为自动化 memory
  （2026-11-08.md 新增 + 主窗口 a3d7bb22 memory 修改）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；只 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：v2ray/xray 本日 `exhausted=true`（池子真测完，2131/2494 < cap 2500），
  与 clash/singbox 的「达 cap」成因不同但闸门口径一致，都不需要续跑；别因为 exhausted=true 就想去补测

## 2026-11-09（第十四晚：GATE: done，未跑验证）

- 闸门退出码 0：v2ray「候选已全部测完」(2309/2298)、xray「已测满单轮上限」(2505/2500)、
  clash「已测满单轮上限」(2509/2500)、singbox「已测满单轮上限」(2505/2500)；
  采集日 2026-11-09、summary 生成于 22:37:49
- 本日可用（ok）：v2ray 24 / xray 88 / clash 50 / singbox 42（正常水位）；四内核 `partial=false`
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD 8e3b3d1 已是今日提交）；`git status --short -- free-nodes .github` **无输出**（比前几晚更干净，
  第一窗口未留 memory 尾巴，今日也没有 `free-nodes/.workbuddy/memory/2026-11-09.md`）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后只 publish 一次收掉尾巴
- **给后续窗口的要点**：`git status` 全空时仍要 publish —— 因为本文件（automation memory）本身被跟踪，
  写完就产生改动；判定顺序永远是「先看 status/rev-list 再写文件」，写之前那份干净结论才是第一窗口的真实状态

## 2026-11-10（第十五晚：GATE: done，未跑验证）

- 闸门退出码 0：v2ray「候选已全部测完」(2261/2254)、xray「已测满单轮上限」(2504/2500)、
  clash「已测满单轮上限」(2508/2500)、singbox「已测满单轮上限」(2504/2500)；
  采集日 2026-11-10、summary 生成于 22:35:35
- 本日可用（ok）：v2ray 24 / xray 55 / clash 33 / singbox 45（正常水位，均在 min_available 10 之上）；
  四内核 `partial=false`
- 开工前 taskkill 四内核均「没有找到进程」→ 第一窗口正常收尾，无残留
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD b5a4887 已是今日提交）；`git status --short -- free-nodes .github` 仅一项
  `M free-nodes/.workbuddy/memory/automations/a3d7bb22…/memory.md`（主窗口自己的 memory）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉尾巴
- 观察：singbox 今日失败原因以 `reset` 占绝对多数（1915/2504），与既往以 `timeout` 为主不同，
  但可用数 45 属正常水位、未触及任何阈值，故未动参数；若连续多日如此再取证（记入 review_logs 更合适）
- **给后续窗口的要点**：singbox `reset` 突增但 ok 正常时属上游/DNS 层面波动，不要因为失败原因分布变了就调超时

## 2026-11-13（第十六晚：本窗口整晚空转，第一窗口同时在跑，未占用验证资源）

- **异常背景**：本地 11-11、11-12 两晚窗口**都没触发**（`_test_2026111*.log` 全无，summary/available_* 停在 11-10 22:3x），
  但远端 CI 四晚全成功（`038324c`/`6f409a1`/`a75934c`/`f80af2c`），cron 持续拖到次日 04:17~04:52 才跑。
  → 订阅实际停在 11-10 三天，属「本机没跑」而非「CI 停摆」
- **闸门第一次（09:27，旧版 window_gate）**：`GATE: done`，采集日却是 **2026-11-10** —— 旧闸门不看日期，只信 summary 内容，
  这正是「一晚没跑就永久空转」的坑。第一窗口已修复（`window_gate` 加新鲜度判定，commit `66ebd96`，
  known-issues 61），改完用今日 summary 复跑 → `GATE: done（采集日 2026-11-13，四核 2504/2500、1371/1366、2283/2280、1674/1669）`
- **并发事故（本次最重要教训）**：本窗口 09:35 起了 `--probe-only`，同时第一窗口（a3d7bb22）也在跑同一套流程
  → **两个 probe 同时写 nodes_meta/nodes_uris**。发现后用 `Get-CimInstance Win32_Process` 看到第一窗口的
  `test_nodes.py` 已在 09:48 开跑，立即 kill 本窗口的 probe（PID 8676），改为让路，全程未起第二份验证。
  **以后开工前必须先查 python 进程命令行**（不能只看 taskkill 四内核），否则会双验证互抢端口/CPU
- **本窗口实际动作**：`--sync-only --proxy auto`（一次成功，拉回三晚沉积 → `f80af2c`）；
  `health_check --date 2026-11-13`（0 critical / 5 warn：四核可用率 0.2/0.5/0.1/0.1% + 镜像 10/13）；
  **未发布**（第一窗口仍在跑，避免并发发布冲突）
- **本日验证结果（第一窗口跑出）**：v2ray 兼容池内复测共 3896 测、可用 7；xray 7/1371；clash 3/2283；singbox 1/1674
  —— 全部低于 `min_available=10`，较 11-10 的 24/55/33/45 大幅下降。失败分布 timeout 67% + tls 29%（v2ray）、
  singbox `reset` 1187/1674。**与用户 11-11 的 WIP（多目标探测主判据 5 目标 + 带宽测试 + 弹性配额 cap 1366/2280/1669）首日重合**，
  未改任何参数，留观察
- **风险登记（发布前必须知道）**：用户 11-11 15:39~16:25 有未提交 WIP（collect_nodes/test_nodes/pool/layout +
  新文件 `src/repo_pool.py`，约 856 行），而 `publish_free_nodes.py` 走 `git add --all free-nodes`
  → **发布会把这些未完成改动一起提交推送，CI 次日就按 WIP 代码跑**。已确认五文件均可编译、`repo_pool` 可导入；
  要避免只能发布时排除 `free-nodes/src/*.py`（脚本目前无此开关，需要用户定夺）
- 本地已有 1 个未推送提交（`66ebd96` 闸门修复），待第一窗口发布时一并带上
- **给后续窗口的要点**：① 开工顺序改成「taskkill 四内核 → **查 python 进程** → 再跑闸门」；
  ② 闸门 done 也要看 `summary.generated_at` 是不是今天，不是就按 continue 查到底为什么没跑；
  ③ 发布前先 `git status --short -- free-nodes/src`，一旦有 M/?? 就先问清楚（无人值守时宁可只提交产物路径）

## 2026-11-12 的第二窗口 → 实际 2026-11-13 09:26 才补触发（GATE 由 done 改判为 continue，修了闸门）

- 本会话 11-12 00:07 起过一次（未落盘任何动作），11-13 09:26 被「请继续执行任务」唤醒；
  期间 11-11、11-12 两晚三个窗口**都没跑**（`_test_20261111/12.log` 不存在，`available_*`/`summary.json`
  全停在 11-10 22:3x），远端 CI 正常（`038324c`/`6f409a1`/`a75934c`/`f80af2c`）⇒ 本机休眠，非 CI 故障
- **闸门第一跳骗了人**：`window_gate.py --input …` 输出「采集日 2026-11-10 … GATE: done」。
  按内容判对、按日期判错——summary 只在本地跑过验证时才更新，停跑几晚后每天都拿旧的回 done。
  **修**：加 `_date_fresh()`，未给 `--date` 时「今天」才认可、「昨天且 <06:00」认可（跨零点窗口），
  否则 continue 并打印过期天数。回归纯函数 6 例 + CLI 7 例全绿；真实仓库同命令由 done → continue。
  文档同步 known-issues 61 / CHANGELOGS / automation-prompt / SKILL.md。commit `66ebd96`（本地，未推送）
- 修完闸门结论：`GATE: continue（summary 过期 3 天）`，但本窗口**仍不跑验证**——同时刻第一窗口
  正在 `collect_nodes.py --probe-only`（09:30 起，且有两个并发探测进程 128/256 workers 各一），
  再起验证会让结果全不可信。也**不发布**：并发窗口正在做 sync/probe/publish，避免 git 竞争
- 新情况（需盯）：CI 采集量 11-11 起涨 10 倍，11-13 去重 117,782（原始 237 万），
  `nodes_uris.txt` 11.8 万行，与 `--max-test 2500` 比例 1:32~1:46；`--probe-only` 探 11.8 万条最坏 ~23 分钟，
  会打乱第一窗口时间账。要控量走「单仓产量上限」（11-11 未提交改造里的 `--max-nodes-per-repo`），
  别降探测并发/放宽口径
- 工作区另有 11-11 下午未提交改造（`src/repo_pool.py` + 单仓产量上限 + 多目标/带宽测试，约 856 行），
  编译通过、未跑真实采集；`publish_free_nodes.py` 走 `git add free-nodes`，发布会把它一起带上
- **给后续窗口的要点**：① 闸门现在自带日期校验，stop 掉「done 但没跑」的假象；
  ② 先看 `Get-CimInstance Win32_Process` 里有没有别的窗口在 probe/test，别起第二份验证；
  ③ 本机 sleep 会让整晚窗口全丢，CI 数据不会丢，但订阅会停在旧日期——恢复后应优先补一次验证+发布

## 2026-11-13 晚（第十七次记录：GATE: done，未跑验证）

- 开工前：taskkill 四内核均「没有找到进程」；`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 无结果
  → 本机无并发窗口、无残留（沿用 11-13 上午的「先查进程再跑闸门」顺序）
- 闸门退出码 0：采集日 **2026-11-13（生成于 22:47:01）**，四核均「已测满单轮上限」2513/2504/2511/2510（cap 2500）
  → 停掉上午那次「summary 停在 11-10」的异常，本机流程已恢复正常节奏
- 本日可用（按 `nodes/available_nodes.json` 去重 74 条）：v2ray 17 / xray 54 / clash 32 / singbox 38，正常水位
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` 无输出；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD `a2b1aae`，今日第三次发布）
- 上午登记的「用户 11-11 未提交 WIP（repo_pool.py 等 856 行）」已被今日发布一并入库
  （`src/repo_pool.py` 已 tracked，`62627c0` 带入），风险条目可关闭
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：`available_v2ray.txt` / `available_xray.txt` 是 **base64 订阅包**（整文件一行、无 `\n`），
  `wc -l` 会给出 0 或 1，别据此判「可用数为 0」；要数条数就 `base64 -d` 后数行，或直接读 `available_nodes.json` 的
  `cores` 字段（clash 在 `available_clash.yaml` 的 `proxies`、singbox 在 `available_singbox.json` 的 `outbounds`，
  文件名后缀各内核不同）

## 2026-11-15（第十八次记录：GATE: done，未跑验证；首窗口耗时超标把后两窗自动打开）

- 开工前：`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 无结果、四内核无残留 → 无并发窗口
  （沿用 11-13 的「先查进程再跑闸门」顺序；本次**没有跑 taskkill**，因为闸门 done 本窗口不启动验证，
  盲杀反而有风险）
- 闸门退出码 0：采集日 **2026-11-15（生成于 23:00:43）**，四核均「已测满单轮上限」2510/2505/2505/2507（cap 2500）
- 本日可用（summary.ok）：v2ray 21 / xray 52 / clash 36 / singbox 17，均高于 `min_available` 10，正常水位。
  候选池 6463/6129/8446/8161 远大于 cap ⇒ `exhausted=false` 属「达 cap」而非「测完池子」
- **今晚与既往不同的一点**：首窗口 `elapsed_min=53.6 > 50`，`window_gate --first-window` 把
  `Docs/window_switch.json` 从 off 翻成 **on**（reason「今晚验证耗时 53.6 分钟 > 50 分钟上限，窗口吃紧」），
  于是本窗口被真正启用；但四核内容判定全 done ⇒ 启用了也没活干，属开关只判「耗时/断档」、内容另判的正常组合。
  若 11-16 首窗口回到 ≤50 且 done，开关会再次自动关闭（连续 7 晚计数的 streak 已被今晚打断，需重新累积）
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0（HEAD `43a8a3a`）；
  `git status --short -- free-nodes .github` 两项：主窗口 a3d7bb22 的 memory（M）+ `Docs/window_switch.json`（M，
  即上面那次开关翻转），均为自动化自身产物，不含验证数据
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收干净
- **给后续窗口的要点**：`Docs/window_switch.json` 每晚会因 `--first-window` 判定而变动，它是入库文件，
  所以首窗口只要跑过、第二窗口几乎必然看到它 M —— 属预期尾巴，别当成「第一窗口没发布」的证据；
  真正的未发布信号只看 pending-push.json 与 `rev-list` 的 ahead 数

## 2026-11-16（第十九次记录：GATE: done，未跑验证；首窗口 46.8 分钟回到上限内，但开关仍 on）

- 开工前：`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 无结果 → 无并发窗口、无残留；
  未跑 taskkill（闸门 done 本窗口不启动验证，盲杀无意义）
- 闸门退出码 0：采集日 **2026-11-16（生成于 22:54:57）**，四核均「已测满单轮上限」
  v2ray 2507/2500、**xray 1447/1445**、**clash 2094/2088**、singbox 2505/2500
  → 注意 xray / clash 的 cap 已不是 2500，而是弹性反推值 1445 / 2088（用户弹性配额在生效），
  闸门口径按各自 cap 判，**别看到 1447 < 2500 就以为没测完**
- 本日可用（summary.ok）：v2ray 20 / xray 74 / clash 72 / singbox **120**；四核 `partial=false`、`exhausted=false`
  - singbox 120 是历史新高（既往 17~63），xray 74 / clash 72 也偏上；无异常迹象，未取证未调参
- **开关仍 on**：`Docs/window_switch.json` reason「最近 7 晚跑完 7 晚，耗时达标=False」
  —— 11-15 的 53.6 分钟把「耗时 ≤50」这条打断，今晚 46.8 已回到上限内但需重新累积 7 晚连续达标
  → 于是又是「开关开着 + 内容全 done = 启用了也没活干」的组合（与 11-15 同型）
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD `1d29978` 已是今日第三次提交：CI 采集 ×2 + 本地发布）；`git status --short -- free-nodes .github`
  仅一项 `M free-nodes/.workbuddy/memory/automations/a3d7bb22…/memory.md`（主窗口自己的 memory）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉尾巴
- **给后续窗口的要点**：闸门的「已测满单轮上限」对应的分母是**各内核自己的 cap**（xray 1445 / clash 2088），
  不是固定 2500；读 `Docs/summary.json` 时以 `tested vs cap` 比较，不要拿 2500 硬套

## 2026-11-17（第二十次记录：GATE: done，未跑验证；弹性配额首次把三核压到 800 下限）

- 开工前：`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 无结果 → 无并发窗口、无残留；
  未跑 taskkill（闸门 done 本窗口不启动验证，盲杀无意义）
- 闸门退出码 0：采集日 **2026-11-17（生成于 22:39:41）**，四核均「已测满单轮上限」
  v2ray 2507/2500、**xray 802/800**、**clash 878/872**、singbox 803/800，`elapsed_min=32.6`
- **本轮最值得记的变化**：xray/clash/singbox 的 cap 从 11-16 的 1445/2088/2500 一起掉到 **800 档**，
  即弹性反推撞上 `--min-test 800` 下限（`Docs/quota.md` 第一节：弹性目标 target-avail 30 个/内核）。
  成因是可用率变好——反推到 30 个可用只需 800 测左右就不再往上加。**不是漏测、不是闸门放宽**：
  `partial=false` 且 `tested` 已达各自 cap。
- 本日可用（summary.ok）：v2ray **96** / xray **105** / clash 55 / singbox 70 = 合计 326，
  远高于 quota.md 的「连续 3 晚 <60」告警阈值，也基本是既往最高水位（v2ray 96 尤为突出，前一晚 20）
- 开关仍 on：`Docs/window_switch.json` reason「最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」
  —— 11-15 的 53.6 分钟仍卡着「耗时 ≤50」这条，尽管 11-17 只有 32.6 分钟
  → 又是「开关开着 + 内容全 done = 启用了也没活干」的组合（与 11-15/11-16 同型）
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD `d748ed4`，今日第三次提交：CI 采集 ×2 + 本地发布）；`git status --short -- free-nodes .github`
  仅一项 `M free-nodes/.workbuddy/memory/automations/a3d7bb22…/memory.md`（主窗口自己的 memory）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉尾巴
- **给后续窗口的要点**：cap 掉到 800 不等于「越跑越少」，读 `Docs/quota.md` 第一/二节即可确认；
  判断是否「结果不理想」只看 quota.md 第二节的六个信号（本次 326 个可用、`partial=false`、候选远大于 cap，
  六个信号全不命中），**不要因为 tested 从 2500 掉到 800 就去提高上限**

## 2026-11-18（第二十一次记录：GATE: done，未跑验证）

- 开工前：`tasklist` 查 python.exe 与四内核均「没有找到进程」→ 无并发窗口、无残留；未跑 taskkill（无活可干）
- 闸门退出码 0：采集日 **2026-11-18（生成于 22:36:15）**，四核均「已测满单轮上限」，cap 全部 800
  （弹性反推持续压在下限）：v2ray 813/800、xray 803/800、clash 808/800、singbox 805/800，`elapsed_min=28.4`
- 本日可用（summary.ok）：v2ray **19** / xray 38 / clash 35 / singbox 65 = 合计 157
  - v2ray 19 低于弹性目标 30，且 cap 已贴 `--min-test 800` 下限 → 属「800 个候选里只出 19 个可用」的源池质量，
    不是漏测；quota.md 第二节告警信号按合计 157 看不命中，未调参（连续多晚 <30 才值得取证）
- 开关仍 on：reason「最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」——今晚 28.4 分钟远低于 50，
  但 11-15 的 53.6 分钟仍卡着 streak，故维持 on（历史条目里 11-10 那条之后没有 11-11/12，因本机未跑）
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` **无输出**；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD `207c68f` 已是今日发布）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：`Docs/window_switch.json` 的 `history` 已含 11-13~11-18 连续 6 条 done 且耗时全部 ≤42.5，
  若 11-19 也是 ≤50 且 done，streak 条件（7 晚连续达标）可能首次满足——届时开关会变 off、
  本窗口当天就是最后一次被启用；看到 off 是正常收敛，不要手动改回 on

## 2026-11-19（第二十二次记录：GATE: done，未跑验证）

- 开工前：`tasklist` 查 python.exe 与四内核均「没有找到进程」→ 无并发窗口、无残留；未跑 taskkill（无活可干）
- 闸门退出码 0：采集日 **2026-11-19（生成于 22:38:07）**，四核均「已测满单轮上限」，
  分母各按自己的 cap：v2ray **1298/1284**、xray 802/800、clash 807/800、singbox 803/800，`elapsed_min=29.5`
- **cap 结构第一次「分开走」**：xray/clash/singbox 仍贴 `--min-test 800` 下限，但 v2ray 从 800 抬到 **1284**
  ——弹性反推在 v2ray 上没撞下限（可用率偏低 → 需更多测试量才凑够目标），与 11-17/11-18 三核齐贴 800 不同。
  属正常自适应，不是某核被放宽
- 本日可用（summary.ok）：v2ray 22 / xray 24 / clash 19 / singbox 29 = 合计 94，四核 `partial=false`、`exhausted=false`
  - 较 11-18 的 157 回落，v2ray 22 仍低于弹性目标 30 但高于 `min_available` 10；四核均个位数到二十余属既定水位，未调参
- 开关仍 on：reason「最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」，`streak_done=7`。
  读 `_streak()` 确认窗口是 `history[-7:]` = 11-13~11-19，**11-15 的 53.6 分钟仍在窗口内**，
  故即便今晚 29.5 也不达标。**修正 11-18 的预测**：11-15 要滚出「最近 7 晚」得等 11-22
  （11-20/11-21 的窗口仍含 11-15），所以开关最早 **2026-11-22** 才可能转 off，不是 11-19
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` **无输出**；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD `92af308` 已是今日发布）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：判开关何时转 off 别数「连续几晚 done」，要算 `history[-7:]` 里最慢那晚何时滚出窗口；
  各内核 cap 已互不相同（800~1284 并存），闸门读 `tested vs cap` 时一律取 summary 里各自的 cap

## 2026-11-20（第二十三次记录：GATE: done，未跑验证）

- 开工前：`tasklist` 查 python.exe 与四内核均「没有找到进程」→ 无并发窗口、无残留
- 闸门退出码 0：采集日 **2026-11-20（生成于 22:34:07）**，四核均「已测满单轮上限」，
  v2ray **1781/1770**、xray 1003/1002、clash 1279/1274、singbox 1002/1000，`elapsed_min=27.6`。
  cap 结构继续分化：v2ray 1770 最高（可用率低 → 弹性反推要多测），其余三核 1000~1274
- 本日可用（summary.ok）：v2ray **5** / xray 16 / clash 16 / singbox 18 = 合计 55；
  `nodes/available_nodes.json` 去重 38 条（一节点可服务多内核）。四核 `partial=false`、`exhausted=false`
  - v2ray 5 低于 `min_available` 10，但也已测满 cap 1770 → 属「1770 个候选只出 5 个可用」的源池质量，
    非漏测；按规则 GATE: done 不补测、不重做自检，仅登记
- 开关仍 on：reason「最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」，`streak_done=7`；
  今晚 27.6 分钟远低于 50，但 `history[-7:]` 仍含 11-15 的 53.6 → 与 11-19 预测一致，**最早 11-22 才可能转 off**
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` **无输出**；
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 第一窗口已发布完毕
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：`summary.ok` 是「内核维度计数」（可重复），`available_nodes.json.total` 是「去重节点数」，
  两个数不等是正常；v2ray 个位数可用（5~7）已在 11-13 出现过，属源池波动，别据此调参

## 2026-11-21（第二十四次记录：GATE: done，未跑验证）

- 开工前：`tasklist` 查 python.exe 与四内核均「没有找到进程」→ 无并发窗口、无残留；未跑 taskkill（无活可干）
- 闸门退出码 0：采集日 **2026-11-21（生成于 23:10:15）**，四核均「已测满单轮上限」，
  v2ray **2511/2500**、xray 1882/1881、clash 2402/2398、singbox 1671/1670，`elapsed_min=56.0`
  - cap 再次整体上抬（11-20 是 1770/1002/1274/1000，今晚回到 2500/1881/2398/1670）——弹性反推随前一晚
    可用率变化而放大，属自适应，不是口径放宽
- 本日可用（summary.ok）：v2ray 29 / xray 56 / clash **12** / singbox 36 = 合计 133；
  `nodes/available_nodes.json` 去重 **90** 条（一节点可服务多内核）。四核 `partial=false`、`exhausted=false`
  - clash 12 仅略高于 `min_available` 10，但已测满 cap 2398 → 属源池质量，非漏测；按规则 GATE: done 不补测
  - v2ray 失败分布仍以 timeout 为主（1852/2511）+ tls 595，与 11-20 同型
- **开关再次转为 on（本次是真触发）**：`Docs/window_switch.json` reason「今晚验证耗时 **56.0** 分钟 > 50 分钟上限，
  窗口吃紧；第 2/3 窗口保持/恢复启用」，`streak_done=7`。虽然 11-15 的 53.6 分钟今晚仍是 `history[-7:]`
  （11-15~11-21）里的一员，但**本次不需要靠它**——首窗口自己就超了 50 分钟
  - 推演：11-22 的窗口变成 11-16~11-22，11-15 滚出但 **11-21 的 56.0 进来**，故仍不达标；
    最早转 off 要等 **11-28**（11-21 滚出「最近 7 晚」）。此结论覆盖 11-19/11-20 记的「最早 11-22」
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github`
  仅一项 `M free-nodes/.workbuddy/memory/automations/a3d7bb22…/memory.md`（主窗口自己的 memory）；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD `156f9bd`，今日第三次提交：CI 采集 ×2 + 本地发布）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：① 判开关转 off 的日期要「逐日重算 history[-7:]」，一旦当晚又超 50 分钟就会把
  最晚那晚刷新成新日期（本次把 11-22 推到 11-28）；② 首窗口 `elapsed_min` 已连续多晚 27~33，今晚突然
  56.0，与 cap 从 800~1770 档抬回 2500 档同步 —— 上限抬高 → 测试量翻倍 → 耗时翻倍，两者是同一条因果链，
  属「按现状运行」的正常代价，别因此回调 cap

## 2026-11-22（第二十五次记录：GATE: done，未跑验证）

- 开工前：taskkill 四内核均「没有找到进程」；`Get-CimInstance Win32_Process` 查 python 无结果 → 无并发窗口、无残留
- 闸门退出码 0：采集日 **2026-11-22（生成于 22:51:52）**，四核均「已测满单轮上限」，
  v2ray **2510/2500**、xray 1011/1008、clash 2504/2500、singbox 1393/1392，`elapsed_min=44.5`
- 本日可用（summary.ok）：v2ray 23 / xray 33 / clash 21 / singbox 14 = 合计 91；
  `nodes/available_nodes.json` 去重 **67** 条。四核 `partial=false`、`exhausted=false`
  - singbox 14 仅略高于 `min_available` 10，但已测满 cap 1392 → 属源池质量，非漏测；按规则不补测
- 开关仍 on：reason「维持 on：最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」，`streak_done=7`；
  今晚 44.5 分钟达标，但 `history[-7:]`（11-16~11-22）仍含 **11-21 的 56.0**，故不达停用条件
  - 开关推演（复核 11-21 的结论，那条是对的）：`history[-7:]` 今晚为 11-16~11-22，11-21 的 56.0 在内；
    要让它滚出窗口需其后再攒满 7 条（11-22~11-28）→ 最早 **11-28** 才可能转 off
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github`
  仅一项 `M free-nodes/.workbuddy/memory/automations/a3d7bb22…/memory.md`（主窗口自己的 memory）；
  `rev-list --left-right --count origin/master...HEAD` = 0/0（HEAD `bd60f61` 已是今日发布）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：`nodes/available_nodes.json` 现在的字段是 `date/generated_at/targets/bw_enabled/total/nodes`，
  **没有 `cores` 字段**（历史条目里写「读 cores 字段」已过时），按内核计数只能看 `Docs/summary.json` 的 `cores`
  或读订阅文件；本文件里 `/available_nodes.json` 的 `total` 是去重节点数

## 2026-11-23（第二十六次记录：GATE: done，未跑验证）

- 开工前：`tasklist` 查 python.exe 与四内核均「没有找到进程」→ 无并发窗口、无残留；未跑 taskkill（无活可干）
- 闸门退出码 0：采集日 **2026-11-23（生成于 22:53:31）**，四核均「已测满单轮上限」，
  v2ray **2510/2500**、xray 1005/1000、clash 2502/2500、singbox 2501/2500，`elapsed_min=47.2`
- 本日可用（summary.ok）：v2ray 24 / xray 63 / clash 25 / singbox 28 = 合计 140；
  `nodes/available_nodes.json` 去重 **99** 条（`bw_enabled=true`）。四核 `partial=false`、`exhausted=false`
- 开关仍 on：reason「维持 on：最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」，`streak_done=7`；
  今晚 47.2 分钟达标（≤50），但 `history[-7:]`（11-17~11-23）仍含 **11-21 的 56.0** → 不达停用条件，
  与 11-22 的推演一致：最早 **11-28** 才可能转 off（11-21 滚出窗口）
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD `c72b319`，今日第三次提交：CI 采集 + 本地发布 ×2）；`git status --short -- free-nodes .github` 两项，
  均为 automation memory（`2026-11-23.md` M + 主窗口 a3d7bb22 memory M）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：三核 cap 回到 2500 档、xray 仍是 1000 档，说明弹性反推按各核可用率独立浮动；
  今晚 `elapsed_min=47.2` 已贴近 50 上限，若 11-24 再超 50 会把「最晚那晚」刷新成 11-24，转 off 日期继续后移

## 2026-11-25（第二十八次记录：**GATE: continue，本窗口代跑完整验证 + 补探测**；推送被 deploy key 权限拒绝）

- **异常起点**：23:46 开工，闸门 `GATE: continue（summary 停在昨天）`。查证：`Docs/summary.json`、
  `available_*`、`tested_state.json` 全停在 **11-24** ⇒ 今晚第一窗口（22:00）**一点没跑**（本机未触发/休眠）。
  CI 今天 **07:01:44** 才产出（`CI_READY=0`，早于 20:00 判据），本地只有 09:48 的 `--sync-only` 拉回 CI 原始产物。
- 开工前 `tasklist` 查 python 与四内核均无进程 → 无并发窗口、无残留（未跑 taskkill）
- **验证（本窗口代跑）**：`test_nodes.py --cores v2ray,xray,clash,singbox --resume-tested --fair-budget --time-budget 4800`
  → 51.5 分钟，候选 33421 → 预筛 9963/33419 → 四核 2513/2156/2503/2503，
  可用 **16/26/12/59**（合计 113，去重 76）；四核 `partial=false`、`tested ≥ cap`（xray cap 2151）
- **修掉的真实缺口（known-issues 75）**：自检首轮 **1 critical**「所有节点 TCP 均不可达」。
  归因不是网络：`nodes_meta.json` 的 `generated_at=07:01:44`（CI 时刻）、`reachable=0`、`tcp_latency` 全 null
  ⇒ 清单是 CI 原始未探测版。若不补探测就发布，等于把 33421 条（含 **23537 死节点**）当主清单推出去。
  补 `collect_nodes.py --probe-only --date 2026-11-25`：33385 → 可达 **9882（29.6%）**、313s，
  主清单重写为 9882 条 → 自检 **0 critical / 6 warn**
  - 交叉验证：预筛 9963/33419 vs probe 9882/33385，差 0.2% ⇒ 两边口径一致
  - 安全性已确认：`--probe-only` 只写 `nodes_uris.txt` + 四份 `*_sub`，**不碰 `available_*`**
- 文档：`known-issues` 75、`review_logs` 11-25 观察段、`CHANGELOGS` 11-25 小节、`SKILL.md` 加一行判据
- **推送失败（本次未完成）**：本地已提交 `250fda8`（暂存范围正确，未带用户 C++ 项目），
  但 push 报 **`ERROR: Permission to asdfgh129/Test.git denied to deploy key`** ——
  5 轮通道 + 3 次直连共 8 次全部同一错，属**凭据权限**问题（remote 是 `ssh://git@github.com/asdfgh129/Test.git`，
  key `~/.ssh/github_ed25519`），不是网络也不是非快进。已写 `.git/free-nodes-pending-push.json`，下次自动补推
  - **另注**：`origin/master` 还有 CI 的 `1749201`（本地 `0185cbc` 之后又采了一次）→ 权限修好后
    补推前需先合并远端，别 force
  - 按规则**没有**改 remote/配置、没有手动反复 push
- **给后续窗口的要点**：
  ① 闸门 continue 且 summary 停在昨天时，默认「第一窗口没跑」，**探测也归自己**（先跑 test_nodes，再补 probe，顺序可反）；
  ② 判「清单有没有探测过」只看 `nodes_meta.generated_at` 与 `reachable`，别被文件 mtime 骗（sync 也会更新 mtime）；
  ③ 推送报 `denied to deploy key` 就别再试节点了，那是 GitHub 侧 key 权限，换 8 个节点也一样；
  ④ 本窗口写 memory 又产生尾巴，下次 publish 会一起带上（届时仍需先解决 key 权限）。

## 2026-11-24（第二十七次记录：GATE: done，未跑验证）

- 开工前：taskkill 四内核均「没有找到进程」；`Get-CimInstance Win32_Process` 查 python 无结果 → 无并发窗口、无残留
- 闸门退出码 0：采集日 **2026-11-24（生成于 22:50:42）**，四核均「已测满单轮上限」，
  v2ray **2511/2500**、xray 1004/1000、clash 2505/2500、singbox 2503/2500，`elapsed_min=43.9`
- 本日可用（summary.ok）：v2ray **7** / xray 14 / clash 14 / singbox 25 = 合计 60；
  `nodes/available_nodes.json` 去重 **48** 条（`bw_enabled=true`）。四核 `partial=false`、`exhausted=false`
  - v2ray 7 低于 `min_available` 10，但已测满 cap 2500 → 属源池质量，非漏测；与 11-20 的 5、11-13 的 7 同型
- 开关仍 on：reason「维持 on：最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」；
  今晚 43.9 分钟达标，`history[-7:]`（11-18~11-24）仍含 **11-21 的 56.0** → 与 11-22/11-23 推演一致，
  最早 **11-28** 才可能转 off
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`rev-list --left-right --count` = 0/0
  （HEAD 已是今日发布）；`git status --short -- free-nodes .github` 两项，均为 automation memory
  （`2026-11-24.md` ?? + 主窗口 a3d7bb22 memory M）
- 本窗口零验证、零自检、零修复（GATE: done 按规则不重做自检）；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：可用数低位（合计 60、v2ray 个位数）在 cap 已测满时属源池质量，
  quota.md 第二节告警看的是「连续 3 晚合计 <60」，今晚刚好 60 不命中，别据此提上限

## 2026-11-26（第二十九次记录：GATE: done，但第一窗口漏了自检与发布，本窗口补做两步）

- 开工前：`tasklist` 查 python 与四内核均「没有找到进程」；`rev-list` 0/0、无 pending-push
  （11-25 那笔 `250fda8` 已由后续窗口推送成功，记忆里「待补推」的风险条目可关闭）
- 闸门退出码 0：采集日 **2026-11-26（生成于 23:03:02）**，四核均「已测满单轮上限」
  v2ray 2510/2500、xray 2496/2488、clash 2511/2500、singbox 1294/1273，`elapsed_min=52.7`
- 本日可用（summary.ok）：v2ray 34 / xray 90 / clash 54 / singbox **97** = 合计 275；
  `available_nodes.json` 去重 **176** 条（bw_enabled=true）。四核 `partial=false`、`exhausted=false`
  - singbox 97 是近期高位（前几晚 14~70），xray 90 也偏高，未见异常
- **与规则的一处偏离（有意）**：GATE: done 规定本窗口「不重做自检与发布」，但取证发现第一窗口
  **只跑了验证就结束**——`Docs/health_check.md` 仍停在 11-25、`HEAD` 停在 CI 提交 `92f2acb`，
  工作区躺着 30 个未提交产物（含 `src/pool.py` 的 known-issues 74 修复）。若只补推不补自检，
  等于把当晚清单不经自检推出去（11-25 的教训就是未探测版差点上线）。
  → 本窗口补跑 `health_check --date 2026-11-26`（0 critical / 4 warn）+ publish，判定仍按闸门为准
- **主清单已探测**：`nodes_meta.generated_at=22:05:44`、8136 条全带 `tcp_latency`、`reachable=8136`
  → 第一窗口的 probe 正常，不是 11-25 那种「CI 原始未探测版」
- 自检 4 warn 全属既定类别，未改代码：2 个高贡献仓库 0 条（日志带标签，`Areral/ScarletDevil` HTTP 402、
  `rtwo2/FastNodes` HTTP 404 ⇒ 上游链接失效）、v2ray 可用率 1.4%、clash 2.2%、镜像失效 11/13
- **known-issues 74 已落地**（第一窗口改动，本窗口随发布入库）：`pool.retest_candidates()`
  三级稳定排序 `last_ok` 倒序 → `ok_count` 倒序 → `best_latency` 升序，`DEFAULT_RETEST` 仍 40
- 发布：commit `4590d65` → origin/master 成功（30 文件）。**SSH 又被拒**（deploy key 无写权限），
  但脚本已自动回退 HTTPS 重试并成功 ⇒ 11-25 那种「必须人工解决 key 权限」的阻塞已不复现
- **给后续窗口的要点**：① GATE: done 不等于「第一窗口全做完了」——发布前先看
  `Docs/health_check.md` 的日期与 `HEAD` 是否含当晚发布，两者缺一就补做，别机械跳过；
  ② SSH deploy key 被拒时不用管，`publish_free_nodes.py` 会自己切 HTTPS；
  ③ 判清单是否探测过仍只看 `nodes_meta.generated_at` + `tcp_latency` 是否全非空

## 2026-11-28 凌晨 02:33（第三十次记录：GATE: done，未跑验证；本机休眠把两晚窗口全推后）

- 开工前：`tasklist` 查 python 与四内核均「没有找到进程」→ 无并发窗口、无残留；未跑 taskkill
- **时间异常（本次要点）**：本窗口本应 11-27 23:45 触发，实际 **11-28 02:33** 才跑起来；
  第一窗口同样被推后，采集日在 01:39 起算 ⇒ `Docs/summary.json` 记成 **2026-11-28（生成于 02:11:58）**、
  `elapsed_min=32.1`。属 known-issues 54「schedule 迟到」同型，不是口径错
- 闸门退出码 0：采集日 2026-11-28，四核均「已测满单轮上限」，分母各按自己 cap：
  v2ray **2226/2215**、xray 1016/1000、clash 1406/1395、singbox 1007/1000
- 本日可用（summary.ok）：v2ray **16** / xray **95** / clash 57 / singbox **85** = 合计 253；
  主清单 6160 条全 TCP 可达（中位数 246ms）、去重后发布 6160。四核 `partial=false`、`exhausted=false`
- **按 11-26 的教训做了「闸门之外的两项核对」，均通过**：`Docs/health_check.json` 的 `date=2026-11-28`、
  `generated_at=02:22:28`（第一窗口确实做了自检）；`HEAD` 已有两次当日发布（`36d61b7`、`7d31a0e`）
  ⇒ 第一窗口三件事（验证/自检/发布）齐全，本窗口无需补做任何一步
- 自检 0 critical / 3 warn，全属既定类别：2 个高贡献仓库 0 条（`rtwo2/FastNodes`、`Areral/ScarletDevil`，
  均「下载失败」，与 11-26 同两仓，上游 402/404）、v2ray 可用率 0.7%（16/2226，已测满 cap 2215 ⇒ 源池质量）、
  镜像失效 10/13（环境）。**未改任何代码、未调任何参数**
- 尾巴检查（写本文件前）：无 `.git/free-nodes-pending-push.json`；`git status --short -- free-nodes .github` **无输出**；
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 第一窗口已干净发布
- 开关仍 on：reason「最近 7 晚跑完 7 晚（需 7 晚连续达标才停用，耗时达标=False）」，`streak_done=7`；
  `history[-7:]` = 11-19~11-24 + 11-28（11-25/26/27 未落 history），其中 **11-21 的 56.0** 仍在
  ⇒ 与 11-21 起的一贯推演一致，**仍未到转 off 条件**（"最早 11-28" 的预测今晚不成立，因 11-21 尚未滚出且中间有空档）
- 本窗口零验证、零自检、零修复；写完本文件后 publish 一次收掉 memory 尾巴
- **给后续窗口的要点**：① 本机休眠会让**整晚窗口顺延**，跨零点后采集日按 `date +%F` 变成次日，
  闸门读到的日期与「昨晚」对不上是正常的，别判成故障；② 11-27 晚本地**没有任何发布**
  （`git log` 只有 CI 的 `3648558`，无「更新 2026-11-27」）⇒ 订阅跳过了一天，属本机没跑，恢复后无需补采（CI 数据仍在）
- **给后续窗口的要点（续）**：③ 判「是否要 publish 收尾」只看 `git status --short -- free-nodes .github`
  与 `rev-list` 的 ahead 数；本文件自身被跟踪，写完必然产生一处改动，所以 done 夜晚基本都要 publish 一次

