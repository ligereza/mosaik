# Self-critique

- finding: the adapters exposed internal reports while SessionReplay already had the authoritative public projection
- decision: delegate to SessionReplay.public_report() instead of duplicating redaction or adding adapter-specific fields
- risk checked: the public contract rejects extra top-level fields, so XIO metadata such as replay_type/source_app must remain internal
- validation needed: prove both adapter surfaces omit payloads, signal arguments, and provenance while remaining schema-valid
