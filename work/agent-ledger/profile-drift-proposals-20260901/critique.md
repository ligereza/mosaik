# Decision critique

- Problem: the overlay reported profile drift, but the pending proposal retained a generic reason and could not explain why operator attention was needed.
- Strongest failure mode: a changed range, refresh, or processor assumption is treated as an ordinary review, reducing the chance that the operator checks the soundcheck baseline before show.
- Alternatives considered: expose changed field names or raw profile values, or create a separate proposal type. Both add leakage or contract duplication.
- Selected action: reuse the existing bounded profile comparison and add only a count/status marker to the proposal reason and evidence.
- Safety boundary: the proposal remains explicit, reversible, `proposal_only`, and contains no raw values or hardware instructions.
