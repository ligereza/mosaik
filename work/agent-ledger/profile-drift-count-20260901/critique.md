# Decision critique

- Problem: `compare_signal_profiles()` can report `changed` when only metadata-like profile decisions differ, while the projected `profile_changed_count` remains zero.
- Strongest failure mode: the operator sees a drift warning that claims zero changed fields and cannot distinguish a real profile decision change from a no-op.
- Alternatives considered: expose changed field paths or raw profile values, or remove the count. Paths and values increase leakage; removing the count weakens the bounded operator signal.
- Selected action: count the union of changed, origin-changed, and confidence-dropped fact paths, then add one bounded unit for each changed recommendation, read-only flag, or stage. Expose only the count and a boolean stage marker.
- Safety boundary: no profile values or paths are added to overlay/proposals; all proposals remain explicit, reversible, and `proposal_only`.
