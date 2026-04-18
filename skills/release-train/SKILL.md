---
name: release-train
description: Manage grouped promotion from `dev` to `main`. Use when Codex needs to prepare a release PR, summarize included changes, apply release checks, define rollback notes, or move stable code from the integration branch to the release branch.
---

# release-train

Use this skill when the work is moving from `dev` to `main`.

## Responsibilities

- prepare grouped `dev` to `main` release PRs
- summarize included changes
- apply release-specific checks
- document rollback notes and release notes

## Rules

- do not merge every implementation PR directly to `main`
- stable promotion happens in grouped release PRs
- release PRs must summarize scope, checks, and rollback

## Resources

- use `../ora-et-labora/assets/templates/release-pr.md`
- read `../ora-et-labora/references/workflow.md`
- read `../ora-et-labora/references/verification.md`

## Checks

- regression suite
- browser status when frontend work is included
- migration/schema status if relevant
- CI status
