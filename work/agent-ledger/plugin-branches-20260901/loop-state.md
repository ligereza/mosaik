run_id: plugin-branches-20260901
objective: Advance the isolated MOSAIK plugin branches INSTAR, NAYADE, and IMAGO.
scope: Branch-specific VJ workflows only; no LUCIDA merge, host connection, sockets, GPU, downloads, private works, or automatic actions.
core_acceptance_criteria:
  - keep plugin responsibilities separate
  - publish tested commits on each branch
  - keep new code, schemas, fixtures, identifiers, and comments English ASCII
  - keep processor and show integrations read-only
status: complete

completed:
  - item: Audited INSTAR branch.
    evidence: origin/INSTAR at d68eefb; complete suite passed with 31 tests.
  - item: Implemented NAYADE soundcheck planning and passive processor observation.
    evidence: origin/NAYADE at f77ea24; focused suite passed with 6 tests and branch suite passed with 10 tests.
  - item: Implemented IMAGO show observation, incidents, recovery, closure, and proposal results.
    evidence: Local focused suite passed with 4 tests and branch suite passed with 8 tests; CLI help loaded successfully.
  - item: Verified all three plugin branches after publication.
    evidence: INSTAR 31 passed at d68eefb; NAYADE 10 passed at f77ea24; IMAGO 8 passed at 6d13dc6; each branch matches origin.

current_state:
  files_or_resources: INSTAR, NAYADE, and IMAGO are independently published and synchronized; current branch is IMAGO.
  tests_and_checks: INSTAR 31 passed; NAYADE 10 passed; IMAGO 8 passed; all working trees clean; CLI help loaded; git diff checks clean.
  assumptions: IMAGO observes event evidence and emits proposals; it never invokes Resolume, DMX, or processor commands.
  open_questions: A future host adapter must define permissions and transport separately.
  blockers: None.
  research_refs: Existing MOSAIK architecture and ADR-002 define the proposal-only boundary.
  delegation_refs: None.
  last_critique: IMAGO was kept as a focused live observer rather than porting all INSTAR/NAYADE implementation details.
  estimated_remaining_effort: Low for this branch milestone; final cross-branch verification remains.
  next_action: No further branch-specific work is selected until a concrete feature or host integration is defined.
  next_checkpoint_trigger: After IMAGO push and cross-branch verification.
