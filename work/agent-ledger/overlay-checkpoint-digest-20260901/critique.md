# Overlay checkpoint digest critique

- Risk addressed: recovery could restore a modified view alongside an otherwise valid cursor.
- Selected action: reuse the canonical projected-view digest already required by atomic updates.
- Compatibility: empty checkpoints remain valid with a null digest; ready checkpoints gain one required field.
- Reversibility: this is an additive contract hardening step and does not execute external actions.
- Residual limitation: the digest detects alteration but does not authenticate who produced the checkpoint.
