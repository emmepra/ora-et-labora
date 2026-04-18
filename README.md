# Ora et Labora

Ora et Labora is a repo-first workflow suite for coding agents.

It is not a bag of prompts. It is a working method for taking nontrivial software changes from rough idea to stable release without relying on agent memory or ad hoc habits.

The suite is built around a simple idea:

- shape the work before coding
- check the work against the project blueprint
- keep one issue, one branch, one worktree, and one resumable state surface
- verify using the right modality for the change
- treat browser evidence and Docker runtime behavior as first-class operational concerns
- integrate into `dev`
- release from `dev` to `main`

## How It Works

Ora et Labora starts before code is written.

When the work is nontrivial, it first turns the request into a challenge record, checks it against `.project/blueprint/`, and only then moves into issue and branch execution. The goal is to stop the agent from improvising architecture, forgetting context after compaction, or claiming verification without durable evidence.

Once the issue is shaped, the skill creates or resumes a branch-local execution surface in `.project/`. It keeps the current state short and resumable, while pushing only meaningful deltas into the task log. That is the core memory model: small live state, sparse durable history.

Implementation then happens inside the worktree, with verification driven by the type of change. Frontend work is not "tested" in the abstract; it is verified in the browser, with Playwright evidence collected into a stable repo-local log path. Docker-backed projects are handled with explicit worktree rules so switching branches does not turn into port collisions and stale containers.

The branch flow is PR-first into `dev`, while stable promotion happens through grouped `dev` to `main` release PRs.

## The Basic Workflow

1. Shape the work.
   - turn the request into a clear problem statement
   - define outcome, constraints, and non-goals
2. Run the blueprint fit check.
   - compare the issue against `.project/blueprint/`
   - stop if the blueprint blocks or contradicts the work
3. Open or refine the issue.
   - use rendered markdown templates
   - do not assemble long GitHub bodies inline
4. Initialize branch-local state.
   - one issue
   - one branch
   - one worktree
   - one `CURRENT.md`
   - one append-only task log
5. Implement.
   - work from the worktree
   - keep state resumable after context compaction
6. Verify.
   - select checks by change type
   - store browser evidence under `.project/logs/playwright/<module-id>/<run-id>/`
7. Open or update the PR to `dev`.
   - summarize implementation, verification, and blueprint impact
8. Release `dev` to `main` when requested.
   - grouped release PRs, not one stable merge per implementation PR

## Core Points

- Blueprint fit checks are mandatory for nontrivial work.
- Blueprint updates are mandatory only when durable project knowledge changed.
- Logging is delta-only.
- Verification is modality-specific.
- Browser verification requires evidence, not just a claim.
- Docker behavior across worktrees must be explicit.
- `dev` is the integration branch.
- `main` is the stable branch.

## What’s Inside

```text
skills/ora-et-labora/       shared principles, suite map, shared resources
skills/issue-shaping/       challenge record and issue drafting
skills/blueprint-guard/     blueprint fit check and durable blueprint updates
skills/state-logging/       CURRENT.md and delta-only task log discipline
skills/worktree-flow/       branch naming, worktrees, PR-to-dev, Docker rules
skills/verify-and-evidence/ modality-based verification and Playwright evidence
skills/release-train/       grouped dev-to-main release flow
skills/repo-bootstrap/      repo templates and GitHub defaults/bootstrap
scripts/                    install, sync, and validation helpers
examples/                   concrete end-to-end workflow examples
.github/workflows/          repo-level validation workflow
tests/                      script-level validation
```

The suite includes:

- a shared workflow overview under `skills/ora-et-labora`
- focused trigger skills for each major workflow phase
- detailed self-contained `SKILL.md` bodies with procedure, red flags, rationalization counters, and completion checklists
- issue, PR, release, brainstorm, current-state, and log templates
- bootstrap assets for `.github/` and `.project/blueprint/`
- helper scripts for template rendering, issue workspace initialization, and Playwright artifact collection

The operating procedure is intentionally inline in the skill files. Extra files are reserved for templates, scripts, bootstrap assets, tests, and examples.

## Skill Roles

- `ora-et-labora`
  - shared philosophy, operating model, and reusable resources
  - lightweight umbrella skill, not the main phase trigger
- `issue-shaping`
  - turns rough ideas into challenge records and clean GitHub issues
- `blueprint-guard`
  - checks feasibility against `.project/blueprint/` and decides when blueprint updates are mandatory
- `state-logging`
  - keeps resumable state minimal and durable after context compaction
- `worktree-flow`
  - owns branch naming, worktree lifecycle, Docker coexistence, and PRs into `dev`
- `verify-and-evidence`
  - chooses verification modalities and stores browser evidence correctly
- `release-train`
  - prepares grouped `dev` to `main` release PRs
- `repo-bootstrap`
  - applies workflow templates and bootstraps repo conventions

## Install

Install the full suite from this repo:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo emmepra/ora-et-labora \
  --path skills/ora-et-labora \
  --path skills/issue-shaping \
  --path skills/blueprint-guard \
  --path skills/state-logging \
  --path skills/worktree-flow \
  --path skills/verify-and-evidence \
  --path skills/release-train \
  --path skills/repo-bootstrap
```

Restart Codex after installation so the skill is discovered.

If you are developing from a local clone and want an update-friendly path, use:

```bash
python scripts/sync_local_suite.py --overwrite
```

That copies the suite directly into your local Codex skills directory and is useful when iterating on the repo itself.

## Local Validation

Run the whole suite validator:

```bash
python scripts/validate_all.py
```

Or run the bundled tests directly:

```bash
cd tests
python -m unittest
```

Validate the skill shape:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ../skills/ora-et-labora
```

Repeat for the other skill folders when editing them directly.

## Examples

Start with:

- [Frontend Bugfix With Browser Evidence](examples/01-frontend-bugfix.md)
- [Docker Across Two Worktrees](examples/02-docker-multi-worktree.md)
- [Grouped Release Train](examples/03-release-train.md)
- [Bootstrap A New Repo](examples/04-repo-bootstrap.md)
