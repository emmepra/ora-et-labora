---
name: linear-bridge
description: Use when Linear issues, projects, or captured planning items need to be connected to GitHub issues, PRs, Ora et Labora execution state, or repo-local evidence.
---

# linear-bridge

## Overview

Linear is the planning and cross-project backlog layer. GitHub issues and PRs remain the repo-local execution contract. Ora et Labora still owns shaping, blueprint fit, worktrees, verification, PRs, and evidence.

Use this skill to connect those layers without turning Linear into an implementation log or replacing `.project/logs`.

## When To Use

Use this skill when:

- the user asks Codex to work from a Linear issue or Linear project
- a captured Linear item needs routing into a repo, GitHub issue, or Ora et Labora task
- an implementation PR should be linked back to Linear
- a planning decision made in Linear should be reflected in repo-local workflow state
- Codex needs to comment progress, blockers, verification, or PR links back to Linear

Do not use this skill for:

- raw note capture that belongs in Obsidian
- ordinary GitHub-only implementation when no Linear object exists
- replacing `state-logging`; keep repo execution evidence in `.project/logs`
- broad Linear cleanup or workspace reorganization unless explicitly requested

## Layer Contract

| Layer | Owns |
| --- | --- |
| Linear issue | planning item, priority, project backlog position, cross-project visibility |
| Linear project | outcome/backlog grouping across one area of work |
| GitHub issue | repo-local implementation contract, acceptance criteria, verification plan |
| PR | code change, review, CI, merge record |
| `.project/logs` | concise execution evidence and meaningful deltas |
| `.project/blueprint` | durable repo knowledge and workflow invariants |

One Linear issue can map to no GitHub issue, one GitHub issue, or several GitHub issues. Create GitHub issues only when repo-local implementation or review needs them.

## Capture And Triage Defaults

For the personal capture flow:

- new iPhone or MacBook captures land in `linear-personal`, team `Cerebro`
- use project `Capture & Triage`
- use source labels such as `capture:iphone` or `capture:macbook`
- use the team's existing backlog-like state for raw captures unless the workspace has a dedicated `Triage` status

Triage should:

- retitle obvious raw captures
- ask questions as Linear comments when information is missing
- attach clear items to the right Linear project
- leave unclear items in the capture project or move them to the team's review/clarification state
- avoid creating GitHub issues until a repo and implementation boundary are clear

## Work From Linear

When the user asks to execute a Linear item:

1. Read the Linear issue and project.
2. Identify the target repo from the issue, project, links, comments, or AGENTS routing.
3. Read the closest repo `AGENTS.md` and blueprint before changing files.
4. Decide whether a GitHub issue is needed.
   - If implementation is nontrivial or PR-bound, create or link a GitHub issue.
   - If the work is tiny, a PR can link directly to the Linear issue instead.
5. Use Ora et Labora phase skills for shaping, blueprint fit, state, worktree, verification, and PR flow.
6. Link both directions:
   - Linear comment or description: `GitHub: owner/repo#123` and PR link when available.
   - GitHub issue or PR body: `Linear: <issue key or URL>`.
7. Comment back to Linear only with high-signal updates: GitHub issue, PR, blocker, decision needed, verification result, completion.

## Common Mistakes

- Do not mirror every GitHub issue into Linear. Link selectively.
- Do not use Linear comments as an implementation diary. Keep command/test evidence in repo logs and PR bodies.
- Do not move private captured ideas into shared Linear workspaces without user approval.
- Do not let a scheduled triage job start coding. Triage can classify and ask; execution needs a clear user trigger or an approved queue.
