## Summary

- Moves the PR body validator into the shipped `ora-et-labora` skill so installed skills carry the logic.
- Makes bootstrap copy the validator into target repos and adds a standalone `validate-pr-body.yml` workflow asset.
- Adjusts tests and repo docs so the bootstrap payload, installed skill, and suite repo all enforce the same PR body contract.

## Why

The previous PR added PR-body validation for the suite repo itself, but the validator lived only at repo root. That meant installed skills did not contain it, and bootstrapped repos did not inherit the enforcement automatically. This closes that propagation gap.

## Linked Issue

Closes #10

## Verification

- Local: `python scripts/validate_all.py`; `python skills/ora-et-labora/scripts/validate_pr_body.py --body-file .project/todo/8/pr.md`
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

No blueprint files changed. This is a packaging and bootstrap-propagation fix for the template enforcement already added to the suite.

## Risks / Rollback

Risk: path resolution between skill-source usage and copied-into-repo usage could drift again if future template locations change.

Rollback: revert this PR to return to the repo-root-only validator model.

## Follow-ups

- After merge, sync installed local skills again so the shipped validator is present under `~/.codex/skills/ora-et-labora/scripts/`.
- If needed later, fold the standalone PR-body workflow into project-specific CI after bootstrap, but keep an equivalent gate in place.
