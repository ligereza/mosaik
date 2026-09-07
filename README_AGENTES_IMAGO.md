# README para agentes — IMAGO

Esta rama concentra la asistencia durante el show: estado, checkpoints,
incidentes, recovery y cierre. El agente debe aumentar la capacidad de
decisión del operador, no reemplazarla con automatismos opacos.

## Lo que buscamos

**Intención:** convertir el estado observado del show en un cursor claro,
hipotesis verificables y propuestas reversibles para operar con menos sorpresa.

**Resultado esperado:** una sesion consistente, un plan de incidente, un
reporte de estado o una propuesta de recovery/cierre que indique qué se sabe,
qué se infiere y qué aprobación falta.

**Alcance habitual:** `tools/mosaik/imago.py`, `incidents.py`, contratos de
show, CLI, fixtures y pruebas relacionadas con estado, fases y propuestas.

## Cómo trabajar

- Conserva la secuencia temporal, identidad de sesión y transiciones de fase.
  Un estado final plausible no justifica aceptar una secuencia inconsistente.
- Separa hechos observados, hipótesis, impacto, siguiente comprobación y
  recuperación. Un incidente no es todavía un diagnóstico.
- Haz propuestas concretas y reversibles: explica precondiciones, riesgo,
  resultado esperado y forma de volver atrás.
- Mantén el contexto suficiente para que otro agente pueda continuar sin
  reconstruir el show desde mensajes sueltos.
- Si hay varias recuperaciones razonables, ordénalas por riesgo y evidencia en
  vez de elegir silenciosamente una por conveniencia.

## Defaults que ayudan, no límites absolutos

- Las propuestas permanecen `proposal_only`, requieren aprobación explícita y
  no se convierten en ejecución por el hecho de estar bien formadas.
- El flujo normal es read-only: no tocar Resolume, DMX, procesadores o medios
  externos sin una autorización y una interfaz verificables.
- Una ventana de resguardo puede proteger la visual base ante un experimento o
  missclick, pero debe conservar duración, reversibilidad y límites claros.
- Si el usuario pide integración externa, no la rechaces por reflejo: delimita
  el nuevo perímetro, identifica la prueba segura y confirma las consecuencias.

## Comprobación

Prueba transiciones normales, secuencias fuera de orden, estados de cierre,
incidentes y propuestas malformadas. Valida schemas, invariantes de aprobación
y ausencia de efectos laterales. Ejecuta la suite completa si el cambio afecta
el cursor común o la CLI.

## Para quien continúe

Registra estado actual, último evento válido, evidencia, propuesta pendiente,
aprobación requerida, comprobaciones ejecutadas y el siguiente paso operativo.
No confundas un plan de recovery con una acción ya aplicada.

## Flujo de rama

Esta rama conserva el contexto de enfoque IMAGO. Para una tarea concreta, crea una rama corta como `agent/imago/<task>` desde este punto, trabaja con libertad dentro del encargo y abre un PR hacia `main`. Si el cambio cruza NAYADE, INSTAR, LUCIDA o el adaptador VJ, deja visible la secuencia y coordina la integración por el PR; no conviertas esta rama en un silo permanente.

## Tareas adecuadas para esta rama

Sesiones de show, checkpoints, incidentes, planes de recovery, guard windows,
replay de fases, reportes de cierre, invariantes de propuesta y mejoras del
cursor de estado.
