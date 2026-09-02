# Autonomous loop state

- objective: keep injected VJ signal state strict and recoverable
- hito: reject ambiguous `received_count` values when restoring OSC boundary state
- status: focused regression passed; full verification pending
- branch: LUCIDA
- safety: validation-only; no transport or external mutation
- next: run full suite and schema checks, then publish
