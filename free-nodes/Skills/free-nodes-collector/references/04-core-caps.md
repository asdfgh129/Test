# 四内核能力矩阵与分流规则

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

## 四内核能力分流（layout.CAPS）

采集到的是**一份**去重后的全量节点（`nodes_uris.txt`），写订阅时按四内核各自真实支持的能力**分流**成四个文件。分流不是"按仓库分"，而是按节点的协议特征判定——同一个仓库的订阅里往往混着各内核都能用和各内核都用不了的节点。

> 完整规范（每种协议/传输/加密的字段要求、URI 参数映射、失败分类口径）见
> **`Docs/protocol.md`**；一致性回归跑 `src/protocol_check.py`。
> 自建代理与节点测试链路的**文件组成与函数级说明**见 **`Docs/proxy.md`**。

下表为 **2026-10-25 按内核实测校准**的结果（v2ray 5.53.0 / xray 26.10.21 / mihomo 1.19.33 / sing-box 1.14.4）：

| 维度 | v2ray | xray | clash(mihomo) | singbox |
|---|---|---|---|---|
| 代理协议 | vmess/vless/trojan/ss/hysteria2* | 同左（含 hysteria2*） | 同左 + ssr/hysteria2/tuic | 同左 + hysteria2/tuic |
| 传输层 | tcp/kcp/ws/http/quic/grpc | tcp/kcp/ws/grpc/**httpupgrade/xhttp** | tcp/ws/http/h2/grpc/xhttp | tcp/ws/http/grpc/httpupgrade/quic(TLS) |
| 已移除的传输 | httpupgrade/xhttp | **http/h2、quic** | kcp/quic/httpupgrade | xhttp |
| REALITY | ✗ | ✓ | ✓ | ✓ |
| VLESS flow（xtls-rprx-vision） | ✓ | ✓ | ✓ | ✓ |
| ss 加密 | 仅 AEAD | AEAD + 2022 | 全部（含 CFB/rc4） | 全部（仅出站） |
| ss 插件 | ✗ | ✗ | obfs / v2ray-plugin | obfs-local / v2ray-plugin |
| VLESS/Trojan 必须 TLS | ✗ | ✓（26.x 强制） | ✗ | ✗ |

要点：

- `v2ray` 与 `xray` **共用同一份源订阅**（仓库里针对 v2ray 系内核的那条链接），采集时按上表分流：带 reality / xhttp / httpupgrade 的节点只进 `xray_sub.txt`；带 `type=http`/`h2` 的节点只进 `v2ray_sub.txt`（Xray 26 已移除 HTTP 传输）
- hysteria2 节点现在也进 `v2ray_sub.txt` 和 `xray_sub.txt`（v2fly 5.x、Xray 26.x 均支持，2026-10-25 核实）：v2ray 侧带 `obfs` / `mport` 参数的除外（v2fly 静默忽略，见 known-issues 第 26 条）；xray 侧协议名是 `hysteria`+`version:2`，**支持** salamander 混淆与端口跳跃（见 protocol.md §3.6 与 known-issues 第 27 条）
- v2fly 至今不支持 REALITY，把这类节点写给 v2ray 只会让客户端整份配置导入失败，所以必须前置过滤
- 同一节点可能同时出现在多个内核文件里（说明兼容性好），这不是重复 bug
- 分流实现在 `layout.filter_uris(core, uris)`（判定事实来自 `layout.node_facts()`，与转换器共用一套规则）；能力表在 `layout.CAPS`
- 内核升级后跑 `check_kernels.py` 看能力指纹漂移，再跑 `protocol_check.py` 验证转换器是否仍然合规
- **转换器不许静默降级**：识别不了的传输必须判「不支持」，禁止兜底成 `tcp`（否则节点会因参数丢失而连不上，被误记成不可达，见 known-issues 第 22 条）

---

### 内核版本与能力漂移检查（check_kernels.py）

内核升级会悄悄改变"它到底能吃什么"，历史上已经踩过两次：

- **Xray 26.x 移除 `tlsSettings.allowInsecure`**（报错要求改用 `pinnedPeerCertSha256` / `verifyPeerCertByName`）——沿用老配置模板会让 xray **全部样本验证失败**，看起来像"节点全死了"
- **v2fly 5.x 改了配置校验命令**（`-test -config` 报 `flag provided but not defined`，新写法是 `test -c`）——沿用老命令会让 v2ray 的每个样本都判"未被接受"

所以每次采集前建议跑一次（**推荐与采集合并成一条命令**，代理只建一次）：

```bash
python <free-nodes>/src/check_kernels.py --root <输出根目录>            # 只检查，不改动（结束自动关通道）
python <free-nodes>/src/check_kernels.py --root <输出根目录> --update   # 有新版本就下载安装
python <free-nodes>/src/collect_nodes.py --out <输出根目录> --check-kernels   # 推荐：检查+采集一体
```

**这一步本身就要访问 GitHub（`api.github.com` 查 release），所以它会先自建代理再查**：按
`--uplink auto`（默认）用已验证节点起本地通道。走免费节点代理时出口 IP 与他人共享，**匿名配额
（60/时）几乎必然 403，必须带 token**（`--token` 或凭据文件，自动读取）。检查结束后默认关掉通道；
被 `collect_nodes.py --check-kernels` 调用时，通道直接移交给采集环节继续用。

它做两件事：

1. **版本检查**：对比本地二进制版本与 GitHub 最新 release（XTLS/Xray-core、v2fly/v2fly-core、MetaCubeX/mihomo、SagerNet/sing-box），输出有无更新
2. **能力指纹**：用一组「协议 × 传输层 × 加密方式」样本配置跑内核原生校验命令，比对 accepted 集合与 `kernel_state.json` 里记录的基线有没有变化。**accepted 集合变了就说明"最新支持的节点内容"变了**，需要同步更新 `layout.CAPS` 与节点转换逻辑

内核原生校验命令由 `test_nodes.check_config()` 按候选链自动识别并缓存（`v2ray test -c` / `xray -test -config` / `mihomo -t -f` / `sing-box check -c`），版本变了也不会一次性全哑。

退出码：`0` 无变化 / `1` 有新版本或能力变化 / `2` 检查失败。发现变化时脚本会自己往 `CHANGELOGS.md`（根目录）与 `Docs/known-issues.md` 追加记录。
