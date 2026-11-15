# 可用节点总表（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

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
