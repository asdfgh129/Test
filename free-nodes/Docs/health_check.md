# 每日自检报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

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
