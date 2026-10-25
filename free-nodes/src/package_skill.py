#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""package_skill.py — 把技能目录打包成可分发的 zip（不含代理内核二进制）

用法：
    python scripts/package_skill.py                 # 输出 <当前目录>/dist/<技能名>.zip
    python scripts/package_skill.py --out-dir D     # 指定输出目录
    python scripts/package_skill.py --include-tools  # 连内核一起打包（约 248MB，一般不需要）

打包时自动排除：__pycache__、*.pyc、tools/（内核二进制）、已有 zip。
内核目录放在 ~/.workbuddy/data/free-nodes-tools/bin，与技能包解耦，
所以技能包只有几十 KB，升级代码不需要重传 200MB 内核。
"""

import argparse
import os
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode"}
EXCLUDE_EXT = {".pyc", ".pyo", ".zip", ".log"}


def iter_files(root, include_tools=False):
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS
                   and (include_tools or d != "tools")]
        for name in files:
            if os.path.splitext(name)[1].lower() in EXCLUDE_EXT:
                continue
            path = os.path.join(cur, name)
            yield path, os.path.relpath(path, root)


def main():
    ap = argparse.ArgumentParser(description="打包技能为 zip")
    ap.add_argument("--out-dir", default=os.path.join(os.getcwd(), "dist"),
                    help="输出目录（默认 ./dist）")
    ap.add_argument("--include-tools", action="store_true", help="连内核二进制一起打包")
    args = ap.parse_args()

    name = os.path.basename(SKILL_DIR)
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f"{name}.zip")
    count = 0
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in iter_files(SKILL_DIR, args.include_tools):
            zf.write(path, os.path.join(name, rel))
            count += 1
    size = os.path.getsize(out_path)
    print(f"[done] {out_path}（{count} 个文件，{size/1024:.0f} KB）")
    if size > 5 * 1024 * 1024 and not args.include_tools:
        print("[warn] 包体偏大，检查是否误把大文件打进技能目录", file=sys.stderr)


if __name__ == "__main__":
    main()
