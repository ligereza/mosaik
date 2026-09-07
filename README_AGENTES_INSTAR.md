# README para agentes — INSTAR

Esta rama concentra el trabajo de preparación de material y destino para un
show VJ. El documento orienta el criterio del agente; no sustituye el encargo
del usuario ni convierte una preferencia en una prohibición.

## Lo que buscamos

**Intención:** convertir medios, composiciones y mapping en evidencia útil para
decidir qué está listo, qué riesgo existe y qué adaptación conviene probar.

**Resultado esperado:** un informe, manifiesto, plan, preview o cambio de código
que permita revisar la decisión y repetirla. El resultado puede ser parcial si
el encargo sólo pide una exploración.

**Alcance habitual:** `tools/mosaik/instar.py`, `adapt.py`, `media.py`,
`resolume.py`, `cue_plan.py`, `preflight.py`, los schemas relacionados y sus
pruebas.

## Cómo trabajar

- Empieza por identificar el objetivo real: catálogo, preflight, análisis
  profundo, DXV, CUES, Advanced Output, mapping o adaptación target-specific.
- Elige la profundidad que resuelva la pregunta. No ejecutes análisis GPU,
  conversiones o recorridos pesados sólo por costumbre.
- Conserva los datos de entrada y produce artefactos derivados, comparables y
  trazables. No ocultes advertencias detrás de un estado aparentemente listo.
- Separa hechos medidos, cálculos, recomendaciones y decisiones artísticas.
  INSTAR puede preparar evidencia; no reemplaza el criterio del VJ.
- Si aparece una incompatibilidad entre formato, destino y medio, explica las
  alternativas y el coste de cada una antes de elegir.

## Defaults que ayudan, no límites absolutos

- Los archivos originales y showfiles se conservan; las adaptaciones se
  generan como derivados identificables.
- El fallback silencioso de GPU a CPU no es aceptable cuando cambia la
  interpretación del resultado; si el usuario lo autoriza, déjalo explícito.
- La lectura de Resolume y Advanced Output es el camino normal. La escritura o
  control externo requiere una decisión separada, una interfaz comprobable y
  una verificación proporcional al riesgo.
- Reutiliza contratos, fixtures y utilidades existentes antes de crear otra
  representación. Amplía el diseño cuando el encargo lo justifique.

## Comprobación

Verifica el comportamiento relevante con pruebas focalizadas, validación de
schemas y revisión de los artefactos generados. Para cambios amplios, ejecuta
la suite completa. Registra qué se comprobó, con qué entradas y qué quedó como
supuesto.

## Para quien continúe

Deja al final: estado actual, artefactos y rutas, comprobación relevante,
próximo paso, decisión tomada y cualquier incertidumbre que pueda cambiar el
mapping o la preparación del show. Retira notas obsoletas en vez de acumularlas.

## Flujo de rama

Esta rama conserva el contexto de enfoque INSTAR. Para una tarea concreta,
crea una rama corta como `agent/instar/<task>` desde este punto, trabaja con
libertad dentro del encargo y abre un PR hacia `main`. Si el cambio cruza
NAYADE, IMAGO, LUCIDA o el adaptador VJ, deja visible la frontera y coordina la
integración por el PR; no mantengas divergencias largas sólo por comodidad.

## Tareas adecuadas para esta rama

Preflight de media, análisis visual/temporal, catálogo y caché, mapas de CUES,
lectura de Advanced Output, planes de mapping, derivados para superficies
extremas, validación de perfiles de show y mejoras de sus contratos.
