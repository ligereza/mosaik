# NAYADE profile integration loop

- Objective: connect the validated SignalProfile to NAYADE without exposing raw profile values or executing corrections.
- Branch: `LUCIDA`
- Starting commit: `d6a1ad5`
- Scope: safe profile summary, NAYADE capability state, overlay schema, docs, and tests; no hardware or transport.
- Done: valid and invalid profiles can produce bounded NAYADE state; raw profile values remain outside the public overlay.
- Compatibility note: profile imports are deferred inside NAYADE evaluation to avoid a package initialization cycle with signal boundaries.
- Compatibility note: profile-only overlay metrics allow null when the capability has no profile, matching the existing bounded-state projection.
- Evidence: focused NAYADE/profile/schema tests `12 passed`; complete suite `128 passed`; schema registry reports 20 schemas, 20 IDs, and 18 refs; CLI and overlay contract validation pass; `git diff --check` clean.
- Published: commit `d284a00` pushed to `origin/LUCIDA`; process check pending closure.
- Closure: NAYADE now consumes optional SignalProfile input and exposes only bounded, typed metrics in the read-only overlay; malformed profiles are marked invalid without stopping the event.
