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

python .\tools\mosaik_cli.py instar "D:\VJ\Media" --target-fps 60 --report ".\artifacts\instar.json"
python .\tools\mosaik_cli.py diagnose "D:\VJ\Media\clip.mp4" --report ".\artifacts\clip-report.json"
python .\tools\mosaik_cli.py dxv "D:\VJ\Media\clip.mp4" --fps 60
```

## Dependencias

Instala las dependencias Python con:

```powershell
python -m pip install -r requirements.txt
```

El runtime de MOSAIK usa la biblioteca estándar de Python. Para analizar media
se necesitan `ffmpeg` y `ffprobe` disponibles en `PATH`; para la integración
directa con Resolume se necesita Arena/Avenue 7.26 o posterior y su MCP local.

Los scripts solo leen el estado del equipo y muestran advertencias; no cambian el plan de
energía, BIOS, controladores, archivos ni configuraciones de Resolume.

## Estructura

```text
docs/
  architecture/     Arquitectura de componentes y etapas de MOSAIK.
  decisions/       Decisiones de diseño del repositorio.
  research/        Mapa de conceptos VJ y herramientas open source.
  runbooks/        Procedimientos operativos paso a paso.
  checklists/      Listas breves para usar antes o durante un show.
  templates/       Plantillas para registrar nuevos casos.
schemas/           Contratos compartidos para INSTAR, NAYADE e IMAGO.
tools/             Scripts locales y núcleo de herramientas MOSAIK.
artifacts/         Salidas locales; ignoradas por Git.
```

## Principios

- Priorizar procedimientos que puedan comprobarse en el equipo real.
- Separar hechos observados, hipótesis y acciones recomendadas.
- No versionar medios pesados ni datos que identifiquen innecesariamente al equipo.
- Evitar cambios irreversibles antes de un show.
- Registrar la fecha, el hardware, la versión de software y las condiciones de prueba.

## Próximos incrementos

1. Validar `MOSAIK Diagnose` con clips sintéticos y casos reales.
2. Mejorar `MOSAIK DXV Assistant` con procesamiento por lotes y más perfiles.
3. Empaquetar las herramientas como aplicación portable para colegas.
4. Incorporar una plantilla de incidente para flicker, tearing, frames dropped y pérdida de rutas.
5. Registrar resultados de pruebas reales en `docs/cases/` sin copiar medios al repositorio.
6. Diseñar el perfil de señal de MOSAIK para diagnóstico seguro de GPU, HDMI y procesadores LED.
7. Crear en `INSTAR` el importador de `VENUE` y `BASE DE DATOS PUBLICA`, comenzando por Advanced Output XML.
8. Integrar el auditor de composición Resolume con el MCP local, manteniendo el modo de lectura como comportamiento por defecto.

La arquitectura de esta integración está documentada en
`docs/architecture/integracion-mosaik-resolume-mcp.md`.
