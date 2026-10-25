# 免费节点采集报告 · 2026-10-25

## 概览

- 扫描仓库：**12** 个
- 抓取订阅文件：**5** 个
- 原始提取节点：**35382** 条
- 两级去重后（完整链接 + 服务器:端口）：**4094** 条（剔除重复 31288 条）
- 耗时：512 秒

## TCP 延迟分布

- 可达服务器：**1472/4094**（延迟中位数 230ms，最低 28ms）
- Cloudflare 前置节点：**438** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 101 |
| 100-300ms | 1018 |
| 300-800ms | 327 |
| >800ms | 26 |
| 不可达（排在订阅末尾） | 2622 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

## README 订阅链接采集

共 **10** 个仓库在 README 里给出订阅链接，从中提取 **35382** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| Epodonios/v2ray-configs | 7 | 22657 |
| 0xRadikal/Free-v2ray-Configs | 10 | 11661 |
| igareck/vpn-configs-for-russia | 10 | 883 |
| snakem982/proxypool | 3 | 170 |
| Pawdroid/Free-servers | 1 | 11 |
| crossxx-labs/free-proxy | 3 | 0 |
| bq2015/FreeProxies | 2 | 0 |
| deezertidal/freevpn | 1 | 0 |
| whoahaow/rjsxrd | 10 | 0 |
| SoliSpirit/v2ray-configs | 5 | 0 |

## 协议分布

| 协议 | 数量 |
|---|---|
| vless | 3123 |
| ss | 442 |
| trojan | 243 |
| vmess | 232 |
| hysteria2 | 53 |
| ssr | 1 |

## 输出文件

- v2ray 订阅（base64）：`C:/Users/bemin/WorkBuddy/Test/free-nodes/2026-10-25\v2ray_sub.txt`（4094 条 URI）
- Clash 配置：`C:/Users/bemin/WorkBuddy/Test/free-nodes/2026-10-25\clash.yaml`（4081 个代理）
- sing-box 配置：`C:/Users/bemin/WorkBuddy/Test/free-nodes/2026-10-25\singbox.json`（4081 个 outbound）
- 节点元数据（延迟 + 来源仓库）：`C:/Users/bemin/WorkBuddy/Test/free-nodes/2026-10-25\nodes_meta.json`

## 仓库质量排行（历史四内核实测）

- 暂无历史实测数据，本次验证后会自动建立质量评分



## 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| Pawdroid/Free-servers | ⭐19620 | 2026-10-25 |
| igareck/vpn-configs-for-russia | ⭐9314 | 2026-10-25 |
| Epodonios/v2ray-configs | ⭐3309 | 2026-10-25 |
| Alvin9999-newpac/fanqiang | ⭐3107 | 2026-10-25 |
| snakem982/proxypool | ⭐2210 | 2026-10-25 |
| crossxx-labs/free-proxy | ⭐1838 | 2026-10-25 |
| bq2015/FreeProxies | ⭐903 | 2026-10-25 |
| deezertidal/freevpn | ⭐887 | 2026-10-25 |
| whoahaow/rjsxrd | ⭐865 | 2026-10-25 |
| ermaozi01/free_clash_vpn | ⭐815 | 2026-10-25 |
| 0xRadikal/Free-v2ray-Configs | ⭐766 | 2026-10-25 |
| SoliSpirit/v2ray-configs | ⭐634 | 2026-10-25 |

## 节点来源分布（去重后，前 20）

- `Epodonios/v2ray-configs/Splitted-By-Protocol/vless.txt`：2548 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs_base64.txt`：489 个节点
- `Epodonios/v2ray-configs/Splitted-By-Protocol/ss.txt`：401 个节点
- `Epodonios/v2ray-configs/Splitted-By-Protocol/vmess.txt`：180 个节点
- `Epodonios/v2ray-configs/Splitted-By-Protocol/trojan.txt`：150 个节点
- `Epodonios/v2ray-configs/All_Configs_Sub.txt`：88 个节点
- `igareck/vpn-configs-for-russia/BLACK_VLESS_RUS_mobile.txt`：84 个节点
- `igareck/vpn-configs-for-russia/BLACK_VLESS_RUS.txt`：53 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：40 个节点
- `0xRadikal/Free-v2ray-Configs/top100.txt`：21 个节点
- `igareck/vpn-configs-for-russia/README→translate.yandex.ru`：15 个节点
- `Pawdroid/Free-servers/README→sub.shadowsharing.com`：11 个节点
- `igareck/vpn-configs-for-russia/BLACK_SS+All_RUS.txt`：5 个节点
- `igareck/vpn-configs-for-russia/Export/Clash/RU_DIRECT/BLACK_VLESS_RUS_mobile_clash_rudirect.yaml`：5 个节点
- `igareck/vpn-configs-for-russia/Export/Clash/RU_DIRECT/BLACK_VLESS_RUS_clash_rudirect.yaml`：3 个节点
- `igareck/vpn-configs-for-russia/Export/Clash/RU_DIRECT/BLACK_SS+All_RUS_clash_rudirect.yaml`：1 个节点
