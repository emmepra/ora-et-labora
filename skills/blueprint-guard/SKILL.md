---
name: blueprint-guard
description: Run a mandatory blueprint fit check before nontrivial implementation. Use when Codex needs to compare an issue against `.project/blueprint/`, decide whether the work is feasible under current project constraints, or decide whether `.project/blueprint/` must be updated.
---

# blueprint-guard

Use this skill after issue shaping and before implementation.

## Responsibilities

- identify the relevant blueprint files
- evaluate fit, constraints, and conflicts
- record the fit check in `00_brainstorm.md`
- decide whether blueprint updates are mandatory

## Rules

- every nontrivial issue gets a fit check
- blueprint updates are required only when durable project knowledge changed
- stop and surface contradictions before coding

## Resources

- read `../ora-et-labora/references/blueprint-policy.md`
- read `../ora-et-labora/references/workflow.md`

## Handoff

If the issue fits the blueprint, move to `state-logging` and `worktree-flow`.
If it does not fit, resolve the blueprint conflict first.
