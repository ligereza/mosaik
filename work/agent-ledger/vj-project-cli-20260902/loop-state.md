# Autonomous loop state

- Objective: continue MOSAIK toward an accessible, auditable VJ workflow.
- Scope: expose safe projection of real INSTAR, NAYADE, and IMAGO JSON documents through the CLI.
- Branch: `codex/mosaik-vj-integration`.
- Status: implementation and verification complete; publish pending.
- Changes: added `adapters/vj/project.py`, the `vj-project` CLI command, event and projection modes, previous-phase validation, processor observation input for NAYADE, plus `vj-project-replay` for chaining real stage reports through a manifest.
- Safety: reads only explicitly selected JSON files; writes only an explicitly requested output; performs no transport, hardware, or process action.
- Evidence: full pytest suite (`247 passed`), schema graph validation (`40 schemas`), ASCII guard, and conflict-marker scan passed.
- Next action: commit and push after final repository and process-state checks.
