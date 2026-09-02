# Decision critique

- Objective: make XIO schemas consumable by a real JSON Schema validator, not merely parseable as JSON.
- Evidence: direct validation failed while resolving `application-event.schema.json`; the failure is caused by URN `$id` scopes and relative refs.
- Strongest failure mode: an external host rejects or cannot load a valid XIO result before inspecting its data.
- Alternatives considered: add a custom file resolver, or normalize refs to registered IDs. A custom resolver hides the portability issue; URN IDs align with the existing schema identity model and are less path-dependent.
- Selected action: use URN refs for the XIO dependency graph and test registry-backed validation.
- Decision delta: the published contract becomes registry-oriented; runtime code remains unchanged.
- Verification signal: a generated result validates with `Draft202012Validator` and a registry containing every referenced schema ID.
