# Example: Bootstrap An Existing Repo

## Scenario

- existing repo with no issue templates, no PR template, no `.project/blueprint/`, and no explicit branch model
- the GitHub repository already exists, so repo creation is out of scope

## Workflow

1. `repo-bootstrap`
   - copy `.github/` templates
   - copy `.project/blueprint/` starter docs
2. set GitHub defaults
   - `dev` default branch
   - `main` stable branch
3. add project-specific CI commands to the placeholder workflow files

## Key Point

Bootstrap is about making the workflow visible in files for a repo that already exists. Use `repo-init` instead when the GitHub repo or local repo still needs to be created.
