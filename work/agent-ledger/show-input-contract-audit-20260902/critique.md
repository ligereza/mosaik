# Self-critique

- previous_action: accepted the published projection as complete
- finding: consumers could produce projections but had no public validator for
  received dictionaries
- selected_action: continue with a narrow contract audit rather than add a
  reducer or transport implementation
- decision_delta: add `ShowInputProjection.from_dict()` and
  `validate_show_input()`, plus a kill test for socket and subprocess entry points
- forecast: the next likely integration is a reducer consuming this contract;
  keeping validation public now avoids duplicate parsing and lowers future
  compatibility risk
- limitation: transport labels remain declarative; protocol parsing and actual
  network/hardware access remain outside this branch
- verification_signal: focused suite, complete suite, schema graph, ASCII guard,
  and diff check pass
