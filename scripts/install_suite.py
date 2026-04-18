#!/usr/bin/env python3
"""Install the Ora et Labora suite from GitHub using the Codex skill installer."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


SKILL_PATHS = [
    "skills/ora-et-labora",
    "skills/issue-shaping",
    "skills/blueprint-guard",
    "skills/state-logging",
    "skills/worktree-flow",
    "skills/verify-and-evidence",
    "skills/release-train",
    "skills/repo-bootstrap",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="emmepra/ora-et-labora")
    parser.add_argument("--ref", help="Optional git ref to install from.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    installer = codex_home / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
    cmd = ["python", str(installer), "--repo", args.repo]
    if args.ref:
        cmd.extend(["--ref", args.ref])
    for path in SKILL_PATHS:
        cmd.extend(["--path", path])
    subprocess.run(cmd, check=True)
    print("Restart Codex to pick up the installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
