# 上行通道自建代理与 GitHub 发布

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

### 上行通道：用已验证节点自建代理访问 GitHub（uplink.py）

有些网络里 `api.github.com`、`codeload.github.com` 能直连，但 `github.com:443` 被重置——
采集还能靠镜像凑合，`git push` 却完全不通。本机本来就有四个代理内核和一堆已实测可用的
节点，于是脚本自己「拿节点起内核」，把 GitHub 流量交给它。

**建通道的时机（2026-10-26 用户要求）**：从内核检查那一步就开始建，后续步骤不再重复搭建。

| 步骤 | 行为 |
|---|---|
| 1. `check_kernels.py` | **先自建代理再查版本**（查 release 要连 `api.github.com`）。独立运行时结束即关闭；被 `collect_nodes.py --check-kernels` 调用时，通道移交给采集环节 |
| 2. `collect_nodes.py` | 用 `--check-kernels` 时**直接接管第 1 步的通道**（日志里 `[uplink] 通道就绪` 只出现一次）；没接管到才自建。采集结束主动停掉——验证阶段要独占本地端口，而且要测「节点本身」，留着代理既抢端口又污染代理环境变量 |
| 5. `publish_free_nodes.py --proxy auto` | **不探测本机已有代理端口**，直接用已验证节点自建（先尝试接管登记在案的通道，推不通就换节点/换内核），全部失败才直连兜底 |

`--uplink auto` 的自建顺序：

1. **接管已登记通道**：`~/.workbuddy/data/free-nodes-tools/runtime/uplink_session.json`
   （先校验 pid 存活再探活，通了一律直接用，不重新试节点）
2. **自建代理**：候选节点按可靠性排序 —— `nodes/pool/pool_state.json`（实测通过过，ok_count 高、
   best_latency 低优先）→ `nodes/available_<core>.*`（各内核当日可用清单）→ `nodes/nodes_uris.txt` 兜底。
   先做 TCP 预筛，再逐条节点 × 内核（clash → singbox → xray → v2ray）起本地 HTTP 代理，
   用 `https://github.com/` + `https://api.github.com/rate_limit` 双探测，**2xx 才算通**
3. **直连**：一个代理都起不来时才直连（先实测 GitHub 可达性，避免白等）
4. **等 10 分钟重试**：代理和直连都不通，按 `--uplink-retries`（默认 2）等待后从第 2 步重来

> **跨进程复用是尽力而为**：本机执行环境（job 限制）会在父进程退出时回收内核子进程，
> 且 `CREATE_BREAKAWAY_FROM_JOB` 被拒（WinError 5），所以**分步执行**时第 2 步往往接管不到登记通道、
> 只能重建（约 10~30 秒）。要确保「代理只建一次」，用 `collect_nodes.py --check-kernels` 合并跑。

推送到 GitHub（`src/publish_free_nodes.py`）：`--proxy auto` **不探测本机代理端口**，直接自建，
**推不通就换节点、换内核，直到连通**；也可 `--proxy http://127.0.0.1:7890` 指定现成代理。
全部失败则保留本地提交并记录待推送状态。

单独自测一条通道是否可用：

```bash
python <free-nodes>/src/uplink.py <输出根目录>
```
