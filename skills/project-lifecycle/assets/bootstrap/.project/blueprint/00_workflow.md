# Workflow

- Nontrivial work starts with issue shaping plus a blueprint fit check.
- Implementation work should map to one issue, one branch, one worktree, one `CURRENT.md`, and one task log.
- Implementation PRs target `dev`.
- Verification modality should match the change surface.
- Frontend-impacting work requires browser verification with stored evidence.
- Release promotion happens through grouped `dev` -> `main` PRs.
