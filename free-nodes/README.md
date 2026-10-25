# 免费节点每日采集产物

由 WorkBuddy 定时任务「每日免费节点采集（v2ray/clash/singbox）」自动生成并推送到本仓库。

## 目录结构

```
free-nodes/
  <YYYY-MM-DD>/                 每日一份，按日期归档
    v2ray_sub.txt               base64 订阅（按 TCP 延迟升序），v2rayN/v2rayNG 直接导入
    clash.yaml                  Clash / mihomo 配置（含 PROXY 策略组）
    singbox.json                sing-box outbounds
    nodes_meta.json             每个节点的延迟 + 来源仓库
    report.md                   当日报告（延迟分布 / 协议分布 / 仓库质量排行）
    health_check.md             自检报告（结论 + 分级发现 + 待办清单）
    health_check.json           自检机读版
    tested/<core>/              各内核实测可用清单
      available_<core>.txt        该内核可用节点订阅
      available_<core>_list.txt   明文 URI 列表
    summary.md / summary.json   各内核测试数 / 可用数 / 可用率
  pool/                         跨天累积的可用节点池（pool_<core>.txt/json）
  seed_repos.json               仓库清单 + 质量评分（可用率 / 质量分 / 历史）
  collection_log.md             采集日志，每次运行追加一条
  review_log.md                 自检日志，每次运行追加一条
  <core> ∈ xray / v2ray / mihomo / singbox
```

## 约定

- **只保留最近 14 天**的日期目录，更早的会被自动清理，避免仓库无限膨胀；`pool/`、`seed_repos.json` 和两个日志文件长期保留。
- 免费节点时效极短，**当天导入当天用**。想要低延迟精品，直接导入 `pool/pool_<core>.txt`（跨天累积、已验证可用）。
- 本目录文件全部由脚本生成，无需手工编辑；如需改采集策略，改技能 `free-nodes-collector` 的参数或脚本。
