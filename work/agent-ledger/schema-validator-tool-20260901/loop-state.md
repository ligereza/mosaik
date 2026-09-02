# Schema validator tool loop

- Objective: make local JSON Schema registry and instance validation reproducible.
- Branch: `LUCIDA`
- Starting commit: `da2e256`
- Scope: development tool, development dependencies, docs, and tests; no runtime adapter or external show control.
- Done: registry loader, URN reference check, optional instance validation, and generated XIO CLI coverage added.
- Evidence: CLI reports `schemas: 20`, `registered_ids: 20`, `references: 18`; tool tests `2 passed`; complete suite `118 passed`; `git diff --check` clean.
- Published: commit `96ca7cb` pushed to `origin/LUCIDA`; process check pending closure.
- Closure: schema graph and instance validation are now reproducible locally through `tools/validate_schema_graph.py` without network access.
