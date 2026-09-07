# README para agentes — NAYADE

Esta rama concentra el soundcheck y la evidencia del destino LED. Su objetivo
es ayudar a comprobar una superficie real sin fingir certeza ni encerrar al
agente en una receta fija.

## Lo que buscamos

**Intención:** ordenar observaciones sobre señal, geometría, color, procesador,
modulos y mapping para decidir que esta listo, que entra en revision y que
prueba reduce mejor la incertidumbre.

**Resultado esperado:** una tarjeta, sesion, observacion, reconciliacion,
protocolo o reporte de cierre reproducible. Puede ser `READY`, `INCOMPLETE`,
`REVIEW` o `BLOCKED`; no fuerces un resultado binario si la evidencia no lo
sostiene.

**Alcance habitual:** `tools/mosaik/nayade.py`, `processors.py`,
`output_probe.py`, `reconcile.py`, `protocol.py`, schemas, fixtures y pruebas.

## Cómo trabajar

- Comienza por separar hecho observado, fuente, confianza, calculo, hipotesis y
  siguiente prueba. Una nota de operador no es automaticamente una medicion.
- Usa el contexto disponible: Advanced Output, EDID, señal, procesador,
  modulos, patrones y resultados previos. No descartes un conflicto por hacer
  que el reporte parezca mas simple.
- Prioriza el siguiente paso que mas reduzca la incertidumbre con el menor
  riesgo. El protocolo debe explicar que observar y por que.
- Conserva estados desconocidos y contradicciones. La ausencia de datos es un
  resultado util cuando queda explicitada.
- Reutiliza la matriz de soundcheck y los contratos existentes; crea una nueva
  forma solo si resuelve una necesidad real.

## Defaults que ayudan, no límites absolutos

- El descubrimiento de procesadores es pasivo por defecto: identifica,
  registra y ordena coincidencias sin enviar bytes ni modificar hardware.
- La recomendacion es `proposal_only` hasta que exista una autorizacion,
  interfaz y comprobacion suficientes para una accion externa. Si el encargo
  cambia ese alcance, analiza el salto de riesgo en lugar de bloquearlo por
  reflejo.
- No declares confirmado el estado fisico de una pantalla sólo por un perfil,
  EDID o inferencia. Indica qué evidencia falta.
- Las sesiones y reportes se escriben de forma atomica y no deben sobrescribir
  el original sin una razon explícita.

## Comprobación

Valida schemas e invariantes de seguridad, prueba casos estables y ambiguos, y
comprueba que el flujo no abra puertos ni ejecute acciones cuando el encargo es
de observacion o plan. Para cambios amplios ejecuta la suite completa y el
grafo de schemas.

## Para quien continúe

Deja el estado de la sesión, la evidencia consultada, las contradicciones, el
proximo chequeo y los riesgos pendientes. Indica si el resultado es observado,
calculado, probable, conflictivo o desconocido.

## Tareas adecuadas para esta rama

Tarjetas de prueba, sesiones reproducibles, catalogo de procesadores, perfiles
de modulos, sondas de salida, reconciliacion de cadena, protocolos de
soundcheck, diagnostico de color/señal y reportes de cierre.
