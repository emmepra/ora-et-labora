# ora-et-labora

Standalone source repository for reusable Codex workflow skills.

Current skill:
- `skills/project-lifecycle`

`project-lifecycle` standardizes a repo-first development flow:
- shape work before opening the issue
- run a mandatory blueprint fit check for nontrivial work
- create one issue, one branch, one worktree, and one resumable state surface
- keep logs delta-only
- verify work with the right modality for the change
- treat browser verification as evidence-driven, with disciplined Playwright artifacts
- handle Docker safely across multiple worktrees
- open PRs to `dev`
- release from `dev` to `main` in grouped release PRs

## Layout

```text
skills/project-lifecycle/   installable Codex skill
tests/                      script-level validation
```

## Install

Once this repo is published, install the skill from the repo path:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/ora-et-labora \
  --path skills/project-lifecycle
```

Restart Codex after installation so the skill is discovered.

## Local Validation

Run the bundled tests:

```bash
cd tests
python -m unittest
```

Validate the skill shape:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ../skills/project-lifecycle
```
