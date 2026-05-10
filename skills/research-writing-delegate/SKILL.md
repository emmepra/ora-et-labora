---
name: research-writing-delegate
description: Use when drafting, rewriting, or reviewing academic prose for research papers, LaTeX manuscripts, abstracts, introductions, related work, theory sections, or paper revisions with an external model.
---

# Research Writing Delegate

## Overview

Use an external model as a bounded prose drafter, not as the paper owner. Codex owns context selection, source discipline, critique, user approval, and final integration.

## Core Rules

- Send the smallest brief that can produce a useful draft. Do not send a whole paper by default.
- Before an external call, disclose the provider/model and summarize the material that will leave the machine if the brief includes unpublished, sensitive, or collaborator-owned text.
- Save raw delegate output in local task state or `.project/logs/` before editing it.
- Never patch generated prose into the manuscript without Codex review.
- Never run a second generation pass without first showing Codex's review and proposed revision brief to the user, unless the user explicitly enabled automation for the task.
- Do not store API keys in the repo, skill folder, issues, PRs, logs, or chat. Use environment variables, a local untracked `.env`, or a secret manager.

## Credential Setup

OpenRouter is the default provider. Set `OPENROUTER_API_KEY` in the environment, or use `RESEARCH_WRITING_DELEGATE_API_KEY` as a skill-specific override. Use `OPENAI_API_KEY` only when calling the helper with `--provider openai`.

The default OpenRouter model is `openai/gpt-5.2`. Override it with `RESEARCH_WRITING_DELEGATE_MODEL` or `--model`. The helper requires structured-output support from the routed provider so malformed prose drafts fail fast instead of bypassing the JSON contract.

Copy `.env.example` to a local untracked `.env` if needed:

```bash
cp skills/research-writing-delegate/.env.example .env
```

Keep `.env` local-only. The committed file is only a template. The helper automatically loads `skills/research-writing-delegate/.env` when present; pass `--env-file <path>` to use a different local file. Optional OpenRouter request metadata can be set with `OPENROUTER_SITE_URL` and `OPENROUTER_APP_NAME`.

## Prompt And Template Assets

Runtime prompt and artifact contracts are versioned with the skill:

- `prompts/delegate_system.md`: system prompt sent to OpenRouter/OpenAI.
- `templates/brief.schema.json`: initial brief contract.
- `templates/revision_brief.schema.json`: regeneration brief contract; requires user approval.
- `templates/minimal_brief.json`: starting point for compact first-pass briefs.
- `templates/revision_brief.json`: starting point for user-approved regeneration.
- `templates/review.md`: Codex review artifact before integration or regeneration.

The helper validates initial and revision briefs before dry-run or API calls. This does not replace Codex judgment; it prevents obvious under-specified or unsafe delegation.

## Brief Levels

| Level | Use when | Include |
| --- | --- | --- |
| `minimal` | rewriting or drafting one paragraph | task, goal, target length, current/neighboring text, constraints |
| `grounded` | claims or citations matter | minimal brief plus selected excerpts, citation keys, allowed uses |
| `structural` | section flow matters | grounded brief plus outline and paper-level claim boundaries |

Default to `minimal`; escalate only when the review task needs more context.

## Input Brief

Use JSON or YAML-shaped content with these fields when available:

```yaml
task:
  type: draft_paragraph | rewrite | tighten | bridge | abstract | critique
  target: paragraph | subsection | introduction | related_work | theory | limits
  goal: what the passage must accomplish
  length: desired length or range
context:
  before: short preceding excerpt
  current: optional current draft
  after: short following excerpt
  outline: 3-5 bullets max
claims:
  may_make: []
  must_not_make: []
sources:
  - citation_key: key
    excerpt: short excerpt
    usable_for: specific permitted use
style:
  sample: optional short sample
  constraints: theory-forward, no empirical overclaiming, etc.
feedback:
  previous_draft: only after user-approved revision loop
  requested_changes: only after user-approved revision loop
```

Initial briefs must not include `feedback`. Use `--brief-kind revision` only after Codex has reviewed the delegate output, shown the review to the user, and the user approved sending feedback back to the model.

## Output Contract

The delegate must return:

- `draft`: candidate prose.
- `claims_used`: claims the draft relies on.
- `assumptions`: assumptions introduced by the draft.
- `citation_needs`: citations needed or weakly supported.
- `weak_points`: prose, logic, or evidence weaknesses.
- `revision_notes`: suggestions for the next pass.
- `risk_flags`: overclaiming, invented citation, missing source, scope drift, or confidentiality concerns.

## Codex Review Rubric

Before integration or regeneration, review the delegate output against:

- argument fit: whether the prose advances the requested local function without changing the paper's scope.
- claim fit: whether every substantive claim is in `claims.may_make` or already present in the supplied context.
- source fit: whether source excerpts and citation keys are used only for their stated `usable_for` purpose.
- citation risk: whether the draft needs support that was not present in the brief.
- style fit: whether the passage matches nearby manuscript prose instead of generic academic phrasing.
- overclaiming: whether the draft turns theory, framing, or exploratory evidence into unsupported empirical claims.

Record the decision in `templates/review.md` before showing a regeneration recommendation to the user.

## Workflow

1. Build a compact brief from the repo, paper, blueprint, and source material.
2. Show the brief summary before the external call when sensitive text is involved.
3. Call the delegate and save the artifact.
4. Create a Codex review artifact from `templates/review.md`.
5. Review the output against the paper's claims, sources, tone, and neighboring text.
6. Show the review and recommendation: accept with edits, regenerate, manually edit, or discard.
7. If regenerating, build a `templates/revision_brief.json`-shaped brief with `feedback.user_approved: true` only after the user approves.
8. Apply only the reviewed and approved text to the manuscript.
9. Verify manuscript-impacting changes with the relevant LaTeX/PDF/render check when practical.

## Helper Script

Dry-run the request payload without an API key:

```bash
python skills/research-writing-delegate/scripts/call_delegate.py \
  --brief .project/todo/<task-id>/delegate-brief.json \
  --dry-run
```

Run through OpenRouter and save a local artifact:

```bash
python skills/research-writing-delegate/scripts/call_delegate.py \
  --brief .project/todo/<task-id>/delegate-brief.json \
  --out .project/todo/<task-id>/delegate-output.json
```

Run a user-approved regeneration pass:

```bash
python skills/research-writing-delegate/scripts/call_delegate.py \
  --brief-kind revision \
  --brief .project/todo/<task-id>/delegate-revision-brief.json \
  --out .project/todo/<task-id>/delegate-output-v2.json
```

Use OpenAI's Responses API explicitly when needed:

```bash
python skills/research-writing-delegate/scripts/call_delegate.py \
  --provider openai \
  --model gpt-5.5 \
  --brief .project/todo/<task-id>/delegate-brief.json \
  --out .project/todo/<task-id>/delegate-output.json
```

Use `--env-file <path>` only with an untracked local file. CLI flags such as `--model` override `.env` values.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Sending the whole manuscript | Send the local section, neighboring text, and only source excerpts needed |
| Treating delegate text as final | Review claims, citations, tone, and fit before integration |
| Autoregenerating after critique | Show Codex's review and ask before sending feedback |
| Putting feedback in a first-pass brief | Use `--brief-kind revision` and require `feedback.user_approved: true` |
| Storing keys in `.project/` or skill files | Use environment variables, local `.env`, or a secret manager |
| Letting notebook prose become paper truth | Promote relied-upon claims into blueprint, source notes, code, or manuscript artifacts |
