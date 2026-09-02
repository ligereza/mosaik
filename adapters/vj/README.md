# VJ Adapter

Adaptador de dominio para conectar una sesión VJ con el núcleo reusable de
VJ. En esta primera extracción el adaptador es una máquina de estados pura:
recibe eventos y estado, genera propuestas auditables y registra resultados.

No ejecuta comandos, no abre puertos, no llama a Resolume, no controla
procesadores LED y no modifica un show.

## Uso mínimo

```python
from adapters.vj import VJAdapter

adapter = VJAdapter()
state = adapter.initial_state("session-001")
state, proposals = adapter.process(
    {
        "event_id": "evt-001",
        "timestamp": "2026-01-10T20:00:00Z",
        "phase": "preflight",
        "event_type": "phase.completed",
        "payload": {"status": "pass"},
    },
    state,
)
state = adapter.register_result(
    state,
    {
        "result_id": "res-001",
        "proposal_id": proposals[0].proposal_id,
        "recorded_at": "2026-01-10T20:01:00Z",
        "status": "observed",
        "notes": "Checkpoint revisado por el operador.",
    },
)
```

## Replay

```python
from adapters.vj.replay import replay_path

report = replay_path("adapters/vj/replay/fixtures/session-fictional.json")
assert report["status"] == "PASS"
```

El replay no usa la hora actual ni dependencias externas: con el mismo fixture
produce el mismo resultado. Las propuestas siempre contienen
`requires_explicit_approval=true`, `reversible=true` y
`execution_mode=proposal_only`.

La restauración de propuestas también respeta el schema publicado: exige los
campos obligatorios y rechaza propiedades extra antes de registrar una
propuesta.

## Show input projection

`ShowInputProjector` consumes a canonical `VJEvent` and returns only the
metadata a future LUCIDA reducer needs: `show_state`, `show_phase`, an optional
`preview_candidate`, source timestamp, sequence, and bounded provenance.
Existing `OscResolumeBoundary.normalize()` can provide the event; `artnet`,
`sacn`, and `timecode` are accepted as transport labels without opening a
socket or implementing a protocol parser here.
`project_osc_show_input()` is the convenience path that calls the existing OSC
normalizer and then applies the same bounded projection.

The projector rejects stale sequence or timestamp input and never mutates a
`VJState`, creates a host action, or executes a `VJProposal`. Its replay helper
uses the existing fixture loader and remains deterministic and side-effect free.
The machine-readable contract is
[`show-input.schema.json`](contracts/show-input.schema.json).
`validate_show_input()` provides the matching public validator for a future
reducer or replay consumer.
The kill test patches socket and subprocess entry points and confirms that
projection does not open transport or spawn a process.

## Extensión

Los adaptadores concretos de medios, cues, DXV, Art-Net/DMX/sACN, LED
processors y mapping deben traducir sus observaciones a `VJEvent` y sus
resultados a `VJResult`. No deben saltarse la máquina de estados ni ejecutar
acciones dentro de `VJAdapter`.
