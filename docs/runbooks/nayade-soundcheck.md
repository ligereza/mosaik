# NAYADE: sesión reproducible de soundcheck

NAYADE convierte las pruebas que normalmente quedan en la memoria del VJ en
un registro portable. La sesión se inicia desde un informe de mapping o desde
la tarjeta geométrica y conserva el `input_group_id` como unidad de prueba.
Esto evita tratar como independientes varias slices que comparten el mismo
InputRect.

## Iniciar la sesión

~~~powershell
python .\tools\mosaik_cli.py nayade-session init `
  "Z:\MOSAIK\runs\plox-geometry-testcard-video.json" `
  --output "Z:\MOSAIK\runs\plox-nayade-soundcheck.json" `
  --name "PLOX — Soundcheck Mapping" `
  --seed 4821 `
  --adaptation-plan "Z:\MOSAIK\runs\plox-instar-adaptation-dxv-v1.json"
~~~

La sesión crea una matriz corta y determinista:

- baseline;
- flip horizontal;
- flip vertical;
- rotación de 180 grados;
- pattern por input group;
- marquee en el eje de la superficie.
- variantes target-specific generadas por INSTAR, cuando se entrega
  `--adaptation-plan`.

La semilla permite repetir variaciones futuras. Los pasos comienzan como
`planned`; INSTAR y NAYADE no inventan si una transformación funcionó en la
pantalla real.

## Registrar un resultado

Después de probar una variación en Resolume:

~~~powershell
python .\tools\mosaik_cli.py nayade-session record `
  "Z:\MOSAIK\runs\plox-nayade-soundcheck.json" `
  --operation marquee `
  --scope input_group `
  --target input-group-003 `
  --result approved `
  --parameters '{"axis":"horizontal","speed":0.18,"wrap":true}' `
  --notes "La franja se lee limpia y no invade el slice vecino."
~~~

Los resultados válidos son `approved`, `rejected`, `review`, `running` y
`planned`. Se pueden registrar varios objetivos repitiendo `--target`.

NAYADE vincula automáticamente el registro con el primer paso pendiente que
coincide. Para evitar cualquier ambigüedad se puede indicar el ID exacto:

```powershell
python .\tools\mosaik_cli.py nayade-session record `
  "Z:\MOSAIK\runs\plox-nayade-soundcheck.json" `
  --step-id step-009 `
  --operation instar_adaptation `
  --result approved `
  --notes "El marquee se lee sin costura."
```

Para continuar sin buscar manualmente en el JSON:

```powershell
python .\tools\mosaik_cli.py nayade-session next `
  "Z:\MOSAIK\runs\plox-nayade-soundcheck.json"
```

La sesión todavía registra decisiones, pero no envía órdenes a Resolume. Esto
deja abierta una integración posterior con OSC, MIDI o Chataigne sin mezclar
la capa de control con la evidencia del soundcheck.
