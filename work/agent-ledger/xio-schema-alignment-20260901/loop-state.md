# XIO schema alignment loop

- Objective: make the published XIO result schema describe the nested contracts validated at runtime.
- Branch: `LUCIDA`
- Starting commit: `10810c3`
- Scope: JSON schemas and schema-reference tests only; no transport, host, GUI, GPU, or automatic actions.
- Done: result schema now references VJEvent, SignalEnvelope, SessionReplayRecord, and overlay update contracts.
- Evidence pending: schema parse, reference checks, full tests, diff check, commit, push, and process check.
- Next action: verify every local reference resolves and the generated result remains compatible.
