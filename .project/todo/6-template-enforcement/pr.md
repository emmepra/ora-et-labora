## Summary

- Adds dedicated issue and PR creation wrapper scripts.
- Adds GitHub issue template config that disables blank issues in bootstrapped repos.
- Tightens skill wording and tests so template usage is harder to bypass.

## Why

Template usage was recommended but still easy to bypass with raw gh commands. This change makes wrappers the standard path and adds tests that keep the policy in place.

## Linked Issue

Closes #6

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable; process/docs/script-only change.
- Browser evidence: not applicable.
- CI: pending after PR creation.

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.
- This is an implementation PR targeting `dev`.
- Branch is rebased on `origin/dev`.
- Browser verification is not applicable.
- Branch-local `.project` state is current.

## Blueprint Updates

No blueprint files changed. This hardens workflow execution rules encoded in the skill suite itself.

## Risks / Rollback

Risk: stricter template usage may require agents to adopt the new wrappers.

Rollback: revert this PR if the wrappers or issue-template config prove too rigid.

## Follow-ups

- After merge, sync installed local skills.
- Optionally promote `dev` to `main` if you want the stable installer path updated.
