---
name: repo-init
description: Use when creating a new local or GitHub repository, choosing owner/org, visibility, repo type, source mode, branch model, and applying Ora et Labora setup from the start.
---

# repo-init

Use this skill when a repository does not exist yet, or when the user wants Codex to create a new GitHub repo and initialize it with Ora et Labora conventions.

## Overview

Repo init owns the high-impact first setup decisions: repository owner, name, visibility, local path, source mode, repo type, initial branches, remote creation, and first bootstrap. It is distinct from `repo-bootstrap`, which applies workflow files and conventions to a repo that already exists.

Core principle: before creating a remote repo or mutating GitHub settings, show the creation plan and get explicit user approval.

This skill is self-contained. Follow this file for the repo creation and initialization procedure.

## When To Use

Use this skill when the user says or implies:

- create a new repo
- initialize a new GitHub repository
- start a new project repo
- create a private/public/internal repo under an account or organization
- create a repo from a local folder
- create a repo from a GitHub template
- scaffold a new repo and apply Ora et Labora
- choose repo type, branch model, visibility, or owner before repo creation

Do not use this skill when:

- the repo already exists and only needs Ora et Labora templates or `.project/blueprint/`; use `repo-bootstrap`
- the user only wants to shape an issue; use `issue-shaping`
- the user only wants a branch/worktree for an existing issue; use `worktree-flow`
- creating a remote repo would be premature or unapproved

## Relationship To Repo Bootstrap

Use `repo-init` for creation.

Use `repo-bootstrap` for applying workflow structure to an existing repo.

In a full new-repo flow, `repo-init` creates or prepares the repo, then applies the same baseline workflow surfaces that `repo-bootstrap` manages:

- `.github/ISSUE_TEMPLATE/`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/` placeholders
- `.project/blueprint/`
- `dev` as integration branch
- `main` as stable branch

## Required Inputs

Ask for only the missing critical inputs. If the user already supplied them, do not ask again.

Required before remote creation:

- owner: personal account or organization, such as `emmepra` or `my-org`
- repo name
- visibility: private, public, or internal
- visibility profile: derived from visibility unless the user explicitly wants different artifact behavior
- local path or parent folder
- source mode
- repo type

Useful optional inputs:

- description
- homepage
- template repository
- license
- gitignore template
- stack hints
- CI profile
- Docker expectation
- Playwright/browser testing expectation
- branch protection/ruleset preference
- whether to push immediately

## Repo Type Choices

Use one of these repo types unless the user gives a clearer custom type:

- `frontend-app`: UI app, browser behavior expected, likely build/static/browser checks
- `backend-api`: server/API service, likely unit/integration/API checks
- `full-stack-app`: frontend plus backend, likely cross-stack and browser checks
- `library-package`: reusable package, likely unit/build/package checks
- `cli-tool`: command-line tool, likely CLI behavior checks
- `infra-runtime`: Docker, deployment, CI/CD, or runtime tooling
- `docs-research`: docs, publishing, research, or manuscript repo
- `template-repo`: intended to be reused as a GitHub template
- `monorepo`: multiple packages/apps, needs explicit structure choices

The repo type should drive initial CI placeholders, verification policy wording, browser evidence expectations, and Docker notes.

## Source Modes

Choose exactly one source mode:

- `new-empty`: create a local folder and initialize a new repo
- `existing-local`: use an existing local folder as the source
- `github-template`: create from a GitHub template repository
- `remote-only`: create the GitHub remote without local content
- `scaffolded`: create a local starter layout before creating/pushing the remote

Default to `new-empty` only when the user has not indicated an existing source.

## Visibility Profiles

Repository visibility is not only a GitHub setting. It controls which workflow artifacts are safe to publish.

Use one of these profiles:

| Profile | Default for | Versioned workflow state | Ignored/local workflow state |
| --- | --- | --- | --- |
| `private` | personal private repos | `.project/blueprint/**`, concise `.project/logs/**` summaries, `.github/**`, project `AGENTS.md` when useful | `.project/todo/**`, `.project/worktrees/**`, optional local archives, raw Playwright/browser payloads, secrets, `.env`, local-only overrides |
| `internal` | organization-only repos | same as `private`, but assume broader internal readers and avoid personal/private notes | `.project/todo/**`, `.project/worktrees/**`, optional local archives, raw Playwright/browser payloads, secrets, local-only overrides |
| `public` | open source or public portfolio repos | `.github/**`, sanitized public docs, optionally a short public `AGENTS.md` if contributor-safe | `.project/**` by default, `AGENTS.local.md`, local challenge logs, raw Playwright/browser payloads, private planning notes |

For public repos, do not publish private agent operational state by default. Translate stable, contributor-useful knowledge into public docs such as `CONTRIBUTING.md`, `SECURITY.md`, `docs/architecture.md`, `docs/testing.md`, or `docs/release.md`. Keep `.project/` local unless the user intentionally approves a sanitized subset.

For private and internal repos, durable workflow memory can still be part of the repository, but not every local working surface should be published. Keep `.project/blueprint/**` and concise `.project/logs/**` versioned; keep `.project/todo/**`, `.project/worktrees/**`, and any local archive space on the developer machine. Raw browser artifacts should still be handled carefully: commit concise summaries and evidence paths; keep large traces, videos, HAR files, and screenshots local unless a project explicitly wants curated artifacts versioned.

## Confirmation Gate

Repository creation is high-impact. Before running `gh repo create`, show the plan and ask for approval.

The confirmation must include:

- owner/repo
- visibility
- local path
- source mode
- repo type
- visibility profile and artifact publication policy
- remote creation command shape
- whether the first push will happen
- branch model: `dev` default, `main` stable
- whether Ora et Labora bootstrap files will be applied
- whether `.project/`, `AGENTS.md`, and public docs will be versioned, local-only, or intentionally skipped
- whether branch protection/rulesets will be configured now or recorded as pending

Do not create the GitHub repo before this approval.

## New Repo Procedure

1. Resolve target context.
   - Read the closest `AGENTS.md`.
   - Determine where the local repo should live.
   - Check whether the target path already exists.
   - Check whether the GitHub repo name may already exist if practical.
2. Collect inputs.
   - Owner/org.
   - Repo name.
   - Visibility.
   - Visibility profile.
   - Repo type.
   - Source mode.
   - Local path.
   - Initial stack hints.
3. Produce the creation plan.
   - Keep it concrete.
   - Include the exact `OWNER/REPO`.
   - Include the visibility profile and artifact policy.
   - Include commands to be run conceptually.
   - Ask for explicit approval before GitHub creation.
4. Prepare the local repo.
   - For `new-empty`, create the folder and run `git init`.
   - For `existing-local`, inspect the folder and avoid overwriting.
   - For `github-template`, use `gh repo create --template`.
   - For `remote-only`, do not create local files unless requested.
   - For `scaffolded`, create only the agreed starter structure.
5. Create the GitHub repo.
   - Use `gh repo create OWNER/REPO --private`, `--public`, or `--internal`.
   - Use `--source <path> --remote origin --push` only when pushing local content is part of the approved plan.
   - Use `--template OWNER/TEMPLATE` only for template-based creation.
6. Establish branch model.
   - Ensure `main` exists as stable branch.
   - Ensure `dev` exists as integration branch.
   - Set `dev` as default with `gh repo edit --default-branch dev` after the remote branch exists.
7. Apply Ora et Labora workflow setup.
   - Copy or adapt issue templates.
   - Copy or adapt PR template.
   - Copy or adapt `.project/blueprint/` for `private` and `internal` repos.
   - For `public` repos, keep `.project/` local by default and translate stable guidance into public docs if requested.
   - Add CI/release placeholders appropriate for the repo type.
   - Apply the profile-aware `.gitignore` policy with `bootstrap_repo_templates.py --visibility <profile>`.
   - Plan or apply the standard repo settings and label bundle with `configure_repo_governance.py`.
   - Keep placeholders clearly marked until project-specific commands are known.
8. Commit and push initial setup if approved.
   - Keep initial commit scoped to repo initialization.
   - Push both `main` and `dev` when branch model is being established.
9. Report the result.
   - Repo URL.
   - Local path.
   - Default branch.
   - Stable branch.
   - Files created.
   - Checks run.
   - Branch protection/ruleset status.
   - Remaining manual steps.

## GitHub Command Patterns

Create a new private repo:

```bash
gh repo create OWNER/REPO --private
```

Create and push from an existing local repo:

```bash
gh repo create OWNER/REPO --private --source . --remote origin --push
```

Create from a template:

```bash
gh repo create OWNER/REPO --private --template TEMPLATE_OWNER/TEMPLATE_REPO
```

Set default branch after `dev` exists remotely:

```bash
gh repo edit OWNER/REPO --default-branch dev
```

Plan the standard governance changes first:

```bash
python skills/ora-et-labora/scripts/configure_repo_governance.py --repo OWNER/REPO
```

Apply them explicitly after approval:

```bash
python skills/ora-et-labora/scripts/configure_repo_governance.py --repo OWNER/REPO --apply
```

Do not claim branch protection or rulesets are configured unless the command/API call has actually succeeded.

## Branch Setup Pattern

Preferred model:

- `main`: stable branch
- `dev`: integration/default branch

Safe sequence for a local initialized repo:

1. create initial commit on `main`
2. push `main`
3. create `dev` from `main`
4. push `dev`
5. set default branch to `dev`

If the GitHub account default branch starts as something else, adapt safely but end with `dev` as default and `main` as stable unless the user chooses otherwise.

## Repo Type Effects

Frontend app:

- PR template must include browser evidence.
- `.project/blueprint/03_verification-policy.md` should stress browser verification.
- CI placeholder should mention build/static and browser smoke/e2e.

Backend API:

- CI placeholder should mention unit, integration, contract, and API probes.
- Blueprint should document API contract ownership.

Full-stack app:

- CI placeholder should combine backend and frontend checks.
- Docker worktree policy should be explicit if local services are containerized.
- Browser evidence is expected for user-visible flows.

Library/package:

- CI placeholder should mention package build, unit tests, and publish dry-run if relevant.
- Release policy should mention versioning/tagging if known.

CLI/tooling:

- CI placeholder should include command behavior tests.
- README/bootstrap may need usage examples.

Docs/research:

- CI placeholder may be markdown, link, or compile checks.
- Browser evidence usually not applicable unless docs are rendered and user-visible.

## Branch Protection And Rulesets

Branch protection and rulesets are desirable but should be handled carefully.

If requested:

- inspect whether the repo has required CI checks yet
- configure rules only after branch names and workflows are stable
- use `gh api` or GitHub settings automation as needed
- report exactly what was configured

If not configured:

- record as pending
- do not imply protection exists

The current governance helper covers:

- default branch
- delete branch on merge
- auto-merge enablement
- update-branch allowance
- merge/squash/rebase merge method toggles
- a default issue label set including `bug`, `enhancement`, `chore`, `docs`, and `release`

Branch protection and rulesets should still be reported as pending unless separately configured.

## Red Flags - Stop Before Creating

- owner/org is unclear
- repo visibility is unclear
- visibility profile or artifact publication policy is unclear
- local path already exists and may be overwritten
- remote repo may already exist
- source mode is unclear
- user has not approved the creation plan
- branch model conflicts with the user's request
- template repo is not specified for template mode
- `gh repo create` would run under the wrong authenticated account

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "The owner is probably personal." | Ask or infer only if explicit context makes it safe. Wrong owner is costly. |
| "Private is a safe default." | It is safer than public, but still ask if visibility was not specified. |
| "Public can use the same `.project` policy as private." | Public repos need a publishing boundary. Keep agent-private state local unless explicitly sanitized. |
| "I can create the repo and fix branches later." | Branch model is part of initialization. Plan it before creation. |
| "Branch protection can be claimed from the template files." | Protection is a GitHub setting. Report it as pending unless configured. |
| "Repo type does not matter yet." | Repo type determines templates, CI placeholders, verification policy, and browser evidence expectations. |

## Completion Checklist

- owner/org confirmed
- repo name confirmed
- visibility confirmed
- local path confirmed
- source mode confirmed
- repo type confirmed
- user approved remote creation plan
- GitHub repo created or intentionally skipped
- `main` stable branch exists when applicable
- `dev` integration/default branch exists when applicable
- Ora et Labora workflow files applied or intentionally deferred
- visibility profile applied to `.gitignore` and workflow artifacts
- initial commit/push completed or intentionally skipped
- branch protection/ruleset status reported accurately
- final response includes repo URL, local path, branch model, and pending steps

## Common Mistakes

- using `repo-bootstrap` to create a remote repo
- creating a GitHub repo before confirming owner and visibility
- setting default branch before `dev` exists remotely
- leaving `main` as default when the intended workflow says `dev`
- applying frontend CI placeholders to backend-only repos
- forgetting to report branch protection as pending
- overwriting an existing local folder without approval
- publishing `.project/` or private planning logs in a public repo without explicit sanitization
