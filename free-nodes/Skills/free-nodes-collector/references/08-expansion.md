# 三级自适应扩量、动态仓库清单、去重规则、仓库发现机制

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

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
