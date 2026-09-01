run_id: overlay-consumer-20260901
objective: Build a host-neutral consumer for LUCIDA view, diff, and cursor data.
scope: LUCIDA overlay integration only; preserve the VJ core and existing public APIs.
core_acceptance_criteria:
  - consume view, diff, and cursor incrementally
  - reject stale, skipped, unsafe, or malformed updates
  - remain read-only, deterministic, bounded, auditable, and recoverable
  - keep all code, fields, filenames, schemas, comments, and fixtures English ASCII
  - run the complete suite and push each coherent milestone to origin/LUCIDA
authorized_extensions:
  - additive host-neutral contracts directly required for incremental consumption
status: active

completed:
  - item: Added orchestrator access to bounded overlay diffs.
    evidence: Commit 433c3ab; full suite passed with 85 tests.
  - item: Added machine-readable overlay view and diff schemas.
    evidence: Commit ff90964; full suite passed with 87 tests.
  - item: Added safe overlay revision cursor.
    evidence: Commit 0248e63; full suite passed with 89 tests.
  - item: Implemented host-neutral incremental overlay consumer with explicit recovery checkpoints.
    evidence: Focused overlay suite passed with 18 tests; complete suite passed with 93 tests before commit.

current_state:
  files_or_resources: LUCIDA branch at 0248e635a50c87fbcfba19f11b6064b7b6d5f681 before the consumer commit; consumer files and checkpoint are staged next.
  tests_and_checks: 18 focused overlay tests and 93 complete pytest tests passed; git diff check clean.
  assumptions: A future consumer needs a stateful local buffer and explicit recovery when a delta cannot be applied.
  open_questions: None required for the next additive milestone.
  blockers: None.
  research_refs: None; current implementation is fully local and host-neutral.
  delegation_refs: None.
  last_critique: The strict consumer state machine was selected over more projection fields or host integration because it directly prevents stale and misapplied deltas.
  estimated_remaining_effort: Low; publish this milestone and perform a final scope review.
  next_action: Commit and push the consumer milestone, then verify branch synchronization and decide whether any safe high-value extension remains.
  next_checkpoint_trigger: After consumer tests pass and before commit/push.
