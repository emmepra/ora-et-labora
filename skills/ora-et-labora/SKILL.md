---
name: ora-et-labora
description: Shared principles and suite map for the Ora et Labora repo-first workflow suite. Use when Codex needs the suite map, shared conventions, common templates/scripts, or a cross-phase overview for issue shaping, blueprint checks, state logging, worktree flow, verification evidence, release trains, or repo bootstrap.
---

# ora-et-labora

Use this skill as the suite index and shared overview.

This is not the main operational trigger for most tasks. The primary workflow phases live in peer skills:

- `issue-shaping`
- `blueprint-guard`
- `state-logging`
- `worktree-flow`
- `verify-and-evidence`
- `release-train`
- `repo-bootstrap`

## Core Policy

- Read the closest `AGENTS.md` before acting.
- Treat `.project/` as the canonical operational surface unless the target repo explicitly chose a different convention before this skill was invoked.
- Run a blueprint fit check for every nontrivial issue before implementation starts.
- Update `.project/blueprint/` only when durable project knowledge changes.
- Keep logs delta-only. Do not restate information that already lives in GitHub or `CURRENT.md`.
- Use one issue, one owning branch, one worktree, one resumable `CURRENT.md`, and one append-only log per nontrivial task.
- Choose verification modalities based on the change type. Do not treat "tests" as a single generic step.
- For frontend-impacting work, require browser verification locally and prefer CI browser coverage as well.
- Treat Playwright artifacts as required evidence for browser verification, not as disposable temp output.
- Open implementation PRs into `dev`.
- Promote `dev` to `main` through grouped release PRs, not one `main` merge per implementation PR.
- Render GitHub issue and PR bodies from files or templates. Do not assemble complex markdown inline in a shell command.

## Suite Map

- `issue-shaping`
  - own the challenge record and issue drafting flow
- `blueprint-guard`
  - own the blueprint fit check and blueprint-update decision
- `state-logging`
  - own `CURRENT.md`, resumable state, and delta-only logs
- `worktree-flow`
  - own branch naming, worktree lifecycle, Docker coexistence, and PRs to `dev`
- `verify-and-evidence`
  - own modality-based verification and browser evidence
- `release-train`
  - own grouped promotion from `dev` to `main`
- `repo-bootstrap`
  - own repo templates, GitHub defaults, and bootstrap flow

## Shared Artifact Model

Use these surfaces with strict responsibilities across the suite:

- GitHub issue: problem statement, constraints, acceptance criteria, verification plan.
- `.project/todo/<module-id>/00_brainstorm.md`: challenge record, feasibility notes, options, and the blueprint fit check.
- `.project/todo/<module-id>/CURRENT.md`: current resumable state only.
- `.project/logs/<module-id>.md`: meaningful deltas only.
- Pull request: implementation summary, verification evidence, risk/rollback notes, blueprint changes.
- Release PR: grouped promotion from `dev` to `main`.

## Shared Blueprint Rules

- Mandatory fit check: yes.
- Mandatory blueprint update on every issue: no.
- Mandatory blueprint update when architecture, contracts, environment assumptions, verification policy, release policy, or workflow invariants changed: yes.

If the issue clearly fits the current blueprint, record the fit result in `00_brainstorm.md` and move on.
If the blueprint blocks or contradicts the issue, stop and surface the conflict before implementation.

## Shared Branching And Release Rules

- Preferred branch names:
  - `feat/<issue>-<slug>`
  - `fix/<issue>-<slug>`
  - `chore/<issue>-<slug>`
  - `hotfix/<issue>-<slug>`
- Prefer worktree folder names without slashes, such as `fix-123-login-race`.
- Treat `dev` as the integration branch.
- Treat `main` as the stable branch.
- Release by opening a grouped `dev` -> `main` PR with release notes and release checks.

## Docker And Worktrees

- Default mode: one active Docker or Compose stack across worktrees.
- If switching worktrees in default mode, bring the current stack down before bringing the next one up.
- Parallel worktree stacks are allowed only when the repo has explicit per-worktree isolation for compose project name, ports, and service/container naming.
- Do not leave Docker runtime conventions implicit. Durable local-runtime rules belong in `.project/blueprint/`.

## Shared Logging Rules

Only append to the task log when one of these changed:

- chosen approach
- known blocker
- verification result
- PR state
- release state

Do not log every command, edit, or micro-commit.

Use [assets/templates/current.md](assets/templates/current.md) for resumable state.
Use [assets/templates/log.md](assets/templates/log.md) for the append-only log shape.

## Shared Verification Rules

- Pick verification modalities from the change surface:
  - docs/process-only: spellcheck, lint, structural validation as needed
  - backend/API: unit, integration, contract, migration, and CLI/API probing as needed
  - frontend/UI: browser verification plus relevant unit/build checks
  - cross-stack changes: combine the relevant backend and frontend modalities
- For browser verification, collect evidence under `.project/logs/playwright/<module-id>/<run-id>/`.
- Record only the latest meaningful verification result in `CURRENT.md` and the task log.
- Keep large browser artifacts out of ad hoc temp folders once they matter to the task outcome.

## Shared Resources

- `scripts/render_template.py`
  - Render markdown bodies from template files with strict placeholder checking.
- `scripts/init_issue_workspace.py`
  - Create `00_brainstorm.md`, `CURRENT.md`, and the initial task log for a new issue/module.
- `scripts/bootstrap_repo_templates.py`
  - Copy issue/PR templates, blueprint docs, and workflow examples into a target repo.
- `scripts/collect_playwright_artifacts.py`
  - Store browser verification evidence in a stable repo-local log layout with a machine-readable manifest.

## Template Assets

Use these assets rather than rewriting structure each time:

- `assets/templates/issue-bug.md`
- `assets/templates/issue-feature.md`
- `assets/templates/pr.md`
- `assets/templates/release-pr.md`
- `assets/templates/brainstorm.md`
- `assets/templates/current.md`
- `assets/templates/log.md`

For repo bootstrap, use the files under `assets/bootstrap/`.
