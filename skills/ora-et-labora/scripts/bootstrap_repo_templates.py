#!/usr/bin/env python3
"""Copy workflow bootstrap templates into a target repo."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def copy_tree(src_root: Path, dst_root: Path, force: bool) -> None:
    for src in src_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        if dst.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file without --force: {dst}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    bootstrap_root = skill_root / "assets" / "bootstrap"
    copy_tree(bootstrap_root, args.repo_root, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
