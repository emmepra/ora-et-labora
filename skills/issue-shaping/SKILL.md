---
name: issue-shaping
description: Shape nontrivial bugs and features before implementation. Use when Codex needs to turn a rough idea into a challenge record, capture constraints and acceptance criteria, draft or refine a GitHub issue body, or prepare `00_brainstorm.md` before code is written.
---

# issue-shaping

Use this skill before implementation starts.

## Overview

Turn a rough request into an implementation-ready issue shape without writing code.

## Responsibilities

- clarify the problem and intended outcome
- capture constraints, non-goals, risks, and acceptance checks
- produce or update `00_brainstorm.md`
- draft or refine the GitHub issue body with templates

## Rules

- do not jump into implementation
- shape the issue enough that another agent could start without rereading the whole chat
- keep the brainstorm file focused on challenge, feasibility, options, and risks
- use rendered markdown templates instead of assembling complex GitHub markdown inline
- keep the source of truth split clean:
  - GitHub issue: problem, acceptance criteria, verification plan
  - `00_brainstorm.md`: challenge record, tradeoffs, risks, feasibility notes
- if the request is trivial enough that no branch-local state or issue is needed, keep the shaping lightweight and avoid unnecessary ceremony

## Output Contract

Produce or refine:

- a clear problem or outcome statement
- constraints and non-goals
- acceptance checks
- risks or unknowns
- a challenge record in `00_brainstorm.md`

For the brainstorm file, include:

- problem
- desired outcome
- constraints
- blueprint fit placeholder or early feasibility notes
- options considered
- chosen direction
- risks / unknowns
- acceptance checks

## Common Mistakes

- writing code before the issue shape is stable
- opening a GitHub issue with no acceptance criteria
- mixing implementation details into the issue before feasibility is clear
- composing complex issue markdown inline in the shell instead of rendering a body file

## Resources

- use `../ora-et-labora/assets/templates/brainstorm.md`
- use `../ora-et-labora/assets/templates/issue-bug.md`
- use `../ora-et-labora/assets/templates/issue-feature.md`
- use `../ora-et-labora/scripts/render_template.py` when deterministic body rendering is helpful

## Handoff

Once the issue is shaped, move to `blueprint-guard`.
