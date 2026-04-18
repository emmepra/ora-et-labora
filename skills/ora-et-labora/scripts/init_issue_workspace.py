#!/usr/bin/env python3
"""Initialize branch-local .project state for a task."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--issue-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--kind", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--issue-url", required=True)
    parser.add_argument("--module-id")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def render(template_path: Path, data: dict[str, str]) -> str:
    text = template_path.read_text()
    for key, value in data.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "assets" / "templates"

    module_id = args.module_id or args.issue_id
    data = {
        "DATE": date.today().isoformat(),
        "ISSUE_ID": args.issue_id,
        "ISSUE_URL": args.issue_url,
        "TITLE": args.title,
        "KIND": args.kind,
        "BRANCH": args.branch,
        "MODULE_ID": module_id,
    }

    todo_dir = args.repo_root / ".project" / "todo" / module_id
    log_path = args.repo_root / ".project" / "logs" / f"{module_id}.md"

    write_file(todo_dir / "00_brainstorm.md", render(templates / "brainstorm.md", data), args.force)
    write_file(todo_dir / "CURRENT.md", render(templates / "current.md", data), args.force)
    write_file(log_path, render(templates / "log.md", data), args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
