# Decision critique

- Problem: the public report had a schema, but a consumer had no runtime-only validator and the generator did not self-check its output.
- Strongest failure mode: a manually altered or incorrectly assembled public report can carry a payload or unsafe safety flag while appearing structurally plausible.
- Alternatives considered: load JSON Schema on every runtime call, or trust the generator. Runtime schema loading adds filesystem/dependency coupling; trust leaves external consumer inputs unchecked.
- Selected action: provide a dependency-free structural validator that checks exact allowlists, counts, redaction fields, proposal safety, and nested overlay views.
- Safety boundary: validation rejects unsafe reports before consumers use them; it never executes, repairs, or sends an external action.
- Host-result boundary: public receipts retain only the enumerated decision status and `execution_asserted=false`; free-form reason and provenance remain omitted.
