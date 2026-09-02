# Overlay replay validation critique

- Risk addressed: a host could discover an invalid replay only after beginning application.
- Selected action: expose validation-only preflight using the same strict checks as replay, without constructing a transport or executing a record.
- Alternative rejected: duplicate validation in a future host; that would allow contract drift and inconsistent error handling.
- Reversibility: additive public API; existing replay behavior remains available and uses the same envelope checks.
- Residual limitation: validation proves shape, safety, and ordering prerequisites; it does not authenticate the producer.
