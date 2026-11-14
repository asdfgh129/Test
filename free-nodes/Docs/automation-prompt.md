# 定时任务口径（三个窗口）

> **权威来源是自动化里配置的任务指令本身**（id 与 rrule 见下），本文件只是
> 口径摘要 + 变更理由，方便排查「为什么这么配」。两者冲突时以自动化配置为准。
> 最近一次同步：2026-11-04（**不再把 cron 当唯一触发源**：新增 21:05 的本地触发任务，
> cron 降级为「机会性备份」；workflow 守卫改为只认远端产物 + 检出用分支尖端，
> 见 `known-issues.md` 第 58 条）。上一次同步 2026-11-02（CI 加第二条 cron + 统一「产物就绪」判据
> + `ci_dispatch.py` 兜底触发，见第 54 条复核与第 56 条）。
> 旧版这里贴的是「请手动粘贴到自动化」的完整 prompt 全文，2026-10-28 起改为摘要——
> 因为 `automation_update` 工具已可用，prompt 可以直接改，正文再抄一份必然会滞后。

| 窗口 | automation id | 时间 | 职责 |
|---|---|---|---|
| CI 触发（**主路径**） | `03493c45-d356-4882-b007-404b6326b265` | 每天北京 **21:05** | 只跑 `ci_dispatch.py --wait 900`：`workflow_dispatch` 触发采集并等结论，不采集/不改文件/不碰 git |
| CI（采集） | `.github/workflows/collect.yml` | 每天北京 21:05 与 21:20 两条 cron（UTC 13:05 / 13:20），**已降级为备份** | 只采集：下载 → 解析 → 去重 → 落盘，**不探测** |
| 第一窗口（主） | `a3d7bb22-948c-4326-b344-f4c5535ddcd0` | 每天 22:00 | 等 CI 产物 → 内核检查 → 本地 TCP 探测 → 验证 → 自检 → 修复 → 推送 → **闸门 + 第 2/3 窗口开关决策**（`--first-window`） |
| 第二窗口（**当前 PAUSED**） | `a4c4ae9d-9d70-4395-b78d-63a0a131e62d` | 每天 23:45（停用中，不触发） | 闸门判定 →（需要时）续跑验证 → 自检 → 推送 |
| 第三窗口（**当前 PAUSED**） | `19f100fb-c01d-4d31-9a1e-76444fbf51ad` | 每天 01:30（停用中，不触发） | 同第二窗口（跨零点，`--date` 必须取 `Docs/summary.json` 的采集日） |

## 第 2/3 窗口自动开关（2026-11-14 定案，见 known-issues 第 65 条）

**开关只由第一窗口控制**：它每晚收尾跑 `window_gate.py --first-window`，把结果写进
`Docs/window_switch.json` 并输出 `SWITCH: on|off` / `SWITCH_ACTION: pause|resume|keep`；
主窗口用 `automation_update` **只改这两个 automation 的 status** 做幂等对齐
（pause=PAUSED、resume=ACTIVE、keep=不动）。第 2/3 窗口的 prompt 不需要改命令——
不带开关的旧闸门命令现在会先读开关，`off` 时直接输出 `GATE: done` 退出 0。

- **证据**：2026-11-01~11-13 第一窗口连续 13 晚 `GATE: done`，验证耗时 31.8~41.1 分钟；
  第二/三窗口同期每夜都记「未跑验证、未占用验证资源」。初始化时 `--backfill` 从
  `Docs/summary.md` 回填最近 7 个有运行的夜晚（11-05~11-13，11-11/12 本机离线无记录），
  全部达标 ⇒ 2026-11-14 开关置 **off**，两个窗口置 PAUSED。
- **关闭**：最近 `STREAK_REQUIRED=7` 个有运行的夜晚全部 done，且每晚 `elapsed_min ≤ 50`。
  用「有运行的夜晚」而不是连续日历日，是为了不让机器离线的空档永久阻断停用。
- **立即开启**（当夜就要靠后两窗口）：`GATE: continue` / 有 pending 内核 / `partial=true` /
  验证耗时 >50 分钟（窗口吃紧）/ 开关 off 但主窗口断档 ≥2 天（fail-safe）。
- **数据**：`Docs/summary.json` 新增 `elapsed_min` 字段供开关直接读取，不再解析 md 文本；
  开关文件保存 history（每晚 gate/耗时/pending）、`followup_used`（后两窗口被真正用到的记录）、
  最近一次 pause/resume 时间，全部随发布入库，可复盘。
- **边界**：若第一窗口自己连续多晚没运行，三个窗口会一起停摆，没人执行 fail-safe。
  恢复本机后手动把两个 automation 置 ACTIVE，或跑一次 `--check-switch`（按断档自动把开关改回 on）。

**上限调整规则**：现行上限与「结果不理想时按什么顺序提高」见 `Docs/quota.md`；
当前按现状运行，连续 3 晚命中触发条件才动手，一次只动一档并观察 3 晚。

**为什么不再依赖 cron（2026-11-04 定案）**：`schedule` 被平台**稳定**拖后 5~9 小时——连续 4 天，
应派发的 13:05Z/13:20Z 全部落在 18:20Z~22:19Z（北京 02:20~06:19）才启动，而 22:00 那一刻一条
run 都没有；同期权限/分支/YAML/配额全部正常，`workflow_dispatch` 9~11 分钟必成（known-issues 58）。
所以把**触发**从 cron 换成 21:05 的本地任务：22:00 主窗口一开窗即 `CI_READY=1`，省掉每晚约 10 分钟等待；
两条 cron 保留但只当机会性备份（迟到时由 workflow 内的「跳过判定」跳过，不再重复采集）。

**跳过判定只看远端（2026-11-04 改）**：`concurrency` 只保证「后一条等前一条跑完」，但
`actions/checkout` 默认按**事件里的 sha** 检出，排队 run 看不到前一条刚推上去的产物 → 必重复采集、
push 非快进失败（每晚一个红叉）。现在检出用 `ref: ${{ github.ref_name }}`（拿分支尖端），
守卫从 `origin/master` 取 `nodes_meta.json` 喂给 `--ci-status`——判据仍只有一处实现。

**为什么要拆成「CI 采集 / 本地探测」**：CI 解决本机到 GitHub 的通道问题（不再需要 uplink 代理与镜像回退）；
但可达性依赖出口位置，runner 是 Azure 数据中心 IP，会让大量被封数据中心 ASN 的节点变成假阴性。
所以 CI 用 `--no-latency-sort` 只落盘，**TCP 探测与四内核实测留在本地**。

## 关键命令

```bash
# 采集（CI，每天北京 21:05 与 21:20 两条 cron；本地只在 CI 没产出时兜底跑老命令）
python free-nodes/src/collect_nodes.py --out free-nodes --readme-only --no-latency-sort \
  --uplink direct --time-budget 1500 --date $(TZ=Asia/Shanghai date +%F)

# 判「今天的 CI 产物到位没有」（唯一判据实现；不碰 git/网络，退出码 0=就绪 / 1=未就绪）
# 就绪 = nodes_meta.date 是今天 **且** generated_at >= 今天 20:00
#        （或 generated_at 距现在 <= 90 分钟：调度器拖过零点时「今天 20:00」还在未来，
#          这条新鲜度豁免让后一条 cron 不再重复采集，见 known-issues 57）
# 只看 date 会被「跨零点补跑」骗（known-issues 56）：调度器迟到时 runner 的 date +%F 已是明天
python <root>/src/publish_free_nodes.py --ci-status

# 不就绪时主动触发 CI（**主路径**：21:05 的定时任务就是跑这两行；主窗口的兜底也用它）
# api.github.com 直连可用，不用建通道；workflow_dispatch 不看调度队列，9~11 分钟出全套产物
# --check 用一个不存在的 ref 换 422，只验证凭据/路径/权限，不会真的排一次采集
python <root>/src/ci_dispatch.py --check
python <root>/src/ci_dispatch.py --wait 900

# 第一窗口开工第一步：把 CI 提交的采集产物拉到本地（拉取同样要翻墙，复用推送的自建通道）
# 只用 --ff-only，绝不 rebase/reset。实测 2026-10-31：直连 fetch 必然先失败 → 自建通道 → 成功，全程 52 秒
# 退出码 1（拉不下来）：换更大的候选池重试一次 —— 加 --uplink-candidates 120
# candidates() 是确定性排序，原样重试 = 同一批 40 个节点；扩池才取得到第 41~120 个
# 仍失败直接兜底采集，不要空等 15 分钟（本地文件不会自己变新）
# 同步成功后会顺手打印 CI_READY=1|0，等价于再跑一次 --ci-status
python <root>/src/publish_free_nodes.py --sync-only --proxy auto

# 第一窗口：本地 TCP 可达探测（取代原来的采集步骤）
python <root>/src/collect_nodes.py --out <root> --probe-only --latency-workers 128 --latency-timeout 1.5

# 验证（第一窗口；第二/三窗口同参再加 --resume-tested，--cores 只给待补内核）
python <root>/src/test_nodes.py --input <root> --cores v2ray,xray,clash,singbox \
  --full-below 2500 --max-test 2500 --workers 24 --test-timeout 3 --retry 0 \
  --fair-budget --time-budget <5400 - 已用秒数 - 600>

# 收尾闸门（每个窗口都要跑；第三窗口必须带 --date <采集日期>）
# 不带 --date 时闸门自己按本机时钟校验 summary 新鲜度：停在昨天（非凌晨）或更早一律 GATE: continue
python <root>/src/window_gate.py --input <root> [--date <采集日期>]
```

## 口径与依据（2026-10-28 实测）

| 旋钮 | 取值 | 依据 |
|---|---|---|
| 采集是否留死节点 | **不留**（`--keep-dead` 可关） | 16620 条里仅 ~6800 条 TCP 可达；留着只撑大订阅、让验证白跑一半 |
| 单节点验证超时 | **3s** | 昨天可用节点复测：p50 1.39s / p90 1.87s / max 2.24s；3s 误杀 2.5%（2/80，4~5s 慢节点）；12s 会让 95% 的失败节点白等 |
| 失败复测 | **不复测**（`--retry 0`），超时类代码层面永不重试 | 3s 判失败的 117 个里放宽到 12s 只 2 个变可用（1.7%），代价是吞吐腰斩 |
| 单内核并发 | **24** | 12 并发 1.3 节点/s、24 并发 4.9~5.7 节点/s；瓶颈是网络等待不是 CPU（4 核机器够用） |
| TCP 预筛 | **256 并发 / 1.5s** | 64 并发跑 16620 个要 ~8 分钟，会把 `--time-budget` 整块吃光、四个内核全被跳过 |
| 每内核验证量 | **2500** | 4 核 × 2500 ≈ 29 分钟；加上采集 36 分钟 + 自检发布 7 分钟 ≈ 73 分钟，90 分钟红线内有余量 |

时间账（第一窗口，2026-10-31 起）：探测 ~3min + 验证 ~29min + 自检发布 ~7min ≈ 39min（采集已移出本机）。

## 不变量（改参数时别碰）

- **第一窗口第一步必须是 `--sync-only`**：CI 21:05 提交、本地 22:00 探测，不先拉就是探昨天的清单
  （CI 白跑、本地白测），而且拉取同样要翻墙。只用 `--ff-only`，绝不 rebase / reset / stash
  - 硬约束只是「**早于 `--probe-only`**」，不必早于内核检查。**换顺序换不来通道复用**：
    `check_kernels.py` 默认 `close_uplink=True` 命令结束即停通道，`do_sync` 又是「先直连、失败才自建」
    不调 `resume()`；就算都改成复用，`resume` 探活本身要 12 秒，省不下什么（详见 known-issues 第 50 条）
  - 失败分支要分清：**同步成功 + 产物不就绪** = CI 没跑完/被调度器漏了，先 `ci_dispatch.py` 主动触发
    再等（每 60 秒重跑同步，最多 15 分钟）；**同步失败** = 拉不下来，等多久都不会变新，重试一次后直接兜底
  - **不等待的三档**（按「花多少时间换多少新鲜度」排）：① 就绪 → 直接开工；② 不就绪但 `nodes_meta.total > 0`
    → 触发 CI 等 15 分钟后仍不就绪，就**用现有批次开工**并在汇报里写明它的生成时刻（窗口只有 90 分钟，
    为「更新一点」花 1 小时重采不划算）；③ `nodes_meta` 缺失或 `total = 0` → 才走本地兜底采集
  - 重试**必须扩大候选池**（加 `--uplink-candidates 120`）：`candidates()` 按池内质量确定性排序取前 N 个，
    原样重试挑到的是完全同一批 40 个节点，等于白跑
- **按环节分配通道，别一锅炖**（2026-10-31）：内核检查走 `--uplink off` 直连（只访问 api.github.com，
  实测 0.43s 可用，四内核查完 22 秒）；`--probe-only` 完全不碰 GitHub（TCP 握手到节点，纯本地）；
  只有**同步和推送**必须建通道（要 `github.com:443`）。三者共用一个通道既不划算也不需要
  ——`--probe-only` 会 `sys.exit` 在内核检查之前，本来就不可能同进程（详见 known-issues 第 51 条）
- **CI 只采集、不做 TCP 探测**（`--no-latency-sort`）：runner 是数据中心出口，探测会引入系统性假阴性/假阳性。
  要改这一点，先拿同一批节点在 CI 与本地各测一遍，比重合率再决定
- **本地第一窗口必须跑 `--probe-only`**：它同时负责「只留 TCP 可达」与「延迟排序」两件事，
  跳过它就等于把未过滤的候选直接发出去
- **每个窗口收尾必须跑 `window_gate.py`**：判定有四个分支（partial / exhausted / 测满上限 / 漏跑），
  三个窗口必须用同一套标准；第三窗口带 `--date <采集日期>`，否则每晚都判「日期不符」白跑一次。
  不带 `--date` 时闸门自带新鲜度校验（summary 停在昨天且过了 06:00、或更早 ⇒ `GATE: continue`），
  因为 summary 只在**本地跑过验证**时才会更新：本地停跑几晚后，旧 summary 会让闸门永远回 done
  （2026-11-13 实测：本地停跑两晚，闸门拿 11-10 的 summary 回了 done，见 known-issues 61）
- **`--max-test` 不按「怕超时」降级**：要给余量就调 `--time-budget` / `--fair-budget`，
  不要退回 1000/600 那种拍脑袋数字（2026-10-27 用户明确要求）
- **`--fair-budget` 必加**：内核顺序跑，不加会让第一个内核吃光预算、后面三个一个都不测
- **探测地址保持裸域 HTTPS**（`https://gstatic.com/generate_204`）：换成 `www.` 或明文 http
  会测出「假可用」
- **第二/三窗口只用 `--resume-tested`**：`--date` 取 `Docs/summary.json` 的 `date`，
  第三窗口跨零点时尤其不能 `date +%F`
- **口径差异不是 bug**：`Docs/report.md` / `collection_logs.md` 是 CI 口径（含 TCP 不可达），
  `nodes/nodes_uris.txt` / `nodes_meta.json` 是本地探测口径（只含可达）
- 平台对单次运行有 **90 分钟硬上限**（`[CANCELLED] Run timed out`），任务内部改不掉；
  靠 `--time-budget` 让脚本自己收尾 + 增量落盘，不要指望「跑久一点」
- 三个窗口开工前都先 `taskkill` 残留内核（被强杀的窗口会留下 xray/v2ray/mihomo/sing-box 占端口）

## 历史沿革（避免重走弯路）

- 10-25：上限 30000 是笔误，当晚纠正为 3000
- 10-26：把「内核检查 + 采集」合并到同一进程（代理只建一次）
- 10-27：删掉「超 35 分钟就降 `--max-test 600`」的自我设限；加 `--time-budget` /
  `--fair-budget` / `--resume-tested`，靠三窗口接力
- 10-28：定位到真正的成本是「12s 超时 × 复测 × 12 并发」，改为 3s / 不复测 / 24 并发；
  采集侧只发 TCP 可达节点；验证量 3000 → 2500。预期第一窗口即可跑完四内核，
  第二/三窗口退化为兜底
- 10-31：采集搬上 GitHub Actions（直连、免代理、配额 5000/时），CI 用 `--no-latency-sort`
  只落盘；本地新增 `--probe-only` 做可达探测与排序（出口位置决定可达性，探测不能上云）。
  新增 `window_gate.py`：第一窗口跑完后两窗口先判定，跑满就跳过，不再空跑 90 分钟。
  第一窗口的时间账从 73min 降到 ~39min
- 11-02：11-01 那次定时任务被 GitHub 调度器迟了 5h16m（跑到次日 02:20，产物被标成明天的日期，
  当晚白等）。修法三条：CI 加第二条 cron（北京 21:20，必须晚于主 cron 否则每晚都会用到偏旧的数据）互为备份 + workflow 内「跳过判定」；
  「产物就绪」判据收敛到 `publish_free_nodes.py --ci-status`（date 是今天 **且** generated_at ≥ 20:00）；
  新增 `ci_dispatch.py` 走 `workflow_dispatch` 做确定性兜底（`--check` 用不存在的 ref 换 422 验证权限）
- 11-11：架构改造落地（仓库地址池 + 评分 + 多仓库去重登记 + 三步测试 + 弹性测试量），
  11-13 已产出 `Docs/available_nodes.md` / `nodes/available_nodes.json` / `Docs/repo_yield.md`；
  同日修掉带宽 403（第 64 条）
- 11-14：用户拍板「按现状运行，结果不理想再提高上限」→ 新增 `Docs/quota.md` 固化分档顺序；
  「最近一段时间用不到第 2/3 窗口就关掉、时间不够再开启」→ 开关判定固定到第一窗口：
  `window_gate.py --first-window` 写 `Docs/window_switch.json` 并输出 `SWITCH_ACTION`，
  主窗口据此用 `automation_update` 只改后两窗口 status。连续 13 晚未使用后，
  两窗口置 PAUSED（第 65 条）
