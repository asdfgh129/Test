---
name: free-nodes-collector
description: 免费节点每日采集与自检技能。用于每天跟踪 GitHub 上 v2ray/xray/clash/sing-box 等免费节点项目的当日更新，只检索当天有更新的仓库，先读每个仓库的 README 跟随其声明的订阅链接，按「完整链接」+「服务器地址:端口」两级去重，按四内核各自支持的代理协议/传输层/加密方式分流成 4 个订阅文件（nodes/v2ray_sub.txt、nodes/xray_sub.txt、nodes/clash_sub.yaml、nodes/singbox_sub.json），做 TCP 延迟探测并按延迟升序输出；内置四代理内核（v2ray/xray/mihomo(clash)/sing-box）可用性实测（默认全量测试：候选 ≤3000 全测，超过只测排序前 3000 个）、按仓库统计节点可用率作为仓库质量考核依据（下次优先采高质量仓库、跳过长期 0 可用仓库）、每内核跨天累积的可用节点池、三级自适应扩量、内核版本与能力漂移检查、以及采集后的自动自检（health_check.py 输出待修复清单）。产物不分日期，按 nodes/Docs/src 三分层存放。当用户要求"收集今天的免费节点"、"更新节点订阅"、"采集 GitHub 免费节点"、"合并去重节点"、"检查采集是否有问题"或触发每日定时任务时使用本技能。
agent_created: true
---

# free-nodes-collector — GitHub 免费节点每日采集

采集 GitHub 上有更新的 v2ray/xray/clash/sing-box 免费节点仓库，下载、合并、两级去重，**按四内核各自的能力分流**，输出可直接导入客户端的订阅文件。**内置三级自适应扩量**：节点数不足 1000 时自动逐级扩大采集范围。**内置每日自检**：跑完自动体检并给出可执行的修复建议。

四个质量环节串成一条链路：

1. **读 README**：每个仓库先读 README，跟随它声明的订阅链接——很多仓库的真实订阅文件只写在这里
2. **按仓库质量排序采集**：四内核实测出的「仓库可用率」回写到仓库清单，下次优先采高质量仓库、跳过长期 0 可用的
3. **TCP 延迟排序**：采集完立即探测 TCP 握手延迟，订阅按延迟升序输出，低延迟节点排在最前
4. **可用节点池**：每内核一份跨天累积的池，今天验证通过的节点明天继续复测复用

**产物不分日期**：输出根目录下分 `nodes/`（节点产物）、`Docs/`（文档与日志）、`src/`（脚本与采集状态）、`Skills/`（技能定义）四个子目录，外加 `.workbuddy/memory/`（项目记忆，纳入 git 跟踪），根目录只留 `README.md` 与 `CHANGELOGS.md`，每次运行覆盖更新——免费节点过期就没意义，留历史日期目录只会制造「看起来有、其实已死」的误导。

## 核心工作流

**三步：采集 → 验证 → 自检。**采集前建议先做内核检查，且它和采集**在同一进程里跑**（`--check-kernels`），这样自建代理只建一次。

```bash
# 1+2. 内核检查 + 采集 + 四内核可用性验证（一条命令，代理只建一次）
python <free-nodes>/src/collect_nodes.py --out <工作区>/free-nodes --readme-only --test --check-kernels

# 3. 自检：机械评估本次结果是否异常，输出待修复清单
python <free-nodes>/src/health_check.py --dir <工作区>/free-nodes

# 可选：单独跑内核版本 / 能力漂移检查（要连 api.github.com，必须带 token，否则走代理必 403）
python <free-nodes>/src/check_kernels.py --root <工作区>/free-nodes
```

> **为什么用 `--check-kernels` 而不是分两条命令**：内核检查要访问 `api.github.com`，本机直连不通时必须先自建代理。
> 但内核子进程会随父进程退出被回收（本机 job 限制），所以**分步执行时第 1 步建的通道活不到第 2 步**；
> 用 `--check-kernels` 把两步放进同一进程，通道建一次、采集直接接管（日志只出现一次 `[uplink] 通道就绪`）。
> 分步执行仍然可用：每步都会先尝试接管已登记的通道，接管不到才自建（约 10~30 秒）。

`health_check.py` 退出码：`0` 健康 / `1` 有告警 / `2` 有严重问题。有问题时按它的「待办清单」逐条处理，对照 `Docs/known-issues.md` 定位根因。

`collect_nodes.py` 退出码：`0` 正常 / `3` 本次采到 0 条但**保留了根目录里已有的旧结果**（不写空文件，检查配额/网络后重跑即可）。

**使用 `src/collect_nodes.py` 完成全部采集工作，纯 Python 标准库实现，无需安装任何依赖。**

### 标准采集

```bash
python <free-nodes>/src/collect_nodes.py --out <工作区>/free-nodes
```

- 输出根目录下分子目录（**不按日期建子目录**）：`nodes/` 放节点产物、`Docs/` 放文档与日志、`src/` 放脚本与采集状态、`Skills/` 放技能定义；根目录只留 `README.md` 与 `CHANGELOGS.md`。同一天多次运行会覆盖当天小节（md 日志按日期小节去重）
- 脚本自动完成：搜索当天更新仓库 → **读 README 取订阅链接** → 挑选候选文件 → 下载解析 → 两级去重 → **TCP 延迟探测排序** → 按四内核能力分流写出 4 个订阅文件 + 节点元数据 + 报告

### 常用参数

| 参数 | 说明 |
|---|---|
| `--out <dir>` | 输出根目录，默认 `./free-nodes`。内部按 `nodes/`（节点）+ `Docs/`（文档）+ `src/`（脚本与状态）分目录存放，**不分日期**，每次运行覆盖更新 |
| `--token <t>` | GitHub Token（可选）。**查找优先级**：`--token` → `GITHUB_TOKEN`/`GH_TOKEN` 环境变量 → 本地凭据文件 `~/.workbuddy/data/free-nodes-tools/github_token.txt`（不在 git 仓库里，权限 600）。带 token 后核心配额从 60/时升到 **5000/时**、搜索从 10/分升到 **30/分**，仓库池能大一个量级；日志里只打印 `前4…后4` 的打码形式 |
| `--max-repos N` | 每阶段最多扫描的新增仓库数，默认 **80**（带 token 时）；匿名限额下建议降到 20-30 |
| `--max-seeds N` | 节点不足时最多补充采集的种子仓库数，默认 **30** |
| `--search-pages N` | 每个关键词翻几页（每页 100 条），默认 **2**；关键词共 26 组，所以默认约 52 次搜索请求。单关键词前 100 条常被几个日更大仓库占满，翻页才能捞到中小仓库 |
| `--search-days N` | 阶段 2（节点不足时）把时间窗放宽到**前 N 天**有更新的仓库，默认 **3** |
| `--readme-date-tolerance N` | README 里按日期分列的订阅，允许取最近 N 天内的链接，默认 **0 = 严格只要当天**；日更仓库凌晨还没更新时可设为 1 |
| `--target-nodes N` | 目标节点数门槛，默认 1000，不足触发逐级扩量 |
| `--min-stars N` | 仓库最低 star 数过滤，默认 0。想要更稳定的来源可设为 50 |
| `--seed-file <path>` | 动态仓库清单路径（默认 `<输出根目录>/src/seed_repos.json`），同时承载仓库质量评分 |
| `--date YYYY-MM-DD` | 指定日期标记（只影响日志小节与 summary 的日期，不影响目录结构） |
| `--no-latency-sort` | 跳过 TCP 延迟探测与排序（省 1-2 分钟，但订阅不按延迟排序、也不写 nodes_meta.json） |
| `--latency-workers N` | 延迟探测并发，默认 128 |
| `--latency-timeout S` | 延迟探测超时（秒），默认 1.5；高延迟线路多时可放宽到 2.5 |
| `--drop-dead` | 丢弃 TCP 不可达节点（默认保留，排在订阅末尾） |
| `--keep-nodes N` | 按延迟排序后只保留前 N 条（0 = 不截断）；想「只要精华」时设 1000-2000 |
| `--keep-bad-repos` | 不跳过历史可用率为 0 的仓库（默认跳过以省配额） |
| `--time-budget N` | 采集阶段时间预算（秒），默认 2400=40 分钟；0=不限。超预算停止扫描剩余仓库，已有结果照常输出 |
| `--pool-dir <dir>` | 可用节点池目录（默认 `<输出根目录>/nodes/pool`） |
| `--readme-only` | **只跟随 README 声明的订阅链接**，不再按文件名扫描仓库目录；README 没有订阅链接的仓库直接跳过（命中率集中、不浪费配额，代价是来源数量变少） |
| `--uplink auto` | **默认值**。先接管前一步登记的自建代理（用 `--check-kernels` 时与内核检查共用同一条通道，不会再建第二次），接管不到才用已验证节点自建；代理不可用再直连，都不通则等 `--uplink-wait` 秒后重试（见下方「上行通道」） |
| `--uplink direct` | 只用直连，不自建代理 |
| `--uplink <url>` | 指定现成代理，如 `http://127.0.0.1:7890` |
| `--uplink-wait N` | 代理与直连都不通时每次重试前等待的秒数，默认 600=10 分钟 |
| `--uplink-retries N` | 上述重试次数，默认 2 |
| `--uplink-max-candidates N` | 自建代理时最多尝试多少个候选节点，默认 40 |
| `--check-kernels` | 采集前在**同一进程**里先跑内核版本与能力检查，共用同一条自建代理通道（推荐：分步执行时通道无法跨进程存活，用它可避免重复搭建）。可配 `--check-kernels-update`（有新版本就升级）、`--check-kernels-skip-network`（只做本地能力指纹） |
| `--test` | 采集完自动做四内核可用性验证 |
| `--test-cores <list>` | 要验证的内核，默认 `v2ray,xray,clash,singbox` |
| `--test-full-below N` | **全量测试阈值**（默认策略）：某内核候选数不超过 N 就**全部验证**，默认 3000 |
| `--test-max-test N` | **全量测试上限**：候选数超过 `--test-full-below` 时，只验证排序前 N 个，默认 3000。排序 = 协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序 |
| `--test-no-full-test` | 关闭全量测试，回到「`--test-limit` 初始取样 + 自适应扩量」旧模式 |
| `--test-limit N` | [旧模式] 每个内核**单轮**验证的节点数（初始取样量，也是扩量时每轮的追加量），默认 200 |
| `--test-min-available N` | [旧模式] **自适应扩量阈值**：某内核可用数低于该值就继续往后追加测试，默认 10；0=关闭扩量 |
| `--test-limit-cap N` | [旧模式] 单内核累计验证上限，默认 0=自动（`--test-limit` 的 5 倍，且不低于 `--test-min-available` 的 10 倍） |
| `--time-budget N`（test_nodes.py） | 整轮验证的**墙钟预算**（秒），默认 **0 = 不限**。到期后不再提交新节点、跳过尚未开始的内核，已测结果照常落盘；要补跑剩下的内核用 `--cores <内核>`。用途只有一个：在平台强杀之前自己优雅收尾、给发布留时间。**它不是测试量上限**——每内核测多少由候选数与窗口决定，不要用拍脑袋的数字去压 |
| `--test-url <url>` | 验证目标地址，默认 `https://gstatic.com/generate_204`（**裸域 HTTPS**，见下方「探测地址为什么用裸域」） |
| `--no-mirror-check` | 跳过开头的通道探活（省 10s，但会退化成"每文件都去撞死镜像"） |
| `FREE_NODES_MIRRORS`（环境变量） | 覆盖 raw 镜像候选池（逗号分隔），设为空字符串可禁用镜像。默认 11 个候选，实际只用探活通过的 |

### 输出文件（根目录只留 README.md 与 CHANGELOGS.md，其余分三个子目录 + Skills/）

**`nodes/` — 生成的节点信息**。节点文件（按四内核能力分流，一内核一文件，只写该客户端能直接导入的格式）：

| 文件 | 格式 | 导入对象 |
|---|---|---|
| `nodes/v2ray_sub.txt` | base64 订阅 | v2rayN / v2rayNG / v2ray 系客户端 |
| `nodes/xray_sub.txt` | base64 订阅 | Xray 系客户端（与 v2ray 同一来源订阅，按 xray 额外能力分流，含 reality/flow/xhttp） |
| `nodes/clash_sub.yaml` | Clash 配置（合法 YAML，含 PROXY 策略组） | Clash / mihomo |
| `nodes/singbox_sub.json` | sing-box outbounds 配置 | sing-box |
| `nodes/nodes_uris.txt` | 明文 URI 一行一条 | 内部主清单（全量唯一节点），其余四文件由它派生 |
| `nodes/nodes_meta.json` | JSON | 每节点 TCP 延迟 + 来源仓库（验证取样与仓库质量考核依据） |

可用清单（验证阶段产出，命名与节点文件一一对应）：

| 文件 | 格式 |
|---|---|
| `nodes/available_v2ray.txt` / `nodes/available_xray.txt` | base64 订阅（可用节点） |
| `nodes/available_clash.yaml` | Clash 配置（可用节点） |
| `nodes/available_singbox.json` | sing-box 配置（可用节点） |

**`Docs/` — 文档**（报告与日志全部**按日期倒序**，新的在最前，累积保留最近 30 个小节）：

| 文件 | 内容 |
|---|---|
| `Docs/protocol.md` | 四内核解析规范与实测校准报告 |
| `Docs/proxy.md` | 自建代理与节点测试链路代码组成说明 |
| `Docs/known-issues.md` | 踩坑知识库（每条含现象/根因/修复/教训，修复闭环的对查表）**+ 末尾「自检发现」区块**（`health_check.py` 自动写入，按日期倒序）。一个文件装两类内容，**不再有 `known_issues.md`** |
| `Docs/sources.md` | 种子仓库来源与维护建议 |
| `Docs/tools-setup.md` | 四内核二进制部署/升级方法 |
| `Docs/report.md` | 采集报告：延迟分布、README 战果、仓库质量排行、协议分布、各内核分流数 |
| `Docs/summary.md` / `Docs/summary.json` | 验证汇总：各内核测试数/可用数/可用率/测试策略与轮次 |
| `Docs/collection_logs.md` | 每次运行的执行阶段、仓库清单、去重结果、输出路径 |
| `Docs/health_check.md` / `Docs/health_check.json` | 自检结论 + 分级发现 + 待办清单 |
| `Docs/review_logs.md` | 跨天摘要（时间倒序） |

**`src/` — 脚本与采集状态**（全链路脚本的**唯一事实来源**，直接在这里改，无同步动作）：

| 文件 | 内容 |
|---|---|
| `src/*.py` | 采集/验证/自检/发布全链路脚本（collect_nodes、test_nodes、layout、pool、uplink、health_check、check_kernels、protocol_check、publish_free_nodes） |
| `src/seed_repos.json` | 动态仓库清单 + 质量评分（采集优先级依据） |
| `src/repo_quality.json` | 本次按仓库汇总的实测可用率 / 平均延迟 / 质量分 |
| `src/kernel_state.json` | 四内核版本与能力指纹基线（`check_kernels.py` 判定漂移用） |

**`Skills/free-nodes-collector/SKILL.md`** — 本技能的定义文档（工作流、参数表、故障排查入口）。

**`.workbuddy/memory/`** — 项目记忆（MEMORY.md 长期约定 + 每日工作日志），纳入 git 跟踪。

### 运行后必做

0. **跑 `health_check.py`**（见下文「每日自检与自优化」），有 critical/warn 就按修复闭环处理
1. 读取 `Docs/report.md`、`Docs/collection_logs.md`、`Docs/summary.md`、`Docs/health_check.md` 的**第一小节**（时间倒序，最新在最前），向用户汇报：唯一节点数、协议分布、执行到第几级扩量、TCP 可达率与延迟中位数、README 采集战果、仓库可用率 Top3、各内核可用数与池内节点数、主要来源仓库、自检结论
2. 提醒用户：免费节点时效性极短，建议当天导入当天使用；想只要低延迟精品可直接导入 `nodes/pool/pool_<core>.<ext>`（跨天累积的已验证节点池，扩展名随内核：`pool_v2ray.txt` / `pool_xray.txt` / `pool_clash.yaml` / `pool_singbox.json`）
3. 若结果为 0 条：检查网络连通性、GitHub API 限额（匿名搜索 10 次/分钟、核心 API 60 次/小时），建议提供 `--token` 重试

## README 订阅链接采集

**每个仓库先读 README，再挑文件。** 大量仓库把真正的订阅文件写在 README 里（`clash 订阅`、`sing-box 配置`、一键导入链接），这些文件名往往不带 sub/node 关键字，靠目录扫描挑不出来。

流程（`collect_from_readme`）：

1. 在文件树里找 README（根目录优先，兼容 `README_CN.md` / `readme.rst`）
2. 抽取链接：markdown `[x](url)`、HTML `href`、`clash://install-config?url=` 一键导入链接、裸链接
3. 分类：**同仓库文件** → 转成仓库内路径下载；**别的仓库文件** → 自动换成 `raw.githubusercontent.com` 地址（走镜像回退链）；**自建订阅接口** → 直接下载
4. **识别内核**（`KERNEL_LINK_HINTS`）：从文件名 → 目录名 → 链接文字 → 域名逐级判断，命中 `v2ray`/`xray`/`clash|mihomo`/`singbox` 就记下归属；认不出记为「通用」。作用有两个：日志能说清每个内核各采多少；**该链接的节点写入对应内核文件时豁免 `layout.CAPS` 预筛**（作者已声明格式，CAPS 的保守规则可能把真能用的判死）
5. **按日期筛选**（用户策略：只取当天）：两种写法都认——① 链接自带日期（`.../2026-10-25/all.txt`、`Nodes-20261025.txt`）；② 有日期小标题（`### 2026-10-25` 下面才列当天链接）。只保留 `[今天 - --readme-date-tolerance, 今天]` 内的；**整份 README 完全没提日期 → 视为通用订阅，全部保留**（否则非日更仓库会被全砍）。因日期跳过的数量单独记 `-4` 状态，日志里与「未声明链接」区分开
6. 过滤噪声：徽章/图片、仓库主页、`/issues`、`/releases`、`/forks`、`star-history`、`jsdelivr.com/package`、`*.github.io` 页面、`example/template/sample` 示例配置
7. 同一文件的多个 CDN 写法（raw / cdn / fastly / testingcf / gcore）按「仓库+路径」归一，只下一次
8. 单仓库最多跟随 10 个链接；链接**并发 4 路**下载，单仓库总预算 90 秒（超预算放弃剩余链接，避免一个慢站拖住整轮采集）；README 已拿到节点时少扫 1 个文件，把时间留给下一个仓库

实测收益：`Epodonios/v2ray-configs` README 一条 `All_Configs_Sub.txt` 就是 7600+ 条；`mahdibland/V2RayAggregator` README 指向 4 个外部仓库订阅，一次拿到 1.2 万条。README 链路是否正常，自检的「README 采集」项会直接告警。

## 仓库质量考核（可用率 → 采集优先级）

四内核实测的结果会按**节点来源仓库**汇总，写回 `seed_repos.json`：

| 字段 | 含义 |
|---|---|
| `tested` / `ok` / `avail_rate` | 本次实测数 / 可用数 / 可用率 |
| `avg_latency` | 可用节点的平均延迟 |
| `quality` | 质量分（0-100）= 可用率 × 70 + 延迟项 × 30（5000ms 归零）；**可用率为 0 时延迟项记 0**（没有可用节点就没有延迟样本） |
| `quality_history` | 最近 7 次的日期/可用率/质量分，用于看走势 |

生效方式：

- **采集顺序**：阶段 1/2/3 的仓库都按**实测可用率**降序处理（未知仓库走 25% 中性先验，同分保持 star/更新时间顺序）——配额有限时先采高质量仓库
- **验证取样**：四内核取样同样按仓库可用率排序，先测高质量仓库的节点
- **跳过死源**：实测 ≥20 个且可用 0 个、或实测 ≥50 个且可用率 <2% 的仓库，下次直接跳过并在采集日志记「质量过低跳过」（`--keep-bad-repos` 可关闭）
- `nodes_meta.json` 的 `repo` 字段是这条链路的依据：采集时给每个节点打来源仓库标记，验证时才能算账

## TCP 延迟排序

采集完成后立刻对**所有去重节点**做并发 TCP 握手探测（默认 128 并发 / 1.5s 超时，同一 `host:port` 只探一次），然后：

1. `v2ray_sub.txt`、`clash.yaml`、`singbox.json` 统一按「可达 → 非 CF → 延迟」排序写入：真实低延迟节点在最前
2. **Cloudflare 前置节点整体降权**：它们的 TCP 握手只有 10-40ms（就近接入 CF 边缘），但代理是否真通取决于回源配置，免费节点里大量是死的。若纯按延迟排，订阅头部会被这类节点霸占、实测可用率直接塌到 0（2026-10-24 实测：低延迟 707 条里 90% 是 CF，采样 200 个只通 0-3 个）。因此它们排在**真实可达节点之后、不可达节点之前**
3. 不可达节点（`tcp_latency = null`）排在最后，默认保留（免费节点抖动大，明天可能就通了）
4. 需要「只要精华」时用 `--keep-nodes 1500` 截断，或 `--drop-dead` 直接丢弃不可达
5. 结果落盘 `nodes_meta.json`：延迟分桶统计（<100 / 100-300 / 300-800 / >800ms / 不可达）+ 每节点延迟、是否 CF 前置、来源仓库

CF 网段清单在 `collect_nodes.CF_NET_CIDRS` 维护（官方 IPv4/IPv6 段）。验证取样同样遵循这条规则：先测真实节点，CF 只做补位。

> 探测超时对高延迟线路偏严。若自检报「可达率 <5%」，先把 `--latency-timeout` 放宽到 2.5 再判断。

## 四内核能力分流（layout.CAPS）

采集到的是**一份**去重后的全量节点（`nodes_uris.txt`），写订阅时按四内核各自真实支持的能力**分流**成四个文件。分流不是"按仓库分"，而是按节点的协议特征判定——同一个仓库的订阅里往往混着各内核都能用和各内核都用不了的节点。

> 完整规范（每种协议/传输/加密的字段要求、URI 参数映射、失败分类口径）见
> **`Docs/protocol.md`**；一致性回归跑 `src/protocol_check.py`。
> 自建代理与节点测试链路的**文件组成与函数级说明**见 **`Docs/proxy.md`**。

下表为 **2026-10-25 按内核实测校准**的结果（v2ray 5.53.0 / xray 26.10.21 / mihomo 1.19.33 / sing-box 1.14.4）：

| 维度 | v2ray | xray | clash(mihomo) | singbox |
|---|---|---|---|---|
| 代理协议 | vmess/vless/trojan/ss/hysteria2* | 同左（含 hysteria2*） | 同左 + ssr/hysteria2/tuic | 同左 + hysteria2/tuic |
| 传输层 | tcp/kcp/ws/http/quic/grpc | tcp/kcp/ws/grpc/**httpupgrade/xhttp** | tcp/ws/http/h2/grpc/xhttp | tcp/ws/http/grpc/httpupgrade/quic(TLS) |
| 已移除的传输 | httpupgrade/xhttp | **http/h2、quic** | kcp/quic/httpupgrade | xhttp |
| REALITY | ✗ | ✓ | ✓ | ✓ |
| VLESS flow（xtls-rprx-vision） | ✓ | ✓ | ✓ | ✓ |
| ss 加密 | 仅 AEAD | AEAD + 2022 | 全部（含 CFB/rc4） | 全部（仅出站） |
| ss 插件 | ✗ | ✗ | obfs / v2ray-plugin | obfs-local / v2ray-plugin |
| VLESS/Trojan 必须 TLS | ✗ | ✓（26.x 强制） | ✗ | ✗ |

要点：

- `v2ray` 与 `xray` **共用同一份源订阅**（仓库里针对 v2ray 系内核的那条链接），采集时按上表分流：带 reality / xhttp / httpupgrade 的节点只进 `xray_sub.txt`；带 `type=http`/`h2` 的节点只进 `v2ray_sub.txt`（Xray 26 已移除 HTTP 传输）
- hysteria2 节点现在也进 `v2ray_sub.txt` 和 `xray_sub.txt`（v2fly 5.x、Xray 26.x 均支持，2026-10-25 核实）：v2ray 侧带 `obfs` / `mport` 参数的除外（v2fly 静默忽略，见 known-issues 第 26 条）；xray 侧协议名是 `hysteria`+`version:2`，**支持** salamander 混淆与端口跳跃（见 protocol.md §3.6 与 known-issues 第 27 条）
- v2fly 至今不支持 REALITY，把这类节点写给 v2ray 只会让客户端整份配置导入失败，所以必须前置过滤
- 同一节点可能同时出现在多个内核文件里（说明兼容性好），这不是重复 bug
- 分流实现在 `layout.filter_uris(core, uris)`（判定事实来自 `layout.node_facts()`，与转换器共用一套规则）；能力表在 `layout.CAPS`
- 内核升级后跑 `check_kernels.py` 看能力指纹漂移，再跑 `protocol_check.py` 验证转换器是否仍然合规
- **转换器不许静默降级**：识别不了的传输必须判「不支持」，禁止兜底成 `tcp`（否则节点会因参数丢失而连不上，被误记成不可达，见 known-issues 第 22 条）

## 可用节点池（跨天累积复用）

每内核**一个**池文件 + 四内核**共用**一份状态，位于 `<输出根目录>/nodes/pool/`：

| 文件 | 说明 |
|---|---|
| `pool_v2ray.txt` / `pool_xray.txt` | base64 订阅（可直接导入客户端） |
| `pool_clash.yaml` | Clash 配置 |
| `pool_singbox.json` | sing-box 配置 |
| `pool_state.json` | **唯一**的元数据：每节点首次通过、最近通过、通过次数、最佳/最近延迟、来源仓库 |

为什么这样分：池文件是**给人用的**（直接导入），格式必须跟内核一一对应；元数据是**给脚本用的**（复测优先级、淘汰策略），集中一份才不会四份互相打架。旧版的 `pool_<core>.txt` + `_list.txt` + `.json` 三件套已经取消——`_list.txt` 与 base64 解码后完全等价，纯冗余；`.json` 与池文件重复存节点列表，只是把同一份数据抄了一遍。

规则：

- **入池**：该内核实测通过的节点（身份 = `host:port`），刷新 `last_ok` / `ok_count` / `best_latency`
- **复用**：每天每内核额外捞 `--pool-retest 40` 个「池里有、今天新鲜列表里没有」的节点复测（先过 TCP 预筛，低延迟优先），通过即继续留在池里并计入当日可用清单
- **淘汰**：连续 `--pool-days 14` 天没再通过就移除；池上限 `--pool-max 3000`，按「通过次数 + 最佳延迟」排序截断
- 池节点同样参与仓库质量统计（来源仓库沿用入池时记录的值）
- 池文件里只存 URI，`pool_state.json` 才存元数据——两者不要互相复制

效果：每天新采到的高质量节点会沉淀下来，某天上游停更或采集失败时仍有可用节点兜底，不会「一天没采到就全丢」。

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

### 内核版本与能力漂移检查（check_kernels.py）

内核升级会悄悄改变"它到底能吃什么"，历史上已经踩过两次：

- **Xray 26.x 移除 `tlsSettings.allowInsecure`**（报错要求改用 `pinnedPeerCertSha256` / `verifyPeerCertByName`）——沿用老配置模板会让 xray **全部样本验证失败**，看起来像"节点全死了"
- **v2fly 5.x 改了配置校验命令**（`-test -config` 报 `flag provided but not defined`，新写法是 `test -c`）——沿用老命令会让 v2ray 的每个样本都判"未被接受"

所以每次采集前建议跑一次（**推荐与采集合并成一条命令**，代理只建一次）：

```bash
python <free-nodes>/src/check_kernels.py --root <输出根目录>            # 只检查，不改动（结束自动关通道）
python <free-nodes>/src/check_kernels.py --root <输出根目录> --update   # 有新版本就下载安装
python <free-nodes>/src/collect_nodes.py --out <输出根目录> --check-kernels   # 推荐：检查+采集一体
```

**这一步本身就要访问 GitHub（`api.github.com` 查 release），所以它会先自建代理再查**：按
`--uplink auto`（默认）用已验证节点起本地通道。走免费节点代理时出口 IP 与他人共享，**匿名配额
（60/时）几乎必然 403，必须带 token**（`--token` 或凭据文件，自动读取）。检查结束后默认关掉通道；
被 `collect_nodes.py --check-kernels` 调用时，通道直接移交给采集环节继续用。

它做两件事：

1. **版本检查**：对比本地二进制版本与 GitHub 最新 release（XTLS/Xray-core、v2fly/v2fly-core、MetaCubeX/mihomo、SagerNet/sing-box），输出有无更新
2. **能力指纹**：用一组「协议 × 传输层 × 加密方式」样本配置跑内核原生校验命令，比对 accepted 集合与 `kernel_state.json` 里记录的基线有没有变化。**accepted 集合变了就说明"最新支持的节点内容"变了**，需要同步更新 `layout.CAPS` 与节点转换逻辑

内核原生校验命令由 `test_nodes.check_config()` 按候选链自动识别并缓存（`v2ray test -c` / `xray -test -config` / `mihomo -t -f` / `sing-box check -c`），版本变了也不会一次性全哑。

退出码：`0` 无变化 / `1` 有新版本或能力变化 / `2` 检查失败。发现变化时脚本会自己往 `CHANGELOGS.md`（根目录）与 `Docs/known-issues.md` 追加记录。

### 验证流程（TCP 预筛 + 全量实测 + 失败分层）

1. **TCP 预筛**：高并发（默认 64）测试服务器 `host:port` 是否可连，2s 超时，快速剔除死节点
2. **内核实测（默认全量策略）**：对每个内核，候选 ≤ `--full-below`（3000）个时**全部测试**；超过则只测排序前 `--max-test`（3000）个。排序 = 协议轮流交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序。每个节点生成该内核的临时配置 → 启动内核 → 通过本地 HTTP 代理访问 `https://gstatic.com/generate_204`（裸域 HTTPS，走代理访问，只有真正把流量送出境外才可能返回 204）→ 判定可用并记录延迟
3. **限量模式（可选）**：加 `--no-full-test` 回到旧行为——每内核单轮 `--limit`（200）个初始取样，可用数低于 `--min-available`（10）时顺着同一顺序追加，直到达标 / 候选耗尽 / 触到单内核上限 / 时间预算用完。测试策略与轮次写进 `Docs/summary.md` / `Docs/summary.json`
4. **失败分层**（决定"测不过"到底赖谁）：
   - `unsupported`：能力预筛或转换器判定该内核无法表达（协议/传输/加密/插件/残缺公钥）→ **不发布、不计入不可达**
   - `config`：配置生成出来了但被内核校验拒绝（参数不符）→ 同上
   - `tls` / `auth` / `refused` / `reset` / `timeout`：内核日志与客户端异常文本都指向节点侧 → 计入不可达
   - 网络类失败自动复测 `--retry`（默认 1）次，两次都失败才定案
5. **增量落盘（抗强杀）**：每个内核测完立刻写一次 `available_<core>.*`、`Docs/summary.*`、
   仓库质量与 `nodes/pool/pool_state.json`。平台对单次运行有 **90 分钟硬上限**
   （超时消息 `[CANCELLED] Run timed out`，见 known-issues 第 31/36 条），
   被强杀时**已完成的内核不会白跑**，也不会出现「一个内核是新数字、其余是旧数字」的混合状态。
   想主动在强杀前收尾（例如给发布留 10 分钟），加 `--time-budget <秒>`：到期不再提交新节点、
   跳过未开始的内核，`summary.md` 会标「本轮未跑完（墙钟预算到期主动收尾，不是失败）」，
   下次用 `--cores <剩余内核>` 补跑即可。**默认 0 = 不限，不要用固定测试量去硬压**

判定口径与每类原因的原文证据见 `Docs/protocol.md` 第 4 节；`Docs/summary.md` 会给出
「不支持 / 配置错误 / 不可达」三列与「失败原因分布」表——成片 `config` 是转换器有 Bug，
成片 `unsupported` 是能力矩阵要跟内核对齐，都不代表节点质量下降。

### 运行方式

```bash
# 单独验证已有采集结果（默认全量测试：候选 ≤3000 全测，超过测排序前 3000 个）
python <free-nodes>/src/test_nodes.py --input <输出根目录> --cores v2ray,xray,clash,singbox

# 采集时自动验证（默认即全量测试，可显式传阈值）
python <free-nodes>/src/collect_nodes.py --out <输出根目录> --test --test-full-below 3000 --test-max-test 3000
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

代价是耗时更长（实测 0.9～16.7s，因为要真出境），所以 `--test-timeout` 默认 12s、并发默认 12（8s 会误杀大量真实可用节点）。
需要换探测点时用 `--test-url`，维持「裸域域名的 HTTPS 地址」即可，例如 `--test-url https://www.google.com/generate_204`。

`--retry`（默认 1）控制网络类失败的复测次数；`--startup-timeout`（默认 6s）是内核端口就绪等待，
超时不足以区分「内核启动慢」和「配置被拒」，所以失败时会再用内核实测校验命令复核一次。

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

### 输出（订阅文件在 `nodes/`，报告类在 `Docs/`）

**一内核一文件**，格式与该内核客户端一致，不再有四件套：

| 文件 | 说明 |
|---|---|
| `nodes/available_v2ray.txt` | v2ray 可用节点的 base64 订阅 |
| `nodes/available_xray.txt` | xray 可用节点的 base64 订阅 |
| `nodes/available_clash.yaml` | clash(mihomo) 可用节点的 Clash 配置 |
| `nodes/available_singbox.json` | sing-box 可用节点的 outbounds 配置 |
| `Docs/summary.md` / `Docs/summary.json` | 各内核测试数、可用数、可用率、不支持数、配置错误数、不可达数、扩量轮次、候选是否已测完、失败原因分布 |
| `src/repo_quality.json` | 本次按仓库汇总的实测可用率 / 平均延迟 / 质量分 |

旧版的 `available_<core>_list.txt`（明文 URI）、`available_<core>_clash.yaml`、`available_<core>_singbox.json` 全部取消：base64 订阅解码即得明文列表，跨内核格式转换（xray 的可用清单转成 clash 配置）在能力矩阵上本来就不成立——xray 支持 REALITY 而 clash 的转换不保真，转出来的配置导进去只会报错。

同一节点可能在多个内核都可用（说明协议兼容性更好），按内核分开保存便于直接对应客户端使用。

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

### 列目录通道（不消耗 GitHub 配额）

列仓库文件列表**默认走 jsDelivr data API**（`data.jsdelivr.com/v1/packages/gh/<repo>@<branch>?structure=flat`），
返回完整扁平文件树且**不计入 GitHub 核心配额**——匿名配额只有 60 次/小时，列目录曾是采集卡住的主因。
jsDelivr 不可用时才回落 GitHub contents API（此时只列根目录，消耗配额）。

### 下载回退链（内置，自动处理 raw 直连失败）

`raw.githubusercontent.com` 直连经常被网络重置。脚本内置四级回退，**按序尝试、第一个成功即用**：

1. `raw.githubusercontent.com` 直连
2. **raw 镜像代理前缀**（形式 `https://gh-proxy.com/<完整 raw URL>`）
3. jsDelivr CDN（`@main` / `@master` 分支 × 各边缘节点）
4. GitHub contents API（base64，消耗核心配额，最后手段）

大文件（>2MB）走镜像极易被截断，这类文件把 jsDelivr 提到镜像之前，超时也放宽到 90s。

**通道自动探活**（每轮采集开始时执行一次，约 10s；触发备用补位时约 +12s）：
- 探测 raw 直连、全部镜像前缀、全部 jsDelivr 边缘节点，结果写入
  `~/.workbuddy/data/free-nodes-tools/mirrors_state.json`（有效期 24h）
- **探活后只用活着的通道**：死镜像会被整体踢出下载链，而不是"排到后面"——
  否则每个下载失败的文件都要在 N 个死镜像上各等一次超时（5 个死镜像 ≈ 100s/文件）
- raw 直连已知不通时排到最后，省掉每个文件一次 TLS 失败等待
- 全部镜像死掉不算故障：自动退回 raw 直连 + jsDelivr 两路
- **备用候选自动补位**：主清单存活镜像 <2 个时，补测 `MIRROR_SPARE_CANDIDATES`
  （只收「域名能解析、当前被墙/限流」的站点，DNS 不存在的域名不进池），
  救回的并入可用清单并写进状态文件。公共代理域名会成批烂掉——2026-10-24 实测
  13 个候选只剩 1 个活、其余多为 DNS 解析失败，靠补位恢复到了 3 个
- 跳过探活用 `--no-mirror-check`；自检结果里的「下载通道」项与这份状态一致

两个清单的性质不同，别混用：
- `DEFAULT_MIRROR_PREFIXES` / `JSDELIVR_HOSTS` 是**候选池**，公共代理存活率随出口网络剧烈变化
  （同批域名实测 1/11 ~ 7/11），不能当可信清单
- `get_mirror_prefixes()` / `get_cdn_hosts()` 返回**当前可用**的，下载链只用这个
- 但 README 链接归一化（`_repo_path_from_url`）必须用 `_base_mirrors()` 全量候选，
  否则失效镜像上的链接认不出来，同一文件会被重复下载

**jsDelivr 不能写死单域名**：`cdn.jsdelivr.net` 在部分网络被 DNS/SNI 阻断，
而 `fastly.` / `gcore.` / `testingcf.` 三个边缘节点仍可取回同一份内容。
镜像通道不会携带 GitHub Token（避免凭据泄漏给第三方镜像）。

### 候选文件识别（决定「这个仓库有没有节点」）

三层判定，逐层放宽：

1. **根目录文件**：扩展名命中 `CANDIDATE_EXT`（`.txt/.yaml/.yml/.json/.list/.log`），
   或命中 `BARE_SUB_NAMES` 的无扩展名裸文件（`clash`/`v2`/`configs`/`sub` 等，要求 ≥4KB）
2. **子目录文件**：顶层目录名命中 `is_subdir_hint()`（英文锚定 + 中文/内核名包含匹配，
   覆盖 `Mihomo内核系`、`节点订阅` 这类命名），**不限层级**（`sub/raw/01.yaml` 这种两层布局很常见）
3. **进目录扫描**：若文件树来自 contents API 且只有 `dir` 条目（子项根本没列出来），
   才对命中提示词的目录付配额真进一次

**格式不由扩展名决定，按内容嗅探**（`sniff_ext()`）：先认 `proxies:` → YAML，
再认 `outbounds` / `{` / `[` → JSON，否则按纯 URI 文本。理由很实际：
`ts-sf/fly` 的裸文件 `clash` 按文本解析得 0 条，按 YAML 解析得 200 条。

`SKIP_FILE_PATTERNS` 负责排除干扰项：`whitelist-all.txt`、`cidrwhitelist.txt`、`geosite`、
`rule`、`scrapy.log` 这类分流表与运行日志**不是**节点文件，误收会白耗下载与解析。

`github_api()` 会自动转义非 ASCII 路径（中文目录/文件名）；调用方传**未转义**的 path，
自己 quote 过再传会二次编码。

## 每日自检与自优化（health_check.py）

采集 + 验证跑完后必须跑一次自检。它不做修改，只做**诊断 + 给出可执行建议**，修复动作由 agent 决定。

```bash
python <free-nodes>/src/health_check.py --dir <输出根目录>            # 默认目标 1000 条
python <free-nodes>/src/health_check.py --dir <输出根目录> --skip-network   # 离线快速模式
```

### 检查项

| 类别 | 检查内容 | 严重度触发条件 |
|---|---|---|
| 产物 | `nodes/nodes_uris.txt` + 4 个 `nodes/*_sub.*` + `Docs/report.md` 是否齐全，四内核分流数是否合理 | 缺文件 = critical |
| 规模 | 去重后节点数 vs `--target-nodes` | <10% critical，<50% warn |
| 仓库效率 | 按「有产出 / 解析不到节点 / 下载失败 / 无候选文件」四类统计，产出率低则按主导失败类型给针对性建议 | 产出率 <10% critical |
| 来源稳定性 | 历史高贡献仓库本次是否 0 条，并标注原因（下载失败/解析失败/无候选） | 有掉线 = warn |
| README 采集 | 有多少仓库在 README 中识别到订阅链接、从中提取多少节点 | 一个都没识别 = warn |
| 延迟排序 | `nodes/nodes_meta.json` 是否生成、TCP 可达率、延迟中位数、订阅头部是否混入不可达节点 | 全不可达 critical，头部混入 warn |
| 仓库质量 | 已评分仓库数、可用率 ≥10% 的比例、长期 0 可用的仓库数 | 过半 0 可用 = warn |
| 节点池 | `nodes/pool/` 下 4 个池文件 + `pool_state.json` 是否存在、各内核池内节点数 | 池缺失/为空 = warn |
| 验证 | 各内核可用数、可用率、`nodes/available_*` 与 `Docs/summary.json` 是否一致、内核二进制是否在位 | 0 可用 = critical |
| 下载通道 | 探测 raw 直连 + 全部镜像前缀 + 全部 jsDelivr 边缘节点 | 镜像与 raw 全挂 critical，部分挂 warn，jsDelivr 四节点全挂 warn |
| 配额 | GitHub core / search 剩余、是否配置 token | 匿名且 core <20 = warn |
| 来源质量 | 单一服务器占比 >50% | warn |
| 趋势 | 与近 7 次中位数比较，跌幅 >60% | warn |
| 性能 | 采集耗时 >45 分钟 | warn |

### 输出

报告类全部位于输出根目录的 `Docs/`，**统一按日期倒序（最新小节在最前）**，累积保留最近 30 个小节：

- `Docs/health_check.md` — 结论 + 指标表 + 分级发现 + **待办清单**
- `Docs/health_check.json` — 机读版（供自动化判断）
- `Docs/known-issues.md` 末尾的「自检发现」区块 — 本次自检发现的问题（同一天重跑会替换当天小节，不会重复堆叠；上面的知识库条目不受影响）
- `Docs/review_logs.md` — 每次运行一行摘要，跨天可追溯

根目录的 `CHANGELOGS.md` 由人工/脚本在**修复或升级内核后**写入（`layout.append_changelog`），同样按日期倒序。

### 修复闭环（发现 critical/warn 时按此执行）

1. **读待办清单**，拿最靠前的 critical 项
2. **对照 `Docs/known-issues.md`** 找同类症状的已知根因（多数问题那里已有答案）
3. **定位到具体代码**：抓 1 个失败样本（仓库/URI/内核）单独复现，不要靠猜
4. **改脚本并单点回归**：用该样本验证修复确实生效（不能只看整体数字变化）
5. **重跑受影响环节**：解析类 → 重跑采集；验证类 → 重跑 `test_nodes.py`
6. **再跑 `health_check.py`**，确认该 finding 消失且未引入新问题
7. **记录**：向 `Docs/known-issues.md` 上方知识库按编号追加条目（新发现的现象/根因/修复/教训），自检结果由 `health_check.py` 自动写进同一个文件末尾的「自检发现」区块；根目录 `CHANGELOGS.md` 记「改了什么 + 验证结果」（都按日期倒序，同一天重跑替换当天小节）；行为变化同步更新本文件
8. **提交推送**：`src/publish_free_nodes.py --proxy auto`（路径限定只提交 free-nodes；脚本自身就在 src/ 里，无需同步/打包）
9. **汇报**：说明「发现什么 → 根因 → 改了什么 → 验证结果」

只改有证据支撑的地方。推测性问题先记进 `Docs/review_logs.md` 观察，不要凭感觉动参数。

## 三级自适应扩量（内置）

以 `--target-nodes`（默认 1000）为门槛，节点不足时自动逐级扩量：

1. **阶段 1**：搜索**当天**有更新的仓库（`pushed:>=今天`，默认最多 `--max-repos 30` 个）
2. **阶段 2**：仍不足 → 时间窗口放宽到**前一天**（`pushed:>=昨天`），仓库数量加倍（`max-repos × 2`）
3. **阶段 3**：仍不足 → 补充采集**动态仓库清单**中的主流种子仓库（默认最多 `--max-seeds 15` 个），按历史贡献节点数与 star 排序

每阶段前检查 GitHub 核心 API 配额余量（通过不计配额的 `/rate_limit`），配额不足自动跳过并提示。

## 动态仓库清单（seed_repos.json）

- 位置：默认 `<输出根目录>/src/seed_repos.json`（如 `free-nodes/src/seed_repos.json`），可用 `--seed-file` 指定
- 内置初始种子：barry-far/V2ray-Configs、Epodonios/v2ray-configs、mahdibland/V2RayAggregator、peasoft/NoMoreWalls、Au1rxx/free-vpn-subscriptions
- **每次运行后自动更新**：本次贡献过节点的仓库都会写入清单（记录 star、累计贡献节点数、最近采集日期）；清单按贡献排序，上限 80 个
- **验证后回写质量**：`tested` / `ok` / `avail_rate` / `avg_latency` / `quality` / `quality_history`，供下次采集排序与跳过死源
- 作用：搜索结果少时，阶段 3 从清单补充高价值仓库（**按质量分排序**）；高频聚合仓库会被自动沉淀进清单

## 去重规则（内置）

1. **完整链接去重**：URI 完全相同视为同一节点
2. **服务器:端口去重**：不同协议/参数但服务器地址和端口相同的节点视为重复，保留先出现的（来源按 star 数与更新时间排序，更可靠的来源优先保留）

clash proxies 与 sing-box outbounds 形式的节点同样按 server:port 参与全局去重，并与 URI 节点互通去重。

**三种来源都能反解成标准 URI**（`record_uri`）：`clash_to_uri()` 处理 clash proxy，`singbox_to_uri()` 处理 sing-box outbound（ss / trojan / vless / vmess / hysteria2 / tuic 六种）。反解是必须的——`nodes_uris.txt` 主清单是验证阶段的取样来源，反解不出来的节点就**测不到**，等于未经验证直接发布。sing-box 的 `direct`/`block`/`dns`/`selector`/`urltest` 属于内置出站，解析阶段就排除，不当节点。

## 仓库发现机制

通过 GitHub Search API 搜索，**26 组关键词 × 2 页（每页 100 条）**，按更新时间降序，去重后按 `(star, pushed_at)` 排序：

| 类别 | 关键词 |
|---|---|
| 综合聚合 | v2ray free nodes / v2ray configs / vmess vless trojan / free proxy nodes / proxy subscription / free subscription nodes |
| 按内核 | clash subscription / clash config / mihomo config / sing-box config / singbox nodes / xray configs / xray vless reality |
| 按协议 | hysteria2 nodes / tuic vless / vless reality / vmess subscription / trojan subscription / shadowsocks subscription |
| 中文仓库 | 节点 订阅 / 免费节点 / 免费机场 / 节点分享 / 订阅链接 |
| 日更型 | daily free nodes / daily v2ray |

- **限定符**：`pushed:>=<日期> stars:>=<--min-stars>`
- **黑名单**：`BLACKLIST_REPO_PATTERNS` 排除 docs/tutorial/awesome 类，以及 `sub-store`/`subconverter`/`3x-ui`/`x-ui`/`clash-verge`/`nekoray`/`hiddify` 这类客户端、面板、订阅转换器（它们不产节点，扫了只浪费配额）
- **限速**：带 token 每请求间隔 2.2s（30/分），匿名 6.5s（10/分）
- **三级扩量**：阶段 1 当天 → 阶段 2 前 `--search-days` 天（默认 3）且仓库数翻倍 → 阶段 3 从 `seed_repos.json` 按可用率补最多 30 个种子仓库
- **沉淀**：所有扫过的仓库写进 `seed_repos.json`（上限 300 个），下次作为种子池

关键词在 `src/collect_nodes.py` 顶部的 `SEARCH_QUERIES` 中维护，需增删时直接修改该列表。

补充的固定种子仓库与维护建议见 `Docs/sources.md`。
