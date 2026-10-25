# 定时任务 prompt（新版，待粘贴到自动化 a3d7bb22-948c-4326-b344-f4c5535ddcd0）

> 2026-10-25 整理。旧版 prompt 引用已删除的旧技能目录、`tools/publish_free_nodes.py`、
> `--test-limit 200` 旧测试参数与 `free-nodes\known_issue.md` 旧文件名，已不适用。
> 本会话无 automation_update 工具，无法直接改定时任务，请把下面全文粘贴到
> 自动化「任务指令」里（覆盖旧版）。定时任务名：每日免费节点采集（v2ray/xray/clash/singbox）。

---

按照 `C:\Users\bemin\WorkBuddy\Test\free-nodes\Skills\free-nodes-collector\SKILL.md` 的流程执行每日任务：内核检查 → 采集 → 验证 → 自检 → 按需修复 → 提交推送到 GitHub。发现可修的问题要自己修掉。

【固定路径（一律用绝对路径，禁止相对路径）】
- Python：`C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe`
- 技能定义（流程说明）：`C:\Users\bemin\WorkBuddy\Test\free-nodes\Skills\free-nodes-collector\SKILL.md`
- 脚本目录（全链路唯一事实来源）：`C:\Users\bemin\WorkBuddy\Test\free-nodes\src`
- 文档目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes\Docs`
- 工作区（git 仓库）：`C:\Users\bemin\WorkBuddy\Test`
- 输出根目录：`C:\Users\bemin\WorkBuddy\Test\free-nodes`
  **三分层布局，不带日期**——根目录只留 `README.md` + `CHANGELOGS.md`；节点产物在 `nodes/`；全部文档与日志在 `Docs/`；脚本在 `src/`。每次运行覆盖更新。不要创建、也不要保留任何 YYYY-MM-DD 子目录（过期节点没有意义）。
  日期只用于 md 日志的日期小节和提交信息，用 `date +%F` 取，不要自己推算。
- GitHub token：已存放在 `C:\Users\bemin\.workbuddy\data\free-nodes-tools\github_token.txt`（权限 600，**不在 git 仓库内**）。脚本会自动读取（优先级 `--token` > `GITHUB_TOKEN` 环境变量 > 该文件），**不需要也不要在命令行里传 token，更不要把 token 内容写进任何文件或汇报里**。带 token 后核心配额 5000/时、搜索 30/分。

【1. 内核版本与能力检查（先做，约 10~30 秒）】
```
C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\bemin\WorkBuddy\Test\free-nodes\src\check_kernels.py --root C:\Users\bemin\WorkBuddy\Test\free-nodes
```
- 对比四个内核（v2ray/xray/clash(mihomo)/singbox）本地版本与 GitHub 最新 release，并用「协议 × 传输层 × 加密方式」样本配置跑内核原生校验，比对 accepted 集合与 `src/kernel_state.json` 基线
- 退出码 0 = 无变化；1 = 有新版本或能力变化；2 = 检查失败
- 退出码 1 时：读输出的差异，判断是否影响节点处理逻辑（典型：Xray 移除 allowInsecure、v2fly 换校验命令、某内核新增/移除协议）。需要升级就 `--update` 重新跑一次；改了 `layout.CAPS` 或节点转换逻辑要写进根 `CHANGELOGS.md` 与 `Docs/protocol.md` §7 并在汇报里说明
- 退出码 2 不阻断后续采集，记进汇报

【2. 采集（不带内联测试）】
```
C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\bemin\WorkBuddy\Test\free-nodes\src\collect_nodes.py --out C:\Users\bemin\WorkBuddy\Test\free-nodes --readme-only --max-repos 80 --search-pages 2 --search-days 3 --readme-date-tolerance 0
```

关键行为（脚本已内置，不要绕过）：
- **上行通道（--uplink auto，默认）**：**搜索仓库地址与下载节点数据之前，先用「已验证可用的节点」自建本地代理内核**（按 clash → singbox → xray → v2ray 轮换，同一节点每个内核都试，探测 `https://github.com/` 或 `https://api.github.com/rate_limit` 拿到 2xx 才算通）；四内核都起不来才走直连；代理与直连都不通则等 10 分钟重试（`--uplink-wait 600 --uplink-retries 2`）。通道是全局 opener，所以**搜索 API 与节点下载都走它**，不只是下载。
  唯一的例外是「池与近期清单都为空」时无候选节点可起代理（首次运行/池被清空），此时会打印 `[uplink] 没有可用候选节点` 并降级直连——这不是故障，采集结束后会重新填池。
- **采集完毕会先停掉这个代理内核**，再进入下一步验证——不要干预，也不要让代理进程残留
- **README-only 模式（--readme-only）**：只跟随 README 里声明的订阅链接，不再扫描仓库目录
- **README 按内核分类**：README 里常按内核分列订阅（「Clash 订阅」「sing-box 配置」「V2ray 订阅」），脚本会识别链接归属内核，日志里打印 `[info] <core>: N 条节点来自 README 声明的 <core> 订阅，豁免能力预筛`。这类节点保证进对应内核文件，不受 `layout.CAPS` 保守预筛影响
- **README 按日期筛选（--readme-date-tolerance 0，即只取当天）**：日更仓库常按日期分列订阅，两种写法都认——链接自带日期（`.../2026-10-25/all.txt`）或有日期小标题（`### 2026-10-25` 下的链接）。只取当天；因日期不符被跳过的记 `-4` 状态（与「未声明订阅链接」区分）。整份 README 没提日期的按通用订阅全部保留。
  若某天发现大量仓库报 `-4`（例如凌晨跑、仓库当天还没更新），把该参数改为 `--readme-date-tolerance 1` 再跑一次即可，不要改脚本里的判定逻辑
- **四内核能力分流**：`nodes/v2ray_sub.txt` / `nodes/xray_sub.txt`（base64）、`nodes/clash_sub.yaml`、`nodes/singbox_sub.json`。v2ray 与 xray 共用同一份源订阅，带 REALITY / VLESS flow / xhttp 的节点只进 xray
- **仓库池已扩大**：26 组关键词 × 2 页（每页 100 条）× 三级扩量，`src/seed_repos.json` 上限 300 个仓库
- 三级采集扩量（目标 1000 条）、镜像自动探活 + 下载四级回退、TCP 延迟升序排序、按来源仓库统计可用率并回写 `src/seed_repos.json`

【2b. 验证（独立一步，全量策略）】
```
C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\bemin\WorkBuddy\Test\free-nodes\src\test_nodes.py --input C:\Users\bemin\WorkBuddy\Test\free-nodes --cores v2ray,xray,clash,singbox --full-below 3000 --max-test 3000
```
- **注意参数名**：`test_nodes.py` 用 `--full-below/--max-test`（不带 `--test-` 前缀）；`--test-full-below/--test-max-test` 是 `collect_nodes.py` 的透传参数名，传给 test_nodes.py 会直接报错退出
- 全量策略：每内核候选 ≤3000 全部实测；超过只测排序前 3000 个（排序 = 协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序）。`--limit/--min-available` 在全量模式下不生效，别传
- **时间预算（重要）**：单次自动化运行有 90 分钟硬上限，采集约 30~45 分钟、全量测试约 50~70 分钟、自检+发布约 7 分钟。若启动验证时距运行开始已超过 35 分钟，用 `--max-test 1500` 减半测试量——**优先保证发布成功，不要为多测而超时**（超时=整晚白干，池会跨天累积，不差这一晚）
- 每内核一个跨天可用节点池（`nodes/pool/`）+ 一份共享 `nodes/pool/pool_state.json`，验证结束自动更新

【3. 自检】
```
C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\bemin\WorkBuddy\Test\free-nodes\src\health_check.py --dir C:\Users\bemin\WorkBuddy\Test\free-nodes
```
读 `Docs/health_check.md`（结论 + 分级发现 + 待办清单）与 `Docs/health_check.json`。
注意：README-only 模式下「README 无订阅链接跳过」与「链接日期不是当天跳过」都是既定策略，不计入产出率分母，不要当故障。

【4. 有问题就修】
若自检给出 critical 或 warn，按 SKILL.md「修复闭环」执行：
- 对照 `Docs/known-issues.md` 找同类症状（第 9/9b/9c/9d 条是 README 采集缺失、延迟排序失效、仓库质量不落库、节点池不增长；第 10 条是验证时被节点劫持重定向；第 11 条是探测地址无区分度；第 12 条是 github.com 被重置与上行通道；第 13 条是 README-only 的取舍；第 14 条是可用数低于 10 时的自适应扩量；第 15 条是产物文件膨胀；第 16 条是内核升级导致「所有节点全死」；第 17 条是迁移脚本通配符与新命名撞车；第 18 条是自检统计函数读错格式；第 19 条是仓库质量分倒挂；第 20 条是 md 日志去重粒度；第 21 条是 README 按内核/按日期筛选的误判边界；第 28 条是目录布局三分层；第 29 条是全量测试策略；第 30 条是目录整合与 junction 兼容层；第 31 条是 90 分钟超时与测试量降级规则）
- 抓 1 个失败样本（仓库 / URI / 内核）单独复现，不要凭猜测改代码
- 改脚本后用该样本做单点回归，确认修复生效；重跑受影响环节（解析类→重跑采集，验证类→重跑 `src\test_nodes.py`）
- 再跑一次 `health_check.py`，确认 finding 消失且未引入新问题
- 记录：`Docs/known-issues.md` 追加条目；同时往 `Docs/known_issues.md` 和根 `CHANGELOGS.md` 按日期倒序写小节（按「日期+标题」去重，同一天不同主题并存；同一天同一标题重跑会替换）；采集执行情况写 `Docs/collection_logs.md`；观察项写 `Docs/review_logs.md`
- 行为有变化同步更新 `free-nodes/Skills/free-nodes-collector/SKILL.md`。**不要打包技能**（`package_skill.py` 已删除，`src/` 即唯一事实来源，提交推送即分发）；`__pycache__` 已被 .gitignore 全局忽略，无需清理
只改有证据支撑的地方；推测性问题记入 `Docs/review_logs.md` 观察，不要凭感觉调参数。
注意：每内核可用数个位数到十几个是免费节点的正常水位（探测地址要求真出境且走 HTTPS），不要为了数字好看换回 www.gstatic.com 或明文 http。
若自检报「某内核可用数 < 10 但候选已全部测完（exhausted=true）」，说明验证侧已尽力，属源池质量问题：不要靠继续加大测试量硬凑，也不要放宽探测地址；只在汇报里说明，必要时补充高 star 种子仓库。

【5. 提交并推送到 GitHub】
```
C:\Users\bemin\.workbuddy\binaries\python\versions\3.13.12\python.exe C:\Users\bemin\WorkBuddy\Test\free-nodes\src\publish_free_nodes.py --proxy auto --date <当天日期>
```

脚本行为：
- `--proxy auto`：先探测本机已有代理端口；没有就用**已验证节点自建本地代理**推送（只认 `https://github.com/` 通不通），推不动就换节点、换内核继续试（`--uplink-rounds 5`），全部失败最后才直连重试
- 清理 free-nodes 下历史遗留的日期目录（三分层布局下 `nodes/`、`Docs/`、`src/`、`Skills/`、`.workbuddy/` 永久保留）
- **只暂存 free-nodes 目录，并跳过凭据文件**；绝不提交工作区里的其他改动。仓库里还有用户的 C++ 项目（`Test\`、`Test.sln` 等），**严禁 git add -A / git add . / git commit -a**，也不要 reset / checkout / stash 用户的改动
- 提交信息：`chore(free-nodes): 更新 <当天日期> 免费节点订阅`
- 推送到 origin/master；失败会写 `.git\free-nodes-pending-push.json`，下次运行自动补推
- 退出码：0 = 成功（含"无变更"）/ 1 = push 失败但本地提交已保留 / 2 = git 操作出错

处理规则：
- 退出码 1：不要再手敲 git push 反复重试，也不要改 git 配置/remote；汇报里说明「已本地提交，待推送」并附失败原因首行
- 若 collect_nodes.py 退出码 3（本次 0 条且保留旧结果），跳过提交推送，只说明配额/网络情况

【6. 汇报】
说明：内核检查结果（有无新版本 / 能力指纹是否变化）、上行通道用的哪个内核+节点（若有）/ 是否降级直连、搜索战果（多少个关键词×几页、去重后多少仓库、最终扫描多少个）、唯一节点数、协议分布、四内核分流数（`nodes/` 下各 sub 文件各多少条）、执行到第几级采集扩量、TCP 可达率与延迟中位数、README 采集战果（多少仓库声明了订阅链接 / 提取多少节点 / 多少个因「README 无链接」跳过 / 多少个因「日期不是当天」跳过 / 各内核各多少条节点）、仓库可用率 Top3 与最差 1 个、各内核可用数（v2ray / xray / clash / singbox，并注明共测多少个、候选是否已测完 exhausted）、各内核池内节点数、自检结论（几 critical 几 warn）、产物路径（`C:\Users\bemin\WorkBuddy\Test\free-nodes\nodes\` 下的 v2ray_sub.txt / xray_sub.txt / clash_sub.yaml / singbox_sub.json、available_* 四件、pool\ 下四个池文件 + pool_state.json；`Docs\` 下 report.md / summary.md+json / health_check.md+json；根目录 CHANGELOGS.md；`Docs\known_issues.md`、`Docs\collection_logs.md`）。
再加上 GitHub 发布结果：提交 hash、推送是否成功（origin/master）、用的哪个代理内核+节点、失败原因与补推状态。
若做了修复，按「发现了什么 → 根因 → 改了什么 → 验证结果」说明；无需修复则明确写「本次自检未发现问题」。
若因配额导致节点数不足，说明配额余量（token 已配置，正常应为 5000/时），不要反复重试。

【附注】
- 定时任务自己的记忆文件（系统自动读写）在 `C:\Users\bemin\WorkBuddy\Test\.workbuddy\memory\automations\a3d7bb22-948c-4326-b344-f4c5535ddcd0\memory.md`；该路径经 junction 实际落在 `free-nodes\.workbuddy\memory\` 下，会随每晚发布提交入库，属预期
- `~/.workbuddy/skills/free-nodes-collector/` 是指向仓库的 junction 兼容层（scripts→src、references→Docs），旧路径引用不会炸，但真实内容只在仓库里
