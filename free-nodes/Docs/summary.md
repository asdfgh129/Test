# 节点可用性验证汇总（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

## 2026-10-27 23:21

- 预筛：TCP 连通 6772/16620 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 12
- 测试策略：全量——候选 ≤ 3000 个全部测试；超过则只测排序前 3000 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；网络类失败复测 1 次；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：44.6 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 1584 | 54 | 3.5% | 3 | 23 | 1504 | 截断（上限 3000） | `nodes/available_v2ray.txt` |

> **本轮未跑完**（墙钟预算到期主动收尾或分窗口续跑，不是失败）：未开始：xray、clash、singbox；中途截断：v2ray（1584/3005）。已测结果全部有效且已落盘，剩余部分下次运行用 `--cores` + `--resume-tested` 接着测。

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | TLS 握手失败（证书/协议不匹配） | 1176 |
| v2ray | 连接超时 | 328 |
| v2ray | 配置被内核拒绝（参数不符） | 23 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 3 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 89 | 41 | 13 | `pool/pool_v2ray.txt` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 1 | 1 | 100% | 8863ms | 70.0 |
| Pawdroid/Free-servers | 7 | 3 | 43% | 2968ms | 42.2 |
| 0xRadikal/Free-v2ray-Configs | 43 | 17 | 40% | 1093ms | 51.1 |
| Danialsamadi/v2go | 23 | 9 | 39% | 2538ms | 42.2 |
| snakem982/proxypool | 29 | 6 | 21% | 1333ms | 36.5 |
| kooker/FreeSubsCheck | 12 | 2 | 17% | 776ms | 37.0 |
| peasoft/NoMoreWalls | 117 | 11 | 9% | 2190ms | 23.4 |
| Barabama/FreeNodes | 38 | 1 | 3% | 7454ms | 1.8 |
| barry-far/V2ray-Config | 39 | 1 | 3% | 12385ms | 1.8 |
| nyeinkokoaung404/V2ray-Configs | 653 | 3 | 0% | 4858ms | 1.2 |
| Epodonios/v2ray-configs | 9 | 0 | 0% | -ms | 0.0 |
| Hidashimora/free-vpn-anti-rkn | 125 | 0 | 0% | -ms | 0.0 |
| iboxz/free-v2ray-collector | 2 | 0 | 0% | -ms | 0.0 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 1 | 0 | 0% | -ms | 0.0 |
| liketolivefree/kobabi | 485 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（54 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `146.190.157.232:39644` | ss | 651ms | 0xRadikal/Free-v2ray-Configs |
| `89.125.70.179:8388` | ss | 705ms | kooker/FreeSubsCheck |
| `24.199.106.240:9998` | trojan | 768ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:36812` | vmess | 770ms | snakem982/proxypool |
| `45.32.140.119:9304` | trojan | 801ms | 0xRadikal/Free-v2ray-Configs |
| `164.92.73.218:8931` | trojan | 808ms | Danialsamadi/v2go |
| `137.184.178.208:4804` | trojan | 814ms | Danialsamadi/v2go |
| `45.32.135.70:9213` | trojan | 814ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.232.6:4853` | trojan | 818ms | 0xRadikal/Free-v2ray-Configs |
| `149.28.214.139:7604` | trojan | 818ms | 0xRadikal/Free-v2ray-Configs |
| `209.38.66.47:6105` | trojan | 830ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.203.237:6022` | trojan | 837ms | Danialsamadi/v2go |
| `144.126.223.93:8911` | trojan | 843ms | Danialsamadi/v2go |
| `177.202.111.20:56137` | ss | 846ms | kooker/FreeSubsCheck |
| `66.163.114.132:443` | trojan | 855ms | 0xRadikal/Free-v2ray-Configs |
| `64.23.151.246:7801` | trojan | 867ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.234.144:8563` | trojan | 902ms | 0xRadikal/Free-v2ray-Configs |
| `216.152.156.42:443` | trojan | 903ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 946ms | Pawdroid/Free-servers |
| `66.163.114.106:443` | trojan | 946ms | 0xRadikal/Free-v2ray-Configs |
| `216.152.156.49:443` | trojan | 959ms | 0xRadikal/Free-v2ray-Configs |
| `66.163.114.114:443` | trojan | 968ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 988ms | snakem982/proxypool |
| `202.50.253.18:19999` | ss | 990ms | peasoft/NoMoreWalls |
| `216.152.156.65:443` | trojan | 998ms | peasoft/NoMoreWalls |
| `91.206.92.238:18443` | ss | 1017ms | peasoft/NoMoreWalls |
| `216.152.156.81:443` | trojan | 1044ms | 0xRadikal/Free-v2ray-Configs |
| `64.83.20.73:8388` | ss | 1177ms | 0xRadikal/Free-v2ray-Configs |
| `64.176.163.182:443` | trojan | 1333ms | 0xRadikal/Free-v2ray-Configs |
| `177.202.111.21:56137` | ss | 1689ms | peasoft/NoMoreWalls |
| `47.250.84.25:443` | trojan | 1754ms | peasoft/NoMoreWalls |
| `31.185.105.12:443` | hysteria2 | 1782ms | 0xRadikal/Free-v2ray-Configs |
| `renderer-bridge-1-881.mirra.now:443` | vless | 1813ms | peasoft/NoMoreWalls |
| `202.50.253.90:19999` | ss | 1969ms | peasoft/NoMoreWalls |
| `8.6.112.206:443` | trojan | 2052ms | Danialsamadi/v2go |
| `www.qarvian.ir:443` | vless | 2179ms | snakem982/proxypool |
| `146.75.59.186:443` | vless | 2192ms | snakem982/proxypool |
| `suq.deev-guard.ir:15470` | ss | 2206ms | Danialsamadi/v2go |
| `201.24.121.243:443` | vless | 2316ms | peasoft/NoMoreWalls |
| `172.64.229.21:443` | vmess | 2361ms | nyeinkokoaung404/V2ray-Configs |
| … | 共 54 个 | | |

## 2026-10-25 09:02

- 预筛：TCP 连通 4776/12993 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 12
- 测试策略：全量——候选 ≤ 3000 个全部测试；超过则只测排序前 1000 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；网络类失败复测 1 次；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：51.5 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 1000 | 32 | 3.3% | 3 | 17 | 948 | 截断（上限 1000） | `nodes/available_v2ray.txt` |
| xray | 1000 | 37 | 3.7% | 1 | 6 | 956 | 截断（上限 1000） | `nodes/available_xray.txt` |
| clash | 1000 | 43 | 4.3% | 0 | 2 | 955 | 截断（上限 1000） | `nodes/available_clash.yaml` |
| singbox | 1000 | 46 | 4.6% | 0 | 2 | 952 | 截断（上限 1000） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | TLS 握手失败（证书/协议不匹配） | 761 |
| v2ray | 连接超时 | 185 |
| v2ray | 配置被内核拒绝（参数不符） | 17 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 3 |
| v2ray | 连接被重置 | 2 |
| xray | 网络层失败 | 515 |
| xray | TLS 握手失败（证书/协议不匹配） | 258 |
| xray | 连接超时 | 149 |
| xray | 内核启动失败或超时 | 21 |
| xray | 连接被重置 | 13 |
| xray | 配置被内核拒绝（参数不符） | 6 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | TLS 握手失败（证书/协议不匹配） | 849 |
| clash | 网络层失败 | 69 |
| clash | 连接超时 | 32 |
| clash | 内核启动失败或超时 | 5 |
| clash | 配置被内核拒绝（参数不符） | 2 |
| singbox | 连接被重置 | 628 |
| singbox | TLS 握手失败（证书/协议不匹配） | 321 |
| singbox | 连接被拒绝 | 3 |
| singbox | 配置被内核拒绝（参数不符） | 2 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 27 | 32 | 0 | `pool/pool_v2ray.txt` |
| xray | 43 | 37 | 0 | `pool/pool_xray.txt` |
| clash | 56 | 43 | 0 | `pool/pool_clash.yaml` |
| singbox | 54 | 46 | 0 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| Pawdroid/Free-servers | 36 | 14 | 39% | 1867ms | 46.0 |
| snakem982/proxypool | 106 | 41 | 39% | 1685ms | 47.0 |
| peasoft/NoMoreWalls | 80 | 30 | 38% | 1265ms | 48.7 |
| zhuhaiuk/free-nodes | 19 | 3 | 16% | 1053ms | 34.7 |
| igareck/vpn-configs-for-russia | 65 | 9 | 14% | 1680ms | 29.6 |
| Barabama/FreeNodes | 534 | 23 | 4% | 1359ms | 24.9 |
| barry-far/V2ray-Config | 489 | 17 | 3% | 1516ms | 23.3 |
| NiREvil/vless | 894 | 9 | 1% | 1645ms | 20.8 |
| Delta-Kronecker/V2ray-Config | 908 | 9 | 1% | 773ms | 26.1 |
| PuddinCat/BestClash | 449 | 3 | 1% | 6091ms | 0.5 |
| dongchengjie/airport | 388 | 0 | 0% | -ms | 0.0 |
| ShatakVPN/ConfigForge-V2Ray | 20 | 0 | 0% | -ms | 0.0 |
| xrayfree/free-ssr-ss-v2ray-vpn-clash | 8 | 0 | 0% | -ms | 0.0 |
| free-nodes/clashfree | 4 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（32 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `125.227.86.45:443` | trojan | 388ms | Delta-Kronecker/V2ray-Config |
| `59.125.69.22:443` | vless | 598ms | NiREvil/vless |
| `kw119.zxmm.eu.org:20031` | trojan | 640ms | Delta-Kronecker/V2ray-Config |
| `185.148.107.40:8880` | vless | 748ms | Barabama/FreeNodes |
| `155.46.167.30:8880` | vless | 785ms | Barabama/FreeNodes |
| `185.148.104.30:8880` | vless | 813ms | Barabama/FreeNodes |
| `8.34.70.30:8880` | vless | 824ms | barry-far/V2ray-Config |
| `185.162.229.40:8880` | vless | 830ms | Barabama/FreeNodes |
| `location15.cpanel-host16.ir:56137` | ss | 903ms | barry-far/V2ray-Config |
| `202.50.253.99:19999` | ss | 917ms | peasoft/NoMoreWalls |
| `202.50.253.81:19999` | ss | 920ms | peasoft/NoMoreWalls |
| `202.50.253.63:19999` | ss | 922ms | peasoft/NoMoreWalls |
| `202.50.253.54:19999` | ss | 950ms | peasoft/NoMoreWalls |
| `tjxjp.m2k699.com:24999` | trojan | 955ms | Delta-Kronecker/V2ray-Config |
| `202.50.253.18:19999` | ss | 988ms | peasoft/NoMoreWalls |
| `2.26.6.1:2087` | vless | 990ms | igareck/vpn-configs-for-russia |
| `202.50.253.90:19999` | ss | 1014ms | peasoft/NoMoreWalls |
| `location8.cpanel-host10.ir:56134` | ss | 1077ms | barry-far/V2ray-Config |
| `202.50.253.72:19999` | ss | 1091ms | Pawdroid/Free-servers |
| `202.50.253.27:19999` | ss | 1116ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 1193ms | peasoft/NoMoreWalls |
| `202.50.253.45:19999` | ss | 1352ms | Pawdroid/Free-servers |
| `v24.hdacd.com:30824` | vmess | 1439ms | PuddinCat/BestClash |
| `tjrb.m2k699.com:24999` | trojan | 1861ms | snakem982/proxypool |
| `www.windowssearchtools.com:443` | vmess | 2008ms | NiREvil/vless |
| `starlink-ft.251313.xyz:443` | hysteria2 | 2143ms | Pawdroid/Free-servers |
| `80.93.202.40:8880` | vless | 2281ms | Barabama/FreeNodes |
| `8.6.112.206:443` | trojan | 2530ms | barry-far/V2ray-Config |
| `blackshadow.dpdns.org:443` | trojan | 2561ms | Barabama/FreeNodes |
| `143.246.211.163:443` | hysteria2 | 3030ms | igareck/vpn-configs-for-russia |
| `47.250.84.25:443` | trojan | 3787ms | peasoft/NoMoreWalls |
| `us003.421421.xyz:20230` | trojan | 5130ms | Barabama/FreeNodes |

#### xray（37 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `202.50.253.18:19999` | ss | 884ms | peasoft/NoMoreWalls |
| `202.50.253.54:19999` | ss | 893ms | peasoft/NoMoreWalls |
| `202.50.253.99:19999` | ss | 918ms | peasoft/NoMoreWalls |
| `202.50.253.90:19999` | ss | 926ms | peasoft/NoMoreWalls |
| `202.50.253.27:19999` | ss | 930ms | snakem982/proxypool |
| `202.50.253.72:19999` | ss | 934ms | Pawdroid/Free-servers |
| `202.50.253.36:19999` | ss | 934ms | peasoft/NoMoreWalls |
| `202.50.253.45:19999` | ss | 964ms | Pawdroid/Free-servers |
| `202.50.253.81:19999` | ss | 1008ms | peasoft/NoMoreWalls |
| `45.151.71.160:443` | vless | 1009ms | NiREvil/vless |
| `147.45.46.157:8443` | vless | 1039ms | NiREvil/vless |
| `188.164.248.110:443` | vless | 1127ms | Barabama/FreeNodes |
| `funagfrdfs.alixxplay.com:55688` | vless | 1158ms | zhuhaiuk/free-nodes |
| `85.155.149.9:20285` | vless | 1211ms | NiREvil/vless |
| `213.152.165.203:2092` | vless | 1229ms | snakem982/proxypool |
| `77.239.102.129.sslip.io:17232` | vless | 1247ms | snakem982/proxypool |
| `213.152.165.200:2092` | vless | 1255ms | snakem982/proxypool |
| `2.26.6.1:2087` | vless | 1292ms | igareck/vpn-configs-for-russia |
| `213.152.165.201:2095` | vless | 1435ms | snakem982/proxypool |
| `213.152.165.205:2095` | vless | 1476ms | snakem982/proxypool |
| `one-for-all.levikogjgfdd.ir:2096` | vless | 1556ms | Barabama/FreeNodes |
| `109.234.211.232:443` | trojan | 1592ms | barry-far/V2ray-Config |
| `213.152.165.203:2093` | vless | 1601ms | snakem982/proxypool |
| `213.152.165.205:2093` | vless | 1661ms | snakem982/proxypool |
| `202.50.253.63:19999` | ss | 1664ms | peasoft/NoMoreWalls |
| `143.246.211.163:443` | hysteria2 | 1697ms | igareck/vpn-configs-for-russia |
| `location15.cpanel-host16.ir:56137` | ss | 1711ms | barry-far/V2ray-Config |
| `213.152.165.201:2093` | vless | 1818ms | snakem982/proxypool |
| `www.windowssearchtools.com:443` | vmess | 1974ms | NiREvil/vless |
| `location8.cpanel-host10.ir:56134` | ss | 2124ms | barry-far/V2ray-Config |
| `109.73.192.248:443` | vless | 2191ms | snakem982/proxypool |
| `213.152.165.203:2091` | vless | 2210ms | Pawdroid/Free-servers |
| `213.152.165.200:2095` | vless | 2444ms | snakem982/proxypool |
| `213.152.165.200:2090` | vless | 2473ms | snakem982/proxypool |
| `45-149-147-213.sslip.io:4444` | trojan | 2766ms | barry-far/V2ray-Config |
| `www.speedtest.net:443` | vless | 3143ms | Barabama/FreeNodes |
| `138.124.79.6:443` | vless | 3628ms | Pawdroid/Free-servers |

#### clash（43 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `125.227.86.45:443` | trojan | 343ms | Delta-Kronecker/V2ray-Config |
| `tjxjp.m2k699.com:24999` | trojan | 427ms | Delta-Kronecker/V2ray-Config |
| `59.125.69.22:443` | vless | 496ms | NiREvil/vless |
| `80.93.202.40:8880` | vless | 766ms | Barabama/FreeNodes |
| `185.148.107.40:8880` | vless | 795ms | Barabama/FreeNodes |
| `155.46.167.30:8880` | vless | 830ms | Barabama/FreeNodes |
| `kw119.zxmm.eu.org:20031` | trojan | 848ms | Delta-Kronecker/V2ray-Config |
| `66.235.200.30:8880` | vless | 885ms | Barabama/FreeNodes |
| `185.162.229.40:8880` | vless | 887ms | Barabama/FreeNodes |
| `202.50.253.81:19999` | ss | 889ms | peasoft/NoMoreWalls |
| `8.34.70.30:8880` | vless | 893ms | barry-far/V2ray-Config |
| `202.50.253.27:19999` | ss | 923ms | snakem982/proxypool |
| `202.50.253.54:19999` | ss | 925ms | peasoft/NoMoreWalls |
| `202.50.253.72:19999` | ss | 945ms | Pawdroid/Free-servers |
| `funagfrdfs.alixxplay.com:55688` | vless | 970ms | zhuhaiuk/free-nodes |
| `202.50.253.18:19999` | ss | 985ms | peasoft/NoMoreWalls |
| `202.50.253.63:19999` | ss | 994ms | peasoft/NoMoreWalls |
| `funagfrdfs.alixxplay.com:54528` | vless | 996ms | snakem982/proxypool |
| `109.104.153.43:33336` | ssr | 1034ms | barry-far/V2ray-Config |
| `202.50.253.90:19999` | ss | 1065ms | peasoft/NoMoreWalls |
| `202.50.253.99:19999` | ss | 1069ms | peasoft/NoMoreWalls |
| `2.26.6.1:2087` | vless | 1092ms | igareck/vpn-configs-for-russia |
| `location15.cpanel-host16.ir:56137` | ss | 1111ms | barry-far/V2ray-Config |
| `188.164.248.110:443` | vless | 1190ms | Barabama/FreeNodes |
| `77.239.102.129.sslip.io:17232` | vless | 1281ms | snakem982/proxypool |
| `vless.gem-audio2.us.ci:443` | vless | 1360ms | Barabama/FreeNodes |
| `213.152.165.201:2095` | vless | 1410ms | snakem982/proxypool |
| `213.152.165.205:2095` | vless | 1411ms | snakem982/proxypool |
| `213.152.165.203:2092` | vless | 1436ms | snakem982/proxypool |
| `213.152.165.200:2092` | vless | 1452ms | snakem982/proxypool |
| `213.152.165.200:2095` | vless | 1567ms | snakem982/proxypool |
| `109.234.211.232:443` | trojan | 1627ms | barry-far/V2ray-Config |
| `213.152.165.205:2093` | vless | 1766ms | snakem982/proxypool |
| `tjrb.m2k699.com:24999` | trojan | 1806ms | snakem982/proxypool |
| `143.246.211.163:443` | hysteria2 | 1945ms | igareck/vpn-configs-for-russia |
| `213.152.165.203:2091` | vless | 2183ms | Pawdroid/Free-servers |
| `213.152.165.200:2090` | vless | 2222ms | snakem982/proxypool |
| `213.152.165.203:2093` | vless | 2328ms | snakem982/proxypool |
| `138.124.79.6:443` | vless | 2687ms | Pawdroid/Free-servers |
| `location8.cpanel-host10.ir:56134` | ss | 3229ms | barry-far/V2ray-Config |
| … | 共 43 个 | | |

#### singbox（46 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `125.227.86.45:443` | trojan | 430ms | Delta-Kronecker/V2ray-Config |
| `tjxjp.m2k699.com:24999` | trojan | 480ms | Delta-Kronecker/V2ray-Config |
| `location15.cpanel-host16.ir:56137` | ss | 769ms | barry-far/V2ray-Config |
| `8.34.70.30:8880` | vless | 800ms | barry-far/V2ray-Config |
| `185.148.107.40:8880` | vless | 802ms | Barabama/FreeNodes |
| `155.46.167.30:8880` | vless | 830ms | Barabama/FreeNodes |
| `80.93.202.40:8880` | vless | 851ms | Barabama/FreeNodes |
| `202.50.253.81:19999` | ss | 903ms | peasoft/NoMoreWalls |
| `202.50.253.63:19999` | ss | 908ms | peasoft/NoMoreWalls |
| `202.50.253.54:19999` | ss | 911ms | peasoft/NoMoreWalls |
| `202.50.253.18:19999` | ss | 919ms | peasoft/NoMoreWalls |
| `185.162.229.40:8880` | vless | 927ms | Barabama/FreeNodes |
| `202.50.253.99:19999` | ss | 933ms | peasoft/NoMoreWalls |
| `202.50.253.36:19999` | ss | 936ms | peasoft/NoMoreWalls |
| `202.50.253.90:19999` | ss | 942ms | peasoft/NoMoreWalls |
| `185.148.104.30:8880` | vless | 969ms | Barabama/FreeNodes |
| `funagfrdfs.alixxplay.com:55688` | vless | 1030ms | zhuhaiuk/free-nodes |
| `2.26.6.1:2087` | vless | 1073ms | igareck/vpn-configs-for-russia |
| `tjrb.m2k699.com:24999` | trojan | 1074ms | snakem982/proxypool |
| `location8.cpanel-host10.ir:56134` | ss | 1121ms | barry-far/V2ray-Config |
| `202.50.253.45:19999` | ss | 1146ms | Pawdroid/Free-servers |
| `188.164.248.110:443` | vless | 1183ms | Barabama/FreeNodes |
| `202.50.253.72:19999` | ss | 1193ms | Pawdroid/Free-servers |
| `202.50.253.27:19999` | ss | 1238ms | snakem982/proxypool |
| `213.152.165.203:2092` | vless | 1248ms | snakem982/proxypool |
| `213.152.165.200:2092` | vless | 1257ms | snakem982/proxypool |
| `77.239.102.129.sslip.io:17232` | vless | 1339ms | snakem982/proxypool |
| `213.152.165.201:2095` | vless | 1374ms | snakem982/proxypool |
| `213.152.165.200:2095` | vless | 1430ms | snakem982/proxypool |
| `213.152.165.205:2095` | vless | 1463ms | snakem982/proxypool |
| `213.152.165.203:2093` | vless | 1572ms | snakem982/proxypool |
| `213.152.165.205:2093` | vless | 1610ms | snakem982/proxypool |
| `213.152.165.201:2093` | vless | 1634ms | snakem982/proxypool |
| `8.6.112.206:443` | trojan | 1666ms | barry-far/V2ray-Config |
| `47.250.84.25:443` | trojan | 1744ms | peasoft/NoMoreWalls |
| `www.windowssearchtools.com:443` | vmess | 1897ms | NiREvil/vless |
| `support.zoom.us:443` | trojan | 1917ms | igareck/vpn-configs-for-russia |
| `143.246.211.163:443` | hysteria2 | 2081ms | igareck/vpn-configs-for-russia |
| `213.152.165.203:2091` | vless | 2086ms | Pawdroid/Free-servers |
| `109.73.192.248:443` | vless | 2276ms | snakem982/proxypool |
| … | 共 46 个 | | |
