# Overlay update loop

- Objective: bind LUCIDA overlay view, diff, and revision cursor in one atomic envelope.
- Branch: `LUCIDA`
- Starting commit: `de2d827`
- Scope: host-neutral read-only consumption; no GUI, sockets, GPU, Resolume, or automatic actions.
- Milestone 1: atomic builder, validator, consumer application, schema, and tests implemented.
- Evidence: focused LUCIDA suite `25 passed`; complete suite `100 passed`; `git diff --check` clean; technical additions pass the ASCII check.
- Next: commit and push to `origin/LUCIDA`, then verify the remote tip.
- Recovery: failed validation must leave the consumer checkpoint unchanged.
