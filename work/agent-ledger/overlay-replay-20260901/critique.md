objective: Demonstrate deterministic replay of LUCIDA overlay JSON.
acceptance: Replaying the same snapshot/delta/cursor stream twice yields identical safe reports and no external action.
snapshot: OverlayConsumer applies in-memory mappings but there is no JSON envelope or report path.
strongest_failure_mode: A future host parses records differently, silently ignores a malformed delta, or produces a report containing private input fields.
alternatives:
  - path: Add a live host adapter.
    cost: High and out of current boundary.
    risk: Couples transport and permissions before the contract is proven.
  - path: Add a JSON replay envelope over the existing consumer.
    cost: Moderate, local, and directly testable.
    benefit: Proves parsing, ordering, deterministic audit output, and privacy before host integration.
  - path: Add only more schemas.
    cost: Low, but does not execute the complete data path.
    risk: Contract may look stable without behavior being verified.
selected_action: continue with the pure JSON replay path.
decision_delta: Add a replay boundary while preserving all existing view, diff, cursor, and consumer APIs.
verification_signal: Repeated fixture replay equality, focused negative cases, full pytest suite, and clean diff.
reversal_condition: If replay requires network, subprocesses, host state, or a core VJ change, narrow it back to an in-memory record runner.
