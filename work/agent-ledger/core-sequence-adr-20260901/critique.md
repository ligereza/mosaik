# Self-critique

- finding: `VJState.from_dict()` currently coerces `sequence` with `int(...)`
- boundary decision: patch `adapters/vj` only after direct evidence confirmed a contract incompatibility
- rationale: shared-core compatibility is now preserved for valid snapshots and invalid coercions are rejected
- output: ADR-003 records the decision and regression coverage
