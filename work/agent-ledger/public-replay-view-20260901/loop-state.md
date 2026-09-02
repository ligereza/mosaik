# Public replay view loop

- Objective: provide a shareable replay projection without exposing event payloads, signal arguments, metadata, notes, or raw profile values.
- Branch: `LUCIDA`
- Starting commit: `4835090`
- Scope: `SessionReplay.public_report()`, allowlisted record fields, public replay schema, tests, and documentation; internal replay semantics remain unchanged.
- Done: `SessionReplay.public_report()` now exposes an allowlisted shareable view while preserving the complete internal replay.
- Evidence: replay/privacy suite `55 passed`; full suite `136 passed`; public fixture validation `valid` with 6 records; schema graph `21` schemas, `21` registered ids, `19` references; `git diff --check` passed; no active repository test processes.
- Published implementation commit: `07757f6` (`feat: add redacted public replay report`).
- Next action: integrate the public fixture wrapper, re-run verification, and publish the closure.
