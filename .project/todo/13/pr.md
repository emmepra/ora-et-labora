## Summary

- Makes the PR-body validator distinguish implementation PRs from release PRs.
- Passes the PR base branch into both repo-local and bootstrapped validation workflows.
- Adds release-path tests and documents that release PRs keep the release template instead of being forced into the implementation PR shape.

## Why

The active `dev` -> `main` release PR failed immediately because the validator enforced only the implementation PR template. Release PRs use a different template by design, so the gate needed to become release-aware without weakening implementation PR checks.

## Linked Issue

Closes #13

## Verification

- Local: `python scripts/validate_all.py`; `python skills/ora-et-labora/scripts/validate_pr_body.py --body-file /tmp/ora-et-labora-release-2026-04-24.md --base-branch main`
- Browser: not applicable; workflow/docs/script-only change.
- Browser evidence: not applicable.
- CI: pending after PR creation.

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.
- This is an implementation PR targeting `dev`.
- Branch is rebased on `origin/dev`.
- Browser verification is not applicable.
- Branch-local `.project` state is current.

## Blueprint Updates

No blueprint files changed. This fixes a mismatch between the stable release flow and the PR-body enforcement gate.

## Risks / Rollback

Risk: if mode selection regresses, release PRs could fail again or implementation PRs could accidentally become too permissive.

Rollback: revert this PR to restore the previous validator behavior, then manually relax the release gate until a corrected follow-up lands.

## Follow-ups

- After merge, recheck release PR #12 and merge it once green.
- After the release lands on `main`, resync installed local skills from stable.
