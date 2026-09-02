# Decision critique

- Objective: prevent documentation drift after the XIO bridge became implemented.
- Evidence: the code and tests publish `XioEventConsumer`, `XioConsumeResult`, an atomic overlay update, and `validate_xio_consume_result()`, while two main documents still called XIO a future integration.
- Strongest failure mode: a contributor may duplicate the bridge or assume the contract is not available, increasing integration drift.
- Alternatives considered: leave the stale text until a transport exists, or implement transport now. Both have higher future cost or scope than correcting the factual status.
- Selected action: update only the two stale sections and verify claims against current code and tests.
- Decision delta: change documentation, not runtime behavior.
- Forecast: transport and host work remain future and explicitly marked, so this change should not imply real XIO connectivity.
