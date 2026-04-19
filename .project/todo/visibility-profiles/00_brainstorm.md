# Visibility-Aware Repo Modes

## Problem

Ora et Labora needs explicit public/private/internal repository modes so agents do not publish private workflow state in public repos or lose useful `.project` memory in private/internal repos.

## Challenge Collection

- Public repositories should not commit private agent state, raw browser artifacts, local paths, private hostnames, screenshots with sensitive content, or issue-planning notes.
- Private and internal repositories still benefit from versioned `.project/blueprint/`, `.project/todo/`, and concise `.project/logs/` because those files are the workflow memory layer.
- The rule must be executable, not just advisory, because agents otherwise forget it during repo init/bootstrap.
- Playwright artifact handling must stay disciplined across all modes: summaries and evidence paths are useful; raw traces, videos, HAR files, and screenshots are risky or noisy by default.

## Options

- Documentation only: too weak; agents can still forget the artifact policy.
- Script-only: too opaque; agents need to understand why each profile behaves differently.
- Skill docs plus bootstrap script: preferred because it gives both future-agent context and deterministic repo output.

## Decision

Implement profile-aware repo setup across the skill docs and bootstrap helper:

- `private`: version workflow memory, ignore worktrees and raw browser payloads.
- `internal`: same as private, with broader-reader caution.
- `public`: keep `.project/` and local agent state ignored by default; publish only sanitized public docs and GitHub templates.

## Blueprint Fit

- Fits Ora et Labora's repo-first memory model because the policy is stored in the repo and applied by a helper script.
- Updates durable workflow knowledge because visibility now affects artifact ownership and bootstrap behavior.
- Does not change branch or release policy.

## Verification Plan

- Add unit tests for default/private bootstrap behavior.
- Add unit tests for public bootstrap behavior.
- Run `python scripts/validate_all.py`.
