# 产物文件清单与目录职责

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

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
