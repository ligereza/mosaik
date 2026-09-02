# Decision critique

- Objective: close the runtime validation gap left by the published XIO result schema.
- Evidence: `xio-consume-result.schema.json` existed, but no Python boundary validated a serialized result before acceptance.
- Strongest failure mode: a result can retain individually plausible event, replay, and overlay objects while their session or sequence identities diverge.
- Alternatives considered: external JSON Schema validation would add a dependency and would not enforce cross-object identity; transport work would expand scope without solving receipt integrity.
- Selected action: continue with a dependency-free runtime validator and focused tampering tests.
- Decision delta: none; direct continuation has the lowest review and integration cost.
- Verification signal: generated `XioConsumeResult.to_dict()` must round-trip, while altered cursor, digest, or identity must fail.
