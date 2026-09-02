# Decision critique

- Objective: remove the mismatch between the runtime XIO validator and its machine-readable schema.
- Evidence: runtime validation reconstructed nested VJEvent, SignalEnvelope, proposals, results, LucidaState, and overlay update, while the published schema used generic objects for three of them.
- Strongest failure mode: external consumers accept structurally vague or incompatible receipts that the Python validator later rejects.
- Alternatives considered: weaken runtime validation or leave generic schema fields. Both preserve contract drift; adding local refs is reversible and reviewable.
- Selected action: add small local schemas for SignalEnvelope and SessionReplayRecord and reference existing VJ contracts.
- Decision delta: schema precision increases; runtime behavior is unchanged.
- Verification signal: every local ref resolves and the complete test suite stays green.
