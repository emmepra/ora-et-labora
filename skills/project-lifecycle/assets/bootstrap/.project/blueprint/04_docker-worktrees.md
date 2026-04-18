# Docker Worktrees

- Default mode is one active local Docker or Compose stack across worktrees.
- If the repo needs parallel worktree stacks, it must define:
  - compose project naming
  - host port isolation
  - env or override-file strategy
  - service/container naming rules
- Avoid fixed `container_name` values unless they are worktree-specific.
- After pull, rebase, or merge sync, rebuild or restart affected services before claiming current behavior.
