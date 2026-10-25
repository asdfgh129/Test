# 代理内核部署说明

`test_nodes.py` 依赖四个代理内核的 Windows 可执行文件，默认放在 `~/.workbuddy/data/free-nodes-tools/bin/`（与技能目录分离，避免内核二进制进入技能分发包）。也可用环境变量 `FREE_NODES_TOOLS` 指向任意目录。

## 目录要求

```
~/.workbuddy/data/free-nodes-tools/bin/
├── xray/xray.exe
├── v2ray/v2ray.exe
├── mihomo/mihomo.exe
└── singbox/sing-box.exe
```

sing-box 若为官方 zip 解压，需保留同目录的 `libcronet.dll`。

## 下载来源（2026-10 实测可用版本）

| 内核      | 仓库                | 资产名                                          |
| ------- | ----------------- | -------------------------------------------- |
| xray    | XTLS/Xray-core    | `Xray-windows-64.zip`                        |
| v2ray   | v2fly/v2ray-core  | `v2ray-windows-64.zip`                       |
| mihomo  | MetaCubeX/mihomo  | `mihomo-windows-amd64-compatible-vX.Y.Z.zip` |
| singbox | SagerNet/sing-box | `sing-box-X.Y.Z-windows-amd64.zip`           |

## 下载方式

GitHub releases 直连通常不可用，走加速前缀（与采集脚本同一套镜像）：

```python
url = f"https://github.com/{repo}/releases/download/{tag}/{asset}"
for prefix in ("https://gh-proxy.com/", "https://ghfast.top/", ""):
    # 下载 prefix + url，成功后解压到 ~/.workbuddy/data/free-nodes-tools/bin/<core>/
```

提示：

- 可以用 API 查最新版本与资产名（`/repos/{repo}/releases/latest`），避免硬编码版本号
- 大文件经镜像易被截断：用 `curl -C -` 断点续传补齐后，再用 `zipfile.ZipFile(...).testzip()` 校验完整性
- 2026-10 实测版本：xray v26.10.21 / v2ray v5.53.0 / mihomo v1.19.33 / sing-box v1.14.4

升级内核：覆盖 `bin/<core>/` 内文件即可，脚本按固定文件名寻找可执行文件。

## 内核用途

- **xray / v2ray**：验证 vmess/vless/trojan/ss 节点；xray 额外支持 reality
- **mihomo**：验证含 hysteria2/tuic 的全协议节点（Clash 生态）
- **singbox**：验证全协议节点（sing-box 生态）

验证只使用本地 HTTP 入站 + 单个出站的最小配置，测完立即结束进程并清理临时文件，不写入系统代理设置。

## 配置要点（实测踩坑）

| 内核       | 关键点                                                                               |
| -------- | --------------------------------------------------------------------------------- |
| mihomo   | 必须加 `skip-cert-verify: true`（免费节点常用共享证书，域名不匹配）；每个测试实例需独立的 `-d` 数据目录，否则并发时会话冲突     |
| mihomo   | reality 节点需 `reality-opts`（public-key / short-id）+ `client-fingerprint`           |
| sing-box | reality 节点必须启用 `tls.utls`（否则报 `uTLS is required by reality client`）               |
| xray     | reality 需 `realitySettings`（publicKey / shortId / fingerprint），并置 `allowInsecure` |
| v2ray    | v2fly 不支持 reality，此类节点会被判定为不可用（属正常）                                               |
