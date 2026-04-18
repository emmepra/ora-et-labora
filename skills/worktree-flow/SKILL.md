---
name: worktree-flow
description: Manage branch naming, worktree lifecycle, PR-first integration into `dev`, and Docker coexistence across worktrees. Use when Codex needs to create or resume a worktree, choose a task branch name, handle Docker stacks while switching worktrees, or prepare an implementation PR to `dev`.
---

# worktree-flow

Use this skill for the implementation branch lifecycle.

## Overview

Own the branch/worktree lifecycle, PR-first integration into `dev`, and Docker coexistence across worktrees.

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

## Default Worktree Flow

1. create or reuse the worktree
2. run commands from that worktree root
3. keep the implementation PR targeting `dev`
4. keep the branch rebased on `origin/dev` as needed

## Docker Rules

- default mode is one active Docker stack across worktrees
- parallel stacks require explicit isolation for compose project name, ports, and service/container naming
- durable Docker runtime rules belong in blueprint docs, not only in chat

## Default Mode

Use one active local Docker or Compose stack at a time across worktrees unless the project explicitly supports parallel stacks.

Recommended switching pattern:

- `docker compose -p <active-worktree> down`
- `docker compose -p <next-worktree> up -d`

## Parallel Mode

Run multiple worktree stacks only when all of these are true:

- each worktree uses a unique compose project name
- each worktree has unique host ports
- service discovery or network naming does not collide
- the repo avoids fixed `container_name` values, or makes them worktree-specific

Accepted naming approaches:

- `docker compose -p <worktree-name> ...`
- `COMPOSE_PROJECT_NAME=<worktree-name> docker compose ...`

## Required Isolation Surfaces

For parallel mode, the repo should define:

- compose project naming rule
- port override strategy
- env-file or override-file strategy per worktree
- service/container naming rule

These rules belong in `.project/blueprint/`, not just in chat.

## After Code Sync

After `git pull`, `git rebase`, or merging changes from `dev`, rebuild or restart the affected services before claiming current behavior.

Do not trust stale containers or frontend bundles after sync.

## Common Mistakes

- assuming Docker runtime policy instead of reading the project blueprint
- running parallel stacks with colliding ports or fixed container names
- working from the main checkout after creating a worktree

## Handoff

Once implementation is ready for checks, move to `verify-and-evidence`.
