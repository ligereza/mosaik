# XIO schema resolution loop

- Objective: verify that the published XIO schema graph resolves through a standard JSON Schema registry.
- Branch: `LUCIDA`
- Starting commit: `c103712`
- Scope: schema reference resolution and tests only; no transport, host, GUI, GPU, or automatic actions.
- Observed issue: relative refs under URN `$id` values failed with `jsonschema` before instance validation.
- Method change: normalize the XIO graph and its overlay-update dependency to registered URN IDs.
- Evidence pending: focused tests, registry validation, full suite, commit, push, and process check.
- Next action: run tests and validate a generated XIO result with all referenced schemas registered by `$id`.
