# Self-critique

- finding: restored VJState accepted non-text ids and invalid timestamps
- impact: failures could occur later during event ordering instead of at restoration
- fix: validate optional fields without coercion and record the decision in ADR-004
- regression: cover numeric id, boolean checkpoint, and invalid timestamp
