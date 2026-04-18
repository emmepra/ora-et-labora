# Workflow Reference

## Intent

Encode a consistent repo-first flow with minimal redundancy and strong recovery after context compaction.

## State Machine

1. `shaping`
   - clarify the problem
   - identify constraints and non-goals
   - decide whether the work is trivial or nontrivial
2. `fit-check`
   - compare the issue against `.project/blueprint/`
   - record feasibility, conflicts, and blueprint references
3. `issue-ready`
   - open or refine the GitHub issue
4. `initialized`
   - create or reuse the worktree
   - initialize `.project/todo/<module-id>/` and `.project/logs/<module-id>.md`
5. `implementing`
   - code and test locally
6. `verified`
   - record the latest meaningful verification result
   - store browser evidence in the repo log surface when frontend checks were required
7. `pr-open`
   - PR targets `dev`
   - PR body includes verification and risk notes
8. `merged-dev`
   - implementation landed in `dev`
9. `release-candidate`
   - grouped `dev` -> `main` PR prepared
10. `released`
   - release PR merged to `main`

## Source Of Truth By Concern

- Issue scope and acceptance criteria: GitHub issue
- Design tradeoffs and feasibility: `00_brainstorm.md`
- Current resumable state: `CURRENT.md`
- History worth remembering: task log
- Implementation and verification summary: PR
- Promotion to stable: release PR

## Delta Logging Rule

Append a log entry only when one of these changed:

- a durable design choice
- a failed attempt worth avoiding later
- verification status
- PR state
- release state

## Frontend Verification

For frontend-impacting work:

- local browser verification is mandatory
- CI browser coverage should exist if the project supports it
- Playwright evidence should be stored under `.project/logs/playwright/<module-id>/<run-id>/`
- `CURRENT.md` should record the latest browser verification result and reference the latest meaningful evidence path when needed

## Branch Ownership

Prefer one branch and one worktree per issue/module. If stacked work is required, note the dependency explicitly in the brainstorm file and PR.
