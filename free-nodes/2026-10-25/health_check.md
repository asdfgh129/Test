# 自检报告 · 2026-10-25

**结论：无严重问题，5 个告警可优化**

## 关键指标

| 指标 | 值 |
|---|---|
| 采集目录 | C:\Users\bemin\WorkBuddy\Test\free-nodes\2026-10-25 |
| 目标节点 | 1000 |
| 去重后节点 | 4094 |
| clash 代理 | 4081 |
| singbox outbound | 4082 |
| 协议分布 | hy2 7 / hysteria2 46 / ss 442 / ssr 1 / trojan 243 / vless 3123 / vmess 232 |
| TCP 可达 | 1472/4094（中位数 230ms） |
| 验证已执行 | 是 |
| 各内核可用 | {'xray': '5/40', 'v2ray': '5/40', 'mihomo': '10/40', 'singbox': '5/40'} |
| 可用节点池 | xray 5、v2ray 5、mihomo 10、singbox 5 |

## 发现与建议

### 🟡 [验证] xray 仅 5 个可用（测试 40 个，可用率 12%）

- 建议动作：这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量

### 🟡 [验证] v2ray 仅 5 个可用（测试 40 个，可用率 12%）

- 建议动作：这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量

### 🟡 [验证] singbox 仅 5 个可用（测试 40 个，可用率 12%）

- 建议动作：这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量

### 🟡 [下载通道] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/

- 建议动作：失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选

### 🟡 [配额] GitHub 配额剩余 core 16/60、search 10/10（匿名）

- 建议动作：匿名配额紧张，采集可能被截断；建议给自动化配置 GITHUB_TOKEN

### 🔵 [规模] 节点数 4094 达到目标 1000


### 🔵 [仓库效率] 扫描仓库 12 个：有产出 5、解析不到节点 0、下载失败 0、无候选文件 0、README 无订阅链接跳过 7（产出率 100%，按有尝试采集的 5 个计算）


### 🔵 [README 采集] 10 个仓库的 README 声明了订阅链接，提取 35382 条节点


### 🔵 [延迟排序] 1472/4094 个服务器 TCP 可达（36%），延迟中位数 230ms，<100ms 共 101 条


### 🔵 [延迟排序] 438/4094 条为 Cloudflare 前置节点（TCP 快但代理多不通），已排在真实节点之后


### 🔵 [仓库质量] 已评分 5 个仓库，可用率 >=10% 的 4 个，长期 0 可用 0 个（下次采集会自动跳过）


### 🔵 [节点池] 池内节点：xray 5、v2ray 5、mihomo 10、singbox 5


### 🔵 [下载通道] jsDelivr 可用 1/4：fastly.jsdelivr.net（不可达：gcore.jsdelivr.net、cdn.jsdelivr.net、testingcf.jsdelivr.net）


## 待办清单（需人工或自动修复）

1. [warn] xray 仅 5 个可用（测试 40 个，可用率 12%） → 这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量
2. [warn] v2ray 仅 5 个可用（测试 40 个，可用率 12%） → 这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量
3. [warn] singbox 仅 5 个可用（测试 40 个，可用率 12%） → 这是节点池质量问题而非采集量问题：免费节点本身大量失效。建议优先扩大高质量来源（提高 --target-nodes、补充高 star 种子仓库），而不是继续堆节点数量
4. [warn] 镜像失效 10/13：https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/、https://gh.monlor.com/ → 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选
5. [warn] GitHub 配额剩余 core 16/60、search 10/10（匿名） → 匿名配额紧张，采集可能被截断；建议给自动化配置 GITHUB_TOKEN
