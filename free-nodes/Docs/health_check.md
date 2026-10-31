# 每日自检报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-10-31 23:01

**结论：无严重问题，5 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 7760 |
| 采集总量(过滤前) | 18259 |
| 各内核订阅 | v2ray 5855、xray 6846、clash 7718、singbox 7252 |
| 协议分布 | hysteria2 10 / ss 150 / ssr 1 / trojan 772 / vless 6064 / vmess 763 |
| TCP 可达 | 7760/7760（中位数 216ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '54/2506', 'xray': '122/2505', 'clash': '60/2507', 'singbox': '55/2503'} |
| 可用节点池 | v2ray 181、xray 452、clash 350、singbox 285 |

### 发现与建议

#### 🟡 [来源稳定性] 1 个高贡献仓库本次 0 条：free-nodes/clashfree(历史 324 条, 下载失败)

- 建议动作：按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理

#### 🟡 [验证] v2ray 可用率异常低 2.2%（54/2506）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] clash 可用率异常低 2.4%（60/2507）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] singbox 可用率异常低 2.2%（55/2503）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 7760 条；各内核订阅：v2ray 5855、xray 6846、clash 7718、singbox 7252


#### 🔵 [规模] 节点数 7760 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 67 个：有产出 28、解析不到节点 13、下载失败 6、无候选文件 0、部分链接下载失败 3、README 无订阅链接跳过 17（产出率 56%，按有尝试采集的 50 个计算）


#### 🔵 [README 采集] 50 个仓库的 README 声明了订阅链接，提取 140863 条节点


#### 🔵 [延迟排序] 7760/7760 个服务器 TCP 可达（100%），延迟中位数 216ms，<100ms 共 691 条


#### 🔵 [延迟排序] 2765/7760 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 43 个仓库，可用率 >=10% 的 6 个，长期 0 可用 15 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 181、xray 452、clash 350、singbox 285


#### 🔵 [下载通道] jsDelivr 可用 3/4：fastly.jsdelivr.net、gcore.jsdelivr.net、testingcf.jsdelivr.net（不可达：cdn.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 5000/5000、search 30/30（已配置 token ghp_…x6hY）


### 待办清单（需人工或自动修复）

1. [warn] 1 个高贡献仓库本次 0 条：free-nodes/clashfree(历史 324 条, 下载失败) → 按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理
2. [warn] v2ray 可用率异常低 2.2%（54/2506） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
3. [warn] clash 可用率异常低 2.4%（60/2507） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
4. [warn] singbox 可用率异常低 2.2%（55/2503） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
5. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

## 2026-10-30 01:36

**结论：无严重问题，5 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 3439 |
| 采集总量(过滤前) | 8935 |
| 各内核订阅 | v2ray 3124、xray 3025、clash 3390、singbox 3238 |
| 协议分布 | hysteria2 7 / ss 55 / ssr 7 / trojan 193 / vless 2067 / vmess 1110 |
| TCP 可达 | 3439/3439（中位数 214ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '35/2502', 'xray': '95/2505', 'clash': '49/2507', 'singbox': '35/2506'} |
| 可用节点池 | v2ray 147、xray 367、clash 307、singbox 251 |

### 发现与建议

#### 🟡 [来源稳定性] 2 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 部分链接下载失败)、free-nodes/clashfree(历史 324 条, 解析不到节点)

- 建议动作：按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理

#### 🟡 [验证] v2ray 可用率异常低 1.4%（35/2502）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] clash 可用率异常低 2.0%（49/2507）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] singbox 可用率异常低 1.4%（35/2506）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 3439 条；各内核订阅：v2ray 3124、xray 3025、clash 3390、singbox 3238


#### 🔵 [规模] 节点数 3439 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 68 个：有产出 23、解析不到节点 17、下载失败 4、无候选文件 0、部分链接下载失败 5、README 无订阅链接跳过 19（产出率 47%，按有尝试采集的 49 个计算）


#### 🔵 [README 采集] 49 个仓库的 README 声明了订阅链接，提取 70149 条节点


#### 🔵 [延迟排序] 3439/3439 个服务器 TCP 可达（100%），延迟中位数 214ms，<100ms 共 392 条


#### 🔵 [延迟排序] 1195/3439 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 39 个仓库，可用率 >=10% 的 3 个，长期 0 可用 12 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 147、xray 367、clash 307、singbox 251


#### 🔵 [下载通道] jsDelivr 可用 3/4：fastly.jsdelivr.net、gcore.jsdelivr.net、testingcf.jsdelivr.net（不可达：cdn.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 4980/5000、search 30/30（已配置 token ghp_…x6hY）


### 待办清单（需人工或自动修复）

1. [warn] 2 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 部分链接下载失败)、free-nodes/clashfree(历史 324 条, 解析不到节点) → 按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理
2. [warn] v2ray 可用率异常低 1.4%（35/2502） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
3. [warn] clash 可用率异常低 2.0%（49/2507） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
4. [warn] singbox 可用率异常低 1.4%（35/2506） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
5. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

## 2026-10-29 01:32

**结论：无严重问题，5 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 3912 |
| 采集总量(过滤前) | 10177 |
| 各内核订阅 | v2ray 3438、xray 3347、clash 3870、singbox 3706 |
| 协议分布 | hysteria2 10 / ss 158 / ssr 8 / trojan 266 / vless 2737 / vmess 733 |
| TCP 可达 | 3918/3918（中位数 218ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '30/2502', 'xray': '105/2503', 'clash': '72/2506', 'singbox': '50/2503'} |
| 可用节点池 | v2ray 127、xray 304、clash 276、singbox 230 |

### 发现与建议

#### 🟡 [来源稳定性] 1 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 部分链接下载失败)

- 建议动作：按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理

#### 🟡 [验证] v2ray 可用率异常低 1.2%（30/2502）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] clash 可用率异常低 2.9%（72/2506）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] singbox 可用率异常低 2.0%（50/2503）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 3912 条；各内核订阅：v2ray 3438、xray 3347、clash 3870、singbox 3706


#### 🔵 [规模] 节点数 3912 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 74 个：有产出 31、解析不到节点 14、下载失败 3、无候选文件 0、部分链接下载失败 5、README 无订阅链接跳过 21（产出率 58%，按有尝试采集的 53 个计算）


#### 🔵 [README 采集] 53 个仓库的 README 声明了订阅链接，提取 117984 条节点


#### 🔵 [延迟排序] 3918/3918 个服务器 TCP 可达（100%），延迟中位数 218ms，<100ms 共 166 条


#### 🔵 [延迟排序] 1374/3918 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 38 个仓库，可用率 >=10% 的 5 个，长期 0 可用 8 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 127、xray 304、clash 276、singbox 230


#### 🔵 [性能] 采集耗时 32 分钟

- 建议动作：偏慢，可关注是否有大文件反复重试

#### 🔵 [下载通道] jsDelivr 可用 3/4：fastly.jsdelivr.net、gcore.jsdelivr.net、testingcf.jsdelivr.net（不可达：cdn.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 5000/5000、search 30/30（已配置 token ghp_…x6hY）


### 待办清单（需人工或自动修复）

1. [warn] 1 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 部分链接下载失败) → 按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理
2. [warn] v2ray 可用率异常低 1.2%（30/2502） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
3. [warn] clash 可用率异常低 2.9%（72/2506） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
4. [warn] singbox 可用率异常低 2.0%（50/2503） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
5. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

## 2026-10-28 01:42

**结论：发现 1 个严重问题、5 个告警，需要处理**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 2744 |
| 采集总量(过滤前) | 6931 |
| 各内核订阅 | v2ray 2531、xray 2193、clash 2704、singbox 2611 |
| 协议分布 | hysteria2 2 / ss 91 / trojan 444 / vless 1480 / vmess 727 |
| TCP 可达 | 2744/2744（中位数 232ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '27/2118', 'xray': '127/2159', 'clash': '93/2508', 'singbox': '72/2509'} |
| 可用节点池 | v2ray 112、xray 234、clash 223、singbox 194 |

### 发现与建议

#### 🔴 [下载通道] 14/51 个仓库的文件下载失败（27%）

- 建议动作：查 stderr 的 `下载失败` 行确认是超时还是截断（现在带原因标签）；大文件（>2MB）应优先走 jsDelivr 并放宽超时，镜像列表用 health_check 的镜像探测结果剔除失效项

#### 🟡 [仓库效率] 扫描仓库 51 个：有产出 10、解析不到节点 14、下载失败 14、无候选文件 0、README 无订阅链接跳过 13（产出率 26%，按有尝试采集的 38 个计算）

- 建议动作：产出率偏低，优先按下面细分的失败类型逐项处理

#### 🟡 [来源稳定性] 1 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 解析不到节点)

- 建议动作：按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理

#### 🟡 [验证] v2ray 可用率异常低 1.3%（27/2118）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [验证] singbox 可用率异常低 2.9%（72/2509）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 2744 条；各内核订阅：v2ray 2531、xray 2193、clash 2704、singbox 2611


#### 🔵 [规模] 节点数 2744 达到目标 1000


#### 🔵 [README 采集] 38 个仓库的 README 声明了订阅链接，提取 29937 条节点


#### 🔵 [延迟排序] 2744/2744 个服务器 TCP 可达（100%），延迟中位数 232ms，<100ms 共 226 条


#### 🔵 [延迟排序] 822/2744 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 27 个仓库，可用率 >=10% 的 3 个，长期 0 可用 5 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 112、xray 234、clash 223、singbox 194


#### 🔵 [性能] 采集耗时 43 分钟

- 建议动作：偏慢，可关注是否有大文件反复重试

#### 🔵 [下载通道] jsDelivr 可用 3/4：fastly.jsdelivr.net、gcore.jsdelivr.net、testingcf.jsdelivr.net（不可达：cdn.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 60/60、search 10/10（匿名）


### 待办清单（需人工或自动修复）

1. [critical] 14/51 个仓库的文件下载失败（27%） → 查 stderr 的 `下载失败` 行确认是超时还是截断（现在带原因标签）；大文件（>2MB）应优先走 jsDelivr 并放宽超时，镜像列表用 health_check 的镜像探测结果剔除失效项
2. [warn] 扫描仓库 51 个：有产出 10、解析不到节点 14、下载失败 14、无候选文件 0、README 无订阅链接跳过 13（产出率 26%，按有尝试采集的 38 个计算） → 产出率偏低，优先按下面细分的失败类型逐项处理
3. [warn] 1 个高贡献仓库本次 0 条：crashgfw/free-airport-nodes(历史 1050 条, 解析不到节点) → 按括号里的原因分别处理：下载失败查通道/大文件策略，解析不到查格式覆盖，无候选文件查命名/子目录规则；都不是则属上游停更，无需处理
4. [warn] v2ray 可用率异常低 1.3%（27/2118） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
5. [warn] singbox 可用率异常低 2.9%（72/2509） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
6. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

## 2026-10-27 02:49

**结论：无严重问题，2 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 16620 |
| 各内核订阅 | v2ray 11012、xray 14931、clash 16432、singbox 15574 |
| 协议分布 | hy2 2 / hysteria 1 / hysteria2 186 / ss 613 / ssr 1 / trojan 402 / tuic 2 / vless 13336 / vmess 2077 |
| TCP 可达 | 6859/16629（中位数 234ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '69/3097', 'xray': '80/2592', 'clash': '75/792', 'singbox': '68/840'} |
| 可用节点池 | v2ray 98、xray 134、clash 148、singbox 141 |

### 发现与建议

#### 🟡 [验证] v2ray 可用率异常低 2.2%（69/3097）

- 建议动作：同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准

#### 🟡 [下载通道] 镜像失效 10/13：https://gh.monlor.com/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://ghfast.top/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 16620 条；各内核订阅：v2ray 11012、xray 14931、clash 16432、singbox 15574


#### 🔵 [规模] 节点数 16620 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 74 个：有产出 22、解析不到节点 19、下载失败 16、无候选文件 0、README 无订阅链接跳过 17（产出率 39%，按有尝试采集的 57 个计算）


#### 🔵 [README 采集] 57 个仓库的 README 声明了订阅链接，提取 91302 条节点


#### 🔵 [延迟排序] 6859/16629 个服务器 TCP 可达（41%），延迟中位数 234ms，<100ms 共 510 条


#### 🔵 [延迟排序] 2616/16629 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 27 个仓库，可用率 >=10% 的 10 个，长期 0 可用 4 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 98、xray 134、clash 148、singbox 141


#### 🔵 [性能] 采集耗时 34 分钟

- 建议动作：偏慢，可关注是否有大文件反复重试

#### 🔵 [下载通道] jsDelivr 可用 3/4：fastly.jsdelivr.net、gcore.jsdelivr.net、testingcf.jsdelivr.net（不可达：cdn.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 60/60、search 10/10（匿名）


### 待办清单（需人工或自动修复）

1. [warn] v2ray 可用率异常低 2.2%（69/3097） → 同上，先看单节点日志；若为协议不支持（如 v2fly 不支持 reality）属正常。注意探测地址是裸域 HTTPS（必须真出境），可用率天然低于旧版明文 HTTP 标准
2. [warn] 镜像失效 10/13：https://gh.monlor.com/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://ghfast.top/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

## 2026-10-26 23:25

**结论：无严重问题，1 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 7897 |
| 各内核订阅 | v2ray 7603、xray 6484、clash 7757、singbox 7546 |
| 协议分布 | hy2 3 / hysteria 1 / hysteria2 182 / ss 569 / ssr 1 / trojan 331 / tuic 2 / vless 4781 / vmess 2027 |
| TCP 可达 | 2842/7908（中位数 209ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '32/1000', 'xray': '37/1000', 'clash': '43/1000', 'singbox': '46/1000'} |
| 可用节点池 | v2ray 48、xray 66、clash 85、singbox 84 |

### 发现与建议

#### 🟡 [验证] v2ray 文件条数 52 ≠ 汇总可用数 32

- 建议动作：汇总与文件写出不一致，需排查

#### 🔵 [产物] 主清单 7897 条；各内核订阅：v2ray 7603、xray 6484、clash 7757、singbox 7546


#### 🔵 [规模] 节点数 7897 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 74 个：有产出 17、解析不到节点 18、下载失败 17、无候选文件 0、README 无订阅链接跳过 22（产出率 33%，按有尝试采集的 52 个计算）


#### 🔵 [README 采集] 52 个仓库的 README 声明了订阅链接，提取 66944 条节点


#### 🔵 [延迟排序] 2842/7908 个服务器 TCP 可达（36%），延迟中位数 209ms，<100ms 共 301 条


#### 🔵 [延迟排序] 1107/7908 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 21 个仓库，可用率 >=10% 的 6 个，长期 0 可用 3 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 48、xray 66、clash 85、singbox 84


#### 🔵 [性能] 采集耗时 36 分钟

- 建议动作：偏慢，可关注是否有大文件反复重试

### 待办清单（需人工或自动修复）

1. [warn] v2ray 文件条数 52 ≠ 汇总可用数 32 → 汇总与文件写出不一致，需排查

## 2026-10-25 10:45

**结论：无严重问题，1 个告警可优化**

### 关键指标

| 指标 | 值 |
|---|---|
| 输出目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes |
| 目标节点 | 1000 |
| 去重后节点 | 12993 |
| 各内核订阅 | v2ray 11463、xray 10727、clash 12873、singbox 12597 |
| 协议分布 | hysteria 1 / hysteria2 281 / ss 1837 / ssr 1 / trojan 1852 / tuic 2 / vless 5645 / vmess 3374 |
| TCP 可达 | 5013/13021（中位数 201ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'v2ray': '32/1000', 'xray': '37/1000', 'clash': '43/1000', 'singbox': '46/1000'} |
| 可用节点池 | v2ray 48、xray 66、clash 85、singbox 84 |

### 发现与建议

#### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

#### 🔵 [产物] 主清单 12993 条；各内核订阅：v2ray 11463、xray 10727、clash 12873、singbox 12597


#### 🔵 [规模] 节点数 12993 达到目标 1000


#### 🔵 [仓库效率] 扫描仓库 61 个：有产出 16、解析不到节点 16、下载失败 12、无候选文件 0、README 无订阅链接跳过 17（产出率 36%，按有尝试采集的 44 个计算）


#### 🔵 [README 采集] 44 个仓库的 README 声明了订阅链接，提取 54009 条节点


#### 🔵 [延迟排序] 5013/13021 个服务器 TCP 可达（38%），延迟中位数 201ms，<100ms 共 692 条


#### 🔵 [延迟排序] 2159/13021 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


#### 🔵 [仓库质量] 已评分 21 个仓库，可用率 >=10% 的 6 个，长期 0 可用 3 个（下次采集会自动跳过）


#### 🔵 [节点池] 池内节点：v2ray 48、xray 66、clash 85、singbox 84


#### 🔵 [性能] 采集耗时 43 分钟

- 建议动作：偏慢，可关注是否有大文件反复重试

#### 🔵 [下载通道] jsDelivr 可用 2/4：fastly.jsdelivr.net、gcore.jsdelivr.net（不可达：cdn.jsdelivr.net、testingcf.jsdelivr.net）


#### 🔵 [配额] GitHub 配额剩余 core 56/60、search 10/10（匿名）


### 待办清单（需人工或自动修复）

1. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选
