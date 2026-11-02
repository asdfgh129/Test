#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主动触发 CI 采集工作流（GitHub 调度器的确定性兜底）。

为什么需要这个脚本：`schedule` 不可靠。2026-11-01 北京 21:05 那次定时任务被 GitHub
调度器延迟了 **5 小时 16 分**，跑到次日 02:20 才启动；runner 里 `date +%F` 已经是
「明天」，于是产物被标成明天的日期，当晚本地窗口一无所得（Docs/known-issues.md 第 54 条）。
加第二条 cron 只能把概率降下来，`workflow_dispatch` 才是确定的手段。

用法（api.github.com 直连可用，不需要翻墙、不需要 uplink 通道）：

    python ci_dispatch.py --check        # 只验凭据/仓库路径/权限，不真的触发
    python ci_dispatch.py                # 触发一次，打印 run id 与链接
    python ci_dispatch.py --wait 900     # 触发后轮询到结束（最多 900 秒），打印结论

`--check` 的做法：拿一个**不存在的 ref** 去 POST dispatches，GitHub 会返回 422
（"No ref found"）。收到 422 说明「端点 + 权限 + 仓库」都对，且没有真的排一次采集；
404 = 工作流路径不对，401/403 = token 无效或无 workflow 权限。

退出码：0 已触发（或已在跑、无需重复触发）/ 1 触发失败 / 2 凭据或仓库信息缺失
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.github.com"
UA = "free-nodes-collector/1.0"
# 强制直连：环境里可能残留 GIT_PROXY / 系统代理，而 api.github.com 本来就不用翻墙
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def log(msg: str) -> None:
    print(msg, flush=True)


def api(method: str, path: str, token: str, body: dict | None = None,
        timeout: int = 30) -> tuple[int, dict]:
    """调 GitHub REST API，返回 (status, payload)。HTTP 错误也当返回值，不抛异常。"""
    req = urllib.request.Request(API_BASE + path, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", UA)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    try:
        with _OPENER.open(req, data=data, timeout=timeout) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = {"message": raw[:300]}
        return exc.code, payload
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, {"message": f"{exc.__class__.__name__}: {exc}"}


def load_token(cli_token: str | None) -> str | None:
    """复用采集脚本的 token 查找链（--token > GITHUB_TOKEN/GH_TOKEN > 本地凭据文件）。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from collect_nodes import load_github_token, token_desc  # noqa: PLC0415
    except Exception as exc:                                    # pragma: no cover
        log(f"[error] 无法加载 collect_nodes 的 token 查找链：{exc}")
        return None
    tok = load_github_token(cli_token)
    log(f"[token] 身份 {token_desc(tok)}")
    return tok


def detect_repo(workspace: Path) -> str:
    """从 origin 的 URL 里取 owner/repo（支持 https 与 ssh 两种写法）。"""
    try:
        out = subprocess.run(["git", "-C", str(workspace), "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    if not out:
        return ""
    tail = out.split("github.com", 1)[-1].lstrip(":/")
    parts = [p for p in tail.replace(".git", "").split("/") if p]
    return "/".join(parts[:2]) if len(parts) >= 2 else ""


def latest_dispatch_run(repo: str, wf: str, token: str) -> dict | None:
    path = f"/repos/{repo}/actions/workflows/{wf}/runs?event=workflow_dispatch&per_page=1"
    code, payload = api("GET", path, token)
    if code != 200:
        return None
    runs = payload.get("workflow_runs") or []
    return runs[0] if runs else None


def wait_run(repo: str, run_id: int, token: str, timeout: int) -> str:
    """轮询到运行结束，返回 conclusion（超时返回 'timeout'）。"""
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        code, payload = api("GET", f"/repos/{repo}/actions/runs/{run_id}", token)
        if code == 200:
            status = payload.get("status")
            if status != last:
                log(f"[wait] 状态 {status}（{payload.get('conclusion') or '-'}）")
                last = status
            if status == "completed":
                return str(payload.get("conclusion") or "unknown")
        time.sleep(20)
    return "timeout"


def main() -> int:
    ap = argparse.ArgumentParser(description="主动触发 free-nodes 的 CI 采集工作流")
    ap.add_argument("--workspace", default=str(Path(__file__).resolve().parent.parent.parent),
                    help="git 仓库根目录（默认上溯三级：src → free-nodes → 仓库根）")
    ap.add_argument("--repo", default="", help="owner/repo，默认从 origin 解析")
    ap.add_argument("--workflow", default="collect.yml", help="工作流文件名，默认 collect.yml")
    ap.add_argument("--branch", default="master", help="dispatch 的 ref，默认 master")
    ap.add_argument("--token", default=None, help="GitHub token，默认走凭据查找链")
    ap.add_argument("--check", action="store_true",
                    help="只验证凭据/路径/权限（用一个不存在的 ref 换 422），不真的触发")
    ap.add_argument("--wait", type=int, default=0,
                    help="触发后等本次运行结束，最多等多少秒（0=不等，立即返回）")
    ap.add_argument("--dedup-minutes", type=int, default=10,
                    help="最近这么多分钟内有未完成的 dispatch 运行就不再触发，默认 10")
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    repo = args.repo or detect_repo(workspace)
    if not repo:
        log("[error] 无法确定 owner/repo，请用 --repo 指定")
        return 2
    token = load_token(args.token)
    if not token:
        log("[error] 找不到 GitHub token（--token / GITHUB_TOKEN / 本地凭据文件）")
        return 2
    log(f"[ci] 仓库 {repo} 工作流 {args.workflow} ref {args.branch}")

    # 1. 凭据 / 路径 / 权限自检
    if args.check:
        code, payload = api("POST", f"/repos/{repo}/actions/workflows/{args.workflow}/dispatches",
                            token, {"ref": "__ci_dispatch_check__"})
        if code == 422:
            log("[check] OK：端点、权限、仓库路径都通（422 = ref 不存在，符合预期，未排任何采集）")
            return 0
        log(f"[check] 失败：HTTP {code} —— {payload.get('message', '')}")
        if code == 404:
            log("[check] 404 的含义：工作流文件不在该 ref 上，或 --workflow 文件名写错")
        elif code in (401, 403):
            log("[check] 401/403 的含义：token 无效、过期，或没有 actions:write 权限")
        return 1

    # 2. 防重复：上一轮 dispatch 还在跑就别再排一次（两次采集会互相覆盖同一批文件）
    run = latest_dispatch_run(repo, args.workflow, token)
    if run:
        created = run.get("created_at", "")
        age_min = (time.time() - _parse_ts(created)) / 60 if created else 1e9
        if run.get("status") != "completed" and age_min < args.dedup_minutes:
            log(f"[skip] {age_min:.1f} 分钟前刚触发过一次（run {run.get('id')} "
                f"{run.get('status')}），不重复触发")
            return 0

    # 3. 触发
    code, payload = api("POST", f"/repos/{repo}/actions/workflows/{args.workflow}/dispatches",
                        token, {"ref": args.branch})
    if code != 204:
        log(f"[error] 触发失败：HTTP {code} —— {payload.get('message', '')}")
        return 1
    log("[ci] 已触发（202）：workflow_dispatch 排队中")

    # 4. 找到这次运行（GitHub 那边有几秒延迟，最多等 60 秒）
    run_id, run_url, deadline = None, "", time.time() + 60
    while time.time() < deadline and run_id is None:
        time.sleep(5)
        fresh = latest_dispatch_run(repo, args.workflow, token)
        if fresh and fresh.get("id") != (run.get("id") if run else None):
            run_id, run_url = fresh.get("id"), fresh.get("html_url", "")
    if run_id:
        log(f"[ci] run {run_id} {run_url}")
    else:
        log("[warn] 60 秒内没查到 run id（GitHub 排队慢），用下面的命令自己看一眼：")
        log(f"       api.github.com/repos/{repo}/actions/runs?event=workflow_dispatch")

    # 5. 可选：等它跑完（一次采集约 11 分钟）
    if args.wait and run_id:
        conclusion = wait_run(repo, run_id, token, args.wait)
        log(f"[wait] 结束：{conclusion}")
        return 0 if conclusion == "success" else 1
    return 0


def _parse_ts(iso: str) -> float:
    """把 GitHub 的 2026-11-01T18:20:49Z 转成 epoch 秒；解析不了就当很久以前。"""
    try:
        import datetime as dt
        return dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc).timestamp()
    except (TypeError, ValueError):
        return 0.0


if __name__ == "__main__":
    sys.exit(main())
