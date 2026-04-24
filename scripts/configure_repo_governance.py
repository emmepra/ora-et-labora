#!/usr/bin/env python3
"""Convenience wrapper for the skill-owned repo governance helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "ora-et-labora"
    / "scripts"
    / "configure_repo_governance.py"
)
SPEC = importlib.util.spec_from_file_location("ora_configure_repo_governance", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


if __name__ == "__main__":
    raise SystemExit(MODULE.main())
