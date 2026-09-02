# Decision critique

- Objective: make SignalProfile useful to NAYADE while preserving the read-only safety boundary.
- Evidence: SignalProfile was validated but not consumed by any capability; the overlay already allowed bounded capability state fields.
- Strongest failure mode: exposing raw processor, path, or signal values in the shared overlay, or treating inferred data as an automatic correction.
- Alternatives considered: keep the parser disconnected, expose the entire profile, or expose only aggregate metrics. Aggregate metrics preserve utility and privacy with the lowest integration risk.
- Selected action: add a bounded summary and show only status, stage, counts, confidence minimum, and processor read-only state.
- Decision delta: NAYADE now consumes the profile; no proposal semantics or external action changed.
- Verification signal: a valid profile appears as safe metrics, raw resolution is absent, and malformed profiles become `profile_status=invalid`.
