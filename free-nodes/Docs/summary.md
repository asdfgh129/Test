# 节点可用性验证汇总（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

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
