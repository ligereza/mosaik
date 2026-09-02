# XIO overlay reader loop

- Objective: expose the bounded LUCIDA overlay and revision cursor directly from the XIO consumer.
- Branch: `LUCIDA`
- Starting commit: `fd3fe18`
- Scope: canonical XIO events to safe LUCIDA projection; no storage copy, sockets, host, GUI, GPU, or automatic actions.
- Milestone: `XioEventConsumer.read_overlay()` and `read_overlay_cursor()` implemented and tested against altered private input.
- Evidence: focused XIO/LUCIDA suite `41 passed`; `git diff --check` clean.
- Evidence: focused XIO/LUCIDA suite `41 passed`; complete suite `108 passed`; `git diff --check` clean; no LUCIDA test process active; new code and ledger content pass ASCII.
- Evidence: focused XIO/LUCIDA suite `41 passed`; complete suite `108 passed`; `git diff --check` clean; no LUCIDA test process active; new code and ledger content pass ASCII.
- Published: commit `04c4a08` pushed to `origin/LUCIDA`; working tree clean.
- Closure: XIO now has a direct safe view/cursor path without copying raw payload or provenance into overlay output. Further expansion should require a concrete host or transport contract.
