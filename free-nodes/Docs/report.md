# 免费节点采集报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-10-31 22:24

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**28** 个
- 原始提取节点：**140863** 条
- 两级去重后（完整链接 + 服务器:端口）：**7818** 条（剔除重复 122604 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 6296、xray 6891、clash 7776、singbox 7300
- 耗时：1322 秒

### TCP 延迟分布

- 可达服务器：**7818/7818**（延迟中位数 216ms，最低 16ms）
- Cloudflare 前置节点：**2771** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 801 |
| 100-300ms | 5277 |
| 300-800ms | 1350 |
| >800ms | 390 |
| 不可达（排在订阅末尾） | 0 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **50** 个仓库在 README 里给出订阅链接，从中提取 **140863** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| sakha1370/OpenRay | 10 | 29563 |
| SoliSpirit/v2ray-configs | 5 | 22420 |
| liketolivefree/kobabi | 10 | 21823 |
| Barabama/FreeNodes | 10 | 15728 |
| shabane/kamaji | 10 | 12108 |
| NiREvil/vless | 10 | 11272 |
| Delta-Kronecker/V2ray-Config | 10 | 7424 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7188 |
| whoahaow/rjsxrd | 10 | 3846 |
| DukeMehdi/FreeList-V2ray-Configs | 8 | 2886 |
| danmaifu/mianfeijiedian | 2 | 2310 |
| igareck/vpn-configs-for-russia | 10 | 1120 |
| kooker/FreeSubsCheck | 5 | 677 |
| F0rc3Run/F0rc3Run | 7 | 563 |
| peasoft/NoMoreWalls | 1 | 477 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 13517 |
| vmess | 2203 |
| trojan | 1180 |
| ss | 1038 |
| hysteria2 | 308 |
| ssr | 9 |
| hysteria | 2 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（6296 条，base64 订阅）
- `xray_sub.txt`（6891 条，base64 订阅）
- `clash_sub.yaml`（7776 个代理）
- `singbox_sub.json`（7300 个 outbound）
- `nodes_uris.txt`（7811 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| F0rc3Run/F0rc3Run | 40.1 | 31%（37/119） | 1949ms | 1768 |
| Pawdroid/Free-servers | 29.0 | 13%（3/23） | 1676ms | 102 |
| kooker/FreeSubsCheck | 22.8 | 7%（3/41） | 2048ms | 3349 |
| whoahaow/rjsxrd | 22.7 | 4%（17/480） | 1628ms | 10771 |
| snakem982/proxypool | 22.0 | 6%（12/202） | 2020ms | 1593 |
| peasoft/NoMoreWalls | 20.8 | 5%（6/111） | 2163ms | 3066 |
| NiREvil/vless | 20.1 | 2%（135/7153） | 1866ms | 57004 |
| Delta-Kronecker/V2ray-Config | 19.6 | 0%（7/1531） | 1793ms | 24306 |
| SoliSpirit/v2ray-configs | 17.4 | 0%（27/5591） | 2155ms | 44437 |
| hello-world-1989/cn-news | 16.8 | 17%（1/6） | 4141ms | 18 |
| PuddinCat/BestClash | 0.5 | 1%（3/449） | 6091ms | 3923 |
| liketolivefree/kobabi | 0.1 | 0%（1/1575） | 12758ms | 44861 |

- 本次采集优先级（质量从高到低）：F0rc3Run/F0rc3Run(可用率31%/质量40.1)、hello-world-1989/cn-news(可用率17%/质量16.8)、Pawdroid/Free-servers(可用率13%/质量29.0)、kooker/FreeSubsCheck(可用率7%/质量22.8)、snakem982/proxypool(可用率6%/质量22.0)、peasoft/NoMoreWalls(可用率5%/质量20.8)、whoahaow/rjsxrd(可用率4%/质量22.7)、NiREvil/vless(可用率2%/质量20.1)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| Pawdroid/Free-servers | ⭐19726 | 2026-10-31 |
| free-nodes/clashfree | ⭐17132 | 2026-10-31 |
| free-nodes/v2rayfree | ⭐14693 | 2026-10-31 |
| ddgksf2013/ddgksf2013 | ⭐13817 | 2026-10-31 |
| ermaozi/get_subscribe | ⭐9414 | 2026-10-31 |
| igareck/vpn-configs-for-russia | ⭐9393 | 2026-10-31 |
| chengaopan/AutoMergePublicNodes | ⭐8306 | 2026-10-31 |
| free18/v2ray | ⭐5809 | 2026-10-31 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5685 | 2026-10-31 |
| nguyenphutrong/quotio | ⭐4902 | 2026-10-31 |
| peasoft/NoMoreWalls | ⭐3585 | 2026-10-31 |
| Barabama/FreeNodes | ⭐3354 | 2026-10-31 |
| Alvin9999-newpac/fanqiang | ⭐3170 | 2026-10-31 |
| barry-far/V2ray-Config | ⭐2616 | 2026-10-31 |
| snakem982/proxypool | ⭐2231 | 2026-10-31 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1857 | 2026-10-31 |
| crossxx-labs/free-proxy | ⭐1853 | 2026-10-31 |
| qusong0627/QuantMind | ⭐1843 | 2026-10-31 |
| surgioproject/surgio | ⭐1825 | 2026-10-31 |
| LancelotRar/best-cf-ips | ⭐1627 | 2026-10-31 |
| Leon406/SubCrawler | ⭐1576 | 2026-10-31 |
| jdnei/JiChangTuiJian | ⭐1410 | 2026-10-31 |
| NiREvil/vless | ⭐1361 | 2026-10-31 |
| shaoyouvip/free | ⭐1311 | 2026-10-31 |
| cfal/shoes | ⭐1284 | 2026-10-31 |
| nevertoday/xiaoxiaodong-vps | ⭐1110 | 2026-10-31 |
| Hidashimora/free-vpn-anti-rkn | ⭐1104 | 2026-10-31 |
| SubBoost/subboost | ⭐1004 | 2026-10-31 |
| bq2015/FreeProxies | ⭐918 | 2026-10-31 |
| deezertidal/freevpn | ⭐889 | 2026-10-31 |
| whoahaow/rjsxrd | ⭐873 | 2026-10-31 |
| ermaozi01/free_clash_vpn | ⭐821 | 2026-10-31 |
| 0xRadikal/Free-v2ray-Configs | ⭐780 | 2026-10-31 |
| YuanDevTeam/OneXray | ⭐749 | 2026-10-31 |
| dongchengjie/airport | ⭐743 | 2026-10-31 |
| ts-sf/fly | ⭐713 | 2026-10-31 |
| MatinGhanbari/v2ray-configs | ⭐693 | 2026-10-31 |
| raine/claude-code-proxy | ⭐685 | 2026-10-31 |
| gslege/CloudflareIP | ⭐678 | 2026-10-31 |
| hello-world-1989/cn-news | ⭐642 | 2026-10-31 |
| OpenNetCN/clash | ⭐642 | 2026-10-31 |
| SoliSpirit/v2ray-configs | ⭐635 | 2026-10-31 |
| kort0881/vpn-vless-configs-russia | ⭐622 | 2026-10-31 |
| jichangtuijian-cheap/cheap-airports | ⭐618 | 2026-10-31 |
| sunmiao4458/free-proxy-airport | ⭐556 | 2026-10-31 |
| CCSH/IPTV | ⭐535 | 2026-10-31 |
| kooker/FreeSubsCheck | ⭐449 | 2026-10-31 |
| itsyebekhe/PSG | ⭐445 | 2026-10-31 |
| sinavm/SVM | ⭐444 | 2026-10-31 |
| SubConv/SubConv | ⭐410 | 2026-10-31 |
| zhuhaiuk/free-nodes | ⭐394 | 2026-10-31 |
| cbusifabcap/daily_free_vpn | ⭐381 | 2026-10-31 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-10-31 |
| Delta-Kronecker/V2ray-Config | ⭐370 | 2026-10-31 |
| ovmvo/FreeSub | ⭐352 | 2026-10-31 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-10-31 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐322 | 2026-10-31 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-10-31 |
| WLget/V2Ray_configs_64 | ⭐314 | 2026-10-31 |
| clashv2ray-hub/clashfree | ⭐311 | 2026-10-31 |
| clashv2ray-hub/v2rayfree | ⭐302 | 2026-10-31 |
| crashgfw/free-airport-nodes | ⭐300 | 2026-10-31 |
| Surfboardv2ray/TGParse | ⭐294 | 2026-10-31 |
| wenxig/dongtai-sub | ⭐267 | 2026-10-31 |
| sakha1370/OpenRay | ⭐251 | 2026-10-31 |
| Wunderlandmedia/HotkeyClash | ⭐223 | 2026-10-31 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐211 | 2026-10-31 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-31 |
| tglaoshiji/nodeshare | ⭐198 | 2026-10-31 |
| xyfqzy/free-nodes | ⭐192 | 2026-10-31 |
| iboxz/free-v2ray-collector | ⭐191 | 2026-10-31 |
| mheidari98/.proxy | ⭐191 | 2026-10-31 |
| v2rayclashnode/v2rayclashnode.github.io | ⭐191 | 2026-10-31 |
| xOS/Config | ⭐183 | 2026-10-31 |
| HakurouKen/free-node | ⭐181 | 2026-10-31 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-10-31 |
| shabane/kamaji | ⭐173 | 2026-10-31 |
| liketolivefree/kobabi | ⭐170 | 2026-10-31 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐165 | 2026-10-31 |
| danmaifu/mianfeijiedian | ⭐158 | 2026-10-31 |

### 节点来源分布（去重后，前 20）

- `liketolivefree/kobabi/sub_all.txt`：3868 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：1642 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：378 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261031.txt`：271 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：251 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：191 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：153 个节点
- `Barabama/FreeNodes/nodes/freeclashnode.txt`：108 个节点
- `shabane/kamaji/hub/self/tested/merged.txt`：86 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：86 个节点
- `Barabama/FreeNodes/nodes/clashmeta.yaml`：78 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：68 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/ss.txt`：63 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：60 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：59 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：55 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-all.txt`：44 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：43 个节点
- `xrayfree/free-ssr-ss-v2ray-vpn-clash/README→www.xrayvip.com`：39 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：36 个节点

## 2026-10-30 22:24

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**23** 个
- 原始提取节点：**70149** 条
- 两级去重后（完整链接 + 服务器:端口）：**3439** 条（剔除重复 61214 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 3124、xray 3025、clash 3390、singbox 3238
- 耗时：1270 秒

### TCP 延迟分布

- 可达服务器：**3439/3439**（延迟中位数 214ms，最低 24ms）
- Cloudflare 前置节点：**1195** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 392 |
| 100-300ms | 2376 |
| 300-800ms | 524 |
| >800ms | 147 |
| 不可达（排在订阅末尾） | 0 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **49** 个仓库在 README 里给出订阅链接，从中提取 **70149** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| barry-far/V2ray-Config | 10 | 18483 |
| NiREvil/vless | 10 | 11199 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9496 |
| cbusifabcap/daily_free_vpn | 10 | 7767 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7203 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 10 | 5321 |
| whoahaow/rjsxrd | 10 | 3303 |
| DukeMehdi/FreeList-V2ray-Configs | 8 | 2898 |
| igareck/vpn-configs-for-russia | 10 | 1088 |
| iboxz/free-v2ray-collector | 5 | 746 |
| kooker/FreeSubsCheck | 5 | 675 |
| F0rc3Run/F0rc3Run | 7 | 620 |
| chengaopan/AutoMergePublicNodes | 2 | 440 |
| peasoft/NoMoreWalls | 1 | 438 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | 2 | 252 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4777 |
| vmess | 2955 |
| ss | 550 |
| trojan | 429 |
| hysteria2 | 211 |
| ssr | 9 |
| hysteria | 4 |

### 输出文件

- `v2ray_sub.txt`（3124 条，base64 订阅）
- `xray_sub.txt`（3025 条，base64 订阅）
- `clash_sub.yaml`（3390 个代理）
- `singbox_sub.json`（3238 个 outbound）
- `nodes_uris.txt`（3439 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| F0rc3Run/F0rc3Run | 92.5 | 100%（3/3） | 1242ms | 1205 |
| hello-world-1989/cn-news | 87.9 | 90%（9/10） | 856ms | 12 |
| snakem982/proxypool | 61.7 | 53%（8/15） | 943ms | 1408 |
| Pawdroid/Free-servers | 60.1 | 60%（9/15） | 1990ms | 90 |
| kooker/FreeSubsCheck | 29.1 | 6%（1/18） | 804ms | 2672 |
| NiREvil/vless | 29.0 | 11%（5/47） | 1402ms | 45732 |
| peasoft/NoMoreWalls | 26.7 | 8%（31/388） | 1488ms | 2589 |
| cbusifabcap/daily_free_vpn | 24.2 | 7%（14/205） | 1754ms | 17935 |
| whoahaow/rjsxrd | 24.2 | 7%（130/1817） | 1802ms | 6925 |
| sakha1370/OpenRay | 20.1 | 1%（20/1490） | 1797ms | 22457 |
| Delta-Kronecker/V2ray-Config | 19.6 | 0%（7/1531） | 1793ms | 16882 |
| SoliSpirit/v2ray-configs | 17.4 | 0%（27/5591） | 2155ms | 22017 |

- 本次采集优先级（质量从高到低）：F0rc3Run/F0rc3Run(可用率100%/质量92.5)、hello-world-1989/cn-news(可用率90%/质量87.9)、Pawdroid/Free-servers(可用率60%/质量60.1)、snakem982/proxypool(可用率53%/质量61.7)、NiREvil/vless(可用率11%/质量29.0)、peasoft/NoMoreWalls(可用率8%/质量26.7)、whoahaow/rjsxrd(可用率7%/质量24.2)、cbusifabcap/daily_free_vpn(可用率7%/质量24.2)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| mack-a/v2ray-agent | ⭐22243 | 2026-10-30 |
| Pawdroid/Free-servers | ⭐19705 | 2026-10-30 |
| DiningFactory/panda-vpn-pro | ⭐17135 | 2026-10-30 |
| free-nodes/clashfree | ⭐17119 | 2026-10-30 |
| free-nodes/v2rayfree | ⭐14658 | 2026-10-30 |
| ermaozi/get_subscribe | ⭐9410 | 2026-10-30 |
| igareck/vpn-configs-for-russia | ⭐9377 | 2026-10-30 |
| chengaopan/AutoMergePublicNodes | ⭐8298 | 2026-10-30 |
| free18/v2ray | ⭐5798 | 2026-10-30 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5684 | 2026-10-30 |
| Jsnzkpg/Jsnzkpg | ⭐4317 | 2026-10-30 |
| XTLS/Xray-install | ⭐3651 | 2026-10-30 |
| peasoft/NoMoreWalls | ⭐3582 | 2026-10-30 |
| Barabama/FreeNodes | ⭐3348 | 2026-10-30 |
| Alvin9999-newpac/fanqiang | ⭐3160 | 2026-10-30 |
| barry-far/V2ray-Config | ⭐2613 | 2026-10-30 |
| snakem982/proxypool | ⭐2229 | 2026-10-30 |
| KaWaIDeSuNe/dijiajichang | ⭐2227 | 2026-10-30 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1858 | 2026-10-30 |
| crossxx-labs/free-proxy | ⭐1849 | 2026-10-30 |
| qusong0627/QuantMind | ⭐1838 | 2026-10-30 |
| ZeroDeng01/sublinkPro | ⭐1733 | 2026-10-30 |
| LancelotRar/best-cf-ips | ⭐1625 | 2026-10-30 |
| Leon406/SubCrawler | ⭐1575 | 2026-10-30 |
| jdnei/JiChangTuiJian | ⭐1394 | 2026-10-30 |
| NiREvil/vless | ⭐1362 | 2026-10-30 |
| Abao130/jichangtizi-tuijian | ⭐1329 | 2026-10-30 |
| shaoyouvip/free | ⭐1307 | 2026-10-30 |
| cfal/shoes | ⭐1283 | 2026-10-30 |
| Hidashimora/free-vpn-anti-rkn | ⭐1102 | 2026-10-30 |
| nevertoday/xiaoxiaodong-vps | ⭐1022 | 2026-10-30 |
| bq2015/FreeProxies | ⭐917 | 2026-10-30 |
| deezertidal/freevpn | ⭐889 | 2026-10-30 |
| whoahaow/rjsxrd | ⭐873 | 2026-10-30 |
| 0xRadikal/Free-v2ray-Configs | ⭐779 | 2026-10-30 |
| dongchengjie/airport | ⭐741 | 2026-10-30 |
| ts-sf/fly | ⭐713 | 2026-10-30 |
| MatinGhanbari/v2ray-configs | ⭐692 | 2026-10-30 |
| Leadaxe/LxBox | ⭐679 | 2026-10-30 |
| gslege/CloudflareIP | ⭐677 | 2026-10-30 |
| hello-yunshu/Xray_bash_onekey | ⭐664 | 2026-10-30 |
| OpenNetCN/clash | ⭐641 | 2026-10-30 |
| hello-world-1989/cn-news | ⭐640 | 2026-10-30 |
| SoliSpirit/v2ray-configs | ⭐635 | 2026-10-30 |
| kort0881/vpn-vless-configs-russia | ⭐621 | 2026-10-30 |
| jichangtuijian-cheap/cheap-airports | ⭐618 | 2026-10-30 |
| sunmiao4458/free-proxy-airport | ⭐550 | 2026-10-30 |
| tolinkshare2/tolinkshare2.github.io | ⭐535 | 2026-10-30 |
| CCSH/IPTV | ⭐532 | 2026-10-30 |
| kooker/FreeSubsCheck | ⭐447 | 2026-10-30 |
| itsyebekhe/PSG | ⭐445 | 2026-10-30 |
| sinavm/SVM | ⭐440 | 2026-10-30 |
| zhuhaiuk/free-nodes | ⭐387 | 2026-10-30 |
| cbusifabcap/daily_free_vpn | ⭐378 | 2026-10-30 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-10-30 |
| Delta-Kronecker/V2ray-Config | ⭐369 | 2026-10-30 |
| ovmvo/FreeSub | ⭐350 | 2026-10-30 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-10-30 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐322 | 2026-10-30 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-10-30 |
| WLget/V2Ray_configs_64 | ⭐314 | 2026-10-30 |
| clashv2ray-hub/clashfree | ⭐311 | 2026-10-30 |
| clashv2ray-hub/v2rayfree | ⭐302 | 2026-10-30 |
| crashgfw/free-airport-nodes | ⭐299 | 2026-10-30 |
| Surfboardv2ray/TGParse | ⭐294 | 2026-10-30 |
| wenxig/dongtai-sub | ⭐267 | 2026-10-30 |
| shenaba/2s-ui | ⭐258 | 2026-10-30 |
| sakha1370/OpenRay | ⭐251 | 2026-10-30 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐210 | 2026-10-30 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-30 |
| tglaoshiji/nodeshare | ⭐198 | 2026-10-30 |
| iboxz/free-v2ray-collector | ⭐191 | 2026-10-30 |
| xyfqzy/free-nodes | ⭐191 | 2026-10-30 |
| mheidari98/.proxy | ⭐191 | 2026-10-30 |
| xOS/Config | ⭐183 | 2026-10-30 |
| HakurouKen/free-node | ⭐181 | 2026-10-30 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-10-30 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐164 | 2026-10-30 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-30 |
| flclashnode/flclashnode.github.io | ⭐161 | 2026-10-30 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：2105 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→raw.githubusercontent.com`：435 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：191 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：72 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：59 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：52 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→www.xrayvip.com`：52 个节点
- `iboxz/free-v2ray-collector/main/vless.txt`：43 个节点
- `peasoft/NoMoreWalls/list.txt`：41 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：41 个节点
- `barry-far/V2ray-Config/Sub3.txt`：38 个节点
- `cbusifabcap/daily_free_vpn/sub/URI.yml`：32 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：30 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：29 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：28 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：24 个节点
- `barry-far/V2ray-Config/All_Configs_base64_Sub.txt`：22 个节点
- `barry-far/V2ray-Config/Sub1.txt`：20 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：20 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/combine/clash.config.yaml`：18 个节点

## 2026-10-29 22:35

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**31** 个
- 原始提取节点：**117984** 条
- 两级去重后（完整链接 + 服务器:端口）：**3918** 条（剔除重复 107807 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 3438、xray 3347、clash 3870、singbox 3706
- 耗时：1947 秒

### TCP 延迟分布

- 可达服务器：**3918/3918**（延迟中位数 218ms，最低 23ms）
- Cloudflare 前置节点：**1374** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 166 |
| 100-300ms | 2876 |
| 300-800ms | 671 |
| >800ms | 205 |
| 不可达（排在订阅末尾） | 0 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **53** 个仓库在 README 里给出订阅链接，从中提取 **117984** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| sakha1370/OpenRay | 10 | 22457 |
| SoliSpirit/v2ray-configs | 5 | 22017 |
| barry-far/V2ray-Config | 10 | 18507 |
| NiREvil/vless | 10 | 11347 |
| cbusifabcap/daily_free_vpn | 10 | 10168 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8726 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7008 |
| Barabama/FreeNodes | 10 | 6538 |
| whoahaow/rjsxrd | 10 | 3622 |
| DukeMehdi/FreeList-V2ray-Configs | 8 | 2900 |
| iboxz/free-v2ray-collector | 5 | 750 |
| kooker/FreeSubsCheck | 5 | 655 |
| igareck/vpn-configs-for-russia | 10 | 620 |
| F0rc3Run/F0rc3Run | 7 | 585 |
| chengaopan/AutoMergePublicNodes | 2 | 417 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5903 |
| vmess | 2173 |
| ss | 1273 |
| trojan | 534 |
| hysteria2 | 278 |
| ssr | 12 |
| hysteria | 2 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（3438 条，base64 订阅）
- `xray_sub.txt`（3347 条，base64 订阅）
- `clash_sub.yaml`（3870 个代理）
- `singbox_sub.json`（3706 个 outbound）
- `nodes_uris.txt`（3912 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| Pawdroid/Free-servers | 92.7 | 100%（2/2） | 1210ms | 78 |
| peasoft/NoMoreWalls | 79.5 | 86%（6/7） | 1746ms | 2151 |
| igareck/vpn-configs-for-russia | 33.3 | 24%（5/21） | 2233ms | 4249 |
| kooker/FreeSubsCheck | 25.5 | 5%（9/194） | 1282ms | 1997 |
| NiREvil/vless | 21.0 | 4%（297/7513） | 1965ms | 34533 |
| Delta-Kronecker/V2ray-Config | 19.6 | 0%（7/1531） | 1793ms | 16882 |
| PuddinCat/BestClash | 0.5 | 1%（3/449） | 6091ms | 3923 |
| liketolivefree/kobabi | 0.1 | 0%（1/1575） | 12758ms | 23038 |
| barry-far/V2ray-Config | 0.0 | 0%（0/3） | -ms | 70175 |
| Epodonios/v2ray-configs | 0.0 | 0%（0/9） | -ms | 68245 |
| 0xRadikal/Free-v2ray-Configs | 0.0 | 0%（0/2） | -ms | 59825 |
| Barabama/FreeNodes | 0.0 | 0%（0/12） | -ms | 25704 |

- 本次采集优先级（质量从高到低）：Pawdroid/Free-servers(可用率100%/质量92.7)、peasoft/NoMoreWalls(可用率86%/质量79.5)、igareck/vpn-configs-for-russia(可用率24%/质量33.3)、kooker/FreeSubsCheck(可用率5%/质量25.5)、NiREvil/vless(可用率4%/质量21.0)、PuddinCat/BestClash(可用率1%/质量0.5)、Delta-Kronecker/V2ray-Config(可用率0%/质量19.6)、liketolivefree/kobabi(可用率0%/质量0.1)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| mack-a/v2ray-agent | ⭐22233 | 2026-10-29 |
| Pawdroid/Free-servers | ⭐19689 | 2026-10-29 |
| free-nodes/clashfree | ⭐17101 | 2026-10-29 |
| DiningFactory/panda-vpn-pro | ⭐17063 | 2026-10-29 |
| free-nodes/v2rayfree | ⭐14627 | 2026-10-29 |
| ermaozi/get_subscribe | ⭐9408 | 2026-10-29 |
| igareck/vpn-configs-for-russia | ⭐9364 | 2026-10-29 |
| chengaopan/AutoMergePublicNodes | ⭐8293 | 2026-10-29 |
| yonggekkk/argosbx | ⭐5969 | 2026-10-29 |
| free18/v2ray | ⭐5786 | 2026-10-29 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5678 | 2026-10-29 |
| Jsnzkpg/Jsnzkpg | ⭐4313 | 2026-10-29 |
| peasoft/NoMoreWalls | ⭐3578 | 2026-10-29 |
| Barabama/FreeNodes | ⭐3340 | 2026-10-29 |
| Alvin9999-newpac/fanqiang | ⭐3151 | 2026-10-29 |
| barry-far/V2ray-Config | ⭐2608 | 2026-10-29 |
| snakem982/proxypool | ⭐2225 | 2026-10-29 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1859 | 2026-10-29 |
| crossxx-labs/free-proxy | ⭐1848 | 2026-10-29 |
| qusong0627/QuantMind | ⭐1830 | 2026-10-29 |
| LancelotRar/best-cf-ips | ⭐1621 | 2026-10-29 |
| Leon406/SubCrawler | ⭐1573 | 2026-10-29 |
| everett7623/airport-recommendations-2026 | ⭐1460 | 2026-10-29 |
| jdnei/JiChangTuiJian | ⭐1368 | 2026-10-29 |
| NiREvil/vless | ⭐1361 | 2026-10-29 |
| shaoyouvip/free | ⭐1304 | 2026-10-29 |
| cfal/shoes | ⭐1280 | 2026-10-29 |
| Hidashimora/free-vpn-anti-rkn | ⭐1097 | 2026-10-29 |
| SubBoost/subboost | ⭐995 | 2026-10-29 |
| nevertoday/xiaoxiaodong-vps | ⭐985 | 2026-10-29 |
| bq2015/FreeProxies | ⭐915 | 2026-10-29 |
| deezertidal/freevpn | ⭐888 | 2026-10-29 |
| whoahaow/rjsxrd | ⭐872 | 2026-10-29 |
| ermaozi01/free_clash_vpn | ⭐821 | 2026-10-29 |
| 0xRadikal/Free-v2ray-Configs | ⭐778 | 2026-10-29 |
| dongchengjie/airport | ⭐739 | 2026-10-29 |
| sylearn/AIUsage | ⭐730 | 2026-10-29 |
| ts-sf/fly | ⭐713 | 2026-10-29 |
| MatinGhanbari/v2ray-configs | ⭐691 | 2026-10-29 |
| gslege/CloudflareIP | ⭐675 | 2026-10-29 |
| Leadaxe/LxBox | ⭐673 | 2026-10-29 |
| hello-yunshu/Xray_bash_onekey | ⭐663 | 2026-10-29 |
| OpenNetCN/clash | ⭐641 | 2026-10-29 |
| hello-world-1989/cn-news | ⭐638 | 2026-10-29 |
| SoliSpirit/v2ray-configs | ⭐635 | 2026-10-29 |
| kort0881/vpn-vless-configs-russia | ⭐618 | 2026-10-29 |
| jichangtuijian-cheap/cheap-airports | ⭐616 | 2026-10-29 |
| tolinkshare2/tolinkshare2.github.io | ⭐534 | 2026-10-29 |
| CCSH/IPTV | ⭐530 | 2026-10-29 |
| sunmiao4458/free-proxy-airport | ⭐525 | 2026-10-29 |
| kooker/FreeSubsCheck | ⭐447 | 2026-10-29 |
| itsyebekhe/PSG | ⭐445 | 2026-10-29 |
| sinavm/SVM | ⭐432 | 2026-10-29 |
| IvanSolis1989/Smart-Config-Kit | ⭐429 | 2026-10-29 |
| zhuhaiuk/free-nodes | ⭐384 | 2026-10-29 |
| cbusifabcap/daily_free_vpn | ⭐376 | 2026-10-29 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-10-29 |
| Delta-Kronecker/V2ray-Config | ⭐369 | 2026-10-29 |
| ovmvo/FreeSub | ⭐349 | 2026-10-29 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-10-29 |
| MhdiTaheri/V2rayCollector | ⭐321 | 2026-10-29 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐321 | 2026-10-29 |
| WLget/V2Ray_configs_64 | ⭐315 | 2026-10-29 |
| clashv2ray-hub/clashfree | ⭐310 | 2026-10-29 |
| clashv2ray-hub/v2rayfree | ⭐300 | 2026-10-29 |
| crashgfw/free-airport-nodes | ⭐298 | 2026-10-29 |
| Surfboardv2ray/TGParse | ⭐294 | 2026-10-29 |
| wenxig/dongtai-sub | ⭐266 | 2026-10-29 |
| sakha1370/OpenRay | ⭐250 | 2026-10-29 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐209 | 2026-10-29 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-29 |
| tglaoshiji/nodeshare | ⭐198 | 2026-10-29 |
| iboxz/free-v2ray-collector | ⭐191 | 2026-10-29 |
| mheidari98/.proxy | ⭐191 | 2026-10-29 |
| xyfqzy/free-nodes | ⭐190 | 2026-10-29 |
| xOS/Config | ⭐183 | 2026-10-29 |
| HakurouKen/free-node | ⭐180 | 2026-10-29 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-10-29 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐164 | 2026-10-29 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-29 |

### 节点来源分布（去重后，前 20）

- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：877 个节点
- `SoliSpirit/v2ray-configs/Protocols/vmess.txt`：678 个节点
- `Barabama/FreeNodes/README→gh-proxy.com`：427 个节点
- `sakha1370/OpenRay/output/converted/all_valid_proxies_singbox_config.json`：334 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：218 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：190 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：136 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：116 个节点
- `peasoft/NoMoreWalls/list.txt`：114 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：90 个节点
- `cbusifabcap/daily_free_vpn/Z.txt`：84 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：66 个节点
- `sakha1370/OpenRay/output/site_access/aistudio_iran_verified.txt`：64 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：62 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-1.txt`：59 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：59 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-all.txt`：50 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：45 个节点
- `iboxz/free-v2ray-collector/main/vless.txt`：33 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：26 个节点

## 2026-10-28 22:46

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**10** 个
- 原始提取节点：**29937** 条
- 两级去重后（完整链接 + 服务器:端口）：**2744** 条（剔除重复 23006 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 2531、xray 2193、clash 2704、singbox 2611
- 耗时：2596 秒

### TCP 延迟分布

- 可达服务器：**2744/2744**（延迟中位数 232ms，最低 27ms）
- Cloudflare 前置节点：**822** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 226 |
| 100-300ms | 1715 |
| 300-800ms | 589 |
| >800ms | 214 |
| 不可达（排在订阅末尾） | 0 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **38** 个仓库在 README 里给出订阅链接，从中提取 **29937** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| NiREvil/vless | 10 | 11541 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8098 |
| Delta-Kronecker/V2ray-Config | 10 | 7321 |
| Danialsamadi/v2go | 10 | 1674 |
| kooker/FreeSubsCheck | 5 | 661 |
| peasoft/NoMoreWalls | 1 | 417 |
| snakem982/proxypool | 3 | 172 |
| ermaozi01/free_clash_vpn | 2 | 38 |
| Pawdroid/Free-servers | 3 | 13 |
| shaoyouvip/free | 4 | 2 |
| crashgfw/free-airport-nodes | 10 | 0 |
| ermaozi/get_subscribe | 1 | 0 |
| free18/v2ray | 2 | 0 |
| crossxx-labs/free-proxy | 1 | 0 |
| Leon406/SubCrawler | 5 | 0 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 3775 |
| vmess | 2066 |
| trojan | 670 |
| ss | 334 |
| hysteria2 | 84 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（2531 条，base64 订阅）
- `xray_sub.txt`（2193 条，base64 订阅）
- `clash_sub.yaml`（2704 个代理）
- `singbox_sub.json`（2611 个 outbound）
- `nodes_uris.txt`（2744 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| Delta-Kronecker/V2ray-Config | 96.4 | 100%（1/1） | 604ms | 16882 |
| Pawdroid/Free-servers | 92.7 | 100%（2/2） | 1210ms | 71 |
| NiREvil/vless | 85.3 | 100%（1/1） | 2456ms | 23186 |
| kooker/FreeSubsCheck | 79.5 | 100%（5/5） | 3413ms | 1342 |
| 0xRadikal/Free-v2ray-Configs | 75.0 | 71%（5/7） | 837ms | 51099 |
| Danialsamadi/v2go | 71.1 | 67%（2/3） | 935ms | 3268 |
| ermaozi01/free_clash_vpn | 70.0 | 100%（2/2） | 11234ms | 76 |
| peasoft/NoMoreWalls | 55.9 | 57%（4/7） | 2339ms | 1736 |
| snakem982/proxypool | 42.0 | 60%（3/5） | 6201ms | 1042 |
| igareck/vpn-configs-for-russia | 33.3 | 24%（5/21） | 2233ms | 3629 |
| nyeinkokoaung404/V2ray-Configs | 4.0 | 1%（5/796） | 4408ms | 13451 |
| barry-far/V2ray-Config | 2.2 | 3%（4/129） | 5760ms | 51668 |

- 本次采集优先级（质量从高到低）：NiREvil/vless(可用率100%/质量85.3)、Delta-Kronecker/V2ray-Config(可用率100%/质量96.4)、kooker/FreeSubsCheck(可用率100%/质量79.5)、Pawdroid/Free-servers(可用率100%/质量92.7)、ermaozi01/free_clash_vpn(可用率100%/质量70.0)、0xRadikal/Free-v2ray-Configs(可用率71%/质量75.0)、Danialsamadi/v2go(可用率67%/质量71.1)、snakem982/proxypool(可用率60%/质量42.0)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| Pawdroid/Free-servers | ⭐19677 | 2026-10-28 |
| free-nodes/clashfree | ⭐17085 | 2026-10-28 |
| free-nodes/v2rayfree | ⭐14597 | 2026-10-28 |
| ermaozi/get_subscribe | ⭐9401 | 2026-10-28 |
| igareck/vpn-configs-for-russia | ⭐9348 | 2026-10-28 |
| chengaopan/AutoMergePublicNodes | ⭐8291 | 2026-10-28 |
| free18/v2ray | ⭐5784 | 2026-10-28 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5671 | 2026-10-28 |
| Jsnzkpg/Jsnzkpg | ⭐4305 | 2026-10-28 |
| peasoft/NoMoreWalls | ⭐3573 | 2026-10-28 |
| Barabama/FreeNodes | ⭐3330 | 2026-10-28 |
| Alvin9999-newpac/fanqiang | ⭐3143 | 2026-10-28 |
| barry-far/V2ray-Config | ⭐2600 | 2026-10-28 |
| snakem982/proxypool | ⭐2223 | 2026-10-28 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1856 | 2026-10-28 |
| crossxx-labs/free-proxy | ⭐1843 | 2026-10-28 |
| LancelotRar/best-cf-ips | ⭐1613 | 2026-10-28 |
| Leon406/SubCrawler | ⭐1572 | 2026-10-28 |
| NiREvil/vless | ⭐1361 | 2026-10-28 |
| jdnei/JiChangTuiJian | ⭐1339 | 2026-10-28 |
| shaoyouvip/free | ⭐1299 | 2026-10-28 |
| cfal/shoes | ⭐1278 | 2026-10-28 |
| myikuns/jichangtz-tuijian | ⭐1083 | 2026-10-28 |
| Hidashimora/free-vpn-anti-rkn | ⭐1074 | 2026-10-28 |
| nevertoday/xiaoxiaodong-vps | ⭐960 | 2026-10-28 |
| bq2015/FreeProxies | ⭐914 | 2026-10-28 |
| deezertidal/freevpn | ⭐888 | 2026-10-28 |
| whoahaow/rjsxrd | ⭐868 | 2026-10-28 |
| ermaozi01/free_clash_vpn | ⭐819 | 2026-10-28 |
| 0xRadikal/Free-v2ray-Configs | ⭐775 | 2026-10-28 |
| dongchengjie/airport | ⭐739 | 2026-10-28 |
| ts-sf/fly | ⭐713 | 2026-10-28 |
| MatinGhanbari/v2ray-configs | ⭐691 | 2026-10-28 |
| gslege/CloudflareIP | ⭐674 | 2026-10-28 |
| hello-yunshu/Xray_bash_onekey | ⭐663 | 2026-10-28 |
| OpenNetCN/clash | ⭐640 | 2026-10-28 |
| hello-world-1989/cn-news | ⭐636 | 2026-10-28 |
| SoliSpirit/v2ray-configs | ⭐635 | 2026-10-28 |
| kort0881/vpn-vless-configs-russia | ⭐617 | 2026-10-28 |
| jichangtuijian-cheap/cheap-airports | ⭐616 | 2026-10-28 |
| tolinkshare2/tolinkshare2.github.io | ⭐532 | 2026-10-28 |
| CCSH/IPTV | ⭐528 | 2026-10-28 |
| sunmiao4458/free-proxy-airport | ⭐524 | 2026-10-28 |
| itsyebekhe/PSG | ⭐445 | 2026-10-28 |
| kooker/FreeSubsCheck | ⭐442 | 2026-10-28 |
| sinavm/SVM | ⭐432 | 2026-10-28 |
| IvanSolis1989/Smart-Config-Kit | ⭐427 | 2026-10-28 |
| zhuhaiuk/free-nodes | ⭐381 | 2026-10-28 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-10-28 |
| cbusifabcap/daily_free_vpn | ⭐373 | 2026-10-28 |
| Delta-Kronecker/V2ray-Config | ⭐369 | 2026-10-28 |
| ovmvo/FreeSub | ⭐348 | 2026-10-28 |
| MhdiTaheri/V2rayCollector | ⭐321 | 2026-10-28 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-10-28 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐321 | 2026-10-28 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-10-28 |
| clashv2ray-hub/clashfree | ⭐310 | 2026-10-28 |
| clashv2ray-hub/v2rayfree | ⭐300 | 2026-10-28 |
| crashgfw/free-airport-nodes | ⭐298 | 2026-10-28 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-10-28 |
| ghuntley/underclass | ⭐286 | 2026-10-28 |
| wenxig/dongtai-sub | ⭐265 | 2026-10-28 |
| sakha1370/OpenRay | ⭐249 | 2026-10-28 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐209 | 2026-10-28 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-28 |
| tglaoshiji/nodeshare | ⭐198 | 2026-10-28 |
| mheidari98/.proxy | ⭐191 | 2026-10-28 |
| iboxz/free-v2ray-collector | ⭐189 | 2026-10-28 |
| xyfqzy/free-nodes | ⭐189 | 2026-10-28 |
| xOS/Config | ⭐183 | 2026-10-28 |
| HakurouKen/free-node | ⭐180 | 2026-10-28 |
| sinavm/sing-box | ⭐178 | 2026-10-28 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-10-28 |
| shabane/kamaji | ⭐173 | 2026-10-28 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐164 | 2026-10-28 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-28 |
| 029danio/jichangfree | ⭐159 | 2026-10-28 |
| thsrite/configflow | ⭐155 | 2026-10-28 |
| Danialsamadi/v2go | ⭐155 | 2026-10-28 |
| licheng527/Free-servers | ⭐153 | 2026-10-28 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：2214 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：391 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/ss.txt`：70 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：56 个节点
- `Danialsamadi/v2go/AllConfigsSub.txt`：5 个节点
- `kooker/FreeSubsCheck/byxiaoxi.txt`：5 个节点
- `ermaozi01/free_clash_vpn/subscribe/v2ray.txt`：3 个节点

## 2026-10-27 22:36

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**22** 个
- 原始提取节点：**91302** 条
- 两级去重后（完整链接 + 服务器:端口）：**16629** 条（剔除重复 74673 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 11012、xray 14931、clash 16432、singbox 15574
- 耗时：2041 秒

### TCP 延迟分布

- 可达服务器：**6859/16629**（延迟中位数 234ms，最低 23ms）
- Cloudflare 前置节点：**2616** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 510 |
| 100-300ms | 4402 |
| 300-800ms | 1258 |
| >800ms | 689 |
| 不可达（排在订阅末尾） | 9770 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **57** 个仓库在 README 里给出订阅链接，从中提取 **91302** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| liketolivefree/kobabi | 10 | 23038 |
| Epodonios/v2ray-configs | 10 | 22480 |
| barry-far/V2ray-Config | 10 | 16965 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9983 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6904 |
| Barabama/FreeNodes | 10 | 5274 |
| Danialsamadi/v2go | 10 | 1594 |
| Hidashimora/free-vpn-anti-rkn | 10 | 1093 |
| iboxz/free-v2ray-collector | 5 | 746 |
| kooker/FreeSubsCheck | 5 | 681 |
| igareck/vpn-configs-for-russia | 10 | 443 |
| peasoft/NoMoreWalls | 1 | 433 |
| chengaopan/AutoMergePublicNodes | 2 | 433 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 10 | 391 |
| crashgfw/free-airport-nodes | 10 | 270 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 13336 |
| vmess | 2085 |
| ss | 613 |
| trojan | 402 |
| hysteria2 | 188 |
| ssr | 2 |
| tuic | 2 |
| hysteria | 1 |

### 输出文件

- `v2ray_sub.txt`（11012 条，base64 订阅）
- `xray_sub.txt`（14931 条，base64 订阅）
- `clash_sub.yaml`（16432 个代理）
- `singbox_sub.json`（15574 个 outbound）
- `nodes_uris.txt`（16620 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| peasoft/NoMoreWalls | 48.7 | 38%（30/80） | 1265ms | 1319 |
| snakem982/proxypool | 47.0 | 39%（41/106） | 1685ms | 870 |
| Pawdroid/Free-servers | 46.0 | 39%（14/36） | 1867ms | 58 |
| zhuhaiuk/free-nodes | 34.7 | 16%（3/19） | 1053ms | 55 |
| igareck/vpn-configs-for-russia | 29.6 | 14%（9/65） | 1680ms | 3629 |
| 0xRadikal/Free-v2ray-Configs | 29.0 | 11%（48/420） | 1499ms | 43001 |
| Epodonios/v2ray-configs | 26.4 | 3%（2/78） | 897ms | 68245 |
| Delta-Kronecker/V2ray-Config | 26.1 | 1%（9/908） | 773ms | 9561 |
| Barabama/FreeNodes | 24.9 | 4%（23/534） | 1359ms | 19166 |
| barry-far/V2ray-Config | 23.4 | 4%（17/489） | 1516ms | 51668 |
| NiREvil/vless | 20.8 | 1%（9/894） | 1645ms | 11645 |
| PuddinCat/BestClash | 0.5 | 1%（3/449） | 6091ms | 3923 |

- 本次采集优先级（质量从高到低）：Pawdroid/Free-servers(可用率39%/质量46.0)、snakem982/proxypool(可用率39%/质量47.0)、peasoft/NoMoreWalls(可用率38%/质量48.7)、zhuhaiuk/free-nodes(可用率16%/质量34.7)、igareck/vpn-configs-for-russia(可用率14%/质量29.6)、0xRadikal/Free-v2ray-Configs(可用率11%/质量29.0)、Barabama/FreeNodes(可用率4%/质量24.9)、barry-far/V2ray-Config(可用率4%/质量23.4)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| mack-a/v2ray-agent | ⭐22199 | 2026-10-27 |
| Pawdroid/Free-servers | ⭐19661 | 2026-10-27 |
| free-nodes/clashfree | ⭐17068 | 2026-10-27 |
| free-nodes/v2rayfree | ⭐14573 | 2026-10-27 |
| ermaozi/get_subscribe | ⭐9396 | 2026-10-27 |
| igareck/vpn-configs-for-russia | ⭐9344 | 2026-10-27 |
| chengaopan/AutoMergePublicNodes | ⭐8283 | 2026-10-27 |
| free18/v2ray | ⭐5774 | 2026-10-27 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5667 | 2026-10-27 |
| peasoft/NoMoreWalls | ⭐3571 | 2026-10-27 |
| Barabama/FreeNodes | ⭐3326 | 2026-10-27 |
| Epodonios/v2ray-configs | ⭐3313 | 2026-10-27 |
| Alvin9999-newpac/fanqiang | ⭐3135 | 2026-10-27 |
| barry-far/V2ray-Config | ⭐2595 | 2026-10-27 |
| snakem982/proxypool | ⭐2219 | 2026-10-27 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1856 | 2026-10-27 |
| crossxx-labs/free-proxy | ⭐1842 | 2026-10-27 |
| LancelotRar/best-cf-ips | ⭐1612 | 2026-10-27 |
| Leon406/SubCrawler | ⭐1572 | 2026-10-27 |
| NiREvil/vless | ⭐1359 | 2026-10-27 |
| jdnei/JiChangTuiJian | ⭐1313 | 2026-10-27 |
| shaoyouvip/free | ⭐1294 | 2026-10-27 |
| cfal/shoes | ⭐1274 | 2026-10-27 |
| Hidashimora/free-vpn-anti-rkn | ⭐1071 | 2026-10-27 |
| nevertoday/xiaoxiaodong-vps | ⭐938 | 2026-10-27 |
| bq2015/FreeProxies | ⭐912 | 2026-10-27 |
| deezertidal/freevpn | ⭐888 | 2026-10-27 |
| whoahaow/rjsxrd | ⭐867 | 2026-10-27 |
| ermaozi01/free_clash_vpn | ⭐817 | 2026-10-27 |
| 0xRadikal/Free-v2ray-Configs | ⭐771 | 2026-10-27 |
| dongchengjie/airport | ⭐737 | 2026-10-27 |
| YuanDevTeam/OneXray | ⭐726 | 2026-10-27 |
| ts-sf/fly | ⭐713 | 2026-10-27 |
| MatinGhanbari/v2ray-configs | ⭐689 | 2026-10-27 |
| gslege/CloudflareIP | ⭐674 | 2026-10-27 |
| Leadaxe/LxBox | ⭐663 | 2026-10-27 |
| OpenNetCN/clash | ⭐637 | 2026-10-27 |
| SoliSpirit/v2ray-configs | ⭐635 | 2026-10-27 |
| hello-world-1989/cn-news | ⭐634 | 2026-10-27 |
| kort0881/vpn-vless-configs-russia | ⭐617 | 2026-10-27 |
| jichangtuijian-cheap/cheap-airports | ⭐613 | 2026-10-27 |
| tolinkshare2/tolinkshare2.github.io | ⭐528 | 2026-10-27 |
| CCSH/IPTV | ⭐525 | 2026-10-27 |
| sunmiao4458/free-proxy-airport | ⭐524 | 2026-10-27 |
| itsyebekhe/PSG | ⭐445 | 2026-10-27 |
| kooker/FreeSubsCheck | ⭐441 | 2026-10-27 |
| sinavm/SVM | ⭐432 | 2026-10-27 |
| IvanSolis1989/Smart-Config-Kit | ⭐425 | 2026-10-27 |
| Epodonios/bulk-xray-v2ray-vless-vmess-...-configs | ⭐381 | 2026-10-27 |
| zhuhaiuk/free-nodes | ⭐379 | 2026-10-27 |
| ShatakVPN/ConfigForge-V2Ray | ⭐375 | 2026-10-27 |
| Delta-Kronecker/V2ray-Config | ⭐369 | 2026-10-27 |
| cbusifabcap/daily_free_vpn | ⭐367 | 2026-10-27 |
| ovmvo/FreeSub | ⭐347 | 2026-10-27 |
| MhdiTaheri/V2rayCollector | ⭐321 | 2026-10-27 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-10-27 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐321 | 2026-10-27 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-10-27 |
| clashv2ray-hub/clashfree | ⭐310 | 2026-10-27 |
| clashv2ray-hub/v2rayfree | ⭐300 | 2026-10-27 |
| crashgfw/free-airport-nodes | ⭐296 | 2026-10-27 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-10-27 |
| wenxig/dongtai-sub | ⭐265 | 2026-10-27 |
| 5VNetwork/VX | ⭐255 | 2026-10-27 |
| sakha1370/OpenRay | ⭐249 | 2026-10-27 |
| shenaba/2s-ui | ⭐248 | 2026-10-27 |
| yanisplugg/yptun | ⭐226 | 2026-10-27 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐209 | 2026-10-27 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-27 |
| tglaoshiji/nodeshare | ⭐198 | 2026-10-27 |
| mheidari98/.proxy | ⭐190 | 2026-10-27 |
| iboxz/free-v2ray-collector | ⭐188 | 2026-10-27 |
| xOS/Config | ⭐183 | 2026-10-27 |
| HakurouKen/free-node | ⭐180 | 2026-10-27 |
| V2RayRoot/V2RayConfig | ⭐174 | 2026-10-27 |
| liketolivefree/kobabi | ⭐169 | 2026-10-27 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-27 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐163 | 2026-10-27 |
| Danialsamadi/v2go | ⭐155 | 2026-10-27 |
| thsrite/configflow | ⭐155 | 2026-10-27 |

### 节点来源分布（去重后，前 20）

- `liketolivefree/kobabi/sub_all.txt`：9379 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：1765 个节点
- `Barabama/FreeNodes/README→gh-proxy.com`：1052 个节点
- `barry-far/V2ray-Config/All_Configs_base64_Sub.txt`：849 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：395 个节点
- `peasoft/NoMoreWalls/list.txt`：392 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：372 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/2.1.txt`：271 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：269 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/1.1.txt`：247 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/3.1.txt`：229 个节点
- `liketolivefree/kobabi/sub.txt`：192 个节点
- `liketolivefree/kobabi/singbox.json`：188 个节点
- `nyeinkokoaung404/V2ray-Configs/configs/proxy_configs.txt`：144 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/4.1.txt`：124 个节点
- `barry-far/V2ray-Config/Sub1.txt`：109 个节点
- `Epodonios/v2ray-configs/All_Configs_base64_Sub.txt`：78 个节点
- `barry-far/V2ray-Config/Sub2.txt`：63 个节点
- `iboxz/free-v2ray-collector/main/mix.txt`：61 个节点
- `barry-far/V2ray-Config/Sub3.txt`：57 个节点

## 2026-10-26 22:38

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**17** 个
- 原始提取节点：**66944** 条
- 两级去重后（完整链接 + 服务器:端口）：**7908** 条（剔除重复 59036 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 7603、xray 6484、clash 7757、singbox 7546
- 耗时：2132 秒

### TCP 延迟分布

- 可达服务器：**2842/7908**（延迟中位数 209ms，最低 24ms）
- Cloudflare 前置节点：**1107** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 301 |
| 100-300ms | 1948 |
| 300-800ms | 454 |
| >800ms | 139 |
| 不可达（排在订阅末尾） | 5066 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **52** 个仓库在 README 里给出订阅链接，从中提取 **66944** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| Epodonios/v2ray-configs | 7 | 23108 |
| barry-far/V2ray-Config | 10 | 17306 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9934 |
| Barabama/FreeNodes | 10 | 6897 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6547 |
| iboxz/free-v2ray-collector | 5 | 734 |
| igareck/vpn-configs-for-russia | 10 | 685 |
| peasoft/NoMoreWalls | 1 | 449 |
| chengaopan/AutoMergePublicNodes | 2 | 449 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 10 | 279 |
| crashgfw/free-airport-nodes | 10 | 270 |
| snakem982/proxypool | 3 | 176 |
| free-nodes/clashfree | 1 | 81 |
| Pawdroid/Free-servers | 3 | 10 |
| shaoyouvip/free | 4 | 10 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4781 |
| vmess | 2036 |
| ss | 569 |
| trojan | 331 |
| hysteria2 | 185 |
| hysteria | 2 |
| ssr | 2 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（7603 条，base64 订阅）
- `xray_sub.txt`（6484 条，base64 订阅）
- `clash_sub.yaml`（7757 个代理）
- `singbox_sub.json`（7546 个 outbound）
- `nodes_uris.txt`（7897 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| peasoft/NoMoreWalls | 48.7 | 38%（30/80） | 1265ms | 886 |
| snakem982/proxypool | 47.0 | 39%（41/106） | 1685ms | 694 |
| Pawdroid/Free-servers | 46.0 | 39%（14/36） | 1867ms | 47 |
| zhuhaiuk/free-nodes | 34.7 | 16%（3/19） | 1053ms | 40 |
| igareck/vpn-configs-for-russia | 29.6 | 14%（9/65） | 1680ms | 3186 |
| 0xRadikal/Free-v2ray-Configs | 29.0 | 11%（48/420） | 1499ms | 33018 |
| Epodonios/v2ray-configs | 26.4 | 3%（2/78） | 897ms | 45765 |
| Delta-Kronecker/V2ray-Config | 26.1 | 1%（9/908） | 773ms | 9561 |
| Barabama/FreeNodes | 24.9 | 4%（23/534） | 1359ms | 13892 |
| barry-far/V2ray-Config | 23.4 | 4%（17/489） | 1516ms | 34703 |
| NiREvil/vless | 20.8 | 1%（9/894） | 1645ms | 11645 |
| PuddinCat/BestClash | 0.5 | 1%（3/449） | 6091ms | 3923 |

- 本次采集优先级（质量从高到低）：Pawdroid/Free-servers(可用率39%/质量46.0)、snakem982/proxypool(可用率39%/质量47.0)、peasoft/NoMoreWalls(可用率38%/质量48.7)、zhuhaiuk/free-nodes(可用率16%/质量34.7)、igareck/vpn-configs-for-russia(可用率14%/质量29.6)、0xRadikal/Free-v2ray-Configs(可用率11%/质量29.0)、Barabama/FreeNodes(可用率4%/质量24.9)、barry-far/V2ray-Config(可用率4%/质量23.4)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| mack-a/v2ray-agent | ⭐22178 | 2026-10-26 |
| yanue/V2rayU | ⭐20179 | 2026-10-26 |
| Pawdroid/Free-servers | ⭐19648 | 2026-10-26 |
| free-nodes/clashfree | ⭐17050 | 2026-10-26 |
| free-nodes/v2rayfree | ⭐14549 | 2026-10-26 |
| ermaozi/get_subscribe | ⭐9393 | 2026-10-26 |
| igareck/vpn-configs-for-russia | ⭐9336 | 2026-10-26 |
| chengaopan/AutoMergePublicNodes | ⭐8277 | 2026-10-26 |
| fscarmen/sing-box | ⭐5886 | 2026-10-26 |
| free18/v2ray | ⭐5761 | 2026-10-26 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5663 | 2026-10-26 |
| anaer/Sub | ⭐3673 | 2026-10-26 |
| peasoft/NoMoreWalls | ⭐3566 | 2026-10-26 |
| Barabama/FreeNodes | ⭐3323 | 2026-10-26 |
| Epodonios/v2ray-configs | ⭐3312 | 2026-10-26 |
| Alvin9999-newpac/fanqiang | ⭐3123 | 2026-10-26 |
| barry-far/V2ray-Config | ⭐2587 | 2026-10-26 |
| snakem982/proxypool | ⭐2218 | 2026-10-26 |
| Semporia/Clash | ⭐1866 | 2026-10-26 |
| crossxx-labs/free-proxy | ⭐1841 | 2026-10-26 |
| ZeroDeng01/sublinkPro | ⭐1718 | 2026-10-26 |
| LancelotRar/best-cf-ips | ⭐1607 | 2026-10-26 |
| Leon406/SubCrawler | ⭐1572 | 2026-10-26 |
| everett7623/airport-recommendations-2026 | ⭐1443 | 2026-10-26 |
| NiREvil/vless | ⭐1356 | 2026-10-26 |
| jdnei/JiChangTuiJian | ⭐1293 | 2026-10-26 |
| shaoyouvip/free | ⭐1291 | 2026-10-26 |
| cfal/shoes | ⭐1272 | 2026-10-26 |
| Hidashimora/free-vpn-anti-rkn | ⭐1065 | 2026-10-26 |
| bq2015/FreeProxies | ⭐907 | 2026-10-26 |
| deezertidal/freevpn | ⭐887 | 2026-10-26 |
| whoahaow/rjsxrd | ⭐867 | 2026-10-26 |
| ermaozi01/free_clash_vpn | ⭐817 | 2026-10-26 |
| 0xRadikal/Free-v2ray-Configs | ⭐770 | 2026-10-26 |
| dongchengjie/airport | ⭐736 | 2026-10-26 |
| sylearn/AIUsage | ⭐731 | 2026-10-26 |
| YuanDevTeam/OneXray | ⭐720 | 2026-10-26 |
| ts-sf/fly | ⭐712 | 2026-10-26 |
| MatinGhanbari/v2ray-configs | ⭐689 | 2026-10-26 |
| gslege/CloudflareIP | ⭐675 | 2026-10-26 |
| Leadaxe/LxBox | ⭐661 | 2026-10-26 |
| OpenNetCN/clash | ⭐635 | 2026-10-26 |
| SoliSpirit/v2ray-configs | ⭐634 | 2026-10-26 |
| hello-world-1989/cn-news | ⭐632 | 2026-10-26 |
| kort0881/vpn-vless-configs-russia | ⭐616 | 2026-10-26 |
| jichangtuijian-cheap/cheap-airports | ⭐612 | 2026-10-26 |
| tolinkshare2/tolinkshare2.github.io | ⭐528 | 2026-10-26 |
| CCSH/IPTV | ⭐521 | 2026-10-26 |
| sunmiao4458/free-proxy-airport | ⭐519 | 2026-10-26 |
| itsyebekhe/PSG | ⭐446 | 2026-10-26 |
| kooker/FreeSubsCheck | ⭐440 | 2026-10-26 |
| sinavm/SVM | ⭐432 | 2026-10-26 |
| Epodonios/bulk-xray-v2ray-vless-vmess-...-configs | ⭐381 | 2026-10-26 |
| zhuhaiuk/free-nodes | ⭐379 | 2026-10-26 |
| ShatakVPN/ConfigForge-V2Ray | ⭐375 | 2026-10-26 |
| Delta-Kronecker/V2ray-Config | ⭐368 | 2026-10-26 |
| cbusifabcap/daily_free_vpn | ⭐364 | 2026-10-26 |
| ovmvo/FreeSub | ⭐347 | 2026-10-26 |
| MhdiTaheri/V2rayCollector | ⭐321 | 2026-10-26 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐321 | 2026-10-26 |
| F0rc3Run/F0rc3Run | ⭐320 | 2026-10-26 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-10-26 |
| clashv2ray-hub/clashfree | ⭐310 | 2026-10-26 |
| clashv2ray-hub/v2rayfree | ⭐300 | 2026-10-26 |
| crashgfw/free-airport-nodes | ⭐294 | 2026-10-26 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-10-26 |
| wenxig/dongtai-sub | ⭐264 | 2026-10-26 |
| sakha1370/OpenRay | ⭐250 | 2026-10-26 |
| shenaba/2s-ui | ⭐246 | 2026-10-26 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐209 | 2026-10-26 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-10-26 |
| tglaoshiji/nodeshare | ⭐197 | 2026-10-26 |
| mheidari98/.proxy | ⭐190 | 2026-10-26 |
| xyfqzy/free-nodes | ⭐189 | 2026-10-26 |
| iboxz/free-v2ray-collector | ⭐188 | 2026-10-26 |
| xOS/Config | ⭐183 | 2026-10-26 |
| HakurouKen/free-node | ⭐180 | 2026-10-26 |
| V2RayRoot/V2RayConfig | ⭐174 | 2026-10-26 |
| junjun266/FreeProxyGo | ⭐163 | 2026-10-26 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐163 | 2026-10-26 |

### 节点来源分布（去重后，前 20）

- `barry-far/V2ray-Config/All_Configs_Sub.txt`：2051 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：1724 个节点
- `Barabama/FreeNodes/README→gh-proxy.com`：1606 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：496 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：394 个节点
- `peasoft/NoMoreWalls/list.txt`：372 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：371 个节点
- `barry-far/V2ray-Config/Sub3.txt`：124 个节点
- `barry-far/V2ray-Config/Sub1.txt`：119 个节点
- `Epodonios/v2ray-configs/Splitted-By-Protocol/vless.txt`：117 个节点
- `iboxz/free-v2ray-collector/main/vless.txt`：116 个节点
- `nyeinkokoaung404/V2ray-Configs/configs/proxy_configs_tested.txt`：97 个节点
- `barry-far/V2ray-Config/Sub2.txt`：77 个节点
- `snakem982/proxypool/source/sing-box-2.json`：57 个节点
- `crashgfw/free-airport-nodes/README→ndxy.fn0821.xyz`：30 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/combine/clash.config.yaml`：22 个节点
- `igareck/vpn-configs-for-russia/BLACK_VLESS_RUS_mobile.txt`：22 个节点
- `Epodonios/v2ray-configs/Splitted-By-Protocol/ss.txt`：15 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→www.xrayvip.com`：12 个节点
- `VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy/README→raw.githubusercontent.com`：10 个节点

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
