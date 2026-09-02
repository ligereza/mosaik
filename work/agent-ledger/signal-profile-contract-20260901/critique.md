# Decision critique

- Objective: make the existing signal-profile schema usable by LUCIDA without duplicating vendor logic.
- Evidence: `schemas/signal-profile.schema.json` already defined facts, origins, confidence, capture, house, processor, and recommendation, but no Python parser consumed it.
- Strongest failure mode: NAYADE treats inferred or unknown values like confirmed hardware facts and later proposes unsafe corrections.
- Alternatives considered: use JSON Schema directly at runtime, or embed profile fields in generic event payloads. Direct schema validation adds a runtime dependency; generic payloads lose typed boundaries and provenance.
- Selected action: add a dependency-free typed normalizer that preserves origin and confidence and remains read-only.
- Decision delta: profile data becomes a reusable contract; no automatic inference or hardware control is introduced.
- Verification signal: a canonical profile round-trips, detaches nested values, and rejects invalid origins, confidence, capabilities, and recommendations.
