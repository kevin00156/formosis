"""scripts/update.py 的測試：用本機的 bare repo 當 origin，不連網。

執行：python3 -m unittest discover -s tests
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import update  # noqa: E402


def run(*args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


class VersionTest(unittest.TestCase):
    def test_newest_sorts_numerically(self):
        self.assertEqual(update.newest(["v0.9.0", "v0.10.0", "v0.2.1", "nightly"]), "v0.10.0")
        self.assertIsNone(update.newest(["latest"]))

    def test_is_newer(self):
        self.assertTrue(update.is_newer("v0.2.0", "v0.1.9"))
        self.assertTrue(update.is_newer("v0.1.0", None))
        self.assertFalse(update.is_newer("v0.1.0", "v0.1.0"))
        self.assertFalse(update.is_newer(None, "v0.1.0"))


class GitRepoTest(unittest.TestCase):
    """origin（bare）← 維護者發 release；tool（clone）= 使用者的工具 repo。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.origin, self.dev, self.tool = base / "origin.git", base / "dev", base / "tool"
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t"}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("CI", None)
        os.environ.pop("FORMOSIS_NO_UPDATE_CHECK", None)
        run("git", "init", "-q", "--bare", str(self.origin), cwd=base)
        run("git", "symbolic-ref", "HEAD", "refs/heads/main", cwd=self.origin)
        run("git", "init", "-q", str(self.dev), cwd=base)
        run("git", "symbolic-ref", "HEAD", "refs/heads/main", cwd=self.dev)
        self.release("v0.1.0", "template-v1")
        run("git", "clone", "-q", str(self.origin), str(self.tool), cwd=base)
        patcher = mock.patch.object(update, "REPO_ROOT", self.tool)
        patcher.start()
        self.addCleanup(patcher.stop)

    def release(self, tag, content):
        (self.dev / "profiles").mkdir(exist_ok=True)
        (self.dev / "profiles" / "template.txt").write_text(content, encoding="utf-8")
        run("git", "add", "-A", cwd=self.dev)
        run("git", "commit", "-q", "-m", tag, cwd=self.dev)
        run("git", "tag", tag, cwd=self.dev)
        run("git", "push", "-q", str(self.origin), "main", "--tags", cwd=self.dev)

    def check(self, now=1_000_000.0):
        err = io.StringIO()
        with mock.patch("sys.stderr", err):
            update.cmd_check(now)
        return err.getvalue()

    def apply(self):
        err = io.StringIO()
        with mock.patch("sys.stderr", err):
            code = update.cmd_apply(install_skills=False)
        return code, err.getvalue()

    def test_up_to_date_is_silent(self):
        self.assertEqual(self.check(), "")

    def test_reminds_once_a_day_then_updates(self):
        self.check(now=1_000_000.0)             # 今天查過：v0.1.0
        self.release("v0.2.0", "template-v2")
        self.assertEqual(self.check(now=1_000_100.0), "")   # 快取未過期，不連網
        self.assertIn("v0.2.0 已發布（目前 v0.1.0）", self.check(now=1_000_000.0 + 86_401))
        code, out = self.apply()
        self.assertEqual(code, 0, out)
        self.assertIn("v0.1.0 → v0.2.0", out)
        self.assertIn("論文格式相關檔案", out)
        self.assertEqual((self.tool / "profiles" / "template.txt").read_text(encoding="utf-8"), "template-v2")
        self.assertEqual(self.check(now=1_000_000.0 + 86_500), "")  # apply 後不再提醒
        code, out = self.apply()
        self.assertEqual(code, 0)
        self.assertIn("已是最新版本", out)

    def test_offline_counts_as_checked(self):
        run("git", "remote", "set-url", "origin", str(self.origin) + "-missing", cwd=self.tool)
        self.assertEqual(self.check(now=2_000_000.0), "")
        cache = update.read_cache(update.cache_path())
        self.assertEqual(cache["checked"], 2_000_000.0)

    def test_refuses_to_overwrite_local_changes(self):
        self.release("v0.2.0", "template-v2")
        (self.tool / "profiles" / "template.txt").write_text("my tweak", encoding="utf-8")
        code, out = self.apply()
        self.assertEqual(code, 1)
        self.assertIn("未提交的修改", out)
        self.assertEqual((self.tool / "profiles" / "template.txt").read_text(encoding="utf-8"), "my tweak")

    def test_untracked_thesis_folder_does_not_block(self):
        self.release("v0.2.0", "template-v2")
        (self.tool / "my-thesis").mkdir()
        (self.tool / "my-thesis" / "paper.md").write_text("論文", encoding="utf-8")
        code, out = self.apply()
        self.assertEqual(code, 0, out)
        self.assertEqual((self.tool / "my-thesis" / "paper.md").read_text(encoding="utf-8"), "論文")

    def test_feature_branch_is_skipped_and_refused(self):
        self.release("v0.2.0", "template-v2")
        run("git", "switch", "-q", "-c", "feat/x", cwd=self.tool)
        self.assertEqual(self.check(now=3_000_000.0), "")
        code, out = self.apply()
        self.assertEqual(code, 1)
        self.assertIn("feat/x", out)

    def test_ci_env_skips(self):
        self.release("v0.2.0", "template-v2")
        with mock.patch.dict(os.environ, {"CI": "true"}):
            self.assertEqual(self.check(now=4_000_000.0), "")


if __name__ == "__main__":
    unittest.main()
