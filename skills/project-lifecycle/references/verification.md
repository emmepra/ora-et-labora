# Verification Reference

## Principle

Verification should match the change surface. Do not collapse all validation into a single generic "test" step.

## Modality Matrix

### Process / docs only

- markdown or schema validation
- formatting or lint checks
- link or structural checks when relevant

### Backend / API

- unit tests for local logic
- integration tests for boundary behavior
- contract checks for schemas or API changes
- migration or data-shape checks when state changes
- direct probing for critical endpoints or CLI paths when needed

### Frontend / UI

- local build and static checks
- component or unit tests if the repo supports them
- browser verification for user-visible behavior
- screenshots, traces, videos, or logs when the browser run is relevant to the task outcome

### Cross-stack

- combine the backend and frontend modalities that apply
- ensure one verification summary covers the end-to-end path

## Browser Evidence Policy

For browser verification, treat artifacts as durable evidence when they support a fix, a claim, or a PR.

Store them under:

```text
.project/logs/playwright/<module-id>/<run-id>/
```

Recommended contents:

- `manifest.json`
- `summary.md`
- `trace.zip` when available
- `video.webm` when available
- `screenshot-*.png` for key visual states
- `stdout.log` or exported command output when useful

## Logging Rule

Do not paste large artifact details into `CURRENT.md` or the task log.

Instead:

- record the verdict
- record the run ID or path
- record only the specific evidence needed to justify the state change

## CI Expectation

If the project supports browser automation in CI, PRs affecting frontend behavior should have at least a smoke-level browser gate in CI, even when the primary evidence was gathered locally.
