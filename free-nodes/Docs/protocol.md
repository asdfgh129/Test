# 协议适配规范（protocol.md）

> 本文件回答一件事：**我们生成的节点配置，是否严格符合各代理内核当前版本的要求。**
> 每条结论都有出处：① 内核自带校验命令的实测结果；② 内核源码/官方文档的字段定义。
> 核对日期 **2026-10-25**，基线版本见下表。内核升级后必须重跑 `scripts/protocol_check.py`
> 重新对齐（流程见文末「维护规则」）。

## 1. 基线版本

| 对外名 | 实际内核 | 版本 | 可执行文件 | 配置校验命令 |
|---|---|---|---|---|
| `v2ray` | v2fly/v2ray-core | **5.53.0** | `v2ray.exe` | `v2ray test -c <cfg>` |
| `xray` | XTLS/Xray-core | **26.10.21** | `xray.exe` | `xray -test -config <cfg>` |
| `clash` | MetaCubeX/mihomo | **1.19.33** | `mihomo.exe` | `mihomo -t -f <cfg> -d <dir>` |
| `singbox` | SagerNet/sing-box | **1.14.4** | `sing-box.exe` | `sing-box check -c <cfg>` |

核对方式：对每种「协议 × 传输 × 安全层 × 插件」组合生成一份单节点配置，交给上表的
校验命令。校验命令拒绝 = 该内核不支持这种写法（配置类错误）；校验通过才进入真机连通测试。

## 2. 三层判定模型

```
分享链接(URI)  ──①能力预筛(CAPS)──▶ 该内核能表达吗？
                                        │否 → 归入「不支持」，不发布、不计入不可达
                                        ▼是
                              ②生成内核原生配置
                                        │失败 → 归入「不支持」(参数缺失/无法表达)
                                        ▼
                              ③内核自校验(check)
                                        │失败 → 归入「配置错误」，不发布、不计入不可达
                                        ▼通过
                              ④起进程 + 本地 HTTP 代理 CONNECT 实测
                                        │失败 → 按原因归类(tls/auth/refused/reset/timeout)
                                        ▼2xx
                                     「可用」
```

关键约定：

- **不允许静默降级**。传输层参数识别不了时必须返回「不支持」，禁止退化成 `tcp`。
  历史 Bug：`type=xhttp / httpupgrade / kcp / quic` 曾被当成 `tcp` 生成配置，
  节点必然连不上，却被记成「不可达」（见 known-issues 第 22 条）。
- **`config` / `unsupported` 两种结果永不进入「不可达」分母**。否则可用率会被系统性低估。
- 传输层网络名统一：URI 的 `type=h2` → 规范名 `http`；`type=splithttp` → 规范名 `xhttp`；
  `type=none` / 空 → `tcp`。

## 3. 各内核支持矩阵

### 3.1 协议

| 协议 | v2ray 5.53 | xray 26.10 | clash 1.19 | singbox 1.14 |
|---|---|---|---|---|
| `vmess` | ✅ | ✅（有弃用告警） | ✅ | ✅ |
| `vless` | ✅ | ✅ | ✅ | ✅ |
| `trojan` | ✅ | ✅ | ✅ | ✅ |
| `ss`（Shadowsocks） | ✅ 仅 AEAD | ✅ AEAD + 2022 | ✅ 含旧流加密 | ✅ 含旧流加密 |
| `ssr` | ❌ | ❌ | ✅ | ❌ |
| `hysteria2` / `hy2` | ✅（装填方式特殊，见 §3.6） | ✅（协议名 `hysteria`+`version:2`，见 §3.6） | ✅ | ✅ |
| `hysteria`（v1） | ❌ | ❌ | ❌（本流水线不处理） | ❌ |
| `tuic`（v5） | ❌ | ❌ | ✅ | ✅ |

> **勘误（2026-10-25，二次修正）**：早期版本把 v2ray、xray 的 hysteria2 都标为 ❌，
> **两次都是错的**。① v2fly 5.x 支持 Hysteria2（官方文档 `config/proxy/hy2.md` +
> `config/stream/hy2.md`），实测 v2ray↔sing-box 端到端 HTTP 200。② **Xray 同样支持**：
> 自 v26.1.23 引入，本机 xray 26.10.21 二进制含 `HysteriaClientConfig` /
> `HysteriaServerConfig` / `HysteriaInboundValidator` / `salamander` / `udphop` / `obfs`
> 字样（678 处 hysteria），源码 `infra/conf/hysteria.go` + `proxy/hysteria/client.go` +
> `transport/internet/hysteria/dialer.go` 可证，`xray run -test` 配置校验通过、客户端
> 能拨号并完成到服务端的 TLS 握手。**早先判「Xray 不支持」是双重误判**：一是用
> `xray.exe | grep`（扫的是进程 stdout 而非二进制文件）导致漏检；二是不知道 Xray 把
> 它实现为 `protocol: "hysteria"` + `version: 2`（**不是** `hysteria2` 字样），按
> `hysteria2` 去写配置自然被拒。教训：能力判定必须 grep 二进制**文件** + 查源码 +
> E2E，不能只看进程输出、也不能只按协议名字面猜。
> 容易误判的另一个原因：v2fly 对未知字段宽松（不报错、静默忽略），只跑 config
> check 看不出装填错误，必须端到端实测。

### 3.2 传输层

| URI `type=` | 规范名 | v2ray 5.53 | xray 26.10 | clash 1.19 | singbox 1.14 |
|---|---|---|---|---|---|
| `tcp` / 空 / `none` | tcp | ✅ | ✅ | ✅ | ✅ |
| `ws` | ws | ✅ | ✅（`host` 已迁出 headers） | ✅ | ✅ |
| `grpc` | grpc | ✅ | ✅ | ✅ | ✅ |
| `http` / `h2` | http | ✅ | ❌ 已移除 | ✅（`http-opts` / `h2-opts` 分开写） | ✅ |
| `kcp` / `mkcp` | kcp | ✅ | ✅ | ❌ | ❌ |
| `quic` | quic | ✅ | ❌ 已移除 | ❌ | ✅ 但**强制要求 TLS** |
| `httpupgrade` | httpupgrade | ❌ | ✅ | ⚠️ 未确认，保守跳过 | ✅ |
| `xhttp` / `splithttp` | xhttp | ❌ | ✅ | ✅（`xhttp-opts`） | ❌ |

依据（内核实测原文）：

- Xray 26.x：`The feature HTTP transport (without header padding, etc.) has been removed and
  migrated to XHTTP stream-one H2 & H3.`；QUIC 传输同样报 removed。
- Xray 26.x：`The feature WebSocket transport (with ALPN http/1.1, etc.) is deprecated` +
  `This feature "host" in "headers" is deprecated, will be removed soon and being migrated to
  independent "host".` → 给 Xray 生成 ws 时用 `wsSettings.host`，不再塞 `headers.Host`。
- v2fly 5.53：`Config: unknown transport protocol: httpupgrade / xhttp / splithttp`。
- sing-box 1.14：`outbounds[0].transport: unknown transport type: xhttp`；`quic: TLS required`。

### 3.3 安全层（TLS / REALITY）

| 项 | v2ray 5.53 | xray 26.10 | clash 1.19 | singbox 1.14 |
|---|---|---|---|---|
| 普通 TLS | ✅ `tlsSettings.serverName` | ✅ 同左 | ✅ `tls: true` + `servername` | ✅ `tls.server_name` |
| 跳过证书校验 | `allowInsecure: true` | ❌ **已移除**（见下） | `skip-cert-verify: true` | `tls.insecure: true` |
| ALPN | `tlsSettings.alpn[]` | 同左 | `alpn[]` | `tls.alpn[]` |
| uTLS 指纹 | `tlsSettings.fingerprint` | 同左 | `client-fingerprint` | `tls.utls.fingerprint` |
| REALITY | ❌ 不支持 | ✅ `realitySettings` | ✅ `reality-opts` | ✅ `tls.reality` + `utls` |
| VLESS 必须 TLS | ❌ 不强制 | ✅ **强制**（否则拒绝配置） | ❌ 不强制 | ❌ 不强制 |
| Trojan 必须 TLS | 协议本体要求（配置需补 TLS） | ✅ 强制，且报错 | 协议本体要求 | 协议本体要求 |

**Xray 26.x 的证书校验**：`allowInsecure` 被彻底移除，官方迁移目标是
`pinnedPeerCertSha256`(pcs) 与 `verifyPeerCertByName`(vcn)，二者都不能等价地「跳过校验」。
因此：

- Xray 侧**无法**测试自签/错域名证书的节点，这类节点用 Xray 26 客户端本来也连不上，
  验证失败属于真实不可用，但原因归 `tls`，不是 `timeout`。
- `detect_core_features()` 会先用一条 TLS 样本探测该版本是否还接受 `allowInsecure`，
  不写死版本号，避免升级后配置直接启动失败。

**REALITY 参数要求（四内核一致）**：

| 参数 | URI | 要求 |
|---|---|---|
| `pbk`（公钥） | `?pbk=` | 32 字节 base64url，**恰好 43 字符**；长度不符内核直接拒配置，本流水线判「不支持」 |
| `sid`（shortId） | `?sid=` | 十六进制，≤16 字符，可为空 |
| `sni`（serverName） | `?sni=` | 必填 |
| `fp`（指纹） | `?fp=` | 缺省补 `chrome`；sing-box 必须同时开 `utls` |

**Trojan 的 TLS**：`trojan://` 链接里经常不写 `security=tls`。Trojan 协议本体就运行在 TLS
之上，因此**无论链接怎么写都要补 TLS**。以前直接把 `security` 参数透传，导致这类节点
在 v2ray/xray/clash/sing-box 上全部「不可达」（假阴性）。

### 3.4 Shadowsocks 加密方式与插件

| 加密方式 | v2ray 5.53 | xray 26.10 | clash 1.19 | singbox 1.14 |
|---|---|---|---|---|
| `aes-128-gcm` / `aes-256-gcm` | ✅ | ✅ | ✅ | ✅ |
| `chacha20-ietf-poly1305` | ✅ | ✅ | ✅ | ✅ |
| `xchacha20-ietf-poly1305` | ❌ | ✅ | ✅ | ✅ |
| `2022-blake3-*` | ❌ | ✅ 需定长密钥 | ✅ | ✅ |
| `aes-256-cfb` / `chacha20-ietf` / `rc4-md5` | ❌ `unknown cipher method` | ❌ 同左 | ✅ | ✅（仅出站） |
| `none` | ✅ | ❌ | ✅ | ✅ |

- **2022 系列密钥必须定长**：`2022-blake3-aes-128-gcm` → 16 字节，
  `2022-blake3-aes-256-gcm` / `2022-blake3-chacha20-poly1305` → 32 字节，
  且为 base64 编码（含 `=` 填充）。长度不符时内核报
  `shadowsocks_2022: invalid key` / `decode public_key`，本流水线判「不支持」。
- **sing-box 的旧流加密只支持出站**：客户端能用 `aes-256-cfb` 连（实测与 mihomo 服务端
  端到端互通），但**入站已移除**（`unsupported method: aes-256-cfb`）。我们只作出站，故放行。
- **SS 插件**（URI `?plugin=`）：

| 插件 | URI 写法 | v2ray | xray | clash | singbox |
|---|---|---|---|---|---|
| simple-obfs | `plugin=obfs-local;obfs=http;obfs-host=x` | ❌ | ❌ | ✅ `plugin: obfs` + `plugin-opts{mode,host}` | ✅ `plugin: obfs-local` + `plugin_opts: "obfs=http;obfs-host=x"` |
| v2ray-plugin | `plugin=v2ray-plugin;mode=websocket;host=x;path=/ws;tls` | ❌ | ❌ | ✅ `plugin: v2ray-plugin` | ✅ 原样进 `plugin_opts` |
| shadow-tls | `plugin=shadow-tls;host=..;password=..;version=..` | ❌ | ❌ | ⚠️ 不作为 ss 插件支持 | ⚠️ 未确认 |

v2ray/xray **没有任何 ss 插件机制**，带插件的 ss 节点必须判「不支持」，否则生成的配置
只是「普通 ss」，连不上却会被算作节点失效。

### 3.5 传输层字段映射表

| 传输 | v2ray / xray（streamSettings） | clash（mihomo） | sing-box（transport） |
|---|---|---|---|
| ws | `wsSettings{path, host}`（Xray 用 `host`；v2ray 用 `headers.Host`） | `network: ws` + `ws-opts{path, headers{Host}, max-early-data, early-data-header-name}` | `{type: ws, path, headers{Host}, max_early_data, early_data_header_name}` |
| grpc | `grpcSettings{serviceName}`（URI 的 `serviceName`，缺省用 `path`） | `network: grpc` + `grpc-opts{grpc-service-name}` | `{type: grpc, service_name}` |
| http / h2 | `httpSettings{path, host[]}` | `type=http` → `network: http` + `http-opts{path[], method: GET, headers{Host[]}}`；`type=h2` → `network: h2` + `h2-opts{host[], path}` | `{type: http, host[], path}` |
| kcp | `kcpSettings{mtu, tti, congestion, header{type}, seed}` | ❌ | ❌ |
| quic | `quicSettings{security, key, header{type}}` | ❌ | `{type: quic}` + 必须有 `tls` |
| httpupgrade | `httpupgradeSettings{path, host}` | ⚠️ 跳过 | `{type: httpupgrade, host, path}` |
| xhttp | `xhttpSettings{path, host, mode}`（`splithttp` → xhttp） | `network: xhttp` + `xhttp-opts{path, host, mode}` | ❌ |

### 3.6 其他协议的专属参数

**hysteria2 / hy2**（clash、singbox）

| URI 参数 | 含义 | clash | singbox |
|---|---|---|---|
| userinfo | 认证口令 | `password` | `password` |
| `sni` | TLS 域名 | `sni` | `tls.server_name` |
| `insecure=1` | 跳过证书校验 | `skip-cert-verify` | `tls.insecure` |
| `obfs=salamander` | 混淆类型 | `obfs: salamander` | `obfs{type: salamander}` |
| `obfs-password` | 混淆口令 | `obfs-password` | `obfs.password` |
| `mport=443-8443` | 端口跳跃 | `ports: 443-8443`（+`hop-interval`） | `server_ports: ["443:8443"]`（+`hop_interval: "30s"`） |
| `up` / `down` | 带宽（Mbps） | `up` / `down` | `up_mbps` / `down_mbps` |

**tuic v5**（clash、singbox）

| URI 参数 | 含义 | clash | singbox |
|---|---|---|---|
| `uuid:password` | 认证（缺一不可） | `uuid` / `password` | `uuid` / `password` |
| `sni` | TLS 域名 | `sni` | `tls.server_name` |
| `alpn=h3` | ALPN | `alpn[]` | `tls.alpn[]`（缺省补 `h3`） |
| `congestion_control=bbr` | 拥塞控制 | `congestion-controller` | `congestion_control` |
| `udp_relay_mode=native` | UDP 中继模式 | `udp-relay-mode` | `udp_relay_mode` |
| `disable_sni=1` | 不发送 SNI | `disable-sni` | — |
| `reduce_rtt=1` | 0-RTT | `reduce-rtt` | — |

> `tuic://` 的 userinfo 是 `uuid:password` 两段。`urllib` 会把 `password` 拆到
> `urlsplit().password`，只取 `.username` 会导致 uuid 缺口令、配置生成失败（已修）。

**v2ray 的 hysteria2 装填（特殊，2026-10-25 官方文档 + E2E 实测）**

v2fly 5.x 把 Hysteria2 拆成两层：`TLS + HTTP3` 传输层（认证、拥塞控制）+
`Proxy Header` 代理层（目标地址、Padding）。要连**官方版 / sing-box / mihomo**
的 hysteria2 服务端，必须两层都写：

```json
{
  "protocol": "hysteria2",
  "settings": {"servers": [{"address": "a.com", "port": 443}]},
  "streamSettings": {
    "network": "hysteria2",
    "security": "tls",
    "tlsSettings": {"serverName": "a.com", "allowInsecure": true},
    "hy2Settings": {"password": "口令"}
  }
}
```

要点（全部为 v2ray 5.53 实测 + 官方文档确认）：

- 代理层 `settings.servers` **只有 `address` / `port`，没有密码字段**——密码在
  传输层 `hy2Settings.password`。字段名是 `hy2Settings`（不是 hysteria2Settings）
- 不配证书时官方默认行为即 `allowInsecure`；我们显式写 `security: tls` +
  `allowInsecure`，否则报 `Hysteria2 based on QUIC that requires TLS.`
- **不支持** `obfs`（salamander 混淆）与 `mport`（端口跳跃），且 v2fly 对未知
  字段宽松、静默忽略——转换器遇到这两个参数直接判「不支持」，不许静默降级
- 兼容性实测：v2ray 客户端 ↔ sing-box 服务端端到端 HTTP 200；
  ↔ mihomo listener（hysteria2 入站）认证 404，**mihomo 入站不兼容 v2fly 实现**
  （客户端只关心出站兼容，不影响本流水线）

**xray 的 hysteria2 装填（2026-10-25 源码 + 二进制 + config check 实测）**

Xray 自 v26.1.23 起支持 Hysteria2，但装填与 v2fly **完全不同**（源码
`infra/conf/hysteria.go`、`proxy/hysteria/client.go`、`transport/internet/hysteria/dialer.go`）：

```json
{
  "protocol": "hysteria",
  "settings": {"version": 2, "address": "a.com", "port": 443},
  "streamSettings": {
    "network": "hysteria",
    "hysteriaSettings": {"version": 2, "auth": "口令", "up": "100mbps", "down": "500mbps"},
    "security": "tls",
    "tlsSettings": {"serverName": "a.com"}
  }
}
```

要点：

- **协议名是 `hysteria`（不是 `hysteria2`）**，且 `settings.version` 与
  `hysteriaSettings.version` **都要写 2**，缺一个报 `version != 2`
- `address` / `port` **平铺在 `settings`**（不是 `settings.servers[]`，也不是
  `settings.server`——早期试过这两种都会被拨号时 nil 指针 panic）；认证口令在
  传输层 `hysteriaSettings.auth`（对应 `Hysteria-Auth` 头），**不在 settings**
- `up` / `down`（带宽，`<N>mbps`）是启用 hysteria2 的必要字段；端口跳跃写
  `hysteriaSettings.udphop{port, interval}`；salamander 混淆写
  `streamSettings.finalmask.udp[{type: salamander, settings:{password}}]`
- `streamSettings.allowInsecure` 字段名还在但 **TLS 校验不吃它**；Xray 26 已移除
  `tlsSettings.allowInsecure`，insecure 节点用 `tlsSettings.verifyPeerCertByName`
  （= 服务名，跳过 CA、只校证书名）覆盖，见 §3.5
- 实测状态：`xray run -test` 全过、客户端能拨号并完成到服务端的 TLS 握手；本机
  回环 E2E 卡在**服务端** SNI 选证书（Go 服务端按 DNS 名匹配，测试证书无对应 SAN），
  属回环测试假象，非客户端配置问题——对真实节点（证书匹配域名 + SNI）预期可用，
  见 known-issues 第 27 条


**vmess**（四内核）

URI 是 base64(JSON)，字段落在配置里：

| JSON 字段 | 含义 | 落到配置 |
|---|---|---|
| `add` / `port` / `id` | 服务器 / 端口 / UUID | `server` / `port` / `uuid` |
| `aid` | alterId | `alterId`（clash）/ `alter_id`（sing-box）/ `alterId`（v2ray） |
| `scy` | 加密方式 | `cipher`（clash）/ `security`（sing-box、v2ray `users[].security`） |
| `net` | 传输层 | 见 §3.5 |
| `tls` | `tls`/`true`/`1` 表示 TLS | `tls: true` 或 `tlsSettings` |
| `host` | ws/h2 的 Host，kcp 的 header 类型 | 见 §3.5 |
| `path` | ws 路径 / grpc 服务名 / h2 路径 | 见 §3.5 |
| `sni` | TLS 域名 | `servername` / `tls.server_name` |

> vmess 的 `net` 曾经只认 `tcp/ws/grpc/h2`，`http`、`httpupgrade`、`xhttp`、`kcp`、`quic`
> 一律退化成 `tcp` —— 这是历史上最大的一类假阴性来源，现已按 §3.2 逐个映射。

## 4. 「测不过」如何证明是节点真的不可达

判定链每一环都有可复核的证据，缺一环都不能算「不可达」：

| 环节 | 证据 | 不通过的归类 | 是否计入「不可达」 |
|---|---|---|---|
| ① 能力预筛 | `layout.supports()`：协议/传输/加密/插件/公钥长度 | `unsupported` | ❌ |
| ② 配置生成 | 转换器返回 None（无法表达） | `unsupported` | ❌ |
| ③ 内核自校验 | 失败后用内核 `check` 复核并抓原文 | `config` | ❌ |
| ④ 进程就绪 | 端口在 `startup_timeout` 内监听、进程未退出 | `startup` / `config` | ❌ |
| ⑤ CONNECT 实测 | 通过本地 HTTP 代理取 `https://gstatic.com/generate_204` 得 2xx | 见下 | ✅ |
| ⑥ 复测 | 网络类失败再跑 1 次（`--retry`），两次都失败才定案 | 同上 | ✅ |

**为什么测试地址是 `https://gstatic.com/generate_204`：**

- 用裸域（不带 `www`）：`www.gstatic.com` 解析到国内缓存节点，本机直连就 204，毫无区分度；
  裸域只解析到海外 IP，本机直连超时 —— 只有真把流量送出境外才可能拿到 204。
- 必须 HTTPS：要求节点具备 CONNECT 隧道能力，与真实翻墙场景一致；明文 HTTP 会被中间人篡改。
- 不跟随重定向：3xx 一律判不可用，防止节点把探测流量导向任意站点。

**失败原因分类（依据内核日志 + 客户端异常文本）：**

| 原因 | 典型证据（内核/客户端原文） | 说明 |
|---|---|---|
| `unsupported` | 转换器返回 None；`unknown transport` / `unknown cipher method` | 本机内核不支持，节点本身可能没问题 |
| `config` | `failed to build outbound` / `invalid key` / `is prohibited` / `has been removed` | 参数不符，我们写错了或链接残缺 |
| `tls` | `x509` / `certificate` / `tls handshake failure` / `SSLError` | 证书、SNI 或协议不匹配 |
| `auth` | `authentication failed` / `invalid uuid` / `bad key` | 口令、UUID、密码不对 |
| `refused` | `connection refused` / `actively refused` | 端口无服务 |
| `reset` | `connection reset` / `EOF` / `remote end closed` | 被墙、被中断 |
| `timeout` | `i/o timeout` / `context deadline exceeded` | 丢包或被丢弃 |
| `startup` | 端口未监听且进程仍存活 | 内核自身问题 |

**交叉印证（审计用）：**

1. 同一个节点在四个内核上的结论做对比：**四内核都失败且 TCP 预筛可达 → 高概率真死**；
   只在一个内核失败、其他内核可用 → 优先怀疑该内核的配置映射问题，而不是节点。
2. TCP 预筛（2s 握手）与代理实测分开记录：TCP 都不通的节点根本不进入代理测试，
   避免把「服务器宕机」和「协议参数错」混为一谈。
3. 每次跑完看 `Docs/summary.md` 的「失败原因分布」：出现成片的 `config` 就是转换器有 Bug，
   出现成片的 `unsupported` 就是能力矩阵需要对齐内核，而不是节点质量下降。

## 5. 已知不支持组合（本流水线主动跳过）

| 组合 | 原因 |
|---|---|
| `ss` + 插件 → v2ray / xray | 这两个内核没有插件机制 |
| `ss` 旧流加密（CFB/rc4-md5） → v2ray / xray | 内核已移除，配置直接被拒 |
| `ss2022` → v2ray | v2fly 未实现 2022 |
| `ss2022` 密钥长度不符 → 全部内核 | 内核校验密钥长度 |
| `ssr` → v2ray / xray / singbox | 只有 mihomo 支持 |
| `tuic` → v2ray / xray | 协议未实现 |
| `hysteria2` + `obfs` / `mport` → v2ray | v2fly 无混淆/端口跳跃字段，未知字段被静默忽略 |
| `hysteria`（v1） → 全部 | 四内核均不在支持范围（Xray 的 `hysteria` 只是 v2 的内部协议名） |
| REALITY + v2ray | v2fly 无 REALITY |
| REALITY 公钥非 43 字符 → 全部 | 内核拒绝，属于坏链接 |
| `type=http`/`h2` → xray 26+ | HTTP 传输已移除，只能改用 xhttp stream-one |
| `type=quic` → xray 26+ / clash | 传输已移除 / 未实现 |
| `type=xhttp` → v2ray / singbox | 传输未实现 |
| `type=httpupgrade` → v2ray / clash | 传输未实现（clash 未确认，保守跳过） |
| `type=kcp` → clash / singbox | 传输未实现 |
| VLESS 无 TLS → xray 26+ | 内核禁止（私网地址除外） |

## 6. 维护规则

1. **内核升级后**（`check_kernels.py --update`）依次执行：
   ```
   python scripts/check_kernels.py --root free-nodes          # 版本 + 能力指纹
   python scripts/protocol_check.py                           # 本文件全部结论的回归
   ```
   `protocol_check.py` 退出码 1 表示：转换器或 `layout.CAPS` 与新内核不一致，必须修正后再采集。
2. **新增协议/传输时**，顺序是：先在本文件登记字段规范 → 改 `layout.CAPS` → 改转换器
   （`uri_to_clash` / `uri_to_singbox` / `uri_to_v2ray_outbound`）→ 在 `protocol_check.py`
   里加用例（含预期「不支持」的用例）→ 通过后再跑采集。
3. **禁止**为了让某个节点「测通」而放宽能力矩阵；矩阵只描述内核事实，不描述希望。
4. 版本基线变化时，同步更新本文件 §1 的表格与相关说明，并在 `Docs/known_issue.md` 留一条记录。

## 7. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-10-25 | 建立本文件。按内核实测校准四内核支持矩阵；修复传输层静默退化为 tcp、trojan 缺 TLS、tuic 口令截断、ss 插件丢失、REALITY 公钥校验等 6 类解析缺陷；验证阶段引入失败原因分层与复测 |
| 2026-10-25 | **二次勘误 xray hysteria2**：早先误判「Xray 不支持 Hysteria2」（`xray.exe\|grep` 扫了进程 stdout 漏检 + 不知道协议名是 `hysteria`+`version:2`）。本机 xray 26.10.21 二进制 678 处 hysteria 字样 + 源码 `infra/conf/hysteria.go` + `xray run -test` 实测确认支持（v26.1.23 引入）；§3.1 矩阵、§3.6 装填、§5 不支持表、`layout.CAPS`、`test_nodes.uri_to_v2ray_outbound` 全部改为支持，新增 salamander(udphop)/端口跳跃装填 |
| 2026-10-25 | **目录布局调整 + 验证全量策略**（用户要求）：① free-nodes/ 根目录只保留 README.md 与 CHANGELOGS.md（changelog.md 更名），节点产物全部迁入 `nodes/`、文档迁入 `Docs/`、脚本与采集状态迁入 `src/`；② 验证默认改为**全量测试**：某内核候选 ≤ 3000 全部实测，超过则只测排序前 3000 个（协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序），`--no-full-test` 可回退旧的限量取样 + 自适应扩量模式 |
| 2026-10-25 | **技能迁入仓库 + 消除全部副本同步**（用户要求）：技能目录移至 `Skills/free-nodes-collector/`（只留 SKILL.md），`src/` 成为脚本唯一事实来源（publish_free_nodes.py 从 tools/ 迁入，删除 sync_src 与 package_skill），references 文档全部并入 `Docs/`；文件名复数规范化（known_issues / collection_logs / review_logs）；项目记忆 `.workbuddy/memory/` 纳入 git 跟踪。全量测试上限按用户纠正由 30000 改为 3000 |
