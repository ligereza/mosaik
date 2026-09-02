# Self-critique

- defect: `OscBridgeState.from_dict()` coerced booleans and strings with `int()`
- impact: a restored snapshot could claim a count that was not represented by the contract type
- fix: require a non-negative integer and preserve the value without coercion
- regression: cover boolean, negative, and string values while leaving valid snapshots unchanged
- follow-up: require `seen_sequences` to be strictly increasing and synchronized with `last_sequence`
