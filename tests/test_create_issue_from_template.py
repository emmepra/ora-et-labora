from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "create_issue_from_template.py"


class CreateIssueFromTemplateTests(unittest.TestCase):
    def test_renders_issue_body_in_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            template = tmpdir / "issue.md"
            body_out = tmpdir / "body.md"
            template.write_text("Problem: {{PROBLEM}}\n")
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo",
                    "owner/repo",
                    "--title",
                    "Example issue",
                    "--template",
                    str(template),
                    "--body-out",
                    str(body_out),
                    "--var",
                    "PROBLEM=missing template enforcement",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(body_out.read_text(), "Problem: missing template enforcement\n")


if __name__ == "__main__":
    unittest.main()
