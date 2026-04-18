# Blueprint Policy

## Fit Check

Every nontrivial issue must be evaluated against `.project/blueprint/` before implementation starts.

A valid fit check answers:

- which blueprint files are relevant
- whether the issue fits current architecture and workflow constraints
- what assumptions the issue relies on
- what conflicts or missing decisions exist

Record this in `00_brainstorm.md`.

## When Blueprint Updates Are Mandatory

Update `.project/blueprint/` when the issue changes durable project knowledge, such as:

- architecture boundaries
- API or schema contracts
- runtime assumptions
- CI/verification policy
- branch/release policy
- operator workflow invariants

## When Blueprint Updates Are Not Mandatory

Do not update `.project/blueprint/` for:

- ordinary implementation progress
- one-off debugging details
- transient blockers
- PR status changes
- file-by-file progress logs

## Heuristic

If another agent starting tomorrow would need this knowledge to avoid re-deriving the project model, it belongs in `.project/blueprint/`.
If the knowledge only helps resume this one task, it belongs in `CURRENT.md` or the task log.
