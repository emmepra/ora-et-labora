#!/usr/bin/env python3
"""Copy workflow bootstrap templates into a target repo."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


BEGIN_MARKER = "# BEGIN Ora et Labora artifact policy"
END_MARKER = "# END Ora et Labora artifact policy"

GITIGNORE_PROFILES = {
    "private": [
        "# Local worktree checkouts are never repository content.",
        ".project/worktrees/",
        "",
        "# Keep browser verification summaries, but do not commit raw Playwright payloads by default.",
        ".project/logs/playwright/**/*.zip",
        ".project/logs/playwright/**/*.webm",
        ".project/logs/playwright/**/*.mp4",
        ".project/logs/playwright/**/*.har",
        ".project/logs/playwright/**/*.png",
        ".project/logs/playwright/**/*.jpg",
        ".project/logs/playwright/**/*.jpeg",
        "playwright-report/",
        "test-results/",
    ],
    "internal": [
        "# Local worktree checkouts are never repository content.",
        ".project/worktrees/",
        "",
        "# Internal repos may keep workflow state, but raw browser artifacts stay local unless curated.",
        ".project/logs/playwright/**/*.zip",
        ".project/logs/playwright/**/*.webm",
        ".project/logs/playwright/**/*.mp4",
        ".project/logs/playwright/**/*.har",
        ".project/logs/playwright/**/*.png",
        ".project/logs/playwright/**/*.jpg",
        ".project/logs/playwright/**/*.jpeg",
        "playwright-report/",
        "test-results/",
    ],
    "public": [
        "# Public repos must not publish agent-private operational state by default.",
        ".project/",
        "AGENTS.local.md",
        ".project.local/",
        "",
        "# Raw browser artifacts are local evidence, not public source material.",
        "playwright-report/",
        "test-results/",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--visibility", choices=sorted(GITIGNORE_PROFILES), default="private")
    parser.add_argument("--skip-gitignore", action="store_true")
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


def copy_file(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def artifact_policy_block(visibility: str) -> str:
    lines = [BEGIN_MARKER, f"# Visibility profile: {visibility}"]
    lines.extend(GITIGNORE_PROFILES[visibility])
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def upsert_gitignore_policy(repo_root: Path, visibility: str) -> None:
    gitignore = repo_root / ".gitignore"
    block = artifact_policy_block(visibility)
    if not gitignore.exists():
        gitignore.write_text(block)
        return

    text = gitignore.read_text()
    begin = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if begin != -1 and end != -1 and begin < end:
        end += len(END_MARKER)
        new_text = text[:begin] + block.rstrip("\n") + text[end:]
        if not new_text.endswith("\n"):
            new_text += "\n"
        gitignore.write_text(new_text)
        return

    separator = "" if text.endswith("\n\n") or text == "" else "\n"
    gitignore.write_text(f"{text}{separator}{block}")


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    bootstrap_root = skill_root / "assets" / "bootstrap"
    copy_tree(bootstrap_root, args.repo_root, args.force)
    copy_file(
        skill_root / "scripts" / "validate_pr_body.py",
        args.repo_root / "scripts" / "validate_pr_body.py",
        args.force,
    )
    if not args.skip_gitignore:
        upsert_gitignore_policy(args.repo_root, args.visibility)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
