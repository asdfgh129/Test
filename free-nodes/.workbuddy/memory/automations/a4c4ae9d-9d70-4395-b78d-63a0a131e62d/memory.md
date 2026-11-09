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

