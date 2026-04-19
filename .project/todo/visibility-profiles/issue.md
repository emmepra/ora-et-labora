## Problem

Ora et Labora needs explicit public/private/internal repository modes so agents do not publish private workflow state in public repos or lose useful `.project` memory in private/internal repos.

## Scope

- Define visibility profiles for `repo-init`, `repo-bootstrap`, and the suite index.
- Make bootstrap apply a profile-aware `.gitignore` artifact policy.
- Cover public/private behavior with tests.
- Keep raw Playwright artifacts disciplined by default.

## Acceptance Criteria

- Public mode keeps `.project/` and local agent state ignored by default.
- Private/internal modes keep `.project` workflow memory versionable while ignoring worktrees and raw browser artifacts.
- Bootstrap script accepts a visibility/profile option.
- Tests cover default/private and public behavior.
- README explains the workflow impact.

## Verification

- Run `python scripts/validate_all.py`.

## Notes

This issue is user-directed from the Ora et Labora workflow refinement discussion.
