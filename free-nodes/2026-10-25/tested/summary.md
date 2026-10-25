# 节点可用性验证报告

- 预筛：TCP 连通 1476/4094 个节点
- 测试地址：`https://gstatic.com/generate_204`，并发 12，每内核最多测试 40 个
- 总耗时：3.3 分钟

| 代理内核 | 测试数量 | 可用数量 | 可用率 | 订阅文件（base64） |
|---|---|---|---|---|
| xray | 40 | 5 | 12.5% | `xray/available_xray.txt` |
| v2ray | 40 | 5 | 12.5% | `v2ray/available_v2ray.txt` |
| mihomo | 40 | 10 | 25.0% | `mihomo/available_mihomo.txt` |
| singbox | 40 | 5 | 12.5% | `singbox/available_singbox.txt` |

## 可用节点池（跨天累积）

每个内核一份池：每天实测通过的节点自动入池，池内节点次日继续复测，
已失效的按「连续 N 天未通过」淘汰。

| 内核 | 池内节点 | 今日新增 | 今日复测通过 | 池文件 |
|---|---|---|---|---|
| xray | 5 | 5 | 0 | `pool/pool_xray.txt` |
| v2ray | 5 | 5 | 0 | `pool/pool_v2ray.txt` |
| mihomo | 10 | 10 | 0 | `pool/pool_mihomo.txt` |
| singbox | 5 | 5 | 0 | `pool/pool_singbox.txt` |

池目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes\pool`（`pool_<core>.txt` 可直接导入客户端，`pool_<core>.json` 含首见/最近通过/通过次数/最佳延迟）


## 仓库节点可用率（本次实测）

可用率是仓库质量的硬指标：连续偏低会降低采集优先级，长期 0 可用会被跳过。

| 仓库 | 实测 | 可用 | 可用率 | 平均延迟 | 质量分 |
|---|---|---|---|---|---|
| Pawdroid/Free-servers | 4 | 4 | 100% | 906ms | 81.9 |
| snakem982/proxypool | 8 | 3 | 38% | 629ms | 43.7 |
| 0xRadikal/Free-v2ray-Configs | 32 | 9 | 28% | 2759ms | 19.7 |
| igareck/vpn-configs-for-russia | 38 | 7 | 18% | 1788ms | 12.9 |
| Epodonios/v2ray-configs | 78 | 2 | 3% | 897ms | 13.9 |


## 输出文件命名

每个内核的可用清单文件名都带内核标识，互不覆盖：

| 文件 | 说明 |
|---|---|
| `available_<core>.txt` | base64 订阅，v2rayN / v2rayNG / 各内核客户端直接导入 |
| `available_<core>_list.txt` | 明文 URI 列表，一行一个节点 |
| `available_<core>_clash.yaml` | Clash / mihomo 配置 |
| `available_<core>_singbox.json` | sing-box 配置 |

其中 `<core>` 为 `xray` / `v2ray` / `mihomo` / `singbox`。

## 各内核可用节点详情

### xray（5 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `202.50.253.45:19999` | ss | 881ms | Epodonios/v2ray-configs |
| `49.12.253.100:1080` | ss | 906ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 916ms | Pawdroid/Free-servers |
| `46.17.43.227:18443` | ss | 1241ms | 0xRadikal/Free-v2ray-Configs |
| `156.226.168.166:443` | vless | 11692ms | 0xRadikal/Free-v2ray-Configs |

### v2ray（5 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `59.125.69.22:443` | vless | 384ms | snakem982/proxypool |
| `49.12.253.100:1080` | ss | 798ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 907ms | Pawdroid/Free-servers |
| `202.50.253.45:19999` | ss | 913ms | Epodonios/v2ray-configs |
| `46.17.43.227:18443` | ss | 969ms | 0xRadikal/Free-v2ray-Configs |

### mihomo（10 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `49.12.253.100:1080` | ss | 718ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 902ms | Pawdroid/Free-servers |
| `46.17.43.227:18443` | ss | 1043ms | 0xRadikal/Free-v2ray-Configs |
| `59.125.69.22:443` | vless | 1055ms | snakem982/proxypool |
| `45.88.12.26:443` | hysteria2 | 1322ms | igareck/vpn-configs-for-russia |
| `147.45.61.58:443` | hysteria2 | 1537ms | igareck/vpn-configs-for-russia |
| `video-balancer.7.8.advantage-a.cdnnow.xyz:443` | hysteria2 | 1599ms | igareck/vpn-configs-for-russia |
| `143.246.211.163:443` | hysteria2 | 1876ms | igareck/vpn-configs-for-russia |
| `45.88.12.122:443` | hysteria2 | 1907ms | igareck/vpn-configs-for-russia |
| `156.226.168.166:443` | vless | 6700ms | 0xRadikal/Free-v2ray-Configs |

### singbox（5 个可用）

| 节点 | 协议 | 延迟 | 来源仓库 |
|---|---|---|---|
| `59.125.69.22:443` | vless | 449ms | snakem982/proxypool |
| `49.12.253.100:1080` | ss | 760ms | 0xRadikal/Free-v2ray-Configs |
| `202.50.253.81:19999` | ss | 899ms | Pawdroid/Free-servers |
| `45.88.12.122:443` | hysteria2 | 1959ms | igareck/vpn-configs-for-russia |
| `45.88.12.26:443` | hysteria2 | 2317ms | igareck/vpn-configs-for-russia |
