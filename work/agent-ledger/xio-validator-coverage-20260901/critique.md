# Decision critique

- Objective: ensure the XIO validator's most important cross-contract checks remain exercised.
- Evidence: roundtrip, cursor sequence, and digest tampering were covered; signal identity and provenance were not.
- Strongest failure mode: a future refactor could weaken event pairing or provenance checks while the existing tests still pass.
- Alternatives considered: add broad property testing or stop with current coverage. Broad testing is disproportionate for this dependency-free contract; stopping leaves two high-value checks unguarded.
- Selected action: add two deterministic negative tests and run the full suite.
- Decision delta: none; this is a bounded verification extension.
- Verification signal: both altered receipts must raise `XioSchemaError` before acceptance.
