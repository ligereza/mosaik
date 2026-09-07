---
applyTo: "tools/mosaik/nayade.py,tools/mosaik/processors.py,tools/mosaik/output_probe.py,tools/mosaik/reconcile.py,tools/mosaik/protocol.py,schemas/nayade-*.json,schemas/processor-*.json,schemas/module-*.json,tests/vj/test_nayade_input.py,tools/tests/test_nayade_report.py,tools/tests/test_output_probe.py,tools/tests/test_reconcile.py"
---

NAYADE trabaja con evidencia de soundcheck y superficie LED. Conserva origen,
confianza, incertidumbre y contradicciones. Diferencia observacion, inferencia,
plan y accion. El descubrimiento de hardware es pasivo por defecto; cualquier
I/O o cambio externo requiere una decision explicita y pruebas proporcionales.
No simplifiques un conflicto para hacer que el reporte parezca READY.
