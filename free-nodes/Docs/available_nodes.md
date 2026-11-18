# 可用节点总表（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

## 2026-11-18 22:36

- 可用节点 **89** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `139.162.20.241:443` | singbox | vless | 465ms | 506ms | 678ms | 377ms | 435ms | 16.04Mbps |
| `172.104.48.194:443` | singbox | vless | 478ms | 506ms | 636ms | 398ms | 508ms | 12.81Mbps |
| `172.105.203.15:443` | singbox | vless | 478ms | 452ms | 590ms | 557ms | 479ms | 11.35Mbps |
| `139.162.91.247:443` | singbox | vless | 492ms | 485ms | 606ms | 462ms | 489ms | 13.24Mbps |
| `139.162.125.126:443` | singbox | vless | 497ms | 475ms | 600ms | 471ms | 432ms | 11.58Mbps |
| `139.162.91.239:443` | singbox | vless | 497ms | 473ms | 570ms | 465ms | 496ms | 11.8Mbps |
| `172.104.86.181:443` | singbox | vless | 540ms | 491ms | 622ms | 510ms | 596ms | 12.25Mbps |
| `103.29.68.232:443` | singbox | vless | 557ms | 524ms | 583ms | 481ms | 614ms | 11.63Mbps |
| `13.212.48.8:8443` | singbox/v2ray/xray | ss | 578ms | 581ms | 843ms | 450ms | 581ms | 0.47Mbps |
| `139.162.101.74:443` | singbox | vless | 614ms | 475ms | 641ms | 516ms | 569ms | 12.51Mbps |
| `139.162.91.224:443` | singbox | vless | 619ms | 561ms | 705ms | 479ms | 489ms | 11.15Mbps |
| `18.176.55.211:2377` | clash/singbox | ss | 651ms | 281ms | 407ms | 338ms | 314ms | 12.03Mbps |
| `172.238.18.103:443` | singbox | vless | 726ms | 510ms | 631ms | 567ms | 522ms | 12.22Mbps |
| `18.134.253.71:443` | clash/singbox/xray | ss | 791ms | 723ms | 881ms | 666ms | 2023ms | 5.25Mbps |
| `free.fugui.lol:47396` | clash/singbox/xray | vless | 853ms | 1200ms | 1954ms | 1625ms | 4467ms | 0.58Mbps |
| `zfapi.zalolink.com:43149` | clash/singbox/xray | vless | 888ms | ✗ | 1779ms | 1615ms | 1347ms | 3.41Mbps |
| `88.216.189.192:443` | clash/singbox/xray | vless | 963ms | 1432ms | 1072ms | 1061ms | 925ms | 5.09Mbps |
| `107.161.160.28:8388` | singbox/v2ray | ss | 1005ms | 1042ms | 2712ms | 2350ms | 1368ms | 0.12Mbps |
| `178.17.58.55:443` | v2ray | hysteria2 | 1024ms | ✗ | ✗ | ✗ | ✗ | - |
| `3.38.150.98:8443` | clash/singbox/v2ray/xray | ss | 1030ms | 498ms | 455ms | 442ms | 477ms | 0.29Mbps |
| `202.50.253.36:19999` | clash/singbox/v2ray/xray | ss | 1081ms | ✗ | 1890ms | 4344ms | 1803ms | 0.48Mbps |
| `47.85.162.44:443` | clash/singbox/xray | ss | 1084ms | ✗ | 995ms | 906ms | 918ms | 4.29Mbps |
| `163.245.42.85:443` | singbox | vless | 1106ms | ✗ | ✗ | 1094ms | ✗ | - |
| `48.103.218.241:18443` | clash/xray | ss | 1124ms | ✗ | 1498ms | 970ms | 1112ms | - |
| `149.28.29.156:443` | singbox | vless | 1134ms | 1551ms | 1998ms | 1712ms | 1125ms | - |
| `88.216.60.73:443` | clash/singbox/xray | vless | 1146ms | 2333ms | 1478ms | 1312ms | 1606ms | 0.7Mbps |
| `3.38.150.98:443` | xray | vless | 1171ms | 818ms | 950ms | 913ms | 674ms | 0.56Mbps |
| `95.133.247.20:8443` | xray | vless | 1275ms | ✗ | 2528ms | 1829ms | 1612ms | 2.61Mbps |
| `81.200.152.153:443` | clash/singbox/xray | vless | 1313ms | 1460ms | 1529ms | 1314ms | 1466ms | 3.92Mbps |
| `185.248.141.233:443` | xray | vless | 1364ms | 1207ms | 1280ms | 853ms | 773ms | 6.05Mbps |
| `191.217.252.92:2053` | clash | vless | 1391ms | 1387ms | ✗ | 1762ms | ✗ | 1.56Mbps |
| `172.236.227.60:443` | singbox | vless | 1392ms | ✗ | 1134ms | 1461ms | 2369ms | - |
| `172.233.142.149:443` | singbox | vless | 1400ms | 2538ms | ✗ | 3000ms | 1422ms | - |
| `150.241.92.19:2096` | xray | vless | 1408ms | ✗ | 2409ms | 1309ms | ✗ | 0.71Mbps |
| `45.147.200.232:18443` | clash/singbox/v2ray/xray | ss | 1423ms | 2279ms | 1073ms | 809ms | 963ms | 0.37Mbps |
| `191.217.206.147:8443` | xray | vless | 1431ms | 2853ms | 3501ms | 756ms | 773ms | 1.5Mbps |
| `198.202.24.214:2083` | singbox/v2ray/xray | vless | 1462ms | 1639ms | 1746ms | 1413ms | 1583ms | 5.31Mbps |
| `202.50.253.90:19999` | singbox/v2ray/xray | ss | 1477ms | ✗ | 1547ms | 2076ms | 1438ms | 0.58Mbps |
| `37.114.37.192:443` | clash/singbox | vless | 1478ms | 1381ms | 1438ms | 831ms | 785ms | 4.62Mbps |
| `18.132.198.49:443` | clash/singbox | ss | 1504ms | 995ms | 1091ms | 862ms | 1232ms | 6.17Mbps |
| `84.32.108.7:443` | clash | vless | 1531ms | 1858ms | 2083ms | 1543ms | 2380ms | 4.91Mbps |
| `202.50.253.27:19999` | singbox/xray | ss | 1531ms | 2197ms | 1936ms | 1286ms | 1650ms | - |
| `91.108.152.89:3051` | clash/singbox/v2ray/xray | vmess | 1534ms | 3011ms | 1639ms | 1567ms | 1587ms | 3.02Mbps |
| `ipfast.kingmna.com:443` | singbox/v2ray | trojan | 1608ms | 1680ms | 1912ms | 1544ms | 1451ms | 0.97Mbps |
| `alireza.karamoz1.ir:443` | clash/singbox/xray | trojan | 1614ms | 1397ms | 1151ms | 1013ms | 2689ms | - |
| `209.206.51.236:2083` | singbox/v2ray | vless | 1640ms | 1688ms | 1607ms | 2488ms | 1514ms | 5.56Mbps |
| `206.238.239.20:2083` | clash/singbox/v2ray/xray | vless | 1696ms | 1716ms | 1700ms | 1609ms | 1552ms | 1.16Mbps |
| `45.76.222.108:443` | singbox | vless | 1720ms | 1747ms | 2168ms | ✗ | ✗ | - |
| `80.47.10.106:443` | singbox | vless | 1788ms | ✗ | 3068ms | 1337ms | 4303ms | - |
| `46.247.109.32:443` | clash/singbox | vless | 1795ms | 2130ms | 1900ms | 1409ms | 1677ms | 3.42Mbps |
| `139.180.221.53:443` | singbox | vless | 1807ms | 1577ms | 1031ms | 1807ms | 605ms | - |
| `202.50.253.99:19999` | singbox/v2ray | ss | 1915ms | ✗ | 1224ms | 2675ms | ✗ | 0.87Mbps |
| `177.202.76.31:9443` | xray | vless | 1959ms | 2338ms | 3095ms | 1269ms | 1059ms | - |
| `172.235.37.168:443` | singbox | vless | 1989ms | 2166ms | 2061ms | ✗ | 2266ms | - |
| `3.144.14.254:443` | clash/singbox | ss | 2014ms | 1943ms | 1293ms | 851ms | 908ms | - |
| `zfapi.zalolink.com:30322` | clash/singbox/xray | vless | 2072ms | 1633ms | ✗ | 1818ms | 1352ms | - |
| `v1us9.stablenode.cloud:24413` | clash/v2ray | trojan | 2162ms | 4426ms | 2063ms | 2841ms | 3161ms | 0.93Mbps |
| `172.235.48.245:443` | singbox | vless | 2281ms | 2224ms | ✗ | 1422ms | 1826ms | - |
| `free.fugui.lol:62015` | singbox/xray | vless | 2299ms | 3232ms | 1430ms | 1370ms | 1437ms | - |
| `zfapi.zalolink.com:54528` | clash/singbox/xray | vless | 2353ms | 2265ms | 1478ms | ✗ | 2483ms | 0.13Mbps |
| `172.236.241.130:443` | singbox | vless | 2359ms | 1218ms | ✗ | 1336ms | 1119ms | - |
| `202.50.253.63:19999` | clash | ss | 2425ms | ✗ | 2320ms | 1956ms | ✗ | - |
| `sclass-00.catcat321.com:20103` | singbox/xray | trojan | 2439ms | 2828ms | 2272ms | 3158ms | 2112ms | - |
| `sclass-00.catcat321.com:20123` | clash/singbox | trojan | 2447ms | ✗ | 3570ms | 1432ms | 2710ms | - |
| `zfapi.zalolink.com:42120` | clash/xray | vless | 2449ms | 1447ms | 1132ms | 1032ms | 1231ms | - |
| `198.13.53.39:443` | singbox | vless | 2456ms | 2003ms | 3090ms | 2487ms | 2172ms | - |
| `5.129.202.80:443` | clash/singbox | vless | 2479ms | ✗ | 2320ms | ✗ | ✗ | - |
| `202.50.253.81:19999` | clash | ss | 2486ms | ✗ | 2266ms | 969ms | 4086ms | - |
| `po2.hys.braidx.tech:9443` | xray | vless | 2511ms | 1957ms | 2679ms | 2781ms | 1556ms | - |
| `172.236.231.45:443` | singbox | vless | 2596ms | 2973ms | ✗ | 2363ms | 1165ms | - |
| `172.236.233.130:443` | singbox | vless | 2663ms | 2695ms | 1704ms | ✗ | 1320ms | - |
| `free.fugui.lol:51283` | xray | vless | 2689ms | ✗ | 3351ms | 1585ms | ✗ | - |
| `172.235.63.167:443` | singbox | vless | 2737ms | ✗ | 1600ms | 1308ms | 2944ms | - |
| `172.233.129.65:443` | singbox | vless | 2800ms | 1264ms | 3157ms | 2662ms | ✗ | - |
| `202.50.253.54:19999` | clash/singbox/xray | ss | 2896ms | ✗ | 4052ms | 3636ms | 1835ms | 0.26Mbps |
| `178.160.228.139:443` | xray | vless | 2921ms | ✗ | 3332ms | ✗ | 1365ms | - |
| `104.17.128.1:2096` | v2ray | trojan | 3081ms | ✗ | ✗ | ✗ | ✗ | - |
| `13.141.51.2:443` | xray | vless | 3084ms | 2642ms | 2431ms | ✗ | 2917ms | - |
| `v1us9.stablenode.cloud:24421` | singbox | trojan | 3106ms | 1831ms | 1827ms | 1998ms | ✗ | - |
| `45.134.111.131:443` | clash/singbox | vless | 3109ms | 3462ms | 2374ms | 1079ms | 3238ms | - |
| `202.50.253.72:19999` | clash/singbox/v2ray/xray | ss | 3185ms | ✗ | 3838ms | 1678ms | 1707ms | 1.14Mbps |
| `107.191.58.86:443` | singbox | vless | 3205ms | 1145ms | 2094ms | 1367ms | 1725ms | - |
| `109.104.153.43:33336` | clash | ssr | 3213ms | 3080ms | 1746ms | ✗ | ✗ | - |
| `109.71.245.99:8443` | xray | vless | 3287ms | 2665ms | ✗ | 1418ms | 1749ms | - |
| `153.56.230.6:443` | clash | vless | 3380ms | ✗ | 1884ms | 2462ms | 1617ms | - |
| `186.243.218.221:8443` | singbox | vless | 3400ms | ✗ | ✗ | ✗ | ✗ | - |
| `202.50.253.18:19999` | singbox/v2ray/xray | ss | 3403ms | ✗ | 4006ms | 1400ms | 2960ms | 0.84Mbps |
| `support.zoom.us:443` | clash/v2ray | vmess | 3569ms | ✗ | ✗ | 3102ms | 2057ms | 1.53Mbps |
| `202.50.253.45:19999` | v2ray/xray | ss | 4179ms | ✗ | 3371ms | 2536ms | 1756ms | 0.77Mbps |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `139.162.20.241:443`：Areral/ScarletDevil
> - `172.104.48.194:443`：Areral/ScarletDevil
> - `172.105.203.15:443`：zhuhaiuk/free-nodes
> - `139.162.91.247:443`：Areral/ScarletDevil
> - `139.162.125.126:443`：Areral/ScarletDevil
> - `139.162.91.239:443`：Areral/ScarletDevil
> - `172.104.86.181:443`：Areral/ScarletDevil
> - `103.29.68.232:443`：Areral/ScarletDevil
> - `13.212.48.8:8443`：hello-world-1989/cn-news
> - `139.162.101.74:443`：Areral/ScarletDevil
> - `139.162.91.224:443`：Areral/ScarletDevil
> - `18.176.55.211:2377`：Areral/ScarletDevil
> - `172.238.18.103:443`：Areral/ScarletDevil
> - `18.134.253.71:443`：rekt0ro/ProxyRift
> - `free.fugui.lol:47396`：FLAT447/v2ray-lists
> - `zfapi.zalolink.com:43149`：zhuhaiuk/free-nodes
> - `88.216.189.192:443`：JHC000abc/ProxyParseForSing-box
> - `107.161.160.28:8388`：SoliSpirit/v2ray-configs
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `3.38.150.98:8443`：hello-world-1989/cn-news
> - `202.50.253.36:19999`：JHC000abc/ProxyParseForSing-box
> - `47.85.162.44:443`：SoliSpirit/v2ray-configs
> - `163.245.42.85:443`：0xRadikal/Free-v2ray-Configs
> - `48.103.218.241:18443`：SoliSpirit/v2ray-configs
> - `149.28.29.156:443`：Areral/ScarletDevil
> - `88.216.60.73:443`：zhuhaiuk/free-nodes
> - `3.38.150.98:443`：hello-world-1989/cn-news
> - `95.133.247.20:8443`：rekt0ro/ProxyRift
> - `81.200.152.153:443`：JHC000abc/ProxyParseForSing-box
> - `185.248.141.233:443`：FLAT447/v2ray-lists
> - `191.217.252.92:2053`：JHC000abc/ProxyParseForSing-box
> - `172.236.227.60:443`：ermaozi01/free_clash_vpn
> - `172.233.142.149:443`：Areral/ScarletDevil
> - `150.241.92.19:2096`：rekt0ro/ProxyRift
> - `45.147.200.232:18443`：10Dream/sub-mod
> - `191.217.206.147:8443`：FLAT447/v2ray-lists
> - `198.202.24.214:2083`：0xRadikal/Free-v2ray-Configs
> - `202.50.253.90:19999`：FLAT447/v2ray-lists
> - `37.114.37.192:443`：FLAT447/v2ray-lists
> - `18.132.198.49:443`：rekt0ro/ProxyRift
> - `84.32.108.7:443`：rekt0ro/ProxyRift
> - `202.50.253.27:19999`：zhuhaiuk/free-nodes
> - `91.108.152.89:3051`：rekt0ro/ProxyRift
> - `ipfast.kingmna.com:443`：SoliSpirit/v2ray-configs
> - `alireza.karamoz1.ir:443`：SoliSpirit/v2ray-configs
> - `209.206.51.236:2083`：0xRadikal/Free-v2ray-Configs
> - `206.238.239.20:2083`：0xRadikal/Free-v2ray-Configs
> - `45.76.222.108:443`：Areral/ScarletDevil
> - `80.47.10.106:443`：JHC000abc/ProxyParseForSing-box
> - `46.247.109.32:443`：FLAT447/v2ray-lists
> - `139.180.221.53:443`：Areral/ScarletDevil
> - `202.50.253.99:19999`：JHC000abc/ProxyParseForSing-box
> - `177.202.76.31:9443`：rekt0ro/ProxyRift
> - `172.235.37.168:443`：Areral/ScarletDevil
> - `3.144.14.254:443`：rekt0ro/ProxyRift
> - `zfapi.zalolink.com:30322`：FLAT447/v2ray-lists
> - `v1us9.stablenode.cloud:24413`：free-proxy-nodes/free-nodes
> - `172.235.48.245:443`：Areral/ScarletDevil
> - `free.fugui.lol:62015`：Areral/ScarletDevil
> - `zfapi.zalolink.com:54528`：FLAT447/v2ray-lists
> - `172.236.241.130:443`：ermaozi01/free_clash_vpn
> - `202.50.253.63:19999`：JHC000abc/ProxyParseForSing-box
> - `sclass-00.catcat321.com:20103`：0xRadikal/Free-v2ray-Configs
> - `sclass-00.catcat321.com:20123`：SoliSpirit/v2ray-configs
> - `zfapi.zalolink.com:42120`：0xRadikal/Free-v2ray-Configs
> - `198.13.53.39:443`：Areral/ScarletDevil
> - `5.129.202.80:443`：JHC000abc/ProxyParseForSing-box
> - `202.50.253.81:19999`：ermaozi01/free_clash_vpn
> - `po2.hys.braidx.tech:9443`：rekt0ro/ProxyRift
> - `172.236.231.45:443`：Areral/ScarletDevil
> - `172.236.233.130:443`：Areral/ScarletDevil
> - `free.fugui.lol:51283`：FLAT447/v2ray-lists
> - `172.235.63.167:443`：Areral/ScarletDevil
> - `172.233.129.65:443`：ermaozi01/free_clash_vpn
> - `202.50.253.54:19999`：JHC000abc/ProxyParseForSing-box
> - `178.160.228.139:443`：rekt0ro/ProxyRift
> - `104.17.128.1:2096`：rekt0ro/ProxyRift
> - `13.141.51.2:443`：FLAT447/v2ray-lists
> - `v1us9.stablenode.cloud:24421`：free-proxy-nodes/free-nodes
> - `45.134.111.131:443`：Areral/ScarletDevil
> - `202.50.253.72:19999`：JHC000abc/ProxyParseForSing-box
> - `107.191.58.86:443`：ermaozi01/free_clash_vpn
> - `109.104.153.43:33336`：rtwo2/FastNodes
> - `109.71.245.99:8443`：FLAT447/v2ray-lists
> - `153.56.230.6:443`：Areral/ScarletDevil
> - `186.243.218.221:8443`：JHC000abc/ProxyParseForSing-box
> - `202.50.253.18:19999`：JHC000abc/ProxyParseForSing-box
> - `support.zoom.us:443`：rekt0ro/ProxyRift
> - `202.50.253.45:19999`：JHC000abc/ProxyParseForSing-box

## 2026-11-17 22:39

- 可用节点 **205** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `172.104.48.194:443` | singbox | vless | 411ms | 728ms | 580ms | ✗ | 452ms | 12.14Mbps |
| `139.162.20.241:443` | singbox | vless | 451ms | 556ms | 624ms | 450ms | 380ms | 13.72Mbps |
| `139.162.125.126:443` | singbox | vless | 467ms | 436ms | 579ms | 466ms | 448ms | 11.13Mbps |
| `172.105.203.15:443` | singbox | vless | 474ms | 457ms | 619ms | 587ms | 2273ms | 11.18Mbps |
| `172.104.86.181:443` | singbox | vless | 491ms | 522ms | 615ms | 525ms | 470ms | 10.96Mbps |
| `139.162.91.239:443` | singbox | vless | 515ms | 458ms | 531ms | 466ms | 506ms | 12.62Mbps |
| `139.162.101.74:443` | singbox | vless | 527ms | 504ms | 578ms | 593ms | 436ms | 11.88Mbps |
| `139.162.91.224:443` | singbox | vless | 543ms | 451ms | 542ms | 503ms | 468ms | 12.81Mbps |
| `3.38.149.130:443` | clash/singbox/xray | vless | 563ms | 451ms | 625ms | 544ms | 537ms | 0.31Mbps |
| `3.38.149.130:8443` | clash/singbox/v2ray/xray | ss | 661ms | 357ms | 478ms | 348ms | 300ms | 0.48Mbps |
| `54.151.179.216:8443` | clash/singbox/v2ray/xray | ss | 742ms | 705ms | 739ms | 725ms | 692ms | 0.26Mbps |
| `172.238.18.103:443` | singbox | vless | 783ms | 1796ms | 567ms | 548ms | 525ms | 11.82Mbps |
| `35.181.169.46:443` | clash/singbox | ss | 841ms | 936ms | 977ms | 1234ms | 855ms | 5.33Mbps |
| `54.151.179.216:443` | clash/singbox/xray | vless | 843ms | 949ms | 1019ms | 1128ms | 1032ms | 0.22Mbps |
| `179.43.140.24:42831` | clash/singbox | vmess | 861ms | ✗ | 977ms | 1193ms | 900ms | 2.65Mbps |
| `88.216.214.159:443` | clash/singbox/xray | vless | 892ms | 984ms | 1130ms | 1078ms | 1001ms | 4.96Mbps |
| `15.188.27.50:443` | singbox | ss | 919ms | 1043ms | 923ms | 802ms | 838ms | 3.64Mbps |
| `93.183.127.54:2087` | xray | vless | 928ms | 950ms | 1155ms | 494ms | 553ms | 3.64Mbps |
| `178.17.58.55:443` | v2ray | hysteria2 | 936ms | ✗ | ✗ | ✗ | ✗ | - |
| `ench-snet-app.w-ctrip.cn:34926` | clash/singbox | trojan | 967ms | ✗ | 885ms | 411ms | 773ms | 0.07Mbps |
| `18.132.198.49:443` | singbox | ss | 968ms | 918ms | 792ms | 813ms | 881ms | - |
| `193.163.19.232:443` | clash/v2ray/xray | vless | 971ms | 990ms | 1020ms | 926ms | 945ms | 0.21Mbps |
| `163.245.42.85:443` | clash/singbox/xray | vless | 1021ms | ✗ | ✗ | 1326ms | ✗ | 3.03Mbps |
| `93.183.127.54:24446` | xray | vless | 1031ms | 1999ms | 1111ms | 514ms | 577ms | 4.76Mbps |
| `202.50.253.18:19999` | clash/v2ray | ss | 1035ms | ✗ | 3380ms | ✗ | 2372ms | 0.57Mbps |
| `93.183.127.54:24445` | xray | vless | 1038ms | 1080ms | 1440ms | 580ms | 593ms | 4.7Mbps |
| `zfapi.zalolink.com:42120` | clash/singbox | vless | 1059ms | 1526ms | 1206ms | 1411ms | 2877ms | 3.41Mbps |
| `se2.h1cloud.net:25191` | xray | vless | 1063ms | 2048ms | 1232ms | 619ms | 704ms | 3.7Mbps |
| `8.35.211.31:8443` | clash/singbox/v2ray/xray | vless | 1066ms | 2064ms | 2470ms | 2633ms | 3028ms | - |
| `202.50.253.45:19999` | v2ray/xray | ss | 1070ms | ✗ | 2326ms | ✗ | 2236ms | 1.0Mbps |
| `104.16.146.243:2083` | v2ray | vless | 1071ms | ✗ | 3748ms | 2523ms | 2962ms | - |
| `84.32.54.237:443` | clash/singbox/xray | vless | 1071ms | 1382ms | 1278ms | 1647ms | 1622ms | 0.3Mbps |
| `104.18.38.159:2083` | v2ray/xray | vless | 1083ms | 1230ms | 1150ms | 1012ms | 1140ms | - |
| `13.143.239.249:443` | xray | vless | 1083ms | 1200ms | 1185ms | 2037ms | 1044ms | 4.0Mbps |
| `202.50.253.36:19999` | clash/singbox/v2ray/xray | ss | 1083ms | ✗ | 1895ms | 1100ms | 2707ms | 0.54Mbps |
| `104.19.17.63:2053` | v2ray | vless | 1083ms | ✗ | 2337ms | ✗ | 2688ms | - |
| `18.133.182.37:443` | clash/singbox | ss | 1097ms | 718ms | 923ms | 882ms | 788ms | 3.7Mbps |
| `104.17.132.154:2087` | v2ray | vless | 1101ms | 2158ms | 4106ms | 3896ms | ✗ | - |
| `84.32.108.7:443` | clash/xray | vless | 1108ms | 1190ms | 2397ms | 565ms | 968ms | 5.24Mbps |
| `104.17.138.140:8443` | v2ray | vless | 1119ms | 1404ms | 3631ms | 2106ms | 1123ms | - |
| `104.19.33.42:2083` | v2ray/xray | vless | 1127ms | 2500ms | 2360ms | 2182ms | 1432ms | - |
| `104.17.216.251:443` | v2ray | vless | 1130ms | ✗ | 2379ms | 2605ms | 1185ms | - |
| `104.18.33.116:2053` | v2ray | vless | 1139ms | ✗ | 3573ms | ✗ | 1946ms | - |
| `172.64.156.209:443` | v2ray | vless | 1144ms | 1441ms | 1700ms | 2835ms | 1922ms | - |
| `zfapi.zalolink.com:55688` | singbox | vless | 1165ms | 1175ms | 1617ms | 1526ms | 1613ms | - |
| `162.159.236.146:2053` | v2ray | vless | 1174ms | ✗ | 2016ms | 3421ms | 1343ms | - |
| `213.171.31.83:443` | v2ray | vless | 1187ms | ✗ | ✗ | ✗ | ✗ | 4.56Mbps |
| `79.132.141.219:443` | clash/v2ray/xray | vless | 1190ms | 2155ms | 1470ms | 1200ms | 1264ms | 5.82Mbps |
| `172.236.227.60:443` | singbox | vless | 1199ms | ✗ | 2655ms | 2087ms | 1086ms | - |
| `172.235.37.168:443` | singbox | vless | 1216ms | 1677ms | ✗ | 3214ms | 2182ms | - |
| `104.19.32.167:8443` | v2ray/xray | vless | 1223ms | 1091ms | 2771ms | 2335ms | 1869ms | - |
| `194.124.211.127:443` | xray | vless | 1225ms | 1718ms | 2630ms | ✗ | ✗ | - |
| `93.183.127.54:24447` | xray | vless | 1233ms | ✗ | 1654ms | 582ms | 659ms | - |
| `172.67.163.208:2053` | v2ray | vless | 1240ms | 2409ms | 1412ms | 1244ms | 1194ms | - |
| `89.125.175.54:8443` | xray | vless | 1242ms | 1470ms | 1625ms | 1157ms | 1199ms | - |
| `48.102.160.14:443` | xray | vless | 1250ms | 568ms | 691ms | 601ms | 518ms | - |
| `172.64.153.131:8443` | v2ray | vless | 1251ms | 1889ms | 2844ms | 1392ms | 1530ms | - |
| `345739t.de15.h1clayd.click:443` | clash/singbox/xray | vless | 1256ms | 1791ms | 1563ms | 3300ms | ✗ | - |
| `45.32.70.42:443` | singbox | vless | 1260ms | 2600ms | 2336ms | ✗ | 2061ms | - |
| `91.99.18.148:8080` | xray | vless | 1264ms | 1019ms | 1133ms | 1006ms | 1050ms | - |
| `172.235.48.245:443` | singbox | vless | 1290ms | 1714ms | 1396ms | 1129ms | 3352ms | - |
| `136.148.215.248:25191` | xray | vless | 1293ms | 1082ms | 1152ms | 589ms | 735ms | - |
| `88.216.60.73:443` | singbox/xray | vless | 1316ms | ✗ | 3803ms | 2269ms | 1787ms | - |
| `edge.bookmai.com:443` | clash/singbox/xray | vless | 1317ms | ✗ | ✗ | 1505ms | ✗ | - |
| `109.238.95.229:443` | clash/v2ray/xray | vless | 1325ms | 1223ms | 1546ms | 1403ms | 1291ms | 5.3Mbps |
| `202.50.253.99:19999` | clash/singbox/v2ray/xray | ss | 1344ms | 2064ms | 3318ms | 1304ms | 1284ms | 0.48Mbps |
| `zfapi.zalolink.com:43149` | clash/singbox | vless | 1345ms | ✗ | 1894ms | 1868ms | 847ms | 0.38Mbps |
| `89.127.192.104:443` | clash/v2ray/xray | vless | 1358ms | 1411ms | 2559ms | 1268ms | 1403ms | 4.91Mbps |
| `172.64.153.205:2087` | v2ray | vless | 1359ms | 1514ms | 1527ms | 1384ms | 1343ms | - |
| `163.245.42.87:443` | clash/singbox/xray | vless | 1364ms | ✗ | ✗ | 1195ms | ✗ | - |
| `104.16.243.122:2053` | v2ray | vless | 1365ms | ✗ | 1438ms | 1390ms | 1388ms | - |
| `85.136.112.166:443` | clash/v2ray/xray | vless | 1370ms | 1414ms | 1310ms | 1333ms | 1377ms | - |
| `172.64.153.109:2096` | v2ray | vless | 1373ms | 2907ms | 1644ms | 2922ms | 2096ms | - |
| `172.67.72.110:2083` | v2ray | vless | 1375ms | 2077ms | 2929ms | 1080ms | 1200ms | - |
| `37.128.204.210:443` | v2ray/xray | vless | 1397ms | 2207ms | 1590ms | 1406ms | 1563ms | - |
| `83.136.210.129:443` | xray | vless | 1410ms | 3210ms | ✗ | ✗ | ✗ | - |
| `104.19.35.11:2053` | v2ray/xray | vless | 1412ms | 2447ms | 2191ms | 1824ms | 1648ms | - |
| `104.19.59.53:2087` | v2ray | vless | 1416ms | ✗ | 2121ms | 2773ms | 1294ms | - |
| `138.2.66.236:443` | v2ray/xray | vless | 1417ms | 1501ms | 2115ms | 1351ms | 2086ms | - |
| `win2loxfde0202.gggrelay.org:42120` | xray | vless | 1433ms | 829ms | 996ms | 824ms | 875ms | - |
| `37.252.189.207:443` | clash/v2ray/xray | vless | 1434ms | 1391ms | 1424ms | 3047ms | 1234ms | 5.0Mbps |
| `104.18.33.235:2087` | v2ray | vless | 1435ms | 1356ms | 2288ms | 1195ms | 1087ms | - |
| `161.118.211.215:443` | clash/v2ray/xray | vless | 1439ms | 1019ms | 2133ms | 1360ms | 1311ms | 3.27Mbps |
| `104.20.30.179:2096` | xray | vless | 1450ms | ✗ | 1842ms | 1142ms | 2103ms | - |
| `206.238.239.20:2083` | xray | vless | 1462ms | 2239ms | 1857ms | 2066ms | 1480ms | - |
| `172.67.163.209:2087` | v2ray/xray | vless | 1464ms | 2875ms | 1940ms | 3142ms | 1416ms | - |
| `172.67.163.151:2096` | v2ray/xray | vless | 1467ms | 1561ms | 1571ms | 2197ms | 1112ms | - |
| `48.103.231.8:443` | clash/singbox/xray | vless | 1467ms | 1094ms | 1674ms | 989ms | 1278ms | - |
| `83.141.92.168:443` | xray | vless | 1482ms | 1558ms | 1632ms | 1728ms | 1545ms | - |
| `194.88.150.221:443` | clash/v2ray/xray | vless | 1483ms | 1392ms | 1701ms | 1508ms | 1396ms | 5.03Mbps |
| `104.17.144.15:2087` | v2ray | vless | 1488ms | 1081ms | 3359ms | 1433ms | 1111ms | - |
| `107.191.58.86:443` | singbox | vless | 1492ms | 1323ms | ✗ | 2338ms | 1520ms | - |
| `206.238.237.25:2083` | xray | vless | 1503ms | 1797ms | 1688ms | 1801ms | 1672ms | - |
| `104.17.140.91:2053` | v2ray | vless | 1504ms | ✗ | 2830ms | ✗ | ✗ | - |
| `212.64.199.223:8443` | v2ray/xray | vless | 1504ms | 1591ms | 1567ms | 1177ms | 1262ms | - |
| `104.19.50.142:443` | v2ray | vless | 1510ms | 1755ms | 3089ms | ✗ | 3235ms | - |
| `202.50.253.72:19999` | singbox/v2ray | ss | 1510ms | ✗ | 1881ms | 1102ms | 1425ms | - |
| `172.67.163.150:2087` | v2ray | vless | 1514ms | 1269ms | ✗ | 1936ms | 1263ms | - |
| `209.94.90.201:2083` | xray | vless | 1520ms | 1779ms | 1947ms | 2624ms | 1473ms | - |
| `206.238.239.245:2083` | xray | vless | 1522ms | 1628ms | 1960ms | 1795ms | 1431ms | - |
| `83.228.199.3:443` | v2ray/xray | vless | 1523ms | 1619ms | 1577ms | 1285ms | 1250ms | - |
| `104.18.42.16:443` | v2ray | vless | 1531ms | ✗ | 2183ms | ✗ | 2014ms | - |
| `104.17.136.102:2087` | v2ray | vless | 1533ms | ✗ | 2261ms | 1182ms | 1652ms | - |
| `209.206.51.236:2083` | xray | vless | 1564ms | 1583ms | 1750ms | 1793ms | 1450ms | - |
| `82.153.135.54:443` | clash/xray | vless | 1580ms | 1759ms | 1330ms | 1761ms | 2182ms | - |
| `199.232.249.131:443` | clash/singbox/v2ray | trojan | 1589ms | 1715ms | 2230ms | 3051ms | ✗ | - |
| `142.248.83.184:8443` | v2ray | vless | 1605ms | 2815ms | ✗ | 2968ms | ✗ | - |
| `104.17.137.59:2053` | v2ray | vless | 1615ms | 3158ms | 1688ms | 1931ms | ✗ | - |
| `64.188.97.205:443` | v2ray/xray | vless | 1629ms | 2846ms | 3113ms | 1288ms | 2712ms | - |
| `202.50.253.27:19999` | clash/singbox/xray | ss | 1647ms | 1183ms | 1168ms | 1052ms | 4034ms | - |
| `179.253.162.19:443` | clash/singbox/v2ray/xray | hysteria2 | 1660ms | 666ms | 830ms | 848ms | 1567ms | - |
| `94.183.164.96:443` | xray | vless | 1692ms | 1107ms | 1150ms | 543ms | 596ms | - |
| `lv-s1.balalayka-proxy.com:12837` | xray | vless | 1693ms | 636ms | 773ms | 460ms | 626ms | - |
| `104.18.39.63:8443` | v2ray | vless | 1707ms | ✗ | 2320ms | 1844ms | 2847ms | - |
| `104.16.218.13:2053` | v2ray/xray | vless | 1713ms | 2738ms | ✗ | 2918ms | 2558ms | - |
| `104.16.205.138:2083` | v2ray | vless | 1714ms | ✗ | 2149ms | 3197ms | 1936ms | - |
| `172.233.129.172:443` | singbox | vless | 1730ms | 3088ms | 2897ms | 2237ms | 1317ms | - |
| `172.64.146.85:2096` | v2ray | vless | 1744ms | 1425ms | 2051ms | 1493ms | 1500ms | - |
| `194.87.47.165:443` | v2ray/xray | vless | 1760ms | 2749ms | 2394ms | 2229ms | 1805ms | - |
| `zfapi.zalolink.com:30322` | singbox | vless | 1777ms | ✗ | 2907ms | 2179ms | ✗ | - |
| … | 共 205 个 | | | | | |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `172.104.48.194:443`：ermaozi01/free_clash_vpn
> - `139.162.20.241:443`：Areral/ScarletDevil
> - `139.162.125.126:443`：Areral/ScarletDevil
> - `172.105.203.15:443`：ermaozi01/free_clash_vpn
> - `172.104.86.181:443`：ermaozi01/free_clash_vpn
> - `139.162.91.239:443`：Areral/ScarletDevil
> - `139.162.101.74:443`：ermaozi01/free_clash_vpn
> - `139.162.91.224:443`：ermaozi01/free_clash_vpn
> - `3.38.149.130:443`：hello-world-1989/cn-news
> - `3.38.149.130:8443`：hello-world-1989/cn-news
> - `54.151.179.216:8443`：hello-world-1989/cn-news
> - `172.238.18.103:443`：Areral/ScarletDevil
> - `35.181.169.46:443`：rekt0ro/ProxyRift
> - `54.151.179.216:443`：hello-world-1989/cn-news
> - `179.43.140.24:42831`：JHC000abc/ProxyParseForSing-box
> - `88.216.214.159:443`：zhuhaiuk/free-nodes
> - `15.188.27.50:443`：rekt0ro/ProxyRift
> - `93.183.127.54:2087`：rekt0ro/ProxyRift
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `ench-snet-app.w-ctrip.cn:34926`：Areral/ScarletDevil
> - `18.132.198.49:443`：rekt0ro/ProxyRift
> - `193.163.19.232:443`：rekt0ro/ProxyRift
> - `163.245.42.85:443`：Areral/ScarletDevil
> - `93.183.127.54:24446`：rekt0ro/ProxyRift
> - `202.50.253.18:19999`：JHC000abc/ProxyParseForSing-box
> - `93.183.127.54:24445`：rekt0ro/ProxyRift
> - `zfapi.zalolink.com:42120`：rekt0ro/ProxyRift
> - `se2.h1cloud.net:25191`：rekt0ro/ProxyRift
> - `8.35.211.31:8443`：rekt0ro/ProxyRift
> - `202.50.253.45:19999`：JHC000abc/ProxyParseForSing-box
> - `104.16.146.243:2083`：rekt0ro/ProxyRift
> - `84.32.54.237:443`：HamoonSoleimani/Pr0xySh4rk
> - `104.18.38.159:2083`：rekt0ro/ProxyRift
> - `13.143.239.249:443`：rekt0ro/ProxyRift
> - `202.50.253.36:19999`：JHC000abc/ProxyParseForSing-box
> - `104.19.17.63:2053`：rekt0ro/ProxyRift
> - `18.133.182.37:443`：rekt0ro/ProxyRift
> - `104.17.132.154:2087`：rekt0ro/ProxyRift
> - `84.32.108.7:443`：rekt0ro/ProxyRift
> - `104.17.138.140:8443`：rekt0ro/ProxyRift
> - `104.19.33.42:2083`：rekt0ro/ProxyRift
> - `104.17.216.251:443`：rekt0ro/ProxyRift
> - `104.18.33.116:2053`：rekt0ro/ProxyRift
> - `172.64.156.209:443`：rekt0ro/ProxyRift
> - `zfapi.zalolink.com:55688`：JHC000abc/ProxyParseForSing-box
> - `162.159.236.146:2053`：rekt0ro/ProxyRift
> - `213.171.31.83:443`：sakha1370/OpenRay
> - `79.132.141.219:443`：rekt0ro/ProxyRift
> - `172.236.227.60:443`：ermaozi01/free_clash_vpn
> - `172.235.37.168:443`：ermaozi01/free_clash_vpn
> - `104.19.32.167:8443`：rekt0ro/ProxyRift
> - `194.124.211.127:443`：rekt0ro/ProxyRift
> - `93.183.127.54:24447`：rekt0ro/ProxyRift
> - `172.67.163.208:2053`：rekt0ro/ProxyRift
> - `89.125.175.54:8443`：0xRadikal/Free-v2ray-Configs
> - `48.102.160.14:443`：rekt0ro/ProxyRift
> - `172.64.153.131:8443`：rekt0ro/ProxyRift
> - `345739t.de15.h1clayd.click:443`：0xRadikal/Free-v2ray-Configs
> - `45.32.70.42:443`：ermaozi01/free_clash_vpn
> - `91.99.18.148:8080`：rekt0ro/ProxyRift
> - `172.235.48.245:443`：Areral/ScarletDevil
> - `136.148.215.248:25191`：rekt0ro/ProxyRift
> - `88.216.60.73:443`：zhuhaiuk/free-nodes
> - `edge.bookmai.com:443`：0xRadikal/Free-v2ray-Configs
> - `109.238.95.229:443`：rekt0ro/ProxyRift
> - `202.50.253.99:19999`：JHC000abc/ProxyParseForSing-box
> - `zfapi.zalolink.com:43149`：JHC000abc/ProxyParseForSing-box
> - `89.127.192.104:443`：rekt0ro/ProxyRift
> - `172.64.153.205:2087`：rekt0ro/ProxyRift
> - `163.245.42.87:443`：0xRadikal/Free-v2ray-Configs
> - `104.16.243.122:2053`：rekt0ro/ProxyRift
> - `85.136.112.166:443`：rekt0ro/ProxyRift
> - `172.64.153.109:2096`：rekt0ro/ProxyRift
> - `172.67.72.110:2083`：rekt0ro/ProxyRift
> - `37.128.204.210:443`：rekt0ro/ProxyRift
> - `83.136.210.129:443`：rekt0ro/ProxyRift
> - `104.19.35.11:2053`：rekt0ro/ProxyRift
> - `104.19.59.53:2087`：rekt0ro/ProxyRift
> - `138.2.66.236:443`：rekt0ro/ProxyRift
> - `win2loxfde0202.gggrelay.org:42120`：rekt0ro/ProxyRift
> - `37.252.189.207:443`：rekt0ro/ProxyRift
> - `104.18.33.235:2087`：rekt0ro/ProxyRift
> - `161.118.211.215:443`：rekt0ro/ProxyRift
> - `104.20.30.179:2096`：rekt0ro/ProxyRift
> - `206.238.239.20:2083`：0xRadikal/Free-v2ray-Configs
> - `172.67.163.209:2087`：rekt0ro/ProxyRift
> - `172.67.163.151:2096`：rekt0ro/ProxyRift
> - `48.103.231.8:443`：Areral/ScarletDevil
> - `83.141.92.168:443`：0xRadikal/Free-v2ray-Configs
> - `194.88.150.221:443`：rekt0ro/ProxyRift
> - `104.17.144.15:2087`：rekt0ro/ProxyRift
> - `107.191.58.86:443`：ermaozi01/free_clash_vpn
> - `206.238.237.25:2083`：0xRadikal/Free-v2ray-Configs
> - `104.17.140.91:2053`：rekt0ro/ProxyRift
> - `212.64.199.223:8443`：rekt0ro/ProxyRift
> - `104.19.50.142:443`：rekt0ro/ProxyRift
> - `202.50.253.72:19999`：JHC000abc/ProxyParseForSing-box
> - `172.67.163.150:2087`：rekt0ro/ProxyRift
> - `209.94.90.201:2083`：0xRadikal/Free-v2ray-Configs
> - `206.238.239.245:2083`：0xRadikal/Free-v2ray-Configs
> - `83.228.199.3:443`：rekt0ro/ProxyRift
> - `104.18.42.16:443`：rekt0ro/ProxyRift
> - `104.17.136.102:2087`：rekt0ro/ProxyRift
> - `209.206.51.236:2083`：0xRadikal/Free-v2ray-Configs
> - `82.153.135.54:443`：rekt0ro/ProxyRift
> - `199.232.249.131:443`：rekt0ro/ProxyRift
> - `142.248.83.184:8443`：rekt0ro/ProxyRift
> - `104.17.137.59:2053`：rekt0ro/ProxyRift
> - `64.188.97.205:443`：rekt0ro/ProxyRift
> - `202.50.253.27:19999`：zhuhaiuk/free-nodes
> - `179.253.162.19:443`：rekt0ro/ProxyRift
> - `94.183.164.96:443`：rekt0ro/ProxyRift
> - `lv-s1.balalayka-proxy.com:12837`：rekt0ro/ProxyRift
> - `104.18.39.63:8443`：rekt0ro/ProxyRift
> - `104.16.218.13:2053`：rekt0ro/ProxyRift
> - `104.16.205.138:2083`：rekt0ro/ProxyRift
> - `172.233.129.172:443`：Areral/ScarletDevil
> - `172.64.146.85:2096`：rekt0ro/ProxyRift
> - `194.87.47.165:443`：rekt0ro/ProxyRift
> - `zfapi.zalolink.com:30322`：JHC000abc/ProxyParseForSing-box

## 2026-11-16 22:54

- 可用节点 **189** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `13.125.215.163:8443` | v2ray/xray | ss | 292ms | 442ms | 390ms | 236ms | 369ms | 0.42Mbps |
| `139.180.215.25:443` | singbox | vless | 544ms | 964ms | 3181ms | 667ms | 1539ms | 12.54Mbps |
| `172.105.212.91:443` | singbox | vless | 572ms | 563ms | 616ms | 481ms | 491ms | 12.7Mbps |
| `172.238.18.103:443` | singbox | vless | 575ms | 749ms | 755ms | 659ms | 646ms | 11.95Mbps |
| `139.162.91.250:443` | singbox | vless | 579ms | 647ms | 718ms | 690ms | 568ms | 12.06Mbps |
| `139.162.125.126:443` | singbox | vless | 593ms | 527ms | 589ms | 505ms | 506ms | 11.96Mbps |
| `139.162.91.137:443` | singbox | vless | 602ms | 663ms | 645ms | 560ms | 522ms | 11.11Mbps |
| `139.162.91.249:443` | singbox | vless | 606ms | 704ms | 746ms | 558ms | 653ms | 11.12Mbps |
| `139.162.91.200:443` | singbox | vless | 612ms | 550ms | 666ms | 531ms | 486ms | 12.88Mbps |
| `172.104.86.181:443` | singbox | vless | 626ms | 529ms | 640ms | 569ms | 636ms | 12.6Mbps |
| `172.104.186.205:443` | singbox | vless | 638ms | 918ms | 766ms | 654ms | 1024ms | 10.8Mbps |
| `139.162.101.74:443` | singbox | vless | 647ms | 636ms | 752ms | 678ms | 710ms | 12.25Mbps |
| `139.162.91.224:443` | singbox | vless | 649ms | 697ms | 733ms | 846ms | 733ms | 11.46Mbps |
| `172.105.197.24:443` | singbox | vless | 665ms | 581ms | 742ms | 682ms | 549ms | 12.02Mbps |
| `172.237.14.205:443` | singbox | vless | 683ms | 627ms | 644ms | 701ms | 615ms | 1.4Mbps |
| `172.104.105.212:443` | singbox | vless | 695ms | 568ms | 711ms | 708ms | 627ms | 13.13Mbps |
| `172.105.216.21:443` | singbox | vless | 696ms | 680ms | 691ms | 554ms | 522ms | 12.53Mbps |
| `172.105.203.15:443` | singbox | vless | 708ms | 657ms | 688ms | 600ms | 662ms | 12.28Mbps |
| `15.188.27.50:443` | clash/singbox | ss | 726ms | 688ms | 834ms | 704ms | 700ms | - |
| `139.162.89.151:443` | singbox | vless | 731ms | 651ms | 724ms | 567ms | 472ms | 12.28Mbps |
| `139.180.221.53:443` | singbox | vless | 776ms | 1454ms | 838ms | 1286ms | 438ms | 2.33Mbps |
| `149.28.152.20:443` | singbox | vless | 783ms | 1320ms | 3316ms | ✗ | 1683ms | 5.19Mbps |
| `13.38.60.238:443` | singbox | ss | 839ms | 948ms | 837ms | ✗ | 836ms | - |
| `139.162.91.239:443` | singbox | vless | 862ms | 612ms | 684ms | 723ms | 664ms | - |
| `139.162.91.232:443` | singbox | vless | 879ms | 622ms | 721ms | 527ms | 487ms | - |
| `88.216.211.36:443` | clash/singbox | vless | 884ms | 984ms | 2019ms | 1021ms | 1054ms | 0.3Mbps |
| `15.236.134.147:443` | clash/singbox | ss | 891ms | 772ms | 801ms | 744ms | 698ms | 6.0Mbps |
| `172.104.48.194:443` | singbox | vless | 912ms | 902ms | 793ms | 743ms | 911ms | - |
| `163.245.42.87:443` | clash/singbox/xray | vless | 922ms | ✗ | ✗ | 1039ms | ✗ | 4.62Mbps |
| `185.79.19.8:443` | xray | vless | 959ms | ✗ | 1172ms | 1058ms | 994ms | - |
| `185.231.204.244:443` | xray | vless | 970ms | 2009ms | 2820ms | 1202ms | 1667ms | 2.39Mbps |
| `185.79.19.7:443` | xray | vless | 988ms | ✗ | 1160ms | 969ms | 828ms | - |
| `139.162.20.241:443` | singbox | vless | 989ms | 575ms | 722ms | 570ms | 518ms | - |
| `178.17.58.55:443` | v2ray | hysteria2 | 992ms | ✗ | ✗ | ✗ | ✗ | - |
| `serv1.fishtohome.ru:443` | clash/xray | vless | 995ms | 1245ms | 1083ms | 1303ms | 1014ms | 4.1Mbps |
| `88.216.60.73:443` | singbox/xray | vless | 1037ms | 1667ms | 1262ms | 1152ms | 988ms | 4.99Mbps |
| `79.182.39.138:443` | singbox/xray | vless | 1039ms | 1012ms | 1354ms | 996ms | 1068ms | 1.43Mbps |
| `84.32.149.211:443` | clash | vless | 1057ms | 643ms | 709ms | 573ms | 634ms | 3.8Mbps |
| `202.50.253.45:19999` | clash/singbox/v2ray | ss | 1065ms | ✗ | 3305ms | 3059ms | 1591ms | 0.86Mbps |
| `153.76.204.5:443` | xray | vless | 1076ms | 951ms | 1368ms | 960ms | 1234ms | 3.79Mbps |
| `89.125.175.24:8443` | xray | vless | 1091ms | 1347ms | 1334ms | 1167ms | 1215ms | 4.63Mbps |
| `88.216.189.20:8443` | clash/singbox/xray | vless | 1112ms | ✗ | 715ms | 436ms | 452ms | 5.54Mbps |
| `178.130.46.226:443` | clash/xray | vless | 1112ms | 1260ms | 1273ms | 1196ms | 1031ms | 4.78Mbps |
| `51.75.118.18:20113` | v2ray | vless | 1115ms | ✗ | ✗ | 1036ms | ✗ | 6.07Mbps |
| `93.183.127.54:2087` | xray | vless | 1119ms | 1037ms | 1081ms | 561ms | 611ms | 4.43Mbps |
| `136.148.208.218:443` | clash/singbox/xray | vless | 1126ms | 1172ms | 1275ms | 1343ms | 1087ms | 4.91Mbps |
| `47.85.201.22:443` | clash/singbox/xray | ss | 1159ms | 944ms | 1234ms | 1445ms | 2006ms | 0.12Mbps |
| `213.171.31.83:443` | singbox/v2ray | vless | 1170ms | ✗ | ✗ | 1044ms | ✗ | 4.3Mbps |
| `172.233.139.212:443` | singbox | vless | 1183ms | 1483ms | 3056ms | 1443ms | 1104ms | - |
| `37.49.225.93:443` | clash | vless | 1183ms | 3124ms | 1595ms | ✗ | 1477ms | 0.11Mbps |
| `172.235.37.163:443` | singbox | vless | 1189ms | 1484ms | 3025ms | 1922ms | 2314ms | - |
| `zfapi.zalolink.com:55688` | clash | vless | 1210ms | 1282ms | 1203ms | 1439ms | ✗ | - |
| `176.98.176.60:443` | clash/singbox | vless | 1221ms | 2316ms | 1550ms | 1274ms | 2593ms | - |
| `172.235.50.209:443` | singbox | vless | 1230ms | ✗ | 2566ms | 1297ms | 2268ms | - |
| `89.23.107.105:443` | clash/singbox/xray | vless | 1231ms | 506ms | 664ms | 545ms | 525ms | 5.28Mbps |
| `109.71.245.99:8443` | xray | vless | 1231ms | 1554ms | 1432ms | 642ms | 657ms | 4.95Mbps |
| `172.239.67.142:443` | singbox | vless | 1238ms | 1343ms | 3115ms | ✗ | 1198ms | - |
| `84.32.248.124:443` | clash/singbox/xray | vless | 1240ms | 1113ms | 1137ms | 1150ms | 1166ms | 4.77Mbps |
| `84.32.108.7:443` | clash | vless | 1249ms | 1310ms | 1300ms | 2410ms | 1227ms | - |
| `vpn.asdfghjuyt.ru:9443` | clash | vless | 1260ms | 1596ms | 1122ms | 1338ms | 1763ms | - |
| `172.235.49.52:443` | singbox | vless | 1285ms | 1278ms | 1435ms | 1152ms | 1945ms | - |
| `172.235.36.156:443` | singbox | vless | 1287ms | 1505ms | 2719ms | 1948ms | 2847ms | - |
| `172.233.146.140:443` | singbox | vless | 1292ms | 1695ms | 1699ms | 1096ms | 1183ms | - |
| `104.171.133.209:443` | singbox | vless | 1295ms | ✗ | ✗ | ✗ | ✗ | - |
| `217.60.27.93:443` | xray | vless | 1296ms | 1155ms | 1504ms | 1355ms | 1736ms | 1.65Mbps |
| `23.155.44.105:443` | xray | vless | 1300ms | ✗ | 2171ms | 1495ms | 2853ms | - |
| `31.77.236.131:443` | xray | vless | 1302ms | ✗ | ✗ | ✗ | 1718ms | - |
| `win2loxfde0202.gggrelay.org:54528` | clash/singbox/xray | vless | 1321ms | ✗ | 3238ms | 919ms | 1122ms | 7.69Mbps |
| `45.32.70.42:443` | singbox | vless | 1321ms | 1491ms | ✗ | 1353ms | 1317ms | - |
| `202.50.253.18:19999` | clash/singbox/v2ray/xray | ss | 1340ms | ✗ | 3944ms | 1102ms | 3819ms | 0.62Mbps |
| `195.72.62.7:443` | clash/singbox/xray | vless | 1347ms | 1532ms | 1464ms | 930ms | 1059ms | - |
| `84.32.149.222:443` | clash/xray | vless | 1353ms | 573ms | 717ms | 494ms | 646ms | - |
| `129.101.100.219:443` | clash | vless | 1362ms | 1371ms | 1433ms | ✗ | 1347ms | - |
| `193.233.90.115:8443` | xray | vless | 1370ms | 1484ms | 1576ms | 841ms | 870ms | - |
| `172.233.157.18:443` | singbox | vless | 1377ms | 1577ms | 1621ms | 1881ms | 1916ms | - |
| `89.106.88.126:443` | clash/singbox/xray | vless | 1380ms | 590ms | 806ms | 630ms | 551ms | - |
| `172.235.32.253:443` | singbox | vless | 1404ms | 2503ms | 1661ms | 1536ms | 1492ms | - |
| `72.56.4.84:443` | clash/singbox | vless | 1408ms | ✗ | 2048ms | 2403ms | 1360ms | - |
| `188.225.24.62:443` | clash/singbox/xray | vless | 1413ms | 2668ms | 3161ms | 1361ms | 1597ms | - |
| `84.32.54.237:443` | clash/singbox/xray | vless | 1425ms | 1552ms | 1825ms | 959ms | 1928ms | - |
| `zfapi.zalolink.com:43149` | clash | vless | 1433ms | ✗ | ✗ | ✗ | 1073ms | - |
| `172.235.51.71:443` | singbox | vless | 1434ms | 2149ms | 1858ms | 2228ms | 1347ms | - |
| `89.125.175.55:8443` | xray | vless | 1440ms | 1392ms | 1257ms | 1182ms | 1203ms | - |
| `107.191.58.86:443` | singbox | vless | 1442ms | 1483ms | 1272ms | 1606ms | 1643ms | - |
| `172.233.129.172:443` | singbox | vless | 1456ms | 2363ms | 1628ms | 1114ms | 2432ms | - |
| `172.236.241.130:443` | singbox | vless | 1459ms | ✗ | 2022ms | 1199ms | 1162ms | - |
| `tgfree.rush-server.com:443` | singbox | vless | 1464ms | ✗ | ✗ | ✗ | ✗ | - |
| `ee.point.cookie-line.cc:443` | clash/singbox/xray | vless | 1469ms | 1275ms | 1231ms | 1317ms | 1178ms | - |
| `172.235.53.103:443` | singbox | vless | 1511ms | 1221ms | ✗ | 1860ms | 3070ms | - |
| `48.103.120.3:443` | clash/singbox | vless | 1516ms | 2116ms | 3136ms | 1862ms | 2785ms | - |
| `77.83.245.22:443` | clash/singbox/xray | vless | 1539ms | 682ms | 728ms | 586ms | 691ms | - |
| `138.124.181.197:443` | clash/singbox | vless | 1560ms | 1138ms | 1349ms | 1058ms | 1611ms | - |
| `201.51.11.65:443` | clash/singbox | vless | 1568ms | 1565ms | 1519ms | 2645ms | 2139ms | - |
| `138.16.206.147:443` | xray | vless | 1569ms | ✗ | 1115ms | 1323ms | 1334ms | - |
| `45.77.8.233:443` | singbox | vless | 1580ms | 2271ms | 2444ms | 2202ms | ✗ | - |
| `172.236.238.71:443` | singbox | vless | 1599ms | ✗ | 2018ms | 1849ms | 1112ms | - |
| `84.23.52.104:9071` | xray | vless | 1608ms | 706ms | 825ms | 689ms | 1170ms | - |
| `172.235.63.167:443` | singbox | vless | 1608ms | 1490ms | ✗ | 1847ms | 2195ms | - |
| `45.76.172.197:443` | singbox | vless | 1614ms | 1164ms | 3281ms | 1400ms | 2088ms | - |
| `179.254.127.194:443` | xray | vless | 1617ms | 2640ms | 1399ms | 1286ms | 1487ms | - |
| `13.143.239.238:443` | xray | vless | 1622ms | 1610ms | 1057ms | 585ms | 1588ms | - |
| `194.55.167.133:443` | clash/singbox/xray | vless | 1624ms | 1813ms | 1606ms | 1315ms | 1893ms | - |
| `172.233.142.149:443` | singbox | vless | 1626ms | 2178ms | 2988ms | 1256ms | ✗ | - |
| `172.236.239.126:443` | singbox | vless | 1629ms | 3489ms | 1197ms | 2109ms | ✗ | - |
| `89.144.8.91:18888` | clash/v2ray | hysteria2 | 1642ms | ✗ | 719ms | 574ms | 552ms | 7.0Mbps |
| `83.141.70.167:443` | clash/singbox/xray | vless | 1660ms | 1613ms | 1713ms | 1427ms | 1543ms | - |
| `45.76.106.69:443` | singbox | vless | 1671ms | 2185ms | 2288ms | 1681ms | ✗ | - |
| `172.233.140.139:443` | singbox | vless | 1674ms | 2075ms | 1418ms | 2549ms | ✗ | - |
| `77.221.151.94:443` | xray | vless | 1697ms | 1650ms | 1713ms | 1667ms | 1484ms | - |
| `88.216.214.159:443` | clash/singbox/xray | vless | 1712ms | 2079ms | 1325ms | 1089ms | 1062ms | - |
| `202.50.253.99:19999` | clash/v2ray | ss | 1722ms | ✗ | 1555ms | 3259ms | ✗ | 0.8Mbps |
| `130.78.30.147:443` | clash/singbox/xray | vless | 1772ms | 1311ms | 1522ms | 1185ms | 1165ms | - |
| `ce5afbt.us14.h1clayd.click:443` | clash/singbox | vless | 1790ms | ✗ | 1906ms | 3572ms | 2442ms | - |
| `45.192.12.92:443` | xray | vless | 1805ms | ✗ | 3070ms | 1360ms | 1718ms | - |
| `193.160.208.240:443` | clash/xray | vless | 1816ms | 1478ms | 1666ms | 711ms | 1144ms | - |
| `80.96.108.29:443` | xray | vless | 1873ms | 1820ms | 1724ms | 765ms | 858ms | - |
| `202.50.253.90:19999` | v2ray/xray | ss | 1922ms | ✗ | 2429ms | 973ms | 2132ms | 0.91Mbps |
| `41.196.0.128:443` | xray | vless | 1942ms | 1814ms | 2339ms | 1755ms | ✗ | - |
| `172.236.233.130:443` | singbox | vless | 1954ms | 2611ms | 2937ms | ✗ | 1416ms | - |
| `196.196.149.22:443` | xray | vless | 1961ms | 2176ms | 2175ms | 2280ms | 2549ms | - |
| … | 共 189 个 | | | | | |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `13.125.215.163:8443`：hello-world-1989/cn-news
> - `139.180.215.25:443`：Areral/ScarletDevil
> - `172.105.212.91:443`：Areral/ScarletDevil
> - `172.238.18.103:443`：Areral/ScarletDevil
> - `139.162.91.250:443`：Areral/ScarletDevil
> - `139.162.125.126:443`：Areral/ScarletDevil
> - `139.162.91.137:443`：Areral/ScarletDevil
> - `139.162.91.249:443`：Areral/ScarletDevil
> - `139.162.91.200:443`：Areral/ScarletDevil
> - `172.104.86.181:443`：Areral/ScarletDevil
> - `172.104.186.205:443`：Areral/ScarletDevil
> - `139.162.101.74:443`：Areral/ScarletDevil
> - `139.162.91.224:443`：Areral/ScarletDevil
> - `172.105.197.24:443`：Areral/ScarletDevil
> - `172.237.14.205:443`：Areral/ScarletDevil
> - `172.104.105.212:443`：Areral/ScarletDevil
> - `172.105.216.21:443`：Areral/ScarletDevil
> - `172.105.203.15:443`：Areral/ScarletDevil
> - `15.188.27.50:443`：rtwo2/FastNodes
> - `139.162.89.151:443`：Areral/ScarletDevil
> - `139.180.221.53:443`：Areral/ScarletDevil
> - `149.28.152.20:443`：Areral/ScarletDevil
> - `13.38.60.238:443`：rtwo2/FastNodes
> - `139.162.91.239:443`：Areral/ScarletDevil
> - `139.162.91.232:443`：Areral/ScarletDevil
> - `88.216.211.36:443`：whoahaow/rjsxrd
> - `15.236.134.147:443`：rtwo2/FastNodes
> - `172.104.48.194:443`：Areral/ScarletDevil
> - `163.245.42.87:443`：0xRadikal/Free-v2ray-Configs
> - `185.79.19.8:443`：snakem982/proxypool
> - `185.231.204.244:443`：0xRadikal/Free-v2ray-Configs
> - `185.79.19.7:443`：0xRadikal/Free-v2ray-Configs
> - `139.162.20.241:443`：Areral/ScarletDevil
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `serv1.fishtohome.ru:443`：0xRadikal/Free-v2ray-Configs
> - `88.216.60.73:443`：whoahaow/rjsxrd
> - `79.182.39.138:443`：Areral/ScarletDevil
> - `84.32.149.211:443`：rekt0ro/ProxyRift
> - `202.50.253.45:19999`：ermaozi01/free_clash_vpn
> - `153.76.204.5:443`：whoahaow/rjsxrd
> - `89.125.175.24:8443`：0xRadikal/Free-v2ray-Configs
> - `88.216.189.20:8443`：snakem982/proxypool
> - `178.130.46.226:443`：0xRadikal/Free-v2ray-Configs
> - `51.75.118.18:20113`：shabane/kamaji
> - `93.183.127.54:2087`：Mehinator/Derafsh
> - `136.148.208.218:443`：0xRadikal/Free-v2ray-Configs
> - `47.85.201.22:443`：snakem982/proxypool
> - `213.171.31.83:443`：Areral/ScarletDevil
> - `172.233.139.212:443`：Areral/ScarletDevil
> - `37.49.225.93:443`：whoahaow/rjsxrd
> - `172.235.37.163:443`：Areral/ScarletDevil
> - `zfapi.zalolink.com:55688`：0xRadikal/Free-v2ray-Configs
> - `176.98.176.60:443`：Areral/ScarletDevil
> - `172.235.50.209:443`：Areral/ScarletDevil
> - `89.23.107.105:443`：rekt0ro/ProxyRift
> - `109.71.245.99:8443`：0xRadikal/Free-v2ray-Configs
> - `172.239.67.142:443`：Areral/ScarletDevil
> - `84.32.248.124:443`：whoahaow/rjsxrd
> - `84.32.108.7:443`：rekt0ro/ProxyRift
> - `vpn.asdfghjuyt.ru:9443`：0xRadikal/Free-v2ray-Configs
> - `172.235.49.52:443`：Areral/ScarletDevil
> - `172.235.36.156:443`：Areral/ScarletDevil
> - `172.233.146.140:443`：Areral/ScarletDevil
> - `104.171.133.209:443`：Areral/ScarletDevil
> - `217.60.27.93:443`：rekt0ro/ProxyRift
> - `23.155.44.105:443`：snakem982/proxypool
> - `31.77.236.131:443`：rekt0ro/ProxyRift
> - `win2loxfde0202.gggrelay.org:54528`：0xRadikal/Free-v2ray-Configs
> - `45.32.70.42:443`：Areral/ScarletDevil
> - `202.50.253.18:19999`：ermaozi01/free_clash_vpn
> - `195.72.62.7:443`：snakem982/proxypool
> - `84.32.149.222:443`：whoahaow/rjsxrd
> - `129.101.100.219:443`：YawStar/Proxy-Hunter
> - `193.233.90.115:8443`：whoahaow/rjsxrd
> - `172.233.157.18:443`：Areral/ScarletDevil
> - `89.106.88.126:443`：0xRadikal/Free-v2ray-Configs
> - `172.235.32.253:443`：Areral/ScarletDevil
> - `72.56.4.84:443`：snakem982/proxypool
> - `188.225.24.62:443`：YawStar/Proxy-Hunter
> - `84.32.54.237:443`：whoahaow/rjsxrd
> - `zfapi.zalolink.com:43149`：ermaozi01/free_clash_vpn
> - `172.235.51.71:443`：Areral/ScarletDevil
> - `89.125.175.55:8443`：0xRadikal/Free-v2ray-Configs
> - `107.191.58.86:443`：sakha1370/OpenRay
> - `172.233.129.172:443`：Areral/ScarletDevil
> - `172.236.241.130:443`：Areral/ScarletDevil
> - `tgfree.rush-server.com:443`：aviamastersgh/vpn-free-russia
> - `ee.point.cookie-line.cc:443`：rekt0ro/ProxyRift
> - `172.235.53.103:443`：Areral/ScarletDevil
> - `48.103.120.3:443`：0xRadikal/Free-v2ray-Configs
> - `77.83.245.22:443`：whoahaow/rjsxrd
> - `138.124.181.197:443`：rekt0ro/ProxyRift
> - `201.51.11.65:443`：rekt0ro/ProxyRift
> - `138.16.206.147:443`：whoahaow/rjsxrd
> - `45.77.8.233:443`：Areral/ScarletDevil
> - `172.236.238.71:443`：Areral/ScarletDevil
> - `84.23.52.104:9071`：whoahaow/rjsxrd
> - `172.235.63.167:443`：Areral/ScarletDevil
> - `45.76.172.197:443`：Areral/ScarletDevil
> - `179.254.127.194:443`：0xRadikal/Free-v2ray-Configs
> - `13.143.239.238:443`：whoahaow/rjsxrd
> - `194.55.167.133:443`：0xRadikal/Free-v2ray-Configs
> - `172.233.142.149:443`：Areral/ScarletDevil
> - `172.236.239.126:443`：Areral/ScarletDevil
> - `89.144.8.91:18888`：MohammadBahemmat/V2ray-Collector
> - `83.141.70.167:443`：HotDrify/drifyconfigs
> - `45.76.106.69:443`：Areral/ScarletDevil
> - `172.233.140.139:443`：Areral/ScarletDevil
> - `77.221.151.94:443`：whoahaow/rjsxrd
> - `88.216.214.159:443`：HotDrify/drifyconfigs
> - `202.50.253.99:19999`：ermaozi01/free_clash_vpn
> - `130.78.30.147:443`：whoahaow/rjsxrd
> - `ce5afbt.us14.h1clayd.click:443`：rekt0ro/ProxyRift
> - `45.192.12.92:443`：whoahaow/rjsxrd
> - `193.160.208.240:443`：0xRadikal/Free-v2ray-Configs
> - `80.96.108.29:443`：0xRadikal/Free-v2ray-Configs
> - `202.50.253.90:19999`：ermaozi01/free_clash_vpn
> - `41.196.0.128:443`：snakem982/proxypool
> - `172.236.233.130:443`：Areral/ScarletDevil
> - `196.196.149.22:443`：Areral/ScarletDevil

## 2026-11-15 23:00

- 可用节点 **86** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `112.49.65.212:18000` | clash/singbox/v2ray | trojan | 223ms | 2044ms | 345ms | 158ms | 263ms | 23.7Mbps |
| `56.10.12.77:8443` | v2ray/xray | ss | 548ms | 490ms | 541ms | 395ms | 641ms | 0.42Mbps |
| `3.71.179.221:443` | clash/singbox/xray | ss | 732ms | 719ms | 771ms | 662ms | 684ms | 4.64Mbps |
| `92.5.55.38:59924` | xray | ss | 746ms | 729ms | 1021ms | 877ms | ✗ | - |
| `3.79.47.19:443` | clash/singbox/xray | ss | 809ms | 704ms | 837ms | 720ms | 780ms | 5.67Mbps |
| `56.10.12.77:443` | xray | vless | 879ms | 845ms | 961ms | 820ms | 919ms | - |
| `213.182.201.138:3090` | clash/v2ray | vless | 929ms | 924ms | 553ms | 430ms | 446ms | 4.63Mbps |
| `202.50.253.81:19999` | v2ray/xray | ss | 1011ms | ✗ | 3661ms | 2418ms | 2788ms | 0.54Mbps |
| `179.254.127.194:443` | xray | vless | 1054ms | ✗ | ✗ | ✗ | ✗ | 0.93Mbps |
| `zfapi.zalolink.com:42120` | clash/xray | vless | 1070ms | 2655ms | 2207ms | 2835ms | 989ms | - |
| `202.50.253.27:19999` | v2ray/xray | ss | 1119ms | ✗ | 1869ms | 2258ms | 1357ms | 0.22Mbps |
| `151.101.36.128:443` | xray | vless | 1125ms | ✗ | 1827ms | 580ms | 615ms | 0.29Mbps |
| `ench-snet-app.w-ctrip.cn:34926` | singbox | trojan | 1173ms | ✗ | ✗ | ✗ | ✗ | 0.06Mbps |
| `213.171.31.83:443` | clash | vless | 1173ms | ✗ | ✗ | 2068ms | ✗ | - |
| `178.17.58.55:443` | v2ray | hysteria2 | 1176ms | ✗ | ✗ | ✗ | ✗ | - |
| `202.50.253.36:19999` | v2ray/xray | ss | 1185ms | ✗ | 1632ms | 989ms | 2791ms | 0.24Mbps |
| `150.241.75.103:443` | xray | vless | 1209ms | 1253ms | 1304ms | 1324ms | 1544ms | 4.23Mbps |
| `202.50.253.90:19999` | xray | ss | 1223ms | ✗ | 1247ms | ✗ | 4011ms | - |
| `timete.hagrid-connected.com:443` | xray | vless | 1350ms | ✗ | ✗ | ✗ | ✗ | 0.02Mbps |
| `157.173.30.95:443` | xray | vless | 1373ms | ✗ | 1132ms | ✗ | ✗ | 1.13Mbps |
| `179.254.127.219:443` | xray | vless | 1381ms | ✗ | ✗ | ✗ | ✗ | 1.2Mbps |
| `202.50.253.18:19999` | v2ray | ss | 1409ms | ✗ | 2928ms | ✗ | ✗ | 0.42Mbps |
| `176.98.176.60:443` | clash | vless | 1451ms | 1774ms | 1780ms | 1468ms | 1406ms | 0.51Mbps |
| `31.76.31.240:4443` | clash/xray | vless | 1464ms | ✗ | 2984ms | 2347ms | 2983ms | 0.13Mbps |
| `201.51.12.98:443` | xray | vless | 1475ms | ✗ | 736ms | 1685ms | ✗ | - |
| `202.50.253.72:19999` | v2ray/xray | ss | 1516ms | ✗ | 1576ms | 2657ms | 1094ms | 0.44Mbps |
| `176.109.101.18:443` | clash/xray | vless | 1520ms | ✗ | ✗ | 4434ms | ✗ | 3.43Mbps |
| `136.148.213.149:443` | xray | vless | 1530ms | 614ms | 746ms | 651ms | 921ms | - |
| `196.196.149.34:443` | clash/xray | vless | 1549ms | ✗ | 2972ms | 2801ms | 3306ms | - |
| `finland.freegate.win:443` | xray | vless | 1559ms | 1511ms | 1969ms | 1518ms | 1483ms | - |
| `fastly2.dunnexa.ir:443` | singbox/v2ray | trojan | 1570ms | ✗ | 1701ms | 1457ms | 1591ms | 0.91Mbps |
| `72.56.4.84:443` | clash | vless | 1573ms | 1531ms | ✗ | ✗ | ✗ | - |
| `zfapi.zalolink.com:46957` | clash | vless | 1631ms | 1911ms | 5270ms | 1330ms | 2628ms | 2.82Mbps |
| `202.50.253.99:19999` | v2ray/xray | ss | 1651ms | ✗ | 1684ms | 2312ms | 2515ms | 0.58Mbps |
| `zfapi.zalolink.com:11802` | clash/xray | vless | 1694ms | 1875ms | ✗ | 1495ms | 1510ms | 1.09Mbps |
| `tgfree.rush-server.com:443` | xray | vless | 1784ms | ✗ | ✗ | ✗ | ✗ | - |
| `151.101.36.2:443` | clash/xray | vless | 1858ms | 3160ms | 1940ms | 2005ms | ✗ | 0.21Mbps |
| `vps3.nemnogogo.com:443` | v2ray/xray | vless | 1938ms | 684ms | 825ms | 678ms | 828ms | - |
| `196.196.208.20:443` | clash | vless | 1943ms | 1847ms | 1881ms | 1625ms | 1721ms | 2.49Mbps |
| `202.50.253.63:19999` | v2ray/xray | ss | 1945ms | ✗ | 1558ms | 2346ms | 1705ms | 0.24Mbps |
| `217.60.27.93:443` | xray | vless | 1957ms | 1443ms | 2870ms | 1792ms | 1922ms | - |
| `172.235.36.156:443` | singbox | vless | 1982ms | ✗ | 1652ms | ✗ | ✗ | 0.06Mbps |
| `riga.freegate.win:443` | xray | vless | 1983ms | 1861ms | 2613ms | 2298ms | 1416ms | - |
| `202.50.253.45:19999` | v2ray/xray | ss | 1993ms | ✗ | 1166ms | 1377ms | 4162ms | 0.47Mbps |
| `202.50.253.54:19999` | v2ray/xray | ss | 2006ms | ✗ | 1984ms | 1075ms | 2349ms | 0.35Mbps |
| `84.54.57.122:443` | xray | vless | 2008ms | ✗ | ✗ | ✗ | ✗ | - |
| `104.171.133.213:443` | clash | vless | 2012ms | 1377ms | 1403ms | 1378ms | 1603ms | 0.64Mbps |
| `83.171.241.182:25155` | xray | vless | 2045ms | 2468ms | 1945ms | 1550ms | 1100ms | - |
| `31.76.114.22:443` | xray | vless | 2083ms | 1767ms | 2243ms | 1877ms | 1497ms | - |
| `172.236.241.130:443` | singbox | vless | 2086ms | ✗ | ✗ | ✗ | ✗ | - |
| `83.171.241.182:443` | clash/singbox/xray | vless | 2094ms | 1948ms | 1985ms | 1943ms | 1887ms | 1.11Mbps |
| `arranged-samuel-cradle-hayes.trycloudflare.com:443` | xray | vmess | 2115ms | ✗ | 2882ms | ✗ | 1951ms | - |
| `zfapi.zalolink.com:30322` | clash | vless | 2177ms | 3919ms | 4106ms | 2538ms | 3155ms | 2.87Mbps |
| `153.56.228.151:443` | clash | vless | 2202ms | 1459ms | 1487ms | 2072ms | 2147ms | 2.67Mbps |
| `185.71.216.95:2091` | clash/singbox | vless | 2230ms | ✗ | ✗ | ✗ | ✗ | 0.41Mbps |
| `196.245.52.188:443` | clash | vless | 2231ms | ✗ | ✗ | ✗ | 3291ms | - |
| `179.254.92.134:443` | clash | vless | 2251ms | 3278ms | ✗ | ✗ | 3224ms | - |
| `d4a338t.pl8.h1clayd.click:443` | clash | vless | 2258ms | 2622ms | ✗ | 1473ms | 1491ms | - |
| `185.71.216.177:2089` | clash/singbox | vless | 2305ms | ✗ | 2491ms | 3396ms | ✗ | 0.6Mbps |
| `147.224.233.249:63690` | clash | vless | 2315ms | 1839ms | 2073ms | 1636ms | 1984ms | - |
| `13.143.232.205:443` | clash/xray | vless | 2356ms | ✗ | ✗ | ✗ | 840ms | - |
| `v1us9.stablenode.cloud:24413` | singbox/v2ray | trojan | 2389ms | 1676ms | 2982ms | 3574ms | 1415ms | 1.36Mbps |
| `base.hosamobenl.co.uk:443` | xray | vless | 2413ms | ✗ | 1445ms | ✗ | 3016ms | - |
| `46.243.233.165:59715` | v2ray | vless | 2448ms | 1693ms | 1075ms | 1137ms | 1255ms | 0.37Mbps |
| `185.71.216.177:2194` | clash/xray | vless | 2537ms | ✗ | 3474ms | 4577ms | ✗ | - |
| `us032014.ssgreen.org:443` | xray | vmess | 2568ms | ✗ | ✗ | ✗ | ✗ | - |
| `34.55.45.96:443` | clash/xray | vless | 2622ms | 3258ms | 1726ms | 1194ms | 967ms | 0.1Mbps |
| `v1us9.stablenode.cloud:24421` | singbox/v2ray | trojan | 2693ms | 2047ms | 2890ms | 1678ms | 1719ms | 0.57Mbps |
| `167.17.179.175:443` | singbox/v2ray/xray | hysteria2 | 2710ms | 1408ms | 1093ms | 643ms | 646ms | 1.14Mbps |
| `130.78.31.25:443` | xray | vless | 2747ms | ✗ | ✗ | 2722ms | ✗ | - |
| `185.71.216.94:2090` | clash | vless | 2807ms | ✗ | ✗ | ✗ | ✗ | - |
| `213.108.23.226:46312` | xray | vless | 2823ms | 1331ms | 3409ms | 1392ms | 1607ms | - |
| `f3b21at.de18.h1clayd.click:443` | clash | vless | 2943ms | 2401ms | 2591ms | 2334ms | 1148ms | - |
| `zfapi.zalolink.com:43149` | xray | vless | 2986ms | ✗ | 1090ms | 1005ms | 999ms | - |
| `172.233.129.172:443` | singbox | vless | 3072ms | ✗ | 2113ms | ✗ | ✗ | 0.08Mbps |
| `185.71.216.95:2093` | singbox | vless | 3184ms | ✗ | ✗ | ✗ | 3061ms | 0.07Mbps |
| `151.101.36.246:443` | xray | vless | 3411ms | 1973ms | 3105ms | 728ms | 2621ms | - |
| `201.24.116.192:443` | v2ray/xray | vless | 3456ms | 1158ms | 874ms | 692ms | 1125ms | - |
| `13.140.86.73:6079` | clash/xray | ss | 3643ms | 4991ms | ✗ | ✗ | 4855ms | - |
| `196.240.181.132:443` | xray | vless | 3669ms | ✗ | 2301ms | ✗ | ✗ | - |
| `185.71.216.177:2093` | clash/singbox | vless | 3742ms | 3123ms | 2075ms | ✗ | 4303ms | 1.2Mbps |
| `s5.abol.ahbpanel.ir:80` | xray | ss | 3785ms | ✗ | ✗ | ✗ | ✗ | - |
| `196.196.149.80:443` | clash | vless | 4139ms | ✗ | ✗ | ✗ | ✗ | - |
| `185.71.216.94:2194` | clash | vless | 4566ms | ✗ | ✗ | ✗ | ✗ | - |
| `v1us9.stablenode.cloud:24422` | clash/singbox/v2ray | trojan | 4764ms | 1412ms | 2629ms | 1355ms | 2989ms | 0.38Mbps |
| `185.71.216.95:2092` | clash | vless | 4863ms | ✗ | ✗ | ✗ | ✗ | - |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `112.49.65.212:18000`：rtwo2/FastNodes
> - `56.10.12.77:8443`：hello-world-1989/cn-news
> - `3.71.179.221:443`：rekt0ro/ProxyRift
> - `92.5.55.38:59924`：rekt0ro/ProxyRift
> - `3.79.47.19:443`：rekt0ro/ProxyRift
> - `56.10.12.77:443`：hello-world-1989/cn-news
> - `213.182.201.138:3090`：0xRadikal/Free-v2ray-Configs
> - `202.50.253.81:19999`：ermaozi01/free_clash_vpn
> - `179.254.127.194:443`：rekt0ro/ProxyRift
> - `zfapi.zalolink.com:42120`：ishalumi/proxy-node-collector
> - `202.50.253.27:19999`：ermaozi01/free_clash_vpn
> - `151.101.36.128:443`：rekt0ro/ProxyRift
> - `ench-snet-app.w-ctrip.cn:34926`：rekt0ro/ProxyRift
> - `213.171.31.83:443`：rekt0ro/ProxyRift
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `202.50.253.36:19999`：ermaozi01/free_clash_vpn
> - `150.241.75.103:443`：rekt0ro/ProxyRift
> - `202.50.253.90:19999`：ermaozi01/free_clash_vpn
> - `timete.hagrid-connected.com:443`：0xRadikal/Free-v2ray-Configs
> - `157.173.30.95:443`：rekt0ro/ProxyRift
> - `179.254.127.219:443`：whoahaow/rjsxrd
> - `202.50.253.18:19999`：F0rc3Run/F0rc3Run
> - `176.98.176.60:443`：0xRadikal/Free-v2ray-Configs
> - `31.76.31.240:4443`：rekt0ro/ProxyRift
> - `201.51.12.98:443`：zhuhaiuk/free-nodes
> - `202.50.253.72:19999`：ermaozi01/free_clash_vpn
> - `176.109.101.18:443`：whoahaow/rjsxrd
> - `136.148.213.149:443`：Areral/ScarletDevil
> - `196.196.149.34:443`：rekt0ro/ProxyRift
> - `finland.freegate.win:443`：rekt0ro/ProxyRift
> - `fastly2.dunnexa.ir:443`：HamoonSoleimani/Pr0xySh4rk
> - `72.56.4.84:443`：YawStar/Proxy-Hunter
> - `zfapi.zalolink.com:46957`：Areral/ScarletDevil
> - `202.50.253.99:19999`：ermaozi01/free_clash_vpn
> - `zfapi.zalolink.com:11802`：YawStar/Proxy-Hunter
> - `tgfree.rush-server.com:443`：R3ZARAHIMI/tg-v2ray-configs-every2h
> - `151.101.36.2:443`：Mehinator/Derafsh
> - `vps3.nemnogogo.com:443`：zhuhaiuk/free-nodes
> - `196.196.208.20:443`：rekt0ro/ProxyRift
> - `202.50.253.63:19999`：ermaozi01/free_clash_vpn
> - `217.60.27.93:443`：Mehinator/Derafsh
> - `172.235.36.156:443`：Areral/ScarletDevil
> - `riga.freegate.win:443`：rekt0ro/ProxyRift
> - `202.50.253.45:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.54:19999`：ermaozi01/free_clash_vpn
> - `84.54.57.122:443`：rekt0ro/ProxyRift
> - `104.171.133.213:443`：0xRadikal/Free-v2ray-Configs
> - `83.171.241.182:25155`：rekt0ro/ProxyRift
> - `31.76.114.22:443`：ishalumi/proxy-node-collector
> - `172.236.241.130:443`：Areral/ScarletDevil
> - `83.171.241.182:443`：whoahaow/rjsxrd
> - `arranged-samuel-cradle-hayes.trycloudflare.com:443`：sakha1370/OpenRay
> - `zfapi.zalolink.com:30322`：YawStar/Proxy-Hunter
> - `153.56.228.151:443`：0xRadikal/Free-v2ray-Configs
> - `185.71.216.95:2091`：rekt0ro/ProxyRift
> - `196.245.52.188:443`：snakem982/proxypool
> - `179.254.92.134:443`：YawStar/Proxy-Hunter
> - `d4a338t.pl8.h1clayd.click:443`：rekt0ro/ProxyRift
> - `185.71.216.177:2089`：rekt0ro/ProxyRift
> - `147.224.233.249:63690`：rekt0ro/ProxyRift
> - `13.143.232.205:443`：rekt0ro/ProxyRift
> - `v1us9.stablenode.cloud:24413`：VoroninaYanina/free-nodes
> - `base.hosamobenl.co.uk:443`：zhuhaiuk/free-nodes
> - `46.243.233.165:59715`：whoahaow/rjsxrd
> - `185.71.216.177:2194`：rekt0ro/ProxyRift
> - `us032014.ssgreen.org:443`：rekt0ro/ProxyRift
> - `34.55.45.96:443`：rekt0ro/ProxyRift
> - `v1us9.stablenode.cloud:24421`：VoroninaYanina/free-nodes
> - `167.17.179.175:443`：rekt0ro/ProxyRift
> - `130.78.31.25:443`：rekt0ro/ProxyRift
> - `185.71.216.94:2090`：rekt0ro/ProxyRift
> - `213.108.23.226:46312`：rekt0ro/ProxyRift
> - `f3b21at.de18.h1clayd.click:443`：Areral/ScarletDevil
> - `zfapi.zalolink.com:43149`：ermaozi01/free_clash_vpn
> - `172.233.129.172:443`：Areral/ScarletDevil
> - `185.71.216.95:2093`：rekt0ro/ProxyRift
> - `151.101.36.246:443`：rekt0ro/ProxyRift
> - `201.24.116.192:443`：zhuhaiuk/free-nodes
> - `13.140.86.73:6079`：snakem982/proxypool
> - `196.240.181.132:443`：rekt0ro/ProxyRift
> - `185.71.216.177:2093`：rekt0ro/ProxyRift
> - `s5.abol.ahbpanel.ir:80`：F0rc3Run/F0rc3Run
> - `196.196.149.80:443`：YawStar/Proxy-Hunter
> - `185.71.216.94:2194`：rekt0ro/ProxyRift
> - `v1us9.stablenode.cloud:24422`：VoroninaYanina/free-nodes
> - `185.71.216.95:2092`：rekt0ro/ProxyRift

## 2026-11-14 22:50

- 可用节点 **31** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `112.49.65.212:18000` | clash/singbox/v2ray | trojan | 316ms | 311ms | 339ms | 167ms | 213ms | 29.24Mbps |
| `163.61.182.194:34646` | clash | vless | 695ms | 1492ms | 877ms | 747ms | 749ms | 4.47Mbps |
| `edge.bookmai.com:443` | clash | vless | 922ms | ✗ | ✗ | 995ms | ✗ | 4.88Mbps |
| `47.129.144.40:8443` | singbox/v2ray/xray | ss | 1009ms | 535ms | 793ms | 867ms | 1163ms | 0.18Mbps |
| `202.50.253.54:19999` | singbox/v2ray/xray | ss | 1013ms | ✗ | 1074ms | 1001ms | 1665ms | 0.37Mbps |
| `202.50.253.63:19999` | singbox/v2ray | ss | 1016ms | ✗ | 2894ms | 2113ms | 1436ms | 0.31Mbps |
| `yyy.ahbpanel.ir:1081` | v2ray | ss | 1076ms | 1185ms | 1431ms | 811ms | 870ms | - |
| `178.17.58.55:443` | v2ray | hysteria2 | 1215ms | ✗ | ✗ | ✗ | ✗ | - |
| `hkg1.angelsleep9.com:443` | xray | vless | 1326ms | ✗ | ✗ | ✗ | 1299ms | 2.77Mbps |
| `fi4.h1cloud.net:25749` | clash | vless | 1549ms | 1262ms | 1119ms | 1285ms | 1310ms | 3.36Mbps |
| `194.58.60.221:443` | singbox | vless | 1620ms | 879ms | 1857ms | 2002ms | 854ms | 0.5Mbps |
| `ec7a81g.de15.h1clayd.click:443` | clash | vless | 1682ms | 2943ms | ✗ | ✗ | ✗ | 1.7Mbps |
| `204.11.2.93:443` | v2ray | vless | 1779ms | ✗ | ✗ | ✗ | ✗ | 0.29Mbps |
| `202.50.253.99:19999` | singbox/v2ray/xray | ss | 1892ms | 1019ms | 1967ms | 2042ms | 2235ms | 0.31Mbps |
| `202.50.253.90:19999` | singbox/v2ray/xray | ss | 2043ms | ✗ | 2704ms | 1992ms | 1457ms | 0.41Mbps |
| `81.90.17.166:443` | v2ray | hysteria2 | 2047ms | ✗ | 1153ms | 650ms | 678ms | 1.6Mbps |
| `b6d267t.es10.h1clayd.shop:443` | clash/singbox/xray | vless | 2166ms | 2727ms | 1637ms | 1114ms | 1126ms | 1.77Mbps |
| `177.1.187.155:443` | v2ray | vless | 2208ms | ✗ | 1759ms | ✗ | ✗ | 0.38Mbps |
| `87.120.252.67:443` | clash | vless | 2263ms | 1263ms | ✗ | 2907ms | 1761ms | 0.05Mbps |
| `202.50.253.72:19999` | singbox/v2ray/xray | ss | 2266ms | ✗ | 2886ms | 2760ms | 2852ms | 1.03Mbps |
| `g4.staticedge.cfd:443` | clash | vless | 2346ms | 2095ms | 1991ms | 1810ms | 1734ms | - |
| `check-host.net:2053` | clash | vless | 2376ms | ✗ | ✗ | 2902ms | ✗ | - |
| `rma7.rmaaccshop.ir:12146` | xray | vmess | 2446ms | 2607ms | ✗ | 3358ms | ✗ | - |
| `f0f0bet.fi2.h1clayd.click:443` | singbox | vless | 2555ms | ✗ | ✗ | ✗ | ✗ | 1.43Mbps |
| `fremont.freegate.win:443` | xray | vless | 2587ms | ✗ | ✗ | 1959ms | ✗ | 0.38Mbps |
| `130.49.163.188:443` | clash/v2ray | hysteria2 | 2618ms | 1529ms | 2036ms | 1570ms | 1974ms | 1.1Mbps |
| `a813d5t.ch5.h1clayd.click:443` | clash | vless | 2670ms | 1420ms | 2551ms | 1335ms | 1081ms | 1.86Mbps |
| `47.129.144.40:443` | clash | vless | 2801ms | 1228ms | 1707ms | 2116ms | 1120ms | 0.14Mbps |
| `202.50.253.18:19999` | singbox/xray | ss | 2938ms | ✗ | ✗ | 3757ms | 1084ms | 0.51Mbps |
| `202.50.253.81:19999` | v2ray/xray | ss | 3231ms | ✗ | 2555ms | 1370ms | 4016ms | 0.09Mbps |
| `202.50.253.36:19999` | singbox/v2ray | ss | 3303ms | 1161ms | 3557ms | 2217ms | 1075ms | 0.22Mbps |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `112.49.65.212:18000`：rtwo2/FastNodes
> - `163.61.182.194:34646`：rtwo2/FastNodes
> - `edge.bookmai.com:443`：aviamastersgh/vpn-free-russia
> - `47.129.144.40:8443`：hello-world-1989/cn-news
> - `202.50.253.54:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.63:19999`：ermaozi01/free_clash_vpn
> - `yyy.ahbpanel.ir:1081`：MohammadBahemmat/V2ray-Collector
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `hkg1.angelsleep9.com:443`：whoahaow/rjsxrd
> - `fi4.h1cloud.net:25749`：rekt0ro/ProxyRift
> - `194.58.60.221:443`：Areral/ScarletDevil
> - `ec7a81g.de15.h1clayd.click:443`：Areral/ScarletDevil
> - `204.11.2.93:443`：rekt0ro/ProxyRift
> - `202.50.253.99:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.90:19999`：ermaozi01/free_clash_vpn
> - `81.90.17.166:443`：Areral/ScarletDevil
> - `b6d267t.es10.h1clayd.shop:443`：rekt0ro/ProxyRift
> - `177.1.187.155:443`：rekt0ro/ProxyRift
> - `87.120.252.67:443`：rekt0ro/ProxyRift
> - `202.50.253.72:19999`：ermaozi01/free_clash_vpn
> - `g4.staticedge.cfd:443`：Areral/ScarletDevil
> - `check-host.net:2053`：R3ZARAHIMI/tg-v2ray-configs-every2h
> - `rma7.rmaaccshop.ir:12146`：rekt0ro/ProxyRift
> - `f0f0bet.fi2.h1clayd.click:443`：Areral/ScarletDevil
> - `fremont.freegate.win:443`：rekt0ro/ProxyRift
> - `130.49.163.188:443`：Areral/ScarletDevil
> - `a813d5t.ch5.h1clayd.click:443`：rekt0ro/ProxyRift
> - `47.129.144.40:443`：hello-world-1989/cn-news
> - `202.50.253.18:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.81:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.36:19999`：ermaozi01/free_clash_vpn

## 2026-11-13 22:47

- 可用节点 **74** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：2MB 串行下载，每内核最多 20 个

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube | 带宽 |
|---|---|---|---|---|---|---|---|---|
| `13.231.100.94:2377` | clash | ss | 334ms | ✗ | 626ms | 401ms | 1805ms | - |
| `3.39.252.190:443` | clash/singbox/xray | vless | 659ms | 556ms | 586ms | 574ms | 598ms | - |
| `27septgerm.site:444` | clash/singbox/xray | vless | 951ms | 913ms | 1234ms | 1346ms | 1126ms | - |
| `84.32.23.119:443` | clash/singbox/xray | vless | 985ms | 367ms | 1159ms | 1401ms | 1263ms | - |
| `18.175.123.65:443` | clash/singbox/xray | ss | 1008ms | 2049ms | 1406ms | 1300ms | 1965ms | - |
| `94.183.164.96:8443` | xray | vless | 1051ms | 967ms | 1194ms | 1094ms | 986ms | - |
| `edge.bookmai.com:443` | clash/singbox/xray | vless | 1056ms | ✗ | ✗ | 1114ms | ✗ | - |
| `178.17.58.55:443` | v2ray | hysteria2 | 1086ms | ✗ | ✗ | ✗ | ✗ | - |
| `202.50.253.27:19999` | singbox/v2ray/xray | ss | 1112ms | ✗ | 4354ms | 2478ms | 1381ms | - |
| `202.50.253.63:19999` | clash/singbox/v2ray/xray | ss | 1134ms | ✗ | 2547ms | 5050ms | 1138ms | - |
| `94.183.164.96:443` | xray | vless | 1148ms | 1057ms | 2423ms | 546ms | 584ms | - |
| `172.235.36.156:443` | singbox | vless | 1159ms | 1505ms | ✗ | 2188ms | 2409ms | - |
| `202.50.253.36:19999` | clash/singbox/v2ray/xray | ss | 1162ms | 1035ms | 2441ms | 1050ms | 2259ms | - |
| `84.32.217.164:443` | clash/singbox | vless | 1164ms | 1270ms | 1179ms | 1399ms | 1230ms | - |
| `185.42.214.39:23243` | singbox | vless | 1187ms | 1126ms | ✗ | 1192ms | ✗ | - |
| `143.246.204.21:443` | xray | vless | 1188ms | 1380ms | 1678ms | 675ms | 773ms | - |
| `104.171.133.209:443` | xray | vless | 1192ms | ✗ | ✗ | ✗ | ✗ | - |
| `172.233.129.172:443` | singbox | vless | 1265ms | 2267ms | 2816ms | 2345ms | 1127ms | - |
| `217.199.253.177:443` | clash/singbox/xray | vless | 1321ms | 3627ms | 2392ms | 1429ms | 1163ms | - |
| `217.156.123.33:443` | clash/singbox/xray | vless | 1335ms | 817ms | 957ms | 532ms | 1353ms | - |
| `18.199.171.99:443` | singbox/xray | ss | 1355ms | ✗ | 1392ms | 1235ms | 1241ms | - |
| `us-05.avroraservice.online:8443` | xray | vless | 1373ms | 1496ms | 1205ms | 836ms | 883ms | - |
| `us032023.ssgreen.org:443` | xray | vmess | 1379ms | ✗ | 1095ms | ✗ | 1382ms | - |
| `202.50.253.99:19999` | clash/singbox/v2ray | ss | 1430ms | ✗ | 3688ms | 3136ms | 1039ms | - |
| `5.149.250.41:443` | clash/singbox/xray | vless | 1449ms | 509ms | 691ms | 515ms | 580ms | - |
| `162.55.242.208:2096` | xray | vless | 1467ms | 1354ms | 1345ms | 2993ms | 1610ms | - |
| `194.180.207.154:443` | singbox | vless | 1476ms | 694ms | 984ms | 726ms | 628ms | - |
| `80.96.108.29:8443` | xray | vless | 1492ms | 1394ms | 1422ms | 697ms | 697ms | - |
| `202.50.253.54:19999` | clash/singbox/v2ray | ss | 1506ms | ✗ | 2912ms | 966ms | 2393ms | - |
| `104.233.9.100:443` | xray | vless | 1556ms | 593ms | 681ms | 537ms | 653ms | - |
| `13.143.137.98:443` | xray | vless | 1589ms | 2980ms | 3414ms | 3676ms | 878ms | - |
| `201.34.142.108:443` | xray | vless | 1631ms | 1333ms | 1691ms | 1670ms | 720ms | - |
| `7fb7d2t.de31.h1clayd.shop:443` | singbox | vless | 1695ms | 1080ms | 1201ms | 1028ms | 965ms | - |
| `94.139.250.226:443` | clash/singbox/xray | vless | 1697ms | 963ms | 830ms | 681ms | 1086ms | - |
| `vps3.nemnogogo.com:443` | clash/singbox/v2ray/xray | vless | 1745ms | 990ms | 1151ms | 655ms | 1071ms | - |
| `45.63.53.81:443` | singbox | vless | 1756ms | 2563ms | 1382ms | ✗ | 2126ms | - |
| `89.150.45.246:443` | clash/singbox/xray | vless | 1762ms | 653ms | 802ms | 744ms | 743ms | - |
| `202.50.253.18:19999` | clash/singbox/v2ray | ss | 1808ms | 1037ms | 3218ms | 2917ms | 2435ms | - |
| `206.245.153.57:8443` | clash/singbox | hysteria2 | 1814ms | 1825ms | 713ms | 1283ms | 920ms | - |
| `153.56.229.207:443` | xray | vless | 1820ms | 1366ms | 1319ms | 1386ms | 1090ms | - |
| `200.165.236.84:443` | xray | vless | 1877ms | 986ms | 881ms | 1875ms | 1759ms | - |
| `202.50.253.45:19999` | clash/singbox/v2ray/xray | ss | 1911ms | ✗ | 3927ms | 2592ms | 2206ms | - |
| `196.245.52.183:443` | clash/singbox | vless | 2005ms | 2304ms | 3765ms | 2159ms | 2047ms | - |
| `206.53.48.69:443` | clash/singbox/xray | vless | 2008ms | 1404ms | 1167ms | 1090ms | 976ms | - |
| `199.68.156.221:2087` | clash/v2ray/xray | trojan | 2049ms | 3098ms | 1588ms | 1301ms | 2926ms | - |
| `hedgerow.moltex.click:443` | xray | vless | 2080ms | ✗ | 1926ms | 3053ms | ✗ | - |
| `87.121.89.160:8443` | xray | vless | 2096ms | 1635ms | 3894ms | 1526ms | 1343ms | - |
| `forumdrun.xubi.org:443` | xray | vless | 2106ms | 1978ms | 2315ms | 1181ms | 1738ms | - |
| `birchwood.moltex.click:443` | xray | vless | 2293ms | 2173ms | 2782ms | 2016ms | 2677ms | - |
| `201.24.116.192:443` | clash/singbox/v2ray/xray | vless | 2321ms | 813ms | 951ms | 738ms | 1016ms | - |
| `9.247.174.134:8443` | clash/singbox/xray | vless | 2323ms | 2295ms | 1342ms | 1156ms | 1364ms | - |
| `144.31.158.109:443` | xray | vless | 2350ms | ✗ | 3576ms | ✗ | 1893ms | - |
| `nexianetwork.anymor.org:8686` | xray | vless | 2364ms | 1165ms | 1525ms | ✗ | 3244ms | - |
| `202.50.253.81:19999` | clash/singbox/v2ray/xray | ss | 2452ms | 2666ms | 1492ms | 1413ms | 1373ms | - |
| `83.141.69.220:443` | xray | vless | 2519ms | 1872ms | 1625ms | 1604ms | 1647ms | - |
| `hk1t.wawojk.dpdns.org:443` | v2ray/xray | vless | 2579ms | 2232ms | 3317ms | 2851ms | 3098ms | - |
| `172.235.51.71:443` | singbox | vless | 2581ms | 1185ms | 1185ms | 2331ms | 1466ms | - |
| `5b1b23x.pl5.h1clayd.click:443` | clash/xray | vless | 2656ms | ✗ | 3703ms | 907ms | 972ms | - |
| `95.167.57.129:8445` | xray | vless | 2743ms | ✗ | ✗ | ✗ | ✗ | - |
| `201.8.80.82:443` | xray | vless | 2814ms | ✗ | ✗ | ✗ | 1249ms | - |
| `94.156.114.170:444` | xray | vless | 2863ms | 3078ms | 1202ms | ✗ | 1009ms | - |
| `v1us9.stablenode.cloud:24413` | clash | trojan | 2889ms | 1343ms | 1354ms | 1609ms | 1832ms | - |
| `202.50.253.90:19999` | clash/singbox/v2ray/xray | ss | 2909ms | ✗ | 1475ms | 2773ms | 3366ms | - |
| `172.236.241.130:443` | singbox | vless | 2949ms | 1833ms | 3169ms | 2513ms | 2881ms | - |
| `v1us9.stablenode.cloud:24421` | clash/singbox | trojan | 3078ms | ✗ | 2598ms | 2712ms | 2827ms | - |
| `179.254.169.116:8443` | xray | vless | 3093ms | ✗ | ✗ | ✗ | ✗ | - |
| `grove.moltex.click:443` | xray | vless | 3170ms | 2923ms | 1913ms | ✗ | 1816ms | - |
| `5.59.205.56:8455` | xray | vless | 3187ms | ✗ | 1800ms | ✗ | 1588ms | - |
| `luminexorizon.ink:443` | v2ray | vless | 3229ms | 1733ms | 2533ms | 1819ms | 2160ms | - |
| `v1us9.stablenode.cloud:24422` | v2ray | trojan | 3283ms | 3120ms | ✗ | 3527ms | 2933ms | - |
| `202.50.253.72:19999` | clash/singbox/v2ray/xray | ss | 3620ms | ✗ | 1526ms | 2534ms | 1351ms | - |
| `ws3.falmero.store:443` | clash/xray | vless | 3648ms | 2806ms | 3098ms | 1860ms | 2150ms | - |
| `193.228.128.230:443` | xray | vless | 3959ms | 2735ms | ✗ | ✗ | ✗ | - |
| `79.141.166.66:443` | singbox/xray | vless | 3974ms | 1389ms | 1347ms | 1815ms | 1153ms | - |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `13.231.100.94:2377`：bzfq21/proxy-singbox
> - `3.39.252.190:443`：hello-world-1989/cn-news
> - `27septgerm.site:444`：Areral/ScarletDevil
> - `84.32.23.119:443`：10Dream/sub-mod
> - `18.175.123.65:443`：MohammadBahemmat/V2ray-Collector
> - `94.183.164.96:8443`：whoahaow/rjsxrd
> - `edge.bookmai.com:443`：aviamastersgh/vpn-free-russia
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `202.50.253.27:19999`：ermaozi01/free_clash_vpn
> - `202.50.253.63:19999`：ermaozi01/free_clash_vpn
> - `94.183.164.96:443`：rekt0ro/ProxyRift
> - `172.235.36.156:443`：Areral/ScarletDevil
> - `202.50.253.36:19999`：ermaozi01/free_clash_vpn
> - `84.32.217.164:443`：FLAT447/v2ray-lists
> - `185.42.214.39:23243`：MohammadBahemmat/V2ray-Collector
> - `143.246.204.21:443`：aviamastersgh/vpn-free-russia
> - `104.171.133.209:443`：aviamastersgh/vpn-free-russia
> - `172.233.129.172:443`：Areral/ScarletDevil
> - `217.199.253.177:443`：Areral/ScarletDevil
> - `217.156.123.33:443`：Areral/ScarletDevil
> - `18.199.171.99:443`：MohammadBahemmat/V2ray-Collector
> - `us-05.avroraservice.online:8443`：FLAT447/v2ray-lists
> - `us032023.ssgreen.org:443`：rekt0ro/ProxyRift
> - `202.50.253.99:19999`：ermaozi01/free_clash_vpn
> - `5.149.250.41:443`：FLAT447/v2ray-lists
> - `162.55.242.208:2096`：0xRadikal/Free-v2ray-Configs
> - `194.180.207.154:443`：Areral/ScarletDevil
> - `80.96.108.29:8443`：aviamastersgh/vpn-free-russia
> - `202.50.253.54:19999`：ermaozi01/free_clash_vpn
> - `104.233.9.100:443`：rekt0ro/ProxyRift
> - `13.143.137.98:443`：VOID-Anonymity/V.O.I.D-VPN_Bypass
> - `201.34.142.108:443`：aviamastersgh/vpn-free-russia
> - `7fb7d2t.de31.h1clayd.shop:443`：Areral/ScarletDevil
> - `94.139.250.226:443`：FLAT447/v2ray-lists
> - `vps3.nemnogogo.com:443`：zhuhaiuk/free-nodes
> - `45.63.53.81:443`：LeilaoMi/AutoMergePublicNodes-Optimized
> - `89.150.45.246:443`：Areral/ScarletDevil
> - `202.50.253.18:19999`：F0rc3Run/F0rc3Run
> - `206.245.153.57:8443`：Areral/ScarletDevil
> - `153.56.229.207:443`：whoahaow/rjsxrd
> - `200.165.236.84:443`：rekt0ro/ProxyRift
> - `202.50.253.45:19999`：ermaozi01/free_clash_vpn
> - `196.245.52.183:443`：Areral/ScarletDevil
> - `206.53.48.69:443`：FLAT447/v2ray-lists
> - `199.68.156.221:2087`：Mehinator/Derafsh
> - `hedgerow.moltex.click:443`：rekt0ro/ProxyRift
> - `87.121.89.160:8443`：rekt0ro/ProxyRift
> - `forumdrun.xubi.org:443`：0xRadikal/Free-v2ray-Configs
> - `birchwood.moltex.click:443`：rekt0ro/ProxyRift
> - `201.24.116.192:443`：zhuhaiuk/free-nodes
> - `9.247.174.134:8443`：zhuhaiuk/free-nodes
> - `144.31.158.109:443`：rekt0ro/ProxyRift
> - `nexianetwork.anymor.org:8686`：rekt0ro/ProxyRift
> - `202.50.253.81:19999`：ermaozi01/free_clash_vpn
> - `83.141.69.220:443`：rekt0ro/ProxyRift
> - `hk1t.wawojk.dpdns.org:443`：bzfq21/proxy-singbox
> - `172.235.51.71:443`：Areral/ScarletDevil
> - `5b1b23x.pl5.h1clayd.click:443`：FLAT447/v2ray-lists
> - `95.167.57.129:8445`：AmazingCoderA/PypsCFG
> - `201.8.80.82:443`：Areral/ScarletDevil
> - `94.156.114.170:444`：whoahaow/rjsxrd
> - `v1us9.stablenode.cloud:24413`：crashgfw/free-airport-nodes
> - `202.50.253.90:19999`：ermaozi01/free_clash_vpn
> - `172.236.241.130:443`：Areral/ScarletDevil
> - `v1us9.stablenode.cloud:24421`：crashgfw/free-airport-nodes
> - `179.254.169.116:8443`：FLAT447/v2ray-lists
> - `grove.moltex.click:443`：Areral/ScarletDevil
> - `5.59.205.56:8455`：rekt0ro/ProxyRift
> - `luminexorizon.ink:443`：aviamastersgh/vpn-free-russia
> - `v1us9.stablenode.cloud:24422`：crashgfw/free-airport-nodes
> - `202.50.253.72:19999`：ermaozi01/free_clash_vpn
> - `ws3.falmero.store:443`：Areral/ScarletDevil
> - `193.228.128.230:443`：FLAT447/v2ray-lists
> - `79.141.166.66:443`：Areral/ScarletDevil
