# 已知问题清单（时间倒序）

> 按日期倒序；自检发现的未修复问题、待观察项都记在这里

## 2026-10-25

### 下载镜像 10/13 失效（观察项）

- 实测可用仅 `https://gh-proxy.com/`、`https://gh-proxy.org/`、`https://gh.monlor.com/`
- raw 直连不可用；jsDelivr 2/4（`fastly.jsdelivr.net`、`gcore.jsdelivr.net`）
- 判定：公共代理域名成批烂掉是常态，脚本已有「备用候选自动补位」+「只用探活通过的通道」机制，
  本次采集仍正常完成（6632 条），**不作为故障处理**，继续观察
- 若某天可用通道 <2 个且采集节点数明显下滑，再扩充 `MIRROR_SPARE_CANDIDATES`

### 已修复项已迁入 changelog.md

- 自检误判「0 条节点」（主清单明文被当 base64）、sing-box 计数 +1、v2ray 版本查询 404
  三项已在 2026-10-25 修复并验证，不再列为待办
