# CI 主动触发（workflow_dispatch）每日 21:05

任务：用 `src/ci_dispatch.py --wait 900` 主动 dispatch collect.yml，等其跑完，为 22:00 主窗口预热当天产物。
只触发，不采集/不探测/不改文件/不动 git。

## 执行记录

- 2026-11-04 21:05：首次执行成功。run 41835055159，`in_progress` → `completed (success)`，退出码 0，约 9 分钟内完成。
- 备注：本文件在首跑前不存在；脚本输出中 token 已打码（`ghp_…x6hY`），汇报时同样打码。
- 2026-11-05 21:05：成功。run 42032745579，`in_progress` → `completed (success)`，退出码 0，用时 9m31s。
- 坑（重要）：本机 Bash 是 Git Bash，命令里的 Windows 反斜杠路径会被吃掉（`C:Usersbemin...` → command not found）。
  必须给路径加双引号或改用正斜杠，否则第一个 Bash 调用必失败（本次第一跑即因此空转 0.8s，非 GitHub 侧问题）。
- 2026-11-06 21:05：成功。run 42222801205，`in_progress` → `completed（success）`，退出码 0，全程 8m23s
  （含排队+执行）。路径用正斜杠+双引号一次过。产物在 22:00 主窗口开窗前已就绪。
- 2026-11-07 21:06：成功。run 42375435726，`in_progress` → `completed（success）`，退出码 0，约 6m20s
  （21:06 触发、21:12 收尾）。继续沿用正斜杠+双引号路径写法，未再踩坑。
- 2026-11-08 21:06：成功。run 42483348551，`in_progress` → `completed（success）`，退出码 0，全程 5m50s
  （21:06 触发、21:12 收尾）。`--wait 900` 超过单次 Bash 600s 上限，故用后台运行 + TaskOutput 取结果，稳定可复用。
- 2026-11-09 21:05：成功。run 42622506928，`in_progress` → `completed（success）`，退出码 0，全程 6m4s
  （21:05 触发、21:12 收尾）。沿用正斜杠+双引号路径 + 后台运行 + TaskOutput（timeout 600000）一次过。
- 等待方式定型：`run_in_background=true` 启动后直接 `TaskOutput(timeout=600000)` 阻塞取结果，
  单次即可覆盖 6~10 分钟运行，无需轮询。
- 2026-11-10 21:05：成功。run 42821498553，`in_progress` → `completed（success）`，退出码 0，全程 9m0s
  （21:05 触发、21:15 收尾，是近期最慢的一次但仍未触到 900s 等待上限）。产物应在 22:00 主窗口开窗前就绪。
- 2026-11-13（本次触发实际在上午补跑）：成功。run 43345124362，pending → queued → completed（success），
  退出码 0，全程 6m53s。沿用后台运行 + TaskOutput(600000) 一次过，无新坑。
- 2026-11-13：成功。run 43345124362，`pending` → `completed（success）`，退出码 0，后台运行 7m1s 收尾。
  沿用正斜杠+双引号路径 + run_in_background + TaskOutput(timeout 600000) 定型流程，一次过。
- 2026-11-13 21:05（当晚正式窗口）：成功。run 43430768994，`in_progress` → `completed（success）`，退出码 0，
  后台运行 7m10s（21:06 触发、21:13 收尾）。同一定型流程继续有效，无新坑。
- 2026-11-14 21:05：成功。run 43598070509，触发即 202 排队，`in_progress` → `completed（success）`，退出码 0，
  后台运行 5m42s（近期最快）。产物在 22:00 主窗口开窗前就绪。定型流程继续有效，无新坑。
