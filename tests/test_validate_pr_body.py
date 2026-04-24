from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_pr_body.py"
SPEC = importlib.util.spec_from_file_location("validate_pr_body", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
validate_body = MODULE.validate_body


class ValidatePrBodyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = REPO_ROOT / "skills" / "ora-et-labora" / "assets" / "templates" / "pr.md"

    def test_accepts_valid_body(self) -> None:
        body = """## Summary

- Adds a PR body validation gate.

## Why

This makes template structure a real CI requirement.

## Linked Issue

Closes #8

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable
- Browser evidence: not applicable
- CI: pending after PR creation

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.

## Blueprint Updates

No blueprint updates required.

## Risks / Rollback

Rollback: revert this PR.

## Follow-ups

- Sync installed skills after merge.
"""
        self.assertEqual(validate_body(body, self.template), [])

    def test_rejects_missing_section(self) -> None:
        body = """## Summary

- Adds a PR body validation gate.

## Linked Issue

Closes #8

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable
- Browser evidence: not applicable
- CI: pending after PR creation

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.

## Blueprint Updates

No blueprint updates required.

## Risks / Rollback

Rollback: revert this PR.

## Follow-ups

- Sync installed skills after merge.
"""
        errors = validate_body(body, self.template)
        self.assertIn("Missing required section header: ## Why", errors)

    def test_rejects_missing_closes_reference(self) -> None:
        body = """## Summary

- Adds a PR body validation gate.

## Why

This makes template structure a real CI requirement.

## Linked Issue

References #8

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable
- Browser evidence: not applicable
- CI: pending after PR creation

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.

## Blueprint Updates

No blueprint updates required.

## Risks / Rollback

Rollback: revert this PR.

## Follow-ups

- Sync installed skills after merge.
"""
        errors = validate_body(body, self.template)
        self.assertIn("Linked Issue section must contain a `Closes #<issue>` reference.", errors)

    def test_rejects_unresolved_placeholders(self) -> None:
        body = """## Summary

{{SUMMARY}}

## Why

This makes template structure a real CI requirement.

## Linked Issue

Closes #8

## Verification

- Local: `python scripts/validate_all.py`
- Browser: not applicable
- Browser evidence: not applicable
- CI: pending after PR creation

## Auto-Merge Eligibility

- Agent auto-merge requested: yes, once required checks pass.

## Blueprint Updates

No blueprint updates required.

## Risks / Rollback

Rollback: revert this PR.

## Follow-ups

- Sync installed skills after merge.
"""
        errors = validate_body(body, self.template)
        self.assertEqual(
            errors[0],
            "PR body contains unresolved template placeholders: {{SUMMARY}}",
        )


if __name__ == "__main__":
    unittest.main()
