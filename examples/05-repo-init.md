# Initialize A New Repo

Use `repo-init` when the repository itself does not exist yet or the first setup decisions still need to be made.

## Example Prompt

```text
Use $repo-init to create a new private full-stack app repo under my personal GitHub account.
Name it atlas-dashboard and put it under personal/.
Use dev as default and main as stable, then apply Ora et Labora.
```

## Expected Flow

1. Collect missing critical inputs.
   - owner/org
   - repo name
   - visibility
   - local path
   - source mode
   - repo type
2. Show a creation plan and wait for explicit approval before running `gh repo create`.
3. Create or prepare the local repo.
4. Create the GitHub repo.
5. Establish `main` and `dev`.
6. Set `dev` as the default branch.
7. Apply Ora et Labora workflow templates and `.project/blueprint/`.
8. Commit and push the initial setup when approved.
9. Report repo URL, local path, branch model, and pending GitHub settings.

## Important Distinction

- Use `repo-init` to create a repo.
- Use `repo-bootstrap` to apply Ora et Labora conventions to an existing repo.

## Confirmation Gate

Before any remote creation, the agent should show:

- owner/repo
- visibility
- local path
- source mode
- repo type
- whether the first push will happen
- whether branch protection/rulesets are configured now or pending

The agent should not create the remote until the user approves that plan.
