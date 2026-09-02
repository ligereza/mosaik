# Overlay replay recorder critique

- Objective: reduce hand-authored replay JSON while preserving the existing strict consumer boundary.
- Strongest failure mode: a recorder could append a malformed or skipped revision and make later replay failure harder to localize.
- Selected action: reuse `build_overlay_update` and `OverlayConsumer` before appending each record; failed records leave the recorder unchanged.
- Alternatives: a live host adapter has higher permission and coupling cost; another schema has lower behavioral value; focused research is not needed because the local contracts define the boundary.
- Reversibility: the recorder is additive and produces the existing replay envelope; it can be removed without changing core VJ behavior.
- Residual limitation: it records projected states only and does not authenticate external inputs.
