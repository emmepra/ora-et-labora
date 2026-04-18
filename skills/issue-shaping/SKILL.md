---
name: issue-shaping
description: Use when a bug, feature, refactor, or workflow request is still rough, underspecified, risky, or likely to become GitHub issue work before implementation.
---

# issue-shaping

Use this skill before implementation starts. This skill is the entry point for turning a rough request into a challenge record and issue contract.

## Overview

Issue shaping prevents the agent from converting vague intent into code too early. The output is not a solution; it is an implementation-ready problem frame with constraints, acceptance checks, risk notes, and a clean issue body.

Core principle: if another agent cannot start from the shaped issue plus `.project/todo/<module-id>/00_brainstorm.md`, the issue is not shaped enough.

This skill is intentionally self-contained. Follow this file for the shaping procedure.

## When To Use

Use this skill when the user:

- describes a bug, feature, refactor, or workflow improvement that may require implementation
- asks to open, refine, or prepare a GitHub issue
- gives a rough idea and wants help deciding scope
- reports symptoms but the actual problem is not yet clear
- wants to brainstorm before coding
- mentions acceptance criteria, constraints, feasibility, tradeoffs, or "what should we do?"
- is about to start branch/worktree work but the issue contract is not stable

Do not use this skill for:

- a one-line typo or mechanical edit that the user explicitly wants done immediately
- pure discussion where the user does not want artifacts
- post-implementation PR writing, unless the issue contract itself must be repaired

## Quick Reference

| Situation | Required action |
| --- | --- |
| Rough request, no issue yet | Create a challenge record before any code work |
| Existing issue lacks acceptance criteria | Refine the issue body before implementation |
| User asks for quick implementation but scope is risky | Pause implementation and shape the risk first |
| Frontend-visible bug | Include browser verification in the issue plan |
| Docker/runtime concern | Include worktree and service-isolation assumptions |
| Blueprint may conflict | Mark the conflict for blueprint fit checking |

## Responsibilities

- clarify the problem and intended outcome before code changes
- capture constraints, non-goals, risks, unknowns, and acceptance checks
- produce or update `.project/todo/<module-id>/00_brainstorm.md`
- draft or refine the GitHub issue body using a template or body file
- identify the likely verification modalities early
- leave a clean handoff for blueprint checking and worktree setup

## Nontrivial Work Threshold

Treat work as nontrivial when any of these are true:

- more than one file or subsystem may change
- user-visible behavior changes
- API, schema, auth, deployment, Docker, CI, or release behavior may change
- frontend behavior must be checked in a browser
- the work benefits from a GitHub issue, branch, PR, or future audit trail
- the task could be resumed after context compaction
- the user asks for a durable workflow artifact

For trivial work, keep shaping short. A tiny task does not need a full issue lifecycle unless the user explicitly wants it.

## Source Of Truth Split

Do not duplicate every detail across every artifact.

| Artifact | Owns |
| --- | --- |
| GitHub issue | problem statement, scope, constraints, acceptance criteria, verification plan |
| `00_brainstorm.md` | challenge record, assumptions, options considered, feasibility notes, risks, blueprint fit placeholder |
| `CURRENT.md` | current resumable execution state after work starts |
| task log | meaningful deltas after execution starts |
| PR body | implementation summary and verification evidence |

If the same paragraph appears in all artifacts, the workflow is becoming redundant.

## Procedure

1. Classify the request.
   - Decide whether it is a bug, feature, refactor, chore, release, bootstrap, or process change.
   - Decide whether it is trivial or nontrivial.
   - If trivial, state the minimal plan and avoid heavy artifacts.
2. Extract the problem.
   - For bugs, separate observed behavior from expected behavior.
   - For features, separate desired outcome from proposed implementation.
   - For refactors, separate behavior-preserving goals from behavior-changing goals.
3. Capture constraints and non-goals.
   - Record what must not change.
   - Record compatibility, performance, release, UI, API, Docker, and CI constraints when relevant.
4. Challenge the idea.
   - Ask what would make the solution fail.
   - Identify assumptions that need verification.
   - Identify alternative approaches if the initial approach is not obviously correct.
5. Draft acceptance checks.
   - Each acceptance check should be observable.
   - Avoid vague checks like "works correctly."
   - For frontend work, include browser-observable acceptance checks.
6. Draft the verification plan.
   - List local checks.
   - List browser checks if UI behavior is touched.
   - List CI expectations if the work will enter PR flow.
7. Create or update `00_brainstorm.md`.
   - Use the brainstorm template when starting a new module.
   - Keep it focused on challenge and feasibility, not implementation progress.
8. Draft or refine the GitHub issue body.
   - Use `issue-bug.md` for bugs.
   - Use `issue-feature.md` for features.
   - Use a body file with `gh issue create --body-file <file>` when creating the issue.

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

## Quality Bar

A shaped issue is ready only when:

- the problem can be explained without rereading the chat
- the desired outcome is observable
- the scope has at least one explicit non-goal or boundary
- acceptance checks are concrete
- verification modalities are named
- any suspected blueprint conflict is visible
- the issue body is valid markdown rendered from a file or template

## Red Flags - Stop Before Coding

- "This is obvious, I can code first and document later."
- "The GitHub issue can be fixed after the PR."
- "Acceptance criteria are implicit."
- "The browser check can be decided after implementation."
- "The blueprint probably fits, no need to check."
- "I will paste a long markdown body directly into a shell command."

All of these mean the shaping step is incomplete.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "The task is small, so no shaping is needed." | Small may be true; decide explicitly. If it touches user-visible behavior or PR flow, shape at least the acceptance checks. |
| "The user already explained it in chat." | Chat history is not durable after compaction. Capture the durable contract. |
| "I can open a vague issue and refine later." | Vague issues become vague branches. Refine before worktree setup. |
| "Implementation details belong in the issue." | Only stable scope and acceptance details belong there. Exploratory tradeoffs belong in `00_brainstorm.md`. |
| "Markdown formatting is not important." | Bad issue formatting breaks downstream review and PR consistency. Render from files. |

## Example Shape

For a frontend bug:

```markdown
Problem:
- Observed behavior: clicking "Save" leaves the form spinner active after a failed validation response.
- Expected behavior: validation errors render inline and the spinner stops.

Constraints:
- Preserve current API contract.
- Do not redesign the form layout.

Acceptance checks:
- Invalid submission shows the backend validation message.
- Spinner stops within the normal request lifecycle.
- Browser verification captures before/after evidence.

Verification plan:
- Run frontend unit tests if available.
- Run build/static checks.
- Use browser verification against the affected route.
- Store Playwright evidence under .project/logs/playwright/<module-id>/<run-id>/.
```

## Common Mistakes

- writing code before the issue shape is stable
- opening a GitHub issue with no acceptance criteria
- mixing implementation details into the issue before feasibility is clear
- composing complex issue markdown inline in the shell instead of rendering a body file
- treating the brainstorm file as a progress journal
- omitting non-goals and then expanding scope during implementation

## Templates And Tools

- `../ora-et-labora/assets/templates/brainstorm.md`
- `../ora-et-labora/assets/templates/issue-bug.md`
- `../ora-et-labora/assets/templates/issue-feature.md`
- `../ora-et-labora/scripts/render_template.py`

Use templates and rendered body files when producing GitHub issue markdown.

## Handoff

Once the issue is shaped, the next mandatory gate for nontrivial work is the blueprint fit check. Do not start implementation until the blueprint fit result is recorded or the user explicitly overrides the workflow.
