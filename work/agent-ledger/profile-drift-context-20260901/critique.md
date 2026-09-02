# Decision critique

- Problem: a show event without a repeated signal profile caused IMAGO to lose the last soundcheck metrics and drift status.
- Strongest failure mode: the operator enters live show mode with no visible indication that the last soundcheck had a profile mismatch.
- Alternatives considered: persist the full profile in session state, or require every show event to repeat it. Full persistence risks raw-value exposure; repeating it is brittle for live event producers.
- Selected action: persist only the already-projected scalar metrics under an internal context key and mark later use as `inherited`.
- Safety boundary: the context cannot carry profile values or arbitrary keys, is omitted from the public overlay except for approved metrics, and does not create a new measurement or execute a correction.
- Semantic boundary: inherited drift is labeled in the proposal reason and evidence so an old soundcheck observation is not presented as a current show measurement.
