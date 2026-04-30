# Ora et Labora AGENTS Guide

Scope: applies to `personal/ora-et-labora/**`.

## Purpose

- This repo defines the Ora et Labora workflow suite itself.
- Keep changes scoped to the suite repo unless the user explicitly asks for cross-project edits.

## Repo Overrides

- Validation entrypoint: `python scripts/validate_all.py`
- Local runtime state:
  - `.project/todo/**` is local-only task workspace state. Do not commit it.
  - `.project/worktrees/**` is local-only runtime state. Do not commit it.
  - `.project/logs/archive/**` is local-only legacy archive space. Do not commit it.
- Versioned workflow memory:
  - `.project/logs/**` remains the concise durable record.
  - `.project/blueprint/**` remains the durable project model when present.

## Branch Flow

- Normal work goes `dev` -> `feat|fix|chore/<issue>-<slug>` -> PR to `dev`.
- Epic work goes `dev` -> `epic/<slug>` with an early draft PR to `dev`; child issue PRs target the epic branch.
- Hotfix work goes `main` -> `hotfix/<issue>-<slug>` -> PR to `main`, then must be reconciled back to `dev`.
- Stable releases promote grouped `dev` work -> `main` through release PRs.
