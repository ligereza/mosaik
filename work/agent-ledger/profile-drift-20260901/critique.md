# Decision critique

- Objective: make a soundcheck profile useful for detecting changes before or during a show.
- Evidence: SignalProfile was already consumed by NAYADE, but no baseline-versus-observation comparison existed.
- Strongest failure mode: a changed range, refresh, processor identity, or confidence level is treated as unchanged because both profiles are individually valid.
- Alternatives considered: compare and expose raw values, or keep comparison out of the adapter. Raw values would weaken the overlay boundary; no comparison would leave drift invisible.
- Selected action: compare normalized facts and expose only bounded metrics and field paths.
- Decision delta: NAYADE can flag drift without suggesting a hardware write or returning signal values.
- Verification signal: changed values and confidence drops are detected, stable profiles remain stable, and raw values do not appear in comparison output.
