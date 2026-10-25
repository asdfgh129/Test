# 免费节点每日采集产物

由 WorkBuddy 定时任务「每日免费节点采集（v2ray/xray/clash/singbox）」自动生成并推送到本仓库。

## 目录结构

**全部平铺在本目录下，不按日期分目录**——免费节点过期就没意义，留历史日期目录只会制造「看起来有、其实已死」的误导。每次运行覆盖更新。

```
free-nodes/
├─ 节点订阅（按内核实测输出，一内核一文件）
│   v2ray_sub.txt               base64 订阅 → v2rayN / v2rayNG
│   xray_sub.txt                base64 订阅 → Xray 系客户端（含 REALITY / flow / xhttp 节点）
│   clash_sub.yaml              Clash 配置   → Clash / mihomo
│   singbox_sub.json            sing-box outbounds → sing-box
│   nodes_uris.txt              明文主清单（全量唯一节点，延迟升序）
│   nodes_meta.json             每节点 TCP 延迟 + 来源仓库
│
├─ 已验证可用（四内核实测通过，格式同上）
│   available_v2ray.txt
│   available_xray.txt
│   available_clash.yaml
│   available_singbox.json
│
├─ 节点池（跨天累积、已验证可用，格式同上）
│   pool/
│     pool_v2ray.txt
│     pool_xray.txt
│     pool_clash.yaml
│     pool_singbox.json
│     pool_state.json           四内核共用的元数据（首见 / 最近通过 / 通过次数 / 最佳延迟）
│
├─ 报告与日志（统一时间倒序，新的在最前，保留最近 30 小节）
│   report.md                   采集报告（延迟分布 / 协议分布 / 仓库质量排行）
│   summary.md / summary.json   验证汇总（各内核测试数 / 可用数 / 可用率 / 扩量轮次）
│   health_check.md / .json     自检报告（结论 + 分级发现 + 待办清单）
│   known_issue.md              自检发现的问题（按日期累积）
│   changelog.md                修复与内核升级记录（按日期累积）
│   collection_log.md           每次运行一条（执行阶段 / 仓库明细 / 去重结果）
│   review_log.md               跨天摘要
│
├─ seed_repos.json              仓库清单 + 质量评分（可用率 / 质量分 / 历史）
├─ repo_quality.json            本次按仓库汇总的实测可用率 / 平均延迟 / 质量分
└─ kernel_state.json            四内核版本与能力指纹基线（check_kernels.py 用来判定漂移）
```

## 怎么选文件

| 你的客户端 | 直接用 |
|---|---|
| v2rayN / v2rayNG | `v2ray_sub.txt` |
| Xray 系（Nekoray / v2rayN 的 Xray 内核） | `xray_sub.txt`（比 v2ray 多 REALITY / flow / xhttp 节点） |
| Clash / mihomo / Verge / FlClash | `clash_sub.yaml` |
| sing-box | `singbox_sub.json` |

## 约定

- **`*_sub.*` 与 `available_*` 的区别**：前者是「采集到的全部去重节点」（含尚未验证、已失效的），后者是「刚实测通过的」。要稳定就用 `available_*` 或 `pool/`。
- **`pool/` 是精品池**：跨天累积、多次验证通过、按通过次数与延迟排序，上游停更或当天采集失败时仍有兜底。
- 免费节点时效极短，**当天导入当天用**。
- `v2ray` 与 `xray` 共用同一份源订阅，但按各自能力分流：REALITY、VLESS flow、xhttp 类节点只出现在 `xray_sub.txt`（v2ray 官方内核不支持，写进去会导致整份配置导入失败）。
- 本目录所有文件由脚本生成，无需手工编辑；要改采集策略请调整技能 `free-nodes-collector` 的参数或脚本。
