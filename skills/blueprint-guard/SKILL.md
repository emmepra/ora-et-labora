---
name: blueprint-guard
description: Run a mandatory blueprint fit check before nontrivial implementation. Use when Codex needs to compare an issue against `.project/blueprint/`, decide whether the work is feasible under current project constraints, or decide whether `.project/blueprint/` must be updated.
---

# blueprint-guard

Use this skill after issue shaping and before implementation.

## Overview

Decide whether the issue actually fits the current project blueprint and whether the blueprint must change before implementation.

## Responsibilities

- identify the relevant blueprint files
- evaluate fit, constraints, and conflicts
- record the fit check in `00_brainstorm.md`
- decide whether blueprint updates are mandatory

## Rules

- every nontrivial issue gets a fit check
- blueprint updates are required only when durable project knowledge changed
- stop and surface contradictions before coding

## Fit Check

A valid fit check answers:

- which blueprint files are relevant
- whether the issue fits current architecture and workflow constraints
- what assumptions the issue relies on
- what conflicts or missing decisions exist

Record the result in `00_brainstorm.md`.

## When Blueprint Updates Are Mandatory

Update `.project/blueprint/` when the issue changes durable project knowledge, such as:

- architecture boundaries
- API or schema contracts
- runtime assumptions
- CI or verification policy
- branch or release policy
- operator workflow invariants

## When Blueprint Updates Are Not Mandatory

Do not update `.project/blueprint/` for:

- ordinary implementation progress
- one-off debugging details
- transient blockers
- PR status changes
- file-by-file progress notes

## Heuristic

If another agent starting tomorrow would need this knowledge to avoid re-deriving the project model, it belongs in `.project/blueprint/`.
If the knowledge only helps resume this one task, it belongs in `CURRENT.md` or the task log.

## Common Mistakes

- treating blueprint updates as mandatory on every issue
- skipping the fit check because the issue feels obvious
- letting implementation begin while a blueprint contradiction is still unresolved

## Handoff

If the issue fits the blueprint, move to `state-logging` and `worktree-flow`.
If it does not fit, resolve the blueprint conflict first.
