#!/usr/bin/env python3
"""Collect browser verification artifacts into a stable repo-local log layout."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--module-id", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--source", action="append", default=[], help="File or directory to copy into the run folder.")
    parser.add_argument("--run-id", help="Optional explicit run id. Defaults to an ISO-like UTC timestamp.")
    parser.add_argument("--note", default="")
    return parser.parse_args()


def copy_source(src: Path, dest_root: Path) -> str:
    if not src.exists():
        raise SystemExit(f"Source path does not exist: {src}")
    dest = dest_root / src.name
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return dest.name


def main() -> int:
    args = parse_args()
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = args.repo_root / ".project" / "logs" / "playwright" / args.module_id / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    copied: list[str] = []
    for raw in args.source:
        copied.append(copy_source(Path(raw), run_dir))

    manifest = {
        "module_id": args.module_id,
        "run_id": run_id,
        "status": args.status,
        "summary": args.summary,
        "note": args.note,
        "copied_items": copied,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (run_dir / "summary.md").write_text(
        "\n".join(
            [
                f"# Playwright Run {run_id}",
                "",
                f"- Status: {args.status}",
                f"- Summary: {args.summary}",
                f"- Note: {args.note or 'none'}",
                f"- Copied items: {', '.join(copied) if copied else 'none'}",
                "",
            ]
        )
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
