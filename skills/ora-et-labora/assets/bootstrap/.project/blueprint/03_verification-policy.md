# Verification Policy

- Verification modality must match the type of change.
- Backend or API work should use the appropriate unit, integration, contract, and migration checks.
- Frontend-impacting work requires browser verification.
- Browser evidence should be stored under `.project/logs/playwright/<module-id>/<run-id>/`.
- PRs should summarize the verification verdict and reference the meaningful browser evidence path when relevant.
