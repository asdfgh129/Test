# 免费节点采集报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-10-25 13:35

### 概览

- 扫描仓库：**30** 个
- 抓取订阅文件：**11** 个
- 原始提取节点：**23319** 条
- 两级去重后（完整链接 + 服务器:端口）：**6650** 条（剔除重复 16669 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 5633、xray 6419、clash 6615、singbox 6529
- 耗时：962 秒

### TCP 延迟分布

- 可达服务器：**2016/6650**（延迟中位数 205ms，最低 27ms）
- Cloudflare 前置节点：**806** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 229 |
| 100-300ms | 1344 |
| 300-800ms | 363 |
| >800ms | 80 |
| 不可达（排在订阅末尾） | 4634 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **20** 个仓库在 README 里给出订阅链接，从中提取 **23319** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| 0xRadikal/Free-v2ray-Configs | 10 | 11423 |
| MatinGhanbari/v2ray-configs | 10 | 8127 |
| Firmfox/Proxify | 10 | 963 |
| igareck/vpn-configs-for-russia | 10 | 784 |
| iboxz/free-v2ray-collector | 5 | 722 |
| chengaopan/AutoMergePublicNodes | 2 | 435 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 10 | 395 |
| crashgfw/free-airport-nodes | 10 | 270 |
| snakem982/proxypool | 3 | 168 |
| zhuhaiuk/free-nodes | 3 | 18 |
| Pawdroid/Free-servers | 1 | 14 |
| free18/v2ray | 2 | 0 |
| crossxx-labs/free-proxy | 3 | 0 |
| bq2015/FreeProxies | 2 | 0 |
| whoahaow/rjsxrd | 10 | 0 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vmess | 3028 |
| vless | 1649 |
| ss | 1292 |
| trojan | 466 |
| hysteria2 | 181 |
| ssr | 34 |

### 输出文件

- `v2ray_sub.txt`（5633 条，base64 订阅）
- `xray_sub.txt`（6419 条，base64 订阅）
- `clash_sub.yaml`（6615 个代理）
- `singbox_sub.json`（6529 个 outbound）
- `nodes_uris.txt`（6632 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| Pawdroid/Free-servers | 81.9 | 100%（4/4） | 906ms | 25 |
| snakem982/proxypool | 43.7 | 38%（3/8） | 629ms | 338 |
| 0xRadikal/Free-v2ray-Configs | 19.7 | 28%（9/32） | 2759ms | 23084 |
| Epodonios/v2ray-configs | 13.9 | 3%（2/78） | 897ms | 22657 |
| igareck/vpn-configs-for-russia | 12.9 | 18%（7/38） | 1788ms | 1667 |

- 本次采集优先级（质量从高到低）：Pawdroid/Free-servers(可用率100%/质量81.9)、snakem982/proxypool(可用率38%/质量43.7)、0xRadikal/Free-v2ray-Configs(可用率28%/质量19.7)、igareck/vpn-configs-for-russia(可用率18%/质量12.9)、Epodonios/v2ray-configs(可用率3%/质量13.9)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| Pawdroid/Free-servers | ⭐19620 | 2026-10-25 |
| igareck/vpn-configs-for-russia | ⭐9315 | 2026-10-25 |
| chengaopan/AutoMergePublicNodes | ⭐8268 | 2026-10-25 |
| free18/v2ray | ⭐5745 | 2026-10-25 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5654 | 2026-10-25 |
| Alvin9999-newpac/fanqiang | ⭐3107 | 2026-10-25 |
| snakem982/proxypool | ⭐2210 | 2026-10-25 |
| crossxx-labs/free-proxy | ⭐1838 | 2026-10-25 |
| Hidashimora/free-vpn-anti-rkn | ⭐1061 | 2026-10-25 |
| bq2015/FreeProxies | ⭐903 | 2026-10-25 |
| whoahaow/rjsxrd | ⭐865 | 2026-10-25 |
| 0xRadikal/Free-v2ray-Configs | ⭐766 | 2026-10-25 |
| ts-sf/fly | ⭐712 | 2026-10-25 |
| MatinGhanbari/v2ray-configs | ⭐689 | 2026-10-25 |
| SoliSpirit/v2ray-configs | ⭐634 | 2026-10-25 |
| OpenNetCN/clash | ⭐632 | 2026-10-25 |
| kort0881/vpn-vless-configs-russia | ⭐610 | 2026-10-25 |
| tolinkshare2/tolinkshare2.github.io | ⭐526 | 2026-10-25 |
| sunmiao4458/free-proxy-airport | ⭐518 | 2026-10-25 |
| sinavm/SVM | ⭐433 | 2026-10-25 |
| zhuhaiuk/free-nodes | ⭐374 | 2026-10-25 |
| cbusifabcap/daily_free_vpn | ⭐360 | 2026-10-25 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-10-25 |
| crashgfw/free-airport-nodes | ⭐295 | 2026-10-25 |
| iboxz/free-v2ray-collector | ⭐188 | 2026-10-25 |
| xOS/Config | ⭐183 | 2026-10-25 |
| HakurouKen/free-node | ⭐180 | 2026-10-25 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-25 |
| thsrite/configflow | ⭐154 | 2026-10-25 |
| Firmfox/Proxify | ⭐145 | 2026-10-25 |

### 节点来源分布（去重后，前 20）

- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/all_sub.txt`：2970 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：915 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/filtered/subs/vmess.txt`：676 个节点
- `chengaopan/AutoMergePublicNodes/list.txt`：186 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/super-sub.txt`：177 个节点
- `iboxz/free-v2ray-collector/main/mix.txt`：175 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub3.txt`：171 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub39.txt`：159 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub2.txt`：128 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub1.txt`：113 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/filtered/subs/hysteria2.txt`：96 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub4.txt`：87 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→www.xrayvip.com`：81 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→raw.githubusercontent.com`：54 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：53 个节点
- `0xRadikal/Free-v2ray-Configs/top100.txt`：46 个节点
- `Firmfox/Proxify/v2ray_configs/subscriptions/subscription-2.txt`：43 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/combine/clash.config.yaml`：41 个节点
- `Firmfox/Proxify/v2ray_configs/subscriptions/subscription-4.txt`：40 个节点
- `Firmfox/Proxify/v2ray_configs/subscriptions/subscription-6.txt`：40 个节点
