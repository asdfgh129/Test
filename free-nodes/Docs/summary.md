# 节点可用性验证汇总（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

## 2026-11-04 22:35

- 预筛：TCP 连通 4243/4286 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：31.8 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2509 | 29 | 1.2% | 3 | 32 | 2445 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2508 | 71 | 2.8% | 1 | 5 | 2431 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2509 | 48 | 1.9% | 0 | 10 | 2451 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2507 | 56 | 2.2% | 0 | 12 | 2439 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1700 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 745 |
| v2ray | 配置被内核拒绝（参数不符） | 32 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 3 |
| xray | 连接超时 | 1560 |
| xray | TLS 握手失败（证书/协议不匹配） | 596 |
| xray | 网络层失败 | 269 |
| xray | 连接被重置 | 6 |
| xray | 配置被内核拒绝（参数不符） | 5 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1779 |
| clash | TLS 握手失败（证书/协议不匹配） | 385 |
| clash | 网络层失败 | 287 |
| clash | 配置被内核拒绝（参数不符） | 10 |
| singbox | 连接被重置 | 1868 |
| singbox | TLS 握手失败（证书/协议不匹配） | 571 |
| singbox | 配置被内核拒绝（参数不符） | 12 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 251 | 10 | 19 | `pool/pool_v2ray.txt` |
| xray | 630 | 42 | 29 | `pool/pool_xray.txt` |
| clash | 472 | 27 | 21 | `pool/pool_clash.yaml` |
| singbox | 419 | 33 | 23 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| crashgfw/free-airport-nodes | 9 | 8 | 89% | 2544ms | 77.0 |
| zhuhaiuk/free-nodes | 9 | 6 | 67% | 1536ms | 67.5 |
| F0rc3Run/F0rc3Run | 128 | 37 | 29% | 1684ms | 40.1 |
| 0xRadikal/Free-v2ray-Configs | 262 | 60 | 23% | 1704ms | 35.8 |
| Pawdroid/Free-servers | 23 | 2 | 9% | 3351ms | 16.0 |
| whoahaow/rjsxrd | 2147 | 66 | 3% | 1662ms | 22.2 |
| snakem982/proxypool | 105 | 3 | 3% | 2176ms | 18.9 |
| cbusifabcap/daily_free_vpn | 234 | 5 | 2% | 2420ms | 17.0 |
| SoliSpirit/v2ray-configs | 468 | 4 | 1% | 2033ms | 18.4 |
| kooker/FreeSubsCheck | 309 | 2 | 1% | 1654ms | 20.5 |
| NiREvil/vless | 3977 | 11 | 0% | 1417ms | 21.7 |
| peasoft/NoMoreWalls | 306 | 0 | 0% | -ms | 0.0 |
| ermaozi01/free_clash_vpn | 44 | 0 | 0% | -ms | 0.0 |
| igareck/vpn-configs-for-russia | 20 | 0 | 0% | -ms | 0.0 |
| PuddinCat/BestClash | 1730 | 0 | 0% | -ms | 0.0 |
| barry-far/V2ray-Config | 7 | 0 | 0% | -ms | 0.0 |
| Hidashimora/free-vpn-anti-rkn | 235 | 0 | 0% | -ms | 0.0 |
| nyeinkokoaung404/V2ray-Configs | 5 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 11 | 0 | 0% | -ms | 0.0 |
| sakha1370/OpenRay | 2 | 0 | 0% | -ms | 0.0 |
| Delta-Kronecker/V2ray-Config | 2 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（29 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `202.50.253.72:19999` | ss | 968ms | F0rc3Run/F0rc3Run |
| `202.50.253.81:19999` | ss | 969ms | F0rc3Run/F0rc3Run |
| `202.50.253.27:19999` | ss | 975ms | F0rc3Run/F0rc3Run |
| `202.50.253.18:19999` | ss | 999ms | F0rc3Run/F0rc3Run |
| `179.43.187.67:443` | vless | 1165ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.36:19999` | ss | 1308ms | F0rc3Run/F0rc3Run |
| `138.124.86.230:48115` | vless | 1526ms | whoahaow/rjsxrd |
| `89.169.47.96:443` | vless | 1541ms | 0xRadikal/Free-v2ray-Configs |
| `188.137.244.128:8444` | vless | 1612ms | whoahaow/rjsxrd |
| `46.17.46.27:18443` | ss | 1644ms | F0rc3Run/F0rc3Run |
| `v1us9.stablenode.cloud:24421` | trojan | 1679ms | crashgfw/free-airport-nodes |
| `5.57.38.177:443` | ss | 1733ms | SoliSpirit/v2ray-configs |
| `wwww.qarvian.ir:443` | vless | 1794ms | zhuhaiuk/free-nodes |
| `167.88.61.20:443` | trojan | 1887ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28452` | vless | 1905ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.90:19999` | ss | 1980ms | F0rc3Run/F0rc3Run |
| `202.50.253.45:19999` | ss | 2007ms | F0rc3Run/F0rc3Run |
| `renderer-bridge-2-129.mirra.now:443` | vless | 2017ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28449` | vless | 2055ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 2066ms | F0rc3Run/F0rc3Run |
| `146.75.59.186:443` | vless | 2097ms | snakem982/proxypool |
| `202.50.253.54:19999` | ss | 2187ms | F0rc3Run/F0rc3Run |
| `84.23.52.120:28448` | vless | 2381ms | 0xRadikal/Free-v2ray-Configs |
| `v1us9.stablenode.cloud:24413` | trojan | 2933ms | crashgfw/free-airport-nodes |
| `5.57.38.179:5005` | ss | 2983ms | SoliSpirit/v2ray-configs |
| `v1us9.stablenode.cloud:24422` | trojan | 3008ms | crashgfw/free-airport-nodes |
| `104.17.70.206:8443` | vless | 3025ms | 0xRadikal/Free-v2ray-Configs |
| `starlink-ft.251313.xyz:443` | hysteria2 | 3598ms | Pawdroid/Free-servers |
| `84.23.52.120:28453` | vless | 4458ms | 0xRadikal/Free-v2ray-Configs |

#### xray（71 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `179.255.139.212:41392` | vless | 668ms | whoahaow/rjsxrd |
| `154.12.47.231:8443` | vless | 819ms | whoahaow/rjsxrd |
| `167.88.61.20:443` | trojan | 846ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.21:8443` | vless | 887ms | whoahaow/rjsxrd |
| `195.189.98.197:443` | vless | 890ms | 0xRadikal/Free-v2ray-Configs |
| `209.33.160.122:39098` | vless | 904ms | whoahaow/rjsxrd |
| `5.104.74.69:8443` | vless | 909ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.27:8443` | vless | 910ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.70:8443` | vless | 911ms | NiREvil/vless |
| `edge.bookmai.com:443` | vless | 918ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.22:8443` | vless | 927ms | NiREvil/vless |
| `202.50.253.72:19999` | ss | 931ms | F0rc3Run/F0rc3Run |
| `202.50.253.36:19999` | ss | 942ms | F0rc3Run/F0rc3Run |
| `212.69.135.70:8443` | vless | 957ms | 0xRadikal/Free-v2ray-Configs |
| `94.183.152.153:443` | vless | 960ms | NiREvil/vless |
| `212.69.135.27:8443` | vless | 967ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.5:8443` | vless | 973ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 989ms | F0rc3Run/F0rc3Run |
| `212.69.135.69:8443` | vless | 992ms | 0xRadikal/Free-v2ray-Configs |
| `212.69.135.30:8443` | vless | 998ms | 0xRadikal/Free-v2ray-Configs |
| `212.69.135.29:8443` | vless | 999ms | whoahaow/rjsxrd |
| `5.104.74.25:8443` | vless | 1000ms | whoahaow/rjsxrd |
| `104.36.69.105:443` | vless | 1002ms | whoahaow/rjsxrd |
| `104.225.239.235:443` | vless | 1013ms | whoahaow/rjsxrd |
| `proxymite.waldron.ir:48146` | vless | 1024ms | 0xRadikal/Free-v2ray-Configs |
| `195.133.39.202:8443` | vless | 1074ms | whoahaow/rjsxrd |
| `212.69.135.26:8443` | vless | 1114ms | 0xRadikal/Free-v2ray-Configs |
| `78.17.93.30:443` | vless | 1122ms | 0xRadikal/Free-v2ray-Configs |
| `9.247.23.209:443` | vless | 1165ms | 0xRadikal/Free-v2ray-Configs |
| `100.55.27.211:10413` | vless | 1177ms | whoahaow/rjsxrd |
| `ca1.fox-lisa.ru:443` | vless | 1197ms | 0xRadikal/Free-v2ray-Configs |
| `snow.betust.net:443` | vless | 1215ms | 0xRadikal/Free-v2ray-Configs |
| `43.163.112.174:443` | vless | 1234ms | zhuhaiuk/free-nodes |
| `179.43.187.67:443` | vless | 1235ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 1259ms | F0rc3Run/F0rc3Run |
| `5.104.74.26:8443` | vless | 1268ms | NiREvil/vless |
| `212.69.135.71:8443` | vless | 1288ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.45:19999` | ss | 1369ms | F0rc3Run/F0rc3Run |
| `138.124.86.230:48115` | vless | 1417ms | whoahaow/rjsxrd |
| `147.45.161.4:443` | vless | 1485ms | kooker/FreeSubsCheck |
| … | 共 71 个 | | |

#### clash（48 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `103.204.174.80:443` | vless | 394ms | whoahaow/rjsxrd |
| `154.12.47.231:8443` | vless | 724ms | whoahaow/rjsxrd |
| `104.18.1.1:2087` | vless | 824ms | cbusifabcap/daily_free_vpn |
| `167.88.61.20:443` | trojan | 874ms | 0xRadikal/Free-v2ray-Configs |
| `104.225.239.235:443` | vless | 915ms | whoahaow/rjsxrd |
| `193.23.218.107:443` | vless | 927ms | whoahaow/rjsxrd |
| `104.36.69.105:443` | vless | 949ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 990ms | F0rc3Run/F0rc3Run |
| `202.50.253.18:19999` | ss | 1001ms | F0rc3Run/F0rc3Run |
| `195.133.39.202:8443` | vless | 1024ms | whoahaow/rjsxrd |
| `100.55.27.211:10413` | vless | 1050ms | whoahaow/rjsxrd |
| `209.33.160.122:39098` | vless | 1069ms | whoahaow/rjsxrd |
| `202.50.253.27:19999` | ss | 1081ms | F0rc3Run/F0rc3Run |
| `104.243.16.178:443` | vless | 1089ms | whoahaow/rjsxrd |
| `31.76.94.21:443` | vless | 1203ms | whoahaow/rjsxrd |
| `202.50.253.90:19999` | ss | 1298ms | F0rc3Run/F0rc3Run |
| `43.163.112.174:443` | vless | 1311ms | zhuhaiuk/free-nodes |
| `du-rov.secureservice.top:8443` | vless | 1398ms | 0xRadikal/Free-v2ray-Configs |
| `71b840t.de7.h1clayd.click:443` | vless | 1426ms | whoahaow/rjsxrd |
| `46.17.46.27:18443` | ss | 1483ms | F0rc3Run/F0rc3Run |
| `89.169.47.96:443` | vless | 1518ms | 0xRadikal/Free-v2ray-Configs |
| `edge.bookmai.com:443` | vless | 1562ms | 0xRadikal/Free-v2ray-Configs |
| `87.232.88.27:443` | vless | 1594ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28449` | vless | 1601ms | 0xRadikal/Free-v2ray-Configs |
| `138.124.86.230:48115` | vless | 1607ms | whoahaow/rjsxrd |
| `202.50.253.81:19999` | ss | 1627ms | F0rc3Run/F0rc3Run |
| `95.85.251.41:8444` | vless | 1630ms | whoahaow/rjsxrd |
| `wwww.qarvian.ir:443` | vless | 1731ms | zhuhaiuk/free-nodes |
| `147.45.161.4:443` | vless | 1823ms | kooker/FreeSubsCheck |
| `179.255.139.212:41392` | vless | 2008ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 2024ms | F0rc3Run/F0rc3Run |
| `146.75.59.186:443` | vless | 2075ms | snakem982/proxypool |
| `84.23.52.120:28452` | vless | 2094ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 2184ms | F0rc3Run/F0rc3Run |
| `v1us9.stablenode.cloud:24413` | trojan | 2211ms | crashgfw/free-airport-nodes |
| `104.17.70.206:8443` | vless | 2247ms | 0xRadikal/Free-v2ray-Configs |
| `201.51.4.89:443` | vless | 2298ms | whoahaow/rjsxrd |
| `84.23.52.120:28448` | vless | 2385ms | 0xRadikal/Free-v2ray-Configs |
| `v1us9.stablenode.cloud:24422` | trojan | 2577ms | crashgfw/free-airport-nodes |
| `188.137.244.128:8444` | vless | 2671ms | whoahaow/rjsxrd |
| … | 共 48 个 | | |

#### singbox（56 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `103.204.174.80:443` | vless | 558ms | whoahaow/rjsxrd |
| `179.255.139.212:41392` | vless | 767ms | whoahaow/rjsxrd |
| `167.88.61.20:443` | trojan | 810ms | 0xRadikal/Free-v2ray-Configs |
| `104.243.16.178:443` | vless | 928ms | whoahaow/rjsxrd |
| `104.36.69.105:443` | vless | 943ms | whoahaow/rjsxrd |
| `154.12.47.231:8443` | vless | 965ms | whoahaow/rjsxrd |
| `edge.bookmai.com:443` | vless | 1022ms | 0xRadikal/Free-v2ray-Configs |
| `100.55.27.211:10413` | vless | 1060ms | whoahaow/rjsxrd |
| `209.33.160.122:39098` | vless | 1088ms | whoahaow/rjsxrd |
| `193.23.218.107:443` | vless | 1153ms | whoahaow/rjsxrd |
| `104.225.239.235:443` | vless | 1191ms | whoahaow/rjsxrd |
| `9.247.23.209:443` | vless | 1194ms | 0xRadikal/Free-v2ray-Configs |
| `45.76.172.197:443` | vless | 1206ms | NiREvil/vless |
| `144.202.126.147:443` | vless | 1213ms | NiREvil/vless |
| `138.124.86.230:48115` | vless | 1241ms | whoahaow/rjsxrd |
| `179.43.187.67:443` | vless | 1251ms | 0xRadikal/Free-v2ray-Configs |
| `31.77.236.114:443` | vless | 1306ms | whoahaow/rjsxrd |
| `172.233.129.172:443` | vless | 1317ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 1324ms | F0rc3Run/F0rc3Run |
| `195.133.39.202:8443` | vless | 1335ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 1378ms | F0rc3Run/F0rc3Run |
| `87.232.88.27:443` | vless | 1395ms | 0xRadikal/Free-v2ray-Configs |
| `43.163.112.174:443` | vless | 1421ms | zhuhaiuk/free-nodes |
| `5.42.99.64:8443` | vless | 1462ms | 0xRadikal/Free-v2ray-Configs |
| `du-rov.secureservice.top:8443` | vless | 1499ms | 0xRadikal/Free-v2ray-Configs |
| `89.169.47.96:443` | vless | 1549ms | 0xRadikal/Free-v2ray-Configs |
| `35.212.211.133:443` | vless | 1566ms | whoahaow/rjsxrd |
| `202.50.253.36:19999` | ss | 1568ms | F0rc3Run/F0rc3Run |
| `v1us9.stablenode.cloud:24421` | trojan | 1635ms | crashgfw/free-airport-nodes |
| `wwww.qarvian.ir:443` | vless | 1724ms | zhuhaiuk/free-nodes |
| `202.50.253.54:19999` | ss | 1734ms | F0rc3Run/F0rc3Run |
| `202.50.253.63:19999` | ss | 1735ms | F0rc3Run/F0rc3Run |
| `v1us9.stablenode.cloud:24413` | trojan | 1762ms | crashgfw/free-airport-nodes |
| `renderer-bridge-2-129.mirra.now:443` | vless | 1769ms | 0xRadikal/Free-v2ray-Configs |
| `146.75.57.111:443` | vless | 1894ms | cbusifabcap/daily_free_vpn |
| `202.50.253.99:19999` | ss | 1982ms | F0rc3Run/F0rc3Run |
| `46.17.46.27:18443` | ss | 1993ms | F0rc3Run/F0rc3Run |
| `84.23.52.120:28449` | vless | 2067ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28448` | vless | 2112ms | 0xRadikal/Free-v2ray-Configs |
| `146.75.59.186:443` | vless | 2355ms | snakem982/proxypool |
| … | 共 56 个 | | |

## 2026-11-03 22:45

- 预筛：TCP 连通 4949/4991 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：31.9 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2507 | 30 | 1.2% | 3 | 26 | 2448 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2509 | 74 | 3.0% | 1 | 3 | 2431 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2507 | 51 | 2.0% | 0 | 12 | 2444 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2506 | 46 | 1.8% | 0 | 5 | 2455 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1425 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 1022 |
| v2ray | 配置被内核拒绝（参数不符） | 26 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 3 |
| v2ray | 连接被重置 | 1 |
| xray | 连接超时 | 1555 |
| xray | TLS 握手失败（证书/协议不匹配） | 558 |
| xray | 网络层失败 | 314 |
| xray | 连接被重置 | 4 |
| xray | 配置被内核拒绝（参数不符） | 3 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1702 |
| clash | TLS 握手失败（证书/协议不匹配） | 459 |
| clash | 网络层失败 | 283 |
| clash | 配置被内核拒绝（参数不符） | 12 |
| singbox | 连接被重置 | 1825 |
| singbox | TLS 握手失败（证书/协议不匹配） | 628 |
| singbox | 配置被内核拒绝（参数不符） | 5 |
| singbox | 认证失败（口令/UUID 不符） | 1 |
| singbox | 连接被拒绝 | 1 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 241 | 16 | 14 | `pool/pool_v2ray.txt` |
| xray | 588 | 47 | 27 | `pool/pool_xray.txt` |
| clash | 445 | 34 | 17 | `pool/pool_clash.yaml` |
| singbox | 386 | 33 | 13 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 61 | 34 | 56% | 1732ms | 58.6 |
| sinavm/SVM | 4 | 2 | 50% | 2776ms | 48.3 |
| hello-world-1989/cn-news | 6 | 2 | 33% | 1068ms | 46.9 |
| xyfqzy/free-nodes | 4 | 1 | 25% | 1144ms | 40.6 |
| 0xRadikal/Free-v2ray-Configs | 275 | 67 | 24% | 1825ms | 36.1 |
| F0rc3Run/F0rc3Run | 72 | 6 | 8% | 2149ms | 22.9 |
| igareck/vpn-configs-for-russia | 92 | 6 | 7% | 2115ms | 21.9 |
| cbusifabcap/daily_free_vpn | 347 | 14 | 4% | 1684ms | 22.7 |
| whoahaow/rjsxrd | 2239 | 62 | 3% | 1863ms | 20.8 |
| NiREvil/vless | 3035 | 7 | 0% | 2453ms | 15.4 |
| peasoft/NoMoreWalls | 254 | 0 | 0% | -ms | 0.0 |
| sakha1370/OpenRay | 958 | 0 | 0% | -ms | 0.0 |
| Pawdroid/Free-servers | 18 | 0 | 0% | -ms | 0.0 |
| snakem982/proxypool | 143 | 0 | 0% | -ms | 0.0 |
| kooker/FreeSubsCheck | 253 | 0 | 0% | -ms | 0.0 |
| barry-far/V2ray-Config | 177 | 0 | 0% | -ms | 0.0 |
| PuddinCat/BestClash | 828 | 0 | 0% | -ms | 0.0 |
| SoliSpirit/v2ray-configs | 108 | 0 | 0% | -ms | 0.0 |
| Delta-Kronecker/V2ray-Config | 1145 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 10 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（30 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `193.163.19.232:443` | trojan | 864ms | cbusifabcap/daily_free_vpn |
| `xunlinknode.csdjhajkshdjkas.com:40006` | ss | 874ms | F0rc3Run/F0rc3Run |
| `179.253.225.34:443` | trojan | 954ms | cbusifabcap/daily_free_vpn |
| `202.50.253.45:19999` | ss | 1073ms | ermaozi01/free_clash_vpn |
| `202.50.253.18:19999` | ss | 1160ms | ermaozi01/free_clash_vpn |
| `202.50.253.90:19999` | ss | 1215ms | ermaozi01/free_clash_vpn |
| `179.43.187.67:443` | vless | 1248ms | 0xRadikal/Free-v2ray-Configs |
| `95.142.32.42:8444` | vless | 1315ms | whoahaow/rjsxrd |
| `www.visa.com.sg:8443` | vless | 1350ms | NiREvil/vless |
| `193.188.21.253:14430` | vless | 1354ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28453` | vless | 1647ms | 0xRadikal/Free-v2ray-Configs |
| `153.76.161.159:443` | trojan | 1675ms | whoahaow/rjsxrd |
| `146.103.118.189:443` | vless | 1775ms | whoahaow/rjsxrd |
| `146.75.57.238:443` | vless | 1873ms | cbusifabcap/daily_free_vpn |
| `202.50.253.99:19999` | ss | 1926ms | ermaozi01/free_clash_vpn |
| `141.193.213.21:8443` | vless | 2003ms | igareck/vpn-configs-for-russia |
| `202.50.253.72:19999` | ss | 2197ms | ermaozi01/free_clash_vpn |
| `202.50.253.81:19999` | ss | 2300ms | ermaozi01/free_clash_vpn |
| `172.66.0.1:443` | vmess | 2318ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 2533ms | ermaozi01/free_clash_vpn |
| `104.17.70.206:8443` | vless | 2533ms | 0xRadikal/Free-v2ray-Configs |
| `84.23.52.120:28449` | vless | 2712ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 2750ms | ermaozi01/free_clash_vpn |
| `176.108.243.235:9570` | vless | 2958ms | NiREvil/vless |
| `202.50.253.36:19999` | ss | 2980ms | ermaozi01/free_clash_vpn |
| `84.23.52.120:28448` | vless | 3032ms | 0xRadikal/Free-v2ray-Configs |
| `95.182.96.13:57788` | vmess | 3112ms | NiREvil/vless |
| `84.23.52.120:28447` | vless | 3151ms | sinavm/SVM |
| `45.132.176.239:9552` | vless | 3207ms | NiREvil/vless |
| `sgtht.wawojk.dpdns.org:443` | vless | 3249ms | cbusifabcap/daily_free_vpn |

#### xray（74 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `212.69.135.71:8443` | vless | 866ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.30:8443` | vless | 871ms | 0xRadikal/Free-v2ray-Configs |
| `212.69.135.26:8443` | vless | 913ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.5:8443` | vless | 934ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 939ms | ermaozi01/free_clash_vpn |
| `195.189.98.197:443` | vless | 940ms | whoahaow/rjsxrd |
| `202.50.253.63:19999` | ss | 946ms | ermaozi01/free_clash_vpn |
| `3.35.166.197:443` | vless | 962ms | hello-world-1989/cn-news |
| `89.110.64.15:443` | vless | 985ms | whoahaow/rjsxrd |
| `94.183.152.153:443` | vless | 989ms | 0xRadikal/Free-v2ray-Configs |
| `9.247.23.209:443` | vless | 999ms | ermaozi01/free_clash_vpn |
| `212.69.135.70:8443` | vless | 1015ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 1019ms | ermaozi01/free_clash_vpn |
| `212.69.135.27:8443` | vless | 1019ms | 0xRadikal/Free-v2ray-Configs |
| `212.69.135.30:8443` | vless | 1032ms | 0xRadikal/Free-v2ray-Configs |
| `5.104.74.71:8443` | vless | 1042ms | whoahaow/rjsxrd |
| `212.69.135.69:8443` | vless | 1067ms | 0xRadikal/Free-v2ray-Configs |
| `38.244.5.231:443` | vless | 1131ms | 0xRadikal/Free-v2ray-Configs |
| `5e094at.de27.h1clayd.click:443` | vless | 1145ms | whoahaow/rjsxrd |
| `176.108.243.235:25602` | vless | 1182ms | whoahaow/rjsxrd |
| `177.3.219.120:443` | vless | 1207ms | whoahaow/rjsxrd |
| `179.43.187.67:443` | vless | 1238ms | 0xRadikal/Free-v2ray-Configs |
| `edge.bookmai.com:443` | vless | 1300ms | ermaozi01/free_clash_vpn |
| `185.76.14.21:443` | vless | 1311ms | NiREvil/vless |
| `89.144.53.4:8445` | vless | 1333ms | 0xRadikal/Free-v2ray-Configs |
| `144.31.242.142:443` | vless | 1364ms | cbusifabcap/daily_free_vpn |
| `book.jarbook.net:443` | vless | 1418ms | 0xRadikal/Free-v2ray-Configs |
| `95.142.32.42:8444` | vless | 1430ms | whoahaow/rjsxrd |
| `185.76.241.52:9601` | vless | 1433ms | whoahaow/rjsxrd |
| `5.129.202.80:443` | vless | 1437ms | 0xRadikal/Free-v2ray-Configs |
| `finlandlanzarotte.live:443` | vless | 1449ms | 0xRadikal/Free-v2ray-Configs |
| `217.19.122.170:2096` | vless | 1453ms | 0xRadikal/Free-v2ray-Configs |
| `5.42.99.64:8443` | vless | 1458ms | 0xRadikal/Free-v2ray-Configs |
| `ie1.fox-lisa.ru:443` | vless | 1478ms | whoahaow/rjsxrd |
| `iproxyland.beshdash.ir:56261` | vless | 1482ms | 0xRadikal/Free-v2ray-Configs |
| `156.252.229.136:8443` | vless | 1486ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.18:19999` | ss | 1502ms | ermaozi01/free_clash_vpn |
| `bg1.fox-lisa.ru:443` | vless | 1533ms | whoahaow/rjsxrd |
| `176.108.243.235:25603` | vless | 1544ms | whoahaow/rjsxrd |
| `89.208.210.53:38963` | vless | 1619ms | whoahaow/rjsxrd |
| … | 共 74 个 | | |

#### clash（51 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.158.71.221:443` | trojan | 691ms | cbusifabcap/daily_free_vpn |
| `179.253.225.34:443` | trojan | 870ms | cbusifabcap/daily_free_vpn |
| `202.50.253.99:19999` | ss | 1000ms | ermaozi01/free_clash_vpn |
| `202.50.253.45:19999` | ss | 1001ms | ermaozi01/free_clash_vpn |
| `9.247.23.209:443` | vless | 1053ms | ermaozi01/free_clash_vpn |
| `202.50.253.63:19999` | ss | 1116ms | ermaozi01/free_clash_vpn |
| `103.102.229.235:443` | vless | 1125ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1128ms | ermaozi01/free_clash_vpn |
| `104.18.1.1:2087` | vless | 1144ms | xyfqzy/free-nodes |
| `95.142.32.42:8444` | vless | 1161ms | whoahaow/rjsxrd |
| `3.35.166.197:443` | vless | 1174ms | hello-world-1989/cn-news |
| `146.103.118.189:443` | vless | 1228ms | whoahaow/rjsxrd |
| `78.17.39.129:443` | vless | 1278ms | whoahaow/rjsxrd |
| `edge.bookmai.com:443` | vless | 1306ms | ermaozi01/free_clash_vpn |
| `72.56.241.230:443` | vless | 1331ms | whoahaow/rjsxrd |
| `89.144.53.4:8445` | vless | 1382ms | 0xRadikal/Free-v2ray-Configs |
| `46.17.46.27:18443` | ss | 1409ms | F0rc3Run/F0rc3Run |
| `193.188.21.253:14430` | vless | 1412ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.54:19999` | ss | 1415ms | ermaozi01/free_clash_vpn |
| `91.195.254.172:443` | vless | 1454ms | whoahaow/rjsxrd |
| `199.189.251.65:443` | vless | 1487ms | whoahaow/rjsxrd |
| `5.129.202.80:443` | vless | 1490ms | 0xRadikal/Free-v2ray-Configs |
| `kz-3.movietop24.site:443` | vless | 1499ms | whoahaow/rjsxrd |
| `177.202.69.195:443` | vless | 1512ms | whoahaow/rjsxrd |
| `156.252.229.136:8443` | vless | 1516ms | 0xRadikal/Free-v2ray-Configs |
| `147.45.245.17:443` | vless | 1546ms | 0xRadikal/Free-v2ray-Configs |
| `es3.h1cloud.net:25150` | vless | 1643ms | 0xRadikal/Free-v2ray-Configs |
| `iproxyland.beshdash.ir:56261` | vless | 1647ms | 0xRadikal/Free-v2ray-Configs |
| `5.42.99.64:8443` | vless | 1742ms | 0xRadikal/Free-v2ray-Configs |
| `cdn-rum-n9kardx-q74mle.keno.su:443` | vless | 1758ms | whoahaow/rjsxrd |
| `195.123.189.221:443` | vless | 1763ms | 0xRadikal/Free-v2ray-Configs |
| `191.217.217.71:443` | vless | 1860ms | whoahaow/rjsxrd |
| `du-rov.secureservice.top:8443` | vless | 1931ms | 0xRadikal/Free-v2ray-Configs |
| `104.17.70.206:8443` | vless | 2010ms | 0xRadikal/Free-v2ray-Configs |
| `vdsin.xvanta.online:443` | vless | 2124ms | whoahaow/rjsxrd |
| `213.176.19.216:443` | vless | 2232ms | whoahaow/rjsxrd |
| `84.23.52.120:28448` | vless | 2249ms | 0xRadikal/Free-v2ray-Configs |
| `141.193.213.21:8443` | vless | 2262ms | igareck/vpn-configs-for-russia |
| `ru-in-ind-4vp.fast-cdn24.com:443` | vless | 2370ms | whoahaow/rjsxrd |
| `alb-4vp.fast-cdn24.com:443` | vless | 2459ms | whoahaow/rjsxrd |
| … | 共 51 个 | | |

#### singbox（46 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `193.163.19.232:443` | trojan | 1055ms | cbusifabcap/daily_free_vpn |
| `185.255.115.58:443` | vless | 1075ms | whoahaow/rjsxrd |
| `195.123.189.214:443` | vless | 1214ms | cbusifabcap/daily_free_vpn |
| `202.50.253.54:19999` | ss | 1222ms | ermaozi01/free_clash_vpn |
| `103.102.229.235:443` | vless | 1231ms | whoahaow/rjsxrd |
| `95.142.32.42:8444` | vless | 1267ms | whoahaow/rjsxrd |
| `202.50.253.18:19999` | ss | 1269ms | ermaozi01/free_clash_vpn |
| `cdn-rum-n9kardx-q74mle.keno.su:443` | vless | 1305ms | whoahaow/rjsxrd |
| `72.56.241.230:443` | vless | 1341ms | whoahaow/rjsxrd |
| `146.75.57.238:443` | vless | 1355ms | cbusifabcap/daily_free_vpn |
| `156.252.229.136:8443` | vless | 1522ms | 0xRadikal/Free-v2ray-Configs |
| `5.42.99.64:8443` | vless | 1542ms | 0xRadikal/Free-v2ray-Configs |
| `191.217.217.71:443` | vless | 1592ms | whoahaow/rjsxrd |
| `177.202.69.195:443` | vless | 1596ms | whoahaow/rjsxrd |
| `199.189.251.65:443` | vless | 1600ms | whoahaow/rjsxrd |
| `83.147.15.84:8443` | trojan | 1609ms | cbusifabcap/daily_free_vpn |
| `202.50.253.90:19999` | ss | 1610ms | ermaozi01/free_clash_vpn |
| `193.188.21.253:14430` | vless | 1619ms | 0xRadikal/Free-v2ray-Configs |
| `qtir1.dnetsolutions.ru:443` | vless | 1630ms | 0xRadikal/Free-v2ray-Configs |
| `109.71.247.200:443` | vless | 1634ms | whoahaow/rjsxrd |
| `141.193.213.21:2083` | vless | 1814ms | igareck/vpn-configs-for-russia |
| `84.23.52.120:28449` | vless | 1816ms | 0xRadikal/Free-v2ray-Configs |
| `news.zoom.us:2083` | vless | 1858ms | igareck/vpn-configs-for-russia |
| `iproxyland.beshdash.ir:58545` | vless | 1863ms | 0xRadikal/Free-v2ray-Configs |
| `89.144.53.4:8445` | vless | 1969ms | 0xRadikal/Free-v2ray-Configs |
| `5.129.202.80:443` | vless | 2020ms | 0xRadikal/Free-v2ray-Configs |
| `201.51.4.89:443` | vless | 2045ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.72:19999` | ss | 2077ms | ermaozi01/free_clash_vpn |
| `104.17.70.206:8443` | vless | 2154ms | 0xRadikal/Free-v2ray-Configs |
| `141.193.213.21:8443` | vless | 2223ms | igareck/vpn-configs-for-russia |
| `213.176.19.216:443` | vless | 2271ms | whoahaow/rjsxrd |
| `84.23.52.120:28447` | vless | 2400ms | sinavm/SVM |
| `du-rov.secureservice.top:8443` | vless | 2442ms | 0xRadikal/Free-v2ray-Configs |
| `46.17.46.27:18443` | ss | 2511ms | F0rc3Run/F0rc3Run |
| `147.45.161.4:443` | vless | 2602ms | whoahaow/rjsxrd |
| `84.23.52.120:28448` | vless | 2620ms | 0xRadikal/Free-v2ray-Configs |
| `130.49.189.36:443` | vless | 2655ms | whoahaow/rjsxrd |
| `vdsin.xvanta.online:443` | vless | 2751ms | whoahaow/rjsxrd |
| `193.188.21.253:10444` | vless | 2792ms | 0xRadikal/Free-v2ray-Configs |
| `5e094at.de27.h1clayd.click:443` | vless | 2891ms | whoahaow/rjsxrd |
| … | 共 46 个 | | |

## 2026-11-02 22:47

- 预筛：TCP 连通 4995/5051 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：32.6 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2507 | 26 | 1.1% | 6 | 28 | 2447 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2509 | 53 | 2.1% | 1 | 0 | 2455 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2508 | 47 | 1.9% | 0 | 26 | 2435 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2507 | 50 | 2.0% | 0 | 17 | 2440 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1438 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 1003 |
| v2ray | 配置被内核拒绝（参数不符） | 28 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 6 |
| v2ray | 连接被重置 | 4 |
| v2ray | 网络层失败 | 2 |
| xray | 连接超时 | 1422 |
| xray | TLS 握手失败（证书/协议不匹配） | 523 |
| xray | 网络层失败 | 498 |
| xray | 连接被重置 | 12 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1579 |
| clash | 网络层失败 | 437 |
| clash | TLS 握手失败（证书/协议不匹配） | 417 |
| clash | 配置被内核拒绝（参数不符） | 26 |
| clash | 连接被重置 | 2 |
| singbox | 连接被重置 | 1791 |
| singbox | TLS 握手失败（证书/协议不匹配） | 640 |
| singbox | 配置被内核拒绝（参数不符） | 17 |
| singbox | 内核启动失败或超时 | 7 |
| singbox | 认证失败（口令/UUID 不符） | 2 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 225 | 11 | 15 | `pool/pool_v2ray.txt` |
| xray | 541 | 21 | 32 | `pool/pool_xray.txt` |
| clash | 411 | 22 | 25 | `pool/pool_clash.yaml` |
| singbox | 353 | 24 | 26 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| ermaozi01/free_clash_vpn | 12 | 10 | 83% | 1509ms | 79.3 |
| hello-world-1989/cn-news | 10 | 6 | 60% | 1253ms | 64.5 |
| F0rc3Run/F0rc3Run | 80 | 33 | 41% | 1558ms | 49.5 |
| Pawdroid/Free-servers | 22 | 5 | 23% | 2296ms | 32.1 |
| 0xRadikal/Free-v2ray-Configs | 263 | 56 | 21% | 1380ms | 36.6 |
| snakem982/proxypool | 61 | 9 | 15% | 1933ms | 28.7 |
| sinavm/SVM | 16 | 1 | 6% | 3078ms | 15.9 |
| whoahaow/rjsxrd | 1963 | 42 | 2% | 1906ms | 20.1 |
| igareck/vpn-configs-for-russia | 79 | 1 | 1% | 2143ms | 18.0 |
| cbusifabcap/daily_free_vpn | 447 | 4 | 1% | 1960ms | 18.9 |
| peasoft/NoMoreWalls | 261 | 2 | 1% | 959ms | 24.8 |
| kooker/FreeSubsCheck | 397 | 3 | 1% | 2273ms | 16.9 |
| barry-far/V2ray-Config | 240 | 1 | 0% | 1174ms | 23.2 |
| NiREvil/vless | 3282 | 3 | 0% | 1128ms | 23.3 |
| sakha1370/OpenRay | 591 | 0 | 0% | -ms | 0.0 |
| dongchengjie/airport | 99 | 0 | 0% | -ms | 0.0 |
| MatinGhanbari/v2ray-configs | 617 | 0 | 0% | -ms | 0.0 |
| ShatakVPN/ConfigForge-V2Ray | 29 | 0 | 0% | -ms | 0.0 |
| SoliSpirit/v2ray-configs | 132 | 0 | 0% | -ms | 0.0 |
| Delta-Kronecker/V2ray-Config | 1416 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 14 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（26 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `152.175.6.229:31884` | vless | 425ms | peasoft/NoMoreWalls |
| `34.222.228.125:80` | vless | 668ms | 0xRadikal/Free-v2ray-Configs |
| `32.199.151.91:80` | vless | 722ms | 0xRadikal/Free-v2ray-Configs |
| `167.88.61.52:443` | trojan | 799ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 965ms | F0rc3Run/F0rc3Run |
| `202.50.253.36:19999` | ss | 971ms | F0rc3Run/F0rc3Run |
| `202.50.253.54:19999` | ss | 1001ms | ermaozi01/free_clash_vpn |
| `56.10.10.106:8443` | ss | 1137ms | hello-world-1989/cn-news |
| `179.43.187.67:443` | vless | 1174ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.18:19999` | ss | 1283ms | F0rc3Run/F0rc3Run |
| `46.17.46.27:18443` | ss | 1327ms | F0rc3Run/F0rc3Run |
| `195.137.226.133:2083` | vless | 1413ms | whoahaow/rjsxrd |
| `202.50.253.90:19999` | ss | 1489ms | F0rc3Run/F0rc3Run |
| `202.50.253.63:19999` | ss | 1489ms | F0rc3Run/F0rc3Run |
| `202.50.253.45:19999` | ss | 1752ms | F0rc3Run/F0rc3Run |
| `199.232.78.160:443` | vless | 1982ms | snakem982/proxypool |
| `200.165.231.209:443` | vless | 2047ms | whoahaow/rjsxrd |
| `fin1.ilysho1.ir:80` | vless | 2143ms | igareck/vpn-configs-for-russia |
| `104.17.70.206:8443` | vless | 2160ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 2263ms | ermaozi01/free_clash_vpn |
| `202.50.253.72:19999` | ss | 2359ms | F0rc3Run/F0rc3Run |
| `xunlinknode.csdjhajkshdjkas.com:40006` | ss | 2488ms | F0rc3Run/F0rc3Run |
| `202.50.253.81:19999` | ss | 2530ms | ermaozi01/free_clash_vpn |
| `172.66.0.162:443` | vless | 3257ms | cbusifabcap/daily_free_vpn |
| `renderer-bridge-2-129.mirra.now:443` | vless | 3575ms | whoahaow/rjsxrd |
| `217.60.73.56:443` | hysteria2 | 3988ms | Pawdroid/Free-servers |

#### xray（53 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `hk010.zestapp778.com:31884` | vless | 604ms | kooker/FreeSubsCheck |
| `212.69.135.70:8443` | vless | 879ms | whoahaow/rjsxrd |
| `5.104.74.71:8443` | vless | 928ms | whoahaow/rjsxrd |
| `202.50.253.27:19999` | ss | 932ms | F0rc3Run/F0rc3Run |
| `lectures.blog-forme.ru:443` | vless | 938ms | 0xRadikal/Free-v2ray-Configs |
| `157.90.165.181:11762` | vless | 949ms | 0xRadikal/Free-v2ray-Configs |
| `2.26.6.244:443` | vless | 966ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 970ms | ermaozi01/free_clash_vpn |
| `5.104.74.70:8443` | vless | 981ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 1016ms | ermaozi01/free_clash_vpn |
| `177.177.215.45:444` | vless | 1019ms | whoahaow/rjsxrd |
| `202.50.253.90:19999` | ss | 1049ms | F0rc3Run/F0rc3Run |
| `202.50.253.36:19999` | ss | 1059ms | F0rc3Run/F0rc3Run |
| `212.69.135.69:8443` | vless | 1072ms | whoahaow/rjsxrd |
| `212.34.128.120:443` | vless | 1113ms | NiREvil/vless |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1115ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.180.142:443` | vless | 1131ms | 0xRadikal/Free-v2ray-Configs |
| `direct-nl.bachidze.com:443` | vless | 1154ms | whoahaow/rjsxrd |
| `5.104.74.69:8443` | vless | 1156ms | whoahaow/rjsxrd |
| `56.10.10.106:8443` | ss | 1191ms | hello-world-1989/cn-news |
| `uso.zqpm.ir:8443` | vless | 1217ms | 0xRadikal/Free-v2ray-Configs |
| `de15.h1cloud.net:25362` | vless | 1248ms | Pawdroid/Free-servers |
| `202.50.253.45:19999` | ss | 1260ms | F0rc3Run/F0rc3Run |
| `185.76.14.21:443` | vless | 1305ms | NiREvil/vless |
| `13.143.182.104:443` | vless | 1349ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.182.103:443` | vless | 1378ms | 0xRadikal/Free-v2ray-Configs |
| `147.45.108.45:443` | vless | 1400ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.72:19999` | ss | 1410ms | F0rc3Run/F0rc3Run |
| `79.182.39.236:25362` | vless | 1442ms | whoahaow/rjsxrd |
| `179.253.82.19:4443` | vless | 1443ms | cbusifabcap/daily_free_vpn |
| `195.137.226.133:2083` | vless | 1474ms | whoahaow/rjsxrd |
| `46.17.46.27:18443` | ss | 1479ms | F0rc3Run/F0rc3Run |
| `13.143.165.126:443` | vless | 1521ms | whoahaow/rjsxrd |
| `5.129.202.80:443` | vless | 1612ms | whoahaow/rjsxrd |
| `202.50.253.18:19999` | ss | 1636ms | F0rc3Run/F0rc3Run |
| `202.50.253.63:19999` | ss | 1703ms | F0rc3Run/F0rc3Run |
| `du-rov.secureservice.top:8443` | vless | 1705ms | whoahaow/rjsxrd |
| `163.245.41.49:2096` | vless | 1764ms | whoahaow/rjsxrd |
| `176.100.37.154:443` | vless | 1910ms | whoahaow/rjsxrd |
| `yoy-api.bachidze.com:443` | vless | 1929ms | whoahaow/rjsxrd |
| … | 共 53 个 | | |

#### clash（47 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `xunlinknode.csdjhajkshdjkas.com:40006` | ss | 583ms | F0rc3Run/F0rc3Run |
| `34.222.228.125:80` | vless | 716ms | 0xRadikal/Free-v2ray-Configs |
| `56.10.10.106:8443` | ss | 792ms | hello-world-1989/cn-news |
| `167.88.61.52:443` | trojan | 810ms | 0xRadikal/Free-v2ray-Configs |
| `32.199.151.91:80` | vless | 851ms | 0xRadikal/Free-v2ray-Configs |
| `177.177.215.45:444` | vless | 940ms | whoahaow/rjsxrd |
| `157.90.165.181:11762` | vless | 983ms | 0xRadikal/Free-v2ray-Configs |
| `163.245.42.132:443` | vless | 989ms | 0xRadikal/Free-v2ray-Configs |
| `9.247.23.209:443` | vless | 999ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.90:19999` | ss | 1091ms | F0rc3Run/F0rc3Run |
| `202.50.253.45:19999` | ss | 1121ms | F0rc3Run/F0rc3Run |
| `edge.bookmai.com:443` | vless | 1139ms | 0xRadikal/Free-v2ray-Configs |
| `163.245.42.120:443` | vless | 1155ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 1158ms | ermaozi01/free_clash_vpn |
| `202.50.253.54:19999` | ss | 1168ms | ermaozi01/free_clash_vpn |
| `132.243.207.154:443` | vless | 1169ms | 0xRadikal/Free-v2ray-Configs |
| `109.104.153.43:33336` | ssr | 1174ms | barry-far/V2ray-Config |
| `202.50.253.18:19999` | ss | 1175ms | F0rc3Run/F0rc3Run |
| `163.245.42.157:443` | vless | 1183ms | 0xRadikal/Free-v2ray-Configs |
| `de15.h1cloud.net:25362` | vless | 1189ms | Pawdroid/Free-servers |
| `179.43.187.67:443` | vless | 1195ms | 0xRadikal/Free-v2ray-Configs |
| `146.75.57.238:443` | vless | 1214ms | snakem982/proxypool |
| `179.254.92.134:443` | vless | 1250ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.72:19999` | ss | 1309ms | F0rc3Run/F0rc3Run |
| `5.42.99.64:8443` | vless | 1326ms | whoahaow/rjsxrd |
| `13.143.180.142:443` | vless | 1349ms | 0xRadikal/Free-v2ray-Configs |
| `72.56.52.248:443` | vless | 1352ms | snakem982/proxypool |
| `179.253.82.19:4443` | vless | 1376ms | cbusifabcap/daily_free_vpn |
| `46.17.46.27:18443` | ss | 1394ms | F0rc3Run/F0rc3Run |
| `13.143.182.104:443` | vless | 1396ms | 0xRadikal/Free-v2ray-Configs |
| `72.56.241.230:443` | vless | 1403ms | whoahaow/rjsxrd |
| `13.143.182.103:443` | vless | 1436ms | 0xRadikal/Free-v2ray-Configs |
| `179.254.92.190:443` | vless | 1439ms | 0xRadikal/Free-v2ray-Configs |
| `56.10.10.106:443` | vless | 1460ms | hello-world-1989/cn-news |
| `147.45.108.45:443` | vless | 1544ms | 0xRadikal/Free-v2ray-Configs |
| `199.232.78.160:443` | vless | 1607ms | snakem982/proxypool |
| `du-rov.secureservice.top:8443` | vless | 1666ms | whoahaow/rjsxrd |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1761ms | 0xRadikal/Free-v2ray-Configs |
| `5.253.28.240:2443` | vless | 1769ms | 0xRadikal/Free-v2ray-Configs |
| `hydra.yokkastars.com:2443` | vless | 1805ms | 0xRadikal/Free-v2ray-Configs |
| … | 共 47 个 | | |

#### singbox（50 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `hk010.zestapp778.com:31884` | vless | 607ms | kooker/FreeSubsCheck |
| `34.222.228.125:80` | vless | 753ms | 0xRadikal/Free-v2ray-Configs |
| `32.199.151.91:80` | vless | 815ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 995ms | F0rc3Run/F0rc3Run |
| `9.247.23.209:443` | vless | 1054ms | 0xRadikal/Free-v2ray-Configs |
| `163.245.42.132:443` | vless | 1114ms | 0xRadikal/Free-v2ray-Configs |
| `56.10.10.106:8443` | ss | 1154ms | hello-world-1989/cn-news |
| `202.50.253.18:19999` | ss | 1165ms | F0rc3Run/F0rc3Run |
| `202.50.253.81:19999` | ss | 1181ms | ermaozi01/free_clash_vpn |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1195ms | 0xRadikal/Free-v2ray-Configs |
| `132.243.207.154:443` | vless | 1216ms | 0xRadikal/Free-v2ray-Configs |
| `163.245.42.120:443` | vless | 1219ms | 0xRadikal/Free-v2ray-Configs |
| `179.43.187.67:443` | vless | 1263ms | 0xRadikal/Free-v2ray-Configs |
| `167.88.61.52:443` | trojan | 1271ms | 0xRadikal/Free-v2ray-Configs |
| `163.245.42.157:443` | vless | 1283ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.182.104:443` | vless | 1287ms | 0xRadikal/Free-v2ray-Configs |
| `edge.bookmai.com:443` | vless | 1311ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.63:19999` | ss | 1341ms | F0rc3Run/F0rc3Run |
| `147.45.108.45:443` | vless | 1359ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.182.103:443` | vless | 1359ms | 0xRadikal/Free-v2ray-Configs |
| `46.17.46.27:18443` | ss | 1402ms | F0rc3Run/F0rc3Run |
| `200.169.184.168:443` | vless | 1478ms | 0xRadikal/Free-v2ray-Configs |
| `152.175.6.229:31884` | vless | 1493ms | peasoft/NoMoreWalls |
| `201.51.5.181:443` | vless | 1494ms | snakem982/proxypool |
| `202.50.253.54:19999` | ss | 1503ms | ermaozi01/free_clash_vpn |
| `5.42.99.64:8443` | vless | 1580ms | whoahaow/rjsxrd |
| `200.165.231.209:443` | vless | 1595ms | whoahaow/rjsxrd |
| `199.232.78.160:443` | vless | 1683ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 1687ms | F0rc3Run/F0rc3Run |
| `202.50.253.72:19999` | ss | 1718ms | F0rc3Run/F0rc3Run |
| `146.75.59.186:443` | vless | 1764ms | cbusifabcap/daily_free_vpn |
| `du-rov.secureservice.top:8443` | vless | 1769ms | whoahaow/rjsxrd |
| `56.10.10.106:443` | vless | 1782ms | hello-world-1989/cn-news |
| `app-mi-26.spbstudentlife.com:443` | vless | 1801ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.180.142:443` | vless | 1849ms | 0xRadikal/Free-v2ray-Configs |
| `147.45.245.17:443` | vless | 1893ms | whoahaow/rjsxrd |
| `72.56.241.230:443` | vless | 1936ms | whoahaow/rjsxrd |
| `79.182.70.56:25362` | vless | 2117ms | whoahaow/rjsxrd |
| `179.254.92.134:443` | vless | 2181ms | 0xRadikal/Free-v2ray-Configs |
| `177.177.215.45:444` | vless | 2225ms | whoahaow/rjsxrd |
| … | 共 50 个 | | |

## 2026-11-01 23:35

- 预筛：TCP 连通 3682/3698 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：32.6 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2509 | 48 | 1.9% | 3 | 32 | 2426 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2506 | 120 | 4.8% | 1 | 0 | 2385 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2509 | 56 | 2.2% | 0 | 0 | 2453 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2506 | 63 | 2.5% | 0 | 0 | 2443 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1385 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 1039 |
| v2ray | 配置被内核拒绝（参数不符） | 32 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 3 |
| v2ray | 连接被重置 | 2 |
| xray | 连接超时 | 1427 |
| xray | TLS 握手失败（证书/协议不匹配） | 600 |
| xray | 网络层失败 | 349 |
| xray | 连接被重置 | 9 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1769 |
| clash | TLS 握手失败（证书/协议不匹配） | 427 |
| clash | 网络层失败 | 256 |
| clash | 连接被重置 | 1 |
| singbox | 连接被重置 | 1882 |
| singbox | TLS 握手失败（证书/协议不匹配） | 560 |
| singbox | 认证失败（口令/UUID 不符） | 1 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 214 | 33 | 15 | `pool/pool_v2ray.txt` |
| xray | 520 | 68 | 52 | `pool/pool_xray.txt` |
| clash | 389 | 39 | 17 | `pool/pool_clash.yaml` |
| singbox | 329 | 44 | 19 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| hello-world-1989/cn-news | 10 | 6 | 60% | 462ms | 69.2 |
| F0rc3Run/F0rc3Run | 12 | 7 | 58% | 1504ms | 61.8 |
| snakem982/proxypool | 104 | 36 | 35% | 1772ms | 43.6 |
| peasoft/NoMoreWalls | 341 | 23 | 7% | 1881ms | 23.4 |
| shabane/kamaji | 255 | 17 | 7% | 1473ms | 25.8 |
| whoahaow/rjsxrd | 1875 | 101 | 5% | 1762ms | 23.2 |
| NiREvil/vless | 1406 | 53 | 4% | 1418ms | 24.1 |
| kooker/FreeSubsCheck | 197 | 4 | 2% | 1255ms | 23.9 |
| nyeinkokoaung404/V2ray-Configs | 3582 | 40 | 1% | 1973ms | 18.9 |
| Delta-Kronecker/V2ray-Config | 2003 | 0 | 0% | -ms | 0.0 |
| sinavm/SVM | 60 | 0 | 0% | -ms | 0.0 |
| DukeMehdi/FreeList-V2ray-Configs | 154 | 0 | 0% | -ms | 0.0 |
| igareck/vpn-configs-for-russia | 12 | 0 | 0% | -ms | 0.0 |
| crashgfw/free-airport-nodes | 6 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 11 | 0 | 0% | -ms | 0.0 |
| sakha1370/OpenRay | 2 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（48 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.125.163.184:8443` | ss | 293ms | hello-world-1989/cn-news |
| `ench-snet-app.w-ctrip.cn:43638` | trojan | 514ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:47786` | trojan | 735ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:45502` | trojan | 833ms | peasoft/NoMoreWalls |
| `178.83.111.166:3090` | vless | 929ms | NiREvil/vless |
| `202.50.253.18:19999` | ss | 951ms | nyeinkokoaung404/V2ray-Configs |
| `85.155.179.206:443` | vless | 956ms | whoahaow/rjsxrd |
| `88.216.69.253:443` | vless | 991ms | nyeinkokoaung404/V2ray-Configs |
| `us3.shtil.io:443` | vless | 1050ms | whoahaow/rjsxrd |
| `178.83.111.151:3090` | vless | 1067ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:24133` | trojan | 1162ms | peasoft/NoMoreWalls |
| `77.216.2.178:30` | ss | 1172ms | F0rc3Run/F0rc3Run |
| `199.232.78.120:443` | trojan | 1201ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:45503` | trojan | 1223ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 1274ms | nyeinkokoaung404/V2ray-Configs |
| `202.50.253.90:19999` | ss | 1280ms | nyeinkokoaung404/V2ray-Configs |
| `ench-snet-app.w-ctrip.cn:35929` | trojan | 1280ms | snakem982/proxypool |
| `mirajh.morteza1388m1122.ir:30299` | ss | 1311ms | NiREvil/vless |
| `46.17.46.27:18443` | ss | 1316ms | F0rc3Run/F0rc3Run |
| `ench-snet-app.w-ctrip.cn:42338` | trojan | 1337ms | snakem982/proxypool |
| `141.0.187.6:2083` | vless | 1374ms | whoahaow/rjsxrd |
| `b2friday.buzrel.ir:443` | ss | 1415ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:53004` | trojan | 1427ms | snakem982/proxypool |
| `176.114.95.242:443` | trojan | 1433ms | whoahaow/rjsxrd |
| `200.165.231.209:443` | vless | 1465ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 1474ms | nyeinkokoaung404/V2ray-Configs |
| `95.81.102.121:443` | vless | 1511ms | NiREvil/vless |
| `49.51.39.148:443` | ss | 1517ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 1535ms | nyeinkokoaung404/V2ray-Configs |
| `jp032008.ssgreen.org:443` | vmess | 1697ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:38994` | trojan | 1858ms | snakem982/proxypool |
| `217.60.73.56:443` | hysteria2 | 1919ms | whoahaow/rjsxrd |
| `www.qarvian.ir:443` | vless | 1977ms | peasoft/NoMoreWalls |
| `45.88.12.120:443` | hysteria2 | 2037ms | whoahaow/rjsxrd |
| `151.101.201.242:443` | vless | 2235ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:22003` | trojan | 2262ms | peasoft/NoMoreWalls |
| `146.75.37.242:443` | vless | 2274ms | whoahaow/rjsxrd |
| `wstg.datasynctrue.online:443` | vless | 2281ms | whoahaow/rjsxrd |
| `wwww.qarvian.ir:443` | vless | 2329ms | nyeinkokoaung404/V2ray-Configs |
| `202.50.253.63:19999` | ss | 2340ms | nyeinkokoaung404/V2ray-Configs |
| … | 共 48 个 | | |

#### xray（120 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.125.163.184:8443` | ss | 385ms | hello-world-1989/cn-news |
| `13.125.163.184:443` | vless | 464ms | hello-world-1989/cn-news |
| `49.51.39.148:443` | ss | 590ms | NiREvil/vless |
| `85.155.179.206:443` | vless | 859ms | whoahaow/rjsxrd |
| `62.233.33.127:8443` | vless | 880ms | whoahaow/rjsxrd |
| `91.132.48.199:443` | vless | 894ms | NiREvil/vless |
| `us3.shtil.io:443` | vless | 896ms | whoahaow/rjsxrd |
| `62.233.33.118:8443` | vless | 903ms | NiREvil/vless |
| `94.183.152.153:443` | vless | 905ms | shabane/kamaji |
| `62.233.33.126:8443` | vless | 934ms | NiREvil/vless |
| `edge.bookmai.com:443` | vless | 939ms | shabane/kamaji |
| `62.233.33.229:8443` | vless | 940ms | whoahaow/rjsxrd |
| `202.50.253.36:19999` | ss | 948ms | nyeinkokoaung404/V2ray-Configs |
| `79.182.39.75:25362` | vless | 961ms | NiREvil/vless |
| `62.233.33.178:8443` | vless | 962ms | NiREvil/vless |
| `162.35.191.50:25389` | vless | 964ms | whoahaow/rjsxrd |
| `195.189.98.197:443` | vless | 976ms | whoahaow/rjsxrd |
| `62.233.33.177:8443` | vless | 979ms | NiREvil/vless |
| `202.50.253.45:19999` | ss | 985ms | nyeinkokoaung404/V2ray-Configs |
| `62.233.33.181:8443` | vless | 994ms | NiREvil/vless |
| `2.26.6.244:443` | vless | 1001ms | NiREvil/vless |
| `38.244.5.231:443` | vless | 1008ms | NiREvil/vless |
| `62.233.33.117:8443` | vless | 1009ms | whoahaow/rjsxrd |
| `79.182.39.236:25362` | vless | 1012ms | NiREvil/vless |
| `72.56.52.248:443` | vless | 1013ms | whoahaow/rjsxrd |
| `9.247.23.209:443` | vless | 1035ms | shabane/kamaji |
| `177.177.215.45:444` | vless | 1036ms | whoahaow/rjsxrd |
| `84.32.177.63:443` | vless | 1046ms | whoahaow/rjsxrd |
| `89.125.11.155:443` | vless | 1059ms | NiREvil/vless |
| `89.125.11.238:8443` | vless | 1071ms | whoahaow/rjsxrd |
| `89.125.11.187:8443` | vless | 1088ms | NiREvil/vless |
| `89.125.11.149:8443` | vless | 1101ms | NiREvil/vless |
| `89.125.11.148:8443` | vless | 1101ms | NiREvil/vless |
| `89.125.11.188:8443` | vless | 1112ms | NiREvil/vless |
| `46.29.27.3:443` | vless | 1114ms | whoahaow/rjsxrd |
| `185.186.78.170:2083` | vless | 1124ms | shabane/kamaji |
| `89.125.11.147:443` | vless | 1133ms | NiREvil/vless |
| `132.243.207.154:443` | vless | 1145ms | whoahaow/rjsxrd |
| `72.56.52.229:443` | vless | 1146ms | whoahaow/rjsxrd |
| `163.245.42.157:443` | vless | 1172ms | shabane/kamaji |
| … | 共 120 个 | | |

#### clash（56 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.125.163.184:8443` | ss | 275ms | hello-world-1989/cn-news |
| `7gqt4-g01.jp04-3771-vm0.entry.fr0307a.art:444` | vmess | 399ms | nyeinkokoaung404/V2ray-Configs |
| `hik160.pacemakere.com:20014` | trojan | 587ms | snakem982/proxypool |
| `49.51.39.148:443` | ss | 641ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:15589` | trojan | 808ms | peasoft/NoMoreWalls |
| `ench-snet-app.w-ctrip.cn:22003` | trojan | 831ms | peasoft/NoMoreWalls |
| `ench-snet-app.w-ctrip.cn:47786` | trojan | 888ms | snakem982/proxypool |
| `85.155.179.206:443` | vless | 903ms | whoahaow/rjsxrd |
| `177.177.215.45:444` | vless | 909ms | whoahaow/rjsxrd |
| `77.216.2.178:30` | ss | 1032ms | F0rc3Run/F0rc3Run |
| `163.245.42.132:443` | vless | 1035ms | kooker/FreeSubsCheck |
| `202.50.253.36:19999` | ss | 1037ms | nyeinkokoaung404/V2ray-Configs |
| `47.129.229.144:443` | vless | 1038ms | hello-world-1989/cn-news |
| `202.50.253.45:19999` | ss | 1039ms | nyeinkokoaung404/V2ray-Configs |
| `72.56.52.229:443` | vless | 1074ms | whoahaow/rjsxrd |
| `9.247.23.209:443` | vless | 1081ms | shabane/kamaji |
| `92.243.74.224:8443` | vless | 1155ms | whoahaow/rjsxrd |
| `13.143.180.141:443` | vless | 1178ms | snakem982/proxypool |
| `72.56.52.248:443` | vless | 1190ms | whoahaow/rjsxrd |
| `202.50.253.18:19999` | ss | 1204ms | nyeinkokoaung404/V2ray-Configs |
| `mdk.mdmekjll.best:80` | vmess | 1204ms | nyeinkokoaung404/V2ray-Configs |
| `ench-snet-app.w-ctrip.cn:45503` | trojan | 1216ms | snakem982/proxypool |
| `edge.bookmai.com:443` | vless | 1237ms | shabane/kamaji |
| `ench-snet-app.w-ctrip.cn:45502` | trojan | 1261ms | peasoft/NoMoreWalls |
| `us.huahua.wiki:443` | vless | 1270ms | kooker/FreeSubsCheck |
| `191.217.245.227:443` | vless | 1294ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1323ms | nyeinkokoaung404/V2ray-Configs |
| `13.143.180.142:443` | vless | 1431ms | whoahaow/rjsxrd |
| `141.0.187.6:2083` | vless | 1463ms | whoahaow/rjsxrd |
| `141.0.187.4:2083` | vless | 1525ms | whoahaow/rjsxrd |
| `ench-snet-app.w-ctrip.cn:26429` | trojan | 1542ms | peasoft/NoMoreWalls |
| `ench-snet-app.w-ctrip.cn:29628` | trojan | 1558ms | peasoft/NoMoreWalls |
| `46.17.46.27:18443` | ss | 1607ms | F0rc3Run/F0rc3Run |
| `191.217.245.10:443` | vless | 1644ms | whoahaow/rjsxrd |
| `45.198.0.101:443` | vless | 1723ms | whoahaow/rjsxrd |
| `ench-snet-app.w-ctrip.cn:24133` | trojan | 1733ms | peasoft/NoMoreWalls |
| `fl3.nexfile.net:4443` | vless | 1739ms | whoahaow/rjsxrd |
| `146.75.59.186:443` | vless | 1764ms | nyeinkokoaung404/V2ray-Configs |
| `45.88.12.120:443` | hysteria2 | 1812ms | whoahaow/rjsxrd |
| `202.50.253.63:19999` | ss | 1831ms | nyeinkokoaung404/V2ray-Configs |
| … | 共 56 个 | | |

#### singbox（63 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.125.163.184:8443` | ss | 315ms | hello-world-1989/cn-news |
| `7gqt4-g01.jp04-3771-vm0.entry.fr0307a.art:444` | vmess | 475ms | nyeinkokoaung404/V2ray-Configs |
| `hik160.pacemakere.com:20014` | trojan | 738ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:42338` | trojan | 900ms | snakem982/proxypool |
| `85.155.179.206:443` | vless | 903ms | whoahaow/rjsxrd |
| `ench-snet-app.w-ctrip.cn:15589` | trojan | 910ms | peasoft/NoMoreWalls |
| `ench-snet-app.w-ctrip.cn:29628` | trojan | 1033ms | peasoft/NoMoreWalls |
| `uae.purchasebot.net:443` | vless | 1038ms | whoahaow/rjsxrd |
| `9.247.23.209:443` | vless | 1076ms | shabane/kamaji |
| `72.56.52.229:443` | vless | 1081ms | whoahaow/rjsxrd |
| `ench-snet-app.w-ctrip.cn:24133` | trojan | 1091ms | peasoft/NoMoreWalls |
| `202.50.253.27:19999` | ss | 1130ms | nyeinkokoaung404/V2ray-Configs |
| `177.177.215.45:444` | vless | 1141ms | whoahaow/rjsxrd |
| `163.245.42.132:443` | vless | 1204ms | kooker/FreeSubsCheck |
| `163.245.42.157:443` | vless | 1260ms | shabane/kamaji |
| `13.143.180.142:443` | vless | 1268ms | whoahaow/rjsxrd |
| `72.56.52.248:443` | vless | 1294ms | whoahaow/rjsxrd |
| `43.153.90.117:443` | vless | 1358ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:22100` | trojan | 1371ms | peasoft/NoMoreWalls |
| `edge.bookmai.com:443` | vless | 1380ms | shabane/kamaji |
| `46.17.46.27:18443` | ss | 1391ms | F0rc3Run/F0rc3Run |
| `191.217.245.227:443` | vless | 1399ms | whoahaow/rjsxrd |
| `mirajh.morteza1388m1122.ir:30299` | ss | 1411ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:41184` | trojan | 1413ms | snakem982/proxypool |
| `us.huahua.wiki:443` | vless | 1510ms | kooker/FreeSubsCheck |
| `ench-snet-app.w-ctrip.cn:45503` | trojan | 1517ms | snakem982/proxypool |
| `141.0.187.4:2083` | vless | 1538ms | whoahaow/rjsxrd |
| `191.217.245.10:443` | vless | 1550ms | whoahaow/rjsxrd |
| `13.143.180.141:443` | vless | 1574ms | snakem982/proxypool |
| `200.165.231.209:443` | vless | 1584ms | whoahaow/rjsxrd |
| `p2real1.greewebservices.ir:1310` | vless | 1617ms | NiREvil/vless |
| `b2friday.buzrel.ir:443` | ss | 1625ms | NiREvil/vless |
| `ench-snet-app.w-ctrip.cn:35929` | trojan | 1638ms | snakem982/proxypool |
| `ench-snet-app.w-ctrip.cn:53004` | trojan | 1638ms | snakem982/proxypool |
| `72.56.241.230:443` | vless | 1647ms | whoahaow/rjsxrd |
| `202.50.253.81:19999` | ss | 1677ms | nyeinkokoaung404/V2ray-Configs |
| `202.50.253.99:19999` | ss | 1746ms | nyeinkokoaung404/V2ray-Configs |
| `us3.shtil.io:443` | vless | 1938ms | whoahaow/rjsxrd |
| `151.101.201.242:443` | vless | 1999ms | snakem982/proxypool |
| `45.88.12.120:443` | hysteria2 | 2079ms | whoahaow/rjsxrd |
| … | 共 63 个 | | |

## 2026-10-31 23:01

- 预筛：TCP 连通 7673/7760 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：34.9 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2506 | 54 | 2.2% | 4 | 37 | 2411 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2505 | 122 | 4.9% | 1 | 0 | 2382 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2507 | 60 | 2.4% | 0 | 15 | 2432 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2503 | 55 | 2.2% | 0 | 17 | 2431 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1362 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 1048 |
| v2ray | 配置被内核拒绝（参数不符） | 37 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 4 |
| v2ray | 网络层失败 | 1 |
| xray | 连接超时 | 1389 |
| xray | TLS 握手失败（证书/协议不匹配） | 659 |
| xray | 网络层失败 | 322 |
| xray | 连接被重置 | 12 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1304 |
| clash | 网络层失败 | 701 |
| clash | TLS 握手失败（证书/协议不匹配） | 427 |
| clash | 配置被内核拒绝（参数不符） | 15 |
| singbox | 连接被重置 | 1828 |
| singbox | TLS 握手失败（证书/协议不匹配） | 601 |
| singbox | 配置被内核拒绝（参数不符） | 17 |
| singbox | 认证失败（口令/UUID 不符） | 1 |
| singbox | 连接被拒绝 | 1 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 181 | 34 | 20 | `pool/pool_v2ray.txt` |
| xray | 452 | 85 | 37 | `pool/pool_xray.txt` |
| clash | 350 | 43 | 17 | `pool/pool_clash.yaml` |
| singbox | 285 | 34 | 21 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| nyeinkokoaung404/V2ray-Configs | 1 | 1 | 100% | 1635ms | 90.2 |
| hello-world-1989/cn-news | 6 | 2 | 33% | 1790ms | 42.6 |
| F0rc3Run/F0rc3Run | 68 | 21 | 31% | 1662ms | 41.6 |
| peasoft/NoMoreWalls | 85 | 10 | 12% | 2723ms | 21.9 |
| sinavm/SVM | 104 | 11 | 11% | 2381ms | 23.1 |
| snakem982/proxypool | 128 | 13 | 10% | 1822ms | 26.2 |
| shabane/kamaji | 340 | 19 | 6% | 2354ms | 19.8 |
| whoahaow/rjsxrd | 1684 | 77 | 5% | 1842ms | 22.1 |
| kooker/FreeSubsCheck | 518 | 21 | 4% | 2074ms | 20.4 |
| danmaifu/mianfeijiedian | 895 | 32 | 4% | 2512ms | 17.4 |
| NiREvil/vless | 4058 | 77 | 2% | 1796ms | 20.6 |
| Delta-Kronecker/V2ray-Config | 1465 | 7 | 0% | 2726ms | 14.0 |
| Barabama/FreeNodes | 179 | 0 | 0% | -ms | 0.0 |
| sakha1370/OpenRay | 60 | 0 | 0% | -ms | 0.0 |
| SoliSpirit/v2ray-configs | 416 | 0 | 0% | -ms | 0.0 |
| crashgfw/free-airport-nodes | 3 | 0 | 0% | -ms | 0.0 |
| Pawdroid/Free-servers | 11 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（54 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.143.175.202:116` | vmess | 725ms | NiREvil/vless |
| `177.3.215.199:1125` | vmess | 870ms | NiREvil/vless |
| `141.98.7.19:1114` | vmess | 932ms | NiREvil/vless |
| `153.52.92.224:116` | vmess | 939ms | NiREvil/vless |
| `93.157.138.137:1125` | vmess | 976ms | NiREvil/vless |
| `para.kiavoosh.online:116` | vmess | 1018ms | NiREvil/vless |
| `202.50.253.18:19999` | ss | 1035ms | F0rc3Run/F0rc3Run |
| `202.50.253.81:19999` | ss | 1043ms | shabane/kamaji |
| `202.50.253.54:19999` | ss | 1046ms | F0rc3Run/F0rc3Run |
| `hik160.pacemakere.com:20014` | trojan | 1084ms | NiREvil/vless |
| `179.253.179.109:50083` | vless | 1253ms | whoahaow/rjsxrd |
| `179.253.179.109:63053` | vless | 1254ms | NiREvil/vless |
| `niroo.kiavoosh.online:1125` | vmess | 1362ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 1423ms | sinavm/SVM |
| `194.26.229.214:2200` | vless | 1428ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 1433ms | kooker/FreeSubsCheck |
| `132.243.67.109:443` | vless | 1526ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1537ms | F0rc3Run/F0rc3Run |
| `200.165.231.209:443` | vless | 1555ms | whoahaow/rjsxrd |
| `95.81.102.121:443` | vless | 1570ms | whoahaow/rjsxrd |
| `141.133.174.88:443` | trojan | 1578ms | danmaifu/mianfeijiedian |
| `88.216.195.188:443` | hysteria2 | 1670ms | whoahaow/rjsxrd |
| `cf.0sm.com:443` | vmess | 1707ms | danmaifu/mianfeijiedian |
| `176.114.95.242:443` | trojan | 1726ms | kooker/FreeSubsCheck |
| `202.50.253.63:19999` | ss | 1756ms | F0rc3Run/F0rc3Run |
| `194.87.143.165:8443` | vless | 1779ms | kooker/FreeSubsCheck |
| `199.232.78.160:443` | vless | 1815ms | danmaifu/mianfeijiedian |
| `202.50.253.36:19999` | ss | 1830ms | F0rc3Run/F0rc3Run |
| `146.75.57.238:443` | vless | 1846ms | danmaifu/mianfeijiedian |
| `ph001.zestapp778.com:46298` | trojan | 1912ms | NiREvil/vless |
| `wwww.qarvian.ir:443` | vless | 1949ms | danmaifu/mianfeijiedian |
| `202.50.253.45:19999` | ss | 1952ms | sinavm/SVM |
| `8.211.1.139:443` | vmess | 1982ms | NiREvil/vless |
| `179.253.179.109:63080` | vless | 2100ms | whoahaow/rjsxrd |
| `bzqhefrtvpqyiuqb.v.3dns.vip:443` | vmess | 2171ms | shabane/kamaji |
| `179.253.179.109:57043` | vless | 2201ms | NiREvil/vless |
| `83.147.254.59:2053` | trojan | 2350ms | kooker/FreeSubsCheck |
| `91.250.248.151:443` | trojan | 2407ms | peasoft/NoMoreWalls |
| `179.253.179.109:62083` | vless | 2442ms | NiREvil/vless |
| `179.253.179.109:30443` | vless | 2472ms | NiREvil/vless |
| … | 共 54 个 | | |

#### xray（122 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `141.98.7.19:1114` | vmess | 766ms | NiREvil/vless |
| `177.3.215.199:1125` | vmess | 854ms | NiREvil/vless |
| `163.245.42.120:443` | vless | 925ms | NiREvil/vless |
| `202.50.253.90:19999` | ss | 929ms | F0rc3Run/F0rc3Run |
| `62.233.33.178:8443` | vless | 981ms | whoahaow/rjsxrd |
| `195.189.98.197:443` | vless | 1010ms | whoahaow/rjsxrd |
| `88.216.70.39:443` | vless | 1037ms | whoahaow/rjsxrd |
| `shorts.blog-forme.ru:443` | vless | 1050ms | NiREvil/vless |
| `31.76.81.137:1114` | vmess | 1051ms | NiREvil/vless |
| `84.32.101.102:443` | vless | 1072ms | whoahaow/rjsxrd |
| `89.125.11.151:443` | vless | 1072ms | whoahaow/rjsxrd |
| `13.143.175.202:116` | vmess | 1073ms | NiREvil/vless |
| `88.216.195.188:443` | hysteria2 | 1077ms | whoahaow/rjsxrd |
| `163.245.42.132:443` | vless | 1102ms | kooker/FreeSubsCheck |
| `89.125.11.149:8443` | vless | 1106ms | whoahaow/rjsxrd |
| `89.125.11.155:443` | vless | 1107ms | whoahaow/rjsxrd |
| `202.50.253.63:19999` | ss | 1130ms | F0rc3Run/F0rc3Run |
| `89.125.11.187:8443` | vless | 1142ms | whoahaow/rjsxrd |
| `89.125.11.148:8443` | vless | 1146ms | whoahaow/rjsxrd |
| `62.233.33.126:8443` | vless | 1152ms | whoahaow/rjsxrd |
| `62.233.33.127:8443` | vless | 1156ms | NiREvil/vless |
| `2.26.6.244:443` | vless | 1186ms | NiREvil/vless |
| `185.186.78.170:2083` | vless | 1191ms | whoahaow/rjsxrd |
| `207.148.80.199:443` | vless | 1205ms | snakem982/proxypool |
| `23.94.252.67:443` | vless | 1240ms | NiREvil/vless |
| `144.31.62.224:443` | vless | 1242ms | NiREvil/vless |
| `212.34.128.120:2083` | vless | 1259ms | whoahaow/rjsxrd |
| `144.31.4.234:443` | vless | 1262ms | whoahaow/rjsxrd |
| `niroo.kiavoosh.online:1125` | vmess | 1266ms | NiREvil/vless |
| `132.243.67.109:443` | vless | 1310ms | whoahaow/rjsxrd |
| `89.125.11.147:443` | vless | 1319ms | whoahaow/rjsxrd |
| `217.60.151.222:443` | vless | 1349ms | whoahaow/rjsxrd |
| `84.32.177.63:443` | vless | 1365ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 1382ms | F0rc3Run/F0rc3Run |
| `89.125.11.153:8443` | vless | 1398ms | whoahaow/rjsxrd |
| `132.243.230.251:443` | vless | 1406ms | whoahaow/rjsxrd |
| `212.34.128.120:443` | vless | 1437ms | whoahaow/rjsxrd |
| `62.233.33.124:443` | vless | 1438ms | NiREvil/vless |
| `2.26.6.244:8443` | vless | 1448ms | NiREvil/vless |
| `200.165.231.209:443` | vless | 1502ms | whoahaow/rjsxrd |
| … | 共 122 个 | | |

#### clash（60 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `edge.bookmai.com:443` | vless | 962ms | shabane/kamaji |
| `9.247.23.209:443` | vless | 978ms | shabane/kamaji |
| `153.52.92.224:116` | vmess | 1044ms | NiREvil/vless |
| `163.245.42.157:443` | vless | 1048ms | shabane/kamaji |
| `202.50.253.18:19999` | ss | 1081ms | F0rc3Run/F0rc3Run |
| `177.3.215.199:1125` | vmess | 1084ms | NiREvil/vless |
| `202.50.253.36:19999` | ss | 1156ms | F0rc3Run/F0rc3Run |
| `de8.vpngold.ru:8443` | vless | 1168ms | whoahaow/rjsxrd |
| `hik160.pacemakere.com:20014` | trojan | 1211ms | NiREvil/vless |
| `niroo.kiavoosh.online:1125` | vmess | 1223ms | NiREvil/vless |
| `132.243.67.109:443` | vless | 1244ms | whoahaow/rjsxrd |
| `84.32.184.218:443` | vless | 1286ms | NiREvil/vless |
| `72.56.235.137:443` | vless | 1374ms | snakem982/proxypool |
| `promo3.goonars.com:443` | hysteria2 | 1380ms | NiREvil/vless |
| `88.216.195.188:443` | hysteria2 | 1433ms | whoahaow/rjsxrd |
| `206.1.97.108:25021` | vless | 1527ms | snakem982/proxypool |
| `185.229.9.135:443` | vless | 1560ms | snakem982/proxypool |
| `200.165.231.209:443` | vless | 1591ms | whoahaow/rjsxrd |
| `8.211.1.139:443` | vmess | 1597ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 1603ms | kooker/FreeSubsCheck |
| `109.104.153.43:33336` | ssr | 1635ms | nyeinkokoaung404/V2ray-Configs |
| `146.75.57.238:443` | vless | 1661ms | danmaifu/mianfeijiedian |
| `138.68.104.9:30161` | vless | 1725ms | peasoft/NoMoreWalls |
| `202.50.253.81:19999` | ss | 1777ms | shabane/kamaji |
| `179.253.179.109:54083` | vless | 1790ms | whoahaow/rjsxrd |
| `194.87.143.165:8443` | vless | 1828ms | kooker/FreeSubsCheck |
| `para.kiavoosh.online:116` | vmess | 1850ms | NiREvil/vless |
| `202.50.253.63:19999` | ss | 1889ms | F0rc3Run/F0rc3Run |
| `199.232.239.239:443` | vless | 1971ms | kooker/FreeSubsCheck |
| `179.253.179.109:62083` | vless | 1973ms | NiREvil/vless |
| `109.248.170.245:443` | trojan | 2023ms | danmaifu/mianfeijiedian |
| `202.50.55.76:443` | trojan | 2038ms | danmaifu/mianfeijiedian |
| `hydra.yokkastars.com:2443` | vless | 2186ms | danmaifu/mianfeijiedian |
| `217.60.73.56:443` | hysteria2 | 2290ms | snakem982/proxypool |
| `109.234.211.232:443` | trojan | 2336ms | sinavm/SVM |
| `46.174.142.238:443` | trojan | 2355ms | kooker/FreeSubsCheck |
| `176.114.95.242:443` | trojan | 2369ms | kooker/FreeSubsCheck |
| `wwww.qarvian.ir:443` | vless | 2408ms | danmaifu/mianfeijiedian |
| `193.17.183.48:443` | trojan | 2476ms | danmaifu/mianfeijiedian |
| `93.157.138.137:1125` | vmess | 2532ms | NiREvil/vless |
| … | 共 60 个 | | |

#### singbox（55 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `141.98.7.19:1114` | vmess | 772ms | NiREvil/vless |
| `13.143.175.202:116` | vmess | 896ms | NiREvil/vless |
| `202.50.253.90:19999` | ss | 979ms | F0rc3Run/F0rc3Run |
| `163.245.42.157:443` | vless | 1001ms | shabane/kamaji |
| `153.52.92.224:116` | vmess | 1054ms | NiREvil/vless |
| `177.3.215.199:1125` | vmess | 1160ms | NiREvil/vless |
| `163.245.42.132:443` | vless | 1227ms | kooker/FreeSubsCheck |
| `179.253.179.109:57043` | vless | 1268ms | NiREvil/vless |
| `promo3.goonars.com:443` | hysteria2 | 1319ms | NiREvil/vless |
| `202.50.253.63:19999` | ss | 1361ms | F0rc3Run/F0rc3Run |
| `edge.bookmai.com:443` | vless | 1381ms | shabane/kamaji |
| `9.247.23.209:443` | vless | 1405ms | shabane/kamaji |
| `104.171.135.229:443` | vless | 1464ms | snakem982/proxypool |
| `ph001.zestapp778.com:46298` | trojan | 1476ms | NiREvil/vless |
| `132.243.67.109:443` | vless | 1514ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 1590ms | F0rc3Run/F0rc3Run |
| `95.81.102.121:443` | vless | 1647ms | whoahaow/rjsxrd |
| `194.87.143.165:8443` | vless | 1655ms | kooker/FreeSubsCheck |
| `179.253.179.109:63080` | vless | 1657ms | whoahaow/rjsxrd |
| `179.253.179.109:54083` | vless | 1663ms | whoahaow/rjsxrd |
| `201.24.121.243:443` | vless | 1684ms | kooker/FreeSubsCheck |
| `207.148.80.199:443` | vless | 1729ms | snakem982/proxypool |
| `199.232.78.160:443` | vless | 1733ms | danmaifu/mianfeijiedian |
| `190.93.245.148:443` | trojan | 1744ms | shabane/kamaji |
| `104.16.34.14:443` | trojan | 1746ms | sinavm/SVM |
| `3.36.61.213:443` | vless | 1751ms | hello-world-1989/cn-news |
| `para.kiavoosh.online:116` | vmess | 1779ms | NiREvil/vless |
| `niroo.kiavoosh.online:1125` | vmess | 1794ms | NiREvil/vless |
| `146.75.57.238:443` | vless | 1815ms | danmaifu/mianfeijiedian |
| `144.31.190.230:8443` | vless | 1857ms | whoahaow/rjsxrd |
| `31.76.0.15:443` | trojan | 1878ms | peasoft/NoMoreWalls |
| `207.57.132.189:8443` | trojan | 1929ms | kooker/FreeSubsCheck |
| `72.56.241.230:443` | vless | 1945ms | whoahaow/rjsxrd |
| `wwww.qarvian.ir:443` | vless | 1972ms | danmaifu/mianfeijiedian |
| `217.60.73.56:443` | hysteria2 | 1980ms | snakem982/proxypool |
| `72.56.235.137:443` | vless | 2054ms | snakem982/proxypool |
| `31.76.81.137:1114` | vmess | 2231ms | NiREvil/vless |
| `185.146.234.242:443` | trojan | 2288ms | peasoft/NoMoreWalls |
| `202.50.253.18:19999` | ss | 2323ms | F0rc3Run/F0rc3Run |
| `200.165.231.209:443` | vless | 2403ms | whoahaow/rjsxrd |
| … | 共 55 个 | | |

## 2026-10-30 23:00

- 预筛：TCP 连通 3405/3439 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：32.1 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2502 | 35 | 1.4% | 4 | 36 | 2427 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2505 | 95 | 3.8% | 1 | 0 | 2409 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2507 | 49 | 2.0% | 0 | 0 | 2458 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2506 | 35 | 1.4% | 0 | 1 | 2470 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1718 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 702 |
| v2ray | 配置被内核拒绝（参数不符） | 36 |
| v2ray | 内核启动失败或超时 | 5 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 4 |
| v2ray | 连接被重置 | 2 |
| xray | 连接超时 | 1355 |
| xray | TLS 握手失败（证书/协议不匹配） | 784 |
| xray | 网络层失败 | 259 |
| xray | 连接被重置 | 11 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| clash | 连接超时 | 1701 |
| clash | TLS 握手失败（证书/协议不匹配） | 397 |
| clash | 网络层失败 | 360 |
| singbox | 连接被重置 | 1952 |
| singbox | TLS 握手失败（证书/协议不匹配） | 517 |
| singbox | 认证失败（口令/UUID 不符） | 1 |
| singbox | 配置被内核拒绝（参数不符） | 1 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 147 | 20 | 15 | `pool/pool_v2ray.txt` |
| xray | 367 | 63 | 32 | `pool/pool_xray.txt` |
| clash | 307 | 31 | 18 | `pool/pool_clash.yaml` |
| singbox | 251 | 21 | 14 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| F0rc3Run/F0rc3Run | 119 | 37 | 31% | 1949ms | 40.1 |
| hello-world-1989/cn-news | 6 | 1 | 17% | 4141ms | 16.8 |
| Pawdroid/Free-servers | 23 | 3 | 13% | 1676ms | 29.1 |
| kooker/FreeSubsCheck | 41 | 3 | 7% | 2048ms | 22.8 |
| snakem982/proxypool | 202 | 12 | 6% | 2020ms | 22.0 |
| peasoft/NoMoreWalls | 111 | 6 | 5% | 2163ms | 20.8 |
| whoahaow/rjsxrd | 480 | 17 | 4% | 1628ms | 22.7 |
| NiREvil/vless | 7153 | 135 | 2% | 1866ms | 20.1 |
| cbusifabcap/daily_free_vpn | 61 | 0 | 0% | -ms | 0.0 |
| barry-far/V2ray-Config | 281 | 0 | 0% | -ms | 0.0 |
| iboxz/free-v2ray-collector | 20 | 0 | 0% | -ms | 0.0 |
| 0xRadikal/Free-v2ray-Configs | 32 | 0 | 0% | -ms | 0.0 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 1465 | 0 | 0% | -ms | 0.0 |
| igareck/vpn-configs-for-russia | 4 | 0 | 0% | -ms | 0.0 |
| nyeinkokoaung404/V2ray-Configs | 5 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 12 | 0 | 0% | -ms | 0.0 |
| sakha1370/OpenRay | 2 | 0 | 0% | -ms | 0.0 |
| WLget/V2Ray_configs_64 | 2 | 0 | 0% | -ms | 0.0 |
| Danialsamadi/v2go | 1 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（35 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `80.243.228.61:2085` | vless | 916ms | NiREvil/vless |
| `jp-1.bnc-gt.co.uk:443` | vless | 957ms | NiREvil/vless |
| `179.253.179.109:50083` | vless | 988ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 1073ms | Pawdroid/Free-servers |
| `185.22.155.121:18443` | ss | 1110ms | F0rc3Run/F0rc3Run |
| `130.78.190.21:443` | vless | 1271ms | NiREvil/vless |
| `189.74.114.93:443` | vless | 1289ms | NiREvil/vless |
| `dns22.m3hrzd.ir:1346` | ss | 1303ms | NiREvil/vless |
| `176.114.95.242:443` | trojan | 1305ms | whoahaow/rjsxrd |
| `179.253.179.109:54443` | vless | 1313ms | whoahaow/rjsxrd |
| `202.50.253.27:19999` | ss | 1336ms | F0rc3Run/F0rc3Run |
| `13.143.176.83:443` | vless | 1338ms | NiREvil/vless |
| `59.125.69.22:443` | vless | 1367ms | NiREvil/vless |
| `46.17.46.27:18443` | ss | 1432ms | kooker/FreeSubsCheck |
| `179.253.179.109:62083` | vless | 1438ms | whoahaow/rjsxrd |
| `194.87.143.165:8443` | vless | 1472ms | snakem982/proxypool |
| `200.165.231.209:443` | vless | 1599ms | NiREvil/vless |
| `104.16.34.14:443` | trojan | 1611ms | NiREvil/vless |
| `wstg.datasynctrue.online:443` | vless | 1682ms | NiREvil/vless |
| `146.75.59.186:443` | vless | 1782ms | NiREvil/vless |
| `132.243.66.98:443` | vless | 1812ms | whoahaow/rjsxrd |
| `199.232.78.160:443` | vless | 1829ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 1893ms | peasoft/NoMoreWalls |
| `api.mediaklenov.cc:443` | vless | 1900ms | NiREvil/vless |
| `104.21.102.36:443` | trojan | 1918ms | NiREvil/vless |
| `104.17.70.206:8443` | vless | 1974ms | NiREvil/vless |
| `146.75.57.238:443` | vless | 2009ms | snakem982/proxypool |
| `202.50.253.90:19999` | ss | 2028ms | F0rc3Run/F0rc3Run |
| `202.50.253.18:19999` | ss | 2029ms | F0rc3Run/F0rc3Run |
| `179.253.179.109:57443` | vless | 2059ms | whoahaow/rjsxrd |
| `202.50.253.63:19999` | ss | 2195ms | F0rc3Run/F0rc3Run |
| `turk.bettercallakbar.ir:443` | vless | 2274ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 2466ms | NiREvil/vless |
| `202.50.253.72:19999` | ss | 2656ms | F0rc3Run/F0rc3Run |
| `202.50.253.54:19999` | ss | 2762ms | F0rc3Run/F0rc3Run |

#### xray（95 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `31.76.91.238:443` | vless | 363ms | NiREvil/vless |
| `9.247.23.209:443` | vless | 923ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 955ms | F0rc3Run/F0rc3Run |
| `163.245.42.132:443` | vless | 961ms | NiREvil/vless |
| `163.245.42.157:443` | vless | 1041ms | NiREvil/vless |
| `85.31.148.74:443` | vless | 1054ms | whoahaow/rjsxrd |
| `144.31.62.224:443` | vless | 1063ms | NiREvil/vless |
| `212.34.128.120:443` | vless | 1076ms | NiREvil/vless |
| `sw.neuroniko.com:2083` | vless | 1080ms | NiREvil/vless |
| `179.253.179.109:57443` | vless | 1098ms | whoahaow/rjsxrd |
| `179.253.179.109:63080` | vless | 1104ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1108ms | F0rc3Run/F0rc3Run |
| `201.58.181.132:2027` | vless | 1113ms | NiREvil/vless |
| `edge.bookmai.com:443` | vless | 1127ms | F0rc3Run/F0rc3Run |
| `89.125.11.50:443` | vless | 1185ms | NiREvil/vless |
| `89.125.11.57:443` | vless | 1216ms | NiREvil/vless |
| `79.182.39.37:27591` | vless | 1277ms | NiREvil/vless |
| `150.251.143.86:443` | vless | 1283ms | NiREvil/vless |
| `netherlands.biznes.lol:443` | vless | 1284ms | NiREvil/vless |
| `radio.blog-forme.ru:443` | vless | 1299ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 1316ms | F0rc3Run/F0rc3Run |
| `5.129.249.65:443` | vless | 1325ms | NiREvil/vless |
| `150.251.143.86:8443` | vless | 1332ms | NiREvil/vless |
| `62.233.33.51:443` | vless | 1333ms | NiREvil/vless |
| `185.22.155.121:18443` | ss | 1334ms | F0rc3Run/F0rc3Run |
| `147.45.164.160:443` | vless | 1340ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 1360ms | NiREvil/vless |
| `179.253.179.109:57043` | vless | 1390ms | whoahaow/rjsxrd |
| `177.1.192.67:443` | vless | 1402ms | NiREvil/vless |
| `212.34.128.120:2083` | vless | 1406ms | NiREvil/vless |
| `130.78.190.21:443` | vless | 1422ms | NiREvil/vless |
| `5.129.222.175:443` | vless | 1425ms | NiREvil/vless |
| `179.253.179.109:54443` | vless | 1428ms | whoahaow/rjsxrd |
| `201.24.49.49:2027` | vless | 1445ms | NiREvil/vless |
| `5.129.202.74:443` | vless | 1446ms | NiREvil/vless |
| `s12.bsh-net.ru:443` | vless | 1452ms | NiREvil/vless |
| `148.113.5.22:443` | vless | 1464ms | NiREvil/vless |
| `202.50.253.90:19999` | ss | 1476ms | F0rc3Run/F0rc3Run |
| `84.32.184.218:443` | vless | 1482ms | NiREvil/vless |
| `179.253.179.109:62083` | vless | 1529ms | whoahaow/rjsxrd |
| … | 共 95 个 | | |

#### clash（49 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `31.76.91.238:443` | vless | 506ms | NiREvil/vless |
| `80.243.228.61:2085` | vless | 833ms | NiREvil/vless |
| `130.78.190.21:443` | vless | 959ms | NiREvil/vless |
| `202.50.253.72:19999` | ss | 1009ms | F0rc3Run/F0rc3Run |
| `163.245.42.157:443` | vless | 1039ms | NiREvil/vless |
| `163.245.42.132:443` | vless | 1078ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 1088ms | F0rc3Run/F0rc3Run |
| `185.22.155.121:18443` | ss | 1101ms | F0rc3Run/F0rc3Run |
| `202.50.253.18:19999` | ss | 1115ms | F0rc3Run/F0rc3Run |
| `171.22.119.74:8446` | trojan | 1219ms | peasoft/NoMoreWalls |
| `185.232.205.13:2027` | vless | 1271ms | NiREvil/vless |
| `177.1.192.38:8443` | vless | 1292ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 1326ms | F0rc3Run/F0rc3Run |
| `130.17.18.204:8443` | vless | 1383ms | NiREvil/vless |
| `201.24.49.49:2027` | vless | 1396ms | NiREvil/vless |
| `189.74.114.93:443` | vless | 1404ms | NiREvil/vless |
| `72.56.241.230:443` | vless | 1467ms | NiREvil/vless |
| `194.87.143.165:8443` | vless | 1508ms | snakem982/proxypool |
| `72.56.4.84:443` | vless | 1651ms | snakem982/proxypool |
| `84.32.184.218:443` | vless | 1658ms | NiREvil/vless |
| `edge.bookmai.com:443` | vless | 1664ms | F0rc3Run/F0rc3Run |
| `172.66.0.162:443` | vless | 1671ms | NiREvil/vless |
| `177.1.192.90:443` | vless | 1697ms | NiREvil/vless |
| `140.248.185.253:443` | vless | 1743ms | NiREvil/vless |
| `146.75.59.186:443` | vless | 1773ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 1848ms | F0rc3Run/F0rc3Run |
| `xnod13x.artemida.live:8443` | vless | 1856ms | NiREvil/vless |
| `200.165.231.209:443` | vless | 1868ms | NiREvil/vless |
| `hydra.yokkastars.com:2443` | vless | 2011ms | NiREvil/vless |
| `72.56.38.83:443` | vless | 2110ms | NiREvil/vless |
| `www.windowsmsidownloads.com:443` | vmess | 2126ms | F0rc3Run/F0rc3Run |
| `turk.bettercallakbar.ir:443` | vless | 2453ms | NiREvil/vless |
| `171.25.158.163:443` | vless | 2462ms | NiREvil/vless |
| `177.3.214.133:443` | vless | 2600ms | NiREvil/vless |
| `tunell2027.crackerbinam.org:48312` | vless | 2654ms | snakem982/proxypool |
| `starlink-ft.251313.xyz:443` | hysteria2 | 2864ms | kooker/FreeSubsCheck |
| `177.1.192.117:443` | vless | 2902ms | NiREvil/vless |
| `en001.zestapp778.com:29813` | trojan | 2931ms | NiREvil/vless |
| `13.143.176.83:443` | vless | 3013ms | NiREvil/vless |
| `172.64.231.133:443` | trojan | 3115ms | whoahaow/rjsxrd |
| … | 共 49 个 | | |

#### singbox（35 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `202.50.253.72:19999` | ss | 1093ms | F0rc3Run/F0rc3Run |
| `202.50.253.99:19999` | ss | 1102ms | snakem982/proxypool |
| `202.50.253.45:19999` | ss | 1117ms | Pawdroid/Free-servers |
| `api.mediaklenov.cc:443` | vless | 1117ms | NiREvil/vless |
| `jp-1.bnc-gt.co.uk:443` | vless | 1127ms | NiREvil/vless |
| `80.243.228.61:2085` | vless | 1153ms | NiREvil/vless |
| `13.143.176.83:443` | vless | 1161ms | NiREvil/vless |
| `150.251.143.86:8443` | vless | 1162ms | NiREvil/vless |
| `150.251.143.86:443` | vless | 1203ms | NiREvil/vless |
| `171.22.119.74:8446` | trojan | 1271ms | peasoft/NoMoreWalls |
| `177.1.192.117:443` | vless | 1287ms | NiREvil/vless |
| `177.1.192.38:8443` | vless | 1361ms | NiREvil/vless |
| `202.50.253.63:19999` | ss | 1371ms | F0rc3Run/F0rc3Run |
| `s12.bsh-net.ru:443` | vless | 1437ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 1459ms | F0rc3Run/F0rc3Run |
| `194.87.143.165:8443` | vless | 1521ms | snakem982/proxypool |
| `130.17.18.204:8443` | vless | 1535ms | NiREvil/vless |
| `202.50.253.18:19999` | ss | 1562ms | F0rc3Run/F0rc3Run |
| `201.24.49.49:2027` | vless | 1569ms | NiREvil/vless |
| `104.16.34.14:443` | trojan | 1604ms | NiREvil/vless |
| `185.22.155.121:18443` | ss | 1619ms | F0rc3Run/F0rc3Run |
| `hydra.yokkastars.com:2443` | vless | 1792ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 1829ms | F0rc3Run/F0rc3Run |
| `46.17.46.27:18443` | ss | 1849ms | kooker/FreeSubsCheck |
| `wstg.datasynctrue.online:443` | vless | 1882ms | NiREvil/vless |
| `190.93.245.148:443` | trojan | 1887ms | whoahaow/rjsxrd |
| `104.17.70.206:8443` | vless | 1897ms | NiREvil/vless |
| `177.1.192.67:443` | vless | 1965ms | NiREvil/vless |
| `202.50.253.90:19999` | ss | 2261ms | F0rc3Run/F0rc3Run |
| `202.50.253.36:19999` | ss | 2390ms | peasoft/NoMoreWalls |
| `79.182.39.37:27591` | vless | 2618ms | NiREvil/vless |
| `172.66.0.1:443` | vmess | 2853ms | F0rc3Run/F0rc3Run |
| `104.21.0.87:443` | vless | 3538ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 3797ms | F0rc3Run/F0rc3Run |
| `92.42.203.240:2052` | vmess | 5198ms | F0rc3Run/F0rc3Run |

## 2026-10-29 23:08

- 预筛：TCP 连通 3859/3912 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：31.6 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2502 | 30 | 1.2% | 4 | 38 | 2430 | 截断（上限 2500） | `nodes/available_v2ray.txt` |
| xray | 2503 | 105 | 4.2% | 3 | 2 | 2393 | 截断（上限 2500） | `nodes/available_xray.txt` |
| clash | 2506 | 72 | 2.9% | 0 | 31 | 2403 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2503 | 50 | 2.0% | 0 | 27 | 2426 | 截断（上限 2500） | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1661 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 767 |
| v2ray | 配置被内核拒绝（参数不符） | 38 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 4 |
| v2ray | 连接被重置 | 2 |
| xray | 连接超时 | 1294 |
| xray | TLS 握手失败（证书/协议不匹配） | 809 |
| xray | 网络层失败 | 278 |
| xray | 连接被重置 | 12 |
| xray | 该内核不支持（协议/传输/加密/插件） | 3 |
| xray | 配置被内核拒绝（参数不符） | 2 |
| clash | 连接超时 | 1817 |
| clash | TLS 握手失败（证书/协议不匹配） | 435 |
| clash | 网络层失败 | 151 |
| clash | 配置被内核拒绝（参数不符） | 31 |
| singbox | 连接被重置 | 1860 |
| singbox | TLS 握手失败（证书/协议不匹配） | 564 |
| singbox | 配置被内核拒绝（参数不符） | 27 |
| singbox | 认证失败（口令/UUID 不符） | 2 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 127 | 15 | 15 | `pool/pool_v2ray.txt` |
| xray | 304 | 70 | 35 | `pool/pool_xray.txt` |
| clash | 276 | 53 | 19 | `pool/pool_clash.yaml` |
| singbox | 230 | 36 | 14 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| F0rc3Run/F0rc3Run | 3 | 3 | 100% | 1242ms | 92.5 |
| hello-world-1989/cn-news | 10 | 9 | 90% | 856ms | 87.9 |
| Pawdroid/Free-servers | 15 | 9 | 60% | 1990ms | 60.1 |
| snakem982/proxypool | 15 | 8 | 53% | 943ms | 61.7 |
| NiREvil/vless | 47 | 5 | 11% | 1402ms | 29.0 |
| peasoft/NoMoreWalls | 388 | 31 | 8% | 1488ms | 26.7 |
| whoahaow/rjsxrd | 1817 | 130 | 7% | 1802ms | 24.2 |
| cbusifabcap/daily_free_vpn | 205 | 14 | 7% | 1754ms | 24.3 |
| kooker/FreeSubsCheck | 18 | 1 | 6% | 804ms | 29.1 |
| sakha1370/OpenRay | 1490 | 20 | 1% | 1797ms | 20.2 |
| SoliSpirit/v2ray-configs | 5591 | 27 | 0% | 2155ms | 17.4 |
| Barabama/FreeNodes | 182 | 0 | 0% | -ms | 0.0 |
| DukeMehdi/FreeList-V2ray-Configs | 8 | 0 | 0% | -ms | 0.0 |
| free18/v2ray | 62 | 0 | 0% | -ms | 0.0 |
| gslege/CloudflareIP | 76 | 0 | 0% | -ms | 0.0 |
| iboxz/free-v2ray-collector | 11 | 0 | 0% | -ms | 0.0 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 8 | 0 | 0% | -ms | 0.0 |
| barry-far/V2ray-Config | 3 | 0 | 0% | -ms | 0.0 |
| 0xRadikal/Free-v2ray-Configs | 9 | 0 | 0% | -ms | 0.0 |
| ovmvo/FreeSub | 45 | 0 | 0% | -ms | 0.0 |
| shaoyouvip/free | 4 | 0 | 0% | -ms | 0.0 |
| igareck/vpn-configs-for-russia | 5 | 0 | 0% | -ms | 0.0 |
| nyeinkokoaung404/V2ray-Configs | 1 | 0 | 0% | -ms | 0.0 |
| Danialsamadi/v2go | 1 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（30 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `43.167.186.78:8443` | trojan | 338ms | snakem982/proxypool |
| `125.227.86.45:443` | trojan | 466ms | cbusifabcap/daily_free_vpn |
| `13.124.223.116:8443` | ss | 499ms | hello-world-1989/cn-news |
| `216.152.147.79:443` | trojan | 997ms | whoahaow/rjsxrd |
| `202.50.253.90:19999` | ss | 1017ms | peasoft/NoMoreWalls |
| `169.197.140.171:443` | trojan | 1033ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1064ms | peasoft/NoMoreWalls |
| `202.50.253.54:19999` | ss | 1116ms | Pawdroid/Free-servers |
| `202.50.253.27:19999` | ss | 1149ms | peasoft/NoMoreWalls |
| `202.50.253.99:19999` | ss | 1235ms | peasoft/NoMoreWalls |
| `130.94.16.109:80` | vmess | 1294ms | whoahaow/rjsxrd |
| `176.114.95.242:443` | trojan | 1295ms | whoahaow/rjsxrd |
| `202.50.253.36:19999` | ss | 1415ms | peasoft/NoMoreWalls |
| `103.148.73.167:8443` | vless | 1506ms | NiREvil/vless |
| `31.76.102.130:41445` | trojan | 1536ms | NiREvil/vless |
| `200.165.231.209:443` | vless | 1603ms | whoahaow/rjsxrd |
| `jp032001.ssgreen.org:443` | vmess | 1641ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 1658ms | peasoft/NoMoreWalls |
| `202.50.253.63:19999` | ss | 1903ms | peasoft/NoMoreWalls |
| `jp032011.ssgreen.org:443` | vmess | 1987ms | whoahaow/rjsxrd |
| `www.windowsmsidownloads.com:443` | vmess | 1996ms | whoahaow/rjsxrd |
| `130.94.16.109:443` | hysteria2 | 2145ms | snakem982/proxypool |
| `47.250.84.25:443` | trojan | 2192ms | peasoft/NoMoreWalls |
| `jp032006.ssgreen.org:443` | vmess | 2264ms | whoahaow/rjsxrd |
| `202.50.253.81:19999` | ss | 2283ms | Pawdroid/Free-servers |
| `us032017.ssgreen.org:443` | vmess | 2352ms | whoahaow/rjsxrd |
| `starlink-ft.251313.xyz:443` | hysteria2 | 2628ms | cbusifabcap/daily_free_vpn |
| `wstg.datasynctrue.online:443` | vless | 2996ms | whoahaow/rjsxrd |
| `openai.com:443` | trojan | 3737ms | SoliSpirit/v2ray-configs |
| `us003.421421.xyz:20230` | trojan | 5923ms | cbusifabcap/daily_free_vpn |

#### xray（105 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `13.124.223.116:8443` | ss | 317ms | hello-world-1989/cn-news |
| `jp.vpber.info:443` | vless | 491ms | sakha1370/OpenRay |
| `13.124.223.116:443` | vless | 547ms | hello-world-1989/cn-news |
| `47.128.242.197:443` | vless | 739ms | hello-world-1989/cn-news |
| `94.249.186.139:43000` | vless | 980ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 1011ms | peasoft/NoMoreWalls |
| `202.50.253.90:19999` | ss | 1016ms | peasoft/NoMoreWalls |
| `94.249.189.41:43000` | vless | 1033ms | whoahaow/rjsxrd |
| `radio.blog-forme.ru:443` | vless | 1056ms | SoliSpirit/v2ray-configs |
| `130.94.16.109:8388` | ss | 1069ms | F0rc3Run/F0rc3Run |
| `89.46.38.58:443` | vless | 1081ms | whoahaow/rjsxrd |
| `89.125.11.57:443` | vless | 1083ms | whoahaow/rjsxrd |
| `185.81.115.198:443` | vless | 1089ms | whoahaow/rjsxrd |
| `31.59.206.94:443` | vless | 1097ms | whoahaow/rjsxrd |
| `176.65.149.194:8443` | vless | 1101ms | whoahaow/rjsxrd |
| `89.125.37.193:41445` | vless | 1111ms | whoahaow/rjsxrd |
| `163.245.42.157:443` | vless | 1115ms | sakha1370/OpenRay |
| `89.125.11.50:443` | vless | 1129ms | SoliSpirit/v2ray-configs |
| `216.152.147.79:443` | trojan | 1136ms | whoahaow/rjsxrd |
| `85.31.148.74:443` | vless | 1141ms | whoahaow/rjsxrd |
| `us032019.ssgreen.org:443` | vmess | 1148ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 1151ms | peasoft/NoMoreWalls |
| `cd0.bmi.ir.kolman.com.de:80` | vmess | 1154ms | SoliSpirit/v2ray-configs |
| `169.197.140.171:443` | trojan | 1177ms | whoahaow/rjsxrd |
| `144.31.62.224:443` | vless | 1191ms | NiREvil/vless |
| `94.249.186.64:43000` | vless | 1193ms | whoahaow/rjsxrd |
| `23.94.252.67:443` | vless | 1197ms | whoahaow/rjsxrd |
| `201.58.183.99:443` | vless | 1216ms | whoahaow/rjsxrd |
| `2.59.218.23:443` | vless | 1236ms | whoahaow/rjsxrd |
| `202.50.253.81:19999` | ss | 1245ms | Pawdroid/Free-servers |
| `130.49.177.193:443` | vless | 1274ms | whoahaow/rjsxrd |
| `202.50.253.99:19999` | ss | 1292ms | peasoft/NoMoreWalls |
| `185.32.6.26:443` | vless | 1309ms | whoahaow/rjsxrd |
| `83.97.79.93:8443` | vless | 1362ms | whoahaow/rjsxrd |
| `212.34.128.120:2083` | vless | 1368ms | SoliSpirit/v2ray-configs |
| `176.114.95.242:443` | trojan | 1392ms | whoahaow/rjsxrd |
| `94.249.189.87:43000` | vless | 1404ms | whoahaow/rjsxrd |
| `185.168.208.190:47443` | vless | 1419ms | whoahaow/rjsxrd |
| `2.59.216.239:8443` | vless | 1421ms | whoahaow/rjsxrd |
| `podcasts.blog-forme.ru:2083` | vless | 1441ms | sakha1370/OpenRay |
| … | 共 105 个 | | |

#### clash（72 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `43.167.186.78:8443` | trojan | 339ms | snakem982/proxypool |
| `13.124.223.116:8443` | ss | 422ms | hello-world-1989/cn-news |
| `125.227.86.45:443` | trojan | 491ms | cbusifabcap/daily_free_vpn |
| `13.124.223.116:443` | vless | 656ms | hello-world-1989/cn-news |
| `jp.vpber.info:443` | vless | 657ms | sakha1370/OpenRay |
| `104.18.1.1:2087` | vless | 804ms | kooker/FreeSubsCheck |
| `mm.good2026.com:12961` | ss | 829ms | whoahaow/rjsxrd |
| `94.249.195.31:43000` | vless | 915ms | whoahaow/rjsxrd |
| `16.54.253.154:443` | ss | 917ms | cbusifabcap/daily_free_vpn |
| `185.168.208.190:47443` | vless | 940ms | whoahaow/rjsxrd |
| `94.249.189.87:43000` | vless | 976ms | whoahaow/rjsxrd |
| `172.66.0.162:443` | vless | 995ms | peasoft/NoMoreWalls |
| `202.50.253.72:19999` | ss | 1008ms | peasoft/NoMoreWalls |
| `169.197.140.171:443` | trojan | 1021ms | whoahaow/rjsxrd |
| `202.50.253.90:19999` | ss | 1059ms | peasoft/NoMoreWalls |
| `202.50.253.45:19999` | ss | 1085ms | peasoft/NoMoreWalls |
| `94.249.186.64:43000` | vless | 1087ms | whoahaow/rjsxrd |
| `171.22.119.74:8446` | trojan | 1100ms | peasoft/NoMoreWalls |
| `216.152.147.79:443` | trojan | 1106ms | whoahaow/rjsxrd |
| `94.249.195.81:43000` | vless | 1123ms | whoahaow/rjsxrd |
| `163.245.42.157:443` | vless | 1147ms | sakha1370/OpenRay |
| `89.46.38.58:443` | vless | 1184ms | whoahaow/rjsxrd |
| `201.58.183.99:443` | vless | 1210ms | whoahaow/rjsxrd |
| `35.183.129.117:443` | ss | 1211ms | cbusifabcap/daily_free_vpn |
| `176.114.95.242:443` | trojan | 1223ms | whoahaow/rjsxrd |
| `202.50.253.99:19999` | ss | 1226ms | peasoft/NoMoreWalls |
| `185.81.115.198:443` | vless | 1232ms | whoahaow/rjsxrd |
| `us003.421421.xyz:20230` | trojan | 1255ms | cbusifabcap/daily_free_vpn |
| `94.249.189.41:43000` | vless | 1265ms | whoahaow/rjsxrd |
| `191.217.217.69:443` | vless | 1270ms | SoliSpirit/v2ray-configs |
| `130.49.177.193:443` | vless | 1298ms | whoahaow/rjsxrd |
| `202.50.253.63:19999` | ss | 1316ms | peasoft/NoMoreWalls |
| `144.31.242.142:443` | vless | 1347ms | cbusifabcap/daily_free_vpn |
| `883f1393.con.rasterparcel.tech:443` | vless | 1357ms | whoahaow/rjsxrd |
| `31.76.102.130:41445` | trojan | 1407ms | NiREvil/vless |
| `185.220.249.139:8443` | vless | 1407ms | whoahaow/rjsxrd |
| `217.60.151.141:47443` | vless | 1407ms | whoahaow/rjsxrd |
| `de-2.ffpn.pro:443` | vless | 1463ms | whoahaow/rjsxrd |
| `200.165.231.209:443` | vless | 1464ms | whoahaow/rjsxrd |
| `31.76.2.57:443` | vless | 1498ms | cbusifabcap/daily_free_vpn |
| … | 共 72 个 | | |

#### singbox（50 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `125.227.86.45:443` | trojan | 379ms | cbusifabcap/daily_free_vpn |
| `43.167.186.78:8443` | trojan | 468ms | snakem982/proxypool |
| `13.124.223.116:8443` | ss | 499ms | hello-world-1989/cn-news |
| `54.83.84.17:443` | ss | 782ms | snakem982/proxypool |
| `47.128.242.197:443` | vless | 806ms | hello-world-1989/cn-news |
| `130.94.16.109:8388` | ss | 952ms | F0rc3Run/F0rc3Run |
| `54.237.60.0:443` | ss | 997ms | snakem982/proxypool |
| `202.50.253.63:19999` | ss | 1004ms | peasoft/NoMoreWalls |
| `35.183.129.117:443` | ss | 1036ms | cbusifabcap/daily_free_vpn |
| `169.197.140.171:443` | trojan | 1041ms | whoahaow/rjsxrd |
| `202.50.253.36:19999` | ss | 1062ms | peasoft/NoMoreWalls |
| `89.46.38.58:443` | vless | 1082ms | whoahaow/rjsxrd |
| `94.249.195.81:43000` | vless | 1103ms | whoahaow/rjsxrd |
| `94.249.186.64:43000` | vless | 1104ms | whoahaow/rjsxrd |
| `94.249.195.31:43000` | vless | 1106ms | whoahaow/rjsxrd |
| `216.152.147.79:443` | trojan | 1109ms | whoahaow/rjsxrd |
| `201.58.183.99:443` | vless | 1150ms | whoahaow/rjsxrd |
| `202.50.253.54:19999` | ss | 1175ms | Pawdroid/Free-servers |
| `54.91.51.67:443` | ss | 1179ms | snakem982/proxypool |
| `217.60.151.141:47443` | vless | 1180ms | whoahaow/rjsxrd |
| `94.249.189.41:43000` | vless | 1204ms | whoahaow/rjsxrd |
| `9.247.23.209:443` | vless | 1217ms | SoliSpirit/v2ray-configs |
| `163.245.42.157:443` | vless | 1232ms | sakha1370/OpenRay |
| `cd0.bmi.ir.kolman.com.de:80` | vmess | 1250ms | SoliSpirit/v2ray-configs |
| `130.94.16.109:443` | hysteria2 | 1295ms | snakem982/proxypool |
| `130.94.16.109:80` | vmess | 1360ms | whoahaow/rjsxrd |
| `31.76.102.130:41445` | trojan | 1372ms | NiREvil/vless |
| `94.249.186.139:43000` | vless | 1403ms | whoahaow/rjsxrd |
| `202.50.253.81:19999` | ss | 1417ms | Pawdroid/Free-servers |
| `72.56.241.230:443` | vless | 1455ms | whoahaow/rjsxrd |
| `200.165.231.209:443` | vless | 1526ms | whoahaow/rjsxrd |
| `202.50.253.45:19999` | ss | 1663ms | peasoft/NoMoreWalls |
| `202.50.253.27:19999` | ss | 1756ms | peasoft/NoMoreWalls |
| `202.50.253.99:19999` | ss | 1777ms | peasoft/NoMoreWalls |
| `185.168.208.190:47443` | vless | 1841ms | whoahaow/rjsxrd |
| `185.220.249.139:8443` | vless | 1899ms | whoahaow/rjsxrd |
| `171.22.119.74:8446` | trojan | 1963ms | peasoft/NoMoreWalls |
| `94.249.189.87:43000` | vless | 2193ms | whoahaow/rjsxrd |
| `202.50.253.72:19999` | ss | 2442ms | peasoft/NoMoreWalls |
| `starlink-ft.251313.xyz:443` | hysteria2 | 2476ms | cbusifabcap/daily_free_vpn |
| … | 共 50 个 | | |

## 2026-10-28 23:15

- 预筛：TCP 连通 2698/2744 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 24，超时 3.0s（超时即判失败，不再等）
- 测试策略：全量——候选 ≤ 2500 个全部测试；超过则只测排序前 2500 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；不复测（实测复测收益 1.7%）；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：28.7 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 2118 | 27 | 1.3% | 2 | 35 | 2054 | 全量 | `nodes/available_v2ray.txt` |
| xray | 2159 | 127 | 5.9% | 1 | 1 | 2030 | 全量 | `nodes/available_xray.txt` |
| clash | 2508 | 93 | 3.7% | 0 | 0 | 2415 | 截断（上限 2500） | `nodes/available_clash.yaml` |
| singbox | 2509 | 72 | 2.9% | 0 | 1 | 2436 | 全量 | `nodes/available_singbox.json` |

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | 连接超时 | 1215 |
| v2ray | TLS 握手失败（证书/协议不匹配） | 839 |
| v2ray | 配置被内核拒绝（参数不符） | 35 |
| v2ray | 该内核不支持（协议/传输/加密/插件） | 2 |
| xray | 连接超时 | 1156 |
| xray | TLS 握手失败（证书/协议不匹配） | 562 |
| xray | 网络层失败 | 306 |
| xray | 连接被重置 | 6 |
| xray | 该内核不支持（协议/传输/加密/插件） | 1 |
| xray | 配置被内核拒绝（参数不符） | 1 |
| clash | 连接超时 | 1554 |
| clash | TLS 握手失败（证书/协议不匹配） | 529 |
| clash | 网络层失败 | 332 |
| singbox | 连接被重置 | 1812 |
| singbox | TLS 握手失败（证书/协议不匹配） | 624 |
| singbox | 配置被内核拒绝（参数不符） | 1 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 112 | 14 | 13 | `pool/pool_v2ray.txt` |
| xray | 234 | 100 | 27 | `pool/pool_xray.txt` |
| clash | 223 | 75 | 18 | `pool/pool_clash.yaml` |
| singbox | 194 | 53 | 19 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| peasoft/NoMoreWalls | 7 | 6 | 86% | 1746ms | 79.5 |
| kooker/FreeSubsCheck | 194 | 9 | 5% | 1282ms | 25.6 |
| NiREvil/vless | 7513 | 297 | 4% | 1965ms | 21.0 |
| Delta-Kronecker/V2ray-Config | 1531 | 7 | 0% | 1793ms | 19.6 |
| ermaozi01/free_clash_vpn | 10 | 0 | 0% | -ms | 0.0 |
| Danialsamadi/v2go | 20 | 0 | 0% | -ms | 0.0 |
| Barabama/FreeNodes | 12 | 0 | 0% | -ms | 0.0 |
| 0xRadikal/Free-v2ray-Configs | 2 | 0 | 0% | -ms | 0.0 |
| barry-far/V2ray-Config | 3 | 0 | 0% | -ms | 0.0 |
| snakem982/proxypool | 1 | 0 | 0% | -ms | 0.0 |
| nyeinkokoaung404/V2ray-Configs | 1 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（27 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `dns8.m3hrzd.ir:8044` | ss | 859ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 973ms | NiREvil/vless |
| `202.50.253.99:19999` | ss | 992ms | NiREvil/vless |
| `46.17.41.61:18443` | ss | 1006ms | kooker/FreeSubsCheck |
| `202.50.253.63:19999` | ss | 1036ms | NiREvil/vless |
| `202.50.253.72:19999` | ss | 1146ms | NiREvil/vless |
| `202.50.253.90:19999` | ss | 1328ms | NiREvil/vless |
| `172.64.150.200:443` | vless | 1425ms | NiREvil/vless |
| `w.geogame.ir:2053` | vless | 1752ms | NiREvil/vless |
| `167.82.64.64:443` | vless | 1759ms | NiREvil/vless |
| `199.232.78.160:443` | vless | 1775ms | NiREvil/vless |
| `195.58.49.167:18443` | ss | 1800ms | kooker/FreeSubsCheck |
| `xsru1.ddnsfree.com:443` | vless | 1801ms | NiREvil/vless |
| `103.180.20.108:8443` | vless | 1824ms | NiREvil/vless |
| `59.125.69.22:443` | vless | 1832ms | NiREvil/vless |
| `146.75.59.186:443` | vless | 1866ms | NiREvil/vless |
| `xssite.webredirect.org:443` | vless | 1984ms | NiREvil/vless |
| `104.21.15.251:443` | vmess | 2018ms | NiREvil/vless |
| `202.50.253.27:19999` | ss | 2096ms | NiREvil/vless |
| `ccc.010304.xyz:443` | vless | 2153ms | NiREvil/vless |
| `202.50.253.18:19999` | ss | 2218ms | NiREvil/vless |
| `wwww.qarvian.ir:443` | vless | 2288ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 2441ms | peasoft/NoMoreWalls |
| `202.50.253.36:19999` | ss | 2638ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 2781ms | NiREvil/vless |
| `194.55.239.89:443` | vless | 2878ms | NiREvil/vless |
| `200.165.231.209:443` | vless | 2903ms | NiREvil/vless |

#### xray（127 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `67.159.52.51:443` | vless | 407ms | NiREvil/vless |
| `202.50.253.54:19999` | ss | 989ms | peasoft/NoMoreWalls |
| `31.58.46.154:443` | vless | 1001ms | NiREvil/vless |
| `89.125.11.57:443` | vless | 1071ms | NiREvil/vless |
| `89.125.11.50:443` | vless | 1078ms | NiREvil/vless |
| `202.50.253.99:19999` | ss | 1096ms | NiREvil/vless |
| `202.50.253.63:19999` | ss | 1097ms | NiREvil/vless |
| `cz-prg.dontblockmepls.com:2063` | vless | 1098ms | NiREvil/vless |
| `89.125.11.26:443` | vless | 1100ms | NiREvil/vless |
| `217.216.218.96:443` | vless | 1108ms | NiREvil/vless |
| `144.31.62.224:443` | vless | 1109ms | NiREvil/vless |
| `84.38.187.134:443` | vless | 1110ms | NiREvil/vless |
| `193.233.221.86:443` | vless | 1113ms | NiREvil/vless |
| `dns8.m3hrzd.ir:8044` | ss | 1120ms | NiREvil/vless |
| `202.50.253.81:19999` | ss | 1141ms | NiREvil/vless |
| `46.17.41.61:18443` | ss | 1145ms | kooker/FreeSubsCheck |
| `217.216.218.162:443` | vless | 1164ms | NiREvil/vless |
| `23.94.252.67:443` | vless | 1193ms | NiREvil/vless |
| `217.216.218.123:443` | vless | 1196ms | NiREvil/vless |
| `202.50.253.36:19999` | ss | 1218ms | NiREvil/vless |
| `135.106.142.209:443` | vless | 1228ms | NiREvil/vless |
| `13.143.180.104:443` | vless | 1229ms | NiREvil/vless |
| `201.58.183.147:443` | vless | 1240ms | NiREvil/vless |
| `95.143.188.10:443` | vless | 1304ms | NiREvil/vless |
| `areal3.greewebservices.ir:4445` | vless | 1316ms | NiREvil/vless |
| `883f1393.con.rasterparcel.tech:443` | vless | 1316ms | NiREvil/vless |
| `202.50.253.18:19999` | ss | 1327ms | NiREvil/vless |
| `79.182.39.45:25172` | vless | 1345ms | NiREvil/vless |
| `185.32.6.26:443` | vless | 1346ms | NiREvil/vless |
| `200.165.231.209:443` | vless | 1389ms | NiREvil/vless |
| `79.182.39.235:25172` | vless | 1391ms | NiREvil/vless |
| `135.106.143.114:443` | vless | 1411ms | NiREvil/vless |
| `ru2.radiolumens.uk:9444` | vless | 1437ms | NiREvil/vless |
| `217.11.164.183:2102` | vless | 1446ms | NiREvil/vless |
| `217.11.164.183:2120` | vless | 1462ms | NiREvil/vless |
| `31.76.2.57:443` | vless | 1465ms | NiREvil/vless |
| `s12.bsh-net.ru:443` | vless | 1482ms | NiREvil/vless |
| `213.152.180.104:2095` | vless | 1492ms | NiREvil/vless |
| `188.208.125.104:443` | vless | 1495ms | NiREvil/vless |
| `217.216.218.108:443` | vless | 1510ms | NiREvil/vless |
| … | 共 127 个 | | |

#### clash（93 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `125.227.86.45:443` | trojan | 475ms | Delta-Kronecker/V2ray-Config |
| `103.180.20.108:8443` | vless | 668ms | NiREvil/vless |
| `104.18.1.1:2087` | vless | 796ms | kooker/FreeSubsCheck |
| `202.50.253.99:19999` | ss | 948ms | NiREvil/vless |
| `112.169.175.199:31157` | vless | 972ms | NiREvil/vless |
| `195.58.49.167:18443` | ss | 1009ms | kooker/FreeSubsCheck |
| `dns8.m3hrzd.ir:8044` | ss | 1025ms | NiREvil/vless |
| `31.76.5.144:443` | vless | 1082ms | NiREvil/vless |
| `217.216.218.139:443` | vless | 1097ms | NiREvil/vless |
| `193.160.141.138:8443` | vless | 1101ms | NiREvil/vless |
| `9.247.23.209:443` | vless | 1117ms | NiREvil/vless |
| `217.216.218.151:443` | vless | 1169ms | NiREvil/vless |
| `46.17.41.61:18443` | ss | 1172ms | kooker/FreeSubsCheck |
| `202.50.253.18:19999` | ss | 1211ms | NiREvil/vless |
| `31.76.2.57:443` | vless | 1229ms | NiREvil/vless |
| `217.216.218.96:443` | vless | 1264ms | NiREvil/vless |
| `135.106.143.114:443` | vless | 1267ms | NiREvil/vless |
| `edge.bookmai.com:443` | vless | 1275ms | NiREvil/vless |
| `31.76.7.233:443` | vless | 1295ms | NiREvil/vless |
| `77.42.12.225:443` | vless | 1296ms | NiREvil/vless |
| `31.76.5.42:443` | vless | 1324ms | NiREvil/vless |
| `59.125.69.22:443` | vless | 1329ms | NiREvil/vless |
| `fl3.nexfile.net:4443` | vless | 1337ms | NiREvil/vless |
| `norw-2.failspace.top:443` | vless | 1350ms | NiREvil/vless |
| `norw-1.failspace.top:443` | vless | 1351ms | NiREvil/vless |
| `viper-23.moriarty-web.com:443` | vless | 1352ms | NiREvil/vless |
| `62.133.63.45:8444` | vless | 1377ms | NiREvil/vless |
| `84.32.184.218:443` | vless | 1394ms | NiREvil/vless |
| `196.196.204.174:443` | vless | 1395ms | NiREvil/vless |
| `213.152.180.104:2092` | vless | 1405ms | NiREvil/vless |
| `193.233.221.86:443` | vless | 1418ms | NiREvil/vless |
| `185.220.100.168:443` | trojan | 1420ms | Delta-Kronecker/V2ray-Config |
| `31.76.5.124:443` | vless | 1431ms | NiREvil/vless |
| `46.8.43.125:443` | vless | 1439ms | NiREvil/vless |
| `199.232.78.120:443` | trojan | 1451ms | NiREvil/vless |
| `de-bots4.h1cloud.net:25267` | trojan | 1465ms | Delta-Kronecker/V2ray-Config |
| `kz-central.v8x2b.lol:443` | vless | 1509ms | NiREvil/vless |
| `144.31.217.28:443` | vless | 1527ms | NiREvil/vless |
| `213.152.180.55:2092` | vless | 1570ms | NiREvil/vless |
| `177.7.51.29:8443` | vless | 1591ms | NiREvil/vless |
| … | 共 93 个 | | |

#### singbox（72 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `43.155.199.22:80` | vmess | 397ms | peasoft/NoMoreWalls |
| `125.227.86.45:443` | trojan | 518ms | Delta-Kronecker/V2ray-Config |
| `64.83.20.73:8388` | ss | 822ms | NiREvil/vless |
| `112.169.175.199:31157` | vless | 944ms | NiREvil/vless |
| `9.247.23.209:443` | vless | 987ms | NiREvil/vless |
| `172.66.154.57:443` | vless | 1052ms | NiREvil/vless |
| `202.50.253.63:19999` | ss | 1140ms | NiREvil/vless |
| `46.17.41.61:18443` | ss | 1156ms | kooker/FreeSubsCheck |
| `202.50.253.45:19999` | ss | 1168ms | NiREvil/vless |
| `45.63.53.81:443` | vless | 1193ms | NiREvil/vless |
| `dns8.m3hrzd.ir:8044` | ss | 1215ms | NiREvil/vless |
| `193.160.141.138:8443` | vless | 1235ms | NiREvil/vless |
| `viper-23.moriarty-web.com:443` | vless | 1239ms | NiREvil/vless |
| `31.76.5.42:443` | vless | 1269ms | NiREvil/vless |
| `164.37.224.228:25445` | vless | 1276ms | NiREvil/vless |
| `31.76.5.144:443` | vless | 1293ms | NiREvil/vless |
| `norw-1.failspace.top:443` | vless | 1302ms | NiREvil/vless |
| `31.76.5.124:443` | vless | 1304ms | NiREvil/vless |
| `norway-2.failspace.top:443` | vless | 1335ms | NiREvil/vless |
| `195.58.49.167:18443` | ss | 1339ms | kooker/FreeSubsCheck |
| `edge.bookmai.com:443` | vless | 1364ms | NiREvil/vless |
| `213.152.180.104:2094` | vless | 1369ms | NiREvil/vless |
| `213.152.180.104:2095` | vless | 1434ms | NiREvil/vless |
| `norw-2.failspace.top:443` | vless | 1461ms | NiREvil/vless |
| `xsru1.ddnsfree.com:443` | vless | 1467ms | NiREvil/vless |
| `72.56.4.84:443` | vless | 1479ms | NiREvil/vless |
| `186.246.9.29:443` | vless | 1495ms | NiREvil/vless |
| `146.75.59.186:443` | vless | 1624ms | NiREvil/vless |
| `72.56.241.230:443` | vless | 1624ms | NiREvil/vless |
| `areal3.greewebservices.ir:4445` | vless | 1631ms | NiREvil/vless |
| `177.7.51.29:8443` | vless | 1653ms | NiREvil/vless |
| `w.geogame.ir:2053` | vless | 1679ms | NiREvil/vless |
| `213.152.180.55:2093` | vless | 1698ms | NiREvil/vless |
| `201.24.121.243:443` | vless | 1710ms | NiREvil/vless |
| `199.232.78.160:443` | vless | 1761ms | NiREvil/vless |
| `wwww.qarvian.ir:443` | vless | 1769ms | NiREvil/vless |
| `213.152.180.55:2092` | vless | 1809ms | NiREvil/vless |
| `213.152.180.104:2088` | vless | 1818ms | NiREvil/vless |
| `213.152.180.55:2088` | vless | 1836ms | NiREvil/vless |
| `xssite.webredirect.org:443` | vless | 1859ms | NiREvil/vless |
| … | 共 72 个 | | |

## 2026-10-27 02:46

- 预筛：TCP 连通 6838/16620 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 12
- 测试策略：全量——候选 ≤ 3000 个全部测试；超过则只测排序前 3000 个
- 判定口径：可用 = 通过 HTTP CONNECT 真的取到 2xx；网络类失败复测 1 次；「内核不支持」「配置被内核拒绝」不计入不可达（见 protocol.md 的失败分类）
- 总耗时：75.2 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 不支持 | 配置错误 | 不可达 | 轮次 | 可用文件 |
|---|---|---|---|---|---|---|---|---|
| v2ray | 3097 | 69 | 2.2% | 0 | 18 | 3010 | 截断（上限 3000） | `nodes/available_v2ray.txt` |
| xray | 2592 | 80 | 3.1% | 0 | 3 | 2509 | 截断（上限 3000） | `nodes/available_xray.txt` |
| clash | 792 | 75 | 9.5% | 0 | 0 | 717 | 截断（上限 3000） | `nodes/available_clash.yaml` |
| singbox | 840 | 68 | 8.1% | 0 | 0 | 772 | 截断（上限 3000） | `nodes/available_singbox.json` |

> **本轮未跑完**（墙钟预算到期主动收尾或分窗口续跑，不是失败）：未开始：clash、singbox；中途截断：xray（2592/2414）。已测结果全部有效且已落盘，剩余部分下次运行用 `--cores` + `--resume-tested` 接着测。

### 失败原因分布

「不支持 / 配置被拒绝」属于本机内核能力或参数问题，不是节点问题；只有 tls / auth / refused / reset / timeout 才是节点侧的失败证据。

| 代理内核 | 原因 | 数量 |
|---|---|---|
| v2ray | TLS 握手失败（证书/协议不匹配） | 720 |
| v2ray | 连接超时 | 199 |
| v2ray | 配置被内核拒绝（参数不符） | 18 |
| xray | 网络层失败 | 1035 |
| xray | TLS 握手失败（证书/协议不匹配） | 591 |
| xray | 连接超时 | 319 |
| xray | 连接被重置 | 5 |
| xray | 配置被内核拒绝（参数不符） | 3 |
| clash | TLS 握手失败（证书/协议不匹配） | 633 |
| clash | 网络层失败 | 49 |
| clash | 连接超时 | 35 |
| singbox | 连接被重置 | 574 |
| singbox | TLS 握手失败（证书/协议不匹配） | 198 |


### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 98 | 3 | 66 | `pool/pool_v2ray.txt` |
| xray | 134 | 13 | 67 | `pool/pool_xray.txt` |
| clash | 148 | 0 | 0 | `pool/pool_clash.yaml` |
| singbox | 141 | 0 | 0 | `pool/pool_singbox.json` |

池目录：`nodes/pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| kooker/FreeSubsCheck | 5 | 5 | 100% | 3413ms | 79.5 |
| Pawdroid/Free-servers | 2 | 2 | 100% | 1210ms | 92.7 |
| Delta-Kronecker/V2ray-Config | 1 | 1 | 100% | 604ms | 96.4 |
| NiREvil/vless | 1 | 1 | 100% | 2456ms | 85.3 |
| 0xRadikal/Free-v2ray-Configs | 7 | 5 | 71% | 837ms | 75.0 |
| Danialsamadi/v2go | 3 | 2 | 67% | 935ms | 71.1 |
| snakem982/proxypool | 5 | 3 | 60% | 6201ms | 42.0 |
| peasoft/NoMoreWalls | 7 | 4 | 57% | 2339ms | 56.0 |
| barry-far/V2ray-Config | 129 | 4 | 3% | 5760ms | 2.2 |
| nyeinkokoaung404/V2ray-Configs | 796 | 5 | 1% | 4408ms | 4.0 |
| Barabama/FreeNodes | 265 | 1 | 0% | 6277ms | 0.3 |
| liketolivefree/kobabi | 1575 | 1 | 0% | 12758ms | 0.0 |
| Hidashimora/free-vpn-anti-rkn | 105 | 0 | 0% | -ms | 0.0 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 6 | 0 | 0% | -ms | 0.0 |
| iboxz/free-v2ray-collector | 8 | 0 | 0% | -ms | 0.0 |
| Epodonios/v2ray-configs | 9 | 0 | 0% | -ms | 0.0 |


### 各内核可用节点详情

#### v2ray（69 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `89.125.70.179:8388` | ss | 592ms | kooker/FreeSubsCheck |
| `125.227.86.45:443` | trojan | 604ms | Delta-Kronecker/V2ray-Config |
| `146.190.157.232:39644` | ss | 651ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:46928` | vless | 737ms | 0xRadikal/Free-v2ray-Configs |
| `24.199.106.240:9998` | trojan | 768ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:36812` | vmess | 770ms | snakem982/proxypool |
| `rabin.142.251.153.7.savfasf.ir:41432` | vless | 771ms | 0xRadikal/Free-v2ray-Configs |
| `45.32.140.119:9304` | trojan | 801ms | 0xRadikal/Free-v2ray-Configs |
| `164.92.73.218:8931` | trojan | 808ms | Danialsamadi/v2go |
| `147.182.232.6:4853` | trojan | 813ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.178.208:4804` | trojan | 814ms | Danialsamadi/v2go |
| `45.32.135.70:9213` | trojan | 814ms | 0xRadikal/Free-v2ray-Configs |
| `149.28.214.139:7604` | trojan | 818ms | 0xRadikal/Free-v2ray-Configs |
| `209.38.66.47:6105` | trojan | 830ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.203.237:6022` | trojan | 837ms | Danialsamadi/v2go |
| `144.126.223.93:8911` | trojan | 843ms | Danialsamadi/v2go |
| `177.202.111.20:56137` | ss | 846ms | kooker/FreeSubsCheck |
| `66.163.114.132:443` | trojan | 855ms | 0xRadikal/Free-v2ray-Configs |
| `64.23.151.246:7801` | trojan | 867ms | 0xRadikal/Free-v2ray-Configs |
| `171.22.119.74:8447` | vless | 877ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.234.144:8563` | trojan | 902ms | 0xRadikal/Free-v2ray-Configs |
| `216.152.156.42:443` | trojan | 903ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 933ms | Pawdroid/Free-servers |
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
| `202.50.253.63:19999` | ss | 1455ms | peasoft/NoMoreWalls |
| `202.50.253.81:19999` | ss | 1488ms | Pawdroid/Free-servers |
| `202.50.253.90:19999` | ss | 1512ms | peasoft/NoMoreWalls |
| `209.94.90.201:2083` | vless | 1588ms | igareck/vpn-configs-for-russia |
| `177.202.111.21:56137` | ss | 1689ms | peasoft/NoMoreWalls |
| `47.250.84.25:443` | trojan | 1754ms | peasoft/NoMoreWalls |
| `31.185.105.12:443` | hysteria2 | 1782ms | 0xRadikal/Free-v2ray-Configs |
| … | 共 69 个 | | |

#### xray（80 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `146.190.157.232:39644` | ss | 643ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:36812` | vmess | 735ms | snakem982/proxypool |
| `91.107.128.44:24701` | vmess | 824ms | Danialsamadi/v2go |
| `147.182.203.237:6022` | trojan | 840ms | Danialsamadi/v2go |
| `137.184.178.208:4804` | trojan | 846ms | Danialsamadi/v2go |
| `144.126.223.93:8911` | trojan | 890ms | Danialsamadi/v2go |
| `163.245.42.48:443` | vless | 946ms | kooker/FreeSubsCheck |
| `164.92.73.218:8931` | trojan | 963ms | Danialsamadi/v2go |
| `91.206.92.238:18443` | ss | 999ms | peasoft/NoMoreWalls |
| `91.196.163.150:8443` | vless | 1044ms | Danialsamadi/v2go |
| `45.43.79.92:443` | vless | 1059ms | 0xRadikal/Free-v2ray-Configs |
| `89.125.11.57:443` | vless | 1070ms | 0xRadikal/Free-v2ray-Configs |
| `45.129.242.56:443` | vless | 1077ms | 0xRadikal/Free-v2ray-Configs |
| `89.125.11.50:443` | vless | 1092ms | 0xRadikal/Free-v2ray-Configs |
| `nl2.h1cloud.net:25445` | vless | 1129ms | 0xRadikal/Free-v2ray-Configs |
| `62.233.33.51:443` | vless | 1164ms | 0xRadikal/Free-v2ray-Configs |
| `177.202.111.21:56137` | ss | 1191ms | peasoft/NoMoreWalls |
| `89.125.11.26:443` | vless | 1196ms | Danialsamadi/v2go |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1198ms | Danialsamadi/v2go |
| `45.38.143.210:30584` | vless | 1217ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.172.34:443` | vless | 1230ms | kooker/FreeSubsCheck |
| `62.233.33.23:443` | vless | 1234ms | 0xRadikal/Free-v2ray-Configs |
| `62.233.33.44:443` | vless | 1235ms | 0xRadikal/Free-v2ray-Configs |
| `cz-prg.dontblockmepls.com:2063` | vless | 1237ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.54:19999` | ss | 1293ms | peasoft/NoMoreWalls |
| `lv.peregrine-sub.net:1443` | vless | 1308ms | 0xRadikal/Free-v2ray-Configs |
| `64.83.20.73:8388` | ss | 1460ms | 0xRadikal/Free-v2ray-Configs |
| `31.185.105.12:443` | hysteria2 | 1494ms | 0xRadikal/Free-v2ray-Configs |
| `kz-central.v8x2b.lol:443` | vless | 1496ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.45:19999` | ss | 1498ms | Pawdroid/Free-servers |
| `188.132.232.187:1443` | vless | 1507ms | barry-far/V2ray-Config |
| `se1-cl3.vless-fiberstasis.top:443` | vless | 1637ms | 0xRadikal/Free-v2ray-Configs |
| `45.92.218.130:443` | vless | 1647ms | nyeinkokoaung404/V2ray-Configs |
| `109.234.211.232:443` | trojan | 1705ms | Danialsamadi/v2go |
| `ru11.oshost.network:443` | vless | 1727ms | 0xRadikal/Free-v2ray-Configs |
| `201.24.121.243:443` | vless | 1785ms | peasoft/NoMoreWalls |
| `202.50.253.99:19999` | ss | 1820ms | Pawdroid/Free-servers |
| `202.50.253.72:19999` | ss | 1874ms | peasoft/NoMoreWalls |
| `13.143.172.34:4443` | vless | 1899ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.172.34:2096` | vless | 1913ms | 0xRadikal/Free-v2ray-Configs |
| … | 共 80 个 | | |

#### clash（75 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `43.155.199.22:80` | vmess | 319ms | peasoft/NoMoreWalls |
| `47.250.84.25:443` | trojan | 527ms | peasoft/NoMoreWalls |
| `146.190.157.232:39644` | ss | 599ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:36812` | vmess | 639ms | snakem982/proxypool |
| `89.125.70.179:8388` | ss | 678ms | kooker/FreeSubsCheck |
| `91.107.128.44:46928` | vless | 740ms | 0xRadikal/Free-v2ray-Configs |
| `45.32.135.70:9213` | trojan | 770ms | 0xRadikal/Free-v2ray-Configs |
| `rabin.142.251.153.7.savfasf.ir:41432` | vless | 777ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.234.144:8563` | trojan | 815ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:24701` | vmess | 816ms | Danialsamadi/v2go |
| `164.92.73.218:8931` | trojan | 820ms | Danialsamadi/v2go |
| `144.126.223.93:8911` | trojan | 834ms | Danialsamadi/v2go |
| `45.32.140.119:9304` | trojan | 835ms | 0xRadikal/Free-v2ray-Configs |
| `149.28.214.139:7604` | trojan | 854ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.203.237:6022` | trojan | 860ms | Danialsamadi/v2go |
| `209.38.66.47:6105` | trojan | 872ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.178.208:4804` | trojan | 874ms | Danialsamadi/v2go |
| `64.23.151.246:7801` | trojan | 900ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.18:19999` | ss | 960ms | peasoft/NoMoreWalls |
| `45.129.242.56:443` | vless | 963ms | 0xRadikal/Free-v2ray-Configs |
| `64.83.20.73:8388` | ss | 965ms | 0xRadikal/Free-v2ray-Configs |
| `45.38.143.210:30584` | vless | 973ms | 0xRadikal/Free-v2ray-Configs |
| `9.247.23.209:443` | vless | 1002ms | 0xRadikal/Free-v2ray-Configs |
| `nl2.h1cloud.net:25445` | vless | 1032ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.45:19999` | ss | 1043ms | Pawdroid/Free-servers |
| `202.50.253.99:19999` | ss | 1049ms | Pawdroid/Free-servers |
| `se1-cl3.vless-fiberstasis.top:443` | vless | 1086ms | 0xRadikal/Free-v2ray-Configs |
| `cz-prg.dontblockmepls.com:2063` | vless | 1140ms | 0xRadikal/Free-v2ray-Configs |
| `45.43.79.92:443` | vless | 1190ms | 0xRadikal/Free-v2ray-Configs |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1238ms | Danialsamadi/v2go |
| `13.143.172.34:2096` | vless | 1240ms | 0xRadikal/Free-v2ray-Configs |
| `13.143.172.34:4443` | vless | 1280ms | 0xRadikal/Free-v2ray-Configs |
| `64.176.163.182:443` | trojan | 1290ms | 0xRadikal/Free-v2ray-Configs |
| `195.123.213.28:443` | vless | 1383ms | snakem982/proxypool |
| `13.143.172.34:443` | vless | 1385ms | kooker/FreeSubsCheck |
| `201.24.121.243:443` | vless | 1395ms | peasoft/NoMoreWalls |
| `31.76.5.144:443` | vless | 1407ms | snakem982/proxypool |
| `31.76.5.137:443` | vless | 1408ms | snakem982/proxypool |
| `viper-23.moriarty-web.com:443` | vless | 1448ms | snakem982/proxypool |
| `31.76.5.124:443` | vless | 1449ms | snakem982/proxypool |
| … | 共 75 个 | | |

#### singbox（68 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `43.155.199.22:80` | vmess | 555ms | peasoft/NoMoreWalls |
| `146.190.157.232:39644` | ss | 628ms | 0xRadikal/Free-v2ray-Configs |
| `91.107.128.44:36812` | vmess | 629ms | snakem982/proxypool |
| `91.107.128.44:24701` | vmess | 663ms | Danialsamadi/v2go |
| `91.107.128.44:46928` | vless | 719ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.234.144:8563` | trojan | 775ms | 0xRadikal/Free-v2ray-Configs |
| `137.184.178.208:4804` | trojan | 783ms | Danialsamadi/v2go |
| `144.126.223.93:8911` | trojan | 822ms | Danialsamadi/v2go |
| `209.38.66.47:6105` | trojan | 839ms | 0xRadikal/Free-v2ray-Configs |
| `45.32.135.70:9213` | trojan | 842ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.232.6:4853` | trojan | 850ms | 0xRadikal/Free-v2ray-Configs |
| `45.32.140.119:9304` | trojan | 858ms | 0xRadikal/Free-v2ray-Configs |
| `147.182.203.237:6022` | trojan | 898ms | Danialsamadi/v2go |
| `149.28.214.139:7604` | trojan | 927ms | 0xRadikal/Free-v2ray-Configs |
| `64.23.151.246:7801` | trojan | 961ms | 0xRadikal/Free-v2ray-Configs |
| `45.38.143.210:30584` | vless | 974ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 1020ms | Pawdroid/Free-servers |
| `post.mailelo.com:443` | vless | 1029ms | Danialsamadi/v2go |
| `164.92.73.218:8931` | trojan | 1048ms | Danialsamadi/v2go |
| `875f9760-be1a-4dfe-8c2b-3f080b5ab158.node1.runet.network:20065` | vless | 1066ms | Danialsamadi/v2go |
| `cz-prg.dontblockmepls.com:2063` | vless | 1098ms | 0xRadikal/Free-v2ray-Configs |
| `47.250.84.25:443` | trojan | 1104ms | peasoft/NoMoreWalls |
| `202.50.253.18:19999` | ss | 1119ms | peasoft/NoMoreWalls |
| `64.83.20.73:8388` | ss | 1133ms | 0xRadikal/Free-v2ray-Configs |
| `91.206.92.238:18443` | ss | 1184ms | peasoft/NoMoreWalls |
| `45.43.79.92:443` | vless | 1217ms | 0xRadikal/Free-v2ray-Configs |
| `31.76.5.124:443` | vless | 1220ms | snakem982/proxypool |
| `9.247.23.209:443` | vless | 1242ms | 0xRadikal/Free-v2ray-Configs |
| `31.76.5.144:443` | vless | 1246ms | snakem982/proxypool |
| `viper-23.moriarty-web.com:443` | vless | 1299ms | snakem982/proxypool |
| `201.24.121.243:443` | vless | 1301ms | peasoft/NoMoreWalls |
| `13.143.172.34:4443` | vless | 1303ms | 0xRadikal/Free-v2ray-Configs |
| `64.176.163.182:443` | trojan | 1326ms | 0xRadikal/Free-v2ray-Configs |
| `50.7.5.166:443` | vless | 1368ms | snakem982/proxypool |
| `se1-cl3.vless-fiberstasis.top:443` | vless | 1386ms | 0xRadikal/Free-v2ray-Configs |
| `norw-mori-5.failspace.top:443` | vless | 1393ms | snakem982/proxypool |
| `rabin.142.251.153.7.savfasf.ir:41432` | vless | 1406ms | 0xRadikal/Free-v2ray-Configs |
| `31.76.5.137:443` | vless | 1411ms | snakem982/proxypool |
| `ee.h1cloud.net:25895` | vless | 1504ms | Pawdroid/Free-servers |
| `24.199.106.240:9998` | trojan | 1510ms | 0xRadikal/Free-v2ray-Configs |
| … | 共 68 个 | | |

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
