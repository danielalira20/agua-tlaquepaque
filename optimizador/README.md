# Priorizador de pipas y cisternas

Carril de Jass (rol B). Decide, para cada fecha, **a dónde mandar los viajes de pipa**
con los recursos reales del municipio, y mide cuánto mejora eso frente al reparto actual.

**Lo que manda es `ESPECIFICACION.md`** (en preparación). Este README solo orienta.

## Qué lee y qué escribe

| | Archivo | Quién lo produce |
|---|---|---|
| Entrada | Estado por manzana y fecha (`contratos/estado.schema.json`) | Motor de Dani |
| Entrada | `datos/manzanas_centroides.csv` (ubicación de cada manzana) | Datos del equipo |
| Entrada | `datos/cisternas_tlaquepaque.csv` (cisternas del municipio) | Datos del equipo |
| Entrada | `supuestos.json` (recursos y parámetros) | Este carril |
| Salida | `salidas/plan.json` con la forma de `contratos/plan.schema.json` | Este carril |

`salidas/` no se versiona (está en `.gitignore`). Las tablas finales que cita el reporte
van en `resultados/`.

> `contratos/plan.schema.json` todavía es la versión del plan v1. Se actualiza en la rama
> `feat/plan-contrato`, junto con su fixture.

## Estructura

    README.md            este archivo
    ESPECIFICACION.md    reglas del priorizador y casos resueltos a mano (pendiente)
    supuestos.json       recursos y parámetros compartidos
    docs/decisiones/     una decisión por archivo: contexto, opciones, qué se decidió y por qué
    priorizador/         código: entradas, cobertura, asignación diaria, baseline
    analisis/            comparación baseline contra priorizado y sensibilidad
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
| Capacidad de cisterna comunitaria | pendiente | Ver `docs/decisiones/01-baseline-cisternas.md` |

200 L por hogar equivale a un día de consumo: 3.7 personas × 50 L ≈ 185 L.

## Reglas del carril

- Solo biblioteca estándar de Python, igual que `motor/`.
- Todo número sale de `supuestos.json` o de un archivo de datos; nada fijo en el código.
- Cuando cambia `contratos/plan.schema.json`, su fixture cambia en el mismo commit.
- Cada decisión de diseño queda en `docs/decisiones/` antes de programarla.

## Avance

| Rama | Qué entrega | Estado |
|---|---|---|
| `feat/priorizador-especificacion` | Esqueleto, supuestos, decisiones, `ESPECIFICACION.md` | En curso |
| `feat/plan-contrato` | `plan.schema.json` v2 y su fixture | Pendiente (coordinar con Dani) |
| `feat/priorizador-referencia` | Cobertura y asignación diaria, con pruebas | Pendiente |
| `feat/priorizador-baseline` | Reparto actual alrededor de las cisternas | Pendiente (decisión 01) |
| `feat/priorizador-comparador` | Baseline contra priorizado, sensibilidad | Pendiente |
| `feat/viabilidad-presupuestal` | Costo de un viaje de pipa, con fuente | Pendiente |

## Cómo correrlo

Pendiente: se completa con `feat/priorizador-referencia`.
