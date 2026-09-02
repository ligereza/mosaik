# XIO overlay reader critique

- Risk addressed: an XIO consumer had to inspect replay internals to obtain a LUCIDA view, encouraging raw payload or provenance leakage.
- Selected action: project the existing replay state through the established bounded view and cursor builders.
- Alternative rejected: duplicate a new XIO-specific overlay schema; that would fragment the single LUCIDA surface.
- Reversibility: additive methods only; XIO event conversion, SessionReplay, and audit provenance remain unchanged.
- Verification signal: deterministic view/cursor output and explicit private payload redaction test.
