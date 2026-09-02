# Atomic overlay replay loop

- Objective: consume atomic LUCIDA overlay updates through the offline replay path.
- Branch: `LUCIDA`
- Starting commit: `49c982a`
- Scope: snapshots, explicit deltas, atomic updates, cursors, recovery, and safe rejection; no host, transport, GUI, GPU, or automatic actions.
- Milestone 1: replay accepts strict `update` records and reports update counts.
- Evidence: focused overlay suite `27 passed`.
- Evidence: focused overlay suite `27 passed`; complete suite `102 passed`; all overlay JSON contracts parse; `git diff --check` clean; new code, fixture, schema, and ledger content pass the ASCII check. Existing README Unicode is unchanged except for ASCII additions.
- Next: commit and push to `origin/LUCIDA`, then verify the remote tip.
