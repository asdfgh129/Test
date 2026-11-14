# 现行上限口径与调整规则

> 用户口径（2026-11-14）：**按现状运行，根据结果再来调整；以后结果不理想就提高上限**。
> 本文是「什么时候调、先调哪个、调完怎么验」的唯一说明。当前**不改任何参数**，只固定规则。
> 每次实际调整都要在根 `CHANGELOGS.md` 写小节，并在 `Docs/known-issues.md` 追加编号条目，
> 注明依据的是哪几晚的哪个数字；禁止凭感觉调参（历史教训见第 40 条）。

## 一、现行上限（2026-11-14 生效值）

| 环节 | 参数 / 常量 | 现值 | 位置 | 作用 |
|---|---|---|---|---|
| 验证量 | `--max-test` / `layout.MAX_TEST` | **2500** / 内核 | `src/layout.py:133`、`src/test_nodes.py:68` | 候选超过 2500 时只测排序前 2500 |
| 验证量下限 | `--min-test` | 800 | `src/test_nodes.py` | 弹性反推的下限 |
| 弹性目标 | `--target-avail` | 30 个 / 内核 | `src/test_nodes.py` | 反推「要达到 30 个可用需测多少」 |
| 带宽覆盖 | `DEFAULT_BW_MAX` | **20** / 内核 | `src/test_nodes.py:647` | 只测主目标+≥1 附加目标里延迟最低的 20 个 |
| 带宽预算 | `DEFAULT_BW_BUDGET` | 240 秒 / 内核 | `src/test_nodes.py:648` | 串行 2MB 下载的墙钟上限 |
| 带宽单次 | `DEFAULT_BW_BYTES` / `DEFAULT_BW_TIMEOUT` | 2MB / 15 秒 | `src/test_nodes.py:645-646` | 慢节点按已下载字节折算 Mbps |
| 采集仓库数 | `--max-repos` | 80（弹性 80~120） | `src/collect_nodes.py` | 池内按评分取前 N 个仓库 |
| 单仓节点上限 | `--max-nodes-per-repo` | 40000 | `src/collect_nodes.py` | 防单仓吞掉整轮（第 62 条） |
| 仓库池 | `STALE_DAYS` / `SCORE_W` | 5 天 / 40·25·20·15 | `src/repo_pool.py` | 5 天没 push 出池；评分权重 |
| 窗口开关 | `STREAK_REQUIRED` / `MAX_ELAPSED_MIN` / `STALE_DAYS` | 7 晚 / 50 分钟 / 2 天 | `src/window_gate.py` | 第 2/3 窗口自动停用与恢复 |
| 单窗口墙钟 | `--time-budget` | `5400 - 已用秒 - 600` | 主窗口 prompt | 平台 90 分钟硬上限前主动收尾 |

**明确不动的口径**（实测定死，调了会破坏可比性）：`--test-timeout 3`、`--workers 24`、`--retry 0`、
`--fair-budget`、多目标主判据 `gstatic/generate_204`、只发 TCP 可达节点、CF 前置排末尾、
仓库评分的「产量按仓库数均分」。`--max-test 2500` 属于**可调上限**，但提高它必须先看过下面的触发条件。

## 二、什么算「结果不理想」（连续 3 晚命中任一才动手）

判据全部来自已有产物，不需要新埋点：

| 信号 | 从哪读 | 阈值 |
|---|---|---|
| 可用总量持续走低 | `Docs/summary.json` 四核 `ok` 之和 | 连续 3 晚 < **60**，且同期 TCP 可达数没有同步下降 |
| 某内核长期低产 | `summary.json` 单核 `ok` 与 `exhausted` | 连续 3 晚 < **10** 且 `exhausted=true`（源池质量问题，见第 4 节） |
| 时间不够 / 没测完 | `summary.json` 的 `partial`、`Docs/window_switch.json` 的 `followup_used` | 连续 3 晚 `partial=true` 或第 2/3 窗口被恢复启用 |
| 候选没测完 | `summary.json` 单核 `exhausted=false` 且 `tested >= cap` | 连续 3 晚四核全部因 cap 被截断 |
| 带宽数据太少 | `Docs/available_nodes.md` 带宽列有数值的行数 | 连续 3 晚 < **20** 行（或 `bw.ok == 0`） |
| 自检同类告警 | `Docs/health_check.md` | 同一条 warn 连续 3 晚出现且已排除环境原因 |

单晚波动（某天可用数掉一半、镜像全挂、上游仓库换源）**不算**，先看 3 晚。
`TCP 可达率` 明显下降导致的可用数下降属于上游质量，去调 `collect_nodes.py` 的源池/链接配额，
不要靠加大验证量硬凑（第 40 条、第 62 条）。

## 三、提高上限的顺序（一次只动一档，观察 3 晚）

按「先补信息、再加测试量、最后扩源池」排，避免一上来把窗口撑爆：

1. **带宽覆盖不够** → `DEFAULT_BW_MAX 20 → 40`，`DEFAULT_BW_BUDGET 240 → 360`。
   只影响可用节点里的一小撮，成本可控；若 403/超时占比 >30%，先按第 64 条查请求头与原因分类，别先调量。
2. **候选被 cap 截断且时间还有余量**（首窗总耗时 < 40 分钟）→ `layout.MAX_TEST 2500 → 3000`，
   主窗口与第 2/3 窗口的 `--max-test` 一起改（三处必须同步，否则口径打架）。
   提高后必须先确认 `--time-budget` 仍有 ≥10 分钟余量给自检+发布。
3. **弹性反推永远顶到上限**（`Docs/summary.md` 里每晚都写「取 2500」）→ 这是可用率过低导致的，
   **不要提高 `--target-avail`**（只会更顶）；要么接受固定 2500 并在 `known-issues` 记结论，
   要么按第 2 档抬高 `MAX_TEST`。
4. **源池不够**（去重后条数连续走低、`Docs/repo_yield.md` 里高分仓产量普遍下降）→
   `--max-repos 80 → 120`、`--search-pages 2 → 3`，并复核 `repo_pool.py` 的 5 天出池没有误杀活跃仓库。
5. **窗口频繁不够用**（第 2/3 窗口一个月内被恢复 ≥3 次）→ 收紧开关口径而不是放宽：
   `MAX_ELAPSED_MIN 50 → 45`（更早让后两窗口待命）或 `STREAK_REQUIRED 7 → 10`（更谨慎地停用）。

每档调整后固定做三件事：① 当晚跑一次 `health_check.py` 确认没有新 critical；
② 连续观察 3 晚的「首窗总耗时 / 四核可用数 / GATE 结论」；③ 没有改善就回退该档，别叠加下一档。

## 四、不属于「提高上限」能解决的问题

- `exhausted=true` 且可用数仍 < 10：候选已全测完，是源池质量，加测试量没有意义。
- 带宽全 0 且失败原因是 403：请求头问题（第 64 条），不是测得太少。
- `GATE: continue` 由本机断档 / CI 产物迟到引起：走 `--sync-only`、`--ci-status`、`ci_dispatch.py` 的兜底分支，
  不要靠延长 `--time-budget` 硬扛平台 90 分钟上限。
- 某内核可用率骤降但 `config_error` 同步升高：先查内核版本/能力指纹（`check_kernels.py`），不是量的问题。

## 五、窗口开关的边界

开关只由第一窗口 `--first-window` 写 `Docs/window_switch.json`，第 2/3 窗口只读。
`--check-switch`（以及不带任何开关的旧闸门命令）在 `off` 时直接输出 `GATE: done` 并退出 0，
所以即便平台状态漂移、后两窗口被误触发，也不会空转验证。

一个已知边界：**若第一窗口本身连续多晚没运行**（机器离线 / 平台取消），而第 2/3 窗口又处于 PAUSED，
没有窗口能执行 fail-safe 恢复。此时需要在恢复本机后手动把两个 automation 置回 ACTIVE，
或跑一次 `window_gate.py --check-switch`（它会按「主窗口断档 ≥2 天」自动把开关改回 on）。
