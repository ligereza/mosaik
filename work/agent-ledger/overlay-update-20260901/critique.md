# Overlay update critique

- Risk addressed: a future host could receive a valid delta and cursor but pair them with the wrong projected view.
- Design decision: include the complete target view and reject a truncated change list; the consumer reconstructs the candidate before mutating state.
- Privacy check: the envelope uses the existing bounded projection and cursor only; raw payloads, metadata, paths, credentials, and host details remain excluded.
- Safety check: the envelope is read-only and proposal-only; it cannot execute or authorize a show action.
- Residual limitation: the envelope remains a data contract. A host still needs explicit operator policy for transport, persistence, and presentation.
