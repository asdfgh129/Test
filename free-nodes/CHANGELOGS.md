# 变更与修复记录（时间倒序）

> 按日期倒序；包含脚本修复、参数调整、内核版本升级等

## 2026-10-27 一夜跑三个窗口：`--resume-tested` 让验证接力不重测、不冲掉当日可用

- **背景**：平台 90 分钟硬上限改不掉，一个窗口测不完四个内核。改为 22:00 采集+验证 →
  23:45 续跑 → 01:30 再续跑，每个窗口都能把已测结果落盘并发布
- **`--resume-tested`（默认关）**：跳过本日已测过的 `host:port`（`nodes/tested_state.json`
  按日期自动重置），只测排序里的下一批候选；否则第二个窗口从头部重测，90 分钟全是重复劳动
- **当日可用并回**：续跑时把前面窗口已验证可用的节点并回 `available_<core>.*` 与汇总。
  实测踩到过：第二轮测 96 个全不可用，第一轮的 20 个可用节点被覆盖清零
- **汇总累积**：`Docs/summary.*` 合并同一天前序窗口的内核结果，换个 `--cores` 跑不会把
  别的内核从汇总里抹掉。`tested` 记本日累计、`partial` 只针对本窗口
- **口径**：路径助手 `layout.tested_state_path()` 新增（路径单一事实来源不变）；
  `summary.json` 补 `policy` 字段，合并后「轮次」列不再退化成数字
- 详见 `Docs/known-issues.md` 第 37 条；`Skills/free-nodes-collector/SKILL.md` 已同步

## 2026-10-27 验证侧不再拍脑袋限测试量：增量落盘 + `--time-budget`（用户要求「不要设限」）

- **删掉自定的 35 分钟降级规则**：那条「超过 35 分钟就 `--max-test 600`」是我们自己写在 prompt 里的，
  实测吞吐对不上（600 个/内核要 40 分钟），已作废；测试量不再设人为上限
- **平台 90 分钟硬上限留下，但不再是致命伤**：`test_nodes.py` 原先只在四核全跑完后才写
  `summary.*` 与 `pool_state.json`，被强杀等于白干。现在**每个内核结束立即增量落盘**，
  被砍最多丢当前内核
- **新增 `--time-budget`（默认 0 = 不限）**：主动收尾用，到期停止提交新节点、跳过未开始的内核，
  汇总里标注「本轮未跑完（主动收尾，不是失败）」，下次 `--cores <剩余>` 补跑；
  `summary.json` 新增 `sampled` / `partial` 字段
- **顺手修两个自己引入的坑**：`Executor.map` 一次性吃空迭代器（预算检查失效，改按块提交）；
  `for c in ...` 覆盖了模块别名 `c`（`collect_nodes`）导致汇总写入抛 AttributeError
- 详见 `Docs/known-issues.md` 第 36 条

## 2026-10-26 README 反引号/加粗裸链接被吸进 URL 导致 404（已修复）

- **问题**：`URL_RE` 的排除字符集没有反引号和星号，中文 README 常见的
  `` `https://...` ``（行内代码）与 `**https://...**`（加粗）写法会把装饰符带进 URL 尾部，
  下载必然 404。本次采集命中 2 例（`ts-sf/fly` 的 `clash`、`tglaoshiji/nodeshare` 的 `freenode`），
  日志里表现为「README 声明的链接全部下载失败」
- **改动**：`collect_nodes.py` 的 `URL_RE` 排除集加 `` ` ``/`*`/`|`；
  `_strip_url_tail()` 的 rstrip 集合同步扩充
- **验证**：单点回归 `ts-sf/fly` README，链接目标由 `.../main/clash`` ` ``（404）
  变为干净的 `.../main/clash`，并正确识别为 `kernel=clash` 订阅
- 详见 `Docs/known-issues.md` 第 35 条

## 2026-10-26 上行通道前移 + 推送不探测本机端口 + known-issues 合并（用户三点要求）

- **第 1 步就自建代理**：`check_kernels.py` 原先完全没有代理能力（`latest_release(proxy=...)`
  参数留着没人传），查 `api.github.com` 只能指望直连。现在默认 `--uplink auto`：
  用已验证节点建通道 → 查版本 → 结束关闭（独立运行无残留）
- **代理只建一次**：`check_kernels` 拆出 `run_check() -> (rc, uplink_mod, handle)`，
  `collect_nodes.py --check-kernels` 在同一进程里先跑检查、再接管该通道采集。
  原因：本机 job 限制会在命令结束时回收 detached 子进程（`CREATE_BREAKAWAY_FROM_JOB`
  被拒 WinError 5），跨进程复用只能尽力而为 → 详见 known-issues 第 34 条
- **版本查询必须带 token**：走免费节点代理时出口 IP 与他人共享，匿名配额（60/时）
  几乎必然 403（实测四核全被限流），`latest_release` 现在带 `Authorization`
- **推送不探测本机端口**（用户要求）：`publish_free_nodes.py --proxy auto` 删掉
  `PROXY_CANDIDATES` / `detect_proxy()`，直接用已验证节点自建（先尝试接管登记在案的通道）；
  `--proxy http://...` 仍可指定现成代理
- **known-issues 合并为一个文件**（用户要求）：`Docs/known-issues.md`（人工知识库）与
  `Docs/known_issues.md`（自检表格）名字只差一个连字符、内容还会互相抄串。现合并为单文件：
  上方编号知识库，末尾「自检发现」区块（条目用 `### 日期 标题`，`layout.append_issue`
  独立插入、不碰知识库条目、幂等去重、最多 30 条）
- 顺手修：`collect_nodes.py` 空结果时 `uniq[0]` 抛 `IndexError`（预算过短 / 来源全失败时整轮失败）

## 2026-10-25 内核检查与升级

- v2ray 新增支持：hysteria2/-/tls、vless/tcp/vision（可考虑放宽 layout.CAPS）
- xray 新增支持：hysteria2/-/tls（可考虑放宽 layout.CAPS）

## 2026-10-25 扩大仓库池 + token 接入 + README 按内核/日期取数

- **token 接入**（用户提供）：新增 `load_github_token()` 查找链
  `--token` → `GITHUB_TOKEN`/`GH_TOKEN` 环境变量 → 本地凭据文件
  `~/.workbuddy/data/free-nodes-tools/github_token.txt`（权限 600，不在仓库内，
  `.gitignore` 另加 `github_token.txt` 兜底）。实测配额 **核心 5000/时、搜索 30/分**
  （匿名是 60/时、10/分）。日志只打印 `前4…后4` 打码形式
- **仓库池扩大**：
  - `SEARCH_QUERIES` 10 组 → **26 组**，补上按内核（mihomo/xray）、按协议
    （hysteria2/tuic/reality/vmess/trojan/ss）、中文（免费机场/节点分享/订阅链接）、
    日更型（daily free nodes）四类
  - `search_repos()` 支持翻页：每页 100 条 × `--search-pages`（默认 2）
  - 限速按身份自适应：带 token 2.2s/请求，匿名 6.5s
  - `--max-repos` 30 → **80**，`--max-seeds` 15 → **30**
  - 阶段 2 时间窗从「前一天」放宽到 `--search-days`（默认前 **3** 天）
  - `seed_repos.json` 上限 80 → **300** 个仓库
- **README 按内核分类**：新增 `KERNEL_LINK_HINTS`，从文件名 → 目录名 → 链接文字 → 域名
  逐级识别 v2ray/xray/clash/singbox。识别出的节点写入对应内核文件时**豁免 CAPS 预筛**
  （作者已声明格式，CAPS 的保守规则可能把真能用的判死）
- **README 按日期筛选**：新增 `DATE_TOKEN_RE` / `DATE_HEADING_RE`，两种写法都认——
  链接自带日期（`.../2026-10-25/all.txt`、`Nodes-20261025.txt`）和有日期小标题
  （`### 2026-10-25` 下的链接，回溯 4000 字符取最近标题）。只取当天
  （`--readme-date-tolerance` 默认 0）。**整份 README 没提日期 → 全部保留**，
  否则非日更仓库会被一刀砍死。因日期跳过记 `-4` 状态，与「未声明链接」区分
- **补 sing-box 反解**（`singbox_to_uri()`）：旧代码对 `kind=singbox` 直接返回空串，
  导致 sing-box JSON 订阅的节点进不了 `nodes_uris.txt` 主清单 → **完全不参与可用性验证**。
  现覆盖 ss/trojan/vless/vmess/hysteria2/tuic 六种，其余返回 None

**验证结果**（隔离目录试跑，12 分 48 秒，不污染正式产物）：
- 搜索：26 组关键词 × 1 页 = 26 次请求，去重 **396** 个仓库（阶段 1）；
  阶段 2 放宽至 2026-10-22 起，去重 **689** 个仓库
- 日期筛选真实命中：`VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy` 有 **17 个链接
  因日期不是当天被跳过**，保留 10 个当天链接采到 255 条
- 主清单 7189 条 → v2ray 6841 / xray 7110 / clash 7167 / singbox 6953
- sing-box 反解：6 种协议往返一致（server/port 不变）；四内核原生校验
  vless(reality/ws)/vmess 全接受、hysteria2 只有 clash/singbox 能构造（符合能力边界）；
  端到端验证 sing-box 来源节点能进主清单与四个 sub 文件

## 2026-10-25 md 日志去重粒度修正

- **问题**：`upsert_section()` 按「日期前缀」删旧小节，同一天写第二条不同主题时，
  会把当天先写入的记录整段抹掉（本次差点丢掉「布局重构与内核检查」整节，已用 git 恢复）
- **改动**：加 `match_heading` 开关——`report/summary/health_check` 仍按日期替换（当天一份结论），
  `changelog/known_issue` 改为按「日期 + 标题」替换（一天多事件并存）

## 2026-10-25 修复仓库质量分倒挂

- **改了什么**：`collect_nodes.quality_score()`
  - 可用率 ≤0 或 `avg_latency` 为空时直接 `return rate*70`（延迟项 0），不再把「无数据」当满分
  - 延迟归零点 1500ms → 5000ms（`100 - latency/50`），让 30 分权重真正起作用
- **回填结果**（16 个仓库）：

  | 仓库 | 可用率 | 旧分 | 新分 |
  |---|---|---|---|
  | snakem982/proxypool | 61.9% | 43.3 | **63.8** |
  | Pawdroid/Free-servers | 65.0% | 45.5 | 54.9 |
  | 0xRadikal/Free-v2ray-Configs | 11.4% | 8.0 | 29.0 |
  | Epodonios/v2ray-configs | 2.6% | 13.9 | 26.4 |
  | igareck/vpn-configs-for-russia | 33.3% | 23.3 | 23.3 |
  | MatinGhanbari 等 5 个 0% 仓库 | 0.0% | 30.0 | **0.0** |

- **验证**：排序恢复单调（可用高的分高、0 可用的垫底）；`repo_sort_key` 未改动，
  采集优先级行为不变（仍按 `avail_rate`）
- 记录：`references/known-issues.md` 第 19 条；`SKILL.md` 质量分公式说明同步更新

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
