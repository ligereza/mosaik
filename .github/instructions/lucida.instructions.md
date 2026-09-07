---
applyTo: "lucida/**/*.py,lucida/**/*.json,schemas/lucida-*.json,schemas/signal-*.json,schemas/overlay-*.json,schemas/host-*.json,schemas/xio-*.json,tests/lucida/**/*.py"
---

LUCIDA mantiene contratos y fronteras auditables. Revisa primero el schema y
los consumidores; conserva identidad, secuencia, provenance y compatibilidad.
Las vistas publicas deben ser acotadas y no filtrar payloads, rutas, notas ni
secretos. Usa replay determinista y tests de invalidos. No impongas una regla
de validacion sin relacionarla con una invariante, seguridad o compatibilidad.
