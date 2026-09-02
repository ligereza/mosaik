# Schema validator tool loop

- Objective: make local JSON Schema registry and instance validation reproducible.
- Branch: `LUCIDA`
- Starting commit: `da2e256`
- Scope: development tool, development dependencies, docs, and tests; no runtime adapter or external show control.
- Done: registry loader, URN reference check, optional instance validation, and generated XIO CLI coverage added.
- Evidence pending: tool tests, full suite, CLI execution, commit, push, and process check.
- Next action: run the tool and tests, then publish only if the local registry and generated result validate.
