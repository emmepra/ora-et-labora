---
name: state-logging
description: Maintain minimal but durable execution state for nontrivial work. Use when Codex needs to initialize or update `CURRENT.md`, append only meaningful deltas to the task log, or preserve resumable state across context compaction without redundant logging.
---

# state-logging

Use this skill whenever a task has enough scope to need resumable state.

## Overview

Keep execution state minimal, durable, and resumable after context compaction.

## Responsibilities

- initialize branch-local task state
- keep `CURRENT.md` short and current
- keep the task log delta-only
- avoid repeating information that already lives in GitHub or blueprint docs

## Rules

- one issue, one branch, one worktree, one `CURRENT.md`, one task log
- `CURRENT.md` is overwrite-in-place state, not history
- the task log is append-only, but only for meaningful deltas
- do not log every command, edit, or commit

## Source Of Truth

Use one source of truth per concern:

- GitHub issue: issue scope and acceptance criteria
- `00_brainstorm.md`: design tradeoffs and feasibility
- `CURRENT.md`: current resumable state
- task log: history worth remembering
- PR: implementation and verification summary
- release PR: promotion to stable

## Resources

- use `../ora-et-labora/scripts/init_issue_workspace.py`
- use `../ora-et-labora/assets/templates/current.md`
- use `../ora-et-labora/assets/templates/log.md`

## Meaningful Deltas

- chosen approach changed
- blocker appeared or cleared
- verification result changed
- PR state changed
- release state changed

## Common Mistakes

- duplicating issue text into `CURRENT.md`
- treating the task log like a command transcript
- storing historical notes in `CURRENT.md` instead of the log
