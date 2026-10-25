#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 free-nodes 采集产物提交并推送到 GitHub。

设计要点：
- 只提交 free-nodes 目录（路径限定的 git add --all free-nodes），
  绝不碰工作区里其他未完成的改动（例如用户自己的 C++ 项目修改）。
- 提交前清理过期的日期目录（默认保留最近 14 天），避免仓库无限膨胀。
- push 失败（GitHub 主站 443 被重置/超时很常见）时保留本地提交，
  把待推送状态写入 <workspace>/.git/free-nodes-pending-push.json，
  下次运行会先补推上一次没推上去的提交。

退出码：0 成功（含"无变更"）/ 1 push 失败但本地提交已保留 / 2 git 操作出错
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# 这些条目不属于"每日快照"，清理时永远保留
KEEP_NAMES = {"pool", "seed_repos.json", "collection_log.md", "review_log.md", "README.md", ".gitattributes"}


def log(msg: str) -> None:
    print(msg, flush=True)


# 可选代理：GitHub 主站 443 被重置时，用 --proxy 或环境变量 GIT_PROXY 指定，例如 http://127.0.0.1:7890
GIT_PROXY = ""


def git(workspace: Path, *args: str, timeout: int = 180) -> tuple[int, str]:
    """执行 git 命令，返回 (returncode, 合并后的输出)。"""
    cmd = ["git"]
    if GIT_PROXY:
        cmd += ["-c", f"http.proxy={GIT_PROXY}", "-c", f"https.proxy={GIT_PROXY}"]
    cmd += list(args)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"git {' '.join(args)} 超时（{timeout}s）"
    except FileNotFoundError:
        return 127, "找不到 git 可执行文件"


def pending_file(workspace: Path) -> Path:
    return workspace / ".git" / "free-nodes-pending-push.json"


def read_pending(workspace: Path) -> dict | None:
    p = pending_file(workspace)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"unreadable": True}


def write_pending(workspace: Path, payload: dict) -> None:
    p = pending_file(workspace)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def clear_pending(workspace: Path) -> None:
    p = pending_file(workspace)
    if p.exists():
        p.unlink()


def prune_old_days(out_root: Path, keep_days: int, today: dt.date) -> list[str]:
    """删除 out_root 下早于 keep_days 天的日期目录，返回被删列表。"""
    if keep_days <= 0 or not out_root.is_dir():
        return []
    cutoff = today - dt.timedelta(days=keep_days)
    removed: list[str] = []
    for child in sorted(out_root.iterdir()):
        if not child.is_dir() or child.name in KEEP_NAMES or not DATE_DIR_RE.match(child.name):
            continue
        try:
            d = dt.date.fromisoformat(child.name)
        except ValueError:
            continue
        if d >= cutoff:
            continue
        for f in sorted(child.rglob("*"), reverse=True):
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                f.rmdir()
        child.rmdir()
        removed.append(child.name)
    return removed


def push_with_retry(workspace: Path, branch: str, retries: int, wait: int) -> tuple[bool, str]:
    last_err = ""
    for attempt in range(1, retries + 1):
        log(f"[push] 第 {attempt}/{retries} 次尝试推送到 origin/{branch} …")
        code, out = git(workspace, "push", "origin", branch, timeout=180)
        if code == 0:
            return True, out
        last_err = out.strip()
        log(f"[push] 失败：{last_err.splitlines()[-1] if last_err else '未知错误'}")
        if attempt < retries:
            time.sleep(wait)
    return False, last_err


def main() -> int:
    ap = argparse.ArgumentParser(description="提交并推送 free-nodes 产物到 GitHub")
    ap.add_argument("--workspace", default=str(Path(__file__).resolve().parent.parent),
                    help="git 仓库根目录（默认脚本上一级）")
    ap.add_argument("--dir", default="free-nodes", help="相对仓库的产物目录名，默认 free-nodes")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="提交信息里的日期，默认今天")
    ap.add_argument("--branch", default="master", help="目标分支，默认 master")
    ap.add_argument("--keep-days", type=int, default=14, help="保留最近多少天的日期目录，0=不清理")
    ap.add_argument("--retries", type=int, default=3, help="push 重试次数，默认 3")
    ap.add_argument("--retry-wait", type=int, default=20, help="重试间隔秒数，默认 20")
    ap.add_argument("--no-push", action="store_true", help="只提交不推送")
    ap.add_argument("--proxy", default=os.environ.get("GIT_PROXY", ""),
                    help="推送时使用的 HTTP 代理，如 http://127.0.0.1:7890（也可用环境变量 GIT_PROXY）")
    args = ap.parse_args()

    global GIT_PROXY
    GIT_PROXY = (args.proxy or "").strip()
    if GIT_PROXY:
        log(f"[proxy] 推送走代理 {GIT_PROXY}")

    workspace = Path(args.workspace).resolve()
    if not (workspace / ".git").exists():
        log(f"[error] {workspace} 不是 git 仓库")
        return 2

    out_root = workspace / args.dir
    if not out_root.is_dir():
        log(f"[error] 产物目录不存在：{out_root}")
        return 2

    # 0. 上次没推成功的，先补推
    pend = read_pending(workspace)
    if pend and not args.no_push:
        log(f"[pending] 发现上次未推送的提交：{pend.get('commit', '?')}（{pend.get('date', '?')}），先补推")
        ok, _ = push_with_retry(workspace, args.branch, 1, args.retry_wait)
        if ok:
            clear_pending(workspace)
            log("[pending] 补推成功，已清除待推送标记")
        else:
            log("[pending] 补推仍失败，稍后会带上本次提交一起重试")

    # 1. 清理过期日期目录
    removed = prune_old_days(out_root, args.keep_days, dt.date.fromisoformat(args.date))
    if removed:
        log(f"[prune] 移除过期目录：{', '.join(removed)}")

    # 2. 路径限定地暂存（只动 free-nodes）
    code, out = git(workspace, "add", "--all", "--", args.dir)
    if code != 0:
        log(f"[error] git add 失败：{out.strip()}")
        return 2

    code, out = git(workspace, "diff", "--cached", "--name-only", "--", args.dir)
    staged = [line for line in out.splitlines() if line.strip()]
    commit_hash = ""
    if staged:
        log(f"[stage] 待提交文件 {len(staged)} 个")
        msg = f"chore(free-nodes): 更新 {args.date} 免费节点订阅"
        code, out = git(workspace, "commit", "-m", msg, "--", args.dir)
        if code != 0:
            log(f"[error] git commit 失败：{out.strip()}")
            return 2
        code, commit_hash = git(workspace, "rev-parse", "--short", "HEAD")
        commit_hash = commit_hash.strip()
        log(f"[commit] {commit_hash} {msg}")
    else:
        log("[stage] free-nodes 无变更，跳过提交")

    if args.no_push:
        log("[push] 已指定 --no-push，跳过推送")
        return 0

    # 3. 推送（无新提交也要尝试补推历史未推的）
    code, ahead = git(workspace, "rev-list", "--count", f"origin/{args.branch}..HEAD")
    has_unpushed = code == 0 and ahead.strip().isdigit() and int(ahead.strip()) > 0
    if not staged and not has_unpushed:
        log("[push] 本地与远端一致，无需推送")
        clear_pending(workspace)
        return 0

    ok, err = push_with_retry(workspace, args.branch, args.retries, args.retry_wait)
    if ok:
        clear_pending(workspace)
        log(f"[push] 成功，origin/{args.branch} 已更新")
        return 0

    write_pending(workspace, {
        "date": args.date,
        "commit": commit_hash or "已有未推送提交",
        "branch": args.branch,
        "error": err[-1500:],
        "failed_at": dt.datetime.now().isoformat(timespec="seconds"),
        "next": f"下次运行会先执行 git push origin {args.branch} 补推；也可手动在 {workspace} 执行",
    })
    log("[push] 全部重试失败：提交已保留在本地，待推送状态已记录，下次运行会自动补推")
    return 1


if __name__ == "__main__":
    sys.exit(main())
