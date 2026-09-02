# IMAGO profile continuity loop

- Objective: preserve NAYADE profile drift awareness when the session enters IMAGO show events.
- Branch: `LUCIDA`
- Starting commit: `5becb54`
- Scope: shared profile-state helper, IMAGO integration, overlay contract, docs, and tests; no hardware or automatic corrections.
- Done: NAYADE and IMAGO reuse one bounded profile projection; show events can report profile drift without raw values.
- Evidence: focused suite `50 passed`; full suite `131 passed`; schema graph `20` schemas, `20` registered ids, `18` references; `git diff --check` passed; no active repository test processes.
- Next action: commit and push the verified change, then perform a final clean-tree and remote check.
