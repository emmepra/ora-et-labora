## Summary

- add `close_task_workspace.py` to archive merged task workspaces and retire the owning worktree/local branch through a dry-run-first flow
- add regression tests for dry-run planning, apply cleanup, and unmerged-branch refusal
- wire the cleanup flow into the README, suite index, and relevant execution skills

## Why

Phase 2 closes the post-merge gap in Ora et Labora. The suite could shape work and drive PRs into `dev`, but it had no standard way to archive finished task state or retire merged worktrees and local branches.

## Linked Issue

Closes #17

## Verification

- Local: `python scripts/validate_all.py`
- Browser: Not applicable; workflow/docs/scripts only.
- Browser evidence: Not applicable.
- CI: Pending GitHub `validate`.

## Auto-Merge Eligibility

- Eligible for implementation auto-merge into `dev` after `validate` passes.
- Branch is current with `origin/dev` before push.
- Local verification is recorded in `.project/todo/17/CURRENT.md` and `.project/logs/17.md`.
- Browser verification is not applicable for this workflow/docs/scripts change.

## Blueprint Updates

None.

## Risks / Rollback

Low risk and limited to workflow helpers, documentation, and regression tests. Roll back by reverting the cleanup helper, wrapper, and associated docs/tests.

## Follow-ups

- Continue the roadmap with the public-mode audit gate.
