# 定时任务口径（三个窗口）

> **权威来源是自动化里配置的任务指令本身**（id 与 rrule 见下），本文件只是
> 口径摘要 + 变更理由，方便排查「为什么这么配」。两者冲突时以自动化配置为准。
> 最近一次同步：2026-10-31（采集搬上 GitHub Actions + 本地 `--probe-only` + 窗口闸门，见 `known-issues.md` 第 50 条）。
> 旧版这里贴的是「请手动粘贴到自动化」的完整 prompt 全文，2026-10-28 起改为摘要——
> 因为 `automation_update` 工具已可用，prompt 可以直接改，正文再抄一份必然会滞后。

| 窗口 | automation id | 时间 | 职责 |
|---|---|---|---|
| CI（采集） | `.github/workflows/collect.yml` | 每天北京 21:05（UTC 13:05） | 只采集：下载 → 解析 → 去重 → 落盘，**不探测** |
| 第一窗口（主） | `a3d7bb22-948c-4326-b344-f4c5535ddcd0` | 每天 22:00 | 等 CI 产物 → 内核检查 → 本地 TCP 探测 → 验证 → 自检 → 修复 → 推送 → 闸门 |
| 第二窗口 | `a4c4ae9d-9d70-4395-b78d-63a0a131e62d` | 每天 23:45 | 闸门判定 →（需要时）续跑验证 → 自检 → 推送 |
| 第三窗口 | `19f100fb-c01d-4d31-9a1e-76444fbf51ad` | 每天 01:30 | 同第二窗口（跨零点，`--date` 必须取 `Docs/summary.json` 的采集日） |

**为什么要拆成「CI 采集 / 本地探测」**：CI 解决本机到 GitHub 的通道问题（不再需要 uplink 代理与镜像回退）；
但可达性依赖出口位置，runner 是 Azure 数据中心 IP，会让大量被封数据中心 ASN 的节点变成假阴性。
所以 CI 用 `--no-latency-sort` 只落盘，**TCP 探测与四内核实测留在本地**。

## 关键命令

```bash
# 采集（CI，每天 21:05；本地只在 CI 没产出时兜底跑老命令）
python free-nodes/src/collect_nodes.py --out free-nodes --readme-only --no-latency-sort \
  --uplink direct --time-budget 1500 --date $(TZ=Asia/Shanghai date +%F)

# 第一窗口开工第一步：把 CI 提交的采集产物拉到本地（拉取同样要翻墙，复用推送的自建通道）
# 只用 --ff-only，绝不 rebase/reset。实测 2026-10-31：直连 fetch 必然先失败 → 自建通道 → 成功，全程 52 秒
# 退出码 1（拉不下来）：换更大的候选池重试一次 —— 加 --uplink-candidates 120
# candidates() 是确定性排序，原样重试 = 同一批 40 个节点；扩池才取得到第 41~120 个
# 仍失败直接兜底采集，不要空等 15 分钟（本地文件不会自己变新）
python <root>/src/publish_free_nodes.py --sync-only --proxy auto

# 第一窗口：本地 TCP 可达探测（取代原来的采集步骤）
python <root>/src/collect_nodes.py --out <root> --probe-only --latency-workers 128 --latency-timeout 1.5

# 验证（第一窗口；第二/三窗口同参再加 --resume-tested，--cores 只给待补内核）
python <root>/src/test_nodes.py --input <root> --cores v2ray,xray,clash,singbox \
  --full-below 2500 --max-test 2500 --workers 24 --test-timeout 3 --retry 0 \
  --fair-budget --time-budget <5400 - 已用秒数 - 600>

# 收尾闸门（每个窗口都要跑；第三窗口必须带 --date <采集日期>）
python <root>/src/window_gate.py --input <root>
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
  - 失败分支要分清：**同步成功 + 日期旧** = CI 没跑完，值得等（每 60 秒重跑同步，最多 15 分钟）；
    **同步失败** = 拉不下来，等多久都不会变新，重试一次后直接兜底采集
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
  三个窗口必须用同一套标准；第三窗口带 `--date <采集日期>`，否则每晚都判「日期不符」白跑一次
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
