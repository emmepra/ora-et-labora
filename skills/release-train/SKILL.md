---
name: release-train
description: Use when promoting accumulated work from `dev` to `main`, preparing release PRs, checking release readiness, writing release notes, or documenting rollback.
---

# release-train

Use this skill when work is moving from the integration branch to the stable branch.

## Overview

Release train manages grouped promotion from `dev` to `main`. Normal implementation PRs and completed epic PRs land in `dev`; stable releases are deliberate grouped PRs into `main`.

Core principle: `main` is stable, not a second integration branch. A release PR should explain what is included, how it was checked, and how to roll back.

This skill is self-contained. Follow this file for the release train procedure.

## When To Use

Use this skill when:

- the user asks to release, promote, ship, or merge `dev` to `main`
- multiple implementation PRs have accumulated on `dev`
- release notes or changelog text are needed
- stable branch readiness must be checked
- rollback, migration, or production risk must be documented
- CI status for `dev` or release PRs matters
- the project needs a release PR body

Do not use this skill for:

- normal implementation PRs into `dev`
- issue shaping before implementation
- executing emergency production hotfixes; use `worktree-flow` for the hotfix lane, then return here only if the hotfix changes release scope or stabilization

## Responsibilities

- identify what changed between `main` and `dev`
- group included PRs/issues into a coherent release scope
- check release readiness
- prepare a release PR from `dev` to `main`
- summarize verification status and gaps
- document migrations, operational notes, and rollback
- avoid promoting every individual implementation PR directly to `main`

## Quick Reference

| Release concern | Required handling |
| --- | --- |
| Included changes | list PRs/issues or grouped scope |
| CI | current status, not stale status |
| Frontend changes | browser verification status and evidence summary |
| Schema/migrations | apply/rollback or explicit status |
| Docker/runtime changes | deployment/runtime notes |
| Risk | known risks and mitigations |
| Rollback | concrete rollback path |
| Release notes | user-facing summary where relevant |

## Branch Model

- `dev` is the integration branch.
- `main` is the stable branch.
- Normal implementation PRs target `dev`.
- Completed epic PRs target `dev` after child work is integrated and the draft epic PR is ready.
- Hotfix PRs target `main` first only for urgent stable-branch fixes, then must be reconciled back to `dev`.
- Release PRs target `main`.
- A release PR may include many implementation PRs.

Do not merge every feature/fix PR directly into `main`. That defeats grouped release management. The exception is the hotfix lane, which is narrow, explicitly approved, and reconciled back to `dev`.

## Release Procedure

1. Confirm branch state.
   - Fetch remote branches.
   - Confirm `dev` contains the intended normal and completed epic PRs.
   - Confirm `main` is the current stable base.
2. Identify release scope.
   - Compare `main...dev`.
   - Collect merged PRs and related issues.
   - Group changes by user-facing outcome or subsystem.
3. Check readiness.
   - CI status for `dev` or release PR.
   - Regression suite status if available.
   - Browser verification status when frontend work is included.
   - Migration/schema status when persistence changed.
   - Docker/deployment notes when runtime changed.
4. Identify release risks.
   - Backward compatibility.
   - Data migration.
   - Feature flag state.
   - Deployment order.
   - Browser or cross-stack coverage gaps.
5. Prepare release PR body.
   - Use `../ora-et-labora/assets/templates/release-pr.md`.
   - Prefer a body file and `gh pr create --body-file <file>`.
   - The PR-body validation gate accepts the release template shape for PRs targeting `main`; do not rewrite release PRs into the implementation template just to satisfy CI.
   - Do not assemble complex markdown inline in shell strings.
6. Open or update the release PR.
   - Base: `main`.
   - Head: `dev` or a release stabilization branch if the project uses one.
7. Record release state.
   - Update task/release log if the repo tracks release logs.
   - Do not duplicate the entire release PR body in local logs.
8. Merge only when release gates are satisfied.
   - If gates are blocked, record blocker and do not claim release readiness.
   - Release PRs into `main` require explicit user approval before merge. Hotfix PRs into `main` also require explicit user approval and are outside the normal release train.
   - Do not enable auto-merge for release PRs unless the user explicitly approves auto-merge for that specific release PR.

## Release Checks

Run or confirm:

- current CI
- regression suite
- build/package checks
- browser verification when frontend work is included
- migration/schema checks if relevant
- deployment or runtime config checks if relevant
- release-note accuracy
- rollback plan plausibility
- explicit user approval before merging a release PR into `main`

If a check is skipped, the release PR must say why.

## Release PR Body Requirements

A release PR should include:

- release scope
- included PRs or grouped changes
- release checks and current status
- browser verification status when frontend changes exist
- migration/schema status
- operational notes
- known risks
- rollback plan
- follow-ups that should not block release

## Rollback Guidance

Rollback should be concrete enough for an operator to act.

Good rollback notes:

- revert the release merge commit if no migrations or irreversible data changes are included
- disable feature flag `<flag-name>` if the release exposes the feature through a flag
- restore previous container image tag `<tag>` if deploy pipeline supports image rollback
- run documented down migration only if it has been tested

Weak rollback notes:

- "revert if needed"
- "rollback normally"
- "monitor and fix forward"
- "N/A" without explanation

## Red Flags - Stop The Release

- `dev` has not been checked against current CI.
- Frontend changes are included but browser status is unknown.
- Migration changes are included but schema status is unknown.
- Release PR body does not list included changes.
- Rollback says only "revert if needed."
- The release is being made by merging each implementation PR separately to `main` instead of using the release train.
- The release uses stale verification from before recent `dev` merges.
- Auto-merge is enabled for a release or hotfix PR into `main` without explicit user approval.

All of these mean the release train is not ready.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "The PRs already passed individually." | A release train needs current aggregate status on `dev`. |
| "This is just a small release." | Small releases still need scope, checks, and rollback. |
| "Rollback is obvious." | If it is obvious, write the concrete rollback action. |
| "No browser check is needed because frontend PRs were already reviewed." | Review is not browser verification. Include current browser status or explain why not needed. |
| "We can promote directly from feature branch to `main`." | Normal flow is implementation to `dev`, release train to `main`. Only narrow hotfixes target `main` first, and they must be reconciled back to `dev`. |
| "Checks are green, so the release PR can auto-merge." | `main` is stable. Release merges require explicit user approval unless the user approved auto-merge for that specific release PR. |

## Template And Tools

- `../ora-et-labora/assets/templates/release-pr.md`

Use the template as the release body structure. Fill unknown statuses explicitly as `pending`, `not applicable`, or `blocked`, not as blanks.

## Completion Checklist

- `main...dev` scope reviewed
- included PRs/issues summarized
- current CI status known
- browser status known when frontend changes are included
- migration/schema status known when relevant
- operational notes captured when runtime/deploy changed
- rollback plan concrete
- release PR targets `main` from `dev` or an explicit release stabilization branch
- explicit user approval recorded before merge
- release state recorded without duplicating the entire PR body locally

## Common Mistakes

- promoting individual implementation PRs directly to `main` outside the hotfix lane
- forgetting rollback notes
- using stale verification status that no longer reflects current `dev`
- failing to identify included PRs
- auto-merging a release PR into `main` without explicit user approval
- treating release notes as optional when users or operators need them
- merging a release train while required checks are still pending
