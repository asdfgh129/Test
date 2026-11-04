# CI 主动触发（workflow_dispatch）每日 21:05

任务：用 `src/ci_dispatch.py --wait 900` 主动 dispatch collect.yml，等其跑完，为 22:00 主窗口预热当天产物。
只触发，不采集/不探测/不改文件/不动 git。

## 执行记录

- 2026-11-04 21:05：首次执行成功。run 41835055159，`in_progress` → `completed (success)`，退出码 0，约 9 分钟内完成。
- 备注：本文件在首跑前不存在；脚本输出中 token 已打码（`ghp_…x6hY`），汇报时同样打码。
