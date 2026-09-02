# Mapa de CUES de Resolume

## Objetivo

Leer los CUES existentes en una composición `.avc` para que INSTAR, NAYADE e
IMAGO puedan reutilizarlos sin modificar el showfile original.

## Uso

```powershell
python .\tools\mosaik_cli.py resolume-cues "C:\ruta\show.avc" `
  --report ".\artifacts\resolume-cues.json"
```

El resultado es un `ResolumeCueMap` con:

- clip, nombre, capa y columna;
- medios asociados al clip;
- duración y transporte;
- BPM manual o detectado guardado por Resolume;
- posiciones `Position1`, `Position2`, etc.;
- posición en milisegundos, segundos y proporción del clip;
- slots CUE vacíos;
- duración de transición de la capa.

## Interpretación

Esta primera versión conserva los nombres técnicos de Resolume. `Position1` no
se interpreta todavía como `inicio`, `build` o `drop`: esa capa semántica se
añadirá después con revisión humana o con el análisis de NAYADE.

Los CUES son posiciones dentro del clip. No son una ventana de seguridad, no
reemplazan la transición de capa y no modifican el movimiento de un efecto.
El futuro gap de preparación deberá implementarse como una capa STAGE separada.

## Seguridad

- El comando es de solo lectura sobre la composición.
- El JSON se escribe únicamente en la ruta indicada con `--report`.
- No se reemplazan ni editan archivos `.avc`.
- Antes de generar una composición preparada se deberá trabajar sobre una copia
  y validar que Resolume la abra correctamente.
