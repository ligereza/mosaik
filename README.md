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

python .\tools\mosaik_cli.py instar "D:\VJ\Media" --target-fps 60 --report ".\artifacts\instar.json" --sidecars-dir ".\artifacts\instar-sidecars"
python .\tools\mosaik_cli.py instar "D:\VJ\Media" --deep --report ".\artifacts\instar-deep.json"
python .\tools\mosaik_cli.py diagnose "D:\VJ\Media\clip.mp4" --report ".\artifacts\clip-report.json"
python .\tools\mosaik_cli.py dxv "D:\VJ\Media\clip.mp4" --fps 60
```

## Dependencias

Instala las dependencias Python con:

```powershell
python -m pip install -r requirements.txt
```

Para habilitar el análisis visual GPU en una máquina NVIDIA:

```powershell
python -m pip install -r requirements-gpu.txt
```

El runtime de MOSAIK usa la biblioteca estándar de Python. El preflight técnico
de INSTAR usa sólo FFprobe y no decodifica todo el video; `--deep` activa el
diagnóstico adicional de luminancia. `--gpu` usa NVDEC/CUDA y no hace fallback
silencioso a CPU. Para analizar media
se necesitan `ffmpeg` y `ffprobe` disponibles en `PATH`; para la integración
directa con Resolume se necesita Arena/Avenue 7.26 o posterior y su MCP local.

INSTAR también puede construir perfiles reutilizables, comparar la media con un
perfil de show y guardar una caché SQLite. Las dependencias Python de catálogo
(`PyAV`, `NumPy`, `Pillow`, `PySceneDetect`, OpenCV y `jsonschema`) están fijadas
en `requirements.txt`; el backend NVIDIA sigue separado en `requirements-gpu.txt`.

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

## Catálogo INSTAR

Para preparar material contra un objetivo conocido:

```powershell
python .\tools\mosaik_cli.py instar "D:\VJ\Media" `
  --show-profile ".\docs\templates\show-profile.json" `
  --cache-db ".\artifacts\instar.sqlite3" `
  --report ".\artifacts\instar.json" `
  --html-report ".\artifacts\instar.html" `
  --manifest ".\artifacts\instar-manifest.json"
```

El resultado incluye un `ClipProfile` por visual con metadata, compatibilidad,
energía visual, periodicidad, loopabilidad y eventos detectados. La caché evita
repetir el trabajo mientras el archivo y los parámetros de análisis no cambien.
El manifiesto permite consumir el catálogo desde otras herramientas sin volver a
leer el reporte completo. El detalle operativo está en `docs/runbooks/instar-catalogo.md`.

## Principios

- Priorizar procedimientos que puedan comprobarse en el equipo real.
- Separar hechos observados, hipótesis y acciones recomendadas.
- No versionar medios pesados ni datos que identifiquen innecesariamente al equipo.
- Evitar cambios irreversibles antes de un show.
- Registrar la fecha, el hardware, la versión de software y las condiciones de prueba.

## Próximos incrementos

1. Validar `INSTAR Media Preflight` con clips sintéticos y casos reales.
2. Mejorar `MOSAIK DXV Assistant` con procesamiento por lotes y más perfiles.
3. Empaquetar las herramientas como aplicación portable para colegas.
4. Incorporar una plantilla de incidente para flicker, tearing, frames dropped y pérdida de rutas.
5. Registrar resultados de pruebas reales en `docs/cases/` sin copiar medios al repositorio.
6. Diseñar el perfil de señal de MOSAIK para diagnóstico seguro de GPU, HDMI y procesadores LED.
7. Crear en `INSTAR` el importador de `VENUE` y `BASE DE DATOS PUBLICA`, comenzando por Advanced Output XML.
8. Integrar el auditor de composición Resolume con el MCP local, manteniendo el modo de lectura como comportamiento por defecto.

La arquitectura de esta integración está documentada en
`docs/architecture/integracion-mosaik-resolume-mcp.md`.
