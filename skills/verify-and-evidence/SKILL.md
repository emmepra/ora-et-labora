---
name: verify-and-evidence
description: Choose verification modalities based on the change surface and store durable evidence for important checks. Use when Codex needs to decide which tests actually apply, run browser verification, collect Playwright artifacts, or summarize verification evidence for CURRENT.md and PRs.
---

# verify-and-evidence

Use this skill before claiming the work is done.

## Overview

Choose the right verification modalities for the change and store durable evidence for the checks that matter.

## Responsibilities

- choose the right verification modalities
- ensure frontend-impacting work gets browser verification
- collect Playwright evidence into the repo-local log surface
- summarize the verdict without dumping raw command noise

## Rules

- do not collapse validation into one generic "test" step
- browser verification requires evidence when it supports a fix, a claim, or a PR
- keep large artifacts in `.project/logs/playwright/<module-id>/<run-id>/`
- record the verdict and evidence path, not raw artifact dumps, in logs and PRs

## Modality Matrix

- docs/process-only:
  - markdown or schema validation
  - formatting or lint checks
  - link or structural checks when relevant
- backend/API:
  - unit tests
  - integration tests
  - contract checks
  - migration or data-shape checks
  - direct probing for critical endpoints or CLI paths when needed
- frontend/UI:
  - local build and static checks
  - component or unit tests if the repo supports them
  - browser verification for user-visible behavior
- cross-stack:
  - combine the backend and frontend modalities that apply

## Browser Evidence Policy

For browser verification, treat artifacts as durable evidence when they support a fix, a claim, or a PR.

Store them under:

`.project/logs/playwright/<module-id>/<run-id>/`

Recommended contents:

- `manifest.json`
- `summary.md`
- `trace.zip` when available
- `video.webm` when available
- `screenshot-*.png` for key visual states
- `stdout.log` or exported command output when useful

## Logging Rule

Do not paste large artifact details into `CURRENT.md` or the task log.

Instead:

- record the verdict
- record the run ID or path
- record only the specific evidence needed to justify the state change

## CI Expectation

If the project supports browser automation in CI, PRs affecting frontend behavior should have at least a smoke-level browser gate in CI, even when the primary evidence was gathered locally.

## Resources

- use `../ora-et-labora/scripts/collect_playwright_artifacts.py`
- use `../ora-et-labora/assets/templates/pr.md`

## Common Mistakes

- treating browser verification as optional for frontend behavior changes
- claiming a fix without durable evidence
- dumping raw artifact noise into logs or PRs instead of a clean verdict and path
