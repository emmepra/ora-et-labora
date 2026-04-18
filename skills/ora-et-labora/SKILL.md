---
name: ora-et-labora
description: Manage a repo-first issue-to-release workflow for Git/GitHub projects that use `.project/` as the execution surface. Use when Codex needs to shape work before implementation, run a mandatory blueprint fit check against existing project constraints, create or resume issue/worktree state, keep logs minimal but resumable, choose verification modalities based on the type of change, enforce browser verification with disciplined Playwright evidence for frontend-impacting work, open PRs to `dev`, prepare grouped releases from `dev` to `main`, or bootstrap repo templates for issues, PRs, blueprint docs, and workflow examples.
---

# ora-et-labora

Use this skill to keep implementation work consistent from issue shaping through release.

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

## Artifact Model

Use these surfaces with strict responsibilities:

- GitHub issue: problem statement, constraints, acceptance criteria, verification plan.
- `.project/todo/<module-id>/00_brainstorm.md`: challenge record, feasibility notes, options, and the blueprint fit check.
- `.project/todo/<module-id>/CURRENT.md`: current resumable state only.
- `.project/logs/<module-id>.md`: meaningful deltas only.
- Pull request: implementation summary, verification evidence, risk/rollback notes, blueprint changes.
- Release PR: grouped promotion from `dev` to `main`.

Read [references/workflow.md](references/workflow.md) for the state model and artifact boundaries.
Read [references/blueprint-policy.md](references/blueprint-policy.md) before deciding whether `.project/blueprint/` must change.
Read [references/docker-worktrees.md](references/docker-worktrees.md) when the repo uses Docker or Compose and multiple worktrees may run locally.
Read [references/verification.md](references/verification.md) before deciding which checks are required and how browser evidence must be stored.
Read [references/repo-bootstrap.md](references/repo-bootstrap.md) when bootstrapping a repo or applying templates.

## Blueprint Rules

- Mandatory fit check: yes.
- Mandatory blueprint update on every issue: no.
- Mandatory blueprint update when architecture, contracts, environment assumptions, verification policy, release policy, or workflow invariants changed: yes.

If the issue clearly fits the current blueprint, record the fit result in `00_brainstorm.md` and move on.
If the blueprint blocks or contradicts the issue, stop and surface the conflict before implementation.

## Branching And Release Rules

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

## Logging Rules

Only append to the task log when one of these changed:

- chosen approach
- known blocker
- verification result
- PR state
- release state

Do not log every command, edit, or micro-commit.

Use [assets/templates/current.md](assets/templates/current.md) for resumable state.
Use [assets/templates/log.md](assets/templates/log.md) for the append-only log shape.

## Verification Rules

- Pick verification modalities from the change surface:
  - docs/process-only: spellcheck, lint, structural validation as needed
  - backend/API: unit, integration, contract, migration, and CLI/API probing as needed
  - frontend/UI: browser verification plus relevant unit/build checks
  - cross-stack changes: combine the relevant backend and frontend modalities
- For browser verification, collect evidence under `.project/logs/playwright/<module-id>/<run-id>/`.
- Record only the latest meaningful verification result in `CURRENT.md` and the task log.
- Keep large browser artifacts out of ad hoc temp folders once they matter to the task outcome.

## Task Flow

1. Resolve repo root and read the closest `AGENTS.md`.
2. Run the blueprint fit check for the issue and capture it in `00_brainstorm.md`.
3. Shape or refine the GitHub issue using a rendered template.
4. Create the branch/worktree and initialize `.project/todo/<module-id>/` plus `.project/logs/<module-id>.md`.
5. Implement.
6. Verify.
7. Open or update the PR into `dev`.
8. Record only meaningful deltas.
9. When a release is requested, prepare a grouped `dev` -> `main` release PR.

## Scripts

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
