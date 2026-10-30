# proxy.md — 自建四内核代理与节点测试代码组成说明

> 更新：2026-10-25（随内核版本 v2ray 5.53.0 / xray 26.10.21 / mihomo 1.19.33 / sing-box 1.14.4 校准）
> 本文只覆盖「**自建代理**」与「**节点测试**」两条链路的全部代码；采集侧细节见 `Skills/free-nodes-collector/SKILL.md` 与 `Docs/protocol.md`。

## 0. 总体架构

```
                    ┌──────────────────────────────────────────┐
                    │  定时任务（WorkBuddy automation, 22:00）   │
                    └───────┬───────────────────────┬──────────┘
                            ▼                       ▼
        ┌─────────────────────────────┐   ┌──────────────────────────┐
        │ collect_nodes.py（采集）      │   │ tools/publish_free_nodes.py│
        │  └─ uplink.ensure() 前置代理 │   │  └─ uplink.ensure() 推送   │
        └──────────┬──────────────────┘   └──────────┬───────────────┘
                   ▼                                 ▼
        ┌─────────────────────────────┐        github.com（经自建代理）
        │ test_nodes.py（节点实测）     │
        │  ├─ uplink.start() 起代理    │
        │  ├─ build_config() 装填     │
        │  └─ http_via_proxy() 探测   │
        └──────────┬──────────────────┘
                   ▼
        ┌─────────────────────────────┐
        │ pool.py（可用节点池，下一轮   │
        │ 起代理的候选来源）            │
        └─────────────────────────────┘
```

核心思想：**先用上一轮测出来的可用节点起一个本地代理，再让采集 / 测试 / 推送流量走这个代理**。四个内核任选一个，不通换下一个，全不通才直连。

## 1. 内核二进制层（不是代码，但属于本链路组成）

| 路径 | 内容 |
|---|---|
| `C:\Users\bemin\.workbuddy\data\free-nodes-tools\bin\v2ray\v2ray.exe` | v2fly v2ray-core 5.x |
| `...\bin\xray\xray.exe` | XTLS Xray-core 26.x |
| `...\bin\mihomo\mihomo.exe` | Clash.Meta 内核 mihomo（对外统一叫 clash） |
| `...\bin\singbox\sing-box.exe` | SagerNet sing-box |
| `free-nodes/src/kernel_state.json` | `check_kernels.py` 维护的版本/能力指纹状态 |

由 `check_kernels.py` 负责下载安装与更新；四个 exe 均不进 git（`.gitignore` 兜底）。

## 2. 公共基础层 — `scripts/layout.py`

所有脚本共享的常量与纯函数库，**无副作用**（不联网、不起进程）。

| 成员 | 功能 |
|---|---|
| `CORES` | 四内核固定顺序 `["v2ray","xray","clash","singbox"]` |
| `ALIASES` | 内核别名归一（`mihomo→clash`、`hy2→hysteria2` 等） |
| `CORE_BIN` | 内核名 → 二进制目录名（clash → `mihomo`） |
| `SUB_FILE` / `AVAIL_FILE` / `POOL_FILE` | 每内核的订阅文件 / 可用清单 / 池文件命名 |
| `CAPS` | **能力矩阵**：每内核的协议集合、传输层（含「已移除」项）、REALITY/flow 支持、ss 加密白名单、ss 插件白名单 —— 2026-10-25 按内核实测校准 |
| `canon()` / `canon_net()` / `parse_cores()` | 名称归一与 `--cores` 参数解析 |
| `node_facts(uri)` | 把任意节点 URI 解析成事实字典（协议/传输/加密/插件/REALITY/flow），与转换器共用一套规则 |
| `supports(core, uri)` | 五层预筛：协议 → REALITY → flow → 传输 → ss 加密/插件；拿不准就放行，由内核实测终审 |
| `filter_uris(core, uris)` | 批量预筛，写订阅文件前分流用 |
| `split_plugin()` / `canon_plugin()` / `ss_2022_key_ok()` | ss 插件串解析、插件名归一、ss2022 密钥长度校验 |
| `upsert_section()` / `append_changelog()` / `append_issue()` | md 日志时间倒序写入（去重粒度可配） |

## 3. 自建代理层 — `scripts/uplink.py`（核心之一）

职责：用池内可用节点起一个**本地 HTTP 代理**，供采集/测试/推送复用；失败按内核轮换，全败降直连。

| 函数/类 | 功能 |
|---|---|
| `CORE_ORDER` | 内核尝试顺序 `["clash","singbox","xray","v2ray"]` —— 前两个协议覆盖最全，优先消耗 |
| `DEFAULT_PROBES` | 通道可用性判定地址：`https://github.com/`（git push 实际目标）+ `https://api.github.com/rate_limit`（API 通道） |
| `candidates(root, cores, limit)` | 汇总代理候选：**池节点优先**（`nodes/pool/pool_<core>.<ext>`），池空再从近期可用清单补 |
| `_cores_for(node)` | 节点协议 → 可用内核映射（读 `layout.CAPS`：hysteria2 现四内核都试，顺序 clash→singbox→xray→v2ray） |
| `class Uplink` | 一次代理会话：`core`（所用内核）、`uri`（节点）、`port`（本地端口）、`url`（`http://127.0.0.1:port`）、`proc`（进程句柄）、`stop()` |
| `_free_port()` | 从 26000 起找空闲本地端口 |
| `build_one(core, uri, ...)` | **单节点起核**：调 `test_nodes.build_config()` 生成配置 → 启动内核（`CREATE_NO_WINDOW`）→ `_probe()` 实测探测地址拿 2xx 才算成功 |
| `_probe(port, urls, timeout)` | 借用 `test_nodes.http_via_proxy()` 走刚起的代理访问探测地址 |
| `start(root, ...)` | 候选逐条尝试：TCP 预筛（`tcp_alive`）→ 起核 → 探测；`skip` 参数支持「通了但 git 还失败」时换一批节点重试 |
| `set_proxy_env(url)` / `install_opener(url)` | 把代理写进进程环境变量（git 子进程自动继承）+ 装 urllib 全局 opener（采集/下载流量自动走代理）；传空串 = 强制直连 |
| `direct_ok()` | 临时清空代理变量后直连实测探测地址；**区分** api.github.com 通但 github.com 不通的情况（采集可继续，push 需代理） |
| `ensure(root, ...)` | 对外主入口：`start()` 起代理 → 失败且直连通 → 返回 direct → 都不通等 `retry_wait` 秒重试，最多 `retries` 次。返回 `(mode, uplink)`，调用方用完必须 `uplink.stop(up)` |

**使用方**：`collect_nodes.py`（采集前置）、`src/publish_free_nodes.py`（git push）、`test_nodes.py` 推测阶段（可选）。通道是**全局 opener**，所以搜索 API 与订阅下载都走代理，不只是下载。

## 4. 节点测试层 — `scripts/test_nodes.py`（核心之二）

职责：对每个内核，把节点 URI **按内核官方规范装填成临时配置**，真实启动内核、从本地代理发起请求，判定可用性并记录失败原因。

### 4.1 内核规格与预检

| 成员 | 功能 |
|---|---|
| `CORES` | 每内核的启动规格：exe 路径、配置格式（json/yaml）、启动参数（`run -c` / `-f`）、协议与 REALITY 能力（引用 `layout.CAPS`）；含历史别名 `mihomo` |
| `DEFAULT_TOOLS` | 内核二进制目录默认路径 |
| `check_config(core, exe, path)` | **配置预校验**：调用各内核自带的 config check 子命令（v2ray `test -c`、xray `-test -config`、mihomo `-t -f`、sing-box `check -c`）—— 在启动前就拦截参数错误 |
| `detect_core_features(core, exe)` | **内核能力指纹探测**：用探针配置实测内核行为，当前探测 `allow_insecure`（Xray 26.x 已移除该字段，写了即启动失败）；结果缓存 |
| `RATE_PRIOR` | 未实测仓库取样时的中性可用率先验（0.25） |

### 4.2 配置装填（URI → 内核配置）

| 成员 | 功能 |
|---|---|
| `_v2_stream()` / `_stream_settings()` | v2ray/xray 的 streamSettings 装填：REALITY（publicKey/shortId/fingerprint）与 TLS 分路；`allow_insecure` 按内核实测结果决定是否写；不认识的传输**直接判不支持**（禁止静默降级成 tcp） |
| `uri_to_v2ray_outbound()` | vmess(JSON base64)/vless/trojan/ss → v2ray/xray outbound；`user:pass` 双段解析（tuic 等）；REALITY 参数逐字段保真 |
| `build_config(core, uri, port)` | **统一入口**：按内核分发装填 —— clash 走 `collect_nodes.uri_to_clash()`，singbox 走 `uri_to_singbox()`，v2ray/xray 走本地转换器；失败返回 None（计为 config 类原因，**不计入节点不可达**） |

### 4.3 实测执行

| 成员 | 功能 |
|---|---|
| `load_sub_uris()` / `node_proto()` / `load_core_keys()` | 读订阅清单、取协议名、按协议轮转取样（保证每种协议都有代表进测试样本） |
| `tcp_alive()` / `tcp_prefilter()` | 一级 TCP 预筛：高并发测 `host:port` 可连，2s 超时，快速剔除死节点 |
| `class PortAllocator` | 本地监听端口分配器，避免并发测试端口冲突 |
| `wait_port(port, timeout)` | 等内核监听端口就绪（启动判定） |
| `class _NoRedirect` | 阻止 urllib 跟随 3xx —— 重定向不算可用 |
| `http_via_proxy(port, url, timeout)` | **二级真测**：通过刚起的本地代理访问 `https://gstatic.com/generate_204`（裸域 HTTPS，必须真出境才可能 204）；只认 2xx；返回 4 元组 `(ok, latency, code, err_desc)`，`err_desc` 供失败分类 |
| `classify_failure(log_text, note)` | **失败原因分类**：内核日志 + 客户端错误描述 → `unsupported / config / startup / tls / auth / refused / reset / timeout / http`；只有节点侧原因（tls/auth/refused/reset/timeout/http）才计入不可达，我们自己的装填错误单独统计 |
| `_read_log()` | 收集内核 stdout/stderr 日志供分类 |

### 4.4 编排与产出

| 成员 | 功能 |
|---|---|
| `test_one()` | 单节点完整流程：分配端口 → `build_config` → 预校验（失败记 config）→ 启动内核 → 等端口 → 探测 → 失败**二次复测**（区分偶发网络抖动）→ 分类 → 清理临时目录 |
| `test_core()` | 单内核并发实测一批节点（ThreadPoolExecutor），收集可用结果与全部明细 |
| 全量测试循环（main 内，默认） | 某内核候选 ≤ `--full-below`(3000) 时**全部测试**；超过则只测排序前 `--max-test`(3000) 个。排序 = 协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序（TCP 不通的已在预筛剔除）。加 `--no-full-test` 回到旧的「可用数 < `--min-available`(10) 沿序追加，上限 limit×5、时间预算 1800s」模式；候选测完记 `exhausted=true` |
| `write_core_outputs()` | 写 `nodes/available_<core>.<ext>`（按延迟排序） |
| `write_summary()` | 写 `Docs/summary.md` / `Docs/summary.json`：测试数、可用数、可用率、测试策略与轮次、**失败原因分布**、候选是否测完 |

## 5. 数据支撑层

### `scripts/pool.py`（VERSION=2）
| 成员 | 功能 |
|---|---|
| `load_state()` / `save_state()` | `nodes/pool/pool_state.json`：12 字段元数据（每内核总数、最近可用时间等，不复制节点列表） |
| `load()` / `merge()` / `prune()` | 池读写、把本轮测试结果并入（含延迟/可用率）、14 天淘汰 + 单内核 3000 上限 |
| `_write_pool_file()` | 写 `nodes/pool/pool_<core>.<ext>`（起代理的候选来源） |
| `retest_candidates()` | 池内优先复测节点（最近可用过的先测） |
| `all_uris()` / `summary_lines()` | 汇总全部 URI / 生成 md 汇报段落 |

### `scripts/collect_nodes.py`（与代理/测试相关的部分）
| 成员 | 功能 |
|---|---|
| `uri_to_clash(uri, name)` | URI → mihomo 代理字典（REALITY、xhttp/httpupgrade 传输、ss 插件全字段保真） |
| `uri_to_singbox(uri, tag)` | URI → sing-box outbound（uTLS 强制、QUIC 传输要求 TLS 等规范细节都在这） |
| `singbox_to_uri()` / `clash_to_uri()` | 反向转换（sing-box 订阅 / clash 配置 → 标准 URI），保证单文件制输出 |
| `main()` | 采集主流程：`uplink.ensure()` 前置代理 → GitHub 搜索/README 提取 → 下载订阅 → 按 CAPS 分流写四内核文件 → 可选触发测试 |

## 6. 维护与回归层

| 脚本 | 功能 |
|---|---|
| `check_kernels.py` | 内核更新检查 + 自动安装；**能力指纹探测**（REALITY pbk、allowInsecure 等探针配置实测），指纹漂移写进 `src/kernel_state.json` 并告警 |
| `protocol_check.py` | **一致性回归**：56 个「URI → 装填 → 内核 config check」用例 + ss 加密白名单核对，验证转换器与四内核当前版本完全一致；内核升级后必跑 |
| `health_check.py` | 产物自检：文件齐全性、可用率合理性、失败原因分布（config/unsupported 占比过高说明装填有问题）、镜像/配额/趋势等；输出 `Docs/health_check.md` |
| `package_skill.py` | 重打包技能 zip |
| `Docs/known-issues.md` | 24 条踩坑记录（每条含复现特征与修复方式） |
| `Docs/protocol.md` | 四内核解析参数规范（与本文配套，讲「怎么装填」；本文讲「哪些代码负责装填」） |

## 7. 调用方

| 文件 | 与本链路的关系 |
|---|---|
| `src/publish_free_nodes.py` | 发布订阅到仓库；push 前 `uplink.ensure()` 起代理（脚本自身就在 src/ 里，提交即带上最新版，无需同步），git 子进程经环境变量走代理；失败写 pending 标记下次补推 |
| WorkBuddy 定时任务 | 22:00 调 `collect_nodes.py --readme-only --test ...`，串起「代理 → 采集 → 测试 → 池更新 → 发布」全链路 |

## 8. 典型运行链路（节点测试部分）

```bash
python scripts/collect_nodes.py \
  --out free-nodes --readme-only --test \
  --test-full-below 2500 --test-max-test 2500 \
  --max-repos 80 --search-pages 2 --search-days 3 \
  --readme-date-tolerance 0
```

单测节点测试（不采集；默认即全量测试）：

```bash
python scripts/test_nodes.py \
  --input free-nodes --out free-nodes \
  --cores v2ray,xray,clash,singbox \
  --full-below 2500 --max-test 2500 --workers 24 \
  --test-url https://gstatic.com/generate_204 --test-timeout 3 --retry 0
```

> 验证口径以 `Docs/known-issues.md` 第 40 条为准：2500 取样上限 / 3s 超时 / 24 并发 / `--retry 0`
> （10-28 由 3000 与 12s、12 并发下调，实测依据在该条里）。

回到旧的限量取样 + 自适应扩量模式：

```bash
python scripts/test_nodes.py \
  --input free-nodes --out free-nodes \
  --no-full-test --limit 200 --min-available 10 --workers 12
```

## 9. 依赖关系

```
layout.py ─────────────────────────────────────┐
    │                                          │
    ▼                                          ▼
collect_nodes.py ◄── uplink.py ──► test_nodes.py
    │                  │                │
    │                  ├────────────────┤
    ▼                  ▼                ▼
 pool.py          git/push          nodes/available_*.*
（下一轮起        （publish 脚本）    Docs/summary.md/json
 代理的候选）                        nodes/pool/pool_*.*
```

- `uplink.py` 同时依赖 `collect_nodes`（网络工具）与 `test_nodes`（起核+探测），是两条链路的粘合层
- 所有配置装填逻辑只有**一份真源**：`layout.node_facts()` 定义「节点是什么」，各转换器定义「怎么装填」，`protocol_check.py` 保证两者与内核一致
