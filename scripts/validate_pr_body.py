#!/usr/bin/env python3
"""Validate a PR body against the Ora et Labora PR template contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
REQUIRED_VERIFICATION_PREFIXES = (
    "- Local:",
    "- Browser:",
    "- Browser evidence:",
    "- CI:",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body-file", type=Path)
    group.add_argument("--body")
    parser.add_argument("--template", type=Path)
    return parser.parse_args()


def load_body(args: argparse.Namespace) -> str:
    if args.body_file is not None:
        return args.body_file.read_text()
    return args.body


def load_required_headers(template_path: Path) -> list[str]:
    return [line.strip() for line in template_path.read_text().splitlines() if line.startswith("## ")]


def extract_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_header: Optional[str] = None
    current_lines: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line.strip()
            current_lines = []
            continue
        if current_header is not None:
            current_lines.append(line)

    if current_header is not None:
        sections[current_header] = "\n".join(current_lines).strip()
    return sections


def validate_body(body: str, template_path: Path) -> list[str]:
    errors: list[str] = []

    placeholders = sorted(set(PLACEHOLDER_RE.findall(body)))
    if placeholders:
        errors.append(
            "PR body contains unresolved template placeholders: " + ", ".join(placeholders)
        )

    sections = extract_sections(body)
    required_headers = load_required_headers(template_path)
    for header in required_headers:
        if header not in sections:
            errors.append(f"Missing required section header: {header}")
            continue
        if not sections[header]:
            errors.append(f"Section is empty: {header}")

    linked_issue = sections.get("## Linked Issue", "")
    if linked_issue and not re.search(r"(?im)\bcloses\s+#\d+\b", linked_issue):
        errors.append("Linked Issue section must contain a `Closes #<issue>` reference.")

    verification = sections.get("## Verification", "")
    for prefix in REQUIRED_VERIFICATION_PREFIXES:
        if verification and prefix not in verification:
            errors.append(f"Verification section is missing required line prefix: {prefix}")

    return errors


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    template_path = args.template or repo_root / "skills" / "ora-et-labora" / "assets" / "templates" / "pr.md"
    body = load_body(args)
    errors = validate_body(body, template_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PR body matches the Ora et Labora template contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
