# Self-critique

- finding: VJProposal.from_dict() silently discarded unknown fields and
  defaulted schema-required fields
- decision: enforce required and allowed fields at the adapter boundary while
  preserving optional evidence and the existing safety invariants
- compatibility: proposals produced by to_dict() remain unchanged; malformed
  snapshots now fail early and visibly
- safety: no execution behavior was introduced; proposal_only remains required
- validation: focused adapter/LUCIDA suites, full suite, schema graph, and diff
  check all pass
