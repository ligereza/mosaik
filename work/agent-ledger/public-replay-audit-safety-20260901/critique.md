# Decision critique

- Problem: public audit projection accepted arbitrary text in the `mode` field even though the public contract promises a proposal-only replay.
- Strongest failure mode: a host receipt can place private or misleading free-form text in a field intended to describe execution mode.
- Alternatives considered: expose all host receipt fields, or omit the whole audit section. Keeping a small allowlist preserves provenance without carrying notes or arbitrary mode labels.
- Selected action: include `mode` only when it equals `proposal_only`; omit non-canonical values from the public projection.
- Safety boundary: internal audit logs are unchanged, while public safety remains explicitly replay-only and proposal-only.
