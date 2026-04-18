from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "project-lifecycle" / "scripts" / "bootstrap_repo_templates.py"


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
            self.assertTrue((repo_root / ".project" / "blueprint" / "00_workflow.md").exists())


if __name__ == "__main__":
    unittest.main()
