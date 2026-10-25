# 已知问题清单（时间倒序）

> 按日期倒序；自检发现的未修复问题、待观察项都记在这里

## 2026-10-25 自检发现

**结论：无严重问题，1 个告警可优化**

| 级别 | 领域 | 问题 | 建议动作 |
|---|---|---|---|
| warn | 下载通道 | 镜像失效 11/13：https://gh.monlor.com/、https://ghfast.top/、https://ghproxy.net/、https://gh-proxy.net/、https://hub.gitmirror.com/、https://gh.llkk.cc/、https://gitdl.cn/、https://ghproxy.cc/、https://ghp.ci/、https://ghps.cc/、https://raw.gitmirror.com/；可用：https://gh-proxy.com/、https://gh-proxy.org/ | 失效项已从下载链剔除（不再逐个重试），本次不影响采集。若可用数降到 1 个，建议在 DEFAULT_MIRROR_PREFIXES 补新候选 |

## 2026-10-25 仓库质量分倒挂（已修复）

- **现象**：`seed_repos.json` 里 0% 可用率的仓库质量分 30.0，而 11.4% 可用率的
  `0xRadikal/Free-v2ray-Configs` 只有 8.0 分——全死的仓库排在活的前面
- **根因**（`quality_score()` 两处叠加）：
  1. `lat = 100.0 if not avg_latency`——没延迟样本（= 一个节点都没通过）被当满分 30 分
  2. 延迟归零点 1500ms 太苛刻，免费节点普遍 1500~7000ms，延迟项恒为 0，30 分权重等于废掉
- **影响面**：`repo_sort_key()` 用 `avail_rate` 而非 `quality`，采集优先级一直是安全的；
  只污染 `report.md` 排行与 `seed_repos.json` 展示
- **修复**：可用率 ≤0 或延迟缺失时延迟项记 0；归零点 1500ms → 5000ms；存量 16 个仓库已回填

## 2026-10-25 下载镜像 10/13 失效（观察项）

- 实测可用仅 `https://gh-proxy.com/`、`https://gh-proxy.org/`、`https://gh.monlor.com/`
- raw 直连不可用；jsDelivr 2/4（`fastly.jsdelivr.net`、`gcore.jsdelivr.net`）
- 判定：公共代理域名成批烂掉是常态，脚本已有「备用候选自动补位」+「只用探活通过的通道」机制，
  本次采集仍正常完成（6632 条），**不作为故障处理**，继续观察
- 若某天可用通道 <2 个且采集节点数明显下滑，再扩充 `MIRROR_SPARE_CANDIDATES`
