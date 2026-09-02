# Atomic replay critique

- Risk addressed: a valid-looking update could be parsed without checking that its target view, change list, and revision cursor belong together.
- Design decision: replay validates the full update envelope, then lets `OverlayConsumer.apply_update` reconstruct the target before state mutation.
- Alteration coverage: private payload injection, changed `after` value, and skipped cursor sequence are rejected offline.
- Compatibility: existing snapshot/delta records remain supported; atomic records are counted separately while applied deltas retain their existing metric.
- Residual limitation: replay proves the data path only; it does not infer operator intent or connect to a live host.
