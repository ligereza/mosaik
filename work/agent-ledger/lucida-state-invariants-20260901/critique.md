# Self-critique

- finding: top-level pending ids were ignored and pending ids could lack global proposals
- decision: validate duplicate projections and proposal references at LucidaState.from_dict()
- compatibility: generated LucidaState.to_dict() roundtrips unchanged
- validation needed: tampered projections, missing proposal records, full suite, and schema graph
