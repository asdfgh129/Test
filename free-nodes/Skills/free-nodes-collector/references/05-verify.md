# 节点可用性验证全流程、探测口径、协议回归、取样排序、重定向安全

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

## 节点可用性验证（test_nodes.py）

采集完成后可自动验证节点是否真的可用，并按代理内核分别输出可用清单。

### 内核环境

四个代理内核的可执行文件**不在技能包内**（约 248MB），存放在用户数据目录 `~/.workbuddy/data/free-nodes-tools/bin/`：

| 对外名 | 目录/可执行 | 二进制自报名 | 支持协议 |
|---|---|---|---|
| `v2ray` | `v2ray/v2ray.exe` | v2fly | vmess / vless / trojan / ss / hysteria2（无 REALITY；hysteria2 需两层装填，见 protocol.md §3.6） |
| `xray` | `xray/xray.exe` | Xray-core | vmess / vless / trojan / ss / hysteria2（含 reality / flow / xhttp；hysteria2 需 `hysteria`+`version:2` 装填，见 protocol.md §3.6） |
| `clash` | `mihomo/mihomo.exe` | mihomo | vmess / vless / trojan / ss / ssr / hysteria2 / tuic |
| `singbox` | `singbox/sing-box.exe` | sing-box | vmess / vless / trojan / ss / hysteria2 / tuic |

对外统一用 `v2ray` / `xray` / `clash` / `singbox` 四个名字（文件名、`--cores` 参数、日志、产物都用这套）；`mihomo`、`meta`、`v2fly`、`sing-box`、`sb` 等旧写法由 `layout.canon()` 归一，其中 **`mihomo` → `clash`**（同一个内核，避免两套名字各写一份产物）。

脚本查找顺序：`FREE_NODES_TOOLS` 环境变量 → 用户数据目录 `~/.workbuddy/data/free-nodes-tools/bin`。内核缺失时该内核自动跳过（不影响其他内核）。部署/升级方法见 `Docs/tools-setup.md`。

### 验证流程（TCP 预筛 + 全量实测 + 失败分层）

1. **TCP 预筛**：高并发（默认 256）测试服务器 `host:port` 是否可连，1.5s 超时，快速剔除死节点。
   采集侧默认已只发布 TCP 可达节点（`--keep-dead` 可关闭），这里的预筛只是复核「采集到验证之间新死的」
2. **内核实测（默认全量策略）**：对每个内核，候选 ≤ `--full-below`（2500）个时**全部测试**；超过则只测排序前 `--max-test`（2500）个。排序 = 协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序。每个节点生成该内核的临时配置 → 启动内核 → 通过本地 HTTP 代理访问 `https://gstatic.com/generate_204`（裸域 HTTPS，走代理访问，只有真正把流量送出境外才可能返回 204）→ 判定可用并记录延迟。**超时 3s，超过即判失败不再等**（并发 24）
3. **限量模式（可选）**：加 `--no-full-test` 回到旧行为——每内核单轮 `--limit`（200）个初始取样，可用数低于 `--min-available`（10）时顺着同一顺序追加，直到达标 / 候选耗尽 / 触到单内核上限 / 时间预算用完。测试策略与轮次写进 `Docs/summary.md` / `Docs/summary.json`
4. **失败分层**（决定"测不过"到底赖谁）：
   - `unsupported`：能力预筛或转换器判定该内核无法表达（协议/传输/加密/插件/残缺公钥）→ **不发布、不计入不可达**
   - `config`：配置生成出来了但被内核校验拒绝（参数不符）→ 同上
   - `tls` / `auth` / `refused` / `reset` / `timeout`：内核日志与客户端异常文本都指向节点侧 → 计入不可达
   - 超时类不重试；其他网络类失败按 `--retry`（**默认 0，不复测**）控制。实测 3s 判失败的 117 个节点里放宽到 12s 只有 2 个变可用（1.7%），而复测一次要多花一整个超时、吞吐腰斩
5. **增量落盘（抗强杀）**：每个内核测完立刻写一次 `available_<core>.*`、`Docs/summary.*`、
   仓库质量与 `nodes/pool/pool_state.json`。平台对单次运行有 **90 分钟硬上限**
   （超时消息 `[CANCELLED] Run timed out`，见 known-issues 第 31/36 条），
   被强杀时**已完成的内核不会白跑**，也不会出现「一个内核是新数字、其余是旧数字」的混合状态。
   想主动在强杀前收尾（例如给发布留 10 分钟），加 `--time-budget <秒>`：到期不再提交新节点、
   跳过未开始的内核，`summary.md` 会标「本轮未跑完（墙钟预算到期主动收尾，不是失败）」，
   下次用 `--cores <剩余内核>` 补跑即可。**默认 0 = 不限，不要用固定测试量去硬压**
6. **多窗口续跑（`--resume-tested`）**：一个 90 分钟窗口往往测不完四个内核，
   就把一夜拆成 2~3 个窗口接力（22:00 采集+验证 / 23:45 续跑 / 01:30 再续跑）。
   加了这个开关后：
   - 读 `nodes/tested_state.json`，**跳过本日已测过的 host:port**，只测排序里的下一批候选
     ——否则下个窗口会从排序头部重测一遍，90 分钟全花在重复劳动上；
   - 每测完一个内核就把已测清单写回该文件（按日期自动重置，跨天不继承）；
   - **把前面窗口已验证可用的节点并回** `available_<core>.*` 与汇总，
     否则后续窗口只测到排序尾部的差节点，会把可用清单覆盖成更少甚至 0 条
     （实测踩过：第二轮测 96 个全不可用，第一轮的 20 个可用节点被冲掉）；
   - `summary.json` 里该内核的 `tested` 记的是**本日累计**（各窗口去重后），
     `partial` 只针对本窗口，所以「测了多少」看 `tested`、「这轮跑完没」看 `partial` +
     `summary.md` 的「本轮未跑完」说明。
   多个窗口写同一份汇总时，`Docs/summary.*` 会**累积同一天前面窗口的内核结果**，
   不会因为本窗口只测了 clash 就把 v2ray 从汇总里抹掉。
7. **按内核均分墙钟（`--fair-budget`，推荐第二/第三窗口都加）**：内核是**顺序**跑的，
   而 `--time-budget` 原先对每个内核都用「整轮剩余时间」，于是候选多的第一个内核会把预算吃光，
   后面的内核直接「预算已用满，跳过」（2026-10-27 首窗口：v2ray 吃满 2321s，
   xray/clash/singbox 当天零数据，available 文件停在前一天，见 known-issues 第 38 条）。
   开了这个开关就把剩余墙钟按「本内核 + 后面还没跑的内核数」均分，每个内核开始时重算，
   前面内核提前测完的空档自动被后面吸收。**只改时间分配，不改取样口径**
   （`--full-below` / `--max-test` 仍是 2500）。取舍是「四个内核都有当天新数据」
   优先于「一个内核测满」——免费节点的价值在新鲜度。

判定口径与每类原因的原文证据见 `Docs/protocol.md` 第 4 节；`Docs/summary.md` 会给出
「不支持 / 配置错误 / 不可达」三列与「失败原因分布」表——成片 `config` 是转换器有 Bug，
成片 `unsupported` 是能力矩阵要跟内核对齐，都不代表节点质量下降。

### 运行方式

```bash
# 单独验证已有采集结果（默认全量测试：候选 ≤2500 全测，超过测排序前 2500 个）
python <free-nodes>/src/test_nodes.py --input <输出根目录> --cores v2ray,xray,clash,singbox

# 采集时自动验证（默认即全量测试，可显式传阈值）
python <free-nodes>/src/collect_nodes.py --out <输出根目录> --test --test-full-below 2500 --test-max-test 2500

# 第二个/第三个窗口续跑：接着测本日还没测过的候选，并累积当日已可用的节点
# --fair-budget 把剩余墙钟按内核数均分，避免第一个内核吃光预算、后面内核零数据
python <free-nodes>/src/test_nodes.py --input <输出根目录> --cores v2ray,xray,clash,singbox \
  --resume-tested --time-budget 4800 --fair-budget --date <采集当天日期>

# 跨零点收尾时，自检也必须带 --date <采集日>，否则会另起一天的小节（本次踩过：
# 23:45 起跑、00:57 跑完自检 → 数据记到了 2026-10-28 名下）
python <free-nodes>/src/health_check.py --dir <输出根目录> --date <采集当天日期>
```

#### 探测地址为什么用裸域 HTTPS

默认 `https://gstatic.com/generate_204`。三个条件缺一不可：

| 条件 | 反面例子 | 为什么不能用 |
|---|---|---|
| **裸域**（不带 www） | `www.gstatic.com` | 它解析到 `120.253.253.34`（国内 Google 缓存节点），**本机直连就返回 204/111ms**，毫无区分度——国内中转节点、甚至走直连规则的节点都会被判成"可用" |
| **HTTPS** | `http://...` | 明文请求可被节点/中间人篡改，"通过"不可信；且宿主的「明文 HTTP 需确认」规则会弹窗打断自动化；真实翻墙场景里网页全是 HTTPS |
| **走代理** | 直连 | 直连测的是本机网络，不是节点 |

裸域 `gstatic.com` 只解析到海外 IP（`142.250.196.195`），**本机直连 10s 超时**（实测），只有真正把流量送出境外才拿得到 204。

**这不是"更严"而是"更真"**：实测 6 个节点对比，`www + 明文 http` 全部 6/6 通过；裸域 HTTPS 只有 4/6 通过，
多出来的两个节点 HTTPS 表现是「连接被重置」「TLS 握手超时」——现在网页全走 HTTPS，它们实际不可用，属于假可用。

代价是耗时更长（要真出境），所以超时要给足——但 2026-10-28 实测把口径定了下来：
拿昨天**已验证可用**的 80 个节点复测，单节点 HTTP 耗时 p50=1.39s / p90=1.87s / max=2.24s，
`--test-timeout 3` 只误杀 2.5%（2/80，都是 4~5s 才返回的慢节点）；而超时节点从 12s 降到 3s，
单节点成本直接砍掉四分之三。所以 `--test-timeout` 默认 **3s**、并发默认 **24**
（实测 12 并发 1.3 节点/s、24 并发 4.9~5.7 节点/s，瓶颈是网络等待不是 CPU）。
需要换探测点时用 `--test-url`，维持「裸域域名的 HTTPS 地址」即可，例如 `--test-url https://www.google.com/generate_204`。

`--retry`（默认 **0**，不复测）控制网络类失败的复测次数；`--startup-timeout`（默认 6s）是内核端口就绪等待，
超时不足以区分「内核启动慢」和「配置被拒」，所以失败时会再用内核实测校验命令复核一次。
实测复测收益只有 1.7%（3s 判失败的 117 个里 12s 下仅 2 个变可用），代价是吞吐腰斩，不值得。

### 协议一致性回归（protocol_check.py）

改了转换器、或内核升级之后跑一次：

```bash
python <free-nodes>/src/protocol_check.py            # 全量
python <free-nodes>/src/protocol_check.py --core xray --verbose
```

它检查三件事，任何一项不通过都说明「生成的配置不再是内核当前版本的正确用法」：

1. **样本矩阵**：29 组「协议 × 传输 × 安全层 × 插件」逐内核生成配置并跑内核校验，
   预期支持却生成失败 / 校验不过即失败；预期不支持的组合若被生成出来也算失败
2. **参数保真**：生成出的配置里 `network` / `transport` 必须与 URI 声明一致
   （防止历史 bug「未知传输静默退化成 tcp」复现）
3. **加密方式**：ss 各 cipher 逐个交给内核，与 `layout.CAPS[*]["ss_ciphers"]` 白名单比对

退出码 `0` 一致 / `1` 有不一致（改转换器或 CAPS）/ `2` 内核缺失。规范细节见 `Docs/protocol.md`。

### 取样与排序策略

1. 读取 `nodes_meta.json`，给每个节点带上 `repo`、采集时的 `tcp_latency` 与 `cf`（是否 CF 前置）
2. TCP 预筛顺带记录真实握手延迟
3. 按协议分桶，**桶内排序键 = 仓库实测可用率（高→低，未知走 25% 先验）→ 非 CF 优先 → 延迟升序**，再轮转取样：
   - 优先测高质量仓库的节点（这是「优先采集高质量仓库」在验证环节的落地）
   - CF 前置节点只做补位（否则 200 个样本全是握手 20ms 的死节点，可用数会从十几个掉到 0-3 个，见 known-issues 9e）
4. 每内核额外复测池内节点（`--pool-retest`，默认 40 个），通过的直接进当日可用清单

常用参数：`--seed-file`（回写仓库质量）、`--pool-dir` / `--pool-retest` / `--pool-days` / `--pool-max`、`--no-pool`、`--date`。

### 验证安全：不跟随节点重定向

验证时是**拿节点的本地代理端口**去请求 `https://gstatic.com/generate_204`（可用 `--test-url` 改）。
被测节点完全可以把这条请求 302/301 到任意站点——一旦跟随，就等于**替这个节点去访问了那个域名**：
既把本机 IP 暴露给第三方，也可能触发宿主系统的网络拦截弹窗，打断自动化。
注意默认地址改成 HTTPS 只解决了「我们自己发明文 HTTP」，**并不能阻止节点把跳转目标指向 `http://` 站点**，
所以重定向保护必须保留。

因此 `http_via_proxy()` 用 `_NoRedirect` **禁止跟随重定向**：

- 3xx 直接判为不可用，失败原因记为 `HTTP 3xx 重定向(未跟随)`
- 判定只认 2xx（`generate_204` 正常返回 204，出现重定向本身就说明节点不可信）

> 排查「为什么弹窗要访问某个陌生域名」时，该域名通常**不在任何产物、节点清单、README 里**——
> 它是节点的**重定向目标**，不是节点本身。定位方法见 `Docs/known-issues.md` 第 10 条。
