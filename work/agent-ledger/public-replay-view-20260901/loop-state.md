# Public replay view loop

- Objective: provide a shareable replay projection without exposing event payloads, signal arguments, metadata, notes, or raw profile values.
- Branch: `LUCIDA`
- Starting commit: `4835090`
- Scope: `SessionReplay.public_report()`, allowlisted record fields, public replay schema, tests, and documentation; internal replay semantics remain unchanged.
- Done: pending.
- Evidence pending: focused tests, full suite, schema validation, commit, push, and process check.
- Next action: run focused and full verification, then publish if the public report contains no raw fields.
