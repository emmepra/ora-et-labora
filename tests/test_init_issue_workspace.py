from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "init_issue_workspace.py"


class InitIssueWorkspaceTests(unittest.TestCase):
    def test_creates_workspace_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                    "--issue-id",
                    "123",
                    "--title",
                    "Fix login race",
                    "--kind",
                    "bug",
                    "--branch",
                    "fix/123-login-race",
                    "--issue-url",
                    "https://example.com/issues/123",
                ],
                check=True,
            )

            current = repo_root / ".project" / "todo" / "123" / "CURRENT.md"
            brainstorm = repo_root / ".project" / "todo" / "123" / "00_brainstorm.md"
            log = repo_root / ".project" / "logs" / "123.md"

            self.assertTrue(current.exists())
            self.assertTrue(brainstorm.exists())
            self.assertTrue(log.exists())
            self.assertIn("fix/123-login-race", current.read_text())
            self.assertIn("Fix login race", brainstorm.read_text())


if __name__ == "__main__":
    unittest.main()
