---
name: worktree-flow
description: Manage branch naming, worktree lifecycle, PR-first integration into `dev`, and Docker coexistence across worktrees. Use when Codex needs to create or resume a worktree, choose a task branch name, handle Docker stacks while switching worktrees, or prepare an implementation PR to `dev`.
---

# worktree-flow

Use this skill for the implementation branch lifecycle.

## Responsibilities

- create or resume the worktree
- enforce branch naming
- keep implementation PRs targeting `dev`
- manage Docker runtime behavior across worktrees

## Rules

- one task branch per worktree
- prefer branch names:
  - `feat/<issue>-<slug>`
  - `fix/<issue>-<slug>`
  - `chore/<issue>-<slug>`
  - `hotfix/<issue>-<slug>`
- worktree folder names should avoid slashes
- PR-first integration into `dev`

## Docker Rules

- default mode is one active Docker stack across worktrees
- parallel stacks require explicit isolation for compose project name, ports, and service/container naming
- durable Docker runtime rules belong in blueprint docs, not only in chat

## Resources

- read `../ora-et-labora/references/docker-worktrees.md`
- read `../ora-et-labora/references/workflow.md`

## Handoff

Once implementation is ready for checks, move to `verify-and-evidence`.
