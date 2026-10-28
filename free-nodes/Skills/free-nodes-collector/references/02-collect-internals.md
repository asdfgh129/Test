# README 订阅采集、列目录通道、下载回退链、候选文件识别

> 本文件是 `free-nodes-collector` 的细节参考，从主 SKILL.md 拆出以降低常驻上下文。
> 触发条件见主 SKILL.md 末尾的「参考文件索引」。内容与拆分前逐字一致。

## README 订阅链接采集

**每个仓库先读 README，再挑文件。** 大量仓库把真正的订阅文件写在 README 里（`clash 订阅`、`sing-box 配置`、一键导入链接），这些文件名往往不带 sub/node 关键字，靠目录扫描挑不出来。

流程（`collect_from_readme`）：

1. 在文件树里找 README（根目录优先，兼容 `README_CN.md` / `readme.rst`）
2. 抽取链接：markdown `[x](url)`、HTML `href`、`clash://install-config?url=` 一键导入链接、裸链接
3. 分类：**同仓库文件** → 转成仓库内路径下载；**别的仓库文件** → 自动换成 `raw.githubusercontent.com` 地址（走镜像回退链）；**自建订阅接口** → 直接下载
4. **识别内核**（`KERNEL_LINK_HINTS`）：从文件名 → 目录名 → 链接文字 → 域名逐级判断，命中 `v2ray`/`xray`/`clash|mihomo`/`singbox` 就记下归属；认不出记为「通用」。作用有两个：日志能说清每个内核各采多少；**该链接的节点写入对应内核文件时豁免 `layout.CAPS` 预筛**（作者已声明格式，CAPS 的保守规则可能把真能用的判死）
5. **按日期筛选**（用户策略：只取当天）：两种写法都认——① 链接自带日期（`.../2026-10-25/all.txt`、`Nodes-20261025.txt`）；② 有日期小标题（`### 2026-10-25` 下面才列当天链接）。只保留 `[今天 - --readme-date-tolerance, 今天]` 内的；**整份 README 完全没提日期 → 视为通用订阅，全部保留**（否则非日更仓库会被全砍）。因日期跳过的数量单独记 `-4` 状态，日志里与「未声明链接」区分开
6. 过滤噪声：徽章/图片、仓库主页、`/issues`、`/releases`、`/forks`、`star-history`、`jsdelivr.com/package`、`*.github.io` 页面、`example/template/sample` 示例配置
7. 同一文件的多个 CDN 写法（raw / cdn / fastly / testingcf / gcore）按「仓库+路径」归一，只下一次
8. 单仓库最多跟随 10 个链接；链接**并发 4 路**下载，单仓库总预算 90 秒（超预算放弃剩余链接，避免一个慢站拖住整轮采集）；README 已拿到节点时少扫 1 个文件，把时间留给下一个仓库

实测收益：`Epodonios/v2ray-configs` README 一条 `All_Configs_Sub.txt` 就是 7600+ 条；`mahdibland/V2RayAggregator` README 指向 4 个外部仓库订阅，一次拿到 1.2 万条。README 链路是否正常，自检的「README 采集」项会直接告警。

### 列目录通道（不消耗 GitHub 配额）

列仓库文件列表**默认走 jsDelivr data API**（`data.jsdelivr.com/v1/packages/gh/<repo>@<branch>?structure=flat`），
返回完整扁平文件树且**不计入 GitHub 核心配额**——匿名配额只有 60 次/小时，列目录曾是采集卡住的主因。
jsDelivr 不可用时才回落 GitHub contents API（此时只列根目录，消耗配额）。

### 下载回退链（内置，自动处理 raw 直连失败）

`raw.githubusercontent.com` 直连经常被网络重置。脚本内置四级回退，**按序尝试、第一个成功即用**：

1. `raw.githubusercontent.com` 直连
2. **raw 镜像代理前缀**（形式 `https://gh-proxy.com/<完整 raw URL>`）
3. jsDelivr CDN（`@main` / `@master` 分支 × 各边缘节点）
4. GitHub contents API（base64，消耗核心配额，最后手段）

大文件（>2MB）走镜像极易被截断，这类文件把 jsDelivr 提到镜像之前，超时也放宽到 90s。

**通道自动探活**（每轮采集开始时执行一次，约 10s；触发备用补位时约 +12s）：
- 探测 raw 直连、全部镜像前缀、全部 jsDelivr 边缘节点，结果写入
  `~/.workbuddy/data/free-nodes-tools/mirrors_state.json`（有效期 24h）
- **探活后只用活着的通道**：死镜像会被整体踢出下载链，而不是"排到后面"——
  否则每个下载失败的文件都要在 N 个死镜像上各等一次超时（5 个死镜像 ≈ 100s/文件）
- raw 直连已知不通时排到最后，省掉每个文件一次 TLS 失败等待
- 全部镜像死掉不算故障：自动退回 raw 直连 + jsDelivr 两路
- **备用候选自动补位**：主清单存活镜像 <2 个时，补测 `MIRROR_SPARE_CANDIDATES`
  （只收「域名能解析、当前被墙/限流」的站点，DNS 不存在的域名不进池），
  救回的并入可用清单并写进状态文件。公共代理域名会成批烂掉——2026-10-24 实测
  13 个候选只剩 1 个活、其余多为 DNS 解析失败，靠补位恢复到了 3 个
- 跳过探活用 `--no-mirror-check`；自检结果里的「下载通道」项与这份状态一致

两个清单的性质不同，别混用：
- `DEFAULT_MIRROR_PREFIXES` / `JSDELIVR_HOSTS` 是**候选池**，公共代理存活率随出口网络剧烈变化
  （同批域名实测 1/11 ~ 7/11），不能当可信清单
- `get_mirror_prefixes()` / `get_cdn_hosts()` 返回**当前可用**的，下载链只用这个
- 但 README 链接归一化（`_repo_path_from_url`）必须用 `_base_mirrors()` 全量候选，
  否则失效镜像上的链接认不出来，同一文件会被重复下载

**jsDelivr 不能写死单域名**：`cdn.jsdelivr.net` 在部分网络被 DNS/SNI 阻断，
而 `fastly.` / `gcore.` / `testingcf.` 三个边缘节点仍可取回同一份内容。
镜像通道不会携带 GitHub Token（避免凭据泄漏给第三方镜像）。

### 候选文件识别（决定「这个仓库有没有节点」）

三层判定，逐层放宽：

1. **根目录文件**：扩展名命中 `CANDIDATE_EXT`（`.txt/.yaml/.yml/.json/.list/.log`），
   或命中 `BARE_SUB_NAMES` 的无扩展名裸文件（`clash`/`v2`/`configs`/`sub` 等，要求 ≥4KB）
2. **子目录文件**：顶层目录名命中 `is_subdir_hint()`（英文锚定 + 中文/内核名包含匹配，
   覆盖 `Mihomo内核系`、`节点订阅` 这类命名），**不限层级**（`sub/raw/01.yaml` 这种两层布局很常见）
3. **进目录扫描**：若文件树来自 contents API 且只有 `dir` 条目（子项根本没列出来），
   才对命中提示词的目录付配额真进一次

**格式不由扩展名决定，按内容嗅探**（`sniff_ext()`）：先认 `proxies:` → YAML，
再认 `outbounds` / `{` / `[` → JSON，否则按纯 URI 文本。理由很实际：
`ts-sf/fly` 的裸文件 `clash` 按文本解析得 0 条，按 YAML 解析得 200 条。

`SKIP_FILE_PATTERNS` 负责排除干扰项：`whitelist-all.txt`、`cidrwhitelist.txt`、`geosite`、
`rule`、`scrapy.log` 这类分流表与运行日志**不是**节点文件，误收会白耗下载与解析。

`github_api()` 会自动转义非 ASCII 路径（中文目录/文件名）；调用方传**未转义**的 path，
自己 quote 过再传会二次编码。
