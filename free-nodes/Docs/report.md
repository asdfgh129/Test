# 免费节点采集报告（时间倒序）

> 按日期倒序累积，最新一次运行在最上面

## 2026-11-14 21:11

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**33** 个
- 原始提取节点：**196903** 条
- 两级去重后（完整链接 + 服务器:端口）：**30321** 条（剔除重复 166582 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 20812、xray 25930、clash 29859、singbox 28700
- 耗时：291 秒

### TCP 延迟分布

- 可达服务器：**0/30308**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**2210** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 30308 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **44** 个仓库在 README 里给出订阅链接，从中提取 **196903** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| rtwo2/FastNodes | 10 | 40000 |
| asgharkapk/Sub-Config-Extractor | 6 | 40000 |
| 10Dream/sub-mod | 6 | 40000 |
| sakha1370/OpenRay | 6 | 15306 |
| aviamastersgh/vpn-free-russia | 4 | 10886 |
| AmazingCoderA/PypsCFG | 6 | 10776 |
| shabane/kamaji | 6 | 10290 |
| 0xRadikal/Free-v2ray-Configs | 6 | 5308 |
| fmw86/free-proxy-pool | 4 | 3213 |
| rekt0ro/ProxyRift | 6 | 2898 |
| cheshi888/freesub-v2 | 6 | 2427 |
| R3ZARAHIMI/tg-v2ray-configs-every2h | 6 | 2052 |
| Areral/ScarletDevil | 3 | 1932 |
| whoahaow/rjsxrd | 6 | 1833 |
| bzfq21/proxy-singbox | 5 | 1803 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 17089 |
| vmess | 5483 |
| ss | 3967 |
| trojan | 3200 |
| hysteria2 | 519 |
| ssr | 50 |
| hysteria | 8 |
| tuic | 5 |

### 输出文件

- `v2ray_sub.txt`（20812 条，base64 订阅）
- `xray_sub.txt`（25930 条，base64 订阅）
- `clash_sub.yaml`（29859 个代理）
- `singbox_sub.json`（28700 个 outbound）
- `nodes_uris.txt`（30272 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| rtwo2/FastNodes | 93.5 | 100%（1/1） | 1086ms | 9157326 |
| ermaozi01/free_clash_vpn | 59.6 | 60%（158/265） | 2019ms | 1126 |
| hello-world-1989/cn-news | 53.2 | 42%（16/38） | 1044ms | 174 |
| F0rc3Run/F0rc3Run | 51.3 | 49%（18/37） | 2125ms | 19275 |
| zhuhaiuk/free-nodes | 45.8 | 38%（21/56） | 1742ms | 291 |
| LeilaoMi/AutoMergePublicNodes-Optimized | 42.8 | 33%（1/3） | 1756ms | 2505 |
| FLAT447/v2ray-lists | 41.8 | 34%（16/47） | 1997ms | 2557 |
| Areral/ScarletDevil | 39.1 | 31%（28/91） | 2075ms | 5932 |
| rekt0ro/ProxyRift | 33.9 | 23%（11/47） | 2077ms | 15349 |
| 0xRadikal/Free-v2ray-Configs | 32.4 | 19%（175/929） | 1786ms | 284185 |
| Mehinator/Derafsh | 27.4 | 14%（3/21） | 2097ms | 1500 |
| bzfq21/proxy-singbox | 26.3 | 9%（3/32） | 1719ms | 5529 |

- 本次采集优先级（质量从高到低）：rtwo2/FastNodes(分63.1/可用率100%/push1天前)、10Dream/sub-mod(分52.8/可用率0%/push1天前)、ermaozi01/free_clash_vpn(分50.2/可用率60%/push1天前)、Areral/ScarletDevil(分48.7/可用率31%/push1天前)、rekt0ro/ProxyRift(分47.8/可用率23%/push1天前)、F0rc3Run/F0rc3Run(分47.4/可用率49%/push1天前)、aviamastersgh/vpn-free-russia(分45.0/可用率0%/push1天前)、hello-world-1989/cn-news(分44.9/可用率42%/push1天前)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| rtwo2/FastNodes | ⭐104 | 2026-11-14 |
| 10Dream/sub-mod | ⭐23 | 2026-11-14 |
| ermaozi01/free_clash_vpn | ⭐835 | 2026-11-14 |
| Areral/ScarletDevil | ⭐14 | 2026-11-14 |
| rekt0ro/ProxyRift | ⭐6 | 2026-11-14 |
| F0rc3Run/F0rc3Run | ⭐324 | 2026-11-14 |
| aviamastersgh/vpn-free-russia | ⭐71 | 2026-11-14 |
| hello-world-1989/cn-news | ⭐656 | 2026-11-14 |
| 0xRadikal/Free-v2ray-Configs | ⭐867 | 2026-11-14 |
| LeilaoMi/AutoMergePublicNodes-Optimized | ⭐47 | 2026-11-14 |
| AmazingCoderA/PypsCFG | ⭐5 | 2026-11-14 |
| whoahaow/rjsxrd | ⭐890 | 2026-11-14 |
| MohammadBahemmat/V2ray-Collector | ⭐93 | 2026-11-14 |
| sakha1370/OpenRay | ⭐256 | 2026-11-14 |
| Mehinator/Derafsh | ⭐5 | 2026-11-14 |
| zhuhaiuk/free-nodes | ⭐434 | 2026-11-14 |
| bzfq21/proxy-singbox | ⭐8 | 2026-11-14 |
| VOID-Anonymity/V.O.I.D-VPN_Bypass | ⭐46 | 2026-11-14 |
| fmw86/free-proxy-pool | ⭐8 | 2026-11-14 |
| FLAT447/v2ray-lists | ⭐104 | 2026-11-13 |
| shabane/kamaji | ⭐173 | 2026-11-13 |
| cheshi888/freesub-v2 | ⭐5 | 2026-11-14 |
| Eleven1985/Scrape-By-Country | ⭐29 | 2026-11-14 |
| ProblemTheCode/SylphNet-public | ⭐15 | 2026-11-14 |
| hamedcode/port-based-v2ray-configs | ⭐140 | 2026-11-14 |
| Alirewa/V2ray-Configs | ⭐43 | 2026-11-14 |
| HamoonSoleimani/Pr0xySh4rk | ⭐7 | 2026-11-14 |
| Mokafela/Config-Finder | ⭐17 | 2026-11-14 |
| YawStar/Proxy-Hunter | ⭐11 | 2026-11-14 |
| SnapdragonLee/SystemProxy | ⭐138 | 2026-11-14 |
| cxddgtb/dljdsjq | ⭐26 | 2026-11-14 |
| Maskkost93/kizyak-vpn-4.0 | ⭐60 | 2026-11-14 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-13 |
| miladtahanian/Config-Collector | ⭐48 | 2026-11-14 |
| snakem982/proxypool | ⭐2272 | 2026-11-14 |
| Andy181-github/Autoscrapefreenodes | ⭐5 | 2026-11-14 |
| MahanKenway/Freedom-V2Ray | ⭐123 | 2026-11-14 |
| Idolvpn/Automate-V2ray-Config-Collector | ⭐16 | 2026-11-14 |
| chenzhihan1751-cyber/node-sub-zixf | ⭐8 | 2026-11-14 |
| adop1344-bot/LetoVPN_free | ⭐6 | 2026-11-14 |
| 2dust/v2rayN | ⭐120599 | 2026-11-14 |
| Arianlavi/RebeldevConfig | ⭐30 | 2026-11-14 |
| Bailin-Love/CFLark-Harmony | ⭐30 | 2026-11-14 |
| CCSH/IPTV | ⭐554 | 2026-11-14 |
| Dushnilin/tachyon-proxy | ⭐32 | 2026-11-14 |
| Efration/ZerondOne | ⭐5 | 2026-11-14 |
| Egor051/vpnbot | ⭐7 | 2026-11-14 |
| EikeiDev/remnawave-configs | ⭐10 | 2026-11-14 |
| G1oow/SubBoost-Worker-Lite | ⭐14 | 2026-11-14 |
| LalatinaHub/LatinaSub | ⭐12 | 2026-11-14 |
| LancelotRar/best-cf-ips | ⭐1668 | 2026-11-14 |
| LancelotRar/free-subs | ⭐134 | 2026-11-14 |
| MFSGA/Chimera | ⭐5 | 2026-11-14 |
| MhdiTaheri/V2rayCollector | ⭐324 | 2026-11-14 |
| Mistgate/mistgate | ⭐299 | 2026-11-14 |
| MohammadBahemmat/npvt-collector | ⭐9 | 2026-11-14 |
| Mr-Meshky/vify | ⭐56 | 2026-11-14 |
| NeuralNode-Dev/vpn | ⭐6 | 2026-11-14 |
| NezZeen/CoreShift-Release | ⭐14 | 2026-11-14 |
| OpenNetCN/clash | ⭐652 | 2026-11-14 |
| Q7DF1/XrayFA | ⭐145 | 2026-11-14 |
| R3ZARAHIMI/tg-v2ray-configs-every2h | ⭐56 | 2026-11-14 |
| RandomJackor/jichangtuijian2026 | ⭐54 | 2026-11-14 |
| Re0XIAOPA/AutoScrapeFreeNodes | ⭐118 | 2026-11-14 |
| Romaxa55/MegaV_Public | ⭐107 | 2026-11-14 |
| Saekisui/claude-p-pipeline | ⭐96 | 2026-11-14 |
| Shayanthn/V2ray-Tester-Pro | ⭐69 | 2026-11-14 |
| SpecterLogic/Drkozol | ⭐5 | 2026-11-14 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-14 |
| T3stAcc/V2Ray | ⭐19 | 2026-11-14 |
| TG-NAV/clashnode | ⭐44 | 2026-11-14 |
| TelegaVPN/free-vpn-keys | ⭐10 | 2026-11-14 |
| TheCrowCreature/v2rayExtractor | ⭐6 | 2026-11-14 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-14 |
| YuanDevTeam/OneXray | ⭐803 | 2026-11-14 |
| ZeroDeng01/sublinkPro | ⭐1754 | 2026-11-14 |
| aaANDkk/ClashConfig | ⭐13 | 2026-11-14 |
| aimalygin/xray-rust-mobile | ⭐11 | 2026-11-14 |
| asgharkapk/Sub-Config-Extractor | ⭐62 | 2026-11-14 |
| bin1site1/V2rayFree | ⭐95 | 2026-11-14 |

### 节点来源分布（去重后，前 20）

- `rtwo2/FastNodes/sub/verified_tls.txt`：8204 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/mixed/rasool083-sub.yaml`：6296 个节点
- `10Dream/sub-mod/sub/normal/mix.txt`：5919 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/rasool083-sub.yaml`：2877 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/Surfboardv2ray/TGParse/splitted/mixed.yaml`：1853 个节点
- `AmazingCoderA/PypsCFG/output/LiteBlackList.txt`：754 个节点
- `AmazingCoderA/PypsCFG/output/WhiteList.txt`：511 个节点
- `rtwo2/FastNodes/sub/verified.txt`：491 个节点
- `rtwo2/FastNodes/sub/ipv6_only.txt`：400 个节点
- `aviamastersgh/vpn-free-russia/all_configs.txt`：372 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：301 个节点
- `sakha1370/OpenRay/output/converted/all_valid_proxies_singbox_config.json`：274 个节点
- `Areral/ScarletDevil/README→scarlet-devil.vercel.app`：252 个节点
- `rtwo2/FastNodes/sub/top.txt`：237 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：223 个节点
- `AmazingCoderA/PypsCFG/output/BlackList.txt`：194 个节点
- `rtwo2/FastNodes/sub/top_ipv6.txt`：158 个节点
- `R3ZARAHIMI/tg-v2ray-configs-every2h/conf-week.txt`：139 个节点
- `rekt0ro/ProxyRift/subscriptions/all.txt`：133 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：110 个节点

## 2026-11-13 21:12

### 概览

- 扫描仓库：**108** 个
- 抓取订阅文件：**43** 个
- 原始提取节点：**166119** 条
- 两级去重后（完整链接 + 服务器:端口）：**16853** 条（剔除重复 149266 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 11828、xray 14064、clash 16645、singbox 16013
- 耗时：376 秒

### TCP 延迟分布

- 可达服务器：**0/16824**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**2004** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 16824 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **71** 个仓库在 README 里给出订阅链接，从中提取 **166119** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| Eleven1985/Scrape-By-Country | 6 | 40000 |
| 10Dream/sub-mod | 6 | 40000 |
| aviamastersgh/vpn-free-russia | 4 | 11505 |
| shabane/kamaji | 6 | 10290 |
| AmazingCoderA/PypsCFG | 6 | 9462 |
| hamedcode/port-based-v2ray-configs | 6 | 6661 |
| MahanKenway/Freedom-V2Ray | 6 | 6010 |
| 0xRadikal/Free-v2ray-Configs | 6 | 5800 |
| Andy181-github/Autoscrapefreenodes | 6 | 4384 |
| fmw86/free-proxy-pool | 4 | 3198 |
| rekt0ro/ProxyRift | 6 | 2902 |
| chenzhihan1751-cyber/node-sub-zixf | 3 | 2718 |
| cheshi888/freesub-v2 | 6 | 2379 |
| Alirewa/V2ray-Configs | 4 | 2266 |
| cxddgtb/dljdsjq | 4 | 2258 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 9181 |
| vmess | 3333 |
| ss | 2400 |
| trojan | 1492 |
| hysteria2 | 384 |
| ssr | 51 |
| hysteria | 9 |
| tuic | 3 |

### 输出文件

- `v2ray_sub.txt`（11828 条，base64 订阅）
- `xray_sub.txt`（14064 条，base64 订阅）
- `clash_sub.yaml`（16645 个代理）
- `singbox_sub.json`（16013 个 outbound）
- `nodes_uris.txt`（16798 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 47.1 | 37%（17/46） | 1461ms | 162 |
| ermaozi01/free_clash_vpn | 41.1 | 59%（125/213） | -ms | 1038 |
| zhuhaiuk/free-nodes | 40.7 | 32%（12/38） | 1908ms | 278 |
| Maskkost93/kizyak-vpn-4.0 | 33.4 | 19%（11/58） | 1647ms | 1950 |
| 0xRadikal/Free-v2ray-Configs | 32.0 | 19%（174/929） | 1844ms | 273683 |
| crashgfw/free-airport-nodes | 31.4 | 26%（29/111） | 2818ms | 6304 |
| F0rc3Run/F0rc3Run | 28.6 | 41%（20/49） | -ms | 17694 |
| shabane/kamaji | 25.5 | 5%（37/710） | 1359ms | 227312 |
| hamedcode/port-based-v2ray-configs | 24.6 | 0%（1/1317） | 916ms | 213796 |
| miladtahanian/Config-Collector | 24.4 | 2%（1/43） | 1204ms | 939 |
| igareck/vpn-configs-for-russia | 22.6 | 5%（42/814） | 1833ms | 24002 |
| jichangx/free-nodes | 21.6 | 0%（1/368） | 1439ms | 7416 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(分34.0/可用率37%/push?天前)、ermaozi01/free_clash_vpn(分32.3/可用率59%/push?天前)、zhuhaiuk/free-nodes(分31.0/可用率32%/push?天前)、Maskkost93/kizyak-vpn-4.0(分28.3/可用率19%/push?天前)、0xRadikal/Free-v2ray-Configs(分27.0/可用率19%/push?天前)、crashgfw/free-airport-nodes(分26.9/可用率26%/push?天前)、miladtahanian/Config-Collector(分25.2/可用率2%/push?天前)、F0rc3Run/F0rc3Run(分24.5/可用率41%/push?天前)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| hello-world-1989/cn-news | ⭐655 | 2026-11-13 |
| ermaozi01/free_clash_vpn | ⭐835 | 2026-11-13 |
| zhuhaiuk/free-nodes | ⭐433 | 2026-11-13 |
| Maskkost93/kizyak-vpn-4.0 | ⭐59 | 2026-11-13 |
| 0xRadikal/Free-v2ray-Configs | ⭐856 | 2026-11-13 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-13 |
| miladtahanian/Config-Collector | ⭐48 | 2026-11-13 |
| F0rc3Run/F0rc3Run | ⭐324 | 2026-11-13 |
| rekt0ro/ProxyRift | ⭐5 | 2026-11-13 |
| shabane/kamaji | ⭐173 | 2026-11-13 |
| hamedcode/port-based-v2ray-configs | ⭐139 | 2026-11-13 |
| igareck/vpn-configs-for-russia | ⭐9574 | 2026-11-13 |
| whoahaow/rjsxrd | ⭐890 | 2026-11-13 |
| 029danio/jichangfree | ⭐160 | 2026-11-13 |
| 1000ttank/free-vpn-clash-aggregator | ⭐7 | 2026-11-13 |
| 10Dream/sub-mod | ⭐23 | 2026-11-13 |
| 2dust/v2rayN | ⭐120530 | 2026-11-13 |
| 4n0nymou3/multi-proxy-config-fetcher | ⭐103 | 2026-11-13 |
| Alirewa/V2ray-Configs | ⭐43 | 2026-11-13 |
| AmazingCoderA/PypsCFG | ⭐5 | 2026-11-13 |
| Andy181-github/Autoscrapefreenodes | ⭐5 | 2026-11-13 |
| Areral/ScarletDevil | ⭐14 | 2026-11-13 |
| Arianlavi/RebeldevConfig | ⭐30 | 2026-11-13 |
| BROadmin/BROray | ⭐7 | 2026-11-13 |
| Banten-IT-Solutions/BITS-VPN-Cloudflare | ⭐28 | 2026-11-13 |
| CCSH/IPTV | ⭐552 | 2026-11-13 |
| Edsel-Rahimi/Ariston | ⭐7 | 2026-11-13 |
| Egor051/vpnbot | ⭐7 | 2026-11-13 |
| Eleven1985/Scrape-By-Country | ⭐29 | 2026-11-13 |
| FLAT447/v2ray-lists | ⭐104 | 2026-11-13 |
| G1oow/SubBoost-Worker-Lite | ⭐14 | 2026-11-13 |
| HakurouKen/free-node | ⭐179 | 2026-11-13 |
| HamoonSoleimani/Pr0xySh4rk | ⭐7 | 2026-11-13 |
| Idolvpn/Automate-V2ray-Config-Collector | ⭐16 | 2026-11-13 |
| JHC000abc/ProxyParseForSing-box | ⭐4 | 2026-11-13 |
| LalatinaHub/LatinaSub | ⭐12 | 2026-11-13 |
| LancelotRar/best-cf-ips | ⭐1665 | 2026-11-13 |
| LancelotRar/free-subs | ⭐134 | 2026-11-13 |
| LeilaoMi/AutoMergePublicNodes-Optimized | ⭐47 | 2026-11-13 |
| Lemonochka/keqdroid | ⭐168 | 2026-11-13 |
| MFSGA/Chimera | ⭐5 | 2026-11-13 |
| MahanKenway/Freedom-V2Ray | ⭐123 | 2026-11-13 |
| Maoyangui/m-ui | ⭐21 | 2026-11-13 |
| Mehinator/Derafsh | ⭐4 | 2026-11-13 |
| MhdiTaheri/V2rayCollector | ⭐324 | 2026-11-13 |
| MohammadBahemmat/V2ray-Collector | ⭐93 | 2026-11-13 |
| MohammadBahemmat/npvt-collector | ⭐9 | 2026-11-13 |
| Mokafela/Config-Finder | ⭐17 | 2026-11-13 |
| Mr-Meshky/vify | ⭐56 | 2026-11-13 |
| Nelxi/ghostly-vpn | ⭐9 | 2026-11-13 |
| NeuralNode-Dev/vpn | ⭐6 | 2026-11-13 |
| OgdenThomas/freesub | ⭐27 | 2026-11-13 |
| OpenNetCN/clash | ⭐652 | 2026-11-13 |
| ProblemTheCode/SylphNet-public | ⭐15 | 2026-11-13 |
| Romaxa55/MegaV_Public | ⭐107 | 2026-11-13 |
| Shayanthn/V2ray-Tester-Pro | ⭐69 | 2026-11-13 |
| SnapdragonLee/SystemProxy | ⭐138 | 2026-11-13 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-13 |
| T3stAcc/V2Ray | ⭐19 | 2026-11-13 |
| TG-NAV/clashnode | ⭐44 | 2026-11-13 |
| TG-NAV/nodeshare | ⭐87 | 2026-11-13 |
| TelegaVPN/free-vpn-keys | ⭐10 | 2026-11-13 |
| TheCrowCreature/v2rayExtractor | ⭐6 | 2026-11-13 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-13 |
| VOID-Anonymity/V.O.I.D-VPN_Bypass | ⭐46 | 2026-11-13 |
| VoroninaYanina/free-nodes | ⭐107 | 2026-11-13 |
| XVSVTsama/XVSVT-Clash-Config | ⭐20 | 2026-11-13 |
| Xiongdaxz/shenbi-maliang-gpt-image-workbench | ⭐40 | 2026-11-13 |
| YawStar/Proxy-Hunter | ⭐11 | 2026-11-13 |
| YuanDevTeam/OneXray | ⭐800 | 2026-11-13 |
| ZaoHub/HopWorld | ⭐8 | 2026-11-13 |
| abshare/abshare.github.io | ⭐1122 | 2026-11-13 |
| adop1344-bot/LetoVPN_free | ⭐6 | 2026-11-13 |
| aimalygin/xray-rust | ⭐42 | 2026-11-13 |
| aimalygin/xray-rust-mobile | ⭐11 | 2026-11-13 |
| andrewbakercloudscale/claude-burst | ⭐17 | 2026-11-13 |
| aviamastersgh/vpn-free-russia | ⭐70 | 2026-11-13 |
| begoniacommunity/MaterialXray | ⭐32 | 2026-11-13 |
| bgpeer/nodekit | ⭐13 | 2026-11-13 |
| bin1site1/V2rayFree | ⭐95 | 2026-11-13 |
| bzfq21/proxy-singbox | ⭐8 | 2026-11-13 |
| ch-vpn/vpn2026 | ⭐57 | 2026-11-13 |
| chaishpish/free_server_v2ray | ⭐7 | 2026-11-13 |
| chenzhihan1751-cyber/node-sub-zixf | ⭐6 | 2026-11-13 |
| cheshi888/freesub-v2 | ⭐5 | 2026-11-13 |
| clash-s/clash-s.github.io | ⭐35 | 2026-11-13 |
| clashbest/clashbest.github.io | ⭐7 | 2026-11-13 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐168 | 2026-11-13 |
| clashstash/clashstash.github.io | ⭐10 | 2026-11-13 |
| clashv2ray-hub/clashfree | ⭐316 | 2026-11-13 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐326 | 2026-11-13 |
| clashv2ray-hub/clashv2rayshare | ⭐7 | 2026-11-13 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-13 |
| clashv2rayu/clashv2rayu.github.io | ⭐27 | 2026-11-13 |
| crackbest/V2ray-Config | ⭐68 | 2026-11-13 |
| crossxx-labs/free-proxy | ⭐1866 | 2026-11-13 |
| currycan/sb-xray | ⭐14 | 2026-11-13 |
| cxddgtb/dljdsjq | ⭐26 | 2026-11-13 |
| cybersecplayground/V2Hive | ⭐7 | 2026-11-13 |
| deezertidal/fee-based | ⭐128 | 2026-11-13 |
| deezertidal/freevpn | ⭐894 | 2026-11-13 |
| ermaozi/get_subscribe | ⭐9467 | 2026-11-13 |
| fiamitaa/jichangtuijian | ⭐5 | 2026-11-13 |
| flclashnode/flclashnode.github.io | ⭐165 | 2026-11-13 |
| fmw86/free-proxy-pool | ⭐8 | 2026-11-13 |
| free-nodes/v2rayfree | ⭐15033 | 2026-11-13 |
| free-proxy-nodes/free-nodes | ⭐41 | 2026-11-13 |
| free-v2ray-node/free-v2ray-node.github.io | ⭐5 | 2026-11-13 |

### 节点来源分布（去重后，前 20）

- `10Dream/sub-mod/sub/normal/mix.txt`：7062 个节点
- `aviamastersgh/vpn-free-russia/all_configs.txt`：3230 个节点
- `MahanKenway/Freedom-V2Ray/configs/mix_sub.txt`：1251 个节点
- `Alirewa/V2ray-Configs/config.txt`：765 个节点
- `cxddgtb/dljdsjq/README→raw.githubusercontent.com`：722 个节点
- `AmazingCoderA/PypsCFG/output/WhiteList.txt`：532 个节点
- `AmazingCoderA/PypsCFG/output/LiteBlackList.txt`：435 个节点
- `F0rc3Run/F0rc3Run/Best-Results/clash.yaml`：257 个节点
- `aviamastersgh/vpn-free-russia/verified_configs.txt`：252 个节点
- `VOID-Anonymity/V.O.I.D-VPN_Bypass/url_work.txt`：222 个节点
- `AmazingCoderA/PypsCFG/output/BlackList.txt`：209 个节点
- `Eleven1985/Scrape-By-Country/configs/protocols/AllProtocols.txt`：200 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：166 个节点
- `MohammadBahemmat/V2ray-Collector/all_servers.txt`：164 个节点
- `Areral/ScarletDevil/README→scarlet-devil.vercel.app`：135 个节点
- `MahanKenway/Freedom-V2Ray/configs/vless.txt`：112 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：106 个节点
- `adop1344-bot/LetoVPN_free/checked1.txt`：96 个节点
- `Andy181-github/Autoscrapefreenodes/artifacts/subs/mihomo.yaml`：94 个节点
- `crackbest/V2ray-Config/config.txt`：79 个节点

## 2026-11-12 04:17

### 概览

- 扫描仓库：**160** 个
- 抓取订阅文件：**50** 个
- 原始提取节点：**1055702** 条
- 两级去重后（完整链接 + 服务器:端口）：**105551** 条（剔除重复 950151 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 70941、xray 73012、clash 103147、singbox 100607
- 耗时：646 秒

### TCP 延迟分布

- 可达服务器：**0/105528**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**9333** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 105528 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **79** 个仓库在 README 里给出订阅链接，从中提取 **1055702** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| rtwo2/FastNodes | 10 | 696721 |
| pog7x/vpn-configs | 10 | 133692 |
| asgharkapk/Sub-Config-Extractor | 10 | 68595 |
| SoliSpirit/v2ray-configs | 5 | 23659 |
| MustafaBaqer/VestraNet-Nodes | 6 | 18218 |
| hamedcode/port-based-v2ray-configs | 10 | 15986 |
| sakha1370/OpenRay | 10 | 14842 |
| shabane/kamaji | 10 | 12998 |
| NiREvil/vless | 10 | 11576 |
| aviamastersgh/vpn-free-russia | 4 | 10747 |
| cbusifabcap/daily_free_vpn | 10 | 9646 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8097 |
| MahanKenway/Freedom-V2Ray | 10 | 7012 |
| Hidashimora/free-vpn-anti-rkn | 10 | 3488 |
| whoahaow/rjsxrd | 10 | 3080 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 75529 |
| ss | 9399 |
| vmess | 9384 |
| trojan | 8308 |
| hysteria2 | 2326 |
| ssr | 292 |
| tuic | 243 |
| hysteria | 70 |

### 输出文件

- `v2ray_sub.txt`（70941 条，base64 订阅）
- `xray_sub.txt`（73012 条，base64 订阅）
- `clash_sub.yaml`（103147 个代理）
- `singbox_sub.json`（100607 个 outbound）
- `nodes_uris.txt`（105550 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 60.0 | 60%（150/250） | 1993ms | 958 |
| zhuhaiuk/free-nodes | 40.7 | 32%（12/38） | 1908ms | 248 |
| 0xRadikal/Free-v2ray-Configs | 31.6 | 17%（205/1197） | 1723ms | 248658 |
| hello-world-1989/cn-news | 31.6 | 45%（19/42） | -ms | 144 |
| crashgfw/free-airport-nodes | 31.4 | 26%（29/111） | 2818ms | 5600 |
| snakem982/proxypool | 31.0 | 21%（71/336） | 2290ms | 4881 |
| F0rc3Run/F0rc3Run | 28.6 | 41%（20/49） | -ms | 16114 |
| cbusifabcap/daily_free_vpn | 25.6 | 8%（19/234） | 1678ms | 192832 |
| shabane/kamaji | 25.5 | 5%（37/710） | 1359ms | 204024 |
| jichangx/free-nodes | 21.6 | 0%（1/368） | 1439ms | 6531 |
| igareck/vpn-configs-for-russia | 20.4 | 4%（29/703） | 2078ms | 21568 |
| NiREvil/vless | 19.1 | 0%（86/18719） | 1876ms | 299721 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率60%/质量60.0)、hello-world-1989/cn-news(可用率45%/质量31.6)、F0rc3Run/F0rc3Run(可用率41%/质量28.6)、zhuhaiuk/free-nodes(可用率32%/质量40.7)、crashgfw/free-airport-nodes(可用率26%/质量31.4)、snakem982/proxypool(可用率21%/质量31.0)、0xRadikal/Free-v2ray-Configs(可用率17%/质量31.6)、Pawdroid/Free-servers(可用率14%/质量9.5)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120418 | 2026-11-11 |
| mack-a/v2ray-agent | ⭐22337 | 2026-11-09 |
| Pawdroid/Free-servers | ⭐19899 | 2026-11-11 |
| DiningFactory/panda-vpn-pro | ⭐17694 | 2026-11-11 |
| free-nodes/clashfree | ⭐17272 | 2026-11-11 |
| free-nodes/v2rayfree | ⭐14991 | 2026-11-11 |
| alireza0/s-ui | ⭐10296 | 2026-11-10 |
| igareck/vpn-configs-for-russia | ⭐9549 | 2026-11-11 |
| ermaozi/get_subscribe | ⭐9459 | 2026-11-11 |
| chengaopan/AutoMergePublicNodes | ⭐8375 | 2026-11-11 |
| yonggekkk/argosbx | ⭐6071 | 2026-11-11 |
| free18/v2ray | ⭐5886 | 2026-11-11 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5731 | 2026-11-11 |
| nguyenphutrong/quotio | ⭐4914 | 2026-11-11 |
| Jsnzkpg/Jsnzkpg | ⭐4375 | 2026-11-11 |
| anaer/Sub | ⭐3684 | 2026-11-11 |
| peasoft/NoMoreWalls | ⭐3609 | 2026-11-11 |
| Barabama/FreeNodes | ⭐3409 | 2026-11-11 |
| barry-far/V2ray-Config | ⭐2673 | 2026-11-11 |
| John19187/The-40-Best-VPNs | ⭐2392 | 2026-11-09 |
| ripaojiedian/freenode | ⭐2389 | 2026-11-11 |
| KaWaIDeSuNe/dijiajichang | ⭐2286 | 2026-11-10 |
| snakem982/proxypool | ⭐2262 | 2026-11-11 |
| fscarmen/ArgoX | ⭐2081 | 2026-11-09 |
| PuddinCat/BestClash | ⭐2075 | 2026-11-11 |
| qusong0627/QuantMind | ⭐1906 | 2026-11-11 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1872 | 2026-11-11 |
| crossxx-labs/free-proxy | ⭐1865 | 2026-11-11 |
| LancelotRar/best-cf-ips | ⭐1664 | 2026-11-11 |
| jdnei/JiChangTuiJian | ⭐1659 | 2026-11-11 |
| everett7623/airport-recommendations-2026 | ⭐1507 | 2026-11-11 |
| NiREvil/vless | ⭐1374 | 2026-11-11 |
| shaoyouvip/free | ⭐1331 | 2026-11-11 |
| cfal/shoes | ⭐1306 | 2026-11-11 |
| Hidashimora/free-vpn-anti-rkn | ⭐1191 | 2026-11-09 |
| myikuns/jichangtz-tuijian | ⭐1151 | 2026-11-11 |
| deezertidal/freevpn | ⭐894 | 2026-11-11 |
| whoahaow/rjsxrd | ⭐887 | 2026-11-11 |
| pengchujin/tower | ⭐852 | 2026-11-11 |
| ermaozi01/free_clash_vpn | ⭐833 | 2026-11-11 |
| 0xRadikal/Free-v2ray-Configs | ⭐820 | 2026-11-11 |
| YuanDevTeam/OneXray | ⭐791 | 2026-11-11 |
| dongchengjie/airport | ⭐767 | 2026-11-11 |
| Leadaxe/LxBox | ⭐741 | 2026-11-10 |
| ts-sf/fly | ⭐717 | 2026-11-11 |
| MatinGhanbari/v2ray-configs | ⭐706 | 2026-11-11 |
| gslege/CloudflareIP | ⭐683 | 2026-11-11 |
| hello-yunshu/Xray_bash_onekey | ⭐671 | 2026-11-11 |
| hello-world-1989/cn-news | ⭐653 | 2026-11-11 |
| OpenNetCN/clash | ⭐652 | 2026-11-11 |
| SoliSpirit/v2ray-configs | ⭐643 | 2026-11-11 |
| kort0881/vpn-vless-configs-russia | ⭐638 | 2026-11-11 |
| jichangtuijian-cheap/cheap-airports | ⭐633 | 2026-11-10 |
| bannedbook/v2ray.vpn | ⭐614 | 2026-11-10 |
| sunmiao4458/free-proxy-airport | ⭐568 | 2026-11-11 |
| CCSH/IPTV | ⭐551 | 2026-11-11 |
| Huibq/TrojanLinks | ⭐547 | 2026-11-11 |
| tolinkshare2/tolinkshare2.github.io | ⭐539 | 2026-11-11 |
| kooker/FreeSubsCheck | ⭐456 | 2026-11-11 |
| sinavm/SVM | ⭐449 | 2026-11-11 |
| itsyebekhe/PSG | ⭐448 | 2026-11-11 |
| zhuhaiuk/free-nodes | ⭐429 | 2026-11-11 |
| cbusifabcap/daily_free_vpn | ⭐404 | 2026-11-11 |
| ShatakVPN/ConfigForge-V2Ray | ⭐382 | 2026-11-11 |
| Delta-Kronecker/V2ray-Config | ⭐372 | 2026-11-11 |
| mkshare3/mkshare3.github.io | ⭐345 | 2026-11-11 |
| Mahdi0024/ProxyCollector | ⭐331 | 2026-11-11 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐325 | 2026-11-11 |
| F0rc3Run/F0rc3Run | ⭐324 | 2026-11-11 |
| MhdiTaheri/V2rayCollector | ⭐324 | 2026-11-11 |
| clashv2ray-hub/clashfree | ⭐316 | 2026-11-11 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-11 |
| crashgfw/free-airport-nodes | ⭐304 | 2026-11-11 |
| clashv2ray-hub/v2rayfree | ⭐303 | 2026-11-11 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-11 |
| Mistgate/mistgate | ⭐292 | 2026-11-11 |
| shenaba/2s-ui | ⭐285 | 2026-11-11 |
| wenxig/dongtai-sub | ⭐279 | 2026-11-09 |
| yanisplugg/yptun | ⭐259 | 2026-11-11 |
| sakha1370/OpenRay | ⭐253 | 2026-11-11 |
| jichangx/free-nodes | ⭐252 | 2026-11-10 |
| crystalmasta/unbihex | ⭐240 | 2026-11-09 |
| Wunderlandmedia/HotkeyClash | ⭐233 | 2026-11-10 |
| xmwengxing/CFPilot | ⭐216 | 2026-11-11 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐215 | 2026-11-11 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-11 |
| tglaoshiji/nodeshare | ⭐201 | 2026-11-11 |
| iboxz/free-v2ray-collector | ⭐195 | 2026-11-11 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-11 |
| mheidari98/.proxy | ⭐193 | 2026-11-11 |
| kazeyukiro/3m-ui | ⭐192 | 2026-11-11 |
| sinavm/sing-box | ⭐189 | 2026-11-11 |
| xOS/Config | ⭐183 | 2026-11-11 |
| HakurouKen/free-node | ⭐180 | 2026-11-11 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-11 |
| shabane/kamaji | ⭐173 | 2026-11-10 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐168 | 2026-11-11 |
| Stintik-123/StintikVPN | ⭐166 | 2026-11-10 |
| junjun266/FreeProxyGo | ⭐163 | 2026-11-11 |
| mhmdxahmd/mafly | ⭐162 | 2026-11-11 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-11 |
| enriquephl/QuantumultX_config | ⭐161 | 2026-11-10 |
| 029danio/jichangfree | ⭐160 | 2026-11-11 |
| thsrite/configflow | ⭐157 | 2026-11-11 |
| Danialsamadi/v2go | ⭐156 | 2026-11-11 |
| licheng527/Free-servers | ⭐153 | 2026-11-11 |
| fafnirov/KaproTUN | ⭐153 | 2026-11-10 |
| Medium1992/mihomo-proxy-ros | ⭐152 | 2026-11-11 |
| Firmfox/Proxify | ⭐148 | 2026-11-11 |
| Q7DF1/XrayFA | ⭐145 | 2026-11-11 |
| RKPchannel/RKP_bypass_configs | ⭐143 | 2026-11-10 |
| hamedcode/port-based-v2ray-configs | ⭐139 | 2026-11-11 |
| Lemonochka/keqdroid | ⭐139 | 2026-11-11 |
| SnapdragonLee/SystemProxy | ⭐138 | 2026-11-11 |
| LancelotRar/free-subs | ⭐132 | 2026-11-11 |
| nikships/droidproxy | ⭐129 | 2026-11-11 |
| deezertidal/fee-based | ⭐128 | 2026-11-11 |
| splify2/steer | ⭐123 | 2026-11-11 |
| MahanKenway/Freedom-V2Ray | ⭐122 | 2026-11-11 |
| Re0XIAOPA/AutoScrapeFreeNodes | ⭐116 | 2026-11-11 |
| nodesfree/v2raynode | ⭐109 | 2026-11-11 |
| VoroninaYanina/free-nodes | ⭐107 | 2026-11-11 |
| Romaxa55/MegaV_Public | ⭐107 | 2026-11-11 |
| rtwo2/FastNodes | ⭐104 | 2026-11-11 |
| 4n0nymou3/multi-proxy-config-fetcher | ⭐103 | 2026-11-11 |
| mohamadfg-dev/telegram-v2ray-configs-collector | ⭐100 | 2026-11-11 |
| FLAT447/v2ray-lists | ⭐100 | 2026-11-11 |
| bin1site1/V2rayFree | ⭐95 | 2026-11-11 |
| MohammadBahemmat/V2ray-Collector | ⭐93 | 2026-11-11 |
| MustafaBaqer/VestraNet-Nodes | ⭐92 | 2026-11-11 |
| TG-NAV/nodeshare | ⭐87 | 2026-11-11 |
| queencindy927/jichangtuijian | ⭐84 | 2026-11-10 |
| nodesfree/clashnode | ⭐82 | 2026-11-11 |
| lufficc/clash-traffic | ⭐80 | 2026-11-10 |
| eishare/Xray-go | ⭐78 | 2026-11-09 |
| WLget/V2ray_free | ⭐75 | 2026-11-11 |
| toml66l/fanqiang | ⭐74 | 2026-11-11 |
| inferno1978/Chimera-Project | ⭐74 | 2026-11-11 |
| v2raynnodes/v2rayfree | ⭐74 | 2026-11-11 |
| hysteria350/free-jichang | ⭐73 | 2026-11-11 |
| krambovic/Lumen | ⭐73 | 2026-11-10 |
| nozikov/vless-relay-setup | ⭐73 | 2026-11-10 |
| jctz123/jichang-tuijian | ⭐72 | 2026-11-11 |
| fodmod-one/jichangtuijian | ⭐71 | 2026-11-10 |
| Shayanthn/V2ray-Tester-Pro | ⭐69 | 2026-11-11 |
| aviamastersgh/vpn-free-russia | ⭐68 | 2026-11-11 |
| crackbest/V2ray-Config | ⭐68 | 2026-11-11 |
| penhandev/AutoAiVPN | ⭐66 | 2026-11-11 |
| pog7x/vpn-configs | ⭐65 | 2026-11-11 |
| liangshengyong/LanWan | ⭐63 | 2026-11-11 |
| asgharkapk/Sub-Config-Extractor | ⭐62 | 2026-11-10 |
| Maskkost93/kizyak-vpn-4.0 | ⭐59 | 2026-11-11 |
| rockbenben/free-llm-intel | ⭐58 | 2026-11-11 |
| SoliSpirit/SolVPN | ⭐56 | 2026-11-11 |
| R3ZARAHIMI/tg-v2ray-configs-every2h | ⭐56 | 2026-11-11 |
| Mr-Meshky/vify | ⭐56 | 2026-11-11 |
| lanzm/MetaFetch | ⭐54 | 2026-11-11 |
| XIIIFOX/flutter_vless | ⭐54 | 2026-11-11 |
| pathetixx/190x4-Ninety | ⭐52 | 2026-11-11 |
| yy1588133/proxy-pool | ⭐49 | 2026-11-11 |

### 节点来源分布（去重后，前 20）

- `rtwo2/FastNodes/sub/ipv4_only.txt`：78625 个节点
- `pog7x/vpn-configs/githubmirror/2.txt`：13754 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/mixed/rasool083-sub.yaml`：2579 个节点
- `pog7x/vpn-configs/githubmirror/3.txt`：2160 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/rasool083-sub.yaml`：1301 个节点
- `pog7x/vpn-configs/githubmirror/10.txt`：1084 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/mixed/moneyfly1_merged_proxies_new.yaml`：996 个节点
- `rtwo2/FastNodes/sub/stable.txt`：618 个节点
- `rtwo2/FastNodes/sub/top.txt`：561 个节点
- `pog7x/vpn-configs/githubmirror/1.txt`：508 个节点
- `rtwo2/FastNodes/sub/ipv6_only.txt`：388 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/vmess.txt`：348 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/vless.txt`：312 个节点
- `rtwo2/FastNodes/sub/verified.txt`：263 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：237 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/trojan.txt`：183 个节点
- `MustafaBaqer/VestraNet-Nodes/subscriptions/mix-base64.txt`：171 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/Surfboardv2ray/TGParse/splitted/mixed.yaml`：168 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：160 个节点
- `rtwo2/FastNodes/sub/top_ipv6.txt`：94 个节点

## 2026-11-11 04:33

### 概览

- 扫描仓库：**160** 个
- 抓取订阅文件：**45** 个
- 原始提取节点：**1044406** 条
- 两级去重后（完整链接 + 服务器:端口）：**106098** 条（剔除重复 938308 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 70497、xray 74381、clash 103723、singbox 101107
- 耗时：601 秒

### TCP 延迟分布

- 可达服务器：**0/106078**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**9295** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 106078 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **74** 个仓库在 README 里给出订阅链接，从中提取 **1044406** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| rtwo2/FastNodes | 10 | 694203 |
| pog7x/vpn-configs | 10 | 132963 |
| asgharkapk/Sub-Config-Extractor | 10 | 68601 |
| SoliSpirit/v2ray-configs | 5 | 23380 |
| MustafaBaqer/VestraNet-Nodes | 6 | 17997 |
| hamedcode/port-based-v2ray-configs | 10 | 15959 |
| sakha1370/OpenRay | 10 | 14305 |
| shabane/kamaji | 10 | 12998 |
| NiREvil/vless | 10 | 11301 |
| aviamastersgh/vpn-free-russia | 4 | 10554 |
| cbusifabcap/daily_free_vpn | 10 | 9473 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8980 |
| MahanKenway/Freedom-V2Ray | 10 | 7112 |
| whoahaow/rjsxrd | 10 | 2700 |
| R3ZARAHIMI/tg-v2ray-configs-every2h | 10 | 2223 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 76520 |
| vmess | 9253 |
| ss | 9214 |
| trojan | 8161 |
| hysteria2 | 2347 |
| ssr | 290 |
| tuic | 243 |
| hysteria | 70 |

### 输出文件

- `v2ray_sub.txt`（70497 条，base64 订阅）
- `xray_sub.txt`（74381 条，base64 订阅）
- `clash_sub.yaml`（103723 个代理）
- `singbox_sub.json`（101107 个 outbound）
- `nodes_uris.txt`（106098 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 60.0 | 60%（150/250） | 1993ms | 916 |
| zhuhaiuk/free-nodes | 40.7 | 32%（12/38） | 1908ms | 240 |
| 0xRadikal/Free-v2ray-Configs | 31.6 | 17%（205/1197） | 1723ms | 240561 |
| hello-world-1989/cn-news | 31.6 | 45%（19/42） | -ms | 138 |
| crashgfw/free-airport-nodes | 31.4 | 26%（29/111） | 2818ms | 5160 |
| snakem982/proxypool | 31.0 | 21%（71/336） | 2290ms | 4702 |
| F0rc3Run/F0rc3Run | 28.6 | 41%（20/49） | -ms | 15349 |
| cbusifabcap/daily_free_vpn | 25.6 | 8%（19/234） | 1678ms | 183186 |
| shabane/kamaji | 25.5 | 5%（37/710） | 1359ms | 191026 |
| jichangx/free-nodes | 21.6 | 0%（1/368） | 1439ms | 5612 |
| igareck/vpn-configs-for-russia | 20.4 | 4%（29/703） | 2078ms | 20711 |
| NiREvil/vless | 19.1 | 0%（86/18719） | 1876ms | 288145 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率60%/质量60.0)、hello-world-1989/cn-news(可用率45%/质量31.6)、F0rc3Run/F0rc3Run(可用率41%/质量28.6)、zhuhaiuk/free-nodes(可用率32%/质量40.7)、crashgfw/free-airport-nodes(可用率26%/质量31.4)、snakem982/proxypool(可用率21%/质量31.0)、0xRadikal/Free-v2ray-Configs(可用率17%/质量31.6)、Pawdroid/Free-servers(可用率14%/质量9.5)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120343 | 2026-11-10 |
| mack-a/v2ray-agent | ⭐22330 | 2026-11-09 |
| yanue/V2rayU | ⭐20183 | 2026-11-08 |
| Pawdroid/Free-servers | ⭐19890 | 2026-11-10 |
| DiningFactory/panda-vpn-pro | ⭐17653 | 2026-11-10 |
| free-nodes/clashfree | ⭐17259 | 2026-11-10 |
| free-nodes/v2rayfree | ⭐14967 | 2026-11-10 |
| alireza0/s-ui | ⭐10291 | 2026-11-10 |
| igareck/vpn-configs-for-russia | ⭐9538 | 2026-11-10 |
| ermaozi/get_subscribe | ⭐9458 | 2026-11-10 |
| chengaopan/AutoMergePublicNodes | ⭐8367 | 2026-11-10 |
| yonggekkk/argosbx | ⭐6065 | 2026-11-09 |
| fscarmen/sing-box | ⭐6014 | 2026-11-08 |
| free18/v2ray | ⭐5884 | 2026-11-10 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5727 | 2026-11-10 |
| XTLS/REALITY | ⭐5605 | 2026-11-08 |
| nguyenphutrong/quotio | ⭐4910 | 2026-11-10 |
| Jsnzkpg/Jsnzkpg | ⭐4367 | 2026-11-09 |
| anaer/Sub | ⭐3683 | 2026-11-10 |
| peasoft/NoMoreWalls | ⭐3606 | 2026-11-10 |
| Barabama/FreeNodes | ⭐3406 | 2026-11-10 |
| barry-far/V2ray-Config | ⭐2665 | 2026-11-10 |
| lxhao61/integrated-examples | ⭐2536 | 2026-11-08 |
| ripaojiedian/freenode | ⭐2390 | 2026-11-09 |
| John19187/The-40-Best-VPNs | ⭐2368 | 2026-11-09 |
| KaWaIDeSuNe/dijiajichang | ⭐2283 | 2026-11-10 |
| snakem982/proxypool | ⭐2259 | 2026-11-10 |
| fscarmen/ArgoX | ⭐2079 | 2026-11-09 |
| PuddinCat/BestClash | ⭐2073 | 2026-11-10 |
| qusong0627/QuantMind | ⭐1905 | 2026-11-10 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1871 | 2026-11-10 |
| crossxx-labs/free-proxy | ⭐1863 | 2026-11-10 |
| LancelotRar/best-cf-ips | ⭐1660 | 2026-11-10 |
| jdnei/JiChangTuiJian | ⭐1637 | 2026-11-10 |
| everett7623/airport-recommendations-2026 | ⭐1505 | 2026-11-10 |
| nevertoday/xiaoxiaodong-vps | ⭐1491 | 2026-11-08 |
| NiREvil/vless | ⭐1373 | 2026-11-10 |
| shaoyouvip/free | ⭐1330 | 2026-11-10 |
| cfal/shoes | ⭐1303 | 2026-11-10 |
| Hidashimora/free-vpn-anti-rkn | ⭐1190 | 2026-11-09 |
| iluobei/miaomiaowu | ⭐1172 | 2026-11-08 |
| myikuns/jichangtz-tuijian | ⭐1150 | 2026-11-08 |
| deezertidal/freevpn | ⭐894 | 2026-11-10 |
| whoahaow/rjsxrd | ⭐883 | 2026-11-10 |
| pengchujin/tower | ⭐851 | 2026-11-09 |
| supvpn/supvpn | ⭐834 | 2026-11-10 |
| ermaozi01/free_clash_vpn | ⭐832 | 2026-11-10 |
| 0xRadikal/Free-v2ray-Configs | ⭐815 | 2026-11-10 |
| YuanDevTeam/OneXray | ⭐788 | 2026-11-09 |
| dongchengjie/airport | ⭐766 | 2026-11-10 |
| Leadaxe/LxBox | ⭐733 | 2026-11-10 |
| ts-sf/fly | ⭐717 | 2026-11-10 |
| MatinGhanbari/v2ray-configs | ⭐706 | 2026-11-10 |
| gslege/CloudflareIP | ⭐683 | 2026-11-10 |
| hello-yunshu/Xray_bash_onekey | ⭐671 | 2026-11-10 |
| hello-world-1989/cn-news | ⭐653 | 2026-11-10 |
| OpenNetCN/clash | ⭐651 | 2026-11-10 |
| SoliSpirit/v2ray-configs | ⭐643 | 2026-11-10 |
| kort0881/vpn-vless-configs-russia | ⭐638 | 2026-11-10 |
| jichangtuijian-cheap/cheap-airports | ⭐633 | 2026-11-10 |
| bannedbook/v2ray.vpn | ⭐607 | 2026-11-10 |
| sunmiao4458/free-proxy-airport | ⭐569 | 2026-11-10 |
| CCSH/IPTV | ⭐550 | 2026-11-10 |
| Huibq/TrojanLinks | ⭐547 | 2026-11-10 |
| tolinkshare2/tolinkshare2.github.io | ⭐538 | 2026-11-10 |
| kooker/FreeSubsCheck | ⭐456 | 2026-11-10 |
| sinavm/SVM | ⭐449 | 2026-11-10 |
| itsyebekhe/PSG | ⭐448 | 2026-11-10 |
| fev125/dstatus | ⭐423 | 2026-11-09 |
| zhuhaiuk/free-nodes | ⭐422 | 2026-11-10 |
| cbusifabcap/daily_free_vpn | ⭐404 | 2026-11-10 |
| ShatakVPN/ConfigForge-V2Ray | ⭐382 | 2026-11-10 |
| Delta-Kronecker/V2ray-Config | ⭐373 | 2026-11-10 |
| mkshare3/mkshare3.github.io | ⭐346 | 2026-11-09 |
| DevDock-AI/claude-unlimited | ⭐343 | 2026-11-09 |
| Mahdi0024/ProxyCollector | ⭐331 | 2026-11-10 |
| MhdiTaheri/V2rayCollector | ⭐325 | 2026-11-10 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐325 | 2026-11-10 |
| F0rc3Run/F0rc3Run | ⭐324 | 2026-11-10 |
| clashv2ray-hub/clashfree | ⭐317 | 2026-11-10 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-10 |
| crashgfw/free-airport-nodes | ⭐304 | 2026-11-10 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-10 |
| ghuntley/underclass | ⭐296 | 2026-11-10 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-10 |
| Mistgate/mistgate | ⭐287 | 2026-11-10 |
| shenaba/2s-ui | ⭐284 | 2026-11-10 |
| wenxig/dongtai-sub | ⭐278 | 2026-11-09 |
| yanisplugg/yptun | ⭐257 | 2026-11-10 |
| sakha1370/OpenRay | ⭐253 | 2026-11-10 |
| jichangx/free-nodes | ⭐247 | 2026-11-10 |
| crystalmasta/unbihex | ⭐238 | 2026-11-09 |
| Wunderlandmedia/HotkeyClash | ⭐233 | 2026-11-10 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐215 | 2026-11-10 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-10 |
| tglaoshiji/nodeshare | ⭐200 | 2026-11-10 |
| iboxz/free-v2ray-collector | ⭐195 | 2026-11-10 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-10 |
| mheidari98/.proxy | ⭐193 | 2026-11-10 |
| kazeyukiro/3m-ui | ⭐192 | 2026-11-10 |
| sinavm/sing-box | ⭐189 | 2026-11-08 |
| xOS/Config | ⭐183 | 2026-11-10 |
| HakurouKen/free-node | ⭐180 | 2026-11-10 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-10 |
| shabane/kamaji | ⭐173 | 2026-11-10 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐169 | 2026-11-10 |
| Stintik-123/StintikVPN | ⭐166 | 2026-11-10 |
| junjun266/FreeProxyGo | ⭐163 | 2026-11-10 |
| danmaifu/mianfeijiedian | ⭐163 | 2026-11-10 |
| mhmdxahmd/mafly | ⭐161 | 2026-11-10 |
| 029danio/jichangfree | ⭐160 | 2026-11-10 |
| thsrite/configflow | ⭐157 | 2026-11-10 |
| Danialsamadi/v2go | ⭐156 | 2026-11-10 |
| licheng527/Free-servers | ⭐153 | 2026-11-10 |
| Medium1992/mihomo-proxy-ros | ⭐152 | 2026-11-10 |
| fafnirov/KaproTUN | ⭐152 | 2026-11-10 |
| Firmfox/Proxify | ⭐148 | 2026-11-10 |
| Q7DF1/XrayFA | ⭐144 | 2026-11-10 |
| hamedcode/port-based-v2ray-configs | ⭐139 | 2026-11-10 |
| SnapdragonLee/SystemProxy | ⭐138 | 2026-11-10 |
| JohnWatsoon/WatTunnel | ⭐134 | 2026-11-08 |
| LancelotRar/free-subs | ⭐133 | 2026-11-10 |
| nikships/droidproxy | ⭐129 | 2026-11-10 |
| deezertidal/fee-based | ⭐128 | 2026-11-10 |
| Lemonochka/keqdroid | ⭐125 | 2026-11-09 |
| MahanKenway/Freedom-V2Ray | ⭐122 | 2026-11-10 |
| Re0XIAOPA/AutoScrapeFreeNodes | ⭐116 | 2026-11-10 |
| nodesfree/v2raynode | ⭐109 | 2026-11-10 |
| VoroninaYanina/free-nodes | ⭐107 | 2026-11-10 |
| Romaxa55/MegaV_Public | ⭐106 | 2026-11-10 |
| rtwo2/FastNodes | ⭐104 | 2026-11-10 |
| 4n0nymou3/multi-proxy-config-fetcher | ⭐103 | 2026-11-10 |
| FLAT447/v2ray-lists | ⭐101 | 2026-11-10 |
| mohamadfg-dev/telegram-v2ray-configs-collector | ⭐100 | 2026-11-10 |
| bin1site1/V2rayFree | ⭐95 | 2026-11-10 |
| MohammadBahemmat/V2ray-Collector | ⭐93 | 2026-11-10 |
| MustafaBaqer/VestraNet-Nodes | ⭐92 | 2026-11-10 |
| TG-NAV/nodeshare | ⭐89 | 2026-11-10 |
| queencindy927/jichangtuijian | ⭐85 | 2026-11-10 |
| nodesfree/clashnode | ⭐83 | 2026-11-10 |
| WLget/V2ray_free | ⭐75 | 2026-11-10 |
| eishare/Xray-go | ⭐75 | 2026-11-09 |
| inferno1978/Chimera-Project | ⭐74 | 2026-11-10 |
| toml66l/fanqiang | ⭐74 | 2026-11-10 |
| v2raynnodes/v2rayfree | ⭐74 | 2026-11-10 |
| hysteria350/free-jichang | ⭐73 | 2026-11-10 |
| nozikov/vless-relay-setup | ⭐73 | 2026-11-10 |
| fodmod-one/jichangtuijian | ⭐71 | 2026-11-10 |
| jctz123/jichang-tuijian | ⭐71 | 2026-11-08 |
| Shayanthn/V2ray-Tester-Pro | ⭐69 | 2026-11-10 |
| aviamastersgh/vpn-free-russia | ⭐69 | 2026-11-10 |
| crackbest/V2ray-Config | ⭐68 | 2026-11-10 |
| penhandev/AutoAiVPN | ⭐66 | 2026-11-10 |
| pog7x/vpn-configs | ⭐65 | 2026-11-10 |
| liangshengyong/LanWan | ⭐63 | 2026-11-10 |
| asgharkapk/Sub-Config-Extractor | ⭐62 | 2026-11-10 |
| Maskkost93/kizyak-vpn-4.0 | ⭐59 | 2026-11-10 |
| SoliSpirit/SolVPN | ⭐56 | 2026-11-10 |
| Mr-Meshky/vify | ⭐56 | 2026-11-10 |
| R3ZARAHIMI/tg-v2ray-configs-every2h | ⭐56 | 2026-11-10 |

### 节点来源分布（去重后，前 20）

- `rtwo2/FastNodes/sub/everything.txt`：68095 个节点
- `pog7x/vpn-configs/githubmirror/2.txt`：13267 个节点
- `rtwo2/FastNodes/sub/verified_tls.txt`：12515 个节点
- `pog7x/vpn-configs/githubmirror/3.txt`：2144 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/mixed/rasool083-sub.yaml`：2073 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/rasool083-sub.yaml`：1166 个节点
- `pog7x/vpn-configs/githubmirror/10.txt`：1121 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/mixed/moneyfly1_merged_proxies_new.yaml`：996 个节点
- `rtwo2/FastNodes/sub/top.txt`：592 个节点
- `pog7x/vpn-configs/githubmirror/1.txt`：514 个节点
- `rtwo2/FastNodes/sub/ipv6_only.txt`：422 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/vmess.txt`：324 个节点
- `rtwo2/FastNodes/sub/verified.txt`：251 个节点
- `hamedcode/port-based-v2ray-configs/sub/port_443.txt`：243 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/vless.txt`：239 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：237 个节点
- `asgharkapk/Sub-Config-Extractor/output_configs/clash/Surfboardv2ray/TGParse/splitted/mixed.yaml`：160 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：160 个节点
- `MustafaBaqer/VestraNet-Nodes/protocols/trojan.txt`：131 个节点
- `hamedcode/port-based-v2ray-configs/sub/vmess.txt`：128 个节点

## 2026-11-10 21:14

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**26** 个
- 原始提取节点：**91838** 条
- 两级去重后（完整链接 + 服务器:端口）：**9578** 条（剔除重复 82260 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 8054、xray 8252、clash 9462、singbox 9070
- 耗时：443 秒

### TCP 延迟分布

- 可达服务器：**0/9568**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1045** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 9568 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **47** 个仓库在 README 里给出订阅链接，从中提取 **91838** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23329 |
| sakha1370/OpenRay | 10 | 13698 |
| shabane/kamaji | 10 | 12998 |
| NiREvil/vless | 10 | 11393 |
| cbusifabcap/daily_free_vpn | 10 | 10440 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9264 |
| whoahaow/rjsxrd | 10 | 3039 |
| Danialsamadi/v2go | 10 | 1964 |
| danmaifu/mianfeijiedian | 2 | 1303 |
| F0rc3Run/F0rc3Run | 7 | 801 |
| igareck/vpn-configs-for-russia | 10 | 730 |
| kooker/FreeSubsCheck | 5 | 676 |
| jichangx/free-nodes | 2 | 604 |
| peasoft/NoMoreWalls | 1 | 452 |
| chengaopan/AutoMergePublicNodes | 2 | 444 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5330 |
| vmess | 2408 |
| ss | 1058 |
| trojan | 457 |
| hysteria2 | 314 |
| hysteria | 8 |
| tuic | 2 |
| ssr | 1 |

### 输出文件

- `v2ray_sub.txt`（8054 条，base64 订阅）
- `xray_sub.txt`（8252 条，base64 订阅）
- `clash_sub.yaml`（9462 个代理）
- `singbox_sub.json`（9070 个 outbound）
- `nodes_uris.txt`（9554 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 60.6 | 60%（144/240） | 1892ms | 858 |
| hello-world-1989/cn-news | 58.0 | 49%（21/43） | 1029ms | 132 |
| snakem982/proxypool | 34.4 | 21%（64/300） | 1746ms | 4534 |
| crashgfw/free-airport-nodes | 31.4 | 26%（29/111） | 2818ms | 4720 |
| F0rc3Run/F0rc3Run | 30.3 | 26%（27/103） | 3010ms | 14607 |
| 0xRadikal/Free-v2ray-Configs | 29.2 | 14%（194/1341） | 1818ms | 231581 |
| kooker/FreeSubsCheck | 26.4 | 2%（22/1449） | 780ms | 16082 |
| cbusifabcap/daily_free_vpn | 24.8 | 7%（14/198） | 1696ms | 173713 |
| danmaifu/mianfeijiedian | 23.2 | 2%（39/1793） | 1391ms | 14335 |
| igareck/vpn-configs-for-russia | 21.4 | 4%（23/583） | 1896ms | 19969 |
| whoahaow/rjsxrd | 19.5 | 2%（161/9874） | 1941ms | 70961 |
| sakha1370/OpenRay | 18.9 | 0%（1/231） | 1903ms | 183891 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率60%/质量60.6)、hello-world-1989/cn-news(可用率49%/质量58.0)、F0rc3Run/F0rc3Run(可用率26%/质量30.3)、crashgfw/free-airport-nodes(可用率26%/质量31.4)、zhuhaiuk/free-nodes(可用率26%/质量17.9)、snakem982/proxypool(可用率21%/质量34.4)、0xRadikal/Free-v2ray-Configs(可用率14%/质量29.2)、Pawdroid/Free-servers(可用率14%/质量9.5)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120326 | 2026-11-10 |
| Pawdroid/Free-servers | ⭐19882 | 2026-11-10 |
| DiningFactory/panda-vpn-pro | ⭐17634 | 2026-11-10 |
| free-nodes/clashfree | ⭐17252 | 2026-11-10 |
| free-nodes/v2rayfree | ⭐14955 | 2026-11-10 |
| igareck/vpn-configs-for-russia | ⭐9532 | 2026-11-10 |
| ermaozi/get_subscribe | ⭐9455 | 2026-11-10 |
| chengaopan/AutoMergePublicNodes | ⭐8365 | 2026-11-10 |
| free18/v2ray | ⭐5884 | 2026-11-10 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5726 | 2026-11-10 |
| peasoft/NoMoreWalls | ⭐3605 | 2026-11-10 |
| Barabama/FreeNodes | ⭐3404 | 2026-11-10 |
| barry-far/V2ray-Config | ⭐2664 | 2026-11-10 |
| KaWaIDeSuNe/dijiajichang | ⭐2280 | 2026-11-10 |
| snakem982/proxypool | ⭐2260 | 2026-11-10 |
| PuddinCat/BestClash | ⭐2072 | 2026-11-10 |
| qusong0627/QuantMind | ⭐1904 | 2026-11-10 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1871 | 2026-11-10 |
| crossxx-labs/free-proxy | ⭐1863 | 2026-11-10 |
| LancelotRar/best-cf-ips | ⭐1660 | 2026-11-10 |
| jdnei/JiChangTuiJian | ⭐1628 | 2026-11-10 |
| everett7623/airport-recommendations-2026 | ⭐1505 | 2026-11-10 |
| NiREvil/vless | ⭐1372 | 2026-11-10 |
| shaoyouvip/free | ⭐1328 | 2026-11-10 |
| deezertidal/freevpn | ⭐894 | 2026-11-10 |
| whoahaow/rjsxrd | ⭐883 | 2026-11-10 |
| supvpn/supvpn | ⭐834 | 2026-11-10 |
| ermaozi01/free_clash_vpn | ⭐832 | 2026-11-10 |
| 0xRadikal/Free-v2ray-Configs | ⭐813 | 2026-11-10 |
| dongchengjie/airport | ⭐765 | 2026-11-10 |
| ts-sf/fly | ⭐717 | 2026-11-10 |
| MatinGhanbari/v2ray-configs | ⭐706 | 2026-11-10 |
| gslege/CloudflareIP | ⭐683 | 2026-11-10 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-10 |
| OpenNetCN/clash | ⭐650 | 2026-11-10 |
| SoliSpirit/v2ray-configs | ⭐643 | 2026-11-10 |
| kort0881/vpn-vless-configs-russia | ⭐637 | 2026-11-10 |
| jichangtuijian-cheap/cheap-airports | ⭐633 | 2026-11-10 |
| bannedbook/v2ray.vpn | ⭐605 | 2026-11-10 |
| sunmiao4458/free-proxy-airport | ⭐569 | 2026-11-10 |
| CCSH/IPTV | ⭐550 | 2026-11-10 |
| tolinkshare2/tolinkshare2.github.io | ⭐538 | 2026-11-10 |
| kooker/FreeSubsCheck | ⭐456 | 2026-11-10 |
| sinavm/SVM | ⭐449 | 2026-11-10 |
| itsyebekhe/PSG | ⭐448 | 2026-11-10 |
| zhuhaiuk/free-nodes | ⭐421 | 2026-11-10 |
| cbusifabcap/daily_free_vpn | ⭐403 | 2026-11-10 |
| ShatakVPN/ConfigForge-V2Ray | ⭐382 | 2026-11-10 |
| Delta-Kronecker/V2ray-Config | ⭐373 | 2026-11-10 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐325 | 2026-11-10 |
| MhdiTaheri/V2rayCollector | ⭐324 | 2026-11-10 |
| F0rc3Run/F0rc3Run | ⭐323 | 2026-11-10 |
| clashv2ray-hub/clashfree | ⭐317 | 2026-11-10 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-10 |
| crashgfw/free-airport-nodes | ⭐304 | 2026-11-10 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-10 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-10 |
| Mistgate/mistgate | ⭐281 | 2026-11-10 |
| shenaba/2s-ui | ⭐281 | 2026-11-10 |
| sakha1370/OpenRay | ⭐253 | 2026-11-10 |
| jichangx/free-nodes | ⭐247 | 2026-11-10 |
| Wunderlandmedia/HotkeyClash | ⭐232 | 2026-11-10 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐215 | 2026-11-10 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-10 |
| tglaoshiji/nodeshare | ⭐200 | 2026-11-10 |
| iboxz/free-v2ray-collector | ⭐195 | 2026-11-10 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-10 |
| mheidari98/.proxy | ⭐193 | 2026-11-10 |
| xOS/Config | ⭐183 | 2026-11-10 |
| HakurouKen/free-node | ⭐180 | 2026-11-10 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-10 |
| shabane/kamaji | ⭐173 | 2026-11-10 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐169 | 2026-11-10 |
| danmaifu/mianfeijiedian | ⭐163 | 2026-11-10 |
| junjun266/FreeProxyGo | ⭐163 | 2026-11-10 |
| mhmdxahmd/mafly | ⭐161 | 2026-11-10 |
| 029danio/jichangfree | ⭐160 | 2026-11-10 |
| thsrite/configflow | ⭐157 | 2026-11-10 |
| Danialsamadi/v2go | ⭐156 | 2026-11-10 |
| licheng527/Free-servers | ⭐153 | 2026-11-10 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4401 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：820 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：630 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs_base64.txt`：540 个节点
- `cbusifabcap/daily_free_vpn/Z.txt`：349 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：336 个节点
- `jichangx/free-nodes/README→raw.githubusercontent.com`：224 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：213 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：204 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：199 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：173 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：146 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：144 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：120 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：115 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：114 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：95 个节点
- `shabane/kamaji/hub/self/tested/merged.txt`：74 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261110.txt`：68 个节点

## 2026-11-09 21:11

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**24** 个
- 原始提取节点：**76708** 条
- 两级去重后（完整链接 + 服务器:端口）：**9298** 条（剔除重复 67410 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 8007、xray 7992、clash 9183、singbox 8826
- 耗时：325 秒

### TCP 延迟分布

- 可达服务器：**0/9287**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1066** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 9287 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **43** 个仓库在 README 里给出订阅链接，从中提取 **76708** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23150 |
| sakha1370/OpenRay | 10 | 13613 |
| NiREvil/vless | 10 | 11233 |
| cbusifabcap/daily_free_vpn | 10 | 10462 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9778 |
| whoahaow/rjsxrd | 10 | 3038 |
| danmaifu/mianfeijiedian | 2 | 1351 |
| F0rc3Run/F0rc3Run | 7 | 783 |
| igareck/vpn-configs-for-russia | 10 | 728 |
| kooker/FreeSubsCheck | 5 | 642 |
| crashgfw/free-airport-nodes | 10 | 440 |
| peasoft/NoMoreWalls | 1 | 421 |
| chengaopan/AutoMergePublicNodes | 2 | 421 |
| sinavm/SVM | 10 | 226 |
| snakem982/proxypool | 3 | 172 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 5135 |
| vmess | 2419 |
| ss | 1048 |
| trojan | 365 |
| hysteria2 | 321 |
| hysteria | 6 |
| tuic | 2 |
| ssr | 2 |

### 输出文件

- `v2ray_sub.txt`（8007 条，base64 订阅）
- `xray_sub.txt`（7992 条，base64 订阅）
- `clash_sub.yaml`（9183 个代理）
- `singbox_sub.json`（8826 个 outbound）
- `nodes_uris.txt`（9276 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 62.0 | 51%（22/43） | 647ms | 120 |
| ermaozi01/free_clash_vpn | 56.6 | 51%（118/230） | 1551ms | 790 |
| zhuhaiuk/free-nodes | 46.2 | 38%（16/42） | 1750ms | 212 |
| F0rc3Run/F0rc3Run | 39.6 | 27%（62/226） | 1602ms | 13033 |
| crashgfw/free-airport-nodes | 35.4 | 28%（23/82） | 2373ms | 4280 |
| Pawdroid/Free-servers | 34.5 | 14%（8/59） | 844ms | 345 |
| 0xRadikal/Free-v2ray-Configs | 32.3 | 17%（222/1326） | 1559ms | 211141 |
| snakem982/proxypool | 24.1 | 10%（35/333） | 2207ms | 4180 |
| igareck/vpn-configs-for-russia | 23.0 | 2%（12/488） | 1466ms | 18482 |
| danmaifu/mianfeijiedian | 22.8 | 2%（34/1484） | 1476ms | 11729 |
| kooker/FreeSubsCheck | 20.6 | 2%（20/1364） | 1742ms | 14748 |
| NiREvil/vless | 19.7 | 1%（72/12098） | 1780ms | 253979 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率51%/质量56.6)、hello-world-1989/cn-news(可用率51%/质量62.0)、zhuhaiuk/free-nodes(可用率38%/质量46.2)、crashgfw/free-airport-nodes(可用率28%/质量35.4)、F0rc3Run/F0rc3Run(可用率27%/质量39.6)、0xRadikal/Free-v2ray-Configs(可用率17%/质量32.3)、Pawdroid/Free-servers(可用率14%/质量34.5)、snakem982/proxypool(可用率10%/质量24.1)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120259 | 2026-11-09 |
| mack-a/v2ray-agent | ⭐22315 | 2026-11-09 |
| Pawdroid/Free-servers | ⭐19873 | 2026-11-09 |
| free-nodes/clashfree | ⭐17239 | 2026-11-09 |
| free-nodes/v2rayfree | ⭐14928 | 2026-11-09 |
| igareck/vpn-configs-for-russia | ⭐9508 | 2026-11-09 |
| ermaozi/get_subscribe | ⭐9454 | 2026-11-09 |
| chengaopan/AutoMergePublicNodes | ⭐8356 | 2026-11-09 |
| yonggekkk/argosbx | ⭐6054 | 2026-11-09 |
| free18/v2ray | ⭐5879 | 2026-11-09 |
| Jsnzkpg/Jsnzkpg | ⭐4360 | 2026-11-09 |
| peasoft/NoMoreWalls | ⭐3606 | 2026-11-09 |
| Barabama/FreeNodes | ⭐3403 | 2026-11-09 |
| Alvin9999-newpac/fanqiang | ⭐3238 | 2026-11-09 |
| barry-far/V2ray-Config | ⭐2661 | 2026-11-09 |
| ripaojiedian/freenode | ⭐2389 | 2026-11-09 |
| snakem982/proxypool | ⭐2261 | 2026-11-09 |
| fscarmen/ArgoX | ⭐2077 | 2026-11-09 |
| PuddinCat/BestClash | ⭐2069 | 2026-11-09 |
| qusong0627/QuantMind | ⭐1896 | 2026-11-09 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1871 | 2026-11-09 |
| crossxx-labs/free-proxy | ⭐1862 | 2026-11-09 |
| ZeroDeng01/sublinkPro | ⭐1748 | 2026-11-09 |
| LancelotRar/best-cf-ips | ⭐1657 | 2026-11-09 |
| jdnei/JiChangTuiJian | ⭐1602 | 2026-11-09 |
| NiREvil/vless | ⭐1372 | 2026-11-09 |
| Hidashimora/free-vpn-anti-rkn | ⭐1190 | 2026-11-09 |
| deezertidal/freevpn | ⭐893 | 2026-11-09 |
| whoahaow/rjsxrd | ⭐880 | 2026-11-09 |
| pengchujin/tower | ⭐849 | 2026-11-09 |
| ermaozi01/free_clash_vpn | ⭐831 | 2026-11-09 |
| 0xRadikal/Free-v2ray-Configs | ⭐812 | 2026-11-09 |
| YuanDevTeam/OneXray | ⭐785 | 2026-11-09 |
| sylearn/AIUsage | ⭐740 | 2026-11-09 |
| Leadaxe/LxBox | ⭐728 | 2026-11-09 |
| ts-sf/fly | ⭐716 | 2026-11-09 |
| MatinGhanbari/v2ray-configs | ⭐705 | 2026-11-09 |
| gslege/CloudflareIP | ⭐683 | 2026-11-09 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-09 |
| OpenNetCN/clash | ⭐647 | 2026-11-09 |
| SoliSpirit/v2ray-configs | ⭐642 | 2026-11-09 |
| jichangtuijian-cheap/cheap-airports | ⭐633 | 2026-11-09 |
| kort0881/vpn-vless-configs-russia | ⭐630 | 2026-11-09 |
| sunmiao4458/free-proxy-airport | ⭐567 | 2026-11-09 |
| CCSH/IPTV | ⭐548 | 2026-11-09 |
| tolinkshare2/tolinkshare2.github.io | ⭐538 | 2026-11-09 |
| kooker/FreeSubsCheck | ⭐455 | 2026-11-09 |
| sinavm/SVM | ⭐449 | 2026-11-09 |
| itsyebekhe/PSG | ⭐447 | 2026-11-09 |
| zhuhaiuk/free-nodes | ⭐418 | 2026-11-09 |
| cbusifabcap/daily_free_vpn | ⭐400 | 2026-11-09 |
| ShatakVPN/ConfigForge-V2Ray | ⭐381 | 2026-11-09 |
| Delta-Kronecker/V2ray-Config | ⭐372 | 2026-11-09 |
| mkshare3/mkshare3.github.io | ⭐345 | 2026-11-09 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐325 | 2026-11-09 |
| F0rc3Run/F0rc3Run | ⭐323 | 2026-11-09 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-09 |
| clashv2ray-hub/clashfree | ⭐317 | 2026-11-09 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-09 |
| Alvin9999-newpac/Sing-Box-Plus | ⭐312 | 2026-11-09 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-09 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-09 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-09 |
| wenxig/dongtai-sub | ⭐277 | 2026-11-09 |
| Mistgate/mistgate | ⭐267 | 2026-11-09 |
| sakha1370/OpenRay | ⭐253 | 2026-11-09 |
| crystalmasta/unbihex | ⭐235 | 2026-11-09 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐215 | 2026-11-09 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-09 |
| tglaoshiji/nodeshare | ⭐200 | 2026-11-09 |
| iboxz/free-v2ray-collector | ⭐194 | 2026-11-09 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-09 |
| mheidari98/.proxy | ⭐193 | 2026-11-09 |
| xOS/Config | ⭐183 | 2026-11-09 |
| HakurouKen/free-node | ⭐180 | 2026-11-09 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-09 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐169 | 2026-11-09 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-09 |
| mhmdxahmd/mafly | ⭐160 | 2026-11-09 |
| thsrite/configflow | ⭐157 | 2026-11-09 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4443 个节点
- `sakha1370/OpenRay/output/all_valid_proxies.txt`：692 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：649 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：596 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261109.txt`：356 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：334 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：205 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：204 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：202 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：172 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：155 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：146 个节点
- `cbusifabcap/daily_free_vpn/Z.txt`：141 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：132 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：122 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：81 个节点
- `igareck/vpn-configs-for-russia/BLACK_VLESS_RUS_mobile.txt`：47 个节点
- `0xRadikal/Free-v2ray-Configs/top100.txt`：46 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-1.txt`：45 个节点

## 2026-11-08 21:11

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**24** 个
- 原始提取节点：**58551** 条
- 两级去重后（完整链接 + 服务器:端口）：**8272** 条（剔除重复 50279 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 7286、xray 7205、clash 8159、singbox 7869
- 耗时：295 秒

### TCP 延迟分布

- 可达服务器：**0/8261**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**953** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 8261 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **47** 个仓库在 README 里给出订阅链接，从中提取 **58551** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23113 |
| NiREvil/vless | 10 | 11402 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9262 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6635 |
| whoahaow/rjsxrd | 10 | 3118 |
| cbusifabcap/daily_free_vpn | 10 | 943 |
| F0rc3Run/F0rc3Run | 7 | 771 |
| kooker/FreeSubsCheck | 5 | 676 |
| igareck/vpn-configs-for-russia | 10 | 658 |
| chengaopan/AutoMergePublicNodes | 2 | 443 |
| crashgfw/free-airport-nodes | 10 | 440 |
| peasoft/NoMoreWalls | 1 | 418 |
| sinavm/SVM | 10 | 250 |
| snakem982/proxypool | 3 | 157 |
| free-nodes/clashfree | 1 | 83 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4465 |
| vmess | 2386 |
| ss | 917 |
| trojan | 322 |
| hysteria2 | 176 |
| hysteria | 5 |
| ssr | 1 |

### 输出文件

- `v2ray_sub.txt`（7286 条，base64 订阅）
- `xray_sub.txt`（7205 条，base64 订阅）
- `clash_sub.yaml`（8159 个代理）
- `singbox_sub.json`（7869 个 outbound）
- `nodes_uris.txt`（8249 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 57.9 | 49%（21/43） | 1042ms | 108 |
| ermaozi01/free_clash_vpn | 54.7 | 52%（119/231） | 1894ms | 692 |
| crashgfw/free-airport-nodes | 35.4 | 30%（15/50） | 2599ms | 3400 |
| F0rc3Run/F0rc3Run | 34.3 | 22%（63/286） | 1850ms | 11480 |
| 0xRadikal/Free-v2ray-Configs | 31.8 | 17%（233/1372） | 1685ms | 193093 |
| Pawdroid/Free-servers | 26.6 | 10%（7/70） | 1730ms | 305 |
| snakem982/proxypool | 24.1 | 7%（27/410） | 1755ms | 3848 |
| cbusifabcap/daily_free_vpn | 23.3 | 3%（21/693） | 1460ms | 139508 |
| SoliSpirit/v2ray-configs | 22.9 | 0%（8/3380） | 1200ms | 366735 |
| danmaifu/mianfeijiedian | 22.8 | 2%（34/1484） | 1476ms | 10378 |
| igareck/vpn-configs-for-russia | 22.6 | 4%（16/405） | 1698ms | 17035 |
| kooker/FreeSubsCheck | 20.9 | 1%（10/1191） | 1617ms | 13471 |

- 本次采集优先级（质量从高到低）：ermaozi01/free_clash_vpn(可用率52%/质量54.7)、hello-world-1989/cn-news(可用率49%/质量57.9)、crashgfw/free-airport-nodes(可用率30%/质量35.4)、zhuhaiuk/free-nodes(可用率26%/质量18.6)、F0rc3Run/F0rc3Run(可用率22%/质量34.3)、0xRadikal/Free-v2ray-Configs(可用率17%/质量31.8)、Pawdroid/Free-servers(可用率10%/质量26.6)、sinavm/SVM(可用率8%/质量18.7)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120187 | 2026-11-08 |
| Pawdroid/Free-servers | ⭐19857 | 2026-11-08 |
| DiningFactory/panda-vpn-pro | ⭐17555 | 2026-11-08 |
| free-nodes/clashfree | ⭐17231 | 2026-11-08 |
| free-nodes/v2rayfree | ⭐14900 | 2026-11-08 |
| igareck/vpn-configs-for-russia | ⭐9491 | 2026-11-08 |
| ermaozi/get_subscribe | ⭐9453 | 2026-11-08 |
| chengaopan/AutoMergePublicNodes | ⭐8353 | 2026-11-08 |
| fscarmen/sing-box | ⭐6002 | 2026-11-08 |
| free18/v2ray | ⭐5874 | 2026-11-08 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5720 | 2026-11-08 |
| XTLS/REALITY | ⭐5599 | 2026-11-08 |
| nguyenphutrong/quotio | ⭐4910 | 2026-11-08 |
| peasoft/NoMoreWalls | ⭐3604 | 2026-11-08 |
| Barabama/FreeNodes | ⭐3400 | 2026-11-08 |
| Alvin9999-newpac/fanqiang | ⭐3230 | 2026-11-08 |
| barry-far/V2ray-Config | ⭐2656 | 2026-11-08 |
| John19187/The-40-Best-VPNs | ⭐2331 | 2026-11-08 |
| snakem982/proxypool | ⭐2260 | 2026-11-08 |
| PuddinCat/BestClash | ⭐2068 | 2026-11-08 |
| qusong0627/QuantMind | ⭐1889 | 2026-11-08 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1869 | 2026-11-08 |
| crossxx-labs/free-proxy | ⭐1863 | 2026-11-08 |
| LancelotRar/best-cf-ips | ⭐1655 | 2026-11-08 |
| jdnei/JiChangTuiJian | ⭐1579 | 2026-11-08 |
| everett7623/airport-recommendations-2026 | ⭐1495 | 2026-11-08 |
| nevertoday/xiaoxiaodong-vps | ⭐1431 | 2026-11-08 |
| NiREvil/vless | ⭐1370 | 2026-11-08 |
| shaoyouvip/free | ⭐1324 | 2026-11-08 |
| cfal/shoes | ⭐1295 | 2026-11-08 |
| Hidashimora/free-vpn-anti-rkn | ⭐1186 | 2026-11-08 |
| deezertidal/freevpn | ⭐893 | 2026-11-08 |
| whoahaow/rjsxrd | ⭐880 | 2026-11-08 |
| ermaozi01/free_clash_vpn | ⭐830 | 2026-11-08 |
| 0xRadikal/Free-v2ray-Configs | ⭐807 | 2026-11-08 |
| YuanDevTeam/OneXray | ⭐785 | 2026-11-08 |
| dongchengjie/airport | ⭐764 | 2026-11-08 |
| ts-sf/fly | ⭐716 | 2026-11-08 |
| MatinGhanbari/v2ray-configs | ⭐705 | 2026-11-08 |
| gslege/CloudflareIP | ⭐683 | 2026-11-08 |
| hello-yunshu/Xray_bash_onekey | ⭐670 | 2026-11-08 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-08 |
| OpenNetCN/clash | ⭐646 | 2026-11-08 |
| SoliSpirit/v2ray-configs | ⭐641 | 2026-11-08 |
| kort0881/vpn-vless-configs-russia | ⭐630 | 2026-11-08 |
| sunmiao4458/free-proxy-airport | ⭐566 | 2026-11-08 |
| CCSH/IPTV | ⭐547 | 2026-11-08 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-08 |
| kooker/FreeSubsCheck | ⭐453 | 2026-11-08 |
| sinavm/SVM | ⭐449 | 2026-11-08 |
| itsyebekhe/PSG | ⭐447 | 2026-11-08 |
| zhuhaiuk/free-nodes | ⭐418 | 2026-11-08 |
| cbusifabcap/daily_free_vpn | ⭐400 | 2026-11-08 |
| ShatakVPN/ConfigForge-V2Ray | ⭐381 | 2026-11-08 |
| Delta-Kronecker/V2ray-Config | ⭐372 | 2026-11-08 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐325 | 2026-11-08 |
| F0rc3Run/F0rc3Run | ⭐323 | 2026-11-08 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-08 |
| clashv2ray-hub/clashfree | ⭐315 | 2026-11-08 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-08 |
| Alvin9999-newpac/Sing-Box-Plus | ⭐311 | 2026-11-08 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-08 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-08 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-08 |
| wenxig/dongtai-sub | ⭐277 | 2026-11-08 |
| Mistgate/mistgate | ⭐260 | 2026-11-08 |
| sakha1370/OpenRay | ⭐253 | 2026-11-08 |
| nbsklang-blip/CF-APEX | ⭐219 | 2026-11-08 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐214 | 2026-11-08 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-08 |
| tglaoshiji/nodeshare | ⭐201 | 2026-11-08 |
| iboxz/free-v2ray-collector | ⭐194 | 2026-11-08 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-08 |
| mheidari98/.proxy | ⭐193 | 2026-11-08 |
| kazeyukiro/3m-ui | ⭐191 | 2026-11-08 |
| sinavm/sing-box | ⭐188 | 2026-11-08 |
| xOS/Config | ⭐183 | 2026-11-08 |
| HakurouKen/free-node | ⭐180 | 2026-11-08 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-08 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐169 | 2026-11-08 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：2357 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：1661 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：648 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：541 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：392 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：364 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：277 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：194 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：186 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：180 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：163 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：143 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：125 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：121 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：118 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-1.txt`：68 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：67 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：45 个节点
- `crashgfw/free-airport-nodes/README→ndxy.fn0821.xyz`：44 个节点

## 2026-11-07 21:12

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**28** 个
- 原始提取节点：**109529** 条
- 两级去重后（完整链接 + 服务器:端口）：**11475** 条（剔除重复 98054 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 10201、xray 10048、clash 11346、singbox 11053
- 耗时：314 秒

### TCP 延迟分布

- 可达服务器：**0/11451**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1834** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 11451 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **45** 个仓库在 README 里给出订阅链接，从中提取 **109529** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23238 |
| barry-far/V2ray-Config | 10 | 22185 |
| shabane/kamaji | 10 | 14260 |
| NiREvil/vless | 10 | 11026 |
| cbusifabcap/daily_free_vpn | 10 | 10494 |
| 0xRadikal/Free-v2ray-Configs | 10 | 9449 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6673 |
| PuddinCat/BestClash | 10 | 3995 |
| whoahaow/rjsxrd | 10 | 2982 |
| danmaifu/mianfeijiedian | 2 | 1283 |
| F0rc3Run/F0rc3Run | 7 | 707 |
| igareck/vpn-configs-for-russia | 10 | 677 |
| kooker/FreeSubsCheck | 5 | 645 |
| crashgfw/free-airport-nodes | 10 | 440 |
| peasoft/NoMoreWalls | 1 | 427 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4269 |
| vmess | 3767 |
| ss | 2333 |
| trojan | 778 |
| hysteria2 | 311 |
| hysteria | 8 |
| ssr | 6 |
| tuic | 3 |

### 输出文件

- `v2ray_sub.txt`（10201 条，base64 订阅）
- `xray_sub.txt`（10048 条，base64 订阅）
- `clash_sub.yaml`（11346 个代理）
- `singbox_sub.json`（11053 个 outbound）
- `nodes_uris.txt`（11441 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 57.0 | 51%（22/43） | 1477ms | 96 |
| ermaozi01/free_clash_vpn | 54.6 | 49%（98/199） | 1648ms | 620 |
| crashgfw/free-airport-nodes | 45.8 | 44%（8/18） | 2544ms | 2960 |
| zhuhaiuk/free-nodes | 41.1 | 26%（12/46） | 1190ms | 174 |
| F0rc3Run/F0rc3Run | 36.3 | 25%（88/356） | 1835ms | 9984 |
| 0xRadikal/Free-v2ray-Configs | 33.8 | 17%（244/1419） | 1379ms | 175368 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 122250 |
| snakem982/proxypool | 24.6 | 7%（29/420） | 1708ms | 3538 |
| kooker/FreeSubsCheck | 24.0 | 1%（12/1246） | 1121ms | 12147 |
| NiREvil/vless | 23.2 | 0%（37/15084） | 1151ms | 209014 |
| peasoft/NoMoreWalls | 21.9 | 0%（6/1416） | 1404ms | 8881 |
| SoliSpirit/v2ray-configs | 21.0 | 0%（5/1616） | 1533ms | 320432 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率51%/质量57.0)、ermaozi01/free_clash_vpn(可用率49%/质量54.6)、crashgfw/free-airport-nodes(可用率44%/质量45.8)、zhuhaiuk/free-nodes(可用率26%/质量41.1)、F0rc3Run/F0rc3Run(可用率25%/质量36.3)、0xRadikal/Free-v2ray-Configs(可用率17%/质量33.8)、Pawdroid/Free-servers(可用率9%/质量6.4)、sinavm/SVM(可用率8%/质量18.7)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120138 | 2026-11-07 |
| Pawdroid/Free-servers | ⭐19842 | 2026-11-07 |
| free-nodes/clashfree | ⭐17213 | 2026-11-07 |
| free-nodes/v2rayfree | ⭐14873 | 2026-11-07 |
| alireza0/s-ui | ⭐10266 | 2026-11-07 |
| igareck/vpn-configs-for-russia | ⭐9482 | 2026-11-07 |
| ermaozi/get_subscribe | ⭐9446 | 2026-11-07 |
| chengaopan/AutoMergePublicNodes | ⭐8344 | 2026-11-07 |
| yonggekkk/argosbx | ⭐6047 | 2026-11-07 |
| free18/v2ray | ⭐5862 | 2026-11-07 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5718 | 2026-11-07 |
| nguyenphutrong/quotio | ⭐4910 | 2026-11-07 |
| XTLS/Xray-install | ⭐3677 | 2026-11-07 |
| peasoft/NoMoreWalls | ⭐3602 | 2026-11-07 |
| Barabama/FreeNodes | ⭐3400 | 2026-11-07 |
| Alvin9999-newpac/fanqiang | ⭐3223 | 2026-11-07 |
| barry-far/V2ray-Config | ⭐2654 | 2026-11-07 |
| snakem982/proxypool | ⭐2258 | 2026-11-07 |
| PuddinCat/BestClash | ⭐2067 | 2026-11-07 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1868 | 2026-11-07 |
| crossxx-labs/free-proxy | ⭐1861 | 2026-11-07 |
| LancelotRar/best-cf-ips | ⭐1652 | 2026-11-07 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-07 |
| jdnei/JiChangTuiJian | ⭐1569 | 2026-11-07 |
| NiREvil/vless | ⭐1368 | 2026-11-07 |
| shaoyouvip/free | ⭐1322 | 2026-11-07 |
| cfal/shoes | ⭐1293 | 2026-11-07 |
| Hidashimora/free-vpn-anti-rkn | ⭐1184 | 2026-11-07 |
| bq2015/FreeProxies | ⭐927 | 2026-11-07 |
| deezertidal/freevpn | ⭐893 | 2026-11-07 |
| whoahaow/rjsxrd | ⭐879 | 2026-11-07 |
| ermaozi01/free_clash_vpn | ⭐829 | 2026-11-07 |
| 0xRadikal/Free-v2ray-Configs | ⭐803 | 2026-11-07 |
| dongchengjie/airport | ⭐759 | 2026-11-07 |
| ts-sf/fly | ⭐715 | 2026-11-07 |
| MatinGhanbari/v2ray-configs | ⭐703 | 2026-11-07 |
| gslege/CloudflareIP | ⭐683 | 2026-11-07 |
| hello-yunshu/Xray_bash_onekey | ⭐669 | 2026-11-07 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-07 |
| OpenNetCN/clash | ⭐646 | 2026-11-07 |
| SoliSpirit/v2ray-configs | ⭐641 | 2026-11-07 |
| kort0881/vpn-vless-configs-russia | ⭐629 | 2026-11-07 |
| jichangtuijian-cheap/cheap-airports | ⭐628 | 2026-11-07 |
| sunmiao4458/free-proxy-airport | ⭐566 | 2026-11-07 |
| CCSH/IPTV | ⭐545 | 2026-11-07 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-07 |
| IvanSolis1989/Smart-Config-Kit | ⭐458 | 2026-11-07 |
| kooker/FreeSubsCheck | ⭐454 | 2026-11-07 |
| sinavm/SVM | ⭐449 | 2026-11-07 |
| itsyebekhe/PSG | ⭐447 | 2026-11-07 |
| zhuhaiuk/free-nodes | ⭐416 | 2026-11-07 |
| cbusifabcap/daily_free_vpn | ⭐397 | 2026-11-07 |
| ShatakVPN/ConfigForge-V2Ray | ⭐380 | 2026-11-07 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-07 |
| F0rc3Run/F0rc3Run | ⭐322 | 2026-11-07 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-07 |
| WLget/V2Ray_configs_64 | ⭐314 | 2026-11-07 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-07 |
| Surfboardv2ray/TGParse | ⭐295 | 2026-11-07 |
| wenxig/dongtai-sub | ⭐277 | 2026-11-07 |
| Mistgate/mistgate | ⭐258 | 2026-11-07 |
| sakha1370/OpenRay | ⭐253 | 2026-11-07 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐214 | 2026-11-07 |
| nyeinkokoaung404/V2ray-Configs | ⭐204 | 2026-11-07 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-07 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-07 |
| mheidari98/.proxy | ⭐192 | 2026-11-07 |
| v2rayclashnode/v2rayclashnode.github.io | ⭐192 | 2026-11-07 |
| kazeyukiro/3m-ui | ⭐191 | 2026-11-07 |
| xOS/Config | ⭐183 | 2026-11-07 |
| HakurouKen/free-node | ⭐180 | 2026-11-07 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-07 |
| shabane/kamaji | ⭐173 | 2026-11-07 |
| junjun266/FreeProxyGo | ⭐163 | 2026-11-07 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-07 |
| 029danio/jichangfree | ⭐159 | 2026-11-07 |
| mhmdxahmd/mafly | ⭐158 | 2026-11-07 |
| thsrite/configflow | ⭐157 | 2026-11-07 |
| licheng527/Free-servers | ⭐154 | 2026-11-07 |
| Firmfox/Proxify | ⭐147 | 2026-11-07 |

### 节点来源分布（去重后，前 20）

- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2914 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：1645 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：1638 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：839 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs.txt`：595 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261107.txt`：365 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：344 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：304 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：301 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：282 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：224 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：168 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：163 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：161 个节点
- `barry-far/V2ray-Config/All_Configs_Sub.txt`：156 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：153 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：146 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：116 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：114 个节点

## 2026-11-06 21:13

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**26** 个
- 原始提取节点：**84786** 条
- 两级去重后（完整链接 + 服务器:端口）：**11453** 条（剔除重复 73333 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 10124、xray 10002、clash 11326、singbox 11046
- 耗时：432 秒

### TCP 延迟分布

- 可达服务器：**0/11429**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1883** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 11429 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **49** 个仓库在 README 里给出订阅链接，从中提取 **84786** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 23205 |
| barry-far/V2ray-Config | 10 | 22407 |
| NiREvil/vless | 10 | 11272 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8814 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6730 |
| PuddinCat/BestClash | 10 | 4009 |
| whoahaow/rjsxrd | 10 | 3004 |
| cbusifabcap/daily_free_vpn | 10 | 1716 |
| igareck/vpn-configs-for-russia | 10 | 735 |
| F0rc3Run/F0rc3Run | 7 | 721 |
| kooker/FreeSubsCheck | 5 | 615 |
| peasoft/NoMoreWalls | 1 | 411 |
| chengaopan/AutoMergePublicNodes | 2 | 411 |
| danmaifu/mianfeijiedian | 2 | 257 |
| sinavm/SVM | 10 | 158 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4548 |
| vmess | 3779 |
| ss | 2120 |
| trojan | 743 |
| hysteria2 | 250 |
| ssr | 7 |
| hysteria | 6 |

### 输出文件

- `v2ray_sub.txt`（10124 条，base64 订阅）
- `xray_sub.txt`（10002 条，base64 订阅）
- `clash_sub.yaml`（11326 个代理）
- `singbox_sub.json`（11046 个 outbound）
- `nodes_uris.txt`（11438 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 49.5 | 43%（73/169） | 1787ms | 546 |
| crashgfw/free-airport-nodes | 45.8 | 44%（8/18） | 2544ms | 2220 |
| hello-world-1989/cn-news | 41.3 | 46%（18/39） | 3510ms | 84 |
| F0rc3Run/F0rc3Run | 38.7 | 26%（90/348） | 1567ms | 8566 |
| 0xRadikal/Free-v2ray-Configs | 34.2 | 18%（212/1169） | 1404ms | 157712 |
| snakem982/proxypool | 27.8 | 11%（53/477） | 1667ms | 3273 |
| NiREvil/vless | 25.9 | 1%（76/12122） | 753ms | 186627 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 93632 |
| igareck/vpn-configs-for-russia | 22.7 | 4%（9/210） | 1720ms | 14450 |
| peasoft/NoMoreWalls | 22.2 | 2%（27/1564） | 1492ms | 8029 |
| whoahaow/rjsxrd | 21.7 | 3%（302/10146） | 1732ms | 46535 |
| danmaifu/mianfeijiedian | 20.9 | 3%（33/1156） | 1858ms | 7754 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率46%/质量41.3)、crashgfw/free-airport-nodes(可用率44%/质量45.8)、ermaozi01/free_clash_vpn(可用率43%/质量49.5)、F0rc3Run/F0rc3Run(可用率26%/质量38.7)、zhuhaiuk/free-nodes(可用率23%/质量18.5)、0xRadikal/Free-v2ray-Configs(可用率18%/质量34.2)、snakem982/proxypool(可用率11%/质量27.8)、xyfqzy/free-nodes(可用率10%/质量7.0)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐120058 | 2026-11-06 |
| Pawdroid/Free-servers | ⭐19835 | 2026-11-06 |
| free-nodes/clashfree | ⭐17200 | 2026-11-06 |
| free-nodes/v2rayfree | ⭐14842 | 2026-11-06 |
| igareck/vpn-configs-for-russia | ⭐9471 | 2026-11-06 |
| ermaozi/get_subscribe | ⭐9442 | 2026-11-06 |
| chengaopan/AutoMergePublicNodes | ⭐8338 | 2026-11-06 |
| free18/v2ray | ⭐5857 | 2026-11-06 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5710 | 2026-11-06 |
| peasoft/NoMoreWalls | ⭐3600 | 2026-11-06 |
| Barabama/FreeNodes | ⭐3393 | 2026-11-06 |
| Alvin9999-newpac/fanqiang | ⭐3213 | 2026-11-06 |
| barry-far/V2ray-Config | ⭐2645 | 2026-11-06 |
| ripaojiedian/freenode | ⭐2386 | 2026-11-06 |
| snakem982/proxypool | ⭐2254 | 2026-11-06 |
| PuddinCat/BestClash | ⭐2064 | 2026-11-06 |
| qusong0627/QuantMind | ⭐1880 | 2026-11-06 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1865 | 2026-11-06 |
| crossxx-labs/free-proxy | ⭐1858 | 2026-11-06 |
| ZeroDeng01/sublinkPro | ⭐1743 | 2026-11-06 |
| LancelotRar/best-cf-ips | ⭐1647 | 2026-11-06 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-06 |
| jdnei/JiChangTuiJian | ⭐1546 | 2026-11-06 |
| everett7623/airport-recommendations-2026 | ⭐1490 | 2026-11-06 |
| nevertoday/xiaoxiaodong-vps | ⭐1382 | 2026-11-06 |
| NiREvil/vless | ⭐1366 | 2026-11-06 |
| shaoyouvip/free | ⭐1320 | 2026-11-06 |
| cfal/shoes | ⭐1293 | 2026-11-06 |
| Hidashimora/free-vpn-anti-rkn | ⭐1179 | 2026-11-06 |
| bq2015/FreeProxies | ⭐926 | 2026-11-06 |
| deezertidal/freevpn | ⭐893 | 2026-11-06 |
| whoahaow/rjsxrd | ⭐876 | 2026-11-06 |
| ermaozi01/free_clash_vpn | ⭐828 | 2026-11-06 |
| 0xRadikal/Free-v2ray-Configs | ⭐799 | 2026-11-06 |
| YuanDevTeam/OneXray | ⭐772 | 2026-11-06 |
| dongchengjie/airport | ⭐757 | 2026-11-06 |
| Leadaxe/LxBox | ⭐714 | 2026-11-06 |
| ts-sf/fly | ⭐714 | 2026-11-06 |
| MatinGhanbari/v2ray-configs | ⭐701 | 2026-11-06 |
| gslege/CloudflareIP | ⭐683 | 2026-11-06 |
| hello-yunshu/Xray_bash_onekey | ⭐669 | 2026-11-06 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-06 |
| OpenNetCN/clash | ⭐645 | 2026-11-06 |
| SoliSpirit/v2ray-configs | ⭐640 | 2026-11-06 |
| kort0881/vpn-vless-configs-russia | ⭐629 | 2026-11-06 |
| sunmiao4458/free-proxy-airport | ⭐567 | 2026-11-06 |
| CCSH/IPTV | ⭐545 | 2026-11-06 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-06 |
| kooker/FreeSubsCheck | ⭐453 | 2026-11-06 |
| sinavm/SVM | ⭐446 | 2026-11-06 |
| itsyebekhe/PSG | ⭐446 | 2026-11-06 |
| zhuhaiuk/free-nodes | ⭐412 | 2026-11-06 |
| cbusifabcap/daily_free_vpn | ⭐394 | 2026-11-06 |
| ShatakVPN/ConfigForge-V2Ray | ⭐379 | 2026-11-06 |
| Delta-Kronecker/V2ray-Config | ⭐371 | 2026-11-06 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐324 | 2026-11-06 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-06 |
| F0rc3Run/F0rc3Run | ⭐322 | 2026-11-06 |
| WLget/V2Ray_configs_64 | ⭐313 | 2026-11-06 |
| clashv2ray-hub/clashfree | ⭐313 | 2026-11-06 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-06 |
| clashv2ray-hub/v2rayfree | ⭐305 | 2026-11-06 |
| Surfboardv2ray/TGParse | ⭐292 | 2026-11-06 |
| wenxig/dongtai-sub | ⭐275 | 2026-11-06 |
| sakha1370/OpenRay | ⭐253 | 2026-11-06 |
| Mistgate/mistgate | ⭐250 | 2026-11-06 |
| crystalmasta/unbihex | ⭐227 | 2026-11-06 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐214 | 2026-11-06 |
| nyeinkokoaung404/V2ray-Configs | ⭐203 | 2026-11-06 |
| tglaoshiji/nodeshare | ⭐200 | 2026-11-06 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-06 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-06 |
| mheidari98/.proxy | ⭐192 | 2026-11-06 |
| xOS/Config | ⭐183 | 2026-11-06 |
| HakurouKen/free-node | ⭐179 | 2026-11-06 |
| V2RayRoot/V2RayConfig | ⭐178 | 2026-11-06 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐167 | 2026-11-06 |
| flclashnode/flclashnode.github.io | ⭐163 | 2026-11-06 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-06 |
| mhmdxahmd/mafly | ⭐157 | 2026-11-06 |

### 节点来源分布（去重后，前 20）

- `NiREvil/vless/README→raw.githubusercontent.com`：4807 个节点
- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2932 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：653 个节点
- `0xRadikal/Free-v2ray-Configs/verified/configs_base64.txt`：611 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `F0rc3Run/F0rc3Run/splitted-by-protocol/shadowsocks.txt`：201 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：178 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：173 个节点
- `peasoft/NoMoreWalls/list.txt`：169 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：151 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-3.txt`：143 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：143 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：137 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：134 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-2.txt`：130 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261106.txt`：114 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-all.txt`：99 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：92 个节点
- `cbusifabcap/daily_free_vpn/sub/ClashMeta.yml`：56 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：48 个节点

## 2026-11-05 21:14

### 概览

- 扫描仓库：**80** 个
- 抓取订阅文件：**28** 个
- 原始提取节点：**102444** 条
- 两级去重后（完整链接 + 服务器:端口）：**12165** 条（剔除重复 90279 条）
- 各内核可处理节点数（按协议/传输/加密分流）：v2ray 10661、xray 10363、clash 12034、singbox 11760
- 耗时：517 秒

### TCP 延迟分布

- 可达服务器：**0/12143**（延迟中位数 Nonems，最低 Nonems）
- Cloudflare 前置节点：**1919** 条（TCP 握手快但代理多不通，已整体排在真实节点之后）

| 延迟区间 | 节点数 |
|---|---|
| <100ms | 0 |
| 100-300ms | 0 |
| 300-800ms | 0 |
| >800ms | 0 |
| 不可达（排在订阅末尾） | 12143 |

> 订阅文件已按 TCP 握手延迟升序排列：低延迟节点在最前面，客户端测速/选路时优先命中。

### README 订阅链接采集

共 **52** 个仓库在 README 里给出订阅链接，从中提取 **102444** 条节点。

| 仓库 | 声明链接数 | 提取节点数 |
|---|---|---|
| SoliSpirit/v2ray-configs | 5 | 22849 |
| barry-far/V2ray-Config | 10 | 22184 |
| NiREvil/vless | 10 | 11183 |
| cbusifabcap/daily_free_vpn | 10 | 9505 |
| 0xRadikal/Free-v2ray-Configs | 10 | 8861 |
| Delta-Kronecker/V2ray-Config | 10 | 7021 |
| nyeinkokoaung404/V2ray-Configs | 10 | 6664 |
| PuddinCat/BestClash | 10 | 4046 |
| whoahaow/rjsxrd | 10 | 3145 |
| Danialsamadi/v2go | 10 | 1490 |
| danmaifu/mianfeijiedian | 2 | 1413 |
| Firmfox/Proxify | 10 | 976 |
| kooker/FreeSubsCheck | 5 | 692 |
| F0rc3Run/F0rc3Run | 7 | 610 |
| peasoft/NoMoreWalls | 1 | 467 |

### 协议分布

| 协议 | 数量 |
|---|---|
| vless | 4556 |
| vmess | 3770 |
| ss | 2172 |
| trojan | 1296 |
| hysteria2 | 354 |
| hysteria | 9 |
| ssr | 6 |
| tuic | 2 |

### 输出文件

- `v2ray_sub.txt`（10661 条，base64 订阅）
- `xray_sub.txt`（10363 条，base64 订阅）
- `clash_sub.yaml`（12034 个代理）
- `singbox_sub.json`（11760 个 outbound）
- `nodes_uris.txt`（12152 条，内部主清单，验证阶段的输入）
- `nodes_meta.json`（节点 TCP 延迟 + 来源仓库）

### 仓库质量排行（历史四内核实测）

| 仓库 | 质量分 | 实测可用率 | 平均延迟 | 累计贡献 |
|---|---|---|---|---|
| hello-world-1989/cn-news | 54.9 | 45%（17/38） | 1068ms | 72 |
| crashgfw/free-airport-nodes | 45.8 | 44%（8/18） | 2544ms | 2220 |
| xyfqzy/free-nodes | 40.6 | 25%（1/4） | 1144ms | 65 |
| F0rc3Run/F0rc3Run | 40.1 | 29%（104/360） | 1684ms | 7144 |
| zhuhaiuk/free-nodes | 38.3 | 25%（9/36） | 1536ms | 145 |
| 0xRadikal/Free-v2ray-Configs | 35.0 | 22%（183/841） | 1704ms | 140626 |
| shabane/kamaji | 25.4 | 6%（36/595） | 1473ms | 79274 |
| ermaozi01/free_clash_vpn | 25.0 | 36%（46/129） | -ms | 476 |
| snakem982/proxypool | 24.9 | 11%（61/541） | 2176ms | 2984 |
| whoahaow/rjsxrd | 22.5 | 4%（348/9908） | 1662ms | 40553 |
| NiREvil/vless | 22.2 | 1%（151/15758） | 1417ms | 164293 |
| kooker/FreeSubsCheck | 21.3 | 2%（30/1674） | 1654ms | 9551 |

- 本次采集优先级（质量从高到低）：hello-world-1989/cn-news(可用率45%/质量54.9)、crashgfw/free-airport-nodes(可用率44%/质量45.8)、ermaozi01/free_clash_vpn(可用率36%/质量25.0)、F0rc3Run/F0rc3Run(可用率29%/质量40.1)、zhuhaiuk/free-nodes(可用率25%/质量38.3)、xyfqzy/free-nodes(可用率25%/质量40.6)、0xRadikal/Free-v2ray-Configs(可用率22%/质量35.0)、snakem982/proxypool(可用率11%/质量24.9)

### 当天接触到的仓库

| 仓库 | Stars | 最近推送 |
|---|---|---|
| 2dust/v2rayN | ⭐119984 | 2026-11-05 |
| Pawdroid/Free-servers | ⭐19822 | 2026-11-05 |
| free-nodes/clashfree | ⭐17181 | 2026-11-05 |
| free-nodes/v2rayfree | ⭐14815 | 2026-11-05 |
| igareck/vpn-configs-for-russia | ⭐9441 | 2026-11-05 |
| ermaozi/get_subscribe | ⭐9438 | 2026-11-05 |
| chengaopan/AutoMergePublicNodes | ⭐8329 | 2026-11-05 |
| free18/v2ray | ⭐5853 | 2026-11-05 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | ⭐5710 | 2026-11-05 |
| Jsnzkpg/Jsnzkpg | ⭐4352 | 2026-11-05 |
| peasoft/NoMoreWalls | ⭐3596 | 2026-11-05 |
| Barabama/FreeNodes | ⭐3386 | 2026-11-05 |
| Alvin9999-newpac/fanqiang | ⭐3207 | 2026-11-05 |
| barry-far/V2ray-Config | ⭐2636 | 2026-11-05 |
| snakem982/proxypool | ⭐2248 | 2026-11-05 |
| PuddinCat/BestClash | ⭐2062 | 2026-11-05 |
| qusong0627/QuantMind | ⭐1873 | 2026-11-05 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | ⭐1864 | 2026-11-05 |
| crossxx-labs/free-proxy | ⭐1858 | 2026-11-05 |
| LancelotRar/best-cf-ips | ⭐1641 | 2026-11-05 |
| Leon406/SubCrawler | ⭐1580 | 2026-11-05 |
| jdnei/JiChangTuiJian | ⭐1525 | 2026-11-05 |
| NiREvil/vless | ⭐1366 | 2026-11-05 |
| shaoyouvip/free | ⭐1318 | 2026-11-05 |
| cfal/shoes | ⭐1289 | 2026-11-05 |
| Hidashimora/free-vpn-anti-rkn | ⭐1178 | 2026-11-05 |
| bq2015/FreeProxies | ⭐924 | 2026-11-05 |
| deezertidal/freevpn | ⭐892 | 2026-11-05 |
| whoahaow/rjsxrd | ⭐875 | 2026-11-05 |
| ermaozi01/free_clash_vpn | ⭐826 | 2026-11-05 |
| 0xRadikal/Free-v2ray-Configs | ⭐796 | 2026-11-05 |
| YuanDevTeam/OneXray | ⭐766 | 2026-11-05 |
| dongchengjie/airport | ⭐752 | 2026-11-05 |
| ts-sf/fly | ⭐714 | 2026-11-05 |
| Leadaxe/LxBox | ⭐710 | 2026-11-05 |
| MatinGhanbari/v2ray-configs | ⭐700 | 2026-11-05 |
| gslege/CloudflareIP | ⭐681 | 2026-11-05 |
| hello-yunshu/Xray_bash_onekey | ⭐670 | 2026-11-05 |
| hello-world-1989/cn-news | ⭐652 | 2026-11-05 |
| OpenNetCN/clash | ⭐643 | 2026-11-05 |
| SoliSpirit/v2ray-configs | ⭐639 | 2026-11-05 |
| kort0881/vpn-vless-configs-russia | ⭐627 | 2026-11-05 |
| sunmiao4458/free-proxy-airport | ⭐567 | 2026-11-05 |
| CCSH/IPTV | ⭐544 | 2026-11-05 |
| tolinkshare2/tolinkshare2.github.io | ⭐536 | 2026-11-05 |
| kooker/FreeSubsCheck | ⭐453 | 2026-11-05 |
| itsyebekhe/PSG | ⭐446 | 2026-11-05 |
| sinavm/SVM | ⭐445 | 2026-11-05 |
| zhuhaiuk/free-nodes | ⭐407 | 2026-11-05 |
| cbusifabcap/daily_free_vpn | ⭐393 | 2026-11-05 |
| ShatakVPN/ConfigForge-V2Ray | ⭐378 | 2026-11-05 |
| Delta-Kronecker/V2ray-Config | ⭐369 | 2026-11-05 |
| clashv2ray-hub/clashv2ray-hub.github.io | ⭐324 | 2026-11-05 |
| MhdiTaheri/V2rayCollector | ⭐322 | 2026-11-05 |
| F0rc3Run/F0rc3Run | ⭐321 | 2026-11-05 |
| clashv2ray-hub/clashfree | ⭐313 | 2026-11-05 |
| WLget/V2Ray_configs_64 | ⭐312 | 2026-11-05 |
| crashgfw/free-airport-nodes | ⭐305 | 2026-11-05 |
| clashv2ray-hub/v2rayfree | ⭐304 | 2026-11-05 |
| Surfboardv2ray/TGParse | ⭐293 | 2026-11-05 |
| shenaba/2s-ui | ⭐273 | 2026-11-05 |
| wenxig/dongtai-sub | ⭐273 | 2026-11-05 |
| sakha1370/OpenRay | ⭐252 | 2026-11-05 |
| DukeMehdi/FreeList-V2ray-Configs | ⭐213 | 2026-11-05 |
| nyeinkokoaung404/V2ray-Configs | ⭐203 | 2026-11-05 |
| tglaoshiji/nodeshare | ⭐199 | 2026-11-05 |
| xyfqzy/free-nodes | ⭐194 | 2026-11-05 |
| iboxz/free-v2ray-collector | ⭐192 | 2026-11-05 |
| mheidari98/.proxy | ⭐192 | 2026-11-05 |
| xOS/Config | ⭐183 | 2026-11-05 |
| freev2rayclash/freev2rayclash.github.io | ⭐180 | 2026-11-05 |
| HakurouKen/free-node | ⭐179 | 2026-11-05 |
| V2RayRoot/V2RayConfig | ⭐177 | 2026-11-05 |
| clashnodev2ray/clashnodev2ray.github.io | ⭐167 | 2026-11-05 |
| junjun266/FreeProxyGo | ⭐163 | 2026-11-05 |
| danmaifu/mianfeijiedian | ⭐162 | 2026-11-05 |
| mhmdxahmd/mafly | ⭐157 | 2026-11-05 |
| Danialsamadi/v2go | ⭐155 | 2026-11-05 |
| licheng527/Free-servers | ⭐153 | 2026-11-05 |
| Firmfox/Proxify | ⭐147 | 2026-11-05 |

### 节点来源分布（去重后，前 20）

- `PuddinCat/BestClash/README→raw.githubusercontent.com`：2978 个节点
- `NiREvil/vless/README→raw.githubusercontent.com`：2290 个节点
- `nyeinkokoaung404/V2ray-Configs/All_Configs_Sub.txt`：1643 个节点
- `0xRadikal/Free-v2ray-Configs/verified/clash.yaml`：643 个节点
- `Delta-Kronecker/V2ray-Config/config/all_configs.txt`：596 个节点
- `SoliSpirit/v2ray-configs/Protocols/ss.txt`：516 个节点
- `danmaifu/mianfeijiedian/feed/v2ray-20261105.txt`：392 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub1.txt`：343 个节点
- `nyeinkokoaung404/V2ray-Configs/Sub2.txt`：293 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-9.txt`：211 个节点
- `kooker/FreeSubsCheck/kooker.jp.txt`：205 个节点
- `SoliSpirit/v2ray-configs/Protocols/vless.txt`：199 个节点
- `F0rc3Run/F0rc3Run/Best-Results/proxies.txt`：188 个节点
- `peasoft/NoMoreWalls/list.txt`：188 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-4.txt`：167 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-8.txt`：155 个节点
- `SoliSpirit/v2ray-configs/Protocols/trojan.txt`：153 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-7.txt`：132 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-6.txt`：123 个节点
- `whoahaow/rjsxrd/githubmirror/bypass/bypass-5.txt`：121 个节点

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
