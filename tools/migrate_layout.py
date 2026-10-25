# -*- coding: utf-8 -*-
"""migrate_layout.py — 把旧版「按日期分目录 + 每内核 3~5 个文件」的产物迁移到新扁平布局

做四件事：
1. 旧 pool/pool_<core>.json → pool/pool_state.json（每内核 1 个池文件由 state 派生）
2. 删除旧版 pool_<core>.txt / pool_<core>_list.txt（与池文件重复）
3. 删除 free-nodes/<YYYY-MM-DD>/ 历史日期目录（节点文件不再按日期存放）
4. collection_log.md / review_log.md 重排为「按日期倒序」

用法：
    python tools/migrate_layout.py [--root free-nodes] [--dry-run]
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

SKILL_SCRIPTS = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                             "free-nodes-collector", "scripts")
sys.path.insert(0, SKILL_SCRIPTS)
import layout as lay  # noqa: E402
import pool as node_pool  # noqa: E402

DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_SECTION = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?\s*$")


def log(msg):
    print(msg, flush=True)


def migrate_pool(root: Path, dry: bool):
    state = node_pool.load_state(root)   # 内部会把旧 pool_<core>.json 迁进来
    cores = sorted((state.get("cores") or {}).keys())
    if not cores:
        log("[pool] 没有可迁移的旧池数据")
    for core in cores:
        pool = node_pool.load(state, core)
        n = len(pool.get("nodes") or [])
        path = Path(lay.pool_path(root, core))
        log(f"[pool] {core}: {n} 条 → {path.name}")
        if not dry:
            node_pool.save(root, core, pool, "2026-10-25", state)
    if cores and not dry:
        node_pool.save_state(root, state, "2026-10-25")

    # 清理旧文件：注意 pool_v2ray.txt / pool_xray.txt / pool_singbox.json 既是「旧命名」
    # 又是「新命名」，必须先用 keep 白名单挡住，否则会把刚写出的新池文件删掉。
    pdir = root / "pool"
    keep = {lay.STATE_FILE, *lay.POOL_FILE.values()}
    legacy = [p for p in pdir.glob("pool_*.json")]
    legacy += list(pdir.glob("pool_*.txt"))      # 含旧名 pool_mihomo.txt / pool_*_list.txt
    legacy = [p for p in dict.fromkeys(legacy) if p.exists() and p.name not in keep]
    for p in legacy:
        log(f"[pool] 删除旧文件 {p.name}")
        if not dry:
            p.unlink()


def migrate_date_dirs(root: Path, dry: bool):
    for child in sorted(root.iterdir()):
        if child.is_dir() and DATE_DIR.match(child.name):
            log(f"[dir] 删除历史日期目录 {child.name}/")
            if not dry:
                shutil.rmtree(child, ignore_errors=True)


def resplit_md(path: Path, doc_title: str, intro: str, dry: bool):
    """把「追加在末尾」的旧日志重排成「按日期倒序」。"""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.lstrip().startswith("#") and "时间倒序" in text.splitlines()[0]:
        log(f"[md] {path.name} 已是新格式，跳过")
        return
    blocks, cur = [], None
    for line in text.splitlines():
        m = LOG_SECTION.match(line.strip())
        if m:
            cur = {"date": m.group(1), "time": m.group(2) or "", "lines": []}
            blocks.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    if not blocks:
        log(f"[md] {path.name} 没有可识别的日期小节，跳过")
        return
    log(f"[md] {path.name}：重排 {len(blocks)} 个小节（时间倒序）")
    if dry:
        return
    path.write_text(f"# {doc_title}\n\n> {intro}\n", encoding="utf-8")
    for b in reversed(blocks):
        lay.upsert_section(str(path), b["date"], b["time"],
                           "\n".join(b["lines"]).strip("\n"),
                           doc_title=doc_title, intro=intro)


def migrate_review_table(path: Path, dry: bool):
    """旧 review_log.md 是表格，逐行转成日期小节。"""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    if "时间倒序" in first:
        return
    rows = [ln for ln in text.splitlines()
            if ln.startswith("| ") and re.match(r"^\|\s*\d{4}-\d{2}-\d{2}", ln)]
    if not rows:
        return
    log(f"[md] review_log.md：表格 {len(rows)} 行 → 日期小节")
    if dry:
        return
    path.write_text("# 每日采集自检日志（时间倒序）\n\n> 跨天摘要，按日期倒序\n", encoding="utf-8")
    for ln in reversed(rows):
        cells = [c.strip() for c in ln.strip("|").split("|")]
        stamp = cells[0]
        date, _, tm = stamp.partition(" ")
        body = (f"- 去重后节点：{cells[1]}（目标 {cells[2]}）\n"
                f"- 各内核可用：{cells[3]}\n"
                f"- 结论：{cells[4]}；待修复 {cells[5]} 项")
        lay.upsert_section(str(path), date, tm, body)


def main():
    ap = argparse.ArgumentParser(description="迁移 free-nodes 到扁平单文件布局")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent / "free-nodes"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        log(f"[error] 目录不存在：{root}")
        return 2
    log(f"[info] 迁移目标：{root}{'（dry-run）' if args.dry_run else ''}")

    migrate_pool(root, args.dry_run)
    migrate_date_dirs(root, args.dry_run)
    resplit_md(root / "collection_log.md", "免费节点采集日志（时间倒序）",
               "每次运行一条，含执行阶段、仓库明细与结果；按日期倒序", args.dry_run)
    migrate_review_table(root / "review_log.md", args.dry_run)
    for name, title, intro in (
        ("report.md", "免费节点采集报告（时间倒序）", "按日期倒序累积"),
        ("summary.md", "节点可用性验证汇总（时间倒序）", "按日期倒序累积"),
        ("health_check.md", "每日自检报告（时间倒序）", "按日期倒序累积"),
    ):
        resplit_md(root / name, title, intro, args.dry_run)
    log("[done] 迁移完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
