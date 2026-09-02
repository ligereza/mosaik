# Profile drift count loop

- Objective: ensure a changed profile always reports a non-zero bounded change count, including recommendation, read-only, stage, origin, and confidence changes.
- Branch: `LUCIDA`
- Starting commit: `dbe7cbe`
- Scope: safe overlay metrics, proposal explanation, schema, tests, and documentation; no raw values or external actions.
- Done: pending.
- Evidence pending: focused tests, full suite, schema validation, commit, push, and process check.
- Next action: run focused and full verification, then publish if the count remains redacted and deterministic.
