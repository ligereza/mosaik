# Overlay checkpoint digest loop

- Objective: bind recoverable LUCIDA consumer checkpoints to their projected view content.
- Branch: `LUCIDA`
- Starting commit: `35799e5`
- Scope: offline checkpoint creation and restoration; no host, transport, GUI, GPU, or automatic actions.
- Milestone: ready checkpoints carry a deterministic SHA-256 view digest; altered checkpoints are rejected before mutation.
- Evidence: focused LUCIDA suite `30 passed`.
- Next: run the complete suite, review diff, commit, push, and verify the remote tip.
