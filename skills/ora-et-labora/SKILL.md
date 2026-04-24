---
name: ora-et-labora
description: Use when a repo task needs the Ora et Labora suite map, shared artifact model, skill selection guidance, or template/script locations.
---

# ora-et-labora

Use this skill as the suite index and shared operating model.

This is not the main execution skill for most tasks. The focused peer skills own the actual workflow phases. Use this skill to decide which phase skill applies, to understand the artifact model, or to find suite templates and scripts.

## Overview

Ora et Labora is a repo-first workflow for agentic software development. It turns rough work into durable issues, checks feasibility against the project blueprint, executes in a branch worktree, verifies with the right modality, opens PRs into `dev`, and promotes grouped releases to `main`.

Core principle: important workflow state must live in the repo, not in agent memory.

The suite intentionally keeps operative guidance inside each `SKILL.md`. Shared reusable materials are scripts and templates, not hidden procedure docs.

## When To Use This Skill

Use this umbrella skill when:

- the user asks what Ora et Labora does
- a request could match multiple Ora et Labora skills
- the agent needs the suite map
- the agent needs the artifact ownership model
- the agent needs to locate templates or helper scripts
- the task spans issue shaping, worktree flow, verification, and release

Do not use this skill as a substitute for the detailed phase skills. If the task clearly belongs to one phase, use that phase skill.

## Suite Skills

| Skill | Use when |
| --- | --- |
| `issue-shaping` | a rough bug, feature, refactor, or workflow request needs a durable challenge record or GitHub issue body |
| `blueprint-guard` | a shaped issue needs a fit check against `.project/blueprint/` or durable project knowledge may need updating |
| `state-logging` | work needs `CURRENT.md`, task logs, compaction recovery, or delta-only state discipline |
| `worktree-flow` | creating/resuming task branches, worktrees, rebasing, Docker worktree runtime, or PRs into `dev` |
| `verify-and-evidence` | choosing and recording tests, browser verification, Playwright evidence, CI status, or PR readiness |
| `release-train` | promoting grouped work from `dev` to `main`, release PRs, release checks, and rollback notes |
| `repo-init` | creating a new local or GitHub repo, choosing owner/org, visibility, repo type, source mode, and initial branch model |
| `repo-bootstrap` | applying Ora et Labora templates, `.project/blueprint/`, CI/release placeholders, and conventions to an existing repo |

## End-To-End Lifecycle

1. Shape the issue.
   - Use `issue-shaping`.
   - Produce a challenge record and issue body.
2. Check blueprint fit.
   - Use `blueprint-guard`.
   - Record fit, assumptions, conflicts, and blueprint update decision.
3. Initialize state.
   - Use `state-logging`.
   - Create or update `CURRENT.md` and the task log.
4. Start implementation branch.
   - Use `worktree-flow`.
   - Create/reuse a worktree, branch from `dev`, and keep PR target as `dev`.
5. Verify.
   - Use `verify-and-evidence`.
   - Select checks by change surface and preserve browser evidence when relevant.
6. Open or update implementation PR.
   - Use `worktree-flow`, `state-logging`, and `verify-and-evidence`.
   - Render PR body from a file or template.
7. Release.
   - Use `release-train`.
   - Promote grouped `dev` work to `main` with release checks and rollback notes.
8. Create new repos.
   - Use `repo-init`.
   - Confirm owner/org, visibility, repo type, source mode, local path, and branch model before creating GitHub remotes.
9. Bootstrap existing repos.
   - Use `repo-bootstrap`.
   - Apply templates, blueprint docs, branch defaults, and GitHub setting plan to a repo that already exists.

## Core Policy

- Read the closest `AGENTS.md` before acting.
- Treat `.project/` as the canonical operational surface unless the target repo explicitly chose a different convention before this skill was invoked.
- Choose the repository visibility profile before creating or bootstrapping workflow artifacts.
- For public repos, keep `.project/` local by default and publish only sanitized contributor-facing docs.
- Run a blueprint fit check for every nontrivial issue before implementation starts.
- Update `.project/blueprint/` only when durable project knowledge changes.
- Keep logs delta-only. Do not restate information that already lives in GitHub or `CURRENT.md`.
- Use one issue, one owning branch, one worktree, one resumable `CURRENT.md`, and one append-only log per nontrivial task.
- Choose verification modalities based on the change type. Do not treat "tests" as a single generic step.
- For frontend-impacting work, require browser verification locally and prefer CI browser coverage as well.
- Treat Playwright artifacts as required evidence for browser verification, not as disposable temp output.
- Open implementation PRs into `dev`.
- Implementation PRs must reference the originating issue with a GitHub closing keyword, such as `Closes #123`, so the issue closes when the PR is merged into the default branch.
- Implementation PRs into `dev` may use agent auto-merge only after branch freshness, verification, CI/review, issue-closure, and state-logging gates are satisfied.
- Promote `dev` to `main` through grouped release PRs, not one `main` merge per implementation PR.
- Release PRs into `main` require explicit user approval before merge; do not enable auto-merge for stable releases by default.
- Render GitHub issue and PR bodies from files or templates. Do not assemble complex markdown inline in a shell command.

## Artifact Ownership

| Artifact | Owns | Should not contain |
| --- | --- | --- |
| GitHub issue | problem, scope, constraints, acceptance criteria, verification plan | command logs, branch status, implementation diary |
| `00_brainstorm.md` | challenge record, assumptions, options, risks, blueprint fit | PR status, raw command output |
| `CURRENT.md` | current status, branch, PR, latest verification, next step, blockers | historical diary, full issue body, raw artifacts |
| task log | meaningful deltas and state transitions | every command, every edit, repeated issue text |
| `.project/blueprint/` | durable project model and workflow invariants | task-local notes, transient blockers |
| PR body | implementation summary, closing issue reference, verification evidence, risks, rollback/follow-ups | unresolved template placeholders, raw traces |
| release PR | grouped scope, release checks, migrations, rollback | individual implementation diaries |

## Visibility Profiles

Ora et Labora supports three repository modes:

| Profile | Use for | Default artifact policy |
| --- | --- | --- |
| `private` | personal/private projects | version `.project/blueprint`, `.project/todo`, and concise `.project/logs`; ignore worktrees and raw browser artifacts |
| `internal` | organization-visible private projects | same as private, but avoid personal notes and write for broader internal readers |
| `public` | open source or public portfolio work | version `.github` and sanitized public docs; keep `.project`, local issue workspaces, raw browser artifacts, and private agent instructions local by default |

Visibility affects workflow design. Do not treat it as only a GitHub setting.

When using `repo-init` or `repo-bootstrap`, apply the profile with:

```bash
python skills/ora-et-labora/scripts/bootstrap_repo_templates.py --repo-root <repo> --visibility <private|internal|public>
```

Public repos can still use Ora et Labora locally. The difference is that local operational memory stays outside the published source unless the user explicitly approves a sanitized subset.

## Nontrivial Work Definition

Treat work as nontrivial when any of these are true:

- it deserves a GitHub issue
- it touches multiple files or subsystems
- it changes user-visible behavior
- it changes API, schema, Docker, CI, release, auth, or deployment behavior
- it requires browser verification
- it may need a PR
- it should survive context compaction

Trivial work can skip the full lifecycle, but the decision should be explicit.

## Blueprint Rules

- Mandatory fit check for nontrivial work: yes.
- Mandatory blueprint update on every issue: no.
- Mandatory blueprint update when durable project knowledge changed: yes.

Durable project knowledge includes architecture boundaries, contracts, environment assumptions, CI/testing policy, Docker worktree rules, branch policy, release policy, and persistent operational invariants.

## Branch And Release Rules

- Preferred branch names:
  - `feat/<issue>-<slug>`
  - `fix/<issue>-<slug>`
  - `chore/<issue>-<slug>`
  - `hotfix/<issue>-<slug>`
- Preferred worktree folder names avoid slashes, such as `fix-123-login-race`.
- `dev` is the integration branch.
- `main` is the stable branch.
- implementation PRs target `dev`.
- implementation PRs include a closing issue reference, for example `Closes #123`.
- implementation PRs may use `gh pr merge --auto` only when all auto-merge gates are satisfied.
- release PRs promote grouped `dev` changes to `main`.
- release PRs require explicit user approval before merge, even when checks are green.

## Docker And Runtime Rules

- Default to one active Docker or Compose stack across worktrees.
- If switching worktrees, bring the current stack down before bringing the next stack up.
- Parallel stacks require isolated Compose project names, ports, env files/overrides, and service/container naming.
- After pull, rebase, or merge sync, rebuild or restart affected services before validating runtime behavior.
- Do not trust stale containers, stale dev servers, or old browser tabs as evidence of current behavior.

## Verification Rules

- Docs/process-only work needs structural checks if available.
- Backend/API work needs the relevant unit, integration, contract, migration, or direct probe checks.
- Frontend/UI work needs build/static checks plus browser verification.
- Cross-stack work needs the backend and frontend modalities that apply.
- Browser evidence belongs under `.project/logs/playwright/<module-id>/<run-id>/`.
- Record verification verdicts and evidence paths, not raw artifact dumps.

## Markdown Body Rules

Use templates and body files for complex GitHub markdown.

Use:

- `create_issue_from_template.py` for issue creation
- `create_pr_from_template.py` for PR creation
- `gh issue create --body-file <file>` only as a fallback after rendering a body file
- `gh pr create --body-file <file>` only as a fallback after rendering a body file

Avoid:

- long inline markdown in shell strings
- PR bodies without a `Closes #<issue>` or equivalent closing keyword for the originating issue
- unresolved placeholders
- hand-built PR bodies with inconsistent sections

## Reusable Templates

Template assets live under `assets/templates/`:

- `issue-bug.md`
- `issue-feature.md`
- `pr.md`
- `release-pr.md`
- `brainstorm.md`
- `current.md`
- `log.md`

Use these rather than recreating structure from memory.

## Reusable Scripts

Scripts live under `scripts/`:

- `render_template.py`: render markdown templates with strict placeholder replacement.
- `create_issue_from_template.py`: render an issue template and create the GitHub issue from the body file.
- `create_pr_from_template.py`: render a PR template and create the GitHub PR from the body file.
- `configure_repo_governance.py`: plan or apply default GitHub repo settings and a standard Ora et Labora issue label set.
- `validate_pr_body.py`: validate a PR body against the Ora et Labora PR template contract.
- `init_issue_workspace.py`: initialize `00_brainstorm.md`, `CURRENT.md`, and task log.
- `bootstrap_repo_templates.py`: copy GitHub templates, blueprint docs, the standalone PR-body workflow, and workflow examples into a target repo.
- `bootstrap_repo_templates.py --visibility <profile>`: also writes the profile-aware artifact policy into `.gitignore`.
- `collect_playwright_artifacts.py`: collect browser verification artifacts into `.project/logs/playwright/<module-id>/<run-id>/`.

Prefer scripts for deterministic file layout and template rendering.

## Red Flags - Suite Misuse

- "I will remember this in chat instead of writing repo state."
- "I will skip the blueprint check because the issue is obvious."
- "I will use one log file for every branch."
- "I will open a PR to `main` for normal feature work."
- "I will open the PR without `Closes #<issue>` and close the issue manually later."
- "I will skip the wrapper script and hand-write the issue or PR body inline."
- "I will enable auto-merge without checking CI, reviews, branch freshness, and task state."
- "I will auto-merge the release PR into `main` because checks are green."
- "I will publish `.project/` in a public repo because it is only process state."
- "I will claim frontend verification without browser evidence."
- "I will paste complex markdown directly into `gh issue create`."
- "I will use parallel Docker stacks without isolated ports and project names."

All of these mean the suite is being bypassed.

## Completion Standard

For any nontrivial task, completion requires:

- issue contract shaped
- blueprint fit checked
- branch-local state initialized
- work performed in the owning worktree
- relevant verification completed
- browser evidence preserved when frontend behavior changed
- PR opened or updated against `dev`
- PR body references and closes the originating issue
- task state and log reflect the latest truth

If any item is intentionally skipped, state why.
