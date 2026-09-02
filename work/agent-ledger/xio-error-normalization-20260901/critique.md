# Self-critique

- defect: `_safe_xio_details` accepted `bool` as an integer before an error result was built
- impact: malformed XIO input could raise during HostResult construction instead of returning a rejected result
- fix: mirror the strict boolean exclusion already used by the generic signal path
- regression: assert rejected status, null sequence, unchanged report, and no replay records
