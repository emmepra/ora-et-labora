# Template Enforcement Hardening

## Problem

Ora et Labora recommends issue/PR templates, but the creation path is still easy to bypass.

## Decision

Harden template usage in four places:

- disable blank issues in bootstrapped repos
- add dedicated helper scripts for issue and PR creation from templates
- tighten skill wording so wrapper/body-file usage is the required path
- add tests that protect these rules

## Acceptance Checks

- issue template config exists and disables blank issues
- helper scripts render bodies and drive `gh ... --body-file`
- skill docs point to the wrappers as the standard path
- validation passes
