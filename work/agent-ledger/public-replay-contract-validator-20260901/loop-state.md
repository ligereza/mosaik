# Public replay contract validator loop

- Objective: validate public replay reports at runtime with the same redaction and safety invariants described by the public schema.
- Branch: `LUCIDA`
- Starting commit: `ccac739`
- Scope: local structural validator, generator integration, tests, and documentation; no internal replay payload changes.
- Done: `validate_public_report()` now checks allowlists, cross-record links, sequence/timestamp order, nested overlay safety, counts, and proposal-only guarantees; generated reports self-validate.
- Evidence: public replay/host/XIO suite `56 passed`; full suite `139 passed`; host receipt report passed runtime and schema validation; schema graph `21` schemas, `21` registered ids, `19` references; `git diff --check` passed; no active repository test processes.
- Published implementation commits: `432ed50` (`feat: validate public replay reports`) and `bba530a` (`feat: preserve safe host decision status`).
- Next action: publish the ledger closure and perform a final clean-tree and remote check.
