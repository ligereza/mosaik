# Self-critique

- finding: callers had to compose OscResolumeBoundary.normalize() manually
  before using the host-neutral projection
- decision: add an explicit project_osc() convenience path that delegates to
  the existing normalizer and keeps all output fields and stale checks unchanged
- alternatives: adding a socket listener or a universal transport parser would
  expand scope and introduce side effects without improving this contract
- limitation: Art-Net, sACN, and timecode remain declarative transport labels;
  no protocol implementation or generic LUCIDA reducer is added
- validation: focused tests, complete suite, schema graph, ASCII guard, diff
  check, and process scan pass
