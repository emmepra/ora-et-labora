## Summary

- Adds the safe agent auto-merge policy for implementation PRs into `dev`.
- Keeps release PRs into `main` gated by explicit user approval.
- Updates PR templates with an auto-merge eligibility section.
- Adds tests to keep the policy present in skills and templates.

## Why

Agents can technically merge PRs when permissions allow it, but Ora et Labora needed a durable policy for when that is safe. This prevents accidental stable releases, stale-branch merges, issue-unlinked merges, and merges with unresolved review or verification gaps.

## Linked Issue

Closes #4

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable; process/docs/template-only change.
- Browser evidence: not applicable.
- CI: pending after PR creation.

## Auto-Merge Eligibility

- Agent auto-merge requested: no for this PR; review before merging.
- This PR defines the policy and should not be used as the first unattended auto-merge test.

## Blueprint Updates

No `.project/blueprint/` files changed. The durable workflow policy is encoded directly in the skill files and templates.

## Risks / Rollback

Risk is procedural: agents may over-apply auto-merge unless the gates are read carefully. The policy explicitly blocks release PR auto-merge to `main` without explicit approval.

Rollback: revert this PR if the auto-merge policy proves too permissive.

## Follow-ups

- After merge, sync installed local skills and optionally promote `dev` to `main`.
