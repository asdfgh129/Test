# 每日自检检查项、输出与修复闭环

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

## 每日自检与自优化（health_check.py）

采集 + 验证跑完后必须跑一次自检。它不做修改，只做**诊断 + 给出可执行建议**，修复动作由 agent 决定。

```bash
python <free-nodes>/src/health_check.py --dir <输出根目录>            # 默认目标 1000 条
python <free-nodes>/src/health_check.py --dir <输出根目录> --skip-network   # 离线快速模式
```

### 检查项

| 类别 | 检查内容 | 严重度触发条件 |
|---|---|---|
| 产物 | `nodes/nodes_uris.txt` + 4 个 `nodes/*_sub.*` + `Docs/report.md` 是否齐全，四内核分流数是否合理 | 缺文件 = critical |
| 规模 | 去重后节点数 vs `--target-nodes` | <10% critical，<50% warn |
| 仓库效率 | 按「有产出 / 解析不到节点 / 下载失败 / 无候选文件」四类统计，产出率低则按主导失败类型给针对性建议 | 产出率 <10% critical |
| 来源稳定性 | 历史高贡献仓库本次是否 0 条，并标注原因（下载失败/解析失败/无候选） | 有掉线 = warn |
| README 采集 | 有多少仓库在 README 中识别到订阅链接、从中提取多少节点 | 一个都没识别 = warn |
| 延迟排序 | `nodes/nodes_meta.json` 是否生成、TCP 可达率、延迟中位数、订阅头部是否混入不可达节点 | 全不可达 critical，头部混入 warn |
| 仓库质量 | 已评分仓库数、可用率 ≥10% 的比例、长期 0 可用的仓库数 | 过半 0 可用 = warn |
| 节点池 | `nodes/pool/` 下 4 个池文件 + `pool_state.json` 是否存在、各内核池内节点数 | 池缺失/为空 = warn |
| 验证 | 各内核可用数、可用率、`nodes/available_*` 与 `Docs/summary.json` 是否一致、内核二进制是否在位 | 0 可用 = critical |
| 下载通道 | 探测 raw 直连 + 全部镜像前缀 + 全部 jsDelivr 边缘节点 | 镜像与 raw 全挂 critical，部分挂 warn，jsDelivr 四节点全挂 warn |
| 配额 | GitHub core / search 剩余、是否配置 token | 匿名且 core <20 = warn |
| 来源质量 | 单一服务器占比 >50% | warn |
| 趋势 | 与近 7 次中位数比较，跌幅 >60% | warn |
| 性能 | 采集耗时 >45 分钟 | warn |

### 输出

报告类全部位于输出根目录的 `Docs/`，**统一按日期倒序（最新小节在最前）**，累积保留最近 30 个小节：

- `Docs/health_check.md` — 结论 + 指标表 + 分级发现 + **待办清单**
- `Docs/health_check.json` — 机读版（供自动化判断）
- `Docs/known-issues.md` 末尾的「自检发现」区块 — 本次自检发现的问题（同一天重跑会替换当天小节，不会重复堆叠；上面的知识库条目不受影响）
- `Docs/review_logs.md` — 每次运行一行摘要，跨天可追溯

根目录的 `CHANGELOGS.md` 由人工/脚本在**修复或升级内核后**写入（`layout.append_changelog`），同样按日期倒序。

### 修复闭环（发现 critical/warn 时按此执行）

1. **读待办清单**，拿最靠前的 critical 项
2. **对照 `Docs/known-issues.md`** 找同类症状的已知根因（多数问题那里已有答案）
3. **定位到具体代码**：抓 1 个失败样本（仓库/URI/内核）单独复现，不要靠猜
4. **改脚本并单点回归**：用该样本验证修复确实生效（不能只看整体数字变化）
5. **重跑受影响环节**：解析类 → 重跑采集；验证类 → 重跑 `test_nodes.py`
6. **再跑 `health_check.py`**，确认该 finding 消失且未引入新问题
7. **记录**：向 `Docs/known-issues.md` 上方知识库按编号追加条目（新发现的现象/根因/修复/教训），自检结果由 `health_check.py` 自动写进同一个文件末尾的「自检发现」区块；根目录 `CHANGELOGS.md` 记「改了什么 + 验证结果」（都按日期倒序，同一天重跑替换当天小节）；行为变化同步更新本文件
8. **提交推送**：`src/publish_free_nodes.py --proxy auto`（路径限定只提交 free-nodes；脚本自身就在 src/ 里，无需同步/打包）
9. **汇报**：说明「发现什么 → 根因 → 改了什么 → 验证结果」

只改有证据支撑的地方。推测性问题先记进 `Docs/review_logs.md` 观察，不要凭感觉动参数。
