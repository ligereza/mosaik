# Self-critique

- finding: a set inside capability state was accepted and later broke json.dumps
- decision: validate JSON serializability at the LUCIDA contract boundary
- scope: preserve private values but reject non-transportable Python objects and NaN
- validation needed: set, NaN, valid private state, full suite, and schema graph
