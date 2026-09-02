# Profile drift loop

- Objective: compare a signal baseline with a later observation for soundcheck/show continuity.
- Branch: `LUCIDA`
- Starting commit: `95abf72`
- Scope: read-only profile comparison, NAYADE safe metrics, overlay schema, docs, and tests; no hardware or automatic corrections.
- Done: comparison reports changed fields, origin changes, confidence drops, unknown delta, recommendation drift, and read-only drift without raw values.
- Evidence pending: tests, schema validation, full suite, commit, push, and process check.
- Next action: verify stable and changed profiles through the public overlay contract.
