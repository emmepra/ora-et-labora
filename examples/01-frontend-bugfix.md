# Example: Frontend Bugfix With Browser Evidence

## Scenario

- Issue: login modal closes unexpectedly after failed submit
- Surface: frontend behavior plus API response handling

## Workflow

1. `issue-shaping`
   - write the challenge record
   - define expected vs observed behavior
2. `blueprint-guard`
   - verify the fix fits the current auth flow and frontend error-handling blueprint
3. `state-logging`
   - initialize `CURRENT.md` and the task log
4. `worktree-flow`
   - create `fix/123-login-modal-close`
   - work in `.project/worktrees/fix-123-login-modal-close`
5. `verify-and-evidence`
   - run build/static checks
   - verify the failure path in the browser
   - collect screenshots/trace under `.project/logs/playwright/123/<run-id>/`
6. PR to `dev`
   - summarize fix
   - include browser evidence path

## Key Point

The browser evidence path matters as much as the pass/fail verdict. The agent should not claim the modal behavior is fixed without durable browser evidence when the UI behavior was the problem.
