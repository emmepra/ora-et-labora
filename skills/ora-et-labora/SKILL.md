---
name: ora-et-labora
description: Use when a repo task needs the Ora et Labora suite map, shared artifact model, skill selection guidance, or template/script locations.
---

# ora-et-labora

Use this skill as the suite index and shared operating model.

This is not the main execution skill for most tasks. The focused peer skills own the actual workflow phases. Use this skill to decide which phase skill applies, to understand the artifact model, or to find suite templates and scripts.

## Overview

Ora et Labora is a repo-first workflow for agentic software development. It turns rough work into durable issues, checks feasibility against the project blueprint, executes in a branch worktree, verifies with the right modality, routes PRs through the correct branch lane, and promotes grouped releases from `dev` to `main`.

Core principle: durable workflow truth must live in the repo, while branch-local task workspace state may stay local to the developer machine.

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
| `worktree-flow` | creating/resuming task branches, worktrees, rebasing, Docker worktree runtime, or PRs in the selected branch lane |
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
   - Create or update the local task workspace plus the durable task log.
4. Start implementation branch.
   - Use `worktree-flow`.
   - Select the branch lane first. Normal work branches from `dev` and targets `dev`; epic child work targets the owning epic branch; hotfix work branches from and targets `main`.
5. Verify.
   - Use `verify-and-evidence`.
   - Select checks by change surface and preserve browser evidence when relevant.
6. Open or update implementation PR.
   - Use `worktree-flow`, `state-logging`, and `verify-and-evidence`.
   - Render PR body from a file or template.
7. Close the merged task workspace.
   - Use `state-logging` and `worktree-flow`.
   - Retire the merged local task workspace under `.project/todo/<task-id>/` and the owning worktree/local branch with the cleanup helper.
8. Release.
   - Use `release-train`.
   - Promote grouped `dev` work to `main` with release checks and rollback notes. Hotfixes are the exception: they may target `main` first, then must be reconciled back into `dev`.
9. Create new repos.
   - Use `repo-init`.
   - Confirm owner/org, visibility, repo type, source mode, local path, and branch model before creating GitHub remotes.
10. Bootstrap existing repos.
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
- The normal lane uses one issue, one owning branch, one worktree, one local resumable task workspace, and one append-only log per nontrivial task. The epic lane and hotfix lane below are explicit overrides to this default. The epic lane replaces the old module-branch wording and must not revive the legacy module lifecycle.
- Choose verification modalities based on the change type. Do not treat "tests" as a single generic step.
- For frontend-impacting work, require browser verification locally and prefer CI browser coverage as well.
- Treat Playwright artifacts as required evidence for browser verification, not as disposable temp output.
- Open implementation PRs into the selected lane target. Normal implementation PRs target `dev`; child PRs inside an epic target `epic/<slug>`; hotfix PRs target `main`.
- Implementation PRs must reference the originating issue with a GitHub closing keyword, such as `Closes #123`, so the issue closes when the PR is merged into the default branch. For epic child PRs, also link the parent epic issue or tracking issue.
- Implementation PRs into `dev` may use agent auto-merge only after branch freshness, verification, CI/review, issue-closure, and state-logging gates are satisfied.
- Promote `dev` to `main` through grouped release PRs, not one `main` merge per implementation PR.
- Release PRs into `main` require explicit user approval before merge; do not enable auto-merge for stable releases by default.
- Render GitHub issue and PR bodies from files or templates. Do not assemble complex markdown inline in a shell command.

## Artifact Ownership

| Artifact | Owns | Should not contain |
| --- | --- | --- |
| GitHub issue | problem, scope, constraints, acceptance criteria, verification plan | command logs, branch status, implementation diary |
| `.project/todo/<task-id>/` | local task or epic workspace (`00_brainstorm.md`, `CURRENT.md`, draft PR body) | durable published history, raw browser artifacts |
| task log | meaningful deltas and state transitions | every command, every edit, repeated issue text |
| `.project/blueprint/` | durable project model and workflow invariants | task-local notes, transient blockers |
| PR body | implementation summary, closing issue reference, verification evidence, risks, rollback/follow-ups | unresolved template placeholders, raw traces |
| release PR | grouped scope, release checks, migrations, rollback | individual implementation diaries |

## Visibility Profiles

Ora et Labora supports three repository modes:

| Profile | Use for | Default artifact policy |
| --- | --- | --- |
| `private` | personal/private projects | version `.project/blueprint` and concise `.project/logs`; keep `.project/todo`, `.project/worktrees`, and optional local archives local-only |
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

## Branch Lanes And Release Rules

This section is authoritative. It overrides older shorthand that implied every task always has exactly one issue, one branch, and one PR directly into `dev`. It also replaces the old `module` terminology with `epic` for multi-issue integration work and does not revive the legacy mandatory `create/run/review module` lifecycle.

Repository branches:

- `main` is the deployment-ready stable branch.
- `dev` is the updated integration branch where normal completed work accumulates before release.
- `epic/<slug>` branches are optional temporary integration lanes for large multi-PR epics.

Preferred branch names:

- `feat/<issue>-<slug>` for normal feature work targeting `dev`.
- `fix/<issue>-<slug>` for normal bug work targeting `dev`.
- `chore/<issue>-<slug>` for maintenance work targeting `dev`.
- `epic/<slug>` for an optional parent epic integration branch.
- `hotfix/<issue>-<slug>` for urgent production fixes branching from `main` and targeting `main`.

Preferred worktree folder names avoid slashes, such as `fix-123-login-race`, `epic-payments-v2`, or `hotfix-123-login-outage`.

Branch lanes:

- Normal lane: `dev -> feat|fix|chore/<issue>-<slug> -> PR to dev -> grouped release PR to main`. Use this for ordinary features, fixes, refactors, docs, and chores.
- Epic lane: `dev -> epic/<slug> -> child issue branches -> PRs to epic/<slug> -> draft epic PR becomes ready -> PR to dev`. Use this only when several child PRs must integrate together before the combined outcome is safe on `dev`. Open a draft PR from `epic/<slug>` to `dev` immediately after creating the epic branch unless the user explicitly says the epic is local or experimental. Each child PR must link its issue and the parent epic issue or tracking issue. Because GitHub closing keywords in child PRs targeting an epic branch may not close issues until the work reaches the default branch, the final epic PR into `dev` must include `Closes #...` references for all child issues, or the parent epic issue must explicitly track child closure. The draft epic PR is the coordination surface for scope, child issues, checklist/status, CI, verification plan, and final readiness; mark it ready only after child work is merged, verified, and reconciled with latest `dev`.
- Hotfix lane: `main -> hotfix/<issue>-<slug> -> PR to main -> reconcile to dev`. Use this for production breakage, deployment-blocking regressions, security-sensitive fixes, data-loss risk, or other priority fixes that should not wait for the next `dev -> main` release. Keep the patch narrow, verify against the stable behavior, require explicit user approval before merging to `main`, and immediately backport, merge, or cherry-pick the fix into `dev`.
- Release stabilization lane: `dev -> release PR to main`, with only release-blocking fixes admitted into the release path. Non-blocking new work continues targeting `dev` or an epic lane.

Parallel epic discipline:

- Multiple `epic/<slug>` branches may exist in parallel, but every active epic draft PR must stay visible and describe overlapping surfaces.
- Each epic branch must rebase on `origin/dev` regularly and before its draft PR is marked ready.
- After one epic merges into `dev`, all other active epic branches must rebase on updated `origin/dev` before merging more child PRs or marking the epic ready.
- If an epic changes shared contracts, APIs, schemas, auth, routing, deployment config, or core UI conventions, affected parallel epics must rebase immediately and record the impact in their draft PRs or task state.
- If two epics modify the same contract, surface the overlap in both draft PRs and decide merge order. If one epic depends on another, make the dependency explicit and keep the dependent epic blocked or stacked until the base epic lands.

Merge and approval rules:

- Normal implementation PRs may use `gh pr merge --auto` only when all auto-merge gates are satisfied.
- Epic child PRs may use auto-merge only if the epic branch owner, branch freshness, verification, CI/review, issue-linking, and state gates are satisfied.
- Release PRs promote grouped `dev` changes to `main` and require explicit user approval before merge, even when checks are green.
- Hotfix PRs into `main` require explicit user approval before merge, even when checks are green.
- After any hotfix merge to `main`, reconciling the same fix into `dev` is mandatory before the hotfix lane is considered complete.

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
- Browser evidence belongs under `.project/logs/playwright/<task-id>/<run-id>`.
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
- `close_task_workspace.py`: retire merged local task state and the owning worktree/local branch through a dry-run-first cleanup flow.
- `bootstrap_repo_templates.py`: copy GitHub templates, blueprint docs, the standalone PR-body workflow, and workflow examples into a target repo.
- `bootstrap_repo_templates.py --visibility <profile>`: also writes the profile-aware artifact policy into `.gitignore`.
- `collect_playwright_artifacts.py`: collect browser verification artifacts into `.project/logs/playwright/<task-id>/<run-id>/`.

Prefer scripts for deterministic file layout and template rendering.

## Red Flags - Suite Misuse

- "I will remember this in chat instead of writing repo state."
- "I will skip the blueprint check because the issue is obvious."
- "I will use one log file for every branch."
- "I will open a PR to `main` for normal feature work."
- "I will route urgent production breakage through the normal `dev` release train when a narrow hotfix to `main` is required."
- "I will merge a hotfix to `main` and forget to reconcile it back into `dev`."
- "I will use an epic branch for routine one-issue work."
- "I will create a new `module/<slug>` branch instead of `epic/<slug>` for multi-issue work."
- "I will revive the legacy mandatory module lifecycle instead of using the current epic lane."
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
- PR opened or updated against the selected lane target (`dev`, `epic/<slug>`, or `main` for hotfixes)
- PR body references and closes the originating issue
- task state and log reflect the latest truth
- merged local task state is retired and the worktree is cleaned up when the branch is complete

If any item is intentionally skipped, state why.
