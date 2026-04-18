#!/usr/bin/env python3
"""Install or update the Ora et Labora suite from a local clone into CODEX_HOME/skills."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        target = args.dest / skill_dir.name
        if target.exists():
            if not args.overwrite:
                raise SystemExit(f"Destination exists; rerun with --overwrite: {target}")
            shutil.rmtree(target)
        shutil.copytree(skill_dir, target)
        print(f"Synced {skill_dir.name} -> {target}")

    print("Restart Codex to pick up synced skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
