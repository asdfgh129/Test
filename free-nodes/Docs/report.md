# 免费节点采集报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-11-05 04:39

### 概览

- 扫描仓库：**160** 个
- 抓取订阅文件：**40** 个
- 原始提取节点：**855932** 条
- 两级去重后（完整链接 + 服务器:端口）：**89659** 条（剔除重复 766273 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 59376、xray 62278、clash 87523、singbox 85424
- 耗时：1076 秒

### TCP 延迟分布

- 可达服务器：**0/89635**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**2625** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 89635 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **81** 个仓库在 README 里给出订阅链接，从中提取 **855932** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| rtwo2/FastNodes | 10 | 691710 |
| SoliSpirit/v2ray-configs | 5 | 22967 |
| barry-far/V2ray-Config | 10 | 22301 |
| MustafaBaqer/VestraNet-Nodes | 6 | 18311 |
| hamedcode/port-based-v2ray-configs | 10 | 15640 |
| shabane/kamaji | 10 | 14358 |
| NiREvil/vless | 10 | 11146 |
| cbusifabcap/daily_free_vpn | 10 | 9363 |
| 0xRadikal/Free-v2ray-Configs | 10 | 7927 |
| MahanKenway/Freedom-V2Ray | 10 | 7208 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6856 |
| Delta-Kronecker/V2ray-Config | 10 | 6747 |
| Stintik-123/StintikVPN | 9 | 5611 |
| PuddinCat/BestClash | 10 | 4006 |
| whoahaow/rjsxrd | 10 | 3178 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 59424 |
| ss | 9994 |
| vmess | 9496 |
| trojan | 7833 |
| hysteria2 | 2304 |
| ssr | 287 |
| tuic | 253 |
| hysteria | 68 |

### 输出文件

- `v2ray_sub.txt`（59376 条，base64 订阅）
- `xray_sub.txt`（62278 条，base64 订阅）
- `clash_sub.yaml`（87523 个代理）
- `singbox_sub.json`（85424 个 outbound）
- `nodes_uris.txt`（89654 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 54.9 | 45%（17/38） | 1068ms | 66 |
| crashgfw/free-airport-nodes | 45.8 | 44%（8/18） | 2544ms | 2220 |
| xyfqzy/free-nodes | 40.6 | 25%（1/4） | 1144ms | 44 |
| F0rc3Run/F0rc3Run | 40.1 | 29%（104/360） | 1684ms | 6534 |
| zhuhaiuk/free-nodes | 38.3 | 25%（9/36） | 1536ms | 142 |
| 0xRadikal/Free-v2ray-Configs | 35.0 | 22%（183/841） | 1704ms | 131765 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 79274 |
| ermaozi01/free_clash_vpn | 25.0 | 36%（46/129） | -ms | 426 |
| snakem982/proxypool | 24.9 | 11%（61/541） | 2176ms | 2871 |
| whoahaow/rjsxrd | 22.5 | 4%（348/9908） | 1662ms | 37408 |
| NiREvil/vless | 22.2 | 1%（151/15758） | 1417ms | 153110 |
| kooker/FreeSubsCheck | 21.3 | 2%（30/1674） | 1654ms | 8859 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率45%/质量54.9)、crashgfw/free-airport-nodes(可用率44%/质量45.8)、ermaozi01/free_clash_vpn(可用率36%/质量25.0)、F0rc3Run/F0rc3Run(可用率29%/质量40.1)、zhuhaiuk/free-nodes(可用率25%/质量38.3)、xyfqzy/free-nodes(可用率25%/质量40.6)、0xRadikal/Free-v2ray-Configs(可用率22%/质量35.0)、snakem982/proxypool(可用率11%/质量24.9)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119945 | 2026-11-04 |
| mack-a/v2ray-agent | ⭐22284 | 2026-11-02 |
| Pawdroid/Free-servers | ⭐19809 | 2026-11-04 |
| DiningFactory/panda-vpn-pro | ⭐17390 | 2026-11-03 |
| free-nodes/clashfree | ⭐17174 | 2026-11-04 |
| free-nodes/v2rayfree | ⭐14802 | 2026-11-04 |
| alireza0/s-ui | ⭐10249 | 2026-11-02 |
| igareck/vpn-configs-for-russia | ⭐9434 | 2026-11-04 |
| ermaozi/get_subscribe | ⭐9433 | 2026-11-04 |
| eooce/nodejs-argo | ⭐8447 | 2026-11-02 |
| chengaopan/AutoMergePublicNodes | ⭐8327 | 2026-11-04 |
| Gozargah/Marzban | ⭐7507 | 2026-11-02 |
| free18/v2ray | ⭐5851 | 2026-11-04 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5708 | 2026-11-04 |
| nguyenphutrong/quotio | ⭐4907 | 2026-11-03 |
| anaer/Sub | ⭐3683 | 2026-11-04 |
| peasoft/NoMoreWalls | ⭐3596 | 2026-11-04 |
| Barabama/FreeNodes | ⭐3380 | 2026-11-04 |
| Alvin9999-newpac/fanqiang | ⭐3202 | 2026-11-04 |
| barry-far/V2ray-Config | ⭐2635 | 2026-11-04 |
| ripaojiedian/freenode | ⭐2386 | 2026-11-04 |
| KaWaIDeSuNe/dijiajichang | ⭐2254 | 2026-11-03 |
| snakem982/proxypool | ⭐2248 | 2026-11-04 |
| PuddinCat/BestClash | ⭐2060 | 2026-11-04 |
| qusong0627/QuantMind | ⭐1865 | 2026-11-04 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1865 | 2026-11-04 |
| crossxx-labs/free-proxy | ⭐1855 | 2026-11-04 |
| ZeroDeng01/sublinkPro | ⭐1737 | 2026-11-04 |
| LancelotRar/best-cf-ips | ⭐1641 | 2026-11-04 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-04 |
| jdnei/JiChangTuiJian | ⭐1512 | 2026-11-04 |
| everett7623/airport-recommendations-2026 | ⭐1481 | 2026-11-04 |
| NiREvil/vless | ⭐1365 | 2026-11-04 |
| Abao130/jichangtizi-tuijian | ⭐1352 | 2026-11-02 |
| shaoyouvip/free | ⭐1316 | 2026-11-02 |
| nevertoday/xiaoxiaodong-vps | ⭐1315 | 2026-11-04 |
| cfal/shoes | ⭐1288 | 2026-11-04 |
| Hidashimora/free-vpn-anti-rkn | ⭐1176 | 2026-11-04 |
| iluobei/miaomiaowu | ⭐1160 | 2026-11-04 |
| bq2015/FreeProxies | ⭐922 | 2026-11-04 |
| deezertidal/freevpn | ⭐892 | 2026-11-04 |
| jichangtuijian1/dizhi | ⭐892 | 2026-11-04 |
| whoahaow/rjsxrd | ⭐875 | 2026-11-04 |
| ermaozi01/free_clash_vpn | ⭐826 | 2026-11-04 |
| 0xRadikal/Free-v2ray-Configs | ⭐792 | 2026-11-04 |
| YuanDevTeam/OneXray | ⭐766 | 2026-11-04 |
| dongchengjie/airport | ⭐751 | 2026-11-04 |
| sylearn/AIUsage | ⭐739 | 2026-11-02 |
| ts-sf/fly | ⭐714 | 2026-11-04 |
| Leadaxe/LxBox | ⭐708 | 2026-11-04 |
| MatinGhanbari/v2ray-configs | ⭐700 | 2026-11-04 |
| gslege/CloudflareIP | ⭐681 | 2026-11-04 |
| hello-yunshu/Xray_bash_onekey | ⭐670 | 2026-11-04 |
| hello-world-1989/cn-news | ⭐650 | 2026-11-04 |
| OpenNetCN/clash | ⭐644 | 2026-11-04 |
| SoliSpirit/v2ray-configs | ⭐637 | 2026-11-04 |
| jichangtuijian-cheap/cheap-airports | ⭐627 | 2026-11-04 |
| kort0881/vpn-vless-configs-russia | ⭐626 | 2026-11-04 |
| jichangzhu/JichangTuijian | ⭐584 | 2026-11-04 |
| sunmiao4458/free-proxy-airport | ⭐561 | 2026-11-04 |
| Huibq/TrojanLinks | ⭐547 | 2026-11-04 |
| CCSH/IPTV | ⭐543 | 2026-11-04 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-04 |
| getmeridian/meridian | ⭐500 | 2026-11-04 |
| VpnNetwork01/vpn-net | ⭐471 | 2026-11-03 |
| ssrlive/proxypool | ⭐454 | 2026-11-03 |
| kooker/FreeSubsCheck | ⭐453 | 2026-11-04 |
| itsyebekhe/PSG | ⭐446 | 2026-11-04 |
| sinavm/SVM | ⭐445 | 2026-11-04 |
| SubConv/SubConv | ⭐412 | 2026-11-04 |
| zhuhaiuk/free-nodes | ⭐406 | 2026-11-04 |
| cbusifabcap/daily_free_vpn | ⭐393 | 2026-11-04 |
| ShatakVPN/ConfigForge-V2Ray | ⭐378 | 2026-11-04 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-03 |
| DevDock-AI/claude-unlimited | ⭐337 | 2026-11-04 |
| Mahdi0024/ProxyCollector | ⭐331 | 2026-11-04 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐324 | 2026-11-04 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-04 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-04 |
| clashv2ray-hub/clashfree | ⭐313 | 2026-11-04 |
| WLget/V2Ray_configs_64 | ⭐312 | 2026-11-04 |
| crashgfw/free-airport-nodes | ⭐304 | 2026-11-04 |
| clashv2ray-hub/v2rayfree | ⭐303 | 2026-11-04 |
| ghuntley/underclass | ⭐295 | 2026-11-04 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-11-04 |
| wenxig/dongtai-sub | ⭐273 | 2026-11-04 |
| shenaba/2s-ui | ⭐270 | 2026-11-04 |
| DanielLavrushin/asuswrt-merlin-xrayui | ⭐264 | 2026-11-04 |
| 5VNetwork/VX | ⭐260 | 2026-11-03 |
| sakha1370/OpenRay | ⭐252 | 2026-11-04 |
| yanisplugg/yptun | ⭐251 | 2026-11-04 |
| Mistgate/mistgate | ⭐233 | 2026-11-04 |
| zuluion/Clash-Template-Config | ⭐227 | 2026-11-04 |
| jichangx/free-nodes | ⭐225 | 2026-11-03 |
| crystalmasta/unbihex | ⭐224 | 2026-11-04 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐213 | 2026-11-04 |
| daimon3332/easy-proxies | ⭐205 | 2026-11-04 |
| nyeinkokoaung404/V2ray-Configs | ⭐203 | 2026-11-04 |
| tglaoshiji/nodeshare | ⭐199 | 2026-11-04 |
| xyfqzy/free-nodes | ⭐193 | 2026-11-04 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-04 |
| mheidari98/.proxy | ⭐192 | 2026-11-04 |
| kazeyukiro/3m-ui | ⭐191 | 2026-11-04 |
| xOS/Config | ⭐183 | 2026-11-04 |
| HakurouKen/free-node | ⭐179 | 2026-11-04 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-04 |
| shabane/kamaji | ⭐173 | 2026-11-04 |
| Iman/caspian | ⭐169 | 2026-11-04 |
| bestnite/sub2sing-box | ⭐168 | 2026-11-03 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐167 | 2026-11-04 |
| Stintik-123/StintikVPN | ⭐164 | 2026-11-02 |
| junjun266/FreeProxyGo | ⭐162 | 2026-11-04 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-04 |
| enriquephl/QuantumultX_config | ⭐159 | 2026-11-04 |
| 029danio/jichangfree | ⭐158 | 2026-11-04 |
| thsrite/configflow | ⭐157 | 2026-11-03 |
| Danialsamadi/v2go | ⭐155 | 2026-11-04 |
| mhmdxahmd/mafly | ⭐155 | 2026-11-04 |
| licheng527/Free-servers | ⭐153 | 2026-11-04 |
| Medium1992/mihomo-proxy-ros | ⭐149 | 2026-11-02 |
| Firmfox/Proxify | ⭐147 | 2026-11-04 |
| kjfx/v2ray1 | ⭐143 | 2026-11-04 |
| jctaoo/ClashConfig | ⭐143 | 2026-11-03 |
| Q7DF1/XrayFA | ⭐140 | 2026-11-04 |
| SnapdragonLee/SystemProxy | ⭐138 | 2026-11-04 |
| hamedcode/port-based-v2ray-configs | ⭐136 | 2026-11-04 |
| LancelotRar/free-subs | ⭐130 | 2026-11-04 |
| deezertidal/fee-based | ⭐129 | 2026-11-04 |
| JohnWatsoon/WatTunnel | ⭐129 | 2026-11-04 |
| nikships/droidproxy | ⭐126 | 2026-11-04 |
| MahanKenway/Freedom-V2Ray | ⭐122 | 2026-11-04 |
| splify2/steer | ⭐120 | 2026-11-04 |
| Re0XIAOPA/AutoScrapeFreeNodes | ⭐115 | 2026-11-04 |
| xianer235/115-media-hub | ⭐115 | 2026-11-02 |
| kure29/flyx | ⭐114 | 2026-11-04 |
| nodesfree/v2raynode | ⭐109 | 2026-11-04 |
| Lemonochka/keqdroid | ⭐108 | 2026-11-02 |
| VoroninaYanina/free-nodes | ⭐103 | 2026-11-04 |
| 4n0nymou3/multi-proxy-config-fetcher | ⭐103 | 2026-11-04 |
| rtwo2/FastNodes | ⭐101 | 2026-11-04 |
| mohamadfg-dev/telegram-v2ray-configs-collector | ⭐100 | 2026-11-04 |
| Romaxa55/MegaV_Public | ⭐100 | 2026-11-04 |
| FLAT447/v2ray-lists | ⭐98 | 2026-11-04 |
| NanoCloud-Release/NanoCloud | ⭐96 | 2026-11-02 |
| bin1site1/V2rayFree | ⭐95 | 2026-11-04 |
| bbq-051116/TG-iamdt009 | ⭐94 | 2026-11-03 |
| MustafaBaqer/VestraNet-Nodes | ⭐92 | 2026-11-04 |
| zzmy1917-svg/cheap-vpn-airport | ⭐90 | 2026-11-03 |
| TG-NAV/nodeshare | ⭐89 | 2026-11-04 |
| MohammadBahemmat/V2ray-Collector | ⭐88 | 2026-11-04 |
| nodesfree/clashnode | ⭐82 | 2026-11-04 |
| xiaoli8571/TunBox | ⭐82 | 2026-11-04 |
| fafnirov/KaproTUN | ⭐76 | 2026-11-04 |
| WLget/V2ray_free | ⭐75 | 2026-11-04 |
| toml66l/fanqiang | ⭐75 | 2026-11-04 |
| enkinvsh/dropweb | ⭐75 | 2026-11-04 |
| farvater-app/farvater | ⭐75 | 2026-11-03 |
| hysteria350/free-jichang | ⭐74 | 2026-11-04 |
| v2raynnodes/v2rayfree | ⭐74 | 2026-11-04 |
| inferno1978/Chimera-Project | ⭐71 | 2026-11-04 |

### 节点来源分布（去重后，前 20）

- `rtwo2/FastNodes/sub/ipv4_only.txt`：67578 个节点
- `rtwo2/FastNodes/sub/verified_tls.txt`：12036 个节点
- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2306 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：860 个节点
- `rtwo2/FastNodes/sub/everything.txt`：791 个节点
- `MustafaBaqer/VestraNet-Nodes/subscriptions/mix-base64.txt`：658 个节点
- `Stintik-123/StintikVPN/README→raw.githubusercontent.com`：654 个节点
- `hamedcode/port-based-v2ray-configs/sub/port_443.txt`：626 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/vless.txt`：547 个节点
- `rtwo2/FastNodes/sub/top.txt`：485 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：479 个节点
- `rtwo2/FastNodes/sub/ipv6_only.txt`：343 个节点
- `hamedcode/port-based-v2ray-configs/sub/vmess.txt`：243 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：188 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/trojan.txt`：170 个节点
- `Stintik-123/StintikVPN/README→gitverse.ru`：155 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：138 个节点
- `rtwo2/FastNodes/sub/top_ipv6.txt`：131 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：126 个节点
- `hamedcode/port-based-v2ray-configs/sub/vless.txt`：101 个节点

## 2026-11-04 21:13

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**26** 个
- 原始提取节点：**93763** 条
- 两级去重后（完整链接 + 服务器:端口）：**12274** 条（剔除重复 81489 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 10460、xray 10479、clash 12111、singbox 11817
- 耗时：388 秒

### TCP 延迟分布

- 可达服务器：**0/12252**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**2075** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 12252 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **46** 个仓库在 README 里给出订阅链接，从中提取 **93763** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 22898 |
| barry-far/V2ray-Config | 10 | 21984 |
| NiREvil/vless | 10 | 11537 |
| cbusifabcap/daily_free_vpn | 10 | 10674 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8251 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6949 |
| PuddinCat/BestClash | 10 | 3876 |
| whoahaow/rjsxrd | 10 | 3171 |
| Hidashimora/free-vpn-anti-rkn | 10 | 1093 |
| F0rc3Run/F0rc3Run | 7 | 686 |
| kooker/FreeSubsCheck | 5 | 663 |
| peasoft/NoMoreWalls | 1 | 430 |
| chengaopan/AutoMergePublicNodes | 2 | 430 |
| igareck/vpn-configs-for-russia | 10 | 395 |
| crashgfw/free-airport-nodes | 10 | 270 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5177 |
| vmess | 3664 |
| ss | 2177 |
| trojan | 865 |
| hysteria2 | 376 |
| hysteria | 7 |
| ssr | 6 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（10460 条，base64 订阅）
- `xray_sub.txt`（10479 条，base64 订阅）
- `clash_sub.yaml`（12111 个代理）
- `singbox_sub.json`（11817 个 outbound）
- `nodes_uris.txt`（12245 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 57.5 | 54%（46/85） | 1732ms | 376 |
| hello-world-1989/cn-news | 54.9 | 45%（17/38） | 1068ms | 60 |
| xyfqzy/free-nodes | 40.6 | 25%（1/4） | 1144ms | 42 |
| F0rc3Run/F0rc3Run | 37.8 | 30%（104/351） | 2149ms | 5978 |
| 0xRadikal/Free-v2ray-Configs | 33.9 | 21%（123/581） | 1825ms | 123838 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 64916 |
| cbusifabcap/daily_free_vpn | 22.0 | 3%（32/1060） | 1684ms | 86787 |
| whoahaow/rjsxrd | 21.3 | 4%（299/8241） | 1863ms | 34230 |
| igareck/vpn-configs-for-russia | 19.8 | 4%（7/192） | 2115ms | 11908 |
| nyeinkokoaung404/V2ray-Configs | 18.9 | 1%（40/3590） | 1973ms | 84016 |
| sinavm/SVM | 18.7 | 8%（14/184） | 2776ms | 1083 |
| danmaifu/mianfeijiedian | 17.4 | 4%（32/895） | 2512ms | 6084 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率54%/质量57.5)、hello-world-1989/cn-news(可用率45%/质量54.9)、F0rc3Run/F0rc3Run(可用率30%/质量37.8)、xyfqzy/free-nodes(可用率25%/质量40.6)、0xRadikal/Free-v2ray-Configs(可用率21%/质量33.9)、Pawdroid/Free-servers(可用率19%/质量13.4)、zhuhaiuk/free-nodes(可用率11%/质量7.8)、snakem982/proxypool(可用率11%/质量7.7)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119918 | 2026-11-04 |
| Pawdroid/Free-servers | ⭐19808 | 2026-11-04 |
| free-nodes/clashfree | ⭐17173 | 2026-11-04 |
| free-nodes/v2rayfree | ⭐14794 | 2026-11-04 |
| igareck/vpn-configs-for-russia | ⭐9432 | 2026-11-04 |
| ermaozi/get_subscribe | ⭐9432 | 2026-11-04 |
| chengaopan/AutoMergePublicNodes | ⭐8326 | 2026-11-04 |
| free18/v2ray | ⭐5849 | 2026-11-04 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5707 | 2026-11-04 |
| peasoft/NoMoreWalls | ⭐3595 | 2026-11-04 |
| Barabama/FreeNodes | ⭐3379 | 2026-11-04 |
| Alvin9999-newpac/fanqiang | ⭐3199 | 2026-11-04 |
| barry-far/V2ray-Config | ⭐2634 | 2026-11-04 |
| snakem982/proxypool | ⭐2243 | 2026-11-04 |
| PuddinCat/BestClash | ⭐2060 | 2026-11-04 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1863 | 2026-11-04 |
| qusong0627/QuantMind | ⭐1862 | 2026-11-04 |
| crossxx-labs/free-proxy | ⭐1855 | 2026-11-04 |
| ZeroDeng01/sublinkPro | ⭐1737 | 2026-11-04 |
| LancelotRar/best-cf-ips | ⭐1640 | 2026-11-04 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-04 |
| jdnei/JiChangTuiJian | ⭐1501 | 2026-11-04 |
| everett7623/airport-recommendations-2026 | ⭐1481 | 2026-11-04 |
| NiREvil/vless | ⭐1365 | 2026-11-04 |
| cfal/shoes | ⭐1288 | 2026-11-04 |
| nevertoday/xiaoxiaodong-vps | ⭐1283 | 2026-11-04 |
| Hidashimora/free-vpn-anti-rkn | ⭐1174 | 2026-11-04 |
| bq2015/FreeProxies | ⭐921 | 2026-11-04 |
| deezertidal/freevpn | ⭐892 | 2026-11-04 |
| jichangtuijian1/dizhi | ⭐891 | 2026-11-04 |
| whoahaow/rjsxrd | ⭐875 | 2026-11-04 |
| ermaozi01/free_clash_vpn | ⭐826 | 2026-11-04 |
| 0xRadikal/Free-v2ray-Configs | ⭐791 | 2026-11-04 |
| dongchengjie/airport | ⭐751 | 2026-11-04 |
| ts-sf/fly | ⭐714 | 2026-11-04 |
| Leadaxe/LxBox | ⭐707 | 2026-11-04 |
| MatinGhanbari/v2ray-configs | ⭐698 | 2026-11-04 |
| gslege/CloudflareIP | ⭐680 | 2026-11-04 |
| hello-yunshu/Xray_bash_onekey | ⭐669 | 2026-11-04 |
| hello-world-1989/cn-news | ⭐650 | 2026-11-04 |
| OpenNetCN/clash | ⭐644 | 2026-11-04 |
| SoliSpirit/v2ray-configs | ⭐637 | 2026-11-04 |
| kort0881/vpn-vless-configs-russia | ⭐626 | 2026-11-04 |
| jichangtuijian-cheap/cheap-airports | ⭐626 | 2026-11-04 |
| jichangzhu/JichangTuijian | ⭐583 | 2026-11-04 |
| sunmiao4458/free-proxy-airport | ⭐560 | 2026-11-04 |
| CCSH/IPTV | ⭐543 | 2026-11-04 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-04 |
| getmeridian/meridian | ⭐500 | 2026-11-04 |
| kooker/FreeSubsCheck | ⭐453 | 2026-11-04 |
| itsyebekhe/PSG | ⭐446 | 2026-11-04 |
| sinavm/SVM | ⭐445 | 2026-11-04 |
| SubConv/SubConv | ⭐412 | 2026-11-04 |
| zhuhaiuk/free-nodes | ⭐406 | 2026-11-04 |
| cbusifabcap/daily_free_vpn | ⭐393 | 2026-11-04 |
| ShatakVPN/ConfigForge-V2Ray | ⭐378 | 2026-11-04 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐324 | 2026-11-04 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-04 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-04 |
| clashv2ray-hub/clashfree | ⭐313 | 2026-11-04 |
| WLget/V2Ray_configs_64 | ⭐312 | 2026-11-04 |
| clashv2ray-hub/v2rayfree | ⭐303 | 2026-11-04 |
| crashgfw/free-airport-nodes | ⭐303 | 2026-11-04 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-11-04 |
| wenxig/dongtai-sub | ⭐273 | 2026-11-04 |
| DanielLavrushin/asuswrt-merlin-xrayui | ⭐264 | 2026-11-04 |
| sakha1370/OpenRay | ⭐252 | 2026-11-04 |
| yanisplugg/yptun | ⭐249 | 2026-11-04 |
| Mistgate/mistgate | ⭐230 | 2026-11-04 |
| zuluion/Clash-Template-Config | ⭐227 | 2026-11-04 |
| crystalmasta/unbihex | ⭐222 | 2026-11-04 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐213 | 2026-11-04 |
| nyeinkokoaung404/V2ray-Configs | ⭐203 | 2026-11-04 |
| tglaoshiji/nodeshare | ⭐199 | 2026-11-04 |
| xyfqzy/free-nodes | ⭐193 | 2026-11-04 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-04 |
| mheidari98/.proxy | ⭐192 | 2026-11-04 |
| xOS/Config | ⭐183 | 2026-11-04 |
| HakurouKen/free-node | ⭐179 | 2026-11-04 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-04 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4507 个节点
- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2919 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：634 个节点
- `0xRadikal/Free-v2ray-Configs/verified/clash.yaml`：540 个节点
- `cbusifabcap/daily_free_vpn/Z.txt`：348 个节点
- `peasoft/NoMoreWalls/list.txt`：256 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：253 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/2.1.txt`：236 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/1.1.txt`：223 个节点
- `F0rc3Run/F0rc3Run/Best-Results/clash.yaml`：220 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `Hidashimora/free-vpn-anti-rkn/configs/3.1.txt`：154 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：149 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：149 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：144 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：139 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：130 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：127 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：119 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：119 个节点

## 2026-11-03 22:11

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**26** 个
- 原始提取节点：**119663** 条
- 两级去重后（完整链接 + 服务器:端口）：**12916** 条（剔除重复 106747 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 11002、xray 10690、clash 12778、singbox 12453
- 耗时：528 秒

### TCP 延迟分布

- 可达服务器：**0/12888**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**2181** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 12888 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **48** 个仓库在 README 里给出订阅链接，从中提取 **119663** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23037 |
| barry-far/V2ray-Config | 10 | 22081 |
| sakha1370/OpenRay | 10 | 18744 |
| NiREvil/vless | 10 | 11586 |
| cbusifabcap/daily_free_vpn | 10 | 11249 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8672 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7005 |
| Delta-Kronecker/V2ray-Config | 10 | 6747 |
| PuddinCat/BestClash | 10 | 4002 |
| whoahaow/rjsxrd | 10 | 3208 |
| kooker/FreeSubsCheck | 5 | 669 |
| F0rc3Run/F0rc3Run | 7 | 599 |
| igareck/vpn-configs-for-russia | 10 | 580 |
| peasoft/NoMoreWalls | 1 | 480 |
| chengaopan/AutoMergePublicNodes | 2 | 480 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5081 |
| vmess | 3649 |
| ss | 2176 |
| trojan | 1605 |
| hysteria2 | 387 |
| hysteria | 8 |
| ssr | 7 |
| tuic | 3 |

### 输出文件

- `v2ray_sub.txt`（11002 条，base64 订阅）
- `xray_sub.txt`（10690 条，base64 订阅）
- `clash_sub.yaml`（12778 个代理）
- `singbox_sub.json`（12453 个 outbound）
- `nodes_uris.txt`（12900 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 62.5 | 57%（24/42） | 1253ms | 48 |
| ermaozi01/free_clash_vpn | 55.9 | 50%（12/24） | 1509ms | 266 |
| F0rc3Run/F0rc3Run | 45.7 | 36%（101/282） | 1558ms | 4693 |
| 0xRadikal/Free-v2ray-Configs | 35.4 | 20%（61/313） | 1380ms | 107154 |
| Pawdroid/Free-servers | 34.4 | 26%（19/73） | 2296ms | 166 |
| snakem982/proxypool | 29.1 | 15%（78/510） | 1933ms | 2390 |
| peasoft/NoMoreWalls | 28.5 | 6%（72/1186） | 959ms | 5318 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 51714 |
| NiREvil/vless | 24.4 | 2%（274/15946） | 1128ms | 118854 |
| barry-far/V2ray-Config | 23.5 | 1%（5/656） | 1174ms | 174708 |
| whoahaow/rjsxrd | 21.9 | 5%（368/7819） | 1906ms | 27789 |
| igareck/vpn-configs-for-russia | 20.6 | 5%（6/121） | 2143ms | 10909 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率57%/质量62.5)、ermaozi01/free_clash_vpn(可用率50%/质量55.9)、F0rc3Run/F0rc3Run(可用率36%/质量45.7)、Pawdroid/Free-servers(可用率26%/质量34.4)、0xRadikal/Free-v2ray-Configs(可用率20%/质量35.4)、snakem982/proxypool(可用率15%/质量29.1)、zhuhaiuk/free-nodes(可用率11%/质量7.8)、Danialsamadi/v2go(可用率8%/质量5.6)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119861 | 2026-11-03 |
| Pawdroid/Free-servers | ⭐19794 | 2026-11-03 |
| free-nodes/clashfree | ⭐17166 | 2026-11-03 |
| free-nodes/v2rayfree | ⭐14768 | 2026-11-03 |
| ermaozi/get_subscribe | ⭐9430 | 2026-11-03 |
| igareck/vpn-configs-for-russia | ⭐9424 | 2026-11-03 |
| chengaopan/AutoMergePublicNodes | ⭐8325 | 2026-11-03 |
| free18/v2ray | ⭐5840 | 2026-11-03 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5700 | 2026-11-03 |
| nguyenphutrong/quotio | ⭐4906 | 2026-11-03 |
| peasoft/NoMoreWalls | ⭐3595 | 2026-11-03 |
| Barabama/FreeNodes | ⭐3375 | 2026-11-03 |
| Alvin9999-newpac/fanqiang | ⭐3193 | 2026-11-03 |
| barry-far/V2ray-Config | ⭐2629 | 2026-11-03 |
| snakem982/proxypool | ⭐2243 | 2026-11-03 |
| KaWaIDeSuNe/dijiajichang | ⭐2243 | 2026-11-03 |
| PuddinCat/BestClash | ⭐2059 | 2026-11-03 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1860 | 2026-11-03 |
| qusong0627/QuantMind | ⭐1859 | 2026-11-03 |
| crossxx-labs/free-proxy | ⭐1856 | 2026-11-03 |
| ZeroDeng01/sublinkPro | ⭐1737 | 2026-11-03 |
| LancelotRar/best-cf-ips | ⭐1639 | 2026-11-03 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-03 |
| jdnei/JiChangTuiJian | ⭐1489 | 2026-11-03 |
| everett7623/airport-recommendations-2026 | ⭐1477 | 2026-11-03 |
| NiREvil/vless | ⭐1365 | 2026-11-03 |
| cfal/shoes | ⭐1287 | 2026-11-03 |
| Hidashimora/free-vpn-anti-rkn | ⭐1164 | 2026-11-03 |
| bq2015/FreeProxies | ⭐920 | 2026-11-03 |
| deezertidal/freevpn | ⭐891 | 2026-11-03 |
| whoahaow/rjsxrd | ⭐874 | 2026-11-03 |
| ermaozi01/free_clash_vpn | ⭐825 | 2026-11-03 |
| 0xRadikal/Free-v2ray-Configs | ⭐785 | 2026-11-03 |
| YuanDevTeam/OneXray | ⭐762 | 2026-11-03 |
| dongchengjie/airport | ⭐752 | 2026-11-03 |
| ts-sf/fly | ⭐714 | 2026-11-03 |
| Leadaxe/LxBox | ⭐702 | 2026-11-03 |
| MatinGhanbari/v2ray-configs | ⭐694 | 2026-11-03 |
| gslege/CloudflareIP | ⭐679 | 2026-11-03 |
| hello-yunshu/Xray_bash_onekey | ⭐668 | 2026-11-03 |
| hello-world-1989/cn-news | ⭐649 | 2026-11-03 |
| OpenNetCN/clash | ⭐644 | 2026-11-03 |
| SoliSpirit/v2ray-configs | ⭐636 | 2026-11-03 |
| kort0881/vpn-vless-configs-russia | ⭐627 | 2026-11-03 |
| jichangtuijian-cheap/cheap-airports | ⭐623 | 2026-11-03 |
| jichangzhu/JichangTuijian | ⭐583 | 2026-11-03 |
| sunmiao4458/free-proxy-airport | ⭐560 | 2026-11-03 |
| CCSH/IPTV | ⭐540 | 2026-11-03 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-03 |
| getmeridian/meridian | ⭐500 | 2026-11-03 |
| VpnNetwork01/vpn-net | ⭐470 | 2026-11-03 |
| kooker/FreeSubsCheck | ⭐452 | 2026-11-03 |
| itsyebekhe/PSG | ⭐446 | 2026-11-03 |
| sinavm/SVM | ⭐445 | 2026-11-03 |
| zhuhaiuk/free-nodes | ⭐401 | 2026-11-03 |
| cbusifabcap/daily_free_vpn | ⭐390 | 2026-11-03 |
| ShatakVPN/ConfigForge-V2Ray | ⭐377 | 2026-11-03 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-03 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐323 | 2026-11-03 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-03 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-03 |
| WLget/V2Ray_configs_64 | ⭐312 | 2026-11-03 |
| clashv2ray-hub/clashfree | ⭐312 | 2026-11-03 |
| clashv2ray-hub/v2rayfree | ⭐303 | 2026-11-03 |
| crashgfw/free-airport-nodes | ⭐302 | 2026-11-03 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-11-03 |
| wenxig/dongtai-sub | ⭐273 | 2026-11-03 |
| shenaba/2s-ui | ⭐265 | 2026-11-03 |
| DanielLavrushin/asuswrt-merlin-xrayui | ⭐264 | 2026-11-03 |
| 5VNetwork/VX | ⭐260 | 2026-11-03 |
| sakha1370/OpenRay | ⭐251 | 2026-11-03 |
| Mistgate/mistgate | ⭐213 | 2026-11-03 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐212 | 2026-11-03 |
| nyeinkokoaung404/V2ray-Configs | ⭐202 | 2026-11-03 |
| tglaoshiji/nodeshare | ⭐199 | 2026-11-03 |
| xyfqzy/free-nodes | ⭐192 | 2026-11-03 |
| iboxz/free-v2ray-collector | ⭐191 | 2026-11-03 |
| mheidari98/.proxy | ⭐191 | 2026-11-03 |
| xOS/Config | ⭐183 | 2026-11-03 |
| HakurouKen/free-node | ⭐180 | 2026-11-03 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4361 个节点
- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2953 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：1115 个节点
- `0xRadikal/Free-v2ray-Configs/verified/clash.yaml`：571 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：490 个节点
- `cbusifabcap/daily_free_vpn/Z.txt`：442 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：431 个节点
- `peasoft/NoMoreWalls/list.txt`：222 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：207 个节点
- `F0rc3Run/F0rc3Run/Best-Results/clash.yaml`：189 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：149 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：141 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：140 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：140 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：137 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：113 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：102 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：100 个节点
- `barry-far/V2ray-Config/Sub1.txt`：88 个节点

## 2026-11-02 22:11

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**28** 个
- 原始提取节点：**128827** 条
- 两级去重后（完整链接 + 服务器:端口）：**13982** 条（剔除重复 114845 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 11815、xray 11706、clash 13863、singbox 13492
- 耗时：501 秒

### TCP 延迟分布

- 可达服务器：**0/13982**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1867** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 13982 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **51** 个仓库在 README 里给出订阅链接，从中提取 **128827** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 22627 |
| barry-far/V2ray-Config | 10 | 21424 |
| sakha1370/OpenRay | 10 | 19620 |
| NiREvil/vless | 10 | 12611 |
| cbusifabcap/daily_free_vpn | 10 | 10804 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9065 |
| MatinGhanbari/v2ray-configs | 10 | 8110 |
| Delta-Kronecker/V2ray-Config | 10 | 7173 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7001 |
| whoahaow/rjsxrd | 10 | 3413 |
| dongchengjie/airport | 10 | 2462 |
| ShatakVPN/ConfigForge-V2Ray | 8 | 993 |
| kooker/FreeSubsCheck | 5 | 707 |
| igareck/vpn-configs-for-russia | 10 | 681 |
| F0rc3Run/F0rc3Run | 7 | 580 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 6045 |
| vmess | 3640 |
| ss | 2001 |
| trojan | 1731 |
| hysteria2 | 528 |
| ssr | 27 |
| hysteria | 5 |
| tuic | 5 |

### 输出文件

- `v2ray_sub.txt`（11815 条，base64 订阅）
- `xray_sub.txt`（11706 条，base64 订阅）
- `clash_sub.yaml`（13863 个代理）
- `singbox_sub.json`（13492 个 outbound）
- `nodes_uris.txt`（13982 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 66.6 | 56%（18/32） | 462ms | 36 |
| F0rc3Run/F0rc3Run | 44.6 | 34%（68/202） | 1504ms | 3514 |
| snakem982/proxypool | 30.1 | 15%（69/450） | 1772ms | 2067 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 38512 |
| kooker/FreeSubsCheck | 25.2 | 4%（38/968） | 1255ms | 5461 |
| peasoft/NoMoreWalls | 24.5 | 8%（76/932） | 1881ms | 4411 |
| NiREvil/vless | 23.5 | 3%（572/20177） | 1418ms | 95997 |
| whoahaow/rjsxrd | 23.3 | 6%（326/5856） | 1762ms | 21264 |
| Pawdroid/Free-servers | 22.5 | 32%（28/87） | -ms | 139 |
| nyeinkokoaung404/V2ray-Configs | 18.9 | 1%（40/3590） | 1973ms | 56007 |
| danmaifu/mianfeijiedian | 17.4 | 4%（32/895） | 2512ms | 4566 |
| ermaozi01/free_clash_vpn | 11.7 | 17%（2/12） | -ms | 176 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率56%/质量66.6)、F0rc3Run/F0rc3Run(可用率34%/质量44.6)、Pawdroid/Free-servers(可用率32%/质量22.5)、ermaozi01/free_clash_vpn(可用率17%/质量11.7)、snakem982/proxypool(可用率15%/质量30.1)、igareck/vpn-configs-for-russia(可用率13%/质量9.2)、0xRadikal/Free-v2ray-Configs(可用率11%/质量7.9)、zhuhaiuk/free-nodes(可用率11%/质量7.8)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119795 | 2026-11-02 |
| mack-a/v2ray-agent | ⭐22271 | 2026-11-02 |
| Pawdroid/Free-servers | ⭐19778 | 2026-11-02 |
| DiningFactory/panda-vpn-pro | ⭐17296 | 2026-11-02 |
| free-nodes/clashfree | ⭐17153 | 2026-11-02 |
| free-nodes/v2rayfree | ⭐14749 | 2026-11-02 |
| ermaozi/get_subscribe | ⭐9426 | 2026-11-02 |
| igareck/vpn-configs-for-russia | ⭐9415 | 2026-11-02 |
| eooce/nodejs-argo | ⭐8440 | 2026-11-02 |
| chengaopan/AutoMergePublicNodes | ⭐8318 | 2026-11-02 |
| Gozargah/Marzban | ⭐7502 | 2026-11-02 |
| free18/v2ray | ⭐5836 | 2026-11-02 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5698 | 2026-11-02 |
| nguyenphutrong/quotio | ⭐4904 | 2026-11-02 |
| peasoft/NoMoreWalls | ⭐3593 | 2026-11-02 |
| Barabama/FreeNodes | ⭐3371 | 2026-11-02 |
| Alvin9999-newpac/fanqiang | ⭐3187 | 2026-11-02 |
| barry-far/V2ray-Config | ⭐2627 | 2026-11-02 |
| ripaojiedian/freenode | ⭐2388 | 2026-11-02 |
| snakem982/proxypool | ⭐2238 | 2026-11-02 |
| KaWaIDeSuNe/dijiajichang | ⭐2238 | 2026-11-02 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1860 | 2026-11-02 |
| crossxx-labs/free-proxy | ⭐1857 | 2026-11-02 |
| qusong0627/QuantMind | ⭐1851 | 2026-11-02 |
| LancelotRar/best-cf-ips | ⭐1633 | 2026-11-02 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-02 |
| jdnei/JiChangTuiJian | ⭐1462 | 2026-11-02 |
| NiREvil/vless | ⭐1363 | 2026-11-02 |
| Abao130/jichangtizi-tuijian | ⭐1341 | 2026-11-02 |
| shaoyouvip/free | ⭐1314 | 2026-11-02 |
| Hidashimora/free-vpn-anti-rkn | ⭐1155 | 2026-11-02 |
| bq2015/FreeProxies | ⭐920 | 2026-11-02 |
| deezertidal/freevpn | ⭐890 | 2026-11-02 |
| whoahaow/rjsxrd | ⭐874 | 2026-11-02 |
| ermaozi01/free_clash_vpn | ⭐825 | 2026-11-02 |
| 0xRadikal/Free-v2ray-Configs | ⭐784 | 2026-11-02 |
| YuanDevTeam/OneXray | ⭐759 | 2026-11-02 |
| dongchengjie/airport | ⭐750 | 2026-11-02 |
| sylearn/AIUsage | ⭐737 | 2026-11-02 |
| ts-sf/fly | ⭐713 | 2026-11-02 |
| Leadaxe/LxBox | ⭐694 | 2026-11-02 |
| MatinGhanbari/v2ray-configs | ⭐694 | 2026-11-02 |
| gslege/CloudflareIP | ⭐679 | 2026-11-02 |
| hello-yunshu/Xray_bash_onekey | ⭐665 | 2026-11-02 |
| hello-world-1989/cn-news | ⭐647 | 2026-11-02 |
| OpenNetCN/clash | ⭐644 | 2026-11-02 |
| SoliSpirit/v2ray-configs | ⭐636 | 2026-11-02 |
| kort0881/vpn-vless-configs-russia | ⭐627 | 2026-11-02 |
| jichangtuijian-cheap/cheap-airports | ⭐621 | 2026-11-02 |
| sunmiao4458/free-proxy-airport | ⭐560 | 2026-11-02 |
| CCSH/IPTV | ⭐538 | 2026-11-02 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-02 |
| getmeridian/meridian | ⭐500 | 2026-11-02 |
| kooker/FreeSubsCheck | ⭐451 | 2026-11-02 |
| itsyebekhe/PSG | ⭐445 | 2026-11-02 |
| sinavm/SVM | ⭐445 | 2026-11-02 |
| zhuhaiuk/free-nodes | ⭐399 | 2026-11-02 |
| cbusifabcap/daily_free_vpn | ⭐388 | 2026-11-02 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-11-02 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-02 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐323 | 2026-11-02 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-02 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-02 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-02 |
| clashv2ray-hub/clashfree | ⭐311 | 2026-11-02 |
| crashgfw/free-airport-nodes | ⭐303 | 2026-11-02 |
| clashv2ray-hub/v2rayfree | ⭐302 | 2026-11-02 |
| Surfboardv2ray/TGParse | ⭐294 | 2026-11-02 |
| wenxig/dongtai-sub | ⭐271 | 2026-11-02 |
| sakha1370/OpenRay | ⭐251 | 2026-11-02 |
| yanisplugg/yptun | ⭐244 | 2026-11-02 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐211 | 2026-11-02 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-11-02 |
| tglaoshiji/nodeshare | ⭐199 | 2026-11-02 |
| iboxz/free-v2ray-collector | ⭐191 | 2026-11-02 |
| mheidari98/.proxy | ⭐191 | 2026-11-02 |
| Mistgate/mistgate | ⭐188 | 2026-11-02 |
| xOS/Config | ⭐183 | 2026-11-02 |
| HakurouKen/free-node | ⭐180 | 2026-11-02 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-11-02 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4532 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/all_sub.txt`：1675 个节点
- `dongchengjie/airport/subs/merged/tested_within.yaml`：1103 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：1037 个节点
- `0xRadikal/Free-v2ray-Configs/verified/clash.yaml`：552 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：510 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：441 个节点
- `cbusifabcap/daily_free_vpn/sub/ClashMeta.yml`：386 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/filtered/subs/vmess.txt`：323 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：298 个节点
- `peasoft/NoMoreWalls/list.txt`：224 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub2.txt`：178 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub3.txt`：169 个节点
- `barry-far/V2ray-Config/All_Configs_base64_Sub.txt`：165 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：163 个节点
- `MatinGhanbari/v2ray-configs/subscriptions/v2ray/subs/sub39.txt`：145 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：142 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：140 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：132 个节点

## 2026-11-01 23:02

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**23** 个
- 原始提取节点：**54006** 条
- 两级去重后（完整链接 + 服务器:端口）：**3727** 条（剔除重复 45527 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 3363、xray 2981、clash 3688、singbox 3575
- 耗时：1193 秒

### TCP 延迟分布

- 可达服务器：**3727/3727**（延迟中位数 217ms，最低 27ms）
- Cloudflare 前置节点：**1167** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 386 |
| 100-300ms | 2571 |
| 300-800ms | 595 |
| >800ms | 175 |
| 不可达（排在订阅末尾） | 0 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **43** 个仓库在 README 里给出订阅链接，从中提取 **54006** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| shabane/kamaji | 10 | 13202 |
| NiREvil/vless | 10 | 13200 |
| Delta-Kronecker/V2ray-Config | 10 | 9299 |
| nyeinkokoaung404/V2ray-Configs | 10 | 7090 |
| whoahaow/rjsxrd | 10 | 3557 |
| DukeMehdi/FreeList-V2ray-Configs | 8 | 2890 |
| igareck/vpn-configs-for-russia | 10 | 1762 |
| kooker/FreeSubsCheck | 5 | 701 |
| F0rc3Run/F0rc3Run | 7 | 583 |
| chengaopan/AutoMergePublicNodes | 2 | 463 |
| peasoft/NoMoreWalls | 1 | 459 |
| crashgfw/free-airport-nodes | 10 | 300 |
| sinavm/SVM | 9 | 202 |
| snakem982/proxypool | 3 | 177 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | 2 | 34 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4488 |
| vmess | 2187 |
| trojan | 1133 |
| ss | 506 |
| hysteria2 | 164 |
| ssr | 1 |

### 输出文件

- `v2ray_sub.txt`（3363 条，base64 订阅）
- `xray_sub.txt`（2981 条，base64 订阅）
- `clash_sub.yaml`（3688 个代理）
- `singbox_sub.json`（3575 个 outbound）
- `nodes_uris.txt`（3727 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| nyeinkokoaung404/V2ray-Configs | 90.2 | 100%（1/1） | 1635ms | 41940 |
| hello-world-1989/cn-news | 42.6 | 33%（2/6） | 1790ms | 24 |
| F0rc3Run/F0rc3Run | 41.7 | 31%（21/68） | 1662ms | 2351 |
| snakem982/proxypool | 26.2 | 10%（13/128） | 1822ms | 1770 |
| sinavm/SVM | 23.1 | 11%（11/104） | 2381ms | 377 |
| whoahaow/rjsxrd | 22.2 | 5%（77/1684） | 1842ms | 14328 |
| peasoft/NoMoreWalls | 21.9 | 12%（10/85） | 2723ms | 3525 |
| NiREvil/vless | 20.6 | 2%（77/4058） | 1796ms | 70204 |
| kooker/FreeSubsCheck | 20.4 | 4%（21/518） | 2074ms | 4050 |
| shabane/kamaji | 19.8 | 6%（19/340） | 2354ms | 25310 |
| danmaifu/mianfeijiedian | 17.4 | 4%（32/895） | 2512ms | 2310 |
| Delta-Kronecker/V2ray-Config | 14.0 | 0%（7/1465） | 2726ms | 33605 |

- 本次采集优先级（质量从高到低）：nyeinkokoaung404/V2ray-Configs(可用率100%/质量90.2)、hello-world-1989/cn-news(可用率33%/质量42.6)、F0rc3Run/F0rc3Run(可用率31%/质量41.7)、peasoft/NoMoreWalls(可用率12%/质量21.9)、sinavm/SVM(可用率11%/质量23.1)、snakem982/proxypool(可用率10%/质量26.2)、shabane/kamaji(可用率6%/质量19.8)、whoahaow/rjsxrd(可用率5%/质量22.2)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119705 | 2026-11-01 |
| mack-a/v2ray-agent | ⭐22261 | 2026-11-01 |
| Pawdroid/Free-servers | ⭐19743 | 2026-11-01 |
| free-nodes/clashfree | ⭐17144 | 2026-11-01 |
| free-nodes/v2rayfree | ⭐14716 | 2026-11-01 |
| ermaozi/get_subscribe | ⭐9417 | 2026-11-01 |
| igareck/vpn-configs-for-russia | ⭐9405 | 2026-11-01 |
| chengaopan/AutoMergePublicNodes | ⭐8309 | 2026-11-01 |
| Gozargah/Marzban | ⭐7498 | 2026-11-01 |
| free18/v2ray | ⭐5821 | 2026-11-01 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5692 | 2026-11-01 |
| nguyenphutrong/quotio | ⭐4903 | 2026-11-01 |
| peasoft/NoMoreWalls | ⭐3588 | 2026-11-01 |
| Barabama/FreeNodes | ⭐3360 | 2026-11-01 |
| Alvin9999-newpac/fanqiang | ⭐3177 | 2026-11-01 |
| barry-far/V2ray-Config | ⭐2619 | 2026-11-01 |
| snakem982/proxypool | ⭐2236 | 2026-11-01 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1860 | 2026-11-01 |
| crossxx-labs/free-proxy | ⭐1856 | 2026-11-01 |
| surgioproject/surgio | ⭐1824 | 2026-11-01 |
| LancelotRar/best-cf-ips | ⭐1631 | 2026-11-01 |
| Leon406/SubCrawler | ⭐1578 | 2026-11-01 |
| everett7623/airport-recommendations-2026 | ⭐1468 | 2026-11-01 |
| jdnei/JiChangTuiJian | ⭐1437 | 2026-11-01 |
| NiREvil/vless | ⭐1362 | 2026-11-01 |
| shaoyouvip/free | ⭐1311 | 2026-11-01 |
| cfal/shoes | ⭐1284 | 2026-11-01 |
| Hidashimora/free-vpn-anti-rkn | ⭐1133 | 2026-11-01 |
| bq2015/FreeProxies | ⭐919 | 2026-11-01 |
| deezertidal/freevpn | ⭐889 | 2026-11-01 |
| whoahaow/rjsxrd | ⭐874 | 2026-11-01 |
| ermaozi01/free_clash_vpn | ⭐823 | 2026-11-01 |
| 0xRadikal/Free-v2ray-Configs | ⭐782 | 2026-11-01 |
| YuanDevTeam/OneXray | ⭐754 | 2026-11-01 |
| dongchengjie/airport | ⭐748 | 2026-11-01 |
| sylearn/AIUsage | ⭐735 | 2026-11-01 |
| ts-sf/fly | ⭐713 | 2026-11-01 |
| MatinGhanbari/v2ray-configs | ⭐694 | 2026-11-01 |
| Leadaxe/LxBox | ⭐687 | 2026-11-01 |
| gslege/CloudflareIP | ⭐678 | 2026-11-01 |
| hello-yunshu/Xray_bash_onekey | ⭐665 | 2026-11-01 |
| hello-world-1989/cn-news | ⭐644 | 2026-11-01 |
| OpenNetCN/clash | ⭐642 | 2026-11-01 |
| SoliSpirit/v2ray-configs | ⭐636 | 2026-11-01 |
| kort0881/vpn-vless-configs-russia | ⭐627 | 2026-11-01 |
| jichangtuijian-cheap/cheap-airports | ⭐619 | 2026-11-01 |
| sunmiao4458/free-proxy-airport | ⭐560 | 2026-11-01 |
| CCSH/IPTV | ⭐538 | 2026-11-01 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-01 |
| getmeridian/meridian | ⭐500 | 2026-11-01 |
| kooker/FreeSubsCheck | ⭐449 | 2026-11-01 |
| itsyebekhe/PSG | ⭐446 | 2026-11-01 |
| sinavm/SVM | ⭐444 | 2026-11-01 |
| zhuhaiuk/free-nodes | ⭐395 | 2026-11-01 |
| cbusifabcap/daily_free_vpn | ⭐383 | 2026-11-01 |
| ShatakVPN/ConfigForge-V2Ray | ⭐376 | 2026-11-01 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-01 |
| ovmvo/FreeSub | ⭐355 | 2026-11-01 |
| DevDock-AI/claude-unlimited | ⭐333 | 2026-11-01 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-01 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐322 | 2026-11-01 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-01 |
| WLget/V2Ray_configs_64 | ⭐315 | 2026-11-01 |
| clashv2ray-hub/clashfree | ⭐311 | 2026-11-01 |
| clashv2ray-hub/v2rayfree | ⭐302 | 2026-11-01 |
| crashgfw/free-airport-nodes | ⭐301 | 2026-11-01 |
| Surfboardv2ray/TGParse | ⭐294 | 2026-11-01 |
| wenxig/dongtai-sub | ⭐269 | 2026-11-01 |
| sakha1370/OpenRay | ⭐251 | 2026-11-01 |
| yanisplugg/yptun | ⭐239 | 2026-11-01 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐212 | 2026-11-01 |
| nyeinkokoaung404/V2ray-Configs | ⭐201 | 2026-11-01 |
| tglaoshiji/nodeshare | ⭐198 | 2026-11-01 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-01 |
| xyfqzy/free-nodes | ⭐192 | 2026-11-01 |
| mheidari98/.proxy | ⭐191 | 2026-11-01 |
| xOS/Config | ⭐183 | 2026-11-01 |
| HakurouKen/free-node | ⭐181 | 2026-11-01 |
| V2RayRoot/V2RayConfig | ⭐175 | 2026-11-01 |
| shabane/kamaji | ⭐173 | 2026-11-01 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：1258 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：623 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/trojan.txt`：526 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：233 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：190 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：120 个节点
- `peasoft/NoMoreWalls/list.txt`：101 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：84 个节点
- `shabane/kamaji/hub/self/tested/merged.txt`：72 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：61 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：60 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：57 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-all.txt`：46 个节点
- `DukeMehdi/FreeList-V2ray-Configs/Configs/All-DukeMehdi-Configs.txt`：35 个节点
- `snakem982/proxypool/source/v2ray-2.txt`：34 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：32 个节点
- `Delta-Kronecker/V2ray-Config/config/protocols/ss.txt`：31 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：31 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：24 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-1.txt`：20 个节点

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
