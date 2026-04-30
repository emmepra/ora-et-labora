from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "configure_repo_governance.py"
SPEC = importlib.util.spec_from_file_location("configure_repo_governance", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ConfigureRepoGovernanceTests(unittest.TestCase):
    def test_build_repo_edit_command_uses_expected_defaults(self) -> None:
        settings = MODULE.GovernanceSettings(
            repo="owner/repo",
            default_branch="dev",
            stable_branch="main",
            delete_branch_on_merge=True,
            enable_auto_merge=True,
            allow_update_branch=True,
            enable_merge_commit=True,
            enable_squash_merge=True,
            enable_rebase_merge=False,
            include_settings=True,
            include_labels=True,
            apply=False,
        )
        cmd = MODULE.build_repo_edit_command(settings)
        self.assertEqual(cmd[:4], ["gh", "repo", "edit", "owner/repo"])
        self.assertIn("--default-branch", cmd)
        self.assertIn("--delete-branch-on-merge", cmd)
        self.assertIn("--enable-auto-merge", cmd)
        self.assertIn("--allow-update-branch", cmd)
        self.assertIn("--enable-merge-commit", cmd)
        self.assertIn("--enable-squash-merge", cmd)
        self.assertIn("--enable-rebase-merge=false", cmd)

    def test_label_bundle_contains_bug_and_enhancement(self) -> None:
        labels = {label["name"] for label in MODULE.DEFAULT_LABELS}
        self.assertIn("bug", labels)
        self.assertIn("enhancement", labels)
        self.assertIn("release", labels)

    def test_dry_run_prints_plan(self) -> None:
        result = subprocess.run(
            [
                "python",
                str(SCRIPT),
                "--repo",
                "owner/repo",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Governance plan for owner/repo", result.stdout)
        self.assertIn("gh repo edit owner/repo --default-branch dev", result.stdout)
        self.assertIn("gh label create bug --repo owner/repo", result.stdout)


if __name__ == "__main__":
    unittest.main()
