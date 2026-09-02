# Overlay replay validation loop

- Objective: preflight LUCIDA replay envelopes before applying records.
- Branch: `LUCIDA`
- Starting commit: `209b71f`
- Scope: offline structural and contract validation for snapshots, deltas, atomic updates, cursors, and recovery; no host, transport, GUI, GPU, or automatic actions.
- Milestone: public `validate_overlay_replay` added and snapshot/session checks strengthened.
- Evidence: focused overlay suite `31 passed`.
- Evidence: focused overlay suite `31 passed`; complete suite `107 passed`; `git diff --check` clean; overlay contracts parse; new code and ledger content pass ASCII.
- Next: commit and push to `origin/LUCIDA`, then verify the remote tip.
