# 第三窗口（01:30）执行记忆

## 2026-11-07 采集日（2026-11-08 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2511/2507/2511/2508，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用数 v2ray 31 / xray 78 / clash 24 / singbox 24（池 278/736/512/454）；
  采集总量 11475 → 去重 3817 → TCP 可达 3817/3817（中位 198ms），CF 前置 1799
- 产物核对：available 31/78/24/**25**（singbox 多出的 1 条是 `direct` outbound，净 24）与 summary 逐项一致；
  `nodes_uris.txt` 3817 与 `nodes_meta.total/reachable` 3817 一致
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
  （第二窗口的记忆文件已被 `c7a4917` 带上，所以这次没有历史常见的「记忆文件尾巴」）
- 本日发布链：CI `83ca63a`(04:04)/`9ebbf64`(21:12) + 第一窗口 `34fe3ec`(22:37)/`77cb4bb`(22:39)
  + 第二窗口 `c7a4917`(23:47)，已全部在 origin/master
- 自检（第一窗口 22:36 产物）：0 critical / **4 warn** = 三核可用率 1.2/1.0/1.0% 低水位 + 镜像失效 10/13
  （可用 3 个：gh-proxy.com / gh-proxy.org / gh.monlor.com）→ 按 known-issues 口径不改代码
- **crashgfw 自愈**：11-03~11-06 连续三晚「整域 URLError」昨晚起因 CI 出口侧限制，本日恢复 440 条；
  印证 11-03 判据（单仓 URLError 不改采集代码，盯同域多仓同时失败）成立
- 自检中 xray 78/2507=3.1% 不在告警阈值内，四核告警数由 6 降到 4，属水位波动非口径变化
- 本窗口记忆文件在核查之后写，留作下一个发布顺带提交（沿用既有约定，不是故障）

## 2026-11-06 采集日（2026-11-07 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2509/2506/2508/2508，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用数 v2ray 14 / xray 69 / clash 26 / singbox 21（池 262/690/500/442）；
  采集总量 11453 → 去重 3916 → TCP 可达 3916/3916（中位 201ms）
- 产物核对：available 14/69/26/**22**（singbox 多出的 1 条是 `direct` outbound，净 21）与 summary 逐项一致；
  `nodes_uris.txt` 与 `nodes_meta.json` 均 3916
- **尾巴**：无 `pending-push.json`、`rev-list` 0/0，但第二窗口的 automation memory 未提交
  → publish `8f9938a` 补推；之后三处全干净（`git status --short -- free-nodes .github` 空）
- 本日发布链：CI `bc0fb4d`(21:13) + 第一窗口 `8b5fc53`(22:42) + 第二窗口 `e809448` + 本窗口 `8f9938a`
- 自检（第一窗口 22:37 产物）：0 critical / 6 warn = 四内核可用率 0.6/2.8/1.0/0.8% 低水位 +
  镜像失效 11/13 + crashgfw 下载失败（URLError）
- **crashgfw 复核（未改代码，与第一窗口 known-issues 60 一致）**：API 查得 `pushed_at=2026-11-06T10:27Z`、
  README 6076B（当天版），其 10 个外链全指向 `ndxy.fn0821.xyz`，本机直连 **200/8860B** 正常
  ⇒ 上游与外链都没问题，是 CI/Azure 出口对该整域不可达（第三晚）；同域多仓同时 URLError 才是通道问题，今日不成立
- 观察项：v2ray 14（前四日 18/29/30/26）连续下行但仍在 min_available(10) 之上，池 262；
  按口径不放宽探测地址；单日四内核合计 130 较昨日 111 回升，仍判上游波动
- 本窗口记忆文件在发布之后写，按既有约定留作下一个发布顺带提交（不是故障）

## 2026-11-05 采集日（2026-11-06 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2509/2510/2508/2507，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用数 v2ray 18 / xray 44 / clash 23 / singbox 26（池 257/644/481/430）；
  采集总量 12165 → 去重 4444 → TCP 可达 4444/4444（中位 203ms）
- 产物核对：available 条目 18/44/23/26 与 summary 的 ok 逐项一致
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `232df37`(04:39)/`d6f386a`(21:14) + 第一窗口 `e387672`(22:37) + 第二窗口 `0efe576`(23:46)，
  已全部在 origin/master
- 自检（第一窗口 22:36 产物）：0 critical / 6 warn = 四内核可用率 0.7/1.8/0.9/1.0% 低水位 +
  镜像失效 11/13 + crashgfw 下载失败（URLError）
- **crashgfw 复核（未改代码）**：`api.github.com` 查得最后提交 2026-11-05T10:25Z、README 6076B 仍在
  → 上游活跃，属单仓下载抖动，沿用 11-03 判据不改采集代码；真正要盯的是同域多仓同时 URLError
- 观察项：v2ray 18（昨 29、前日 30）连续三日下行，仍在 min_available(10) 之上、池 257，
  按口径不放宽探测地址；若明晚跌到个位数再查量大源（F0rc3Run / ermaozi01）
- 本窗口记忆文件在发布之后写，按既有约定留作下一个发布顺带提交（不是故障）

## 2026-11-04 采集日（2026-11-05 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2509/2508/2509/2507，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用数 v2ray 29 / xray 71 / clash 48 / singbox 56（池 251/630/472/419）；
  采集总量 12274 → 去重 4286 → TCP 可达 4286/4286（中位 201ms）；产物条目数与 summary 逐项核对一致
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `c96d745`（21:13）+ 第一窗口 22:42/22:44（`39b4e5a`/`a4eeafd`）+ 第二窗口 23:46（`b1e40cd`），
  已全部在 origin/master
- 自检（第一窗口 22:41 产物）：0 critical / 5 warn = 四内核可用率 1.2/2.8/1.9/2.2% 低水位 + 镜像失效 **10/13**
  （`gh.monlor.com` 从昨日失效恢复，昨日 11/13）；可用镜像仍有 3 个，按 known-issues 不改代码
- 未发现可修问题。v2ray 29（昨日 30）仍属源池波动，非持续下探
- 本窗口记忆文件在发布之后写，按既有约定留作下一个发布顺带提交（不是故障）

## 2026-11-03 采集日（2026-11-04 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2507/2509/2507/2506，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用数 v2ray 30 / xray 74 / clash 51 / singbox 46（池 241/588/445/386）；
  采集总量 12916 → 去重 4991 → TCP 可达 4991/4991（中位 207ms）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：`0bb2f26`（CI 采集）+ 第一/第二窗口 `a33db82`/`351b590`，已推送 origin/master
- 自检（第一窗口 22:46 产物）：0 critical / 6 warn = 四内核可用率 1.2/2.9/2.0/1.8% 低水位 +
  镜像失效 11/13 + crashgfw 0 条（下载失败 URLError）
- **昨日遗留观察项已解除**：v2ray 26 → 30 回升，不是持续下探，无需查量大源
- **新判据（URLError ≠ 上游失效）**：今日 80 仓里仅 2 个 URLError（crashgfw、HakurouKen），
  经 API 核查两仓 README 均在（crashgfw 6076B、HakurouKen 262B）、当日均有 push；且
  `fetch_url_text` 本就有「整条链再走一次」的瞬时重试 + 镜像链。所以日志里的
  「下载失败（URLError）」= 重试后仍失败的单次抖动，**不要据此改采集代码**；
  真正要盯的是同域多仓同时 URLError（那才是通道/出口问题）
- 本窗口记忆文件在发布之后写，按既有约定留作下一个发布顺带提交（不是故障）

## 2026-11-02 采集日（2026-11-03 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2507/2509/2508/2507，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用数 v2ray 26 / xray 53 / clash 47 / singbox 50（池 225/541/411/353）；主清单 5051 条 TCP 全可达
- **尾巴检查三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：第一窗口 22:50/22:52、第二窗口 23:47/23:49 各两次提交，最新 `8123884`；
  第二窗口也在 23:45 判 done 后收尾，属正常接力
- 自检（第一窗口 22:47 产物）：0 critical / 5 warn = 四内核可用率 1.0~2.1% 低水位 + 镜像失效 10/13
- **观察项（未改动，留明天第一窗口看）**：v2ray 可用量从前三天 48/54/69 掉到 **26**，可用率 1.0%
  （近几日最低）。仍属 known-issues 40 的源池质量波动，按口径不放宽探测地址；若明晚继续下探，
  再查是否为某量大源（F0rc3Run / 0xRadikal）当日配置集体失效
- 本窗口记忆文件在发布之后写，按既有约定留作下一个发布顺带提交（不是故障，别反复排查）

## 2026-11-01 采集日（2026-11-02 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2509/2506/2509/2506，cap 2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检
- 本日可用数 v2ray 48 / xray 120 / clash 56 / singbox 63（池 214/520/389/329）
- **尾巴**：无 `pending-push.json`、`rev-list` 0/0，但第二窗口写的 automation memory 未提交（10 行）→
  发布 `d88cfac`；之后补文档订正再发一次 `8f388e7`。两次都推送成功
  （xray @ 202.50.253.81:19999，均第 1 次命中）
- **本窗口的知识订正（第 55 条）**：clashfree 连续两天报「0 条（下载失败）」，此前按第 48 条归为通道问题。
  实查 `git/trees`：`clash20261030/31/1101.yml` 全为 **size=0**（1028/1029 是 688KB 级）、`sub.yml` 也 0
  → 上游生成链停摆；日志「404」与「解析不到」的差异只是**采集时刻文件在不在**（0 字节占位、创建晚于 21:05）
- **判据留用**：`git status --short` 干净但 `rev-list` 不是 0/0 也算有尾巴；反之 `rev-list` 0/0 时
  仍要看一眼第二窗口的记忆文件。两处都干净才是真没尾巴
- **跨窗口待办**：xray 上游 26.10.31（本地 26.10.21）已两晚未升级 —— 升级必须放第一窗口采集前做并跑能力指纹，
  本窗口不升级
- 判据口诀：**404 不一定是自己的 bug，先查 git tree 里文件在不在、size 是否为 0**

## 2026-10-31 采集日（2026-11-01 01:30 运行）

- 闸门退出码 0：四内核全部「已测满单轮上限」（2506/2505/2507/2503，cap 2500），GATE: done
- **本窗口未跑验证、未重跑自检**（按 gate 规则）；本日可用数 v2ray 54 / xray 122 / clash 60 / singbox 55
- 中间窗口（`a4c4ae9d`）已在 23:45 判过 done 并补推 `4fd578e`；本窗口只剩它发布后写入的记忆文件一个尾巴 →
  publish 收干净 `b7a09a9` → origin/master（v2ray @ 202.50.253.81:19999，通道第 1 次命中）
- 自检沿用第一窗口结果：0 critical / 5 warn（三内核可用率 2.2~2.4% 低水位 + clashfree 下载失败 0 条）
- **判据留用**：GATE: done 时必须同时看三处才算「无需补推」——`pending-push.json`、
  `git status --short -- free-nodes`、`git rev-list --left-right --count origin/master...HEAD`（0/0 才算对齐）。
  记忆文件（automation memory / 当日 log）发布后才写，必然产生同样的尾巴，属正常，别当故障反复排查

## 2026-10-30 采集日（2026-10-31 01:30 运行）

- 四内核 `partial=false`、`sampled` 到 2500 上限 → 跳过续跑，未重测任何节点
- **复核上一窗口第 48 条**：crashgfw 当天 README 实跑 10/10 成功（每条 8860B/30 节点）
  → 「外链直连优先」有效，下一轮采集应恢复约 300 条候选（次日要核对它不再报 0 条）
- **本窗口修复（第 49 条，跨窗口留用）**：`classify_readme_link()` 跳过以 `/` 结尾的外链。
  分类页/博客页靠路径里的 `node`/`clash` 命中 `SUB_URL_STRONG_HINT`，会占掉
  `MAX_README_LINKS=10` 的配额（真订阅被截掉），日志还记成「1/10 链接下载成功」
- **订正**：第二窗口记的「clashfree 688KB / 81 条」不成立——`git/trees/HEAD?recursive=1`
  显示 `clash20261030.yml size=0`（`1027` 也是 0，`1026/1028/1029` 才 688KB 级），
  提交 `683e7d01` 改成空文件。**判「上游为空」先看 git tree，别只看正文长度**
- **文档漂移**：`SKILL.md` 的 `--max-test` 写 3000、代码是 2500 → 已改（含命令示例）
- 自检 0 critical / 5 warn（与其他窗口同水位）；提交 `a8d7eea` 推送成功
  （v2ray @ 202.50.253.81:19999）
- 判据口诀：**以 `/` 结尾 = 目录/网页，不是订阅文件**；日志里 `<名字>:0` 有三种含义
  （空文件 / HTML 网页 / 格式未覆盖），别一律说「解析不到节点」

## 2026-10-29 采集日（2026-10-30 01:30 运行）

- `Docs/summary.json` 的 `date` = 2026-10-29；四内核 `partial=false`、`sampled` 已到 2500 上限
  （2502/2503/2506/2503），`exhausted=false` 属取样上限稳态 → 跳过续跑，未重测任何节点
- 自检 0 critical / 5 warn（1.2%/4.2%/2.9%/2.0% 可用率、镜像失效 10/13、crashgfw 0 条）
- **本窗口修复（info 错报，跨窗口留用）**：自检连续三天报「配额 core 60/60（匿名）」。
  `check_quota()` 只看环境变量、且 `rate_limit` 不带 token → 报的是匿名桶；
  真实身份是凭据文件里的 token（5000/5000）。修法：统一 `load_github_token()` + token 传入 +
  `token_desc()` 打码 + 「带 token 失败回退匿名」分支。known-issues 第 45 条
- 判据口诀：**`limit` 字段就是身份指纹**（60=匿名、5000=token），两个桶数字混用不会报错，只会骗人
- 提交 `1262d51` 推送成功（v2ray @ 202.50.253.81:19999）
- 遗留：`free-nodes/.workbuddy/memory/2026-10-29.md` 里「提交 hash」是发布后补写的，未提交，
  下次发布自动带上（沿用既有约定）

## 2026-10-28 采集日（2026-10-29 01:30 运行）

- `Docs/summary.json` 的 `date` = 2026-10-28；四内核 `partial=false`（v2ray 2118 / xray 2159 /
  clash 2508 / singbox 2509 均已达取样上限）→ 按规则跳过续跑，只做自检+修复+发布
- 自检 1 critical / 5 warn：critical 仍是修复前的历史日志（无原因标签）报的「14/51 下载失败」，
  修复要等下一轮采集才体现
- **本窗口最大收获（跨窗口留用）**：critical 的真根因是**我们自己的 URL 解析 bug**——
  `raw.githubusercontent.com/<o>/<r>/refs/heads/main/<path>` 被拆成 `heads/main/<path>`（ref=refs），
  拼出的地址必然 404。`_split_raw_parts()` 修掉后单仓库可回补 150～10980 条
  （SoliSpirit 0→10980、cbusifabcap 0→7674、whoahaow 0→2293、free18 0→350）
- **以后遇到 404 一律先打印 README 原文比对**，别直接归因上游（上一窗口就归错了）
- 顺带：`health_check` 新增 `pfail` 桶（部分链接下载失败 ≠ 解析不到节点）
- 提交 `de43803` 推送成功（v2ray @ 202.50.253.81:19999）

## 2026-10-27 采集日（2026-10-28 01:30 运行）

- 采集日期取 `Docs/summary.json` 的 `date` = 2026-10-27；本窗口不采集，直接 `--resume-tested` 续跑
- 结果：v2ray 新测 936（跳过 2064）→ 本日 69/3097；xray 新测 1968（跳过 602）→ 80/2592；
  clash / singbox 因顺序预算耗尽未跑（仍为第二窗口 75/792、68/840）。并入旧可用：61→69、65→80
- 自检 0 严重 / 2 告警（v2ray 可用率 2.2%、镜像失效 10/13），均为已知水位，未动探测地址
- **修复 1 项**：`health_check.py` 写 `review_logs.md` 时按日期前缀判重，把手写「## <日期> <窗口>」
  小节整段删了 → 改传 `match_heading=True`（只替换「同日期 + 自检摘要」）；两次跑验证小节不再丢
  （known-issues 第 39 条、CHANGELOGS 已记）
- 提交：a7aea06（数据）、b12db67（修复+文档），均已 push origin/master，
  代理内核 v2ray @ 202.50.253.81:19999
- 经验：**第三窗口命令建议加 `--fair-budget`**（SKILL.md 已推荐，prompt 里没带），
  否则 v2ray 测完后 xray 吃光剩余墙钟，clash/singbox 零新增
- 经验：`available_v2ray.txt`/`available_xray.txt` 是 **base64 单行**，核条目数必须先解码，
  不能按行数数；`available_clash.yaml` 实际是 JSON 结构（`"proxies": [...]`）
