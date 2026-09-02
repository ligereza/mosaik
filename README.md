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
python .\tools\mosaik_cli.py instar-map "D:\VJ\Shows\venue-advanced-output.xml" --catalog ".\artifacts\instar-manifest.json" --report ".\artifacts\mapping-plan.json"
python .\tools\mosaik_cli.py instar-testcard "D:\VJ\Shows\venue-advanced-output.xml" --output ".\artifacts\venue-geometry-testcard.mp4" --report ".\artifacts\venue-geometry-testcard.json"
python .\tools\mosaik_cli.py nayade-session init ".\artifacts\venue-geometry-testcard.json" --output ".\artifacts\venue-soundcheck.json" --seed 4821
python .\tools\mosaik_cli.py resolume-cues "D:\VJ\Shows\show.avc" --report ".\artifacts\cues.json"
python .\tools\mosaik_cli.py nayade-processor catalog
python .\tools\mosaik_cli.py nayade-processor discover --report ".\artifacts\processor-discovery.json"
python .\tools\validate_schema_graph.py
python .\tools\mosaik_cli.py vj-replay ".\adapters\vj\replay\fixtures\plugin-bridges-fictional.json" --report ".\artifacts\vj-replay.json"
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

`validate_schema_graph.py` comprueba el registry local de contratos y sus referencias sin
red. Para validar una instancia JSON concreta, agrega `--schema` y `--instance`.

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
energía visual, periodicidad, loopabilidad, eventos detectados y, cuando hay
muestras suficientes, sugerencias de CUE para cambio limpio, impacto, ventana
de strobo y loop. La caché evita repetir el trabajo pesado mientras el archivo
y los parámetros de análisis no cambien; los perfiles derivados se reconstruyen
para incorporar nuevos detectores.
El manifiesto permite consumir el catálogo desde otras herramientas sin volver a
leer el reporte completo. El detalle operativo está en `docs/runbooks/instar-catalogo.md`.

### Mapa de CUES de Resolume

Para inspeccionar los puntos CUE existentes en una composición sin modificarla:

```powershell
python .\tools\mosaik_cli.py resolume-cues "D:\VJ\Shows\show.avc" `
  --report ".\artifacts\resolume-cues.json"
```

El mapa conserva la posición de cada CUE en milisegundos y segundos, su posición
normalizada respecto de la duración del clip, los slots vacíos, el BPM guardado
y la transición configurada en su capa. Todavía no asigna nombres semánticos ni
escribe nuevos CUES en la composición.

### Advanced Output y autoasignación

INSTAR puede leer un preset de Advanced Output y compararlo con el catálogo de
visuals. Conserva Input Selection y Output Transformation como espacios
separados, agrupa slices que comparten InputRect y genera sugerencias
revisables; no modifica showfiles, Resolume ni el procesador. El flujo está en
docs/runbooks/instar-advanced-output.md.

La tarjeta de prueba geométrica de NAYADE genera una sola composición desde el
Advanced Output, con colores por input group, etiquetas, bordes, cuadrícula,
movimiento, círculos y cuadrados. Sirve para detectar deformación, inversión,
deslizamiento y solapamiento durante el soundcheck sin modificar el showfile.
La sesión de NAYADE conserva la matriz de pruebas y permite registrar qué
rotación, flip, pattern o marquee fue aprobada en cada input group. El detalle
está en `docs/runbooks/nayade-soundcheck.md`.

La estrategia para adaptar visuales a banners, tótems y superficies extremas
está documentada en `docs/research/instar-adaptacion-superficies-extremas.md`.
INSTAR prioriza derivados target-specific con crop protegido, fondo, pattern o
marquee antes de permitir deformaciones.

Para generar previews de esas adaptaciones desde un plan de mapping:

```powershell
python .\tools\mosaik_cli.py instar-adapt `
  ".\artifacts\mapping-plan.json" `
  --output-dir ".\artifacts\adapt-previews" `
  --dxv-output-dir ".\artifacts\adapt-dxv" `
  --encoder auto
```

El detalle operativo está en `docs/runbooks/instar-adaptacion.md`.
El flujo completo, desde catálogo hasta soundcheck, está en
`docs/runbooks/instar-preshow.md`.
La decisión de herramientas adoptadas y pendientes está en
`docs/research/adopcion-herramientas.md`.

## Principios

- Priorizar procedimientos que puedan comprobarse en el equipo real.
- Separar hechos observados, hipótesis y acciones recomendadas.
- No versionar medios pesados ni datos que identifiquen innecesariamente al equipo.
- Evitar cambios irreversibles antes de un show.
- Registrar la fecha, el hardware, la versión de software y las condiciones de prueba.

## IMAGO: show

IMAGO observa el show en vivo, registra cues e incidentes, mantiene checkpoints
y publica propuestas reversibles para recovery y cierre. No ejecuta acciones en
Resolume, DMX ni procesadores. El contrato esta en
`schemas/imago-show-session.schema.json` y el flujo en
`docs/runbooks/imago-show.md`.

## Próximos incrementos

1. Validar `INSTAR Media Preflight` con clips sintéticos y casos reales.
2. Mejorar `MOSAIK DXV Assistant` con procesamiento por lotes y más perfiles.
3. Empaquetar las herramientas como aplicación portable para colegas.
4. Incorporar una plantilla de incidente para flicker, tearing, frames dropped y pérdida de rutas.
5. Registrar resultados de pruebas reales en `docs/cases/` sin copiar medios al repositorio.
6. Diseñar el perfil de señal de MOSAIK para diagnóstico seguro de GPU, HDMI y procesadores LED.
7. Crear en `INSTAR` el importador de `VENUE` y `BASE DE DATOS PUBLICA`, comenzando por Advanced Output XML.
8. Integrar el auditor de composición Resolume con el MCP local, manteniendo el modo de lectura como comportamiento por defecto.
9. Permitir que IMAGO consuma un plan de mapping aprobado, sin aplicar cambios
   automáticamente durante el primer ciclo.

La arquitectura de esta integración está documentada en
`docs/architecture/integracion-mosaik-resolume-mcp.md`.

### Replay del flujo VJ

`vj-replay` verifica desde la CLI el recorrido sintético `INSTAR -> NAYADE ->
IMAGO`, incluyendo show, incidente, recuperación y cierre. Sólo procesa el
fixture indicado, no abre transportes y no ejecuta propuestas ni cambios en el
hardware.

### NAYADE y procesadores LED

El catálogo inicial de procesadores está en `data/processors/catalog.json` y
los perfiles físicos de módulos siguen `schemas/module-profile.schema.json`.
NAYADE comienza con descubrimiento USB/COM y snapshots en solo lectura; no
envía comandos ni modifica procesadores. El flujo y sus límites están en
`docs/runbooks/nayade-processor.md`, y la investigación de familias, pitch,
indoor/outdoor y protocolos está en `docs/research/procesadores-led-y-modulos.md`.
