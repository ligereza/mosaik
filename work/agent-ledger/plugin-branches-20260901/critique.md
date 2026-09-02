objective: Progress the remaining plugin branches without mixing their responsibilities.
snapshot: INSTAR and NAYADE are published; IMAGO now has a focused proposal-only observer.
alternatives:
  - path: Merge LUCIDA or the full INSTAR branch into IMAGO.
    risk: Couples the host-neutral layer and unrelated preflight logic to the live observer.
  - path: Keep IMAGO focused on event state, proposals, checkpoints, and results.
    benefit: Preserves a clear future boundary for a host adapter.
selected_action: publish the focused IMAGO branch.
decision_delta: No host integration is needed to validate the show lifecycle contract.
verification_signal: Focused and complete pytest suites, CLI help, clean diff, and pushed branch.
