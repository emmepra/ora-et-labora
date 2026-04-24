---
name: worktree-flow
description: Use when creating, resuming, rebasing, validating, or opening PRs from task branches/worktrees, especially when Docker, ports, services, or `dev` integration are involved.
---

# worktree-flow

Use this skill for the implementation branch lifecycle.

## Overview

Worktree flow keeps implementation isolated, reviewable, and safely integrated through PRs into `dev`. It also prevents Docker-backed worktrees from fighting over ports, container names, services, and stale runtime state.

Core principle: one issue owns one branch, one worktree, one PR to `dev`, and one branch-local `.project` state surface.

This skill is self-contained. Follow this file for the worktree and Docker procedure.

## When To Use

Use this skill when:

- starting or resuming implementation for an issue/module
- creating a branch or worktree
- deciding a branch name
- switching between worktrees
- opening, updating, or preparing a PR to `dev`
- rebasing a task branch on `origin/dev`
- running Docker or Compose from multiple worktrees
- diagnosing stale containers, port conflicts, service naming conflicts, or dev-server mismatches

Do not use this skill for:

- pure issue shaping before implementation is allowed
- release PRs from `dev` to `main`
- direct edits in a repo where the user explicitly requested no branch/worktree flow

## Responsibilities

- create or reuse the correct worktree
- enforce deterministic branch and worktree names
- keep commands running from the worktree root
- keep branch-local `.project` updates in the worktree checkout
- open implementation PRs into `dev`
- keep the branch synced with `origin/dev`
- manage Docker runtime behavior across worktrees
- prevent stale runtime state from being mistaken for current behavior
- retire merged task worktrees and local branches through the standard cleanup helper when the work is complete

## Quick Reference

| Need | Pattern |
| --- | --- |
| Feature branch | `feat/<issue>-<slug>` |
| Bug branch | `fix/<issue>-<slug>` |
| Chore branch | `chore/<issue>-<slug>` |
| Hotfix branch | `hotfix/<issue>-<slug>` |
| Worktree path | `.project/worktrees/<branch-id-without-slashes>` |
| Implementation PR base | `dev` |
| Implementation PR issue link | `Closes #<issue-id>` in the PR body |
| Implementation PR auto-merge | allowed only when all auto-merge gates are satisfied |
| Stable release PR base | `main` |
| Release PR auto-merge | never without explicit user approval |
| Default Docker mode | one active stack across worktrees |
| Parallel Docker mode | only with isolated project names, ports, and container/service names |

## Branch Naming

Choose a branch name that explains both type and issue:

- `feat/123-add-export-flow`
- `fix/124-login-spinner`
- `chore/125-update-ci-node`
- `hotfix/126-prod-auth-redirect`

If there is no issue number yet, do not invent one. Use a stable module ID or short slug, then update the branch only if the project workflow expects issue-numbered branches.

Worktree folder names should avoid slashes:

- branch: `fix/124-login-spinner`
- worktree: `.project/worktrees/fix-124-login-spinner`

## Worktree Procedure

1. Confirm the base branch.
   - Default implementation base is `dev`.
   - Use another base only when the user or project policy requires it.
2. Fetch current remote state.
   - Use `git fetch origin` before creating or rebasing a task branch.
3. Create or reuse the worktree.
   - Preferred location: `.project/worktrees/<worktree-branch-id>`.
   - Reuse existing worktrees for the same branch.
   - Do not create worktrees under `.agents/`, `.claude/`, or other agent tooling folders.
4. Run commands from the worktree root.
   - Use `workdir=<worktree-path>` or `git -C <worktree-path> ...`.
   - Do not accidentally commit from the main checkout.
5. Initialize or update branch-local `.project` state inside the worktree.
   - Write `.project/todo`, `.project/logs`, and `.project/blueprint` in the assigned worktree checkout for branch work.
6. Open a draft PR early when the branch will be active for more than a tiny fix.
   - Base: `dev`.
   - Standard path: use `../ora-et-labora/scripts/create_pr_from_template.py`.
   - Minimum fallback: render a body file first, then use `gh pr create --body-file <file>`.
   - Do not hand-write multi-section PR markdown directly into `gh pr create`.
   - Include `Closes #<issue-id>` or an equivalent GitHub closing keyword for the originating issue.
7. Rebase on `origin/dev` at required gates.
   - At session start in that worktree.
   - After any merge to `dev`.
   - Before pushing.
   - Before marking a PR ready.
8. Before PR readiness, run the relevant verification.
   - Do not mark ready on stale checks.
   - Update `CURRENT.md` and the PR body with the latest verification state.

## PR-First Integration

Implementation work should integrate through a PR into `dev`.

Do not merge local branches directly into `dev` unless the user explicitly requests a direct merge.

Draft PRs are useful early because they expose overlap, CI failures, and branch risk before the end of the task.

Before marking a PR ready:

- branch is rebased on `origin/dev`
- relevant local checks are current
- browser evidence exists for frontend behavior changes
- Docker/runtime state was rebuilt or restarted after sync when relevant
- PR body contains a closing reference to the originating issue, such as `Closes #123`
- PR body is rendered through the wrapper script or from a rendered body file
- branch-local `.project` state points to the PR

After the PR merges into `dev` and the task is complete:

- sync the repo/worktree state to current `dev`
- confirm the originating issue closed as expected
- archive the merged task workspace with `../ora-et-labora/scripts/close_task_workspace.py --repo-root . --module-id <module-id>`
- review the dry-run plan before adding `--apply`
- let the helper retire the owning worktree and local branch instead of ad hoc cleanup commands

## Auto-Merge Policy

Implementation PRs into `dev` may use agent auto-merge when every gate below is satisfied. This policy is permission to use GitHub's merge machinery when safe; it is not permission to bypass repository rules, required checks, branch protection, review requirements, or an explicit user hold.

Auto-merge gates for implementation PRs:

- PR target is `dev`, not `main`.
- PR is not a release PR, hotfix-to-stable PR, or emergency production promotion.
- PR body includes a closing reference for the originating issue, such as `Closes #123`.
- Branch is rebased on current `origin/dev`.
- Local verification is recorded in `CURRENT.md`, the task log, and the PR body.
- Browser evidence exists when frontend-visible behavior changed, or the PR body explains why browser verification is not applicable.
- Required CI is passing, or GitHub auto-merge is enabled while required CI is pending.
- No unresolved review threads, requested changes, merge conflicts, blocked labels, or explicit user hold are present.
- Branch-local `.project` state points to the PR and records the auto-merge decision.

Use `gh pr merge --auto --merge` when required checks are still pending and GitHub auto-merge is available. Use an immediate merge command only when checks are already green and all gates are satisfied.

If GitHub auto-merge is unavailable, blocked by settings, or rejected by branch protection, do not force the merge. Record the blocker and leave the PR open.

Release PRs into `main` require explicit user approval before merge, even when checks are green. Do not enable auto-merge for release PRs unless the user explicitly says to enable auto-merge for that specific release PR.

## Docker Runtime Model

Default mode: one active Docker or Compose stack at a time across worktrees.

This is the safest default because many repos use fixed ports, shared volume names, default Compose project names, or fixed container names.

Switching pattern in default mode:

```bash
docker compose -p <active-worktree> down
docker compose -p <next-worktree> up -d
```

Use the same Compose project name for both `up` and `down`. Otherwise containers, networks, and volumes can be orphaned.

## Parallel Docker Mode

Run multiple worktree stacks only when all isolation surfaces are explicit.

Required isolation:

- unique Compose project name per worktree
- unique host ports per worktree
- service discovery that does not collide
- no fixed `container_name` values, or fixed names made worktree-specific
- per-worktree env file or override file when ports or URLs differ
- documented down/up command pattern

Accepted project-name patterns:

```bash
docker compose -p fix-124-login-spinner up -d
COMPOSE_PROJECT_NAME=fix-124-login-spinner docker compose up -d
```

If the repo cannot isolate ports or container names, do not run parallel stacks. Use default mode and switch stacks deliberately.

## Runtime Freshness Rule

After `git pull`, `git rebase`, or merging changes from `dev`, rebuild or restart affected services before claiming current behavior.

Do not trust:

- pre-rebase containers
- stale frontend dev servers
- cached bundles
- old API containers
- old migration state
- browser tabs from before the latest code sync

If verification depends on runtime behavior, refresh the runtime first.

## Overlapping Worktrees

When two active worktrees overlap:

- prefer merging the branch with fewer dependencies first
- rebase the other branch on `origin/dev` immediately after the first merge
- resolve conflicts in the dependent branch
- use stacked PRs only temporarily when one branch depends on another unmerged branch
- retarget stacked PRs to `dev` after the base PR merges

Do not let two worktrees silently modify the same contract without surfacing overlap in PRs or task logs.

## Red Flags - Stop And Correct Flow

- "I created a worktree but kept editing the main checkout."
- "The PR targets `main` for normal implementation work."
- "The PR references the issue in prose but does not use a closing keyword."
- "I pushed before rebasing on `origin/dev`."
- "I enabled auto-merge without checking reviews, CI, issue closure, and branch freshness."
- "I enabled auto-merge for a release PR into `main` without explicit user approval."
- "The browser is still using the old dev server."
- "Two worktrees run Compose with the same ports."
- "The repo has fixed `container_name` values but I started parallel stacks."
- "I changed branch-local `.project` files in the main checkout."

All of these mean the branch/worktree flow is unsafe.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "I can work in the main checkout just this once." | The workflow depends on branch-local state and clean PR boundaries. Use the worktree. |
| "Docker is probably using the right code." | Containers are not proof of current code. Restart or rebuild after sync. |
| "Ports only conflict if both stacks are active." | Exactly. Default to one active stack unless parallel isolation is documented. |
| "The branch is close enough to `dev`." | Rebase gates exist because stale branches hide conflicts and CI drift. |
| "A direct merge is faster." | PR-first integration is the safety surface unless the user explicitly overrides it. |
| "I can close the issue manually after merge." | The PR should carry `Closes #<issue>` so GitHub closes it automatically and auditably on merge. |
| "Auto-merge means GitHub will handle everything." | Auto-merge only waits for GitHub gates. The agent must still confirm branch freshness, verification, reviews, issue closure, and state logging. |

## Completion Checklist

- branch name matches the issue or module
- worktree exists under `.project/worktrees/`
- commands are run from the worktree root
- branch-local `.project` updates are in the worktree checkout
- branch is synced with `origin/dev`
- Docker mode is clear: default one-stack or isolated parallel mode
- PR targets `dev`
- PR body uses `Closes #<issue-id>` or an equivalent closing keyword for the originating issue
   - PR body comes from `create_pr_from_template.py` or a rendered body file
   - GitHub `validate` rejects PRs whose bodies are missing required template sections or the `Closes #<issue>` reference
- verification is complete before PR readiness
- auto-merge is enabled only for eligible `dev` PRs, or explicitly skipped/blocked in the task log

## Common Mistakes

- assuming Docker runtime policy instead of reading project state
- running parallel stacks with colliding ports or fixed container names
- working from the main checkout after creating a worktree
- opening implementation PRs directly to `main`
- forgetting the closing issue reference in the PR body
- enabling auto-merge on release PRs into `main` without explicit user approval
- failing to rebase after another PR merges to `dev`
- trusting stale browser or container state after code sync

## Handoff

Once implementation is ready for checks, run modality-specific verification and collect durable evidence before claiming completion or marking the PR ready.
