# Profile drift context loop

- Objective: carry only bounded soundcheck profile metrics into later show events when no new profile is supplied.
- Branch: `LUCIDA`
- Starting commit: `54ce042`
- Scope: session state context, IMAGO projection, redaction, schemas, tests, and documentation; no raw values or external actions.
- Done: the session carries only bounded profile metrics into later events; IMAGO marks inherited context and proposals distinguish it from a new measurement.
- Evidence: focused suite `52 passed`; full suite `133 passed`; schema graph `20` schemas, `20` registered ids, `18` references; `git diff --check` passed; no active repository test processes.
- Published implementation commit: `9ae9bce` (`feat: carry bounded soundcheck context`).
- Next action: publish the ledger closure and perform a final clean-tree and remote check.
