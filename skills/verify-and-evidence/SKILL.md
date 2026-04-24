---
name: verify-and-evidence
description: Use when deciding, running, recording, or challenging verification for code changes, browser behavior, Playwright artifacts, CI status, or PR readiness.
---

# verify-and-evidence

Use this skill before claiming work is done, before marking a PR ready, and whenever a verification claim needs evidence.

## Overview

Verification is not one generic "run tests" step. The correct checks depend on the change surface: docs, backend, API, schema, frontend, browser behavior, Docker runtime, CI, release, or cross-stack behavior.

Core principle: every completion claim must name the checks that actually support it. Frontend behavior requires browser evidence when it supports a fix, a PR, or a user-facing claim.

This skill is self-contained. Follow this file for the verification and evidence procedure.

## When To Use

Use this skill when:

- implementation is complete or nearly complete
- the user asks whether a fix is tested
- a PR is about to be opened, updated, or marked ready
- frontend-visible behavior changed
- Playwright, browser testing, screenshots, traces, or videos are involved
- CI is failing, pending, or required before merge
- Docker/runtime behavior may affect the check
- previous verification failed and needs re-run
- a release train needs current verification status

Do not use this skill to justify skipping verification because work is "small." Use it to decide the minimal correct verification.

## Responsibilities

- classify the change surface
- choose the verification modalities that actually apply
- run or request the relevant checks
- require browser verification for frontend-impacting work
- collect Playwright artifacts into a stable repo-local path
- record verdicts in `CURRENT.md`, the task log, and PR/release body as appropriate
- distinguish local verification from CI verification
- avoid raw command-noise dumps

## Quick Reference

| Change surface | Minimum verification expectation |
| --- | --- |
| docs/process only | markdown/schema/structural checks if available |
| backend logic | unit tests and targeted integration/API checks |
| API contract | contract tests, schema checks, direct endpoint probing |
| database/migration | migration apply/rollback or schema validation where supported |
| frontend behavior | build/static checks plus browser verification |
| UI-only styling | browser visual check and screenshot evidence |
| cross-stack feature | backend checks plus browser end-to-end path |
| Docker/runtime | rebuild/restart affected services before validation |
| release train | current CI, regression, migration, browser status as applicable |

## Modality Selection Procedure

1. Identify touched surfaces.
   - Review files changed and intended behavior.
   - Classify as docs, backend, API, schema, frontend, Docker, CI, release, or cross-stack.
2. Choose checks by surface.
   - Do not blindly run every test if a targeted set is enough.
   - Do not run only unit tests if the claim is browser-visible.
3. Refresh runtime if needed.
   - After rebase, pull, merge, dependency change, frontend build change, or container change, restart/rebuild the affected services.
4. Run local checks.
   - Capture command names and verdicts.
   - Keep raw output out of logs unless the failure text is essential.
5. Run browser verification when required.
   - Use the browser or Playwright flow that exercises the real user-visible path.
   - Capture evidence that would convince a reviewer.
6. Collect artifacts.
   - Move important browser artifacts into `.project/logs/playwright/<module-id>/<run-id>/`.
   - Create or keep a manifest and summary.
7. Record the result.
   - Update `CURRENT.md` with latest verdict and evidence path.
   - Append a task-log entry only when the verification result changed or materially matters.
   - Update PR body with local, browser, evidence, and CI status.
8. Challenge the claim.
   - Ask whether the checks actually cover the acceptance criteria.
   - If not, run the missing check or state the gap explicitly.

## Detailed Modality Matrix

Docs/process-only:

- markdown lint or formatting if available
- link checks if links changed
- template/schema validation if repository supports it
- skill validation if editing skills
- no browser check unless user-facing rendered docs are affected

Backend/API:

- unit tests for changed logic
- integration tests for service boundaries
- contract or schema tests when request/response shape changes
- direct API probing for critical endpoints
- migration/schema checks if persistence changes
- logs only when diagnosing service failures

Frontend/UI:

- static checks, typecheck, lint, or build if available
- component/unit tests if the repo supports them and the changed logic is testable there
- browser verification for user-visible behavior
- screenshot evidence for visual states
- trace/video when reproducing a flow, race, redirect, auth behavior, or interaction bug

Cross-stack:

- backend/API verification for server behavior
- frontend build/static checks
- browser end-to-end path through the changed user flow
- Docker/runtime restart before browser verification when services changed

CI/release:

- check current CI status, not stale runs
- distinguish "not run", "pending", "failed", and "passed"
- for release trains, include regression, browser, migration/schema, and rollback readiness where relevant
- for auto-merge, confirm current CI, review state, branch freshness, issue closure reference, and mergeability before enabling or performing the merge

## Browser Verification Is Required When

- user-visible frontend behavior changes
- visual layout, navigation, auth, form behavior, routing, loading states, or error states change
- a bug was reported by observable browser behavior
- the PR body will claim a UI fix
- the acceptance criteria mention user interaction
- screenshots, traces, or videos are needed to prove the fix

Browser verification may be skipped only when the change is provably not browser-visible, such as a backend-only test fixture or documentation-only update. If skipped, record why.

## Auto-Merge Readiness

Before enabling `gh pr merge --auto` or performing an immediate merge, verify the PR is actually eligible:

- target branch is `dev`
- PR is not a release PR into `main`
- latest branch state is rebased on `origin/dev`
- required CI is passing or pending under GitHub auto-merge
- no requested changes, unresolved review threads, merge conflicts, blocked labels, or explicit user hold are present
- local verification in the PR body matches the changed surface
- browser evidence is present when frontend-visible behavior changed
- PR body includes `Closes #<issue>` or an equivalent closing keyword
- `CURRENT.md` and the task log record the latest verification and auto-merge decision

If any item is unknown, treat auto-merge as blocked. Record the gap instead of enabling auto-merge optimistically.

## Playwright Artifact Policy

Store durable browser evidence under:

```text
.project/logs/playwright/<module-id>/<run-id>/
```

Recommended contents:

- `manifest.json`
- `summary.md`
- `trace.zip` when available
- `video.webm` when available
- `screenshot-*.png` for key states
- `stdout.log` when command output supports the verdict
- `stderr.log` when failure diagnostics matter

Use `../ora-et-labora/scripts/collect_playwright_artifacts.py` to collect artifacts when it fits the situation.

Example:

```bash
python ../ora-et-labora/scripts/collect_playwright_artifacts.py \
  --repo-root . \
  --module-id 124-login-spinner \
  --status pass \
  --summary "Invalid login now shows inline error and clears spinner" \
  --source /tmp/playwright-output/trace.zip \
  --source /tmp/playwright-output/screenshot-after.png
```

## What To Record

In `CURRENT.md`:

- latest local check verdict
- latest browser verdict if applicable
- evidence path
- next verification gap if any

In the task log:

- verification changed from pending/fail to pass
- verification failed with a new meaningful reason
- browser evidence was collected
- CI result changed in a way that affects readiness
- auto-merge was enabled, skipped, blocked, or completed

In the PR:

- local checks run
- browser check summary
- browser evidence path
- CI status
- auto-merge eligibility or explicit reason it is not requested
- verification gaps or skipped checks with reason

## Red Flags - Verification Not Good Enough

- "Tests passed" without naming which tests.
- "I checked it manually" without artifact or exact path.
- "The browser behavior should be fixed because the code changed."
- "CI passed yesterday before the rebase."
- "Auto-merge is enabled, so current verification no longer matters."
- "The screenshot is in `/tmp` and not preserved."
- "Frontend changed, but no browser verification was run."
- "Docker services changed, but the old containers were used."
- "I only ran unit tests for a cross-stack user flow."

All of these mean the verification claim is weak.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "The change is small." | Small frontend changes can break visible behavior. Pick the minimal correct check, not no check. |
| "Unit tests cover it." | Unit tests do not prove browser routing, layout, auth redirects, or interaction behavior. |
| "Manual testing is enough." | Manual testing can be enough only when the exact path and durable evidence are recorded. |
| "CI will catch it." | CI does not replace local targeted checks, and CI may not cover browser behavior. |
| "Artifacts are too noisy." | Store artifacts in the evidence path and summarize the verdict cleanly. |
| "I already ran this before rebasing." | Rebase can change behavior. Re-run relevant checks after sync. |

## Completion Checklist

- changed surfaces classified
- relevant local checks run or explicit gap recorded
- frontend-impacting work verified in browser
- Playwright/browser artifacts preserved when they support the claim
- `CURRENT.md` updated with verdict and evidence path
- task log updated only if the verification state changed meaningfully
- PR body includes local, browser, evidence, and CI status
- stale runtime state was avoided by restart/rebuild when needed

## Common Mistakes

- treating browser verification as optional for frontend behavior changes
- claiming a fix without durable evidence
- dumping raw artifact noise into logs or PRs instead of a clean verdict and path
- recording "passed" when CI is still pending
- relying on stale containers after a rebase
- failing to record skipped checks and why they were skipped
