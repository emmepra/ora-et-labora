---
name: repo-bootstrap
description: Bootstrap repositories for the Ora et Labora workflow. Use when Codex needs to copy issue and PR templates, add blueprint workflow docs, prepare CI/release placeholders, or apply initial GitHub defaults such as `dev` as default branch and `main` as stable branch.
---

# repo-bootstrap

Use this skill when a repo needs the workflow structure applied for the first time.

## Overview

Bootstrap a repo so the workflow is visible in files rather than only in habit.

## Responsibilities

- copy workflow templates and blueprint docs into the repo
- prepare CI and release placeholders
- document GitHub defaults and branch model

## Rules

- repo bootstrap should make the workflow visible in files, not only in chat
- branch protection and rulesets are part of the bootstrap target state even if they need separate GitHub API calls
- keep the repo-level bootstrap deterministic

## Baseline Files

Copy or adapt these surfaces:

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml.example`
- `.github/workflows/release.yml.example`
- `.project/blueprint/00_workflow.md`
- `.project/blueprint/01_release-policy.md`
- `.project/blueprint/02_blueprint-fit-check.md`
- `.project/blueprint/03_verification-policy.md`
- `.project/blueprint/04_docker-worktrees.md`

## GitHub Defaults To Apply After Push

- default branch: `dev`
- stable branch: `main`
- implementation PRs target `dev`
- release PRs target `main`
- branch protection or rulesets should require CI before merge

## Markdown Hygiene

To avoid malformed issue and PR bodies:

- render bodies from templates
- prefer `gh issue create --body-file <file>`
- prefer `gh pr create --body-file <file>`
- do not compose complex markdown inline in shell strings

## Browser Evidence Discipline

When Playwright or browser checks matter to the task:

- collect artifacts into `.project/logs/playwright/<module-id>/<run-id>/`
- avoid leaving the only evidence in temporary folders
- summarize the verdict in the PR body instead of attaching raw command noise

## Docker Worktree Discipline

When a repo uses Docker with multiple worktrees:

- default to one active stack at a time unless parallel mode is explicitly defined
- document the compose project naming and port strategy in `.project/blueprint/`
- avoid fixed `container_name` values for parallel stacks unless they are worktree-specific

## Resources

- use `../ora-et-labora/scripts/bootstrap_repo_templates.py`

## Target State

- `.github/ISSUE_TEMPLATE/`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml.example`
- `.github/workflows/release.yml.example`
- `.project/blueprint/`
- `dev` default branch
- `main` stable branch

## Common Mistakes

- bootstrapping templates without documenting the branch model
- leaving CI placeholders in place without project-specific commands
- relying on memory for GitHub defaults instead of making them explicit
