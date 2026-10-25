# 免费节点采集报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-10-25 22:44

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**16** 个
- 原始提取节点：**54009** 条
- 两级去重后（完整链接 + 服务器:端口）：**13021** 条（剔除重复 40988 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 11463、xray 10727、clash 12873、singbox 12597
- 耗时：2554 秒

### TCP 延迟分布

- 可达服务器：**5013/13021**（延迟中位数 201ms，最低 28ms）
- Cloudflare 前置节点：**2159** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 692 |
| 100-300ms | 3428 |
| 300-800ms | 741 |
| >800ms | 152 |
| 不可达（排在订阅末尾） | 8008 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **44** 个仓库在 README 里给出订阅链接，从中提取 **54009** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| barry-far/V2ray-Config | 10 | 17397 |
| NiREvil/vless | 10 | 11645 |
| Delta-Kronecker/V2ray-Config | 10 | 9561 |
| Barabama/FreeNodes | 10 | 6995 |
| PuddinCat/BestClash | 10 | 3923 |
| dongchengjie/airport | 10 | 1487 |
| ShatakVPN/ConfigForge-V2Ray | 8 | 939 |
| igareck/vpn-configs-for-russia | 10 | 834 |
| peasoft/NoMoreWalls | 1 | 437 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | 2 | 252 |
| crashgfw/free-airport-nodes | 10 | 240 |
| snakem982/proxypool | 3 | 180 |
| free-nodes/clashfree | 1 | 81 |
| zhuhaiuk/free-nodes | 3 | 16 |
| Pawdroid/Free-servers | 3 | 12 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5654 |
| vmess | 3389 |
| trojan | 1852 |
| ss | 1837 |
| hysteria2 | 281 |
| ssr | 5 |
| tuic | 2 |
| hysteria | 1 |

### 输出文件

- `v2ray_sub.txt`（11463 条，base64 订阅）
- `xray_sub.txt`（10727 条，base64 订阅）
- `clash_sub.yaml`（12873 个代理）
- `singbox_sub.json`（12597 个 outbound）
- `nodes_uris.txt`（12993 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| snakem982/proxypool | 63.8 | 62%（96/155） | 1586ms | 518 |
| Pawdroid/Free-servers | 54.9 | 65%（26/40） | 3440ms | 37 |
| 0xRadikal/Free-v2ray-Configs | 29.0 | 11%（48/420） | 1499ms | 23084 |
| Epodonios/v2ray-configs | 26.4 | 3%（2/78） | 897ms | 22657 |
| igareck/vpn-configs-for-russia | 23.3 | 33%（2/6） | 7114ms | 2501 |
| MatinGhanbari/v2ray-configs | 0.0 | 0%（0/164） | -ms | 8127 |
| Firmfox/Proxify | 0.0 | 0%（0/8） | -ms | 963 |
| iboxz/free-v2ray-collector | 0.0 | 0%（0/4） | -ms | 722 |
| chengaopan/AutoMergePublicNodes | 0.0 | 0%（0/4） | -ms | 435 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 0.0 | 0%（0/12） | -ms | 395 |

- 本次采集优先级（质量从高到低）：Pawdroid/Free-servers(可用率65%/质量54.9)、snakem982/proxypool(可用率62%/质量63.8)、igareck/vpn-configs-for-russia(可用率33%/质量23.3)、0xRadikal/Free-v2ray-Configs(可用率11%/质量29.0)、Epodonios/v2ray-configs(可用率3%/质量26.4)、MatinGhanbari/v2ray-configs(可用率0%/质量0.0)、Firmfox/Proxify(可用率0%/质量0.0)、iboxz/free-v2ray-collector(可用率0%/质量0.0)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| Pawdroid/Free-servers | ⭐19631 | 2026-10-25 |
| free-nodes/clashfree | ⭐17042 | 2026-10-25 |
| DiningFactory/panda-vpn-pro | ⭐16831 | 2026-10-25 |
| free-nodes/v2rayfree | ⭐14524 | 2026-10-25 |
| ermaozi/get_subscribe | ⭐9386 | 2026-10-25 |
| igareck/vpn-configs-for-russia | ⭐9319 | 2026-10-25 |
| chengaopan/AutoMergePublicNodes | ⭐8272 | 2026-10-25 |
| free18/v2ray | ⭐5750 | 2026-10-25 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5659 | 2026-10-25 |
| peasoft/NoMoreWalls | ⭐3563 | 2026-10-25 |
| Barabama/FreeNodes | ⭐3318 | 2026-10-25 |
| Epodonios/v2ray-configs | ⭐3309 | 2026-10-25 |
| Alvin9999-newpac/fanqiang | ⭐3112 | 2026-10-25 |
| barry-far/V2ray-Config | ⭐2579 | 2026-10-25 |
| snakem982/proxypool | ⭐2214 | 2026-10-25 |
| PuddinCat/BestClash | ⭐2044 | 2026-10-25 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1854 | 2026-10-25 |
| crossxx-labs/free-proxy | ⭐1840 | 2026-10-25 |
| qusong0627/QuantMind | ⭐1794 | 2026-10-25 |
| LancelotRar/best-cf-ips | ⭐1601 | 2026-10-25 |
| Leon406/SubCrawler | ⭐1572 | 2026-10-25 |
| everett7623/airport-recommendations-2026 | ⭐1436 | 2026-10-25 |
| NiREvil/vless | ⭐1356 | 2026-10-25 |
| shaoyouvip/free | ⭐1289 | 2026-10-25 |
| jdnei/JiChangTuiJian | ⭐1273 | 2026-10-25 |
| cfal/shoes | ⭐1264 | 2026-10-25 |
| Hidashimora/free-vpn-anti-rkn | ⭐1061 | 2026-10-25 |
| SubBoost/subboost | ⭐974 | 2026-10-25 |
| bq2015/FreeProxies | ⭐905 | 2026-10-25 |
| deezertidal/freevpn | ⭐887 | 2026-10-25 |
| whoahaow/rjsxrd | ⭐865 | 2026-10-25 |
| ermaozi01/free_clash_vpn | ⭐815 | 2026-10-25 |
| nevertoday/xiaoxiaodong-vps | ⭐796 | 2026-10-25 |
| 0xRadikal/Free-v2ray-Configs | ⭐766 | 2026-10-25 |
| dongchengjie/airport | ⭐735 | 2026-10-25 |
| ts-sf/fly | ⭐712 | 2026-10-25 |
| MatinGhanbari/v2ray-configs | ⭐688 | 2026-10-25 |
| gslege/CloudflareIP | ⭐674 | 2026-10-25 |
| raine/claude-code-proxy | ⭐669 | 2026-10-25 |
| SoliSpirit/v2ray-configs | ⭐633 | 2026-10-25 |
| hello-world-1989/cn-news | ⭐632 | 2026-10-25 |
| OpenNetCN/clash | ⭐632 | 2026-10-25 |
| kort0881/vpn-vless-configs-russia | ⭐612 | 2026-10-25 |
| jichangtuijian-cheap/cheap-airports | ⭐611 | 2026-10-25 |
| Huibq/TrojanLinks | ⭐548 | 2026-10-25 |
| tolinkshare2/tolinkshare2.github.io | ⭐526 | 2026-10-25 |
| CCSH/IPTV | ⭐519 | 2026-10-25 |
| sunmiao4458/free-proxy-airport | ⭐518 | 2026-10-25 |
| itsyebekhe/PSG | ⭐447 | 2026-10-25 |
| kooker/FreeSubsCheck | ⭐440 | 2026-10-25 |
| sinavm/SVM | ⭐432 | 2026-10-25 |
| SubConv/SubConv | ⭐409 | 2026-10-25 |
| Epodonios/bulk-xray-v2ray-vless-vmess-...-configs | ⭐381 | 2026-10-25 |
| zhuhaiuk/free-nodes | ⭐377 | 2026-10-25 |
| ShatakVPN/ConfigForge-V2Ray | ⭐375 | 2026-10-25 |
| Delta-Kronecker/V2ray-Config | ⭐366 | 2026-10-25 |
| cbusifabcap/daily_free_vpn | ⭐360 | 2026-10-25 |
| ovmvo/FreeSub | ⭐345 | 2026-10-25 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐322 | 2026-10-25 |
| MhdiTaheri/V2rayCollector | ⭐321 | 2026-10-25 |
| F0rc3Run/F0rc3Run | ⭐319 | 2026-10-25 |
| WLget/V2Ray_configs_64 | ⭐314 | 2026-10-25 |
| clashv2ray-hub/clashfree | ⭐309 | 2026-10-25 |
| clashv2ray-hub/v2rayfree | ⭐300 | 2026-10-25 |
| crashgfw/free-airport-nodes | ⭐295 | 2026-10-25 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-10-25 |
| wenxig/dongtai-sub | ⭐263 | 2026-10-25 |
| sakha1370/OpenRay | ⭐249 | 2026-10-25 |
| yanisplugg/yptun | ⭐220 | 2026-10-25 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐209 | 2026-10-25 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-25 |
| tglaoshiji/nodeshare | ⭐197 | 2026-10-25 |
| mheidari98/.proxy | ⭐190 | 2026-10-25 |
| iboxz/free-v2ray-collector | ⭐188 | 2026-10-25 |
| xOS/Config | ⭐183 | 2026-10-25 |
| HakurouKen/free-node | ⭐180 | 2026-10-25 |
| V2RayRoot/V2RayConfig | ⭐173 | 2026-10-25 |
| shabane/kamaji | ⭐173 | 2026-10-25 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐163 | 2026-10-25 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-25 |

### 节点来源分布（去重后，前 20）

- `PuddinCat/BestClash/README→raw.githubusercontent.com`：3049 个节点
- `barry-far/V2ray-Config/All_Configs_Sub.txt`：2470 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：2387 个节点
- `Barabama/FreeNodes/README→gh-proxy.com`：1988 个节点
- `dongchengjie/airport/subs/merged/tested_within.yaml`：1230 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：818 个节点
- `peasoft/NoMoreWalls/list.txt`：334 个节点
- `barry-far/V2ray-Config/Sub1.txt`：133 个节点
- `barry-far/V2ray-Config/Sub3.txt`：116 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/ss.txt`：78 个节点
- `barry-far/V2ray-Config/Sub2.txt`：74 个节点
- `ShatakVPN/ConfigForge-V2Ray/configs/all.txt`：72 个节点
- `free-nodes/clashfree/clash20261025.yml`：64 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：57 个节点
- `crashgfw/free-airport-nodes/README→ndxy.fn0821.xyz`：30 个节点
- `igareck/vpn-configs-for-russia/BLACK_VLESS_RUS_mobile.txt`：26 个节点
- `Delta-Kronecker/V2ray-Config/config/batches/v2ray/batch_001.txt`：19 个节点
- `igareck/vpn-configs-for-russia/Export/Clash/RU_DIRECT/BLACK_VLESS_RUS_mobile_clash_rudirect.yaml`：16 个节点
- `xrayfree/free-ssr-ss-v2ray-vpn-clash/README→www.xrayvip.com`：14 个节点
- `Pawdroid/Free-servers/README→sub.shadowsharing.com`：12 个节点
