# 可用节点总表（时间倒序）

> 按日期倒序累积；同一天重跑会替换当天小节

## 2026-11-13 10:40

- 可用节点 **29** 个（按主目标延迟升序；同一服务器在多个内核可用时合并成一行）
- 延迟测试目标：primary、github、x、cloudflare、youtube（主判据 `primary`）
- 带宽：本轮未测（--no-bw）

| 节点 | 内核 | 协议 | 主目标 | github | x | cloudflare | youtube |
|---|---|---|---|---|---|---|---|
| `212.69.135.225:8443` | xray | vless | 899ms | 1254ms | 1029ms | 889ms | 1010ms |
| `104.26.6.171:443` | xray | trojan | 916ms | 912ms | 978ms | ✗ | 985ms |
| `5.104.74.50:8443` | xray | vless | 1106ms | 1241ms | 970ms | 1026ms | 929ms |
| `18.171.57.116:443` | singbox/xray | ss | 1204ms | 967ms | 1384ms | 914ms | 1980ms |
| `k9-85j.pages.dev:443` | clash/v2ray/xray | vless | 1232ms | 1063ms | 1578ms | 1210ms | 1037ms |
| `spacex.com:443` | xray | vless | 1439ms | ✗ | ✗ | ✗ | ✗ |
| `kclx.eu.org:443` | singbox | vless | 1456ms | ✗ | ✗ | ✗ | ✗ |
| `14f7f5f0.mrbl69black.pages.dev:443` | xray | vless | 1513ms | ✗ | ✗ | ✗ | ✗ |
| `vless3.gem-audio2.us.ci:443` | singbox | vless | 1528ms | ✗ | ✗ | ✗ | ✗ |
| `lanzerotte1312.live:443` | clash/xray | vless | 1540ms | 1510ms | 1125ms | 1414ms | 1190ms |
| `1fd53cx.se5.h1clayd.shop:443` | clash/xray | vless | 1597ms | 1495ms | 1437ms | 642ms | 576ms |
| `proxy-34l.pages.dev:2087` | clash | vless | 1750ms | ✗ | ✗ | ✗ | 969ms |
| `104.18.35.86:2096` | clash | trojan | 1784ms | ✗ | ✗ | ✗ | ✗ |
| `62.60.219.235:443` | xray | vless | 1844ms | 1697ms | 1786ms | 810ms | 873ms |
| `157.22.190.220:2053` | clash/singbox/xray | vless | 1902ms | 1827ms | 2040ms | 1748ms | 1738ms |
| `c3b4ce4b957a.vps.myjino.ru:53898` | xray | vless | 2046ms | 1343ms | 1918ms | 1569ms | 1347ms |
| `wells.aisb.dpdns.org:443` | clash/singbox/v2ray/xray | vless | 2184ms | 2325ms | 2064ms | 2023ms | 1997ms |
| `pl3.fox-lisa.ru:443` | xray | vless | 2260ms | 1453ms | 1721ms | 3307ms | 2337ms |
| `lt.t1n2.com:443` | clash/xray | vless | 2284ms | 1112ms | 1275ms | 1213ms | 1105ms |
| `100gramm.pro:443` | xray | vless | 2408ms | 1677ms | 1859ms | 1571ms | 1507ms |
| `yd.2.hhhhh.eu.org:443` | clash | vless | 2601ms | ✗ | ✗ | ✗ | 2830ms |
| `52.77.214.112:8443` | v2ray | ss | ✗ | ✗ | ✗ | ✗ | ✗ |
| `3.34.49.234:8443` | v2ray/xray | ss | ✗ | ✗ | ✗ | ✗ | ✗ |
| `139.224.244.8:49534` | clash/singbox/v2ray/xray | vmess | ✗ | ✗ | ✗ | ✗ | ✗ |
| `178.17.58.55:443` | v2ray/xray | hysteria2 | ✗ | ✗ | ✗ | ✗ | ✗ |
| `de-tg.fastlanehosting.ru:443` | clash/v2ray/xray | hysteria2 | ✗ | ✗ | ✗ | ✗ | ✗ |
| `82.29.36.252:443` | xray | vless | ✗ | ✗ | ✗ | ✗ | ✗ |
| `45.192.203.44:10727` | xray | vless | ✗ | ✗ | ✗ | ✗ | ✗ |
| `52.77.214.112:443` | clash | vless | ✗ | ✗ | ✗ | ✗ | ✗ |

> 来源仓库（可多个，去重时按 1/N 分摊产量）：
> - `212.69.135.225:8443`：Maskkost93/kizyak-vpn-4.0
> - `104.26.6.171:443`：hamedcode/port-based-v2ray-configs
> - `5.104.74.50:8443`：Maskkost93/kizyak-vpn-4.0
> - `18.171.57.116:443`：miladtahanian/Config-Collector
> - `k9-85j.pages.dev:443`：igareck/vpn-configs-for-russia
> - `spacex.com:443`：igareck/vpn-configs-for-russia
> - `kclx.eu.org:443`：igareck/vpn-configs-for-russia
> - `14f7f5f0.mrbl69black.pages.dev:443`：igareck/vpn-configs-for-russia
> - `vless3.gem-audio2.us.ci:443`：igareck/vpn-configs-for-russia
> - `lanzerotte1312.live:443`：Maskkost93/kizyak-vpn-4.0
> - `1fd53cx.se5.h1clayd.shop:443`：Maskkost93/kizyak-vpn-4.0
> - `proxy-34l.pages.dev:2087`：igareck/vpn-configs-for-russia
> - `104.18.35.86:2096`：rekt0ro/ProxyRift
> - `62.60.219.235:443`：0xRadikal/Free-v2ray-Configs
> - `157.22.190.220:2053`：whoahaow/rjsxrd
> - `c3b4ce4b957a.vps.myjino.ru:53898`：Maskkost93/kizyak-vpn-4.0
> - `wells.aisb.dpdns.org:443`：igareck/vpn-configs-for-russia
> - `pl3.fox-lisa.ru:443`：Maskkost93/kizyak-vpn-4.0
> - `lt.t1n2.com:443`：Maskkost93/kizyak-vpn-4.0
> - `100gramm.pro:443`：Maskkost93/kizyak-vpn-4.0
> - `yd.2.hhhhh.eu.org:443`：igareck/vpn-configs-for-russia
> - `52.77.214.112:8443`：hello-world-1989/cn-news
> - `3.34.49.234:8443`：hello-world-1989/cn-news
> - `139.224.244.8:49534`：rtwo2/FastNodes
> - `178.17.58.55:443`：rtwo2/FastNodes
> - `de-tg.fastlanehosting.ru:443`：rtwo2/FastNodes
> - `82.29.36.252:443`：rtwo2/FastNodes
> - `45.192.203.44:10727`：rtwo2/FastNodes
> - `52.77.214.112:443`：hello-world-1989/cn-news
