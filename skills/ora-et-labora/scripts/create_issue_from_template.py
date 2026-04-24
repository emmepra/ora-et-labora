#!/usr/bin/env python3
"""Render an issue template and create a GitHub issue from the body file."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from render_template import parse_vars, render


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--body-out", type=Path, required=True)
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--var", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = render(args.template.read_text(), parse_vars(args.var))
    args.body_out.parent.mkdir(parents=True, exist_ok=True)
    args.body_out.write_text(body)

    if args.dry_run:
        print(args.body_out)
        return 0

    cmd = [
        "gh",
        "issue",
        "create",
        "--repo",
        args.repo,
        "--title",
        args.title,
        "--body-file",
        str(args.body_out),
    ]
    for label in args.label:
        cmd.extend(["--label", label])
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
