from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "bootstrap_repo_templates.py"


class BootstrapRepoTemplatesTests(unittest.TestCase):
    def test_copies_bootstrap_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                ],
                check=True,
            )

            self.assertTrue((repo_root / ".github" / "PULL_REQUEST_TEMPLATE.md").exists())
            self.assertTrue((repo_root / ".github" / "ISSUE_TEMPLATE" / "config.yml").exists())
            self.assertTrue((repo_root / ".github" / "workflows" / "validate-pr-body.yml").exists())
            self.assertTrue((repo_root / ".project" / "blueprint" / "00_workflow.md").exists())
            self.assertTrue((repo_root / "scripts" / "validate_pr_body.py").exists())
            pr_template = (repo_root / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text()
            issue_config = (repo_root / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text()
            pr_workflow = (repo_root / ".github" / "workflows" / "validate-pr-body.yml").read_text()
            self.assertIn("## Linked Issue", pr_template)
            self.assertIn("Closes #", pr_template)
            self.assertIn("blank_issues_enabled: false", issue_config)
            self.assertIn("python scripts/validate_pr_body.py", pr_workflow)
            gitignore = (repo_root / ".gitignore").read_text()
            self.assertIn("Visibility profile: private", gitignore)
            self.assertIn(".project/worktrees/", gitignore)
            self.assertNotIn("\n.project/\n", f"\n{gitignore}")

            body = repo_root / "body.md"
            body.write_text(
                """## Summary

- Bootstrapped smoke test.

## Why

Ensure the copied validator runs in a target repo.

## Linked Issue

Closes #1

## Verification

- Local: smoke
- Browser: not applicable
- Browser evidence: not applicable
- CI: pending

## Auto-Merge Eligibility

- Not applicable.

## Blueprint Updates

None.

## Risks / Rollback

Revert the bootstrap if needed.

## Follow-ups

- None.
"""
            )
            subprocess.run(
                [
                    "python",
                    str(repo_root / "scripts" / "validate_pr_body.py"),
                    "--body-file",
                    str(body),
                ],
                check=True,
                cwd=repo_root,
            )

            release_body = repo_root / "release-body.md"
            release_body.write_text(
                """## Release Scope

- Promote a workflow-only release to main.

## Included PRs

- #1

## Release Checks

- Regression: smoke
- Browser verification: not applicable
- CI status: pending
- Migrations / schema: not applicable

## Notes

- Workflow-only release.

## Rollback

Revert the release merge commit on main if needed.
"""
            )
            subprocess.run(
                [
                    "python",
                    str(repo_root / "scripts" / "validate_pr_body.py"),
                    "--body-file",
                    str(release_body),
                    "--base-branch",
                    "main",
                ],
                check=True,
                cwd=repo_root,
            )

    def test_public_visibility_keeps_project_state_local(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                    "--visibility",
                    "public",
                ],
                check=True,
            )

            gitignore = (repo_root / ".gitignore").read_text()
            self.assertIn("Visibility profile: public", gitignore)
            self.assertIn(".project/", gitignore)
            self.assertIn("AGENTS.local.md", gitignore)
            self.assertIn("playwright-report/", gitignore)

    def test_visibility_policy_replaces_existing_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                    "--visibility",
                    "private",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                    "--visibility",
                    "public",
                    "--force",
                ],
                check=True,
            )

            gitignore = (repo_root / ".gitignore").read_text()
            self.assertEqual(gitignore.count("BEGIN Ora et Labora artifact policy"), 1)
            self.assertIn("Visibility profile: public", gitignore)
            self.assertNotIn("Visibility profile: private", gitignore)


if __name__ == "__main__":
    unittest.main()
