## Summary

- Adds a governance helper that can dry-run or apply standard GitHub repo settings and a default Ora et Labora issue label set.
- Adds a repo-local wrapper plus tests for command planning and label coverage.
- Updates `repo-init`, `repo-bootstrap`, and suite docs to use the governance helper as the standard path for repo defaults.

## Why

Ora et Labora documented the target GitHub state well, but still left too much of it as a manual pending step. This first automation slice turns repo defaults and standard issue labels into an executable path without overreaching into full ruleset orchestration yet.

## Linked Issue

Closes #15

## Verification

- Local: `python scripts/validate_all.py`; `python skills/ora-et-labora/scripts/configure_repo_governance.py --repo emmepra/ora-et-labora`
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

No blueprint files changed. This adds execution capability to the repo-init/bootstrap surfaces already defined by the suite.

## Risks / Rollback

Risk: the governance defaults may be too opinionated for some repos if applied blindly, which is why the helper defaults to dry-run planning and keeps full rulesets out of this first slice.

Rollback: revert this PR to return governance changes to manual-only handling.

## Follow-ups

- Next roadmap slice should add task/worktree cleanup after merge.
- A later slice can extend governance automation into rulesets and branch protections once repo-specific required-check handling is explicit.
