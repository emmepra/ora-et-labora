# Example: Docker Across Two Worktrees

## Scenario

- Worktree A: `feat/210-admin-audit-log`
- Worktree B: `fix/215-login-timeout`
- Both need the same local compose stack

## Default Mode

Use one active stack at a time:

1. `docker compose -p feat-210-admin-audit-log down`
2. switch worktree
3. `docker compose -p fix-215-login-timeout up -d`

## Parallel Mode

Only use this if the repo defines:

- unique compose project names
- unique host ports
- no conflicting fixed `container_name` values
- explicit env or override-file strategy per worktree

## Key Point

The runtime policy belongs in `.project/blueprint/04_docker-worktrees.md`, not just in memory or shell history.
