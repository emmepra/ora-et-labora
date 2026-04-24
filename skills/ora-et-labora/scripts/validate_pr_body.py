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
REQUIRED_RELEASE_CHECK_PREFIXES = (
    "- Regression:",
    "- Browser verification:",
    "- CI status:",
    "- Migrations / schema:",
)
RELEASE_REQUIRED_HEADERS = (
    "## Release Scope",
    "## Included PRs",
    "## Release Checks",
    "## Notes",
    "## Rollback",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body-file", type=Path)
    group.add_argument("--body")
    parser.add_argument("--base-branch", default="")
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


def validate_body(
    body: str,
    template_path: Optional[Path],
    *,
    mode: str = "implementation",
) -> list[str]:
    errors: list[str] = []

    placeholders = sorted(set(PLACEHOLDER_RE.findall(body)))
    if placeholders:
        errors.append(
            "PR body contains unresolved template placeholders: " + ", ".join(placeholders)
        )

    sections = extract_sections(body)
    if template_path is not None:
        required_headers = load_required_headers(template_path)
    elif mode == "release":
        required_headers = list(RELEASE_REQUIRED_HEADERS)
    else:
        raise ValueError("template_path is required for implementation PR validation")

    for header in required_headers:
        if header not in sections:
            errors.append(f"Missing required section header: {header}")
            continue
        if not sections[header]:
            errors.append(f"Section is empty: {header}")

    if mode == "implementation":
        linked_issue = sections.get("## Linked Issue", "")
        if linked_issue and not re.search(r"(?im)\bcloses\s+#\d+\b", linked_issue):
            errors.append("Linked Issue section must contain a `Closes #<issue>` reference.")

        verification = sections.get("## Verification", "")
        for prefix in REQUIRED_VERIFICATION_PREFIXES:
            if verification and prefix not in verification:
                errors.append(f"Verification section is missing required line prefix: {prefix}")
    else:
        release_checks = sections.get("## Release Checks", "")
        for prefix in REQUIRED_RELEASE_CHECK_PREFIXES:
            if release_checks and prefix not in release_checks:
                errors.append(f"Release Checks section is missing required line prefix: {prefix}")

    return errors


def default_implementation_template_path(script_path: Path) -> Path:
    candidates = [
        script_path.resolve().parents[1] / "assets" / "templates" / "pr.md",
        script_path.resolve().parents[1] / ".github" / "PULL_REQUEST_TEMPLATE.md",
        script_path.resolve().parents[2] / ".github" / "PULL_REQUEST_TEMPLATE.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not locate a PR template. Pass --template explicitly or ensure the Ora et Labora PR template is present."
    )


def default_release_template_path(script_path: Path) -> Optional[Path]:
    candidates = [
        script_path.resolve().parents[1] / "assets" / "templates" / "release-pr.md",
        script_path.resolve().parents[1] / ".github" / "release-pr.md",
        script_path.resolve().parents[2] / ".github" / "release-pr.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def resolve_mode(base_branch: str, body: str) -> str:
    if base_branch == "main":
        return "release"
    if "## Release Scope" in body and "## Release Checks" in body:
        return "release"
    return "implementation"


def main() -> int:
    args = parse_args()
    body = load_body(args)
    mode = resolve_mode(args.base_branch.strip(), body)
    if args.template is not None:
        template_path = args.template
    elif mode == "release":
        template_path = default_release_template_path(Path(__file__))
    else:
        template_path = default_implementation_template_path(Path(__file__))
    errors = validate_body(body, template_path, mode=mode)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PR body matches the Ora et Labora {mode} PR contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
