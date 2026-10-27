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
