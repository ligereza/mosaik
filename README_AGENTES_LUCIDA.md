# README para agentes — LUCIDA

Esta rama concentra contratos, estado, señales, overlays, replay y fronteras
host-neutrales. Su trabajo debe hacer que el sistema sea más observable y
componible sin convertir la seguridad en una colección de bloqueos inútiles.

## Lo que buscamos

**Intención:** ofrecer contratos estables y proyecciones acotadas para que
productores, adaptadores y hosts puedan colaborar sin filtrar payloads privados
ni perder la trazabilidad de una decisión.

**Resultado esperado:** un schema, modelo, boundary, replay, vista, validador o
decisión de arquitectura que sea verificable, compatible cuando corresponda y
claro sobre sus límites.

**Alcance habitual:** `lucida/`, sus contratos y fixtures, `schemas/`,
`adapters/vj/` cuando el cambio cruce esa frontera, y `tests/lucida/`.

## Cómo trabajar

- Empieza por el contrato público y sus consumidores. Verifica si el cambio es
  aditivo, incompatible o sólo una corrección de validación.
- Mantén separados los hechos internos, la vista pública, la provenance y los
  payloads. Proyectar no significa copiar todo.
- Preserva identidad, secuencia, cursor, revisiones, digest y fase cuando sean
  parte del contrato. Rechaza incoherencias que puedan ocultar pérdida de
  eventos o una decisión no autorizada.
- Prefiere replay determinista y fixtures pequeños antes que dependencias de
  red, host o hardware. Si el encargo necesita un host real, diseña la
  interfaz y el test de frontera sin simular una confirmación inexistente.
- Actualiza schema, runtime, fixtures, pruebas y documentación en conjunto
  cuando forman una sola decisión.

## Defaults que ayudan, no límites absolutos

- La vista pública usa listas blancas y datos acotados; no expongas rutas,
  payloads, notas, razones o secretos sólo porque estén disponibles internamente.
- Las acciones externas permanecen read-only o proposal-only por defecto. Una
  extensión autorizada debe declarar su nueva frontera y sus garantías.
- La validación estricta es útil cuando protege identidad, orden, seguridad o
  compatibilidad. No agregues restricciones que sólo vuelvan más difícil una
  evolución legítima del contrato.
- Mantén ASCII en campos técnicos y estructuras parseables; la documentación
  humana puede explicar la decisión con el idioma y el detalle necesarios.

## Comprobación

Ejecuta pruebas de schema y runtime, replay determinista, casos inválidos y
kill tests de efectos laterales cuando corresponda. Comprueba referencias del
grafo de schemas y la frontera pública. Una corrección de contrato no está
terminada si sólo compila el modelo interno.

## Para quien continúe

Deja la decisión de compatibilidad, schemas afectados, consumidores revisados,
fixtures, pruebas, riesgos y el siguiente punto de extensión. Enlaza el ADR o
registro de trabajo cuando exista y retira descripciones obsoletas.

## Flujo de rama

Esta rama conserva el contexto de enfoque LUCIDA. Para una tarea concreta, crea una rama corta como `agent/lucida/<task>` desde este punto, trabaja con libertad dentro del encargo y abre un PR hacia `main`. Si el cambio cruza contratos VJ o una etapa de producto, documenta la compatibilidad y coordina la integración por el PR; no mantengas una divergencia permanente sin una decisión explícita.

## Tareas adecuadas para esta rama

Contratos de estado y capacidades, signal profiles, OSC/XIO, overlays,
replay, vistas públicas, host decisions, validadores, provenance, drift y
decisiones de arquitectura de las fronteras VJ.
