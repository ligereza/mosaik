# XIO atomic update critique

- Risk addressed: an incremental XIO consumer could read the current safe view but lose the exact event-to-revision transition.
- Selected action: build the existing atomic envelope from the replay state immediately before and after each accepted event.
- Privacy check: the envelope uses the existing redacted projection and digest; raw XIO payload and provenance remain only in the internal audit record.
- Compatibility: event conversion and SessionReplay behavior are unchanged; the result gains an additive safe field.
- Residual limitation: a host still decides how to transport, display, persist, or approve the update.
