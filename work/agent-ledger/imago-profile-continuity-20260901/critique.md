# Decision critique

- Objective: prevent soundcheck profile warnings from disappearing at the IMAGO boundary.
- Evidence: NAYADE projected profile drift, while IMAGO only projected mode and incident category.
- Strongest failure mode: a show event with a changed signal profile appears normal because the comparison state was dropped at stage transition.
- Alternatives considered: duplicate comparison logic in IMAGO or add a separate handoff object. A shared helper preserves one implementation and avoids the handoff abstraction the workflow does not need.
- Selected action: reuse the existing bounded profile state helper in NAYADE and IMAGO.
- Decision delta: stage continuity is improved without changing proposal-only behavior or exposing raw profile values.
- Verification signal: an IMAGO event with changed profile values reports `profile_comparison_status=changed` and does not contain the changed raw value.
