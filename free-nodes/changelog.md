# 变更与修复记录（时间倒序）

> 按日期倒序；包含脚本修复、参数调整、内核版本升级等

## 2026-10-25 布局重构与内核检查

### 输出布局重构：扁平 + 单文件制

- **动机**：每内核产出 `pool_<core>.txt` / `_list.txt` / `.json` 三件套，验证后再产出
  `available_<core>.txt` / `_list.txt` / `_clash.yaml` / `_singbox.json` 四件套，大半是冗余
- **改动**：
  - 节点文件统一为 `v2ray_sub.txt` / `xray_sub.txt` / `clash_sub.yaml` / `singbox_sub.json`，
    一内核一文件、只写该客户端能直接导入的格式；`nodes_uris.txt` 作为内部主清单（全量明文 URI）
  - 可用清单统一为 `available_v2ray.txt` / `available_xray.txt` / `available_clash.yaml` /
    `available_singbox.json`，取消跨内核格式转换（xray 的 REALITY 节点转成 clash 配置不保真）
  - 池统一为 `pool/pool_<core>.<ext>` 四个文件 + 一份共享 `pool/pool_state.json`（只存元数据）
  - 全部平铺在 `free-nodes/` 根目录，**不再按日期建子目录**（过期节点没有意义）
  - 新增 `layout.py` 集中定义命名/格式/能力矩阵/路径，`collect_nodes`、`test_nodes`、`pool`、
    `uplink`、`health_check`、`check_kernels` 全部改为依赖它，不再各自硬编码文件名

### 四内核能力分流（layout.CAPS）

- v2ray 与 xray 共用同一份源订阅，但按「代理协议 / 传输层 / REALITY / flow」分流：
  带 REALITY、VLESS flow、xhttp 的节点只进 `xray_sub.txt`（v2fly 不支持，写进去会让整份配置导入失败）
- clash 额外收 ssr / hysteria2 / tuic，singbox 额外收 hysteria2 / tuic，各自缺 kcp/quic 的差异也按矩阵过滤
- 本日实测分流结果：主清单 6632 条 → v2ray 5633 / xray 6419 / clash 6615 / singbox 6529

### 内核命名归一

- 对外统一 `v2ray` / `xray` / `clash` / `singbox`；`mihomo`、`meta` → `clash`，`v2fly` → `v2ray`，
  `sing-box`、`sb` → `singbox`。此前同一个 mihomo 内核既有 `pool_mihomo.txt` 又有 `pool_clash.yaml`，
  两份内容一样、名字不同

### md 日志改为时间倒序累积

- `report.md` / `summary.md` / `health_check.md` / `known_issue.md` / `changelog.md` /
  `collection_log.md` / `review_log.md` 统一由 `layout.upsert_section()` 写入：
  新小节插到顶部，同一天重跑**替换**当天小节（不会堆叠重复），超过 30 个小节从尾部丢弃

### 新增 check_kernels.py（内核版本 + 能力漂移检查）

- 比对本地二进制版本与 GitHub 最新 release（XTLS/Xray-core、v2fly/v2ray-core、
  MetaCubeX/mihomo、SagerNet/sing-box）
- 用「协议 × 传输层 × 加密方式」样本跑内核原生校验，比对 accepted 集合与 `kernel_state.json` 基线
- 本日实测：v2ray 5.53.0 / xray 26.10.21 / clash(mihomo) 1.19.33 / singbox 1.14.4 均为最新，
  能力指纹 10/12/14/14 项与基线一致

### 修复：自检误判与计数偏差（3 处）

1. **`health_check.read_sub_stats()` 只认 base64** → 传进去的是明文 `nodes_uris.txt`，
   base64 解码得到乱码、过滤后 0 行，自检报「本次采集到 0 条节点」critical（实际 6632 条）。
   改为先看明文里有没有 `://`，没有再尝试 base64 解码
2. **sing-box 计数比汇总多 1** → `available_singbox.json` 里除了节点还有一个内置
   `{"type":"direct"}` 出站，被当成节点计入。改为排除 `direct/block/dns/selector/urltest/tor`
3. **v2ray 版本查询 404** → `v2fly/v2fly-core` 这个仓库名调 `/releases/latest` 返回 404，
   正确的仓库是 `v2fly/v2ray-core`（tag `v5.53.0`）

验证：修复后自检从「1 critical / 2 warn」降到「0 critical / 1 warn」，剩下一项是镜像失效（见 known_issue）。
