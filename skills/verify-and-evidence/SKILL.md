---
name: verify-and-evidence
description: Choose verification modalities based on the change surface and store durable evidence for important checks. Use when Codex needs to decide which tests actually apply, run browser verification, collect Playwright artifacts, or summarize verification evidence for CURRENT.md and PRs.
---

# verify-and-evidence

Use this skill before claiming the work is done.

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

## Resources

- read `../ora-et-labora/references/verification.md`
- use `../ora-et-labora/scripts/collect_playwright_artifacts.py`
- use `../ora-et-labora/assets/templates/pr.md`

## Modalities

- docs/process: structural checks as needed
- backend/API: unit, integration, contract, migration, probing as needed
- frontend/UI: build/static checks plus browser verification
- cross-stack: combine the relevant modalities
