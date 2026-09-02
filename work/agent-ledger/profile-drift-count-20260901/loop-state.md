# Profile drift count loop

- Objective: ensure a changed profile always reports a non-zero bounded change count, including recommendation, read-only, stage, origin, and confidence changes.
- Branch: `LUCIDA`
- Starting commit: `dbe7cbe`
- Scope: safe overlay metrics, proposal explanation, schema, tests, and documentation; no raw values or external actions.
- Done: the bounded count now includes changed fact paths plus recommendation, read-only, and stage changes; `profile_stage_changed` is exposed safely.
- Evidence: focused suite `51 passed`; full suite `132 passed`; schema graph `20` schemas, `20` registered ids, `18` references; `git diff --check` passed; no active repository test processes.
- Published implementation commit: `8b1775c` (`fix: count all profile drift changes`).
- Next action: publish the ledger closure and perform a final clean-tree and remote check.
