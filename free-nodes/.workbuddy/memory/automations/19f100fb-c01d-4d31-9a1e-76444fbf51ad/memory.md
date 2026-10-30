# 第三窗口（01:30）执行记忆

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
