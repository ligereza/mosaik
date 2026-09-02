# Decision critique

- Objective: replace a manual schema validation command with a repeatable repository tool.
- Evidence: manual `jsonschema` validation succeeded only after constructing an in-memory URN registry; no repository command preserved that setup.
- Strongest failure mode: a contributor changes a contract reference and discovers the break only in an external host.
- Alternatives considered: keep the one-off command or add a runtime dependency. The selected tool keeps validation development-only and leaves the adapter runtime dependency-free.
- Selected action: add a CLI using `jsonschema` and `referencing`, plus tests for all refs and a generated XIO result.
- Decision delta: operational verification becomes reproducible without network access.
- Verification signal: CLI reports the local registry and validates a generated XIO result with exit code zero.
