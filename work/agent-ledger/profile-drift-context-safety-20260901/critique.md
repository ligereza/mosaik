# Decision critique

- Problem: a restored state can contain arbitrary metadata under the reserved profile-context key.
- Strongest failure mode: malformed values could appear in internal state or be promoted to the read-only overlay on a later event.
- Alternatives considered: trust the reserved key because LUCIDA created it, or reject the whole session state. Trust is unsafe across persistence boundaries; rejecting the whole session harms recovery.
- Selected action: accept only known scalar fields with bounded types and enums, then remove invalid context while preserving the rest of the session.
- Completeness rule: a context marked `valid` must also contain the complete base summary; dropping one malformed field invalidates the whole persisted context.
- Safety boundary: invalid context is ignored and cannot trigger a proposal, correction, or external action.
