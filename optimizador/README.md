# Priorizador de pipas y cisternas

Carril de Jass (rol B). Decide, para cada fecha, **a dónde mandar los viajes de pipa**
con los recursos reales del municipio, y mide cuánto mejora eso frente al reparto actual.

**Lo que manda es `ESPECIFICACION.md`** (versión 0.5, borrador). Este README solo orienta.

## Qué lee y qué escribe

| | Archivo | Quién lo produce |
|---|---|---|
| Entrada | Estado por manzana y fecha (`contratos/estado.schema.json`) | Motor de Dani |
| Entrada | `datos/manzanas_centroides.csv` (ubicación de cada manzana) | Datos del equipo |
| Entrada | `datos/manzanas_tlaquepaque.csv` (ocupantes por vivienda) | Datos del equipo |
| Entrada | `datos/cisternas_tlaquepaque.csv` (cisternas del municipio y del SIAPA) | Datos del equipo |
| Entrada | `supuestos.json` (recursos y parámetros) | Este carril |
| Salida | `salidas/plan.json` con la forma de `contratos/plan.schema.json` v2: priorizado y baseline, con cota mínima y máxima, y su comparación | Este carril |

`salidas/` no se versiona (está en `.gitignore`). Las tablas finales que cita el reporte
van en `resultados/`.

> `pruebas/test_salida.py` compara la salida contra `fixtures/plan.fixture.json`: si el
> contrato cambia, esa prueba avisa.

## Estructura

    README.md            este archivo
    ESPECIFICACION.md    reglas del priorizador y casos resueltos a mano
    supuestos.json       recursos y parámetros compartidos
    docs/decisiones/     una decisión por archivo: contexto, opciones, qué se decidió y por qué
    priorizador/         código: entradas, cobertura, asignación diaria, métricas y salida
    analisis/            comparación baseline contra priorizado y sensibilidad (pendiente)
    pruebas/             pruebas; casos/ tiene manzanas inventadas para los casos a mano
    resultados/          tablas y figuras finales (sí se versionan)

## Supuestos de recursos

| Parámetro | Valor | Fuente |
|---|---|---|
| Pipas | 32 | Prensa, octubre 2026 (ver `decisiones/propuesta-dani.md`, decisión 4) |
| Litros por viaje | 10,000 | Prensa |
| Litros por hogar | 200 | Prensa (~50 hogares por viaje) |
| Viajes por día | 63 | Prensa: 565 viajes en 9 días (62.8 al día) |
| Radio de cobertura | 300 m | Supuesto declarado; ver `docs/decisiones/03-radio-cobertura.md` |
| Cota para ordenar | mínima | Ver `docs/decisiones/02-cota-min-max.md` |
| Modo de racha | desempate | Ver `docs/decisiones/04-horizonte-dias.md` |
| Cisterna comunitaria | 1 viaje = 10,000 L | Supuesto; ver `docs/decisiones/01-baseline-cisternas.md` |
| Cisternas del baseline | todas (47) | Sensibilidad con las 35 de coordenada exacta |
| Turnos del baseline | todas | Sensibilidad con `con_necesidad` |

200 L por hogar equivale a un día de consumo: 3.7 personas × 50 L ≈ 185 L.

## Reglas del carril

- Solo biblioteca estándar de Python, igual que `motor/`.
- Todo número sale de `supuestos.json` o de un archivo de datos; nada fijo en el código.
- Cuando cambia `contratos/plan.schema.json`, su fixture cambia en el mismo commit.
- Cada decisión de diseño queda en `docs/decisiones/` antes de programarla.

## Avance

| Rama | Qué entrega | Estado |
|---|---|---|
| `feat/priorizador-especificacion` | Esqueleto, supuestos, decisiones, `ESPECIFICACION.md` | Hecho |
| `feat/plan-contrato` | `plan.schema.json` v2 y su fixture | Hecho por Dani, ya en `dev` |
| `feat/priorizador-referencia` | Cobertura, asignación diaria, métricas y `plan.json`, con pruebas | Hecho |
| `feat/priorizador-baseline` | Baseline estilizado por turnos entre las cisternas | En curso |
| `feat/priorizador-comparador` | Baseline contra priorizado, sensibilidad | Pendiente |
| `feat/viabilidad-presupuestal` | Costo de un viaje de pipa, con fuente | Pendiente |

## Cómo correrlo

Desde la raíz del repo, con el estado que produce el motor:

    python3 motor/referencia.py \
        --manzanas datos/manzanas_tlaquepaque.csv \
        --zonas datos/zonas_siapa/manzana_zona.csv \
        --calendario motor/calendarios/vigente-2026-11-03.json \
        --desde 2026-11-09 --hasta 2026-11-15 \
        --salida salidas/referencia.csv

    python3 -m optimizador.priorizador --estado salidas/referencia.csv

Escribe `salidas/plan.json` con las cuatro corridas (priorizado y baseline, cota mínima y
máxima) e imprime un resumen y la comparación. Para la sensibilidad, sin
tocar `supuestos.json`:

    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set modo_racha=peso
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set radio_cobertura_m=500

Cada corrida incluye el baseline estilizado. Sus variantes:

    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set baseline_turnos=con_necesidad
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set baseline_cisternas=exactas

`--detalle` imprime cada fecha de cada corrida.

Pruebas:

    python3 -m unittest discover -s optimizador/pruebas -t .
