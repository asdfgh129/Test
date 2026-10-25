# 免费节点每日采集产物

由 WorkBuddy 定时任务「每日免费节点采集（v2ray/xray/clash/singbox）」自动生成并推送到本仓库。

## 目录结构

**根目录只放 README 与 CHANGELOGS；节点、文档、脚本、技能各归各的目录**——免费节点过期就没意义，
所有节点文件不按日期分目录，每次运行覆盖更新。

```
free-nodes/
├─ README.md                  本文件
├─ CHANGELOGS.md              修复与内核升级记录（按日期倒序累积）
│
├─ nodes/                     生成的节点信息
│   ├─ v2ray_sub.txt          base64 订阅 → v2rayN / v2rayNG
│   ├─ xray_sub.txt           base64 订阅 → Xray 系客户端（含 REALITY / flow / xhttp 节点）
│   ├─ clash_sub.yaml         Clash 配置   → Clash / mihomo
│   ├─ singbox_sub.json       sing-box outbounds → sing-box
│   ├─ nodes_uris.txt         明文主清单（全量唯一节点）
│   ├─ nodes_meta.json        每节点 TCP 延迟 + 来源仓库
│   ├─ available_v2ray.txt    已验证可用（四内核实测通过，格式同上）
│   ├─ available_xray.txt
│   ├─ available_clash.yaml
│   ├─ available_singbox.json
│   └─ pool/                  节点池（跨天累积、已验证可用，格式同上）
│       ├─ pool_v2ray.txt
│       ├─ pool_xray.txt
│       ├─ pool_clash.yaml
│       ├─ pool_singbox.json
│       └─ pool_state.json    四内核共用的元数据（首见 / 最近通过 / 通过次数 / 最佳延迟）
│
├─ Docs/                      文档（报告与日志统一时间倒序，新的在最前，保留最近 30 小节）
│   ├─ protocol.md            四内核解析规范与实测校准报告
│   ├─ proxy.md               自建代理与节点测试链路说明
│   ├─ known-issues.md        踩坑知识库（现象 / 根因 / 修复 / 教训）
│   ├─ sources.md             种子仓库来源与维护建议
│   ├─ tools-setup.md         四内核二进制部署 / 升级方法
│   ├─ report.md              采集报告（延迟分布 / 协议分布 / 仓库质量排行）
│   ├─ summary.md / .json     验证汇总（各内核测试数 / 可用数 / 可用率 / 测试策略）
│   ├─ health_check.md / .json 自检报告（结论 + 分级发现 + 待办清单）
│   ├─ known_issues.md        自检发现的问题（按日期累积；与 known-issues.md 知识库是两个文件）
│   ├─ collection_logs.md     每次运行一条（执行阶段 / 仓库明细 / 去重结果）
│   └─ review_logs.md         跨天摘要
│
├─ src/                       脚本 + 采集配置/状态（全链路脚本的唯一事实来源，直接在此改）
│   ├─ collect_nodes.py       采集（GitHub 搜索 → README 订阅链接 → 提取 → 去重 → 四内核分流）
│   ├─ test_nodes.py          可用性验证（TCP 预筛 → 逐内核实测 → 池）
│   ├─ layout.py              布局 / 能力矩阵 / md 日志
│   ├─ pool.py / uplink.py    节点池 / 自建代理上行通道
│   ├─ health_check.py        自检
│   ├─ check_kernels.py       内核版本与能力指纹检查
│   ├─ protocol_check.py      协议一致性回归
│   ├─ publish_free_nodes.py  提交并推送到 GitHub
│   ├─ seed_repos.json        仓库清单 + 质量评分（可用率 / 质量分 / 历史）
│   ├─ repo_quality.json      本次按仓库汇总的实测可用率 / 平均延迟 / 质量分
│   └─ kernel_state.json      四内核版本与能力指纹基线（check_kernels.py 用来判定漂移）
│
├─ Skills/                    技能定义（工作流 / 参数表 / 排查入口；脚本与文档分别见 src/ 与 Docs/）
│   └─ free-nodes-collector/
│       └─ SKILL.md
│
└─ .workbuddy/                项目记忆（纳入 git 跟踪）
    └─ memory/
        ├─ MEMORY.md          长期约定（布局 / 策略 / 路径事实来源）
        └─ YYYY-MM-DD.md      每日工作日志
```

## 怎么选文件

| 你的客户端 | 直接用 |
|---|---|
| v2rayN / v2rayNG | `nodes/v2ray_sub.txt` |
| Xray 系（Nekoray / v2rayN 的 Xray 内核） | `nodes/xray_sub.txt`（比 v2ray 多 REALITY / flow / xhttp 节点） |
| Clash / mihomo / Verge / FlClash | `nodes/clash_sub.yaml` |
| sing-box | `nodes/singbox_sub.json` |

## 约定

- **`nodes/*_sub.*` 与 `nodes/available_*` 的区别**：前者是「采集到的全部去重节点」（含尚未验证、已失效的），后者是「刚实测通过的」。要稳定就用 `available_*` 或 `nodes/pool/`。
- **`nodes/pool/` 是精品池**：跨天累积、多次验证通过、按通过次数与延迟排序，上游停更或当天采集失败时仍有兜底。
- 免费节点时效极短，**当天导入当天用**。
- `v2ray` 与 `xray` 共用同一份源订阅，但按各自能力分流：REALITY、VLESS flow、xhttp 类节点只出现在 `xray_sub.txt`（v2ray 官方内核不支持，写进去会导致整份配置导入失败）。
- 验证默认**全量测试**（晚间时段）：某内核候选 ≤ 3000 个全部实测，超过则只测排序前 3000 个（协议交错 + 仓库质量优先 + CF 前置排最后 + TCP 延迟升序）。
- 本目录所有文件由脚本生成，无需手工编辑；要改采集策略请直接调整 `src/` 里的脚本或参数——`src/` 就是脚本的唯一事实来源，不存在第二份副本。
