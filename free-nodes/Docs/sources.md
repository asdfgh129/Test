# 节点来源参考

## 三级采集来源（自适应）

1. **动态发现（主通道）**：GitHub Search API 搜索当天（不足时放宽到前一天）有更新的仓库，10 组关键词自动捕捉新聚合仓库
2. **动态仓库清单（seed_repos.json）**：每次运行自动沉淀贡献过节点的仓库，记录 star 与累计贡献数，阶段 3 按贡献优先补充采集
3. **内置初始种子**：barry-far/V2ray-Configs、Epodonios/v2ray-configs、mahdibland/V2RayAggregator、peasoft/NoMoreWalls、Au1rxx/free-vpn-subscriptions（⭐1000+，Clash/sing-box/V2Ray 订阅聚合）

> 仓库地址会随时间失效。清单是动态自维护的：不再贡献节点的仓库会在排序中自然下沉，贡献多的自动上升，无需人工维护。

## README 是更可靠的订阅入口

很多仓库的订阅文件路径**只写在 README 里**（文件名不带 sub/node 关键字），目录扫描挑不出来。采集时每个仓库都会先读 README 并跟随其中声明的订阅链接。

2026-10-24 实测（README 单条链接的产出）：

| 仓库                            | README 声明的入口                                                | 单次提取节点     |
| ----------------------------- | ----------------------------------------------------------- | ---------- |
| Epodonios/v2ray-configs       | `All_Configs_Sub.txt` + `Splitted-By-Protocol/*`            | 7600+（单文件） |
| mahdibland/V2RayAggregator    | 指向 ShadowsocksAggregator / SSAggregator 的外部订阅               | 12000+（原始） |
| Au1rxx/free-vpn-subscriptions | `output/by-country/{clash,singbox,v2ray}-*.{yaml,json,txt}` | 每国 180-570 |
| peasoft/NoMoreWalls           | `list.txt`（README 里同时列了 4 个 CDN 域名，已归一去重）                   | 456        |
| Pawdroid/Free-servers         | `sub`                                                       | 20         |

> 结论：优先相信 README 声明的入口，再用目录扫描兜底。README 一个链接的产出常常超过扫 3 个文件的合计。

## 关键词维护

搜索关键词位于 `scripts/collect_nodes.py` 的 `SEARCH_QUERIES`（当前 10 组）。调整建议：

- 想扩大覆盖：增加 `"hysteria2 free"`、`"airport subscription"`、`"翻墙 节点"` 等
- 想减少噪音：提高 `--min-stars`（如 50）或减少查询组数（匿名搜索限额 10 次/分钟，每组间隔 6.5s，10 组约 65 秒/阶段）

## 限额与稳定性

- 匿名 GitHub API：搜索 10 次/分钟（脚本内已内置 6.5s 间隔）、核心 60 次/小时
- 提供令牌后限额大幅提升：`--token` 或环境变量 `GITHUB_TOKEN`
- raw.githubusercontent.com 直连经常被网络重置：脚本内置 **gh-proxy.com 等 4 个加速镜像前缀**自动回退（详见 SKILL.md「下载回退链」），镜像失效时改 `DEFAULT_MIRROR_PREFIXES` 或 `FREE_NODES_MIRRORS` 环境变量即可
- 2026-10-24 实测：raw 直连失败时 gh-proxy.com 镜像成功取回节点
