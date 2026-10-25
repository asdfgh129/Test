#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 free-nodes 采集产物提交并推送到 GitHub。

设计要点：
- 只提交 free-nodes 目录（路径限定的 git add --all free-nodes），
  绝不碰工作区里其他未完成的改动（例如用户自己的 C++ 项目修改）。
- 脚本自身就住在 free-nodes/src/（采集/验证/发布全链路的唯一事实来源），
  提交即自动带上最新脚本，无需任何同步动作；
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
# 这些条目不属于"每日快照"，清理时永远保留（新布局：nodes/Docs/src/Skills 三分层）
KEEP_NAMES = {"nodes", "Docs", "src", "Skills", "README.md", "CHANGELOGS.md",
              ".gitattributes", ".workbuddy"}


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


# 常见代理客户端默认端口，--proxy auto 时逐个探活
PROXY_CANDIDATES = [
    "127.0.0.1:7890", "127.0.0.1:7897", "127.0.0.1:7891", "127.0.0.1:7892",
    "127.0.0.1:1080", "127.0.0.1:1081", "127.0.0.1:10808", "127.0.0.1:10809",
    "127.0.0.1:2080", "127.0.0.1:2081", "127.0.0.1:8889", "127.0.0.1:6789",
    "127.0.0.1:20171", "127.0.0.1:33210",
]


def detect_proxy(timeout: float = 8.0) -> str:
    """扫描常见本地代理端口，返回第一个能通过代理取到 github.com 的地址。"""
    import socket
    import urllib.error
    import urllib.request

    for hp in PROXY_CANDIDATES:
        host, port = hp.split(":")
        try:
            with socket.create_connection((host, int(port)), timeout=0.4):
                pass
        except OSError:
            continue  # 端口没监听，直接跳过
        proxy_url = f"http://{hp}"
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
        )
        try:
            with opener.open("https://github.com/", timeout=timeout) as resp:
                if 200 <= resp.status < 400:
                    return proxy_url
        except urllib.error.HTTPError as e:
            if 200 <= e.code < 400:
                return proxy_url
        except Exception:
            continue
    return ""


def remove_legacy_dirs(out_root: Path) -> list[str]:
    """删除历史遗留的日期目录（新布局为扁平目录，节点文件不再按日期分目录）。

    过期的节点没有意义：现在的做法是每次覆盖 nodes/ 下的最新文件，历史留在
    Docs/ 里按日期倒序的 md 和根目录的 CHANGELOGS.md。
    """
    if not out_root.is_dir():
        return []
    removed: list[str] = []
    for child in sorted(out_root.iterdir()):
        if not child.is_dir() or child.name in KEEP_NAMES or not DATE_DIR_RE.match(child.name):
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


def load_uplink(scripts_dir: str):
    """加载技能里的 uplink 模块（用已验证节点自建本地代理）。不可用则返回 None。"""
    if not scripts_dir or not os.path.isdir(scripts_dir):
        return None
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import uplink  # noqa: PLC0415
        return uplink
    except Exception as e:  # noqa: BLE001
        log(f"[uplink] 模块加载失败（{scripts_dir}）：{str(e)[:80]}")
        return None


def do_push(workspace: Path, args, up_mod, out_root: str) -> tuple[bool, str]:
    """推送提交。

    顺序：已有代理（--proxy 指定 / 探测到）→ 自建代理逐节点换核试 → 直连重试。
    自建代理阶段的语义是「推不通就换节点、换内核，直到连通」。
    """
    global GIT_PROXY

    # A. 已有可用代理：直接推
    if GIT_PROXY:
        return push_with_retry(workspace, args.branch, args.retries, args.retry_wait)

    # B. 自建代理：每轮挑一个节点起本地内核，推不动就换下一个
    if up_mod is not None:
        tried: set[str] = set()
        rounds = max(1, args.uplink_rounds)
        for r in range(1, rounds + 1):
            log(f"[uplink] 第 {r}/{rounds} 轮：从已验证节点里起本地代理 …")
            # git push 只依赖 github.com，探测就只认它（api.github.com 通不代表能 push）
            up = up_mod.start(root=out_root, max_candidates=args.uplink_candidates,
                              skip=tried, probes=["https://github.com/"])
            if up is None:
                log("[uplink] 没有更多可用节点可试")
                break
            tried.add(up.uri)
            GIT_PROXY = up.url
            try:
                code, out = git(workspace, "push", "origin", args.branch, timeout=180)
            finally:
                GIT_PROXY = ""
            if code == 0:
                up_mod.stop(up)
                log(f"[push] 经自建代理推送成功（{up.describe()}）")
                return True, out
            tail = out.strip().splitlines()[-1] if out.strip() else "未知错误"
            log(f"[push] 该节点推送失败：{tail} → 换节点/内核重试")
            up_mod.stop(up)
        log("[push] 自建代理轮换全部失败，改直连重试")

    # C. 直连兜底
    return push_with_retry(workspace, args.branch, args.retries, args.retry_wait)


def main() -> int:
    ap = argparse.ArgumentParser(description="提交并推送 free-nodes 产物到 GitHub")
    ap.add_argument("--workspace", default=str(Path(__file__).resolve().parent.parent.parent),
                    help="git 仓库根目录（默认脚本上溯三级：src → free-nodes → 仓库根）")
    ap.add_argument("--dir", default="free-nodes", help="相对仓库的产物目录名，默认 free-nodes")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="提交信息里的日期，默认今天")
    ap.add_argument("--branch", default="master", help="目标分支，默认 master")
    ap.add_argument("--retries", type=int, default=3, help="直连 push 重试次数，默认 3")
    ap.add_argument("--retry-wait", type=int, default=20, help="重试间隔秒数，默认 20")
    ap.add_argument("--no-push", action="store_true", help="只提交不推送")
    ap.add_argument("--proxy", default=os.environ.get("GIT_PROXY", ""),
                    help="推送时使用的 HTTP 代理，如 http://127.0.0.1:7890；"
                         "auto=先探测本地代理端口，探测不到就用已验证节点自建代理"
                         "（也可用环境变量 GIT_PROXY）")
    ap.add_argument("--skill-scripts",
                    default=str(Path(__file__).resolve().parent),
                    help="uplink.py 所在目录（默认即本脚本所在目录 free-nodes/src/）")
    ap.add_argument("--uplink-rounds", type=int, default=5,
                    help="自建代理最多轮换多少轮（每轮一个节点），默认 5")
    ap.add_argument("--uplink-candidates", type=int, default=40,
                    help="每轮自建代理最多尝试的候选节点数，默认 40")
    args = ap.parse_args()

    global GIT_PROXY
    GIT_PROXY = (args.proxy or "").strip()
    up_mod = None
    if GIT_PROXY.lower() == "auto":
        log("[proxy] 先探测本机已有代理端口 …")
        GIT_PROXY = detect_proxy()
        if GIT_PROXY:
            log(f"[proxy] 探测到可用代理 {GIT_PROXY}")
        else:
            up_mod = load_uplink(args.skill_scripts)
            if up_mod is not None:
                log("[proxy] 无现成代理，改为用已验证节点自建本地代理推送")
            else:
                log("[proxy] 无现成代理且 uplink 模块不可用，按直连推送")
    elif GIT_PROXY:
        log(f"[proxy] 推送走代理 {GIT_PROXY}")

    workspace = Path(args.workspace).resolve()
    if not (workspace / ".git").exists():
        log(f"[error] {workspace} 不是 git 仓库")
        return 2

    out_root = workspace / args.dir
    if not out_root.is_dir():
        log(f"[error] 产物目录不存在：{out_root}")
        return 2

    # 0. 上次没推成功的提交：不单独推，最后统一推送（一次 push 会带上所有未推送提交）
    pend = read_pending(workspace)
    if pend and not args.no_push:
        log(f"[pending] 检测到上次未推送的提交（{pend.get('date', '?')}），本次会一并推送")

    # 1. 清理历史遗留的日期目录（新布局为 nodes/Docs/src 三分层，不再按日期分目录）
    removed = remove_legacy_dirs(out_root)
    if removed:
        log(f"[prune] 移除历史日期目录：{', '.join(removed)}")

    # 2. 路径限定地暂存（只动 free-nodes；脚本本身就在 src/ 里，无需同步）
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

    ok, err = do_push(workspace, args, up_mod, str(out_root))
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
