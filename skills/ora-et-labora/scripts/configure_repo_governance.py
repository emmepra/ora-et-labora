#!/usr/bin/env python3
"""Plan or apply standard GitHub repo governance for Ora et Labora repos."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_LABELS = (
    {"name": "bug", "color": "d73a4a", "description": "Something is broken or behaves incorrectly."},
    {"name": "enhancement", "color": "a2eeef", "description": "New feature or capability."},
    {"name": "chore", "color": "cfd3d7", "description": "Maintenance or workflow upkeep."},
    {"name": "docs", "color": "0075ca", "description": "Documentation-only change or request."},
    {"name": "release", "color": "5319e7", "description": "Release train, promotion, or rollout work."},
    {"name": "blocked", "color": "b60205", "description": "Cannot proceed until an external blocker is cleared."},
    {"name": "hold", "color": "fbca04", "description": "Explicitly paused or waiting for user decision."},
    {
        "name": "needs-verification",
        "color": "1d76db",
        "description": "Implementation exists but required verification evidence is still missing.",
    },
)


@dataclass(frozen=True)
class GovernanceSettings:
    repo: str
    default_branch: str
    stable_branch: str
    delete_branch_on_merge: bool
    enable_auto_merge: bool
    allow_update_branch: bool
    enable_merge_commit: bool
    enable_squash_merge: bool
    enable_rebase_merge: bool
    include_settings: bool
    include_labels: bool
    apply: bool


def parse_args() -> GovernanceSettings:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository in OWNER/REPO form.")
    parser.add_argument("--default-branch", default="dev")
    parser.add_argument("--stable-branch", default="main")
    parser.add_argument("--skip-settings", action="store_true")
    parser.add_argument("--skip-labels", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Execute commands instead of printing the plan.")

    parser.add_argument(
        "--delete-branch-on-merge",
        dest="delete_branch_on_merge",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--keep-branch-on-merge",
        dest="delete_branch_on_merge",
        action="store_false",
    )
    parser.add_argument(
        "--enable-auto-merge",
        dest="enable_auto_merge",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--disable-auto-merge",
        dest="enable_auto_merge",
        action="store_false",
    )
    parser.add_argument(
        "--allow-update-branch",
        dest="allow_update_branch",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--disallow-update-branch",
        dest="allow_update_branch",
        action="store_false",
    )
    parser.add_argument(
        "--enable-merge-commit",
        dest="enable_merge_commit",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--disable-merge-commit",
        dest="enable_merge_commit",
        action="store_false",
    )
    parser.add_argument(
        "--enable-squash-merge",
        dest="enable_squash_merge",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--disable-squash-merge",
        dest="enable_squash_merge",
        action="store_false",
    )
    parser.add_argument(
        "--enable-rebase-merge",
        dest="enable_rebase_merge",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--disable-rebase-merge",
        dest="enable_rebase_merge",
        action="store_false",
    )

    args = parser.parse_args()
    return GovernanceSettings(
        repo=args.repo,
        default_branch=args.default_branch,
        stable_branch=args.stable_branch,
        delete_branch_on_merge=args.delete_branch_on_merge,
        enable_auto_merge=args.enable_auto_merge,
        allow_update_branch=args.allow_update_branch,
        enable_merge_commit=args.enable_merge_commit,
        enable_squash_merge=args.enable_squash_merge,
        enable_rebase_merge=args.enable_rebase_merge,
        include_settings=not args.skip_settings,
        include_labels=not args.skip_labels,
        apply=args.apply,
    )


def append_toggle(cmd: list[str], flag: str, enabled: bool) -> None:
    cmd.append(flag if enabled else f"{flag}=false")


def build_repo_edit_command(settings: GovernanceSettings) -> list[str]:
    cmd = ["gh", "repo", "edit", settings.repo, "--default-branch", settings.default_branch]
    append_toggle(cmd, "--delete-branch-on-merge", settings.delete_branch_on_merge)
    append_toggle(cmd, "--enable-auto-merge", settings.enable_auto_merge)
    append_toggle(cmd, "--allow-update-branch", settings.allow_update_branch)
    append_toggle(cmd, "--enable-merge-commit", settings.enable_merge_commit)
    append_toggle(cmd, "--enable-squash-merge", settings.enable_squash_merge)
    append_toggle(cmd, "--enable-rebase-merge", settings.enable_rebase_merge)
    return cmd


def build_label_command(repo: str, label: dict[str, str]) -> list[str]:
    return [
        "gh",
        "label",
        "create",
        label["name"],
        "--repo",
        repo,
        "--color",
        label["color"],
        "--description",
        label["description"],
        "--force",
    ]


def build_commands(settings: GovernanceSettings) -> list[list[str]]:
    commands: list[list[str]] = []
    if settings.include_settings:
        commands.append(build_repo_edit_command(settings))
    if settings.include_labels:
        commands.extend(build_label_command(settings.repo, label) for label in DEFAULT_LABELS)
    return commands


def format_plan(settings: GovernanceSettings) -> str:
    lines = [
        f"Governance plan for {settings.repo}",
        f"- default branch: {settings.default_branch}",
        f"- stable branch (expected): {settings.stable_branch}",
        f"- repo settings: {'apply' if settings.include_settings else 'skip'}",
        f"- default labels: {'apply' if settings.include_labels else 'skip'}",
        "- branch protections/rulesets: pending by design; handled in a later automation slice",
        "",
    ]
    for cmd in build_commands(settings):
        lines.append("$ " + shlex.join(cmd))
    return "\n".join(lines) + "\n"


def run_commands(commands: list[list[str]]) -> None:
    for cmd in commands:
        subprocess.run(cmd, check=True)


def main() -> int:
    settings = parse_args()
    commands = build_commands(settings)
    if not settings.apply:
        sys.stdout.write(format_plan(settings))
        return 0

    run_commands(commands)
    print(f"Applied Ora et Labora governance defaults to {settings.repo}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
