#!/usr/bin/env python3
"""Retire merged local task state and clean up the owning worktree and local branch."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional


PROTECTED_BRANCHES = {"main", "dev"}
WORK_BRANCH_PREFIXES = ("feat/", "fix/", "chore/", "hotfix/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--module-id", required=True)
    parser.add_argument("--branch", help="Owning local branch. Defaults to the branch recorded in CURRENT.md.")
    parser.add_argument(
        "--merged-into",
        default="origin/dev",
        help="Target branch/ref that must already contain the task branch before cleanup.",
    )
    parser.add_argument(
        "--archive-root",
        help="Optional local archive root relative to repo root. When omitted, task state is deleted instead of archived.",
    )
    parser.add_argument("--keep-worktree", action="store_true")
    parser.add_argument("--keep-branch", action="store_true")
    parser.add_argument("--keep-todo", action="store_true")
    parser.add_argument("--prune-merged-branches", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def path_for_module(repo_root: Path, module_id: str) -> tuple[Path, Path]:
    todo_dir = repo_root / ".project" / "todo" / module_id
    log_path = repo_root / ".project" / "logs" / f"{module_id}.md"
    return todo_dir, log_path


def worktree_paths_for_module(repo_root: Path, module_id: str) -> list[tuple[Path, Path]]:
    worktrees_root = repo_root / ".project" / "worktrees"
    if not worktrees_root.exists():
        return []
    matches: list[tuple[Path, Path]] = []
    for current_path in sorted(worktrees_root.glob(f"*/.project/todo/{module_id}/CURRENT.md")):
        todo_dir = current_path.parent
        worktree_root = current_path.parents[3]
        matches.append((todo_dir, worktree_root))
    return matches


def detect_branch(todo_dir: Path) -> Optional[str]:
    current = todo_dir / "CURRENT.md"
    if not current.exists():
        return None
    for line in current.read_text().splitlines():
        if line.startswith("- Branch:"):
            return line.split(":", 1)[1].strip()
    return None


def branch_exists(repo_root: Path, branch: str) -> bool:
    result = git(repo_root, "show-ref", "--verify", f"refs/heads/{branch}", check=False)
    return result.returncode == 0


def ref_exists(repo_root: Path, ref: str) -> bool:
    result = git(repo_root, "rev-parse", "--verify", ref, check=False)
    return result.returncode == 0


def branch_is_merged(repo_root: Path, branch: str, merged_into: str) -> bool:
    result = git(repo_root, "merge-base", "--is-ancestor", branch, merged_into, check=False)
    return result.returncode == 0


def worktree_path(repo_root: Path, branch: str) -> Path:
    return repo_root / ".project" / "worktrees" / branch.replace("/", "-")


def current_git_branch(repo_root: Path) -> str:
    return git(repo_root, "branch", "--show-current").stdout.strip()


def resolve_task_state(
    repo_root: Path,
    module_id: str,
    branch: Optional[str],
) -> tuple[str, Path, Path, Path]:
    repo_todo_dir, repo_log_path = path_for_module(repo_root, module_id)
    if repo_todo_dir.exists():
        detected = branch or detect_branch(repo_todo_dir)
        if detected:
            return detected, repo_todo_dir, repo_log_path, worktree_path(repo_root, detected)

    worktree_matches = worktree_paths_for_module(repo_root, module_id)
    if branch:
        for todo_dir, worktree_root in worktree_matches:
            if detect_branch(todo_dir) == branch:
                return (
                    branch,
                    todo_dir,
                    worktree_root / ".project" / "logs" / f"{module_id}.md",
                    worktree_root,
                )
    else:
        detected_matches = [
            (detected_branch, todo_dir, worktree_root)
            for todo_dir, worktree_root in worktree_matches
            if (detected_branch := detect_branch(todo_dir))
        ]
        if len(detected_matches) == 1:
            detected_branch, todo_dir, worktree_root = detected_matches[0]
            return (
                detected_branch,
                todo_dir,
                worktree_root / ".project" / "logs" / f"{module_id}.md",
                worktree_root,
            )
        if len(detected_matches) > 1:
            choices = ", ".join(sorted(match[0] for match in detected_matches))
            raise SystemExit(
                f"Multiple worktree task states found for module {module_id!r}. Pass --branch explicitly. Choices: {choices}"
            )

    raise SystemExit(
        "Could not determine branch. Pass --branch explicitly or ensure CURRENT.md records it."
    )


def update_current_for_archive(current_path: Path, archive_rel: str) -> None:
    if not current_path.exists():
        return
    lines = current_path.read_text().splitlines()
    replacements = {
        "- Status:": "- Status: merged and archived",
        "- Next step:": "- Next step: none; cleanup complete",
        "- Blockers:": "- Blockers: none",
    }
    new_lines = []
    for line in lines:
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                new_lines.append(value)
                replaced = True
                break
        if not replaced:
            new_lines.append(line)
    new_lines.append(f"- Archive: {archive_rel}")
    current_path.write_text("\n".join(new_lines) + "\n")


def append_log(log_path: Path, message: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as handle:
        handle.write(message)


def ensure_root_log(log_path: Path, source_log_path: Path, module_id: str) -> None:
    if log_path.exists():
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if source_log_path.exists() and source_log_path != log_path:
        shutil.copy2(source_log_path, log_path)
        return
    log_path.write_text(f"# Task Log: {module_id}\n")


def active_worktree_branches(repo_root: Path) -> set[str]:
    result = git(repo_root, "worktree", "list", "--porcelain")
    branches: set[str] = set()
    for line in result.stdout.splitlines():
        if line.startswith("branch refs/heads/"):
            branches.add(line.removeprefix("branch refs/heads/"))
    return branches


def local_branches(repo_root: Path) -> list[str]:
    result = git(repo_root, "for-each-ref", "--format=%(refname:short)", "refs/heads")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def prune_candidates(repo_root: Path, merged_into: str, exclude: set[str]) -> list[str]:
    candidates: list[str] = []
    active = active_worktree_branches(repo_root)
    for branch in local_branches(repo_root):
        if branch in PROTECTED_BRANCHES or branch in exclude or branch in active:
            continue
        if not branch.startswith(WORK_BRANCH_PREFIXES):
            continue
        if not branch_is_merged(repo_root, branch, merged_into):
            continue
        candidates.append(branch)
    return sorted(candidates)


def plan_lines(
    *,
    module_id: str,
    branch: str,
    merged_into: str,
    merged: bool,
    todo_dir: Path,
    archive_dir: Optional[Path],
    worktree_dir: Path,
    keep_todo: bool,
    keep_worktree: bool,
    keep_branch: bool,
    prune_candidates_list: list[str],
) -> list[str]:
    lines = [
        f"Cleanup plan for module {module_id}",
        f"- branch: {branch}",
        f"- merged into {merged_into}: {'yes' if merged else 'no'}",
        f"- todo dir: {todo_dir}",
        f"- task-state cleanup: {'archive to ' + str(archive_dir) if archive_dir else 'delete local todo dir'}",
        f"- worktree dir: {worktree_dir}",
        "",
    ]
    if not keep_todo:
        if archive_dir:
            lines.append(f"$ archive {todo_dir} -> {archive_dir}")
        else:
            lines.append("$ " + shlex.join(["rm", "-rf", str(todo_dir)]))
    if not keep_worktree:
        lines.append("$ " + shlex.join(["git", "worktree", "remove", str(worktree_dir)]))
    if not keep_branch:
        lines.append("$ " + shlex.join(["git", "branch", "-d", branch]))
    if prune_candidates_list:
        lines.append("")
        lines.append("Additional merged branch prune candidates:")
        for candidate in prune_candidates_list:
            lines.append(f"- {candidate}")
    return lines


def ensure_safe_to_apply(repo_root: Path, branch: str, merged: bool, force: bool) -> None:
    if merged or force:
        return
    raise SystemExit(
        f"Refusing cleanup because branch {branch!r} is not merged into the target ref. Use --force to override."
    )


def remove_worktree(repo_root: Path, path: Path, force: bool) -> None:
    if not path.exists():
        return
    cmd = ["worktree", "remove", str(path)]
    if force:
        cmd.insert(2, "--force")
    git(repo_root, *cmd)


def delete_branch(repo_root: Path, branch: str, force: bool) -> None:
    if not branch_exists(repo_root, branch):
        return
    if current_git_branch(repo_root) == branch:
        raise SystemExit(f"Refusing to delete currently checked out branch {branch!r}.")
    git(repo_root, "branch", "-D" if force else "-d", branch)


def retire_task_state(
    todo_dir: Path,
    source_log_path: Path,
    root_log_path: Path,
    module_id: str,
    branch: str,
    merged_into: str,
    archive_dir: Optional[Path],
    archive_rel: Optional[str],
) -> None:
    ensure_root_log(root_log_path, source_log_path, module_id)
    if archive_dir and archive_rel:
        archive_dir.parent.mkdir(parents=True, exist_ok=True)
        if archive_dir.exists():
            raise SystemExit(f"Archive destination already exists: {archive_dir}")
        current_path = todo_dir / "CURRENT.md"
        update_current_for_archive(current_path, archive_rel)
        shutil.move(str(todo_dir), str(archive_dir))
        suffix = f"archive:{archive_rel} | task-state:archived | note:Archived local task workspace after merge cleanup."
    else:
        shutil.rmtree(todo_dir)
        suffix = "task-state:removed | note:Removed local task workspace after merge cleanup."
    append_log(
        root_log_path,
        f"- {date.today().isoformat()} | state:closed | branch:{branch} | merged-into:{merged_into} | {suffix}\n",
    )

def apply_cleanup(
    args: argparse.Namespace,
    branch: str,
    merged: bool,
    source_todo_dir: Path,
    source_log_path: Path,
    root_log_path: Path,
    worktree_dir: Path,
) -> None:
    repo_root = args.repo_root.resolve()
    archive_dir = repo_root / args.archive_root / args.module_id if args.archive_root else None
    archive_rel = str(Path(args.archive_root) / args.module_id) if args.archive_root else None

    ensure_safe_to_apply(repo_root, branch, merged, args.force)
    if not args.keep_todo:
        retire_task_state(
            source_todo_dir,
            source_log_path,
            root_log_path,
            args.module_id,
            branch,
            args.merged_into,
            archive_dir,
            archive_rel,
        )
    if not args.keep_worktree:
        remove_worktree(repo_root, worktree_dir, args.force)
    if not args.keep_branch:
        delete_branch(repo_root, branch, args.force)
    if args.prune_merged_branches:
        extra_candidates = prune_candidates(repo_root, args.merged_into, exclude={branch})
        for candidate in extra_candidates:
            delete_branch(repo_root, candidate, args.force)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    branch, source_todo_dir, source_log_path, worktree_dir = resolve_task_state(
        repo_root,
        args.module_id,
        args.branch,
    )
    _, root_log_path = path_for_module(repo_root, args.module_id)

    merged_ref = args.merged_into if ref_exists(repo_root, args.merged_into) else args.merged_into.removeprefix("origin/")
    merged = branch_exists(repo_root, branch) and ref_exists(repo_root, merged_ref) and branch_is_merged(repo_root, branch, merged_ref)
    archive_dir = repo_root / args.archive_root / args.module_id if args.archive_root else None
    prune_list = prune_candidates(repo_root, merged_ref, exclude={branch}) if args.prune_merged_branches else []

    if not args.apply:
        sys.stdout.write(
            "\n".join(
                plan_lines(
                    module_id=args.module_id,
                    branch=branch,
                    merged_into=merged_ref,
                    merged=merged,
                    todo_dir=source_todo_dir,
                    archive_dir=archive_dir,
                    worktree_dir=worktree_dir,
                    keep_todo=args.keep_todo,
                    keep_worktree=args.keep_worktree,
                    keep_branch=args.keep_branch,
                    prune_candidates_list=prune_list,
                )
            )
            + "\n"
        )
        return 0

    apply_cleanup(
        args,
        branch,
        merged,
        source_todo_dir,
        source_log_path,
        root_log_path,
        worktree_dir,
    )
    print(f"Closed and cleaned up task workspace for module {args.module_id}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
