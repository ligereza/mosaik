# Self-critique

- finding: `VJState.from_dict()` currently coerces `sequence` with `int(...)`
- boundary decision: do not patch `adapters/vj` from this integration branch
- rationale: shared-core compatibility needs an explicit decision and regression coverage
- output: ADR-003 records the exact proposed validation and required tests
