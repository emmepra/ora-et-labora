#!/usr/bin/env python3
"""Validate the entire Ora et Labora suite."""

from __future__ import annotations

import subprocess
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skill_creator_root = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
    validator = skill_creator_root / "scripts" / "quick_validate.py"
    tests_dir = repo_root / "tests"
    skills_dir = repo_root / "skills"

    subprocess.run(["python", "-m", "unittest"], cwd=tests_dir, check=True)
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        subprocess.run(["python", str(validator), str(skill_dir)], cwd=repo_root, check=True)
    print("Ora et Labora suite is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
