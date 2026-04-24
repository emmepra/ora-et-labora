from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TemplateEnforcementPolicyTests(unittest.TestCase):
    def test_issue_shaping_requires_issue_wrapper(self) -> None:
        text = (REPO_ROOT / "skills" / "issue-shaping" / "SKILL.md").read_text()
        self.assertIn("create_issue_from_template.py", text)

    def test_worktree_flow_requires_pr_wrapper(self) -> None:
        text = (REPO_ROOT / "skills" / "worktree-flow" / "SKILL.md").read_text()
        self.assertIn("create_pr_from_template.py", text)

    def test_suite_index_mentions_issue_and_pr_wrappers(self) -> None:
        text = (REPO_ROOT / "skills" / "ora-et-labora" / "SKILL.md").read_text()
        self.assertIn("create_issue_from_template.py", text)
        self.assertIn("create_pr_from_template.py", text)

    def test_wrapper_scripts_use_body_file_creation(self) -> None:
        issue_script = (
            REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "create_issue_from_template.py"
        ).read_text()
        pr_script = (
            REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "create_pr_from_template.py"
        ).read_text()
        self.assertIn("--body-file", issue_script)
        self.assertIn("--body-file", pr_script)

    def test_validate_workflow_runs_pr_body_gate(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
        self.assertIn("Validate PR body", workflow)
        self.assertIn("skills/ora-et-labora/scripts/validate_pr_body.py", workflow)
        self.assertIn("--base-branch \"$BASE_BRANCH\"", workflow)

    def test_skill_contains_pr_body_validator(self) -> None:
        validator = (REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "validate_pr_body.py")
        self.assertTrue(validator.exists())

    def test_repo_init_and_bootstrap_reference_governance_helper(self) -> None:
        repo_init = (REPO_ROOT / "skills" / "repo-init" / "SKILL.md").read_text()
        repo_bootstrap = (REPO_ROOT / "skills" / "repo-bootstrap" / "SKILL.md").read_text()
        self.assertIn("configure_repo_governance.py", repo_init)
        self.assertIn("configure_repo_governance.py", repo_bootstrap)


if __name__ == "__main__":
    unittest.main()
