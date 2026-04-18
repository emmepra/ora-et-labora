---
name: blueprint-guard
description: Use when nontrivial work must be checked against `.project/blueprint/`, when project constraints may block an issue, or when durable project knowledge may need updating.
---

# blueprint-guard

Use this skill after issue shaping and before implementation.

## Overview

Blueprint guard prevents implementation from drifting away from the durable project model. It checks whether the shaped issue fits the repo's architecture, contracts, runtime assumptions, verification policy, branch model, and release policy.

Core principle: the blueprint is not a journal. It is the durable operating model another agent should be able to trust tomorrow.

This skill is self-contained. Follow this file for the blueprint guard procedure.

## When To Use

Use this skill when:

- a shaped bug, feature, refactor, chore, or bootstrap issue is about to enter implementation
- a request may conflict with architecture, API contracts, schema contracts, Docker runtime rules, CI, release policy, or branch policy
- `.project/blueprint/` is missing, stale, contradicted, or incomplete for the task
- implementation would require a durable project decision
- an agent is unsure whether a finding belongs in blueprint, task log, issue, or PR

Do not use this skill for:

- purely transient debugging notes
- command transcripts
- micro-progress updates
- one-off local setup details that will not help future agents

## Responsibilities

- identify the relevant blueprint files
- evaluate fit, constraints, and conflicts
- record the fit check in `00_brainstorm.md`
- decide whether blueprint updates are mandatory
- stop implementation when the blueprint contradicts the issue
- keep durable project knowledge separate from task-local history

## Quick Reference

| Finding | Destination |
| --- | --- |
| Project architecture boundary | `.project/blueprint/` |
| API, schema, auth, runtime, CI, or release invariant | `.project/blueprint/` |
| Issue-specific tradeoff | `00_brainstorm.md` |
| Current branch status | `CURRENT.md` |
| Failed attempt worth remembering | task log |
| Verification result | `CURRENT.md`, task log, PR |
| User-facing work contract | GitHub issue |

## Mandatory Rule

Every nontrivial issue gets a blueprint fit check before implementation starts.

Blueprint update on every issue is not mandatory.

Blueprint update is mandatory only when the work changes durable project knowledge.

## Fit Check Procedure

1. Find the applicable blueprint.
   - Look for `.project/blueprint/` in the target repo or worktree.
   - If absent, record that the blueprint is missing and decide whether repo bootstrap is needed.
   - If a closer project policy uses a different durable context folder, follow that project policy.
2. Identify relevant blueprint surfaces.
   - Architecture and module boundaries.
   - API, schema, and data contracts.
   - Auth, permissions, environment, and runtime assumptions.
   - Docker and multi-worktree rules.
   - CI, testing, browser verification, and evidence policy.
   - Branch, PR, release, and deployment policy.
3. Compare the issue against those surfaces.
   - Does the issue fit the architecture?
   - Does it require a new contract or contract change?
   - Does it require a runtime or Docker assumption that is not documented?
   - Does it change what must be tested?
   - Does it affect release or rollback behavior?
4. Decide the fit result.
   - `fits`: implementation can proceed under current blueprint.
   - `fits-with-assumptions`: implementation can proceed, but assumptions must be recorded in `00_brainstorm.md`.
   - `blocked`: implementation must stop until the conflict is resolved.
   - `blueprint-update-required`: implementation may proceed only after or alongside durable blueprint updates.
5. Record the result in `00_brainstorm.md`.
   - Relevant blueprint docs.
   - Fit result.
   - Assumptions.
   - Conflicts or missing decisions.
   - Required blueprint updates, if any.

## Valid Fit Check Answers

A valid fit check answers all of these:

- which blueprint files are relevant
- whether the issue fits current architecture and workflow constraints
- what assumptions the issue relies on
- what conflicts or missing decisions exist
- whether implementation may proceed
- whether `.project/blueprint/` must be updated

## What Counts As Durable Project Knowledge

Durable project knowledge is information that future agents or maintainers need beyond this single task.

Examples:

- a new module boundary or ownership rule
- a new API endpoint contract
- a changed database schema expectation
- a Docker compose project naming rule for worktrees
- a required browser verification path for UI changes
- a CI gate required before PR merge
- a new release or rollback policy
- a stable environment variable contract
- a persistent limitation or invariant in the architecture

## When Blueprint Updates Are Mandatory

Update `.project/blueprint/` when the issue changes durable project knowledge, such as:

- architecture boundaries
- API or schema contracts
- runtime assumptions
- CI or verification policy
- branch or release policy
- operator workflow invariants

Use concise durable prose. Blueprint docs should not become long implementation diaries.

## When Blueprint Updates Are Not Mandatory

Do not update `.project/blueprint/` for:

- ordinary implementation progress
- one-off debugging details
- transient blockers
- PR status changes
- file-by-file progress notes

Put those details in `CURRENT.md`, the task log, or the PR.

## Heuristic

If another agent starting tomorrow would need this knowledge to avoid re-deriving the project model, it belongs in `.project/blueprint/`.

If the knowledge only helps resume this one task, it belongs in `CURRENT.md` or the task log.

## Red Flags - Stop Before Implementation

- "The blueprint probably fits, so I will skip the check."
- "I will update the blueprint after coding."
- "The issue contradicts the architecture, but I can work around it."
- "Docker or CI behavior changed, but it is just local setup."
- "The project has no blueprint and I can still proceed as if it does."
- "This belongs somewhere, so I will put it in every artifact."

All of these indicate the guard is failing.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "The fit is obvious." | Obvious fit still needs a one-line recorded result so future agents know it was checked. |
| "Blueprint updates are too heavy." | The fit check is mandatory; updates are conditional. Do not conflate them. |
| "This is only a Docker detail." | Docker worktree behavior affects validation and must be durable when it is project policy. |
| "The issue can decide architecture." | Issues can propose changes; blueprint records accepted durable project model. |
| "I will leave the conflict for implementation." | Implementation should not start while a blueprint conflict is unresolved. |

## Example Fit Check Entry

```markdown
## Blueprint Fit Check

- Relevant blueprint docs:
- .project/blueprint/00_workflow.md
- .project/blueprint/03_verification-policy.md
- .project/blueprint/04_docker-worktrees.md
- Fit assessment: fits-with-assumptions
- Assumptions:
- Existing frontend route ownership remains unchanged.
- Browser verification will use the existing local dev server.
- Conflicts or missing decisions:
- No conflict.
- Blueprint update required:
- No, this issue does not change durable project policy.
```

## Common Mistakes

- treating blueprint updates as mandatory on every issue
- skipping the fit check because the issue feels obvious
- letting implementation begin while a blueprint contradiction is still unresolved
- storing task progress in blueprint docs
- failing to record that no blueprint update was needed

## Completion Checklist

- relevant blueprint files identified or blueprint absence recorded
- fit result recorded in `00_brainstorm.md`
- assumptions and conflicts recorded
- blueprint update decision made explicitly
- implementation blocked if the blueprint contradicts the issue
- durable blueprint edits made when required

## Handoff Rule

If the issue fits the blueprint, move to state initialization and worktree setup.

If it does not fit, resolve the blueprint conflict first.
