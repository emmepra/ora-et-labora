# Agent Auto-Merge Policy

## Problem

Ora et Labora has PR-first integration and release gates, but it does not explicitly define when agents may auto-merge PRs.

## Challenge Collection

- Auto-merge is useful for implementation PRs into `dev` when checks are green or pending under GitHub auto-merge.
- Auto-merge is risky for release PRs into `main` because `main` is stable and should require explicit user approval.
- Agents need a deterministic eligibility checklist to avoid merging stale, unreviewed, or issue-unlinked PRs.
- The policy must distinguish `gh pr merge --auto` from immediate merge after checks are already green.
- State logging should record when auto-merge is enabled or blocked.

## Decision

Allow agent auto-merge only for implementation PRs targeting `dev` when all gates are satisfied. Require explicit user approval for release PRs targeting `main`.

## Blueprint Fit

- Fits the existing PR-first model.
- Preserves `main` as stable.
- Extends durable workflow knowledge, so the skill files and templates should be updated.

## Verification Plan

- Add tests requiring the auto-merge policy in the relevant skill files and PR templates.
- Run `python scripts/validate_all.py`.
