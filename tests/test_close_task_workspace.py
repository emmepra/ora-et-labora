from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "close_task_workspace.py"


def git(repo_root: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


class CloseTaskWorkspaceTests(unittest.TestCase):
    def init_repo(self, tmp: Path) -> Path:
        repo = tmp / "repo"
        repo.mkdir()
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.email", "codex@example.com")
        git(repo, "config", "user.name", "Codex")
        (repo / "README.md").write_text("repo\n")
        git(repo, "add", "README.md")
        git(repo, "commit", "-m", "init")
        git(repo, "checkout", "-b", "dev")
        return repo

    def make_task_branch(self, repo: Path, module_id: str = "17", branch: str = "feat/17-cleanup") -> Path:
        worktree = repo / ".project" / "worktrees" / branch.replace("/", "-")
        worktree.parent.mkdir(parents=True, exist_ok=True)
        git(repo, "worktree", "add", str(worktree), "-b", branch, "dev")
        todo_dir = worktree / ".project" / "todo" / module_id
        log_dir = worktree / ".project" / "logs"
        todo_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)
        (todo_dir / "CURRENT.md").write_text(
            "\n".join(
                [
                    "# Current State",
                    "",
                    f"- Module: {module_id}",
                    f"- Branch: {branch}",
                    "- Status: implementation complete",
                    "- Next step: open PR",
                    "- Blockers: none",
                    "",
                ]
            )
        )
        (todo_dir / "00_brainstorm.md").write_text("brainstorm\n")
        (todo_dir / "pr.md").write_text("pr body\n")
        (log_dir / f"{module_id}.md").write_text(f"# Task Log: {module_id}\n")
        (worktree / "feature.txt").write_text("done\n")
        git(repo, "-C", str(worktree), "add", ".")
        git(repo, "-C", str(worktree), "commit", "-m", "feature")
        git(repo, "checkout", "dev")
        return worktree

    def test_dry_run_prints_cleanup_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.init_repo(Path(tmp))
            self.make_task_branch(repo)
            git(repo, "merge", "--no-ff", "feat/17-cleanup", "-m", "merge feature")
            result = subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--module-id",
                    "17",
                    "--merged-into",
                    "dev",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Cleanup plan for module 17", result.stdout)
            self.assertIn("delete local todo dir", result.stdout)
            self.assertIn("rm -rf", result.stdout)
            self.assertIn("git worktree remove", result.stdout)
            self.assertIn("git branch -d feat/17-cleanup", result.stdout)

    def test_apply_removes_local_task_state_and_cleans_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.init_repo(Path(tmp))
            worktree = self.make_task_branch(repo)
            git(repo, "merge", "--no-ff", "feat/17-cleanup", "-m", "merge feature")
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--module-id",
                    "17",
                    "--merged-into",
                    "dev",
                    "--apply",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((repo / ".project" / "todo" / "17").exists())
            self.assertFalse((repo / ".project" / "logs" / "archive" / "17").exists())
            self.assertFalse(worktree.exists())
            branches = git(repo, "branch", "--list", "feat/17-cleanup").stdout.strip()
            self.assertEqual(branches, "")
            log_text = (repo / ".project" / "logs" / "17.md").read_text()
            self.assertNotIn("state:closed", log_text)
            self.assertNotIn("task-state:removed", log_text)

    def test_apply_can_archive_task_state_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.init_repo(Path(tmp))
            worktree = self.make_task_branch(repo)
            git(repo, "merge", "--no-ff", "feat/17-cleanup", "-m", "merge feature")
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--module-id",
                    "17",
                    "--merged-into",
                    "dev",
                    "--archive-root",
                    ".project/local-archive",
                    "--apply",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((repo / ".project" / "todo" / "17").exists())
            self.assertTrue((repo / ".project" / "local-archive" / "17" / "CURRENT.md").exists())
            self.assertFalse(worktree.exists())
            log_text = (repo / ".project" / "logs" / "17.md").read_text()
            self.assertNotIn("task-state:archived", log_text)
            self.assertNotIn(".project/local-archive/17", log_text)

    def test_apply_refuses_when_branch_not_merged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.init_repo(Path(tmp))
            self.make_task_branch(repo)
            result = subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--module-id",
                    "17",
                    "--merged-into",
                    "dev",
                    "--apply",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing cleanup", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
