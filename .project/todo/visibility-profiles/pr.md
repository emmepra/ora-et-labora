## Summary

- Adds public/private/internal visibility profiles to the Ora et Labora repo setup workflow.
- Updates `repo-init`, `repo-bootstrap`, and the suite index so artifact publication policy is explicit before setup.
- Extends `bootstrap_repo_templates.py` with `--visibility <private|internal|public>` and profile-aware `.gitignore` policy.
- Adds tests for private/default, public, and profile replacement behavior.

Closes #1

## Verification

- `python scripts/validate_all.py`

## Risk / Notes

- Public profile now ignores `.project/` by default, so public repos still get local Ora state but do not publish it unless deliberately sanitized.
- Private/internal profiles keep workflow memory versionable while ignoring worktrees and raw Playwright payloads.
