# Signal profile contract loop

- Objective: provide a typed, read-only runtime representation of the shared signal profile for NAYADE and the other stages.
- Branch: `LUCIDA`
- Starting commit: `9df778d`
- Scope: VJ signal contract, exports, docs, and tests; no hardware, transport, inference engine, or automatic action.
- Done: SignalFact, SignalEvidence, SignalProfile, canonical validation, and detached JSON output added.
- Evidence pending: tests, schema compatibility, full suite, commit, push, and process check.
- Next action: validate the profile against the existing JSON schema and run the complete suite.
