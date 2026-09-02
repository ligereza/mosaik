objective: Provide a safe incremental consumer for LUCIDA overlay data.
acceptance: A future host can apply full views and safe deltas in order, detect stale or skipped revisions, and recover without side effects.
snapshot: Existing view, diff, and cursor are deterministic and published at 0248e63; no consumer state exists yet.
strongest_failure_mode: A host applies a delta against the wrong base or accepts a stale update, showing a state that never existed.
alternatives:
  - path: Add more fields to the view.
    cost: Low immediate effort, but it does not enforce update ordering or recovery.
    risk: More surface area without solving incremental correctness.
  - path: Add a stateful host-neutral consumer.
    cost: Moderate implementation and tests.
    benefit: Centralizes cursor ordering, safe projection validation, bounded delta application, and recoverable resync.
  - path: Connect a specific host now.
    cost: High integration and review cost.
    risk: Violates current boundary and couples the contract prematurely.
selected_action: continue with the stateful host-neutral consumer.
decision_delta: This is an additive contract layer; existing view and diff APIs remain unchanged.
verification_signal: Focused consumer tests plus the complete pytest suite and clean git diff.
reversal_condition: If the consumer requires changes to VJ core or cannot reject stale/skipped updates without ambiguity, stop and narrow the contract.
