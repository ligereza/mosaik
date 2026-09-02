# NAYADE: soundcheck reproducible

NAYADE convierte una prueba de pantalla en una matriz explícita y auditable.
Recibe un resumen de mapping o una tarjeta de prueba, agrupa slices por
`input_group_id` y prepara baseline, flips, rotación, patrón y marquee.

## Crear una sesión

```powershell
python tools/mosaik_cli.py nayade-session init `
  .\artifacts\mapping-summary.json `
  --output .\artifacts\nayade-session.json `
  --session-id show-01-nayade `
  --seed 4821
```

La matriz es determinista cuando se conserva la semilla. El archivo fuente se
resume; NAYADE no copia payloads arbitrarios ni modifica el mapping original.

## Ejecutar el siguiente paso

```powershell
python tools/mosaik_cli.py nayade-session next .\artifacts\nayade-session.json
```

El operador realiza la prueba en la cadena real y registra el resultado:

```powershell
python tools/mosaik_cli.py nayade-session record `
  .\artifacts\nayade-session.json `
  --step-id step-001 `
  --result approved `
  --target group-a `
  --parameters '{"signal_lock":true}' `
  --notes "Baseline estable."
```

Registrar un resultado no envía comandos a Resolume, al procesador LED ni a la
red. La observación del procesador debe permanecer separada de la hipótesis
sobre módulos, pixel pitch, indoor/outdoor, gamma o rango de color.
