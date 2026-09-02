objective: Progress the remaining plugin branches without mixing their responsibilities.
snapshot: INSTAR is already functional; NAYADE and IMAGO point to the baseline.
alternatives:
  - path: Merge the full INSTAR branch into every plugin branch.
    risk: Duplicates unrelated capabilities and obscures ownership.
  - path: Build focused branch-specific contracts from the baseline.
    benefit: Keeps NAYADE and IMAGO independently reviewable and preserves future reuse.
selected_action: build focused branch-specific contracts.
decision_delta: NAYADE receives only soundcheck and passive processor work in this milestone.
verification_signal: Branch-local pytest suite, full suite, clean diff, and pushed commit.
