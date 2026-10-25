# 项目长期记忆

## 免费节点每日采集（自动化 a3d7bb22-948c-4326-b344-f4c5535ddcd0，每天 22:00）

- 产出目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes\` —— **三分层布局，不分日期**
  （根目录只留 `README.md` + `CHANGELOGS.md`；`nodes/` 订阅+available+nodes_uris/nodes_meta+pool/；
  `Docs/` 全部文档与报告（protocol/proxy/sources/tools-setup/known-issues 知识库 +
  known_issues/collection_logs/review_logs 复数日志 + report/summary/health_check）；
  `src/` **采集/验证/发布全链路脚本的唯一事实来源**（12 文件：9 脚本 + publish_free_nodes.py
  + seed_repos/repo_quality/kernel_state json）；`Skills/free-nodes-collector/SKILL.md` 技能定义；
  `.workbuddy/memory/` 项目记忆（已纳入 git 跟踪）。过期节点没有意义，禁止再建 YYYY-MM-DD 子目录）
- 发布脚本：`free-nodes/src/publish_free_nodes.py`（只暂存 free-nodes，绝不 `git add -A`；
  `--workspace` 默认脚本上溯三级（src → free-nodes → 仓库根）；`--skill-scripts` 默认即自身所在目录；
  push 失败写 `.git/free-nodes-pending-push.json`，下次补推）
- 技能 junction 兼容层（2026-10-25 建）：`~/.workbuddy/skills/free-nodes-collector/` 的
  `scripts` 是指向 `free-nodes/src` 的目录 junction、`references` 指向 `free-nodes/Docs`，
  SKILL.md 是仓库版副本。**真实内容只在仓库里，改完即生效，零同步**；
  该目录仅为仍引用旧路径的定时任务 prompt 提供路径兼容，技能列表已不再发现它（代价可接受）
- 内核在 `~/.workbuddy/data/free-nodes-tools/bin`（查找顺序：环境变量 → 该目录 → 已失效的 legacy 路径）
- 采集策略：`--readme-only`（只跟随 README 声明的订阅链接，不扫仓库目录）
- **README 订阅链接按内核 + 按日期取数**（用户明确要求）：
  - 识别链接归属内核（v2ray/xray/clash/singbox），命中后该链接节点保证进对应内核文件
  - README 按日期分列订阅时**只取当天**（`--readme-date-tolerance 0`）；
    整份 README 没提日期的按通用订阅全部保留
- 验证策略（2026-10-25 起，用户要求夜间全量）：**每内核候选 ≤3000 全部实测，
  >3000 只测排序前 3000 个**（`--test-full-below 3000 --test-max-test 3000`，
  常量 FULL_BELOW/MAX_TEST 集中在 layout.py，两值相同；上限曾笔误写成 30000，用户当晚纠正为 3000；
  排序 = 协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序）；
  summary 里 `exhausted=true` 表示候选已全部测完，此时不要再加测试量、也不要放宽探测地址。
  旧模式（`--no-full-test` 回退「可用数 <10 沿序追加，上限 limit×5、预算 1800s」）仅供对比
- 仓库池：26 组关键词 × 2 页（100 条/页）× 三级扩量，`src/seed_repos.json` 上限 300 个
- **自动化 prompt 更新受限**：本会话无 automation_update 工具（ToolSearch 也搜不到），
  定时任务 prompt 仍是旧版（引用旧技能目录路径、`tools/publish_free_nodes.py`、
  `--test-limit 200 --test-min-available 10` 旧测试参数、`free-nodes\known_issue.md` 旧文件名）。
  已准备好新版 prompt 文本待用户手工粘贴；junction 兼容层保证旧路径暂时不炸

## 四内核协议能力（2026-10-25 实测校准，详见 Docs/protocol.md）

- 能力矩阵 `layout.CAPS` 是唯一事实来源（test_nodes 分流与 uplink 的 `_cores_for` 都读它）
- **能力判定三原则**（用户两次质疑后沉淀）：① grep 二进制**文件本身**
  （`xray.exe | grep` 扫的是进程 stdout，必漏检，必须 `grep -a` 文件）；
  ② 协议名不能按字面猜（Xray 的 Hysteria2 叫 `hysteria` + `version:2`，名字里没有 "2"）；
  ③ config check 过 ≠ 装填对 ≠ 支持，必须 E2E 实测兜底
- hysteria2 四内核均支持（v2fly 5.x 全系、Xray ≥ v26.1.23）：v2ray 用
  `protocol:hysteria2` + 传输层 `hy2Settings.password`；xray 用 `protocol:hysteria`
  + `settings.version:2`（address/port 平铺）+ 传输层 `hysteriaSettings.auth`；
  xray 另支持 salamander 混淆与 udphop 端口跳跃
- xray hysteria2 回环 E2E 未过（回环服务端 SNI 选证书怪象），**真实节点未端到端验证**：
  线上若仅 xray 失败而其他内核可用，优先怀疑 xray 侧配置/兼容，别急着判节点不可达
- 变更协议能力时的固定同步链：layout.CAPS → test_nodes 转换器 → protocol_check 用例 →
  protocol.md（仅 `Docs/protocol.md` 一份，仓库内即唯一副本）→ `Skills/free-nodes-collector/SKILL.md` → known-issues

## GitHub token（凭据，勿泄露）

- 存放：`C:\Users\bemin\.workbuddy\data\free-nodes-tools\github_token.txt`（权限 600，
  **不在 git 仓库内**；`.gitignore` 已加 `github_token.txt` 兜底）
- 查找链：`--token` → `GITHUB_TOKEN`/`GH_TOKEN` 环境变量 → 上述文件
- 配额：带 token 核心 5000/时、搜索 30/分；匿名只有 60/时、10/分
- **日志与汇报只允许打印打码形式（前 4…后 4），任何情况下不得输出完整 token**

## 网络环境事实（重要）

- `github.com:443` 曾长期被阻断（连接重置）；`api.github.com`、`codeload.github.com` 可直连；
  `raw.githubusercontent.com` 不可直连，靠镜像（gh-proxy.com / gh-proxy.org / gh.monlor.com 等，失效率高）
- 因此 GitHub 采集与 push 都走 **自建代理**：`scripts/uplink.py` 用池内已验证节点起内核
  （clash→singbox→xray→v2ray 轮换），探测 `https://github.com/` 或
  `https://api.github.com/rate_limit` 拿 2xx 才算通；四内核全不通才直连
- 通道是全局 opener，所以**搜索 API 与节点下载都走它**，不只是下载
- 池为空时无候选节点可起代理（首次运行），会降级直连 —— 属物理限制，不是故障
- 推送探测只认 `https://github.com/`（api 通不代表能 push）

## 仓库约定

- git 身份：`bemin <xiaoxuefeng@msn.com>`（仓库级配置）
- 仓库里同时有用户的 C++ 项目（`Test/`、`Test.sln`），自动化只允许路径限定的 add
- `free-nodes/.gitattributes` 用 `* -text` 防止 autocrlf 改写订阅文件
- **路径单一事实来源 = `free-nodes/src/layout.py`**（sub_path/avail_path/pool_path/uris_path/
  meta_path/report_path/summary_path/health_path/issue_path/seed_file_path 等助手），
  全脚本禁止硬编码 join；改目录布局只改 layout.py + `migrate_legacy_flat()`
- md 日志去重粒度：`Docs/report`/`Docs/summary`/`Docs/health_check` 按**日期**替换；
  根 `CHANGELOGS.md`/`Docs/known_issues.md` 按**日期+标题**替换（一天多事件并存）
- 仓库根 `.workbuddy` 是指向 `free-nodes/.workbuddy` 的 junction（宿主 memory 系统固定读
  `Test/.workbuddy/memory/`，靠它不断链）；`.gitignore` 用根锚定 `/.workbuddy/`，
  所以只有 free-nodes/.workbuddy 入库；`__pycache__/`、`*.pyc` 已全局忽略
- 调试产物（hysteria2 回环测试的 `_san_*.pem`、`tmp_xray_hy2_*.py`）在
  `~/.workbuddy/data/free-nodes-tools/debug/`，**绝不入公开仓库**
