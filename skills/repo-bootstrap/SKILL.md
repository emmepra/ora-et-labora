---
name: repo-bootstrap
description: Bootstrap repositories for the Ora et Labora workflow. Use when Codex needs to copy issue and PR templates, add blueprint workflow docs, prepare CI/release placeholders, or apply initial GitHub defaults such as `dev` as default branch and `main` as stable branch.
---

# repo-bootstrap

Use this skill when a repo needs the workflow structure applied for the first time.

## Responsibilities

- copy workflow templates and blueprint docs into the repo
- prepare CI and release placeholders
- document GitHub defaults and branch model

## Rules

- repo bootstrap should make the workflow visible in files, not only in chat
- branch protection and rulesets are part of the bootstrap target state even if they need separate GitHub API calls
- keep the repo-level bootstrap deterministic

## Resources

- use `../ora-et-labora/scripts/bootstrap_repo_templates.py`
- read `../ora-et-labora/references/repo-bootstrap.md`

## Target State

- `.github/ISSUE_TEMPLATE/`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml.example`
- `.github/workflows/release.yml.example`
- `.project/blueprint/`
- `dev` default branch
- `main` stable branch
