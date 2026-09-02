# Self-critique

- finding: `unknown` could carry a concrete value and positive confidence,
  contradicting its documented meaning as unavailable data
- decision: require `value: "unknown"` and `confidence: 0` in Python and JSON
  Schema; leave `inferred.source` optional because no evidence justified a new
  mandatory field
- compatibility: existing canonical fixtures remain valid; one drift fixture
  was corrected to represent the complete transition to unknown
- safety: no raw values are exposed by comparison or overlays; no automatic
  correction or hardware write was added
- validation: focused profile suite, full suite, schema graph, and diff check
  all pass
