run_id: plugin-branches-20260901
objective: Advance the isolated MOSAIK plugin branches INSTAR, NAYADE, and IMAGO.
scope: Branch-specific VJ workflows only; no LUCIDA merge, host connection, sockets, GPU, downloads, private works, or automatic actions.
core_acceptance_criteria:
  - keep plugin responsibilities separate
  - publish tested commits on each branch
  - keep new code, schemas, fixtures, identifiers, and comments English ASCII
  - preserve read-only behavior for processor and show integrations
status: active

completed:
  - item: Audited INSTAR branch.
    evidence: origin/INSTAR at d68eefb; complete suite passed with 31 tests.
  - item: Implemented NAYADE soundcheck planning and passive processor observation.
    evidence: Local focused suite passed with 6 tests and complete branch suite passed with 10 tests.

current_state:
  files_or_resources: NAYADE branch has the new soundcheck module, CLI command, schemas, runbook, tests, and README section; changes are ready for commit.
  tests_and_checks: 6 focused NAYADE tests and 10 total pytest tests passed; git diff check clean.
  assumptions: NAYADE should start from the shared baseline and remain independent from INSTAR implementation details.
  open_questions: IMAGO show scope must remain a proposal-only observer until a concrete host is selected.
  blockers: None.
  research_refs: Existing MOSAIK runbooks and schemas on INSTAR were used as local design evidence.
  delegation_refs: None.
  last_critique: NAYADE was implemented as a focused baseline module instead of porting the larger INSTAR branch, avoiding duplication and branch coupling.
  estimated_remaining_effort: Moderate for IMAGO after publishing NAYADE.
  next_action: Commit and push NAYADE, then implement the first IMAGO show/incident/recovery observer on the IMAGO branch.
  next_checkpoint_trigger: After NAYADE push and before IMAGO implementation.
