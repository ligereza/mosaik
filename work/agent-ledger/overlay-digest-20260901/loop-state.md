# Overlay digest loop

- Objective: bind the atomic overlay target view to a deterministic content digest.
- Branch: `LUCIDA`
- Starting commit: `c26d6f3`
- Scope: local JSON integrity only; no transport, host, GUI, GPU, or automatic actions.
- Milestone 1: SHA-256 digest added to `LucidaOverlayUpdate`, validator, schema, fixture, and tests.
- Evidence: focused LUCIDA suite `27 passed`.
- Next: run the complete suite, review diff, commit, push, and verify the remote tip.
