# 节点可用性验证汇总（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

## 2026-10-25 13:44

- 预筛：TCP 连通 2002/6632 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 12，每内核单轮 200 个
- 自适应扩量：可用数 < 10 时继续追加测试（单内核累计上限 自动，时间预算 1800s）
- 总耗时：9.0 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 扩量轮次 | 可用文件 |
|---|---|---|---|---|---|
| v2ray | 202 | 27 | 13.4% | 1 | `available_v2ray.txt` |
| xray | 202 | 42 | 20.8% | 1 | `available_xray.txt` |
| clash | 205 | 51 | 24.9% | 1 | `available_clash.yaml` |
| singbox | 204 | 52 | 25.5% | 1 | `available_singbox.json` |

### 可用节点池（跨天累积）

每个内核一份池文件：实测通过的节点自动入池，池内节点次日继续复测，连续多天未通过则淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| v2ray | 27 | 22 | 5 | `pool/pool_v2ray.txt` |
| xray | 43 | 38 | 4 | `pool/pool_xray.txt` |
| clash | 56 | 46 | 5 | `pool/pool_clash.yaml` |
| singbox | 54 | 49 | 3 | `pool/pool_singbox.json` |

池目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes\pool`（`pool_<core>.<ext>` 可直接导入客户端；`pool_state.json` 存首见/最近通过/通过次数/最佳延迟）


### 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| Pawdroid/Free-servers | 40 | 26 | 65% | 3440ms | 45.5 |
| snakem982/proxypool | 155 | 96 | 62% | 1586ms | 43.4 |
| igareck/vpn-configs-for-russia | 6 | 2 | 33% | 7114ms | 23.3 |
| 0xRadikal/Free-v2ray-Configs | 420 | 48 | 11% | 1499ms | 8.0 |
| MatinGhanbari/v2ray-configs | 164 | 0 | 0% | -ms | 30.0 |
| iboxz/free-v2ray-collector | 4 | 0 | 0% | -ms | 30.0 |
| Firmfox/Proxify | 8 | 0 | 0% | -ms | 30.0 |
| VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy | 12 | 0 | 0% | -ms | 30.0 |
| chengaopan/AutoMergePublicNodes | 4 | 0 | 0% | -ms | 30.0 |


### 各内核可用节点详情

#### v2ray（27 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `103.180.20.108:8443` | vless | 707ms | snakem982/proxypool |
| `202.50.253.45:19999` | ss | 912ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.63:19999` | ss | 934ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 935ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 950ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.54:19999` | ss | 954ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.90:19999` | ss | 960ms | 0xRadikal/Free-v2ray-Configs |
| `5.175.205.190:27774` | vless | 985ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 987ms | Pawdroid/Free-servers |
| `45.144.48.32:57891` | vmess | 1010ms | 0xRadikal/Free-v2ray-Configs |
| `195.133.23.50:18443` | ss | 1054ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.72:19999` | ss | 1066ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.18:19999` | ss | 1092ms | snakem982/proxypool |
| `46.17.43.227:18443` | ss | 1188ms | snakem982/proxypool |
| `199.232.239.239:443` | vless | 1309ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 1372ms | Pawdroid/Free-servers |
| `46.243.142.104:443` | vless | 1526ms | 0xRadikal/Free-v2ray-Configs |
| `64.227.115.28:443` | trojan | 1742ms | 0xRadikal/Free-v2ray-Configs |
| `deliverya.online:443` | vless | 1913ms | 0xRadikal/Free-v2ray-Configs |
| `59.125.69.22:443` | vless | 1951ms | snakem982/proxypool |
| `185.86.145.142:443` | vless | 1957ms | 0xRadikal/Free-v2ray-Configs |
| `146.75.59.186:443` | vless | 2181ms | snakem982/proxypool |
| `santehdv.site:443` | vless | 2426ms | snakem982/proxypool |
| `172.66.0.1:443` | vmess | 2487ms | 0xRadikal/Free-v2ray-Configs |
| `49.12.253.100:1080` | ss | 2697ms | 0xRadikal/Free-v2ray-Configs |
| `172.66.1.36:443` | trojan | 6240ms | 0xRadikal/Free-v2ray-Configs |
| `us22.sofast.live:58011` | vless | 10251ms | Pawdroid/Free-servers |

#### xray（42 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `45.144.48.32:57891` | vmess | 865ms | 0xRadikal/Free-v2ray-Configs |
| `147.45.47.107:443` | vless | 905ms | snakem982/proxypool |
| `202.50.253.81:19999` | ss | 918ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 922ms | 0xRadikal/Free-v2ray-Configs |
| `45.128.78.176:443` | vless | 925ms | snakem982/proxypool |
| `202.50.253.63:19999` | ss | 935ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.99:19999` | ss | 937ms | Pawdroid/Free-servers |
| `202.50.253.72:19999` | ss | 960ms | 0xRadikal/Free-v2ray-Configs |
| `45.151.71.162:443` | vless | 961ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 963ms | Pawdroid/Free-servers |
| `45.151.71.165:443` | vless | 978ms | snakem982/proxypool |
| `202.50.253.45:19999` | ss | 994ms | 0xRadikal/Free-v2ray-Configs |
| `195.133.23.50:18443` | ss | 996ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.90:19999` | ss | 1004ms | 0xRadikal/Free-v2ray-Configs |
| `193.160.140.119:443` | vless | 1016ms | snakem982/proxypool |
| `193.223.104.140:443` | vless | 1030ms | snakem982/proxypool |
| `202.50.253.54:19999` | ss | 1047ms | 0xRadikal/Free-v2ray-Configs |
| `91.242.228.29:443` | vless | 1068ms | snakem982/proxypool |
| `147.45.46.169:443` | vless | 1167ms | snakem982/proxypool |
| `201.51.8.163:443` | vless | 1185ms | snakem982/proxypool |
| `177.3.220.124:443` | vless | 1188ms | Pawdroid/Free-servers |
| `se1.mycloud1.org:443` | vless | 1196ms | snakem982/proxypool |
| `pl1.mycloud1.org:443` | vless | 1196ms | snakem982/proxypool |
| `51.77.108.218:8443` | vless | 1226ms | Pawdroid/Free-servers |
| `46.17.43.227:18443` | ss | 1246ms | snakem982/proxypool |
| `lv6.himoy.space:443` | vless | 1248ms | snakem982/proxypool |
| `113.30.154.207:8443` | vless | 1316ms | snakem982/proxypool |
| `213.152.165.204:2092` | vless | 1378ms | snakem982/proxypool |
| `213.152.165.203:2092` | vless | 1434ms | snakem982/proxypool |
| `213.152.165.200:2093` | vless | 1595ms | snakem982/proxypool |
| `83.168.69.15:56229` | vless | 1715ms | Pawdroid/Free-servers |
| `213.152.165.200:2090` | vless | 2049ms | snakem982/proxypool |
| `213.152.165.203:2093` | vless | 2093ms | snakem982/proxypool |
| `213.152.165.205:2090` | vless | 2104ms | snakem982/proxypool |
| `202.50.253.18:19999` | ss | 2119ms | snakem982/proxypool |
| `santehdv.site:443` | vless | 2197ms | snakem982/proxypool |
| `138.124.79.6:443` | vless | 2393ms | Pawdroid/Free-servers |
| `fin3.himoy.space:443` | vless | 2514ms | Pawdroid/Free-servers |
| `213.152.165.203:2095` | vless | 2520ms | snakem982/proxypool |
| `151.241.138.22:443` | vless | 2581ms | Pawdroid/Free-servers |
| … | 共 42 个 | | |

#### clash（51 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `202.50.253.54:19999` | ss | 898ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.63:19999` | ss | 921ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 928ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.27:19999` | ss | 928ms | 0xRadikal/Free-v2ray-Configs |
| `45.144.48.32:57891` | vmess | 931ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.45:19999` | ss | 938ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.72:19999` | ss | 943ms | 0xRadikal/Free-v2ray-Configs |
| `5.175.205.190:27774` | vless | 973ms | snakem982/proxypool |
| `45.151.71.165:443` | vless | 994ms | snakem982/proxypool |
| `202.50.253.18:19999` | ss | 995ms | snakem982/proxypool |
| `46.17.43.227:18443` | ss | 1031ms | snakem982/proxypool |
| `147.45.47.107:443` | vless | 1040ms | snakem982/proxypool |
| `45.128.78.176:443` | vless | 1054ms | snakem982/proxypool |
| `49.12.253.100:1080` | ss | 1080ms | 0xRadikal/Free-v2ray-Configs |
| `51.77.108.218:8443` | vless | 1082ms | Pawdroid/Free-servers |
| `se1.mycloud1.org:443` | vless | 1109ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 1113ms | Pawdroid/Free-servers |
| `193.223.104.140:443` | vless | 1135ms | snakem982/proxypool |
| `91.242.228.29:443` | vless | 1139ms | snakem982/proxypool |
| `103.180.20.108:8443` | vless | 1154ms | snakem982/proxypool |
| `pl1.mycloud1.org:443` | vless | 1161ms | snakem982/proxypool |
| `151.241.138.22:443` | vless | 1171ms | Pawdroid/Free-servers |
| `113.30.154.207:8443` | vless | 1196ms | snakem982/proxypool |
| `147.45.46.169:443` | vless | 1233ms | snakem982/proxypool |
| `201.51.8.163:443` | vless | 1239ms | snakem982/proxypool |
| `lv6.himoy.space:443` | vless | 1303ms | snakem982/proxypool |
| `164.92.223.252:443` | trojan | 1329ms | 0xRadikal/Free-v2ray-Configs |
| `213.152.165.203:2092` | vless | 1362ms | snakem982/proxypool |
| `177.3.220.124:443` | vless | 1415ms | Pawdroid/Free-servers |
| `tjadly.m2k699.com:24999` | trojan | 1451ms | snakem982/proxypool |
| `tjmlxy.m2k699.com:24999` | trojan | 1508ms | snakem982/proxypool |
| `fin3.himoy.space:443` | vless | 1525ms | Pawdroid/Free-servers |
| `213.152.165.200:2093` | vless | 1562ms | snakem982/proxypool |
| `213.152.165.203:2095` | vless | 1585ms | snakem982/proxypool |
| `tjtw.m2k699.com:24999` | trojan | 1628ms | snakem982/proxypool |
| `213.152.165.203:2093` | vless | 1648ms | snakem982/proxypool |
| `tjhg.m2k699.com:24999` | trojan | 1649ms | snakem982/proxypool |
| `tjxg.m2k699.com:24999` | trojan | 1756ms | snakem982/proxypool |
| `santehdv.site:443` | vless | 1778ms | snakem982/proxypool |
| `59.125.69.22:443` | vless | 1802ms | snakem982/proxypool |
| … | 共 51 个 | | |

#### singbox（52 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `103.180.20.108:8443` | vless | 786ms | snakem982/proxypool |
| `5.175.205.190:27774` | vless | 848ms | snakem982/proxypool |
| `202.50.253.18:19999` | ss | 887ms | snakem982/proxypool |
| `202.50.253.27:19999` | ss | 924ms | 0xRadikal/Free-v2ray-Configs |
| `45.151.71.165:443` | vless | 925ms | snakem982/proxypool |
| `202.50.253.72:19999` | ss | 934ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.90:19999` | ss | 934ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.63:19999` | ss | 955ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.54:19999` | ss | 966ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 980ms | 0xRadikal/Free-v2ray-Configs |
| `45.144.48.32:57891` | vmess | 981ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.45:19999` | ss | 985ms | 0xRadikal/Free-v2ray-Configs |
| `193.223.104.140:443` | vless | 1003ms | snakem982/proxypool |
| `59.125.69.22:443` | vless | 1013ms | snakem982/proxypool |
| `195.133.23.50:18443` | ss | 1028ms | 0xRadikal/Free-v2ray-Configs |
| `45.151.71.162:443` | vless | 1049ms | snakem982/proxypool |
| `201.51.8.163:443` | vless | 1056ms | snakem982/proxypool |
| `91.242.228.29:443` | vless | 1145ms | snakem982/proxypool |
| `193.160.140.119:443` | vless | 1149ms | snakem982/proxypool |
| `45.128.78.176:443` | vless | 1149ms | snakem982/proxypool |
| `147.45.47.107:443` | vless | 1178ms | snakem982/proxypool |
| `tjhg.m2k699.com:24999` | trojan | 1184ms | snakem982/proxypool |
| `213.152.165.204:2092` | vless | 1225ms | snakem982/proxypool |
| `pl1.mycloud1.org:443` | vless | 1243ms | snakem982/proxypool |
| `se1.mycloud1.org:443` | vless | 1252ms | snakem982/proxypool |
| `147.45.46.169:443` | vless | 1316ms | snakem982/proxypool |
| `tjxg.m2k699.com:24999` | trojan | 1347ms | snakem982/proxypool |
| `49.12.253.100:1080` | ss | 1380ms | 0xRadikal/Free-v2ray-Configs |
| `113.30.154.207:8443` | vless | 1421ms | snakem982/proxypool |
| `213.152.165.203:2095` | vless | 1578ms | snakem982/proxypool |
| `202.50.253.99:19999` | ss | 1634ms | Pawdroid/Free-servers |
| `213.152.165.203:2092` | vless | 1659ms | snakem982/proxypool |
| `213.152.165.203:2093` | vless | 1677ms | snakem982/proxypool |
| `202.50.253.36:19999` | ss | 1757ms | Pawdroid/Free-servers |
| `46.17.43.227:18443` | ss | 1820ms | snakem982/proxypool |
| `146.75.59.186:443` | vless | 1938ms | snakem982/proxypool |
| `tjadly.m2k699.com:24999` | trojan | 2004ms | snakem982/proxypool |
| `tjmg2.m2k699.com:24999` | trojan | 2127ms | snakem982/proxypool |
| `213.152.165.205:2090` | vless | 2291ms | snakem982/proxypool |
| `213.152.165.200:2090` | vless | 2307ms | snakem982/proxypool |
| … | 共 52 个 | | |
