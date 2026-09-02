# Self-critique

- finding: the future reducer needs show metadata without receiving raw OSC or
  Resolume payloads
- decision: project canonical VJEvent data into eight bounded fields and keep
  transport labels declarative; use the existing OSC normalizer as the source
  boundary
- stale policy: reject non-increasing sequence or source timestamp; reject
  malformed previous projections before comparison
- provenance policy: preserve only a fixed set of ASCII metadata fields and
  reject source or transport conflicts
- limitation: Art-Net, sACN, and timecode are not parsed or transported here;
  no generic LUCIDA reducer is implemented
- validation: focused tests, complete MOSAIK/LUCIDA suite, schema graph, ASCII
  guard, compile check, and process scan all pass
