# Public replay audit safety loop

- Objective: prevent free-form host audit mode text from entering the shareable replay report.
- Branch: `LUCIDA`
- Starting commit: `a5fdc36`
- Scope: public audit allowlist, tests, and documentation; internal receipts and replay behavior remain unchanged.
- Done: public audit projection now retains `mode` only when it is the canonical `proposal_only` value.
- Evidence: replay/host-result suite `36 passed`; full suite `137 passed`; schema graph `21` schemas, `21` registered ids, `19` references; `git diff --check` passed; no active repository test processes.
- Published implementation commit: `3d4e5c7` (`fix: restrict public replay audit mode`).
- Next action: publish the ledger closure and perform a final clean-tree and remote check.
