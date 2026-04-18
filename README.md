# Ora et Labora

Ora et Labora is a repo-first workflow skill for coding agents.

It is not a bag of prompts. It is a working method for taking nontrivial software changes from rough idea to stable release without relying on agent memory or ad hoc habits.

The skill is built around a simple idea:

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
skills/ora-et-labora/   installable Codex skill
tests/                  script-level validation
```

The skill includes:

- a core workflow spec
- blueprint, verification, and Docker/worktree policy references
- issue, PR, release, brainstorm, current-state, and log templates
- bootstrap assets for `.github/` and `.project/blueprint/`
- helper scripts for template rendering, issue workspace initialization, and Playwright artifact collection

## Install

Install the skill from this repo path:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo emmepra/ora-et-labora \
  --path skills/ora-et-labora
```

Restart Codex after installation so the skill is discovered.

## Local Validation

Run the bundled tests:

```bash
cd tests
python -m unittest
```

Validate the skill shape:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ../skills/ora-et-labora
```
