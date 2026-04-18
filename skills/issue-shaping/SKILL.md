---
name: issue-shaping
description: Shape nontrivial bugs and features before implementation. Use when Codex needs to turn a rough idea into a challenge record, capture constraints and acceptance criteria, draft or refine a GitHub issue body, or prepare `00_brainstorm.md` before code is written.
---

# issue-shaping

Use this skill before implementation starts.

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

## Resources

- use `../ora-et-labora/assets/templates/brainstorm.md`
- use `../ora-et-labora/assets/templates/issue-bug.md`
- use `../ora-et-labora/assets/templates/issue-feature.md`
- use `../ora-et-labora/scripts/render_template.py` when deterministic body rendering is helpful
- read `../ora-et-labora/references/workflow.md` for artifact boundaries

## Handoff

Once the issue is shaped, move to `blueprint-guard`.
