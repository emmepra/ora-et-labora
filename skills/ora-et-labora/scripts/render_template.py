#!/usr/bin/env python3
"""Render a markdown template with strict placeholder replacement."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"{{([A-Z0-9_]+)}}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Template variable assignment. Repeat as needed.",
    )
    return parser.parse_args()


def parse_vars(items: list[str]) -> dict[str, str]:
    data: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Invalid --var value: {item!r}; expected KEY=VALUE")
        key, value = item.split("=", 1)
        key = key.strip().upper()
        if not key:
            raise SystemExit(f"Invalid empty key in --var value: {item!r}")
        data[key] = value
    return data


def render(template_text: str, data: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in data:
            raise KeyError(key)
        return data[key]

    rendered = PLACEHOLDER_RE.sub(replace, template_text)
    remaining = sorted(set(PLACEHOLDER_RE.findall(rendered)))
    if remaining:
        raise ValueError(f"Unresolved placeholders remain: {', '.join(remaining)}")
    return rendered


def main() -> int:
    args = parse_args()
    template_text = args.template.read_text()
    data = parse_vars(args.var)
    try:
        rendered = render(template_text, data)
    except KeyError as exc:
        missing = exc.args[0]
        print(f"Missing placeholder value for {missing}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
