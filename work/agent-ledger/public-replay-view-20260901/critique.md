# Decision critique

- Problem: `SessionReplay.report()` is intentionally complete for deterministic replay and therefore contains original event payloads and signal arguments.
- Strongest failure mode: a colleague receives an internal report and unintentionally receives private profile data, operator metadata, or free-form result notes.
- Alternatives considered: remove payloads from the internal report, or rely on callers to manually redact JSON. Removing payloads breaks replay evidence; caller-side redaction is inconsistent and unauditable.
- Selected action: add a separate `public_report()` with a fixed allowlist and a dedicated schema. The internal report remains unchanged.
- Safety boundary: public records omit raw payloads, arguments, metadata, notes, and free-form evidence; state projections remain read-only and proposal-only.
