#!/usr/bin/env python3
"""Formosis update — 新版提醒與一鍵更新。

用法：
  update.py check             有新 release 時在 stderr 印一行提醒（build 腳本編譯前呼叫）
  update.py status            顯示目前版本與最新版本（不使用快取）
  update.py apply             更新到最新 release，並重新安裝各 profile 的 Claude Skill

設計：
  - release 就是 git tag（vX.Y.Z）。用 `git ls-remote --tags` 查最新版，不經 GitHub API、
    不受 API 速率限制，也沿用使用者既有的 git 連線設定。
  - check 最多每天連網一次，結果快取在 .git/formosis-update-check.json（不進版控）。
    查詢失敗也算當天查過：離線的電腦每天最多等一次逾時，編譯不會因此變慢或失敗。
  - 只提醒、不自動更新：快口試的論文不該在沒人要求時換格式。apply 只在使用者執行時才動作。
  - 論文在根目錄下的獨立 git repo（scripts/new-thesis），apply 用 fast-forward 更新工具 repo，
    碰不到論文。工具 repo 的受版控檔案被改過時拒絕更新，而不是覆蓋使用者的修改。
  - 以下情況不檢查：CI、設了 FORMOSIS_NO_UPDATE_CHECK、不在 main 分支（工具開發中）、
    不是 git clone（release 壓縮檔安裝）。

Exit code：check / status 永遠 0；apply 成功或已是最新為 0，無法更新為 1。
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECK_EVERY_S = 24 * 60 * 60
# 夠慢速網路回應，又不會讓擋封包的離線環境多等太久（每天最多一次）
QUERY_TIMEOUT_S = 3.0
FETCH_TIMEOUT_S = 120.0
CACHE_NAME = "formosis-update-check.json"
MAIN_BRANCH = "main"
_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")

if sys.stderr.isatty():
    C_YEL, C_GRN, C_RED, C_NC = "\033[0;33m", "\033[0;32m", "\033[0;31m", "\033[0m"
else:
    C_YEL = C_GRN = C_RED = C_NC = ""


def say(msg: str) -> None:
    print(msg, file=sys.stderr)


# ============================================================
# git
# ============================================================

def git(*args: str, timeout: float = 30.0, check: bool = True) -> str:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout, env=env)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def parse_tag(tag: str) -> tuple[int, int, int] | None:
    """"v1.2.3" → (1, 2, 3)，讓 v0.10.0 排在 v0.9.0 之後。非 release tag 回傳 None。"""
    m = _TAG_RE.match(tag)
    return tuple(int(x) for x in m.groups()) if m else None  # type: ignore[return-value]


def newest(tags: list[str]) -> str | None:
    versions = [(parse_tag(t), t) for t in tags]
    versions = [v for v in versions if v[0] is not None]
    return max(versions)[1] if versions else None


def current_version() -> str | None:
    """HEAD 所含的最新 release tag。"""
    tags = git("tag", "--merged", "HEAD", "--list", "v*", check=False).splitlines()
    return newest([t.strip() for t in tags])


def remote_latest(timeout: float = QUERY_TIMEOUT_S) -> str | None:
    """origin 上最新的 release tag。連不上時丟 OSError / CalledProcessError / TimeoutExpired。"""
    out = git("ls-remote", "--tags", "--refs", "origin", "v*", timeout=timeout)
    return newest([line.split("refs/tags/", 1)[-1] for line in out.splitlines() if "refs/tags/" in line])


def is_newer(latest: str | None, current: str | None) -> bool:
    if not latest or parse_tag(latest) is None:
        return False
    if not current or parse_tag(current) is None:
        return True
    return parse_tag(latest) > parse_tag(current)  # type: ignore[operator]


def skip_reason() -> str | None:
    """不該檢查更新的理由；None 表示可以檢查。"""
    if os.environ.get("CI") or os.environ.get("FORMOSIS_NO_UPDATE_CHECK"):
        return "CI 或 FORMOSIS_NO_UPDATE_CHECK"
    try:
        if not (REPO_ROOT / ".git").exists():
            return "不是 git clone"
        if git("branch", "--show-current", check=False) != MAIN_BRANCH:
            return f"不在 {MAIN_BRANCH} 分支"
        if not git("remote", "get-url", "origin", check=False):
            return "沒有 origin"
    except (OSError, subprocess.SubprocessError):
        return "找不到 git"
    return None


# ============================================================
# 快取
# ============================================================

def cache_path() -> Path:
    return Path(git("rev-parse", "--absolute-git-dir")) / CACHE_NAME


def read_cache(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def write_cache(path: Path, data: dict) -> None:
    with contextlib.suppress(OSError):
        path.write_text(json.dumps(data), encoding="utf-8")


def update_command() -> str:
    return r"python scripts\update.py apply" if os.name == "nt" else "make update（或 python3 scripts/update.py apply）"


# ============================================================
# 子指令
# ============================================================

def cmd_check(now: float) -> int:
    if skip_reason():
        return 0
    try:
        path = cache_path()
        state = read_cache(path)
        # 快取時間在未來代表時鐘曾經被調快；不處理的話會一直到那天都不再檢查
        if not 0 <= now - state.get("checked", 0) < CHECK_EVERY_S:
            state["checked"] = now
            # 失敗也算今天查過，沿用上次結果
            with contextlib.suppress(OSError, subprocess.SubprocessError):
                state["latest"] = remote_latest()
            write_cache(path, state)
        current = current_version()
    except (OSError, subprocess.SubprocessError):
        return 0
    latest = state.get("latest")
    if is_newer(latest, current):
        say(f"{C_YEL}[UPDATE]{C_NC} Formosis {latest} 已發布（目前 {current or '未發布版本'}）；"
            f"執行 {update_command()} 更新")
    return 0


def cmd_status() -> int:
    reason = skip_reason()
    current = current_version() if (REPO_ROOT / ".git").exists() else None
    say(f"目前版本：{current or '未發布版本'}")
    try:
        latest = remote_latest(timeout=15.0)
    except (OSError, subprocess.SubprocessError):
        say("最新版本：無法連線到 origin")
        return 0
    say(f"最新版本：{latest or '尚無 release'}")
    if reason:
        say(f"（自動提醒已停用：{reason}）")
    return 0


def reinstall_skills() -> bool:
    if os.name == "nt":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
               "-File", str(REPO_ROOT / "scripts" / "install-skill.ps1"), "-Force"]
    else:
        cmd = ["bash", str(REPO_ROOT / "scripts" / "install-skill.sh"), "--force"]
    try:
        return subprocess.run(cmd, cwd=REPO_ROOT).returncode == 0
    except OSError:
        return False


def cmd_apply(install_skills: bool = True) -> int:
    def fail(msg: str) -> int:
        say(f"{C_RED}[ERROR]{C_NC} {msg}")
        return 1

    if not (REPO_ROOT / ".git").exists():
        return fail("這份 Formosis 不是 git clone（可能是 release 壓縮檔），請到 GitHub Releases 下載新版")
    try:
        branch = git("branch", "--show-current", check=False)
        if branch != MAIN_BRANCH:
            return fail(f"目前在 {branch or '（detached HEAD）'} 分支；工具更新只在 {MAIN_BRANCH} 上進行。"
                        f"請先 git switch {MAIN_BRANCH}")
        dirty = git("status", "--porcelain", "--untracked-files=no")
        if dirty:
            return fail("工具 repo 有未提交的修改，為避免覆蓋你的變更而停止更新：\n" + dirty +
                        "\n個人化的格式調整請改寫在論文 paper.md 的 header-includes；"
                        "確定不需要這些修改時可執行 git restore <檔案>")
        say("取得最新版本資訊……")
        git("fetch", "--tags", "--force", "origin", timeout=FETCH_TIMEOUT_S)
        latest = newest(git("tag", "--list", "v*").splitlines())
        current = current_version()
        if not is_newer(latest, current):
            say(f"{C_GRN}[OK]{C_NC} 已是最新版本（{current or latest or '尚無 release'}）")
            return 0
        old_head = git("rev-parse", "HEAD")
        merged = subprocess.run(["git", "-C", str(REPO_ROOT), "merge", "--ff-only", "-q", latest],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        if merged.returncode != 0:
            return fail(f"無法快轉到 {latest}（本機 {MAIN_BRANCH} 有不在 release 中的 commit）：\n"
                        f"{merged.stderr.strip()}")
        say(f"{C_GRN}[OK]{C_NC} Formosis {current or '未發布版本'} → {latest}")
        fmt = git("diff", "--stat", old_head, "HEAD", "--", "profiles", "shared")
        if fmt:
            stat = "\n".join("  " + line.strip() for line in fmt.splitlines())
            say(f"{C_YEL}[注意]{C_NC} 這次更新改到論文格式相關檔案，編譯後請檢查 PDF 版面：\n{stat}")
        say(f"完整變更：CHANGELOG.md 或 git log {old_head[:7]}..HEAD")
    except subprocess.CalledProcessError as e:
        return fail(f"git {' '.join(e.cmd)} 失敗：{(e.stderr or '').strip()}")
    except (OSError, subprocess.SubprocessError) as e:
        return fail(f"無法執行 git：{e}")
    write_cache(cache_path(), {"checked": time.time(), "latest": latest})
    if install_skills:
        say("重新安裝 Claude Skill……")
        if not reinstall_skills():
            say(f"{C_YEL}[WARN]{C_NC} Skill 重新安裝失敗，請手動執行 scripts/install-skill")
    return 0


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    if cmd == "check":
        return cmd_check(time.time())
    if cmd == "status":
        return cmd_status()
    if cmd == "apply":
        return cmd_apply()
    print(__doc__, file=sys.stderr)
    return 0 if cmd in ("-h", "--help") else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
