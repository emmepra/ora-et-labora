from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "ora-et-labora" / "scripts" / "collect_playwright_artifacts.py"


class CollectPlaywrightArtifactsTests(unittest.TestCase):
    def test_collects_artifacts_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "trace.zip"
            source.write_text("fake-trace")

            result = subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--module-id",
                    "123",
                    "--status",
                    "pass",
                    "--summary",
                    "Login flow verified",
                    "--run-id",
                    "20260418T120000Z",
                    "--source",
                    str(source),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            run_dir = Path(result.stdout.strip())
            manifest = json.loads((run_dir / "manifest.json").read_text())
            self.assertEqual(manifest["module_id"], "123")
            self.assertEqual(manifest["copied_items"], ["trace.zip"])
            self.assertTrue((run_dir / "trace.zip").exists())


if __name__ == "__main__":
    unittest.main()
