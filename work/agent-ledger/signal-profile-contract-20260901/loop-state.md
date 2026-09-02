# Signal profile contract loop

- Objective: provide a typed, read-only runtime representation of the shared signal profile for NAYADE and the other stages.
- Branch: `LUCIDA`
- Starting commit: `9df778d`
- Scope: VJ signal contract, exports, docs, and tests; no hardware, transport, inference engine, or automatic action.
- Done: SignalFact, SignalEvidence, SignalProfile, canonical validation, and detached JSON output added.
- Evidence: SignalProfile suite `8 passed`; complete suite `126 passed`; normalized profile validates against `schemas/signal-profile.schema.json`; `git diff --check` clean.
- Published: commit `30a5e4e` pushed to `origin/LUCIDA`; process check pending closure.
- Closure: NAYADE now has a typed, detached, read-only signal profile that preserves origin, confidence, source, and evidence.
