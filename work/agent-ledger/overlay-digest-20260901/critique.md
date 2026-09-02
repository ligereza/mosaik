# Overlay digest critique

- Risk addressed: a consumer could receive a structurally valid view that was not the view associated with the update revision.
- Design decision: hash the canonical bounded view with SHA-256 and require a lowercase 64-character digest in the atomic envelope.
- Privacy check: the digest is computed only after the existing redaction projection; private payloads and metadata are not introduced.
- Recovery check: digest validation happens before `OverlayConsumer` mutates its checkpoint.
- Residual limitation: this detects accidental or untrusted alteration; it is not an authenticity signature and does not replace operator approval.
