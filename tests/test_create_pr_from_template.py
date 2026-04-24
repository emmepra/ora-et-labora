from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "create_pr_from_template.py"


class CreatePrFromTemplateTests(unittest.TestCase):
    def test_renders_pr_body_in_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            template = tmpdir / "pr.md"
            body_out = tmpdir / "body.md"
            template.write_text("Summary: {{SUMMARY}}\n")
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo",
                    "owner/repo",
                    "--title",
                    "Example pr",
                    "--base",
                    "dev",
                    "--head",
                    "feat/example",
                    "--template",
                    str(template),
                    "--body-out",
                    str(body_out),
                    "--var",
                    "SUMMARY=template-enforced pr",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(body_out.read_text(), "Summary: template-enforced pr\n")


if __name__ == "__main__":
    unittest.main()
