# Overlay privacy critique

- Strongest failure mode: a host-facing overlay can contain raw state, event payloads, metadata, paths, or credentials even when it is labeled read-only.
- Selected action: route all LUCIDA overlay methods through the existing bounded projection and update internal calculations to read typed state directly.
- Alternative rejected: preserve the old raw overlay for compatibility; it would retain the privacy defect and make future consumers likely to copy it.
- Reversibility: the change is local to LUCIDA and the safe fields already have a tested contract; callers that need state can use explicit state APIs.
- Verification signal: focused boundary tests, full suite, redaction assertions, and clean diff.
