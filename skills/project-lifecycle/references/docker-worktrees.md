# Docker Worktrees Reference

## Default Mode

Use one active local Docker or Compose stack at a time across worktrees unless the project explicitly supports parallel stacks.

Switching worktrees in default mode:

1. stop the active stack
2. move to the next worktree
3. start the next stack

Recommended pattern:

- `docker compose -p <active-worktree> down`
- `docker compose -p <next-worktree> up -d`

## Parallel Mode

Run multiple worktree stacks only when all of these are true:

- each worktree uses a unique compose project name
- each worktree has unique host ports
- service discovery or network naming does not collide
- the repo avoids fixed `container_name` values, or makes them worktree-specific

Accepted ways to name the stack:

- `docker compose -p <worktree-name> ...`
- `COMPOSE_PROJECT_NAME=<worktree-name> docker compose ...`

## Required Isolation Surfaces

For parallel mode, the repo should define:

- compose project naming rule
- port override strategy
- env-file or override-file strategy per worktree
- service/container naming rule

Examples:

- `.env.worktree`
- `docker-compose.override.yml`
- `compose.worktree.yaml`

The exact filenames are project-specific. The rule belongs in `.project/blueprint/`, not only in agent memory.

## After Code Sync

After `git pull`, `git rebase`, or merging changes from `dev`, rebuild or restart the affected services before claiming current behavior.

Do not trust stale containers or frontend bundles after sync.

## Logging

If Docker runtime conventions changed, update `.project/blueprint/`.

If a task only used an existing runtime rule, record the meaningful verification result in the task log and avoid repeating runtime setup details.
