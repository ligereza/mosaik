---
applyTo: "adapters/vj/**/*.py,adapters/vj/**/*.json,tests/vj/**/*.py,schemas/event.schema.json,schemas/show-profile.schema.json,schemas/*-manifest.schema.json"
---

El adaptador VJ es una frontera host-neutral. Convierte mediante listas blancas
y contratos compartidos; valida identidad, secuencia, timestamp, fase y
provenance. Mantiene replay determinista y no introduce sockets, procesos,
Resolume, puertos o hardware como efecto secundario. Si se amplia el alcance,
separa contrato y transporte y documenta la autorizacion y el rollback.
