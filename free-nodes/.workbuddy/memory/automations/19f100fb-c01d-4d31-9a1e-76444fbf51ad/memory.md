# 第三窗口（01:30）执行记忆

## 2026-11-21 采集日（2026-11-22 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 2511/2500、xray 1882/1881、clash 2402/2398、
  singbox 1671/1670）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 **v2ray 29 / xray 56 / clash 12 / singbox 36**（池 215/573/327/355）；
  采集 28433 → 去重 8558，TCP 可达 8558/8558（100%，中位 231ms），扫描仓库 100 个
- **clash 12 条为近期最低**（前几日 16/16/19/35/24），可用率 0.5%，但仍 > min_available(10)；
  `exhausted=false`、cand 8067 未耗尽 ⇒ 闸门判 done 合规，属源池质量波动，**不要放宽探测地址**
- 产物核对：available 条目 29/56/12/**37（含 1 条 direct，净 36）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 8558 = `nodes_meta.total/reachable` 8558；tested_state date=11-21（四核 2511/1882/2402/1671）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `00f1e16`(05:03，属 11-20 侧 cron 迟到派发)/`e6d156d`(21:13) + 第一窗口
  `156f9bd`(23:12) + 第二窗口 `932d3c9`(23:51，仅两份 automation memory)，已全部在 origin/master
- 自检（第一窗口 23:10 产物）：**0 critical / 6 warn** = 四核可用率 1.2/3.0/0.5/2.2% 低水位
  + `clash-s/clash-s.github.io` 0 条（历史 626 条，判定「解析不到节点」，单仓、单晚）
  + 镜像失效 10/13（可用 gh-proxy.com / gh-proxy.org / gh.monlor.com / 3 个）
  → 均属既定口径，不改代码；clash-s 若连续两晚报同样原因再按 known-issues 47 查格式覆盖
- 窗口开关仍 on（`elapsed_min=56.0 > 50`，`reason` 写「窗口吃紧」）→ 本窗口被正常触发，属设计
- **仓库根目录有 14 个 10-25 遗留的未跟踪调试文件**（`_diag.py`、`_dl.json`、`_pcfg*.json`、
  `_p_client.go` 等，都不在 free-nodes 下）。publish 走路径限定暂存 ⇒ 不会被误提交；
  按文件安全规则**未删除**，留待用户确认后清理（或加忽略规则）
- 本窗口按 prompt 第 1 步明文规则「GATE: done 且无尾巴 → 直接结束」，**未发布**；
  本记忆文件在核查之后写入，形成 1 个纯文档尾巴，按既有约定留待明晚第一窗口发布时顺带提交

## 2026-11-20 采集日（2026-11-21 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 1781/1770、xray 1003/1002、clash 1279/1274、
  singbox 1002/1000）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 **v2ray 5 / xray 16 / clash 16 / singbox 18**（池 205/566/338/346）；
  采集 27402 → 去重 7548，TCP 可达 7548/7548（100%，中位 247ms），扫描仓库 100 个
- **v2ray 5 条跌破 min_available(10)，为近期最低**（前几日 22/19/14/18/29/26/31）。
  弹性 cap 按 11-19 的 1.7% 反推 1770（目标 30），当日可用率跌到 0.3% ⇒ 测满 cap 仍只 5 条。
  `exhausted=false`、cand 5268 未耗尽 ⇒ 闸门判 done 合规；**cap 由昨日可用率反推，当日可用率
  再跌一半时达不到目标数是正常现象，不要据此提 cap，也不要放宽探测地址**
- 产物核对：available 条目 5/16/16/**19（含 1 条 direct，净 18）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 7548 = `nodes_meta.total/reachable` 7548；tested_state date=11-20（四核 1781/1003/1279/1002）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `f66afa3`(05:21，属 11-19 侧 cron 迟到派发)/`3aba6a2`(21:19) + 第一窗口
  `9cf7aee`(22:41)/`5b75218`(22:44) + 第二窗口 `8fa2a10`(23:46)，已全部在 origin/master
- 自检（第一窗口 22:34 产物）：**0 critical / 6 warn** = 四核可用率 0.3/1.6/1.3/1.8% 低水位
  + 四仓 0 条（crashgfw / VoroninaYanina / hysteria350 / free-proxy-nodes 全 URLError，
  各声明 6 条链接）+ 镜像失效 11/13（可用 gh-proxy.com / gh-proxy.org）
  → 四仓即 known-issues 60 那组同运营方镜像（同指 ndxy.fn0821.xyz），属 CI(Azure) 出口不可达，
  非采集代码问题；其余为既定口径，不改代码
- 窗口开关仍 on（`streak_done` 7/7，`reason` 写 `耗时达标=False`）→ 本窗口被正常触发，属「宁可多跑一次」设计
- 本窗口按 prompt 第 1 步明文规则「GATE: done 且无尾巴 → 直接结束」，**未发布**；
  本记忆文件在核查之后写入，形成 1 个纯文档尾巴，按既有约定留待明晚第一窗口发布时顺带提交

## 2026-11-19 采集日（2026-11-20 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 1298/1284、xray 802/800、clash 807/800、
  singbox 803/800）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 **v2ray 22 / xray 24 / clash 19 / singbox 29**（池 208/577/335/350）；
  CI 采集 28914 → 去重 9084，TCP 可达 9084/9084（100%，中位 236ms），扫描仓库 66 个
- 弹性反推：cap 1284/800/800/800（按 11-18 可用率 2.3%/4.7%/4.3%/8.7% 反推目标 30）。
  v2ray 实测 22 **未达目标 30**（当晚可用率跌到 1.7%），但已测满 cap、cand 6452 未耗尽，
  按闸门口径仍是 done —— **cap 由「昨日可用率」反推，当日可用率下滑时达不到目标数是正常现象**，不要去提高 cap
- 产物核对：available 条目 22/24/19/**30（含 1 条 direct，净 29）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 9084 = `nodes_meta.total/reachable` 9084；tested_state date=11-19（四核 1298/802/807/803）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `3dc384b`(05:19，属 11-18 侧 cron 迟到派发)/`bc1dbd0`(21:11) + 第一窗口
  `98ef69b`(22:42)/`92af308`(22:45) + 第二窗口 `762671d`(23:48)，已全部在 origin/master
- 自检（第一窗口 22:41 产物）：**0 critical / 4 warn** = v2ray 1.7%、xray 3.0%、clash 2.4% 低水位
  + 镜像失效 9/13（可用 gh-proxy.com / gh-proxy.org / gh.monlor.com / ghfast.top 四个）
  → 均为既定口径，按 known-issues 不改代码；singbox 2.4% 未触阈值
- 观察项：singbox `reasons` 首次出现 **reset 525**（远超 tls 226 / timeout 0），即连接被对端 RST，
  与「超时」不同源；可用数 29 仍属正常水位、且是四核最高，暂不改口径，留第一窗口盯两晚
- 本窗口按 prompt 第 1 步明文规则「GATE: done 且无尾巴 → 直接结束」，**未发布**；
  本记忆文件在核查之后写入，形成 1 个纯文档尾巴，按既有约定留待明晚第一窗口发布时顺带提交

## 2026-11-18 采集日（2026-11-19 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 813/800、xray 803/800、clash 808/800、
  singbox 805/800）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 **v2ray 19 / xray 38 / clash 35 / singbox 65**（池 216/605/358/375）；
  主清单 9928 条 TCP 全可达（100%，中位 241ms），CF 前置 2264；采集 30455 → 去重 9928
- 弹性反推继续生效：四核 cap 一律 800（昨日可用率 3.8%/13.1%/6.3%/8.7% → 目标 30 个所需
  783/229/479/344，取整到 800），四核实测 813/803/808/805 均「测满 cap」，耗时仅 28.4min
- 产物核对：available v2ray 4808B / xray 10552B / clash 13179B / singbox 31420B；
  `nodes_uris` 9928 = `nodes_meta.total/reachable` 9928；tested_state date=11-18（四核 813/803/808/805）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `2e926de`(05:41，属 11-17 侧 cron 迟到派发)/`3d7f66e`(21:11) + 第一窗口
  `89cd780`(22:38)/`207c68f`(22:48) + 第二窗口 `ad4051e`(23:47)，已全部在 origin/master
- 自检（第一窗口 22:36 产物）：**0 critical / 2 warn** = v2ray 可用率 2.3%（19/813）低水位
  + 镜像失效 10/13（可用 gh-proxy.com / gh-proxy.* 两个）→ 均为既定口径，不改代码；
  告警数为近期最低（此前 4~6）
- v2ray 19 虽低但 ≫ min_available(10)，池内仍有 216 个历史可用；`reasons` 显示 tls 419 /
  timeout 363 为主，属源池质量，不放宽探测地址
- 窗口开关仍 on（`streak_done` 7/7，`reason` 写 `耗时达标=False`，因历史某晚 elapsed > 50）
  → 本窗口被正常触发；闸门 done 说明这次触发多余但符合「宁可多跑一次」设计
- 本窗口按 prompt 第 1 步明文规则「GATE: done 且无尾巴 → 直接结束」，**未发布**；
  本记忆文件在核查之后写入，形成 1 个纯文档尾巴，按既有约定留待明晚第一窗口发布时顺带提交

## 2026-11-17 采集日（2026-11-18 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 2507/2500、xray 802/800、clash 878/872、
  singbox 803/800）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 **v2ray 96 / xray 105 / clash 55 / singbox 70**（池 221/625/367/378）；
  主清单 6971 条 TCP 全可达（100%，中位 246ms）；采集 24375 → 去重 6971
- **弹性反推首次明显生效**：cap 不再是四核一律 2500 —— 按「昨日可用率 → 目标 30 个」反推，
  xray 800（5.1%）、clash 872（3.4%）、singbox 800（4.8%），只有 v2ray 顶到 2500（昨日 0.8%）。
  结果可用数全部达标（105/55/70 ≫ 目标 30），耗时只 32.6min。**这印证「可用率高的夜不必测满 2500」**，
  以后看到 cap < 2500 且「已测满单轮上限」是正常判定，不要当成漏测/异常
- 产物核对：available 96/105/55/**71（含 1 条 direct，净 70）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 6971 = `nodes_meta.total/reachable` 6971；tested_state date=11-17（四核 2507/802/878/803）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `220e7ec`(06:58，属 11-16 侧 cron 迟到派发)/`9bf25fa`(21:10) + 第一窗口 `d748ed4`(22:41)
  + 第二窗口 `7af5b82`(23:46，只带自己的 memory)，已全部在 origin/master
- 自检（第一窗口 22:40 产物）：**0 critical / 1 warn** = 镜像失效 11/13（可用 gh-proxy.com / gh-proxy.org）
  → 按 known-issues 口径不改代码。告警数创近期最低（此前多为 4~6），因四核可用率全部越过阈值
- 窗口开关仍 on（`streak_done` 7/7，但 `耗时达标=False`，因历史某晚 elapsed > 50）；本窗口被触发属设计
- 本窗口记忆文件在核查之后写入，产生 1 个纯文档尾巴 → 按「有尾巴就收干净」规则 publish 收尾

## 2026-11-16 采集日（2026-11-17 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（v2ray 2507/2500、xray 1447/1445、clash 2094/2088、
  singbox 2505/2500）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用 v2ray 20 / xray 74 / clash 72 / singbox 120（池 148/578/360/376）；
  主清单 9916 条 TCP 全可达（100%，中位 233ms），CF 前置 2073；原始 160917 → 去重 29411
- 产物核对：available 20/74/72/**121（含 1 条 direct，净 120）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 9916 = `nodes_meta.total/reachable` 9916；tested_state date=11-16（四核 2507/1447/2094/2505）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `9def48a`(03:22，11-15 侧 cron 迟到派发)/`8698dfb`(21:18) + 第一窗口 `1d29978`(22:58)
  + 第二窗口 `87607a2`(23:47)，已全部在 origin/master
- 自检（第一窗口 22:55 产物）：0 critical / **3 warn** = v2ray 可用率 0.8% 低水位 + 镜像失效 10/13
  + 「4 个高贡献仓库本次 0 条（全为下载失败 URLError）」
- **四仓 URLError 取证（未改代码，结论与 known-issues 60 一致）**：crashgfw / VoroninaYanina /
  hysteria350 / free-proxy-nodes 四仓 `pushed_at` 全为 11-16T10:45Z（同一运营方镜像组），README 6 条链接
  **同指 `ndxy.fn0821.xyz/nodes/<hash>`**（另有 `f2.st0103.top`）→ 属「同域多仓同时失败」；
  本机实测 `ndxy.fn0821.xyz` 订阅链接 **200 / 4000B 正常**，`f2.st0103.top` 立即 RST ⇒ 仍是 **CI(Azure) 出口侧**
  不可达，采集代码无需改，也不该加镜像（非 GitHub raw，镜像救不了第三方域）
- `735754647/Free-Nodes` HTTP 404：上游文件已删（known-issues 43/55 判据，先看 git trees 再怀疑自己）
- 窗口开关仍 on（`reason` 写 `耗时达标=False`，因 11-15 那晚 elapsed 53.6 > 50；连续 done 已 7/7）
  → 本窗口被正常触发，闸门 done 说明这次触发多余但符合「宁可多跑一次」设计
- 本窗口记忆文件在核查之后写入，产生 1 个纯文档尾巴 → 按「有尾巴就收干净」规则 publish 收尾
- 判据留用：**四条高贡献仓同时 URLError 先看 pushed_at 与链接域名是否同一家**；同一运营方镜像组共用
  一条订阅域，整域被 CI 出口封就会一次性全灭，别当成四个独立故障去改采集代码

## 2026-11-15 采集日（2026-11-16 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2510/2505/2505/2507，cap 2500）→ GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用 v2ray 21 / xray 52 / clash 36 / singbox 17（池 177/611/342/314）；
  主清单 8983 条 TCP 全可达（100%，中位 236ms），CF 前置 1464
- 产物核对：available 21/52/36/**18（含 1 条 direct，净 17）** 与 summary 的 ok 逐项一致；
  `nodes_uris` 8983 = `nodes_meta.total/reachable` 8983；tested_state date=11-15（四核 2510/2505/2505/2507）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `9f98910`(02:46，属 11-14 侧 cron 迟到派发)/`7faf948`(21:10) + 第一窗口 `43a8a3a`(23:03)
  + 第二窗口 `7e4f8d5`(23:47，只带 memory + window_switch.json)，已全部在 origin/master
- 自检（第一窗口 23:01 产物）：0 critical / **5 warn** = 四核可用率 0.8/2.1/1.4/0.7% 低水位
  + 镜像失效 11/13（可用 gh-proxy.org / gh.monlor.com）→ 按 known-issues 口径不改代码
- **窗口开关本日恢复启用**：第一窗口 `elapsed_min=53.6 > 50` → `followup_windows` 由 off 转 on
  （`last_resume_at 2026-11-15 23:04`，`streak_done` 已 7/7 但耗时超限故 fail-safe 开启）。
  因此本窗口被触发；闸门 done 说明这次触发是多余的、但符合设计（宁可多跑一次、不可漏跑）
- 内核进程检查：xray / sing-box 均无残留（第一窗口正常收尾，第二窗口未跑内核）
- 观察项：四核可用率合计 126，较 11-14（15/11/…）回升；singbox 17 为近几日低点但仍在 min_available(10) 之上
- 本窗口记忆文件在核查之后写入，产生 1 个纯文档尾巴 → 按「有尾巴就收干净」规则 publish `3b94095`
  推送成功（v2ray @ 202.50.253.54:19999，通道第 1 次命中）；推后 `status` 空、`rev-list` 0/0

## 2026-11-13 采集日（2026-11-14 01:30 运行）

- 闸门退出码 0：四内核「已测满单轮上限」（2513/2504/2511/2510，cap 2500）→ GATE: done
  → 本窗口未采集、未跑验证、未重跑自检、未发布（未占用验证资源）
- 本日可用 v2ray 17 / xray 54 / clash 32 / singbox 38（池 215/693/376/354）；
  CI 原始 166119 → 去重 16853 → 本地 TCP 可达 **5901/5901**（中位 246ms），CF 前置 2004
- 产物核对：available 17/54/32/**39（含 1 条 direct，净 38）** 与 summary 逐项一致；
  `nodes_uris` 5901 = `nodes_meta.total/reachable` 5901；tested_state date=11-13（四核 5766/4670/5517/5154，跨窗口累计）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI 04:52(迟到派发)/09:33/21:12 + 修窗 `66ebd96`(09:39) + 第一窗口 22:54/22:56 + 第二窗口 `63558f0`(23:48)
- 自检（第一窗口 22:54 产物）：0 critical / **5 warn** = 四核可用率 0.7/2.2/1.3/1.5% 低水位
  + 镜像失效 10/13（可用 gh-proxy.com / gh-proxy.org / gh.monlor.com）→ 按 known-issues 口径不改代码
- **11-11 那批「未提交改造」已入库**：`repo_pool.py` 现已在 `git ls-files` 中、工作区干净，
  不再有悬空改动（上次记录的隐患解除）
- 观察项：11-11 的 10 倍采集量（104 万/去重 10.5 万）不是常态，本日回落 16.6 万/16853；
  批量源由 FastNodes 换成 Eleven1985、10Dream（各 40000 条）→ 属上游波动
- 观察项二：去重 16853 → 本地 TCP 可达 5901（**35%**，前几日近 100%）。新增批量源死号多，
  属上游质量；四核可用数与池均在正常水位，不放宽探测/过滤口径
- 本窗口记忆文件在核查之后写，留作下一个发布顺带提交（沿用既有约定，不是故障）

## 2026-11-13 09:26 迟到触发（采集日期仍为 2026-11-10）

- **断档两晚**：11-11、11-12 两晚的三个窗口都没跑（本机离线）。`Docs/summary.json` 与
  `nodes/tested_state.json` 仍是 11-10 22:35，`available_*` 停 11-10 → 本窗口按规则取
  `summary.date=2026-11-10` 作采集日期，闸门仍判 **GATE: done**（v2ray 2261/2254 测完、
  其余三核测满 2500 上限）。这个 done 只代表「11-10 那份数据」，**不代表今晚跑过**
- 本窗口未采集、未探测、未验证（未占用验证资源），也未发布：`git add free-nodes` 会把
  11-11 下午那批未验证的 src 改造一起带上，绝不能推
- 尾巴处理：无 `pending-push.json`，HEAD 原本落后远端 3 个提交（全是 CI 产物），
  已 `git merge --ff-only` 快进到 `a75934c`（CI 采集 2026-11-13）
- **CI 采集量涨 10 倍（11-11 起）**：原始 104 万 → 去重 10.5 万（此前约 1 万）。
  主因单仓 `rtwo2/FastNodes` 10 条链接吐 694,974 条、`pog7x/vpn-configs` 133,623、
  `asgharkapk/...` 68,382。`nodes_uris.txt` 现 117,760 行、`nodes_meta.reachable=0`（CI 不探测，符合口径）
- CI 派发持续漂移：11-11 04:33、11-12 04:17、11-13 04:52（北京），cron 21:05 迟到 7~8h（known-issues 54/58 同型）；
  今日 09:28 另有两次 `workflow_dispatch`（run 33/34），疑为第一/第二窗口迟到后各自派发
- **工作区有 11-11 15:39~16:25 的未提交改造**（`repo_pool.py` 484 行新增 +
  collect/test/layout/pool 共 856 行）：仓库地址池评分/配额、单仓产量上限 `--max-nodes-per-repo`、
  池条目 `repos` 多归属与 `bw_mbps`。py_compile 与 `--help` 通过，**未跑过真实采集 → 不提交**
- 判据留用：**闸门只看 summary，summary 不更新就说明前一晚整条链没跑**——遇到迟到触发（本窗口 09:26）
  先比对 `summary/tested_state` 的 mtime 与 `nodes_uris` 的 mtime，三者停在同一天就是断档，别当成「今晚已跑完」

## 2026-11-10 采集日（2026-11-11 01:30 运行）

- 闸门退出码 0：v2ray「候选已全部测完」（2261/2254）、xray/clash/singbox「已测满单轮上限」
  （2504/2500、2508/2500、2504/2500）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用数 v2ray 24 / xray 55 / clash 33 / singbox 45（池 279/831/516/458）；
  采集总量 9578 → 去重 3090 → TCP 可达 3090/3090（中位 262ms），CF 前置 972
- 产物核对：available 24/55/33/**46（含 1 条 direct，净 45）** 与 summary 的 ok 逐项一致；
  `nodes_uris.txt` 与 `nodes_meta.total/reachable` 均 3090；`tested_state` 四内核 2261/2504/2508/2504（date=11-10）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `baaa13c`(07:07)/`1f7066a`(21:14) + 第一窗口 `b5a4887`(22:39)
  + 第二窗口 `c9b3c8d`(23:47，已把第二窗口记忆带上)，全部在 origin/master
- 自检（第一窗口 22:36 产物）：0 critical / **6 warn** = 四核可用率 1.1/2.2/1.3/1.8% 低水位
  + crashgfw 0 条（下载失败 URLError）+ 镜像失效 10/13（可用 gh-proxy.com / gh-proxy.org / gh.monlor.com）
- **下载失败 8 仓不构成通道故障**：URLError 3 个（crashgfw、HakurouKen、ripaojiedian，分属不同域名）、
  HTTP 403 2 个、HTTP 404 2 个、`clashv2ray-hub` 两仓「空响应」（known-issues 55 生成链未完成）、HTTP 526 1 个
  → 无「同域多仓同时失败」，按 11-03 判据不改采集代码
- 观察项：CI 在 11-10 **07:07** 还有一次「CI 采集 2026-11-10」，属 11-09 侧 cron 迟到派发
  （known-issues 54 同型）；`Docs/report.md` 仅保留 `## 2026-11-10 21:14` 一条，无 `07:07` 残留 → 无需处置
- 本窗口记忆文件在核查之后写，补推后三处重新变干净（见提交 hash）

## 2026-11-09 采集日（2026-11-10 01:30 运行）

- 闸门退出码 0：v2ray「候选已全部测完」（2309/2298）、xray/clash/singbox「已测满单轮上限」
  （2505/2509/2505，cap 2500）→ GATE: done → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用数 v2ray 24 / xray 88 / clash 50 / singbox 42（池 270/797/496/436）；
  采集总量 9298 → 去重 3118 → TCP 可达 3118/3118（中位 233ms），CF 前置 1027
- 产物核对：available 24/88/50/**43（含 1 条 direct，净 42）** 与 summary 逐项一致；
  `nodes_uris.txt` 与 `nodes_meta.total/reachable` 均 3118；`tested_state` 四内核 2309/2505/2509/2505（date=11-09）
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
- 本日发布链：CI `8e40c4c`(02:26)/`aa89c72`(21:11) + 第一窗口 `e103593`(22:41)/`8e3b3d1`(22:44)
  + 第二窗口 `da5da4f`(23:47，仅 automation memory)，已全部在 origin/master
- 自检（第一窗口 22:38 产物）：0 critical / **4 warn** = v2ray 1.0%、clash 2.0%、singbox 1.7% 低水位
  + 镜像失效 10/13（可用 gh-proxy.com / gh-proxy.org / gh.monlor.com）→ 按 known-issues 口径不改代码
- 观察项一：采集总量 9298、去重 3118（昨 8272/2830），仍低于月初 1.1~1.3 万；但 TCP 可达 100%、
  四核可用数均在正常水位，判上游当日产出偏少，非采集故障
- 观察项二：CI 在 11-09 **02:26** 还有一次「CI 采集 2026-11-09」提交，属 11-08 侧 cron 迟到派发
  （known-issues 54 同型，runner 的 `date +%F` 已跨日）。已核对无残留：`Docs/report.md`、
  `collection_logs.md` 中无 `2026-11-09 02:26` 条目（被 21:11 真实采集按日期替换），
  11-08 的 21:11 条目完好 → 无需处置，只作记录
- 本窗口记忆文件在核查之后写，留作下一个发布顺带提交（沿用既有约定，不是故障）

## 2026-11-08 采集日（2026-11-09 01:30 运行）

- 闸门退出码 0：v2ray/xray「候选已全部测完」（2142/2131、2499/2494），
  clash/singbox「已测满单轮上限」（2511/2500、2506/2500），GATE: done
  → 本窗口未采集、未跑验证、未重跑自检（未占用验证资源）
- 本日可用数 v2ray 29 / xray 80 / clash 42 / singbox 45（池 291/779/534/482）；
  采集总量 8272 → 去重 2830 → TCP 可达 2830/2830（中位 217ms）
- 产物核对：available 29/80/42/**46（含 1 条 direct，净 45）** 与 summary 逐项一致；
  `nodes_uris.txt` 与 `nodes_meta.total/reachable` 均 2830
- **尾巴三处全干净**：无 `pending-push.json`、`git status --short -- free-nodes .github` 空、
  `rev-list --left-right --count origin/master...HEAD` = 0/0 → 无需补推
  （第二窗口记忆文件已被 `bec58be`/`94f3a4d` 带上，没有历史常见的记忆尾巴）
- 本日发布链：CI `0a20cdc`/`29535ac` + 第一窗口 `4537be9` + 第二窗口 `94f3a4d`/`bec58be`，已全部在 origin/master
- 自检（第一窗口 22:43 产物）：0 critical / **4 warn** = v2ray 1.4%、clash 1.7%、singbox 1.8% 低水位
  + 镜像失效 11/13（可用 gh-proxy.com / gh-proxy.org）→ 按 known-issues 口径不改代码
- 观察项：采集总量 8272 明显低于前几日 1.1~1.3 万，去重 2830（前日 3817）；
  但 TCP 可达率 100%、四内核可用数均在正常水位之上，判上游当日产出变少，非采集故障
- 本窗口记忆文件在核查之后写，留作下一个发布顺带提交（沿用既有约定，不是故障）

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
