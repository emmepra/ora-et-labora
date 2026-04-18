---
name: repo-bootstrap
description: Use when an existing repository needs Ora et Labora workflow files, `.project/blueprint/`, issue/PR templates, CI/release placeholders, or documented branch/runtime conventions.
---

# repo-bootstrap

Use this skill when an existing repository needs the Ora et Labora workflow structure applied for the first time or repaired after drifting.

## Overview

Repo bootstrap makes the workflow visible in files and repository settings for a repo that already exists locally or remotely. A project should not depend on an agent remembering branch rules, issue formats, PR formats, browser evidence paths, Docker worktree behavior, or release policy.

Core principle: bootstrap creates durable project surfaces, not just documentation about the skill suite.

This skill is self-contained. Follow this file for the repo bootstrap procedure.

Use `repo-init` instead when the GitHub repository itself still needs to be created.

## When To Use

Use this skill when:

- adding Ora et Labora workflow conventions to an existing repo
- adding issue templates, PR templates, CI placeholders, release placeholders, or `.project/blueprint/`
- setting `dev` as default and `main` as stable
- preparing GitHub branch protection or ruleset automation
- repairing a repo where workflow artifacts are missing or inconsistent
- making Docker multi-worktree behavior explicit for a repo

Do not use this skill when:

- the GitHub repo does not exist yet; use `repo-init`
- the user needs to choose owner/org, visibility, repo type, or source mode; use `repo-init`
- the user only wants a single issue shaped
- the repo already has a stronger local workflow and the user has not asked to change it
- applying templates would overwrite project-specific files without review

## Responsibilities

- inspect the target repo before copying templates
- copy or adapt workflow templates into `.github/`
- create or update `.project/blueprint/` baseline files
- prepare CI and release workflow placeholders
- document branch and release model
- identify GitHub settings that must be applied to the existing remote
- avoid overwriting existing project-specific conventions without explicit approval

## Quick Reference

| Surface | Target |
| --- | --- |
| Bug issue template | `.github/ISSUE_TEMPLATE/bug_report.md` |
| Feature issue template | `.github/ISSUE_TEMPLATE/feature_request.md` |
| PR template | `.github/PULL_REQUEST_TEMPLATE.md` with a `Linked Issue` / `Closes #` section |
| CI placeholder | `.github/workflows/ci.yml.example` |
| Release placeholder | `.github/workflows/release.yml.example` |
| Workflow blueprint | `.project/blueprint/00_workflow.md` |
| Release policy | `.project/blueprint/01_release-policy.md` |
| Blueprint fit policy | `.project/blueprint/02_blueprint-fit-check.md` |
| Verification policy | `.project/blueprint/03_verification-policy.md` |
| Docker worktree policy | `.project/blueprint/04_docker-worktrees.md` |

## Bootstrap Procedure

1. Inspect the repo.
   - Read the closest `AGENTS.md`.
   - Check existing `.github/`, `.project/`, CI, release, Docker, and README conventions.
   - Identify whether the repo already uses `dev` and `main`.
2. Decide bootstrap mode.
   - Fresh repo: copy baseline templates.
   - Existing repo with partial workflow: merge carefully and preserve project-specific conventions.
   - Existing repo with conflicting workflow: stop and ask before changing branch model or overwriting policy.
3. Copy templates.
   - Use `../ora-et-labora/scripts/bootstrap_repo_templates.py` when the baseline layout is acceptable.
   - Use `--force` only when overwrite is explicitly intended.
4. Adapt placeholders.
   - Replace example CI commands with project-specific commands.
   - Replace release placeholders with real release checks when known.
   - Do not leave misleading CI or release placeholders that appear production-ready.
5. Document `.project/blueprint/`.
   - Branch model.
   - Worktree model.
   - Verification modalities.
   - Browser evidence path.
   - Docker worktree runtime rules.
   - Release flow from `dev` to `main`.
6. Apply GitHub defaults when a remote is present and the user approved settings changes.
   - Ensure `dev` exists.
   - Ensure `main` exists.
   - Set default branch to `dev`.
   - Configure branch protections or rulesets if requested and supported.
7. Validate.
   - Check generated markdown formatting.
   - Check template paths.
   - Check CI placeholder names.
   - Confirm issue/PR templates render correctly.
8. Record bootstrap result.
   - Summarize what was created, changed, left as placeholder, and still needs GitHub settings.

## GitHub Defaults

Target state:

- default branch: `dev`
- stable branch: `main`
- implementation PRs target `dev`
- release PRs target `main`
- required checks before merge where project CI exists
- branch protection or rulesets for `dev` and `main` when the repo is ready

Typical CLI operations after the remote exists:

```bash
gh repo edit OWNER/REPO --default-branch dev
```

Branch protection and rulesets may require `gh api` or repository settings automation. Do not pretend they were configured if only templates were copied.

## CI And Release Placeholders

Placeholders are allowed only when clearly marked as examples.

Before enabling CI as a real gate:

- replace placeholder commands with project commands
- include lint/typecheck/test/build as appropriate
- add browser smoke checks for frontend projects when feasible
- define required secrets or environment assumptions
- ensure generated artifacts are not accidentally committed unless intended

Before enabling release automation:

- define how `dev` promotes to `main`
- define tagging policy if any
- define changelog or release-note generation if any
- define deploy target if any
- define rollback expectations

## Markdown Hygiene

Issue and PR formatting should be deterministic.

Use:

- templates under `.github/`
- body files
- `gh issue create --body-file <file>`
- `gh pr create --body-file <file>`
- `Closes #<issue-id>` or an equivalent GitHub closing keyword in implementation PR bodies

Avoid:

- long inline shell strings
- implementation PRs without a closing issue reference
- unescaped newlines in command arguments
- ad hoc markdown assembled from memory
- partially filled templates with unresolved placeholders

## Docker Worktree Policy

Every Docker-backed repo should document:

- whether default mode is one active stack or parallel stacks
- Compose project naming convention
- port override strategy
- env-file or override-file strategy
- service/container naming rule
- down/up commands for switching worktrees
- rebuild/restart requirement after rebase, pull, or merge sync

If the repo does not support parallel stacks, say that explicitly.

## Browser Evidence Policy

For frontend-capable repos, bootstrap should document:

- browser verification is required for frontend-visible behavior changes
- Playwright artifacts belong under `.project/logs/playwright/<module-id>/<run-id>/`
- PR templates must include a browser evidence field
- CI should include smoke-level browser coverage when practical

## Red Flags - Stop Bootstrap

- existing project workflow conflicts with Ora et Labora and the user has not approved migration
- the user actually needs a new repository created, not an existing repository bootstrapped
- templates would overwrite meaningful project-specific files
- CI placeholders look like real required gates but still contain fake commands
- branch default is changed before `dev` exists
- branch protection is claimed but not actually configured
- Docker parallel mode is documented without isolated ports or project names
- issue/PR templates contain unresolved placeholders after rendering

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "Templates are enough." | Bootstrap also needs branch model, blueprint docs, and GitHub settings plan. |
| "We can configure GitHub later and say it is done." | Later is fine, but report it as pending, not complete. |
| "The repo probably uses standard CI commands." | Inspect the project. Placeholder commands are not real gates. |
| "Docker rules can stay in chat." | Runtime rules must be durable in `.project/blueprint/`. |
| "Overwrite is faster." | Existing repo conventions may be intentional. Preserve or ask before overwriting. |

## Templates And Tools

- `../ora-et-labora/scripts/bootstrap_repo_templates.py`

Use the script for baseline copying. Inspect and adapt the copied files before claiming bootstrap is complete.

## Completion Checklist

- existing repo workflow inspected
- `.github/ISSUE_TEMPLATE/` present or intentionally skipped
- `.github/PULL_REQUEST_TEMPLATE.md` present or intentionally skipped
- PR template contains a linked issue / closing keyword section
- CI/release placeholders adapted or clearly marked
- `.project/blueprint/` baseline present
- branch model documented
- Docker worktree behavior documented when relevant
- browser evidence policy documented for frontend projects
- GitHub default branch/ruleset status reported accurately
- no unresolved placeholders remain in generated templates

## Common Mistakes

- bootstrapping templates without documenting the branch model
- leaving CI placeholders in place without project-specific commands
- relying on memory for GitHub defaults instead of making them explicit
- claiming branch protection is done without checking it
- creating `.project` structure but not explaining how agents should use it
- adding too many docs that duplicate each other instead of concise blueprint files
