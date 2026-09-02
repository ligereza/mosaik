# NAYADE profile integration loop

- Objective: connect the validated SignalProfile to NAYADE without exposing raw profile values or executing corrections.
- Branch: `LUCIDA`
- Starting commit: `d6a1ad5`
- Scope: safe profile summary, NAYADE capability state, overlay schema, docs, and tests; no hardware or transport.
- Done: valid and invalid profiles can produce bounded NAYADE state; raw profile values remain outside the public overlay.
- Compatibility note: profile imports are deferred inside NAYADE evaluation to avoid a package initialization cycle with signal boundaries.
- Compatibility note: profile-only overlay metrics allow null when the capability has no profile, matching the existing bounded-state projection.
- Evidence pending: focused tests, full suite, schema validation, commit, push, and process check.
- Next action: verify overlay contract compatibility and publish if all checks pass.
