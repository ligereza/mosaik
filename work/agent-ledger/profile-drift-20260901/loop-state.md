# Profile drift loop

- Objective: compare a signal baseline with a later observation for soundcheck/show continuity.
- Branch: `LUCIDA`
- Starting commit: `95abf72`
- Scope: read-only profile comparison, NAYADE safe metrics, overlay schema, docs, and tests; no hardware or automatic corrections.
- Done: comparison reports changed fields, origin changes, confidence drops, unknown delta, recommendation drift, and read-only drift without raw values.
- Evidence: focused profile/overlay suite `49 passed`; complete suite `130 passed`; schema CLI reports 20 schemas, 20 IDs, and 18 refs; `git diff --check` clean.
- Published: commit `f631268` pushed to `origin/LUCIDA`; process check pending closure.
- Closure: NAYADE now reports profile drift metrics without exposing raw signal values or executing corrections.
