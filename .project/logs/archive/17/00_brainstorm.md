# Add merged-task cleanup and archive flow: Brainstorm

- Date: 2026-04-24
- Issue: [#17](https://github.com/emmepra/ora-et-labora/issues/17)
- Kind: feature
- Module: 17

## Problem

- Ora et Labora is strong at creating issue workspaces and worktrees, but it has no standard closeout path after a PR merges into `dev`.
- Merged task state, worktrees, and local branches can accumulate indefinitely, which weakens repo hygiene and makes the workflow heavier over time.
- Cleanup currently depends on ad hoc manual commands, so agents may forget to archive state, remove the worktree, or retire the local branch consistently.

## Desired Outcome

- Provide a standard helper that plans and applies post-merge cleanup for a task workspace.
- Keep cleanup safe by default: dry-run first, require `--apply`, and refuse destructive cleanup unless the branch is already merged into the integration branch unless explicitly forced.
- Preserve task history by archiving the task workspace before removing the worktree and local branch.

## Constraints

- The cleanup flow must fit the existing Ora et Labora artifact model and branch/worktree conventions.
- The helper must work from the repo root and use deterministic paths derived from the module ID and branch name.
- The archive path should stay consistent with the existing preference for `.project/logs/` as the durable historical surface.
- The flow must not delete protected branches or branches that are still active in another worktree.

## Blueprint Fit Check

- Relevant blueprint docs:
  - `.project/blueprint/00_overview.md`
  - `.project/blueprint/02_worktree-runtime.md`
- Feasibility: fits with an additive helper plus workflow/documentation updates.
- Conflicts or missing decisions: none; this extends the workflow after merge rather than changing integration or release policy.

## Options Considered

- Option A: archive task state under `.project/logs/archive/<module-id>` and leave the main task log in place.
- Option B: introduce a separate `.project/archive/` tree for closed task workspaces.

## Chosen Direction

- Choose option A.
- It keeps archival state under the existing durable-history surface, avoids adding another top-level `.project` area, and matches the user preference to keep the repo operational model tighter rather than broader.

## Risks / Unknowns

- Cleanup should not silently remove branches that are not actually merged.
- Worktree removal and branch deletion should remain optional so the helper can be used in partial-cleanup scenarios.
- The docs need to make clear that this is a post-merge cleanup step, not a substitute for PR/release verification.

## Acceptance Checks

- Dry-run output shows the archive, worktree removal, and branch deletion plan.
- `--apply` archives the task workspace and removes the merged worktree and local branch.
- The helper refuses cleanup when the branch is not merged into the target ref.
- The suite docs point agents to the new post-merge cleanup path.
