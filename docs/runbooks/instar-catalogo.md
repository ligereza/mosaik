# INSTAR: catálogo, perfiles y caché

INSTAR prepara material para un show sin modificar los videos originales. Puede
leer metadata técnica, reutilizar análisis anteriores y comparar cada visual con
un perfil de destino.

## Análisis técnico con caché

```powershell
python .\tools\mosaik_cli.py instar "D:\VJ\Media" `
  --cache-db ".\artifacts\instar.sqlite3" `
  --report ".\artifacts\instar.json" `
  --html-report ".\artifacts\instar.html" `
  --manifest ".\artifacts\instar-manifest.json" `
  --sidecars-dir ".\artifacts\sidecars"
```

La caché identifica cada archivo con una huella rápida de tamaño, fecha de
modificación y extremos del archivo. Si el archivo y los parámetros no cambian,
INSTAR reutiliza el reporte sin volver a llamar a FFprobe ni al análisis visual.

## Comparar contra un perfil de show

```powershell
python .\tools\mosaik_cli.py instar "D:\VJ\Media" `
  --show-profile ".\docs\templates\show-profile.json" `
  --cache-db ".\artifacts\instar.sqlite3" `
  --report ".\artifacts\instar-show.json" `
  --html-report ".\artifacts\instar-show.html"
```

El perfil puede declarar resolución, FPS, codec permitido, alpha, rango de
color y refresco. Las reglas solo agregan advertencias al informe; no escalan,
convierten ni corrigen archivos.

## Modos GPU

Para un análisis visual con NVIDIA se puede añadir `--gpu`. La salida incluye un
`ClipProfile` con movimiento, luminancia, energía, periodicidad, candidatos de
flash, picos visuales y una estimación de continuidad del loop.

```powershell
python .\tools\mosaik_cli.py instar "D:\VJ\Media" `
  --gpu --gpu-max-frames 900 --gpu-batch-size 16 `
  --cache-db ".\artifacts\instar-gpu.sqlite3" `
  --report ".\artifacts\instar-gpu.json"
```

Si el codec no es compatible con la ruta NVDEC disponible, INSTAR lo marca como
`GPU_UNAVAILABLE`; no hace fallback silencioso a CPU.

## Salidas

- `*.json`: informe completo del lote.
- `*.mosaik.json`: sidecar por visual para NAYADE e IMAGO.
- `*.html`: tabla navegable para revisar el material.
- `*-manifest.json`: catálogo portable con rutas relativas, estados y perfiles.
- `*.sqlite3`: caché local, no debe versionarse en Git.
- `clip_profile.schema.json`: contrato de cada visual.

## Seguridad operativa

- El perfil de show es de solo lectura.
- No se modifican videos, composiciones, Resolume ni procesadores.
- La huella rápida no reemplaza una verificación forense; solo decide si es
  razonable reutilizar el análisis local.
- Las alertas de flash, loop y color son señales de revisión, no certificaciones
  de la cadena física de salida.
