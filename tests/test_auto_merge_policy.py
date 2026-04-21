from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class AutoMergePolicyTests(unittest.TestCase):
    def test_worktree_flow_defines_dev_auto_merge_gates(self) -> None:
        text = (REPO_ROOT / "skills" / "worktree-flow" / "SKILL.md").read_text()
        self.assertIn("## Auto-Merge Policy", text)
        self.assertIn("gh pr merge --auto", text)
        self.assertIn("release PRs into `main`", text)
        self.assertIn("explicit user approval", text)

    def test_suite_index_exposes_auto_merge_policy(self) -> None:
        text = (REPO_ROOT / "skills" / "ora-et-labora" / "SKILL.md").read_text()
        self.assertIn("Implementation PRs into `dev` may use agent auto-merge", text)
        self.assertIn("Release PRs into `main` require explicit user approval", text)

    def test_pr_templates_include_auto_merge_eligibility(self) -> None:
        bootstrap_template = (
            REPO_ROOT
            / "skills"
            / "ora-et-labora"
            / "assets"
            / "bootstrap"
            / ".github"
            / "PULL_REQUEST_TEMPLATE.md"
        ).read_text()
        rendered_template = (
            REPO_ROOT / "skills" / "ora-et-labora" / "assets" / "templates" / "pr.md"
        ).read_text()
        self.assertIn("## Auto-Merge Eligibility", bootstrap_template)
        self.assertIn("Agent auto-merge requested", bootstrap_template)
        self.assertIn("## Auto-Merge Eligibility", rendered_template)
        self.assertIn("{{AUTO_MERGE_ELIGIBILITY}}", rendered_template)


if __name__ == "__main__":
    unittest.main()
