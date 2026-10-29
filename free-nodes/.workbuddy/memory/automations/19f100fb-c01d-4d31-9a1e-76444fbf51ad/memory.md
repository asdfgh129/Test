# 第三窗口（01:30）执行记忆

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
