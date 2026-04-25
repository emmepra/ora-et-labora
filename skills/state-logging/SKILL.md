---
name: state-logging
description: Use when work needs resumable state, compact handoffs, task logs, context-compaction recovery, or disciplined updates to `CURRENT.md` and `.project/logs/`.
---

# state-logging

Use this skill whenever a task has enough scope to need resumable state.

## Overview

State logging keeps work recoverable after context compaction without turning the repo into a noisy command transcript. The local task workspace and the durable log are separate artifacts with different jobs.

Core principle: the local task workspace answers "what is the next useful action right now?" The task log answers "what changed that future agents must not lose?"

This skill is self-contained. Follow this file for the logging procedure.

## When To Use

Use this skill when:

- a task has a GitHub issue, branch, worktree, PR, or release train
- the work may last longer than one chat window
- the model may compact context before the task is complete
- another agent may need to resume the branch
- verification evidence, blockers, or PR state must be preserved
- the user asks for logs, state, resumability, memory management, or workflow discipline

Do not use this skill for:

- one-off questions
- trivial edits with no issue or branch
- daily note capture outside the project workflow
- dumping raw command output without a meaningful state change

## Responsibilities

- initialize branch-local task state
- keep `CURRENT.md` short, current, and overwrite-in-place
- keep the task log append-only and delta-only
- avoid repeating information that already lives in GitHub, blueprint docs, or the PR
- record verification verdicts and evidence paths without copying large artifacts
- provide a reliable compaction recovery path

## Artifact Model

| Artifact | Role | Update style |
| --- | --- | --- |
| `.project/todo/<module-id>/CURRENT.md` | local resumable live state | overwrite in place |
| `.project/logs/<module-id>.md` | durable meaningful history | append only |
| `.project/todo/<module-id>/00_brainstorm.md` | local challenge record and fit check | update during shaping/fit |
| GitHub issue | work contract | update when scope changes |
| Pull request | implementation and verification summary | update before review/merge |
| Release PR | grouped stable promotion | update during release |

## Source Of Truth

Use one source of truth per concern:

- GitHub issue: issue scope, acceptance criteria, and verification plan
- local task workspace (`00_brainstorm.md`, `CURRENT.md`): design tradeoffs, next step, blockers, and branch-local resumability
- task log: approach changes, blocker transitions, verification result changes, PR/release state changes
- PR: implementation summary, user-facing verification evidence, risk, rollback, follow-ups
- release PR: promotion scope, included PRs, release checks, rollback plan

## `CURRENT.md` Rules

`CURRENT.md` must stay short. It is local task-state, not a published changelog, and it should be readable in under one minute.

Keep:

- issue link
- title
- kind
- module ID
- branch
- status
- PR link or `pending`
- last verification verdict
- browser evidence path or `pending`
- next step
- blockers
- files touched only when useful for resumption

Do not keep:

- command transcripts
- detailed history
- every file touched
- the full issue body
- raw Playwright output
- large screenshots or artifact dumps

## Task Log Rules

The task log is append-only, but not exhaustive. Append only when there is a meaningful delta.

Meaningful deltas:

- chosen approach changed
- blocker appeared
- blocker cleared
- verification failed
- verification passed after previously failing or being pending
- browser evidence was collected
- PR opened, retargeted, marked ready, merged, or blocked
- originating issue was closed by PR merge or failed to close as expected
- release train prepared, checked, or merged
- blueprint changed because durable knowledge changed

Not meaningful by itself:

- ran `ls`
- opened a file
- fixed a typo
- made a micro-edit
- committed without changing state
- reran the same failing command with the same result
- copied data already present in the issue or PR

## Recommended Log Entry Shape

Use compact one-line entries unless more context is genuinely needed:

```markdown
- 2026-04-18 | verify:pass | local unit tests and browser smoke passed | evidence:.project/logs/playwright/123-login/20260418T101500Z
- 2026-04-18 | blocker:open | CI deploy job fails because required secret is missing
- 2026-04-18 | approach:change | switched from route-level patch to shared form-state fix after validation path review
```

Prefer searchable event labels:

- `state:init`
- `approach:change`
- `blocker:open`
- `blocker:closed`
- `verify:fail`
- `verify:pass`
- `browser:evidence`
- `pr:opened`
- `pr:ready`
- `release:prepared`
- `release:merged`

## Procedure

1. Identify the module ID.
   - Prefer the existing issue/module identifier.
   - Keep it stable across brainstorm, current state, log, branch, PR, and evidence paths.
2. Initialize state if missing.
   - Use `../ora-et-labora/scripts/init_issue_workspace.py` when creating the standard files.
   - Create the local `.project/todo/<module-id>/CURRENT.md`.
   - Create `.project/logs/<module-id>.md`.
3. Before substantial work, update `CURRENT.md`.
   - Status should reflect the active phase.
   - Next step should be concrete.
   - Blockers should be explicit.
4. During work, append log entries only at meaningful transitions.
   - Do not log every command.
   - Do not duplicate the PR body.
5. After verification, update both surfaces.
   - `CURRENT.md`: latest verdict and evidence path.
   - task log: the transition from pending/fail to pass, or the new failure.
6. Before PR handoff, make state resumable.
   - `CURRENT.md` should point to the PR and next action.
   - task log should include the verification state.
   - PR body should include the originating issue closing reference.
7. After merge or release, close the loop.
   - Record final merge/release state.
   - Confirm the originating issue closed when the implementation PR merged, or record the blocker/follow-up if it did not.
   - Update the local task workspace to done if the project keeps it briefly during handoff.
   - When the task branch is truly finished, use `../ora-et-labora/scripts/close_task_workspace.py --repo-root . --module-id <module-id>` to remove the local task workspace and retire the owning worktree/local branch. Review the dry-run plan first, then add `--apply`.

## Context Compaction Recovery

When resuming after compaction:

1. Read the closest `AGENTS.md`.
2. Read `.project/todo/<module-id>/CURRENT.md` if the local task workspace still exists.
3. Read the last meaningful entries in `.project/logs/<module-id>.md`.
4. Inspect the branch and PR state.
5. Run only the commands needed to refresh reality.
6. Update `CURRENT.md` if the resumed state differs.

Do not reconstruct the full history from memory. Trust the artifacts, then verify current repo state.

## Red Flags - Stop And Fix State

- "I will update the log at the end."
- "The chat has all the context."
- "I will paste the whole test output into the log."
- "I need both `CURRENT.md` and the log to repeat the issue body."
- "I changed approach but did not record why."
- "The PR is open, but `CURRENT.md` still says PR pending."
- "The PR merged, but nobody checked whether the issue closed."
- "Verification failed, but the current state still says pending or pass."

All of these mean the state surface is no longer trustworthy.

## Rationalization Countertable

| Excuse | Reality |
| --- | --- |
| "Logging every command is safer." | Command transcripts bury the signal. Log meaningful state transitions. |
| "I can rely on chat history." | Chat compacts and disappears. The repo-local state must survive. |
| "I'll update state after the PR." | Waiting until the end defeats resumability. Update at phase transitions. |
| "The issue already has this information." | Do not duplicate it. Link to the issue and keep only live state in `CURRENT.md`. |
| "The log should include raw browser artifacts." | Store artifacts under `.project/logs/playwright/...` and log the path plus verdict. |

## Templates And Tools

- `../ora-et-labora/scripts/init_issue_workspace.py`
- `../ora-et-labora/scripts/close_task_workspace.py`
- `../ora-et-labora/assets/templates/current.md`
- `../ora-et-labora/assets/templates/log.md`

Use the script for deterministic initial file layout. Edit the resulting files to keep them accurate.

## Completion Checklist

- `CURRENT.md` exists for nontrivial work
- task log exists for nontrivial work
- `CURRENT.md` has current branch, status, PR, verification, next step, and blockers
- PR and issue state are consistent after merge
- log contains meaningful transitions only
- verification verdict and evidence path are recorded when verification matters
- no raw artifact dumps or command transcripts were pasted into state files

## Common Mistakes

- duplicating issue text into `CURRENT.md`
- treating the task log like a command transcript
- storing historical notes in `CURRENT.md` instead of the log
- failing to update state after PR creation
- failing to record failed verification before fixing it
- recording "tests passed" without naming which checks passed
