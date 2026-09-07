---
applyTo: "tools/mosaik/imago.py,tools/mosaik/incidents.py,schemas/imago-*.json,schemas/mosaik-incident-plan.schema.json,tests/vj/test_imago_input.py,tests/vj/test_incidents.py,tools/tests/test_imago.py"
---

IMAGO representa el estado y las decisiones asistidas de un show. Preserva
identidad, secuencia, fase, checkpoints y estado de aprobacion. Mantiene las
propuestas reversibles y proposal_only por defecto. Distingue plan de accion y
observacion de ejecucion; los hosts externos requieren una frontera explicita y
verificacion especifica.
