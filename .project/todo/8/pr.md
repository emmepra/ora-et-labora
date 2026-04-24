## Summary

- Adds a PR body validation script that enforces the Ora et Labora PR template contract.
- Runs the new gate in GitHub `validate` on every pull request before suite validation.
- Adds tests for valid PR bodies, missing sections, missing `Closes #` references, and unresolved placeholders.

## Why

The template wrappers and GitHub issue config hardened issue and PR creation, but malformed PR bodies could still slip through if an agent bypassed the standard rendering path. This adds the missing CI-side enforcement so PR template structure becomes a real gate.

## Linked Issue

Closes #8

## Verification

- Local: `python scripts/validate_all.py`; `python scripts/validate_pr_body.py --body-file .project/todo/6-template-enforcement/pr.md`
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

No blueprint files changed. This extends the template-enforcement workflow already added to the suite by making PR body structure enforceable in CI.

## Risks / Rollback

Risk: the validator could be too strict and reject legitimate PR bodies if the template contract changes without updating the script.

Rollback: revert this PR to remove the CI gate and validator if it blocks valid workflow.

## Follow-ups

- After merge, sync installed local skills.
- If desired later, add a similar review-time gate for issue bodies, though GitHub issue templates and wrapper usage already cover most of that path.
