# Arquitectura MOSAIK por etapas y componentes

Estado: propuesta de diseño  
Fecha: 2026-08-28

## Decisión principal

MOSAIK no debe convertirse en tres versiones del mismo plugin. Las palabras
biológicas describen **cuándo** se usa una herramienta; los tipos de componente
describen **qué** hace. El código y los perfiles se comparten.

```text
                 MOSAIK
                   │
     ┌─────────────┼─────────────┐
     │             │             │
   Probe         Guard         Bridge
  medir        corregir      conectar
     │             │             │
     └─────────────┼─────────────┘
                   │
          Signal Profile + Rules
                   │
       ┌───────────┼───────────┐
       │           │           │
    Python       FFGL        XIO
   offline       live      monitoring
```

Las etapas de uso quedan como una taxonomía independiente:

| Etapa | Uso principal |
|---|---|
| `INSTAR` | PRE SHOW: preparación de media y del sistema |
| `NAYADE` | SOUNDCHEK: prueba estable, handoff y routing con el house |
| `IMAGO` | SHOW: operación real en vivo dentro de Resolume |

Estas etiquetas no obligan a que cada etapa sea un plugin. Algunas serán
herramientas externas, otras perfiles y otras entradas FFGL. Los reportes y
estadísticas se generan como evidencia transversal, no como una cuarta etapa.

## Tipos de componente

### Probe

Mide y explica. No altera el sistema.

Ejemplos:

- `Media Probe`: codec, resolución, FPS, alpha, VFR, luminancia y riesgos.
- `Output Probe`: GPU, monitor, EDID, resolución, Hz, color space y rango.
- `House Probe`: captura, input lock, formato, bus, destino y grupo de salidas.
- `Pattern Probe`: PLUGE, rampa, barras, checkerboard y pruebas de movimiento.

Los probes pueden ser Python, PowerShell o una herramienta portable. No deben
ser FFGL si necesitan inspeccionar todo el archivo, consultar USB o leer una
consola de video.

### Guard

Corrige o contiene una señal en tiempo real. Aquí vive el plugin FFGL.

Primera familia prevista:

- `Signal Guard`: rango, niveles, black level y gamma.
- `Banding Guard`: debanding y dithering controlado.
- `Temporal Guard`: estabilización de luminancia y deflicker.
- `Output Safe`: limitación o protección de flashes y valores extremos cuando
  sea técnicamente viable.

El primer FFGL será `MOSAIK IMAGO — Signal Guard`. Tendrá identidad por defecto
y bypass inmediato. Las correcciones se limitarán a un perfil conocido o a
parámetros manuales explícitos.

### Bridge

Conecta MOSAIK con otros sistemas sin procesar la imagen en el hilo de render.

Ejemplos:

- `XIO Bridge`: recibe monitoreo pasivo, OSC, Art-Net, sACN, timecode y eventos.
- `House Adapter`: normaliza información de un procesador o switcher.
- `Spout Bridge`: comparte frames en Windows cuando el flujo lo necesita.
- `OSC Bridge`: entrega estado a Resolume u otras herramientas.

El Bridge corre como proceso externo o en un hilo controlado fuera del render.
El FFGL carga un snapshot del perfil y no abre USB, red ni subprocesses durante
la llamada de dibujo.

### Record

Guarda evidencia y estadísticas. No tiene que ser un plugin de Resolume.

Incluye:

- perfil usado;
- configuración observada;
- frame time, FPS efectivo y eventos de lock;
- cambios de ruta o handoff;
- clips y hashes involucrados;
- advertencias y acciones tomadas;
- comparación entre soundcheck y show.

## Flujo de un show

```text
INSTAR
  media + sistema + composición
        ↓
NAYADE
  SOUNDCHEK + FIJO ↔ VJ ↔ CONSOLA ↔ destinos
        ↓
IMAGO
  Resolume + FFGL + perfil congelado
```

Las estadísticas, logs y perfiles finales se guardan como salida de cada
etapa. No habrá un plugin post-show separado en la primera arquitectura.

## Contratos compartidos

### Signal Profile

Un único esquema describe la señal, independientemente del fabricante:

```json
{
  "schema_version": "1.0",
  "source": {
    "resolution": "1920x1080",
    "fps": 60,
    "color_model": "RGB",
    "range": "full",
    "transfer": "sRGB",
    "primaries": "BT.709",
    "bit_depth": 8
  },
  "capture": {
    "resolution": null,
    "refresh_hz": null,
    "format": null,
    "lock": null
  },
  "house": {
    "input": null,
    "bus": null,
    "destinations": [],
    "outputs": []
  },
  "processor": {
    "vendor": "unknown",
    "model": "unknown",
    "read_only": true,
    "confidence": 0.0
  },
  "recommendation": {
    "range_transform": "identity",
    "gamma_transform": "identity",
    "deband": false,
    "deflicker": false
  }
}
```

El perfil debe distinguir siempre:

- **declared**: lo que dice el hardware;
- **observed**: lo que ve Windows, la GPU o una capturadora;
- **inferred**: hipótesis calculada por MOSAIK;
- **confidence**: confianza de cada dato.

### Capability profile

Los adaptadores de NovaStar, Colorlight, Barco, Analog Way u otros no deben
crear algoritmos nuevos. Sólo traducen su información al `Signal Profile` y
declaran sus capacidades:

```text
supports_read_only_query
supports_input_format
supports_output_routing
supports_gamma_read
supports_black_level_read
supports_telemetry
```

Si una capacidad no existe o no está verificada, se marca como `unknown` y se
mantiene el modo seguro.

## Cómo evitar duplicación y versiones incompatibles

1. **Un solo esquema de perfil** para Python, FFGL y XIO.
2. **Un solo conjunto de casos de prueba** con clips, rampas, flashes,
   degradados y cambios de escena.
3. **Un solo catálogo de transformaciones**: rango, gamma, LUT, deband y
   temporalidad; no una implementación diferente por fabricante.
4. **Adaptadores delgados**: el hardware sólo aporta datos normalizados.
5. **Una DLL FFGL con varias entradas**, si resulta compatible con el SDK, para
   compartir el núcleo sin duplicar binarios innecesariamente.
6. **Versionado por contrato**, no por copia: un plugin declara qué versión de
   `schema_version` y qué capacidades necesita.
7. **Fixtures sintéticos** para probar los algoritmos sin depender de un
   procesador real.
8. **Perfil congelado durante el show**: los cambios externos requieren una
   recarga explícita y nunca deben aparecer a mitad de un frame.

## Cómo se presentan a los colegas

La marca visible debe ser humana y técnica al mismo tiempo:

```text
MOSAIK IMAGO — Signal Guard
Corrige niveles, negros y gamma durante el show.
Host: Resolume / FFGL
Modo: seguro, reversible, sin conexión al procesador

MOSAIK NAYADE — Handoff Check
Verifica captura, routing, escala y destinos antes de salir.
Host: Windows / XIO / house video
Modo: sólo lectura
```

La web puede ordenar por etapa, pero cada ficha debe mostrar también:

- problema que resuelve;
- momento recomendado;
- entrada y salida;
- host requerido;
- hardware compatible;
- cambios que realiza;
- límites conocidos;
- evidencia de pruebas;
- versión de contrato;
- licencia.

Así una persona no necesita entender `IMAGO` para encontrar “corregir negros
lavados durante el show”.

## Primera implementación

### Paso 1: `MOSAIK INSTAR — Preflight`

Herramienta externa de pre-show:

- diagnostica media, codecs, resolución, FPS y alpha;
- prepara o valida DXV;
- registra estado de GPU, disco, memoria y temperatura;
- genera el perfil inicial de señal;
- prepara los fixtures y el reporte de soundcheck.

### Paso 2: `MOSAIK NAYADE — Handoff Check`

Herramienta externa de soundcheck, sólo lectura:

- captura la salida local de Windows/GPU;
- registra EDID, resolución, Hz y color space cuando estén disponibles;
- incorpora datos de XIO si hay telemetría;
- permite declarar input, bus y destinos cuando la consola no tiene API;
- genera `Signal Profile` y reporte;
- verifica si el problema es routing, canvas, escala, formato o color.

### Paso 3: `MOSAIK IMAGO — Signal Guard`

Plugin FFGL de Resolume:

- carga el perfil al iniciar;
- aplica sólo la transformación recomendada;
- ofrece bypass y control manual estándar del host;
- no escribe en la consola ni en el procesador;
- no depende de Python durante el render;
- comienza con rango/negros/gamma, dejando debanding y deflicker para módulos
  posteriores del mismo núcleo.

Los resultados estadísticos quedan como salida de `INSTAR`, `NAYADE` e `IMAGO`:

- comparan soundcheck y show;
- encuentran cambios de FPS, lock, rutas y frame time;
- miden si una corrección redujo el síntoma o sólo lo ocultó;
- proponen una nueva versión del perfil sin aplicarla automáticamente.

## Decisiones de seguridad

- El comportamiento por defecto es passthrough.
- No se cambia hardware de forma automática.
- No se escribe en USB, red, firmware, receiving cards ni mapping en el MVP.
- Los adaptadores desconocidos funcionan en modo manual y baja confianza.
- Un fallo de MOSAIK no debe impedir que Resolume emita la señal original.
- No se ejecutan procesos persistentes desde el plugin de render.
- Los perfiles y reportes registran fecha, versión, equipo y nivel de confianza.

## Resultado

La unidad de reutilización no será el plugin completo, sino:

```text
algoritmo + perfil + fixtures + reglas + adaptadores de host
```

El mismo conocimiento puede aparecer como CLI, herramienta de soundcheck,
plugin FFGL o puente XIO sin volver a programar la solución desde cero.
