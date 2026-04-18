# Example: Bootstrap A New Repo

## Scenario

- new repo with no issue templates, no PR template, no `.project/blueprint/`, and no explicit branch model

## Workflow

1. `repo-bootstrap`
   - copy `.github/` templates
   - copy `.project/blueprint/` starter docs
2. set GitHub defaults
   - `dev` default branch
   - `main` stable branch
3. add project-specific CI commands to the placeholder workflow files

## Key Point

Bootstrap is about making the workflow visible in files. Templates and blueprint docs should exist before the first serious issue, not after the project is already drifting.
