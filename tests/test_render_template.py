from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "project-lifecycle" / "scripts" / "render_template.py"


class RenderTemplateTests(unittest.TestCase):
    def test_renders_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            template = tmpdir / "template.md"
            output = tmpdir / "out.md"
            template.write_text("Hello {{NAME}}\n")
            subprocess.run(
                [
                    "python",
                    str(SCRIPT),
                    str(template),
                    "--out",
                    str(output),
                    "--var",
                    "NAME=world",
                ],
                check=True,
            )
            self.assertEqual(output.read_text(), "Hello world\n")


if __name__ == "__main__":
    unittest.main()
