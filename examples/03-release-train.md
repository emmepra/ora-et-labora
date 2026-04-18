# Example: Grouped Release Train

## Scenario

- `dev` already contains three merged PRs
- one frontend fix
- one backend validation change
- one docs/process update

## Workflow

1. `release-train`
   - prepare a grouped `dev` to `main` PR
   - summarize included work
   - run release checks
2. `verify-and-evidence`
   - confirm any frontend evidence still reflects the current `dev` state
3. merge release PR

## Key Point

Stable promotion is a release event. It should summarize scope, checks, and rollback, not behave like a direct replay of implementation PRs.
