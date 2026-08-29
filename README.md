# MOSAIK

Repositorio personal de herramientas, procedimientos y conocimiento práctico para trabajo VJ.

El objetivo es convertir problemas reales —preparación de shows, reproducción en Resolume,
conversión a DXV, diagnóstico de rendimiento y organización de medios— en procedimientos
repetibles y verificables.

## Inicio rápido

Desde PowerShell, en la raíz del repositorio:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\Test-VJPreflight.ps1 -MediaRoot "D:\VJ\Media" -ProjectRoot "D:\VJ\Shows\show-01"
.\tools\Get-VJSystemSnapshot.ps1 -OutputPath ".\artifacts\snapshot.json"
```

Los scripts solo leen el estado del equipo y muestran advertencias; no cambian el plan de
energía, BIOS, controladores, archivos ni configuraciones de Resolume.

## Estructura

```text
docs/
  decisions/       Decisiones de diseño del repositorio.
  runbooks/        Procedimientos operativos paso a paso.
  checklists/      Listas breves para usar antes o durante un show.
  templates/       Plantillas para registrar nuevos casos.
tools/             Scripts locales de diagnóstico y verificación.
artifacts/         Salidas locales; ignoradas por Git.
```

## Principios

- Priorizar procedimientos que puedan comprobarse en el equipo real.
- Separar hechos observados, hipótesis y acciones recomendadas.
- No versionar medios pesados ni datos que identifiquen innecesariamente al equipo.
- Evitar cambios irreversibles antes de un show.
- Registrar la fecha, el hardware, la versión de software y las condiciones de prueba.

## Próximos incrementos

1. Añadir un inventario de clips que detecte resolución, FPS, códec y presencia de alpha.
2. Incorporar una plantilla de incidente para flicker, tearing, frames dropped y pérdida de rutas.
3. Registrar resultados de pruebas reales en `docs/cases/` sin copiar medios al repositorio.
