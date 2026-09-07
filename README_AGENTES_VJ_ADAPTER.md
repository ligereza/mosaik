# README para agentes — VJ adapter

Esta rama concentra la frontera que lleva reportes y señales de INSTAR,
NAYADE e IMAGO al contrato comun VJ. Debe ser pequeña, reusable y host-neutral:
su trabajo hace posible integrar, no presume que ya controlemos un show real.

## Lo que buscamos

**Intención:** transformar entradas heterogeneas en eventos canonicos,
proyecciones y replay que conserven orden, fase, provenance y seguridad sin
propagar datos privados ni acoplar el adaptador a una herramienta concreta.

**Resultado esperado:** un contrato, puente, proyector, validador o replay
determinista con fixtures y pruebas que expliquen qué cruza la frontera y qué
queda fuera.

**Alcance habitual:** `adapters/vj/`, sus schemas y fixtures, `tests/vj/` y
los puntos de integración CLI que sólo orquestan la conversión.

## Cómo trabajar

- Identifica productor, evento canonico, consumidor y frontera antes de editar.
- Usa listas blancas y proyecciones acotadas. El reporte completo no debe cruzar
  sólo porque el puente pueda leerlo.
- Valida `event_id`, `sequence`, timestamp, fase, provenance y los invariantes
  de read-only/proposal-only que correspondan.
- Reutiliza la transicion de fases y los modelos compartidos; no inventes una
  segunda semantica para cada plugin.
- Para integraciones externas, implementa primero el contrato y el replay. El
  transporte real es una decisión posterior, no una consecuencia accidental de
  importar una libreria.

## Defaults que ayudan, no límites absolutos

- Los puentes son puros y sin efectos laterales por defecto: no abren sockets,
  procesos, Resolume, puertos ni hardware al construir un evento.
- `osc`, `artnet`, `sacn`, `timecode`, `xio` y `unknown` pueden representar
  provenance o transporte declarado sin afirmar que el protocolo fue abierto.
- Los datos internos, rutas, notas, errores y payloads quedan fuera de la vista
  publica salvo una razon de contrato explicitamente revisada.
- Si el usuario necesita una integración real, separa transporte, permisos,
  observabilidad y rollback. No la rechaces por reflejo ni la escondas en un
  helper aparentemente inocente.

## Comprobación

Prueba entradas validas, campos desconocidos, secuencias fuera de orden,
timestamps sin zona, conflictos de provenance y replay de varias fases. Añade
kill tests para demostrar que el adaptador no abre procesos, sockets ni puertos
cuando el flujo es puramente declarativo.

## Para quien continúe

Deja el mapa de la frontera, campos permitidos, schemas, fixtures, pruebas,
limitaciones de transporte y el siguiente puente o consumidor. Indica si una
garantia es de contrato, de replay o de host real.

## Flujo de rama

Esta rama conserva el contexto de enfoque del adaptador VJ. Para una tarea concreta, crea una rama corta como `agent/vj-adapter/<task>` desde este punto, trabaja con libertad dentro del encargo y abre un PR hacia `main`. Si el cambio toca un productor o un host, documenta la frontera y coordina la integración por el PR; no uses esta rama para esconder acoplamientos que deban revisarse.

## Tareas adecuadas para esta rama

Puentes INSTAR/NAYADE/IMAGO, `ShowInputProjector`, contratos de eventos,
manifest y replay de proyectos, adaptadores OSC declarativos y validadores de
frontera.
