# Motor de autonomía

Calcula, para cada manzana y cada fecha, entre cuántas y cuántas viviendas se quedan
sin agua. **Lo que manda es `ESPECIFICACION.md`.**

    ESPECIFICACION.md      fórmulas, entradas, salidas y casos resueltos a mano
    supuestos.json         parámetros compartidos por las dos implementaciones
    calendarios/           esquema de racionamiento del SIAPA, con versión y fecha de consulta
    referencia.py          implementación de REFERENCIA (Python, solo biblioteca estándar)
    comparar.py            compara dos salidas renglón por renglón
    test_referencia.py     pruebas: los casos A a G y propiedades generales

## Dos implementaciones, un solo trabajo

| | Para qué | Dónde |
|---|---|---|
| **Oficial** | Alimenta la app, la demo y los números del reporte | TypeScript, en `app/` (pendiente de adaptar a la especificación) |
| **Referencia** | Verificar a la oficial. Atrapa errores de programación | `referencia.py` |

La coincidencia entre las dos **no valida los supuestos**, solo el código. Si el
viernes al mediodía no coinciden, gana la oficial y las diferencias se documentan.

## Uso

    python3 motor/test_referencia.py

    python3 motor/referencia.py \
        --manzanas datos/manzanas_tlaquepaque.csv \
        --zonas datos/zonas_siapa/manzana_zona.csv \
        --calendario motor/calendarios/vigente-2026-11-03.json \
        --desde 2026-11-09 --hasta 2026-11-15 \
        --salida salidas/referencia.csv

    python3 motor/comparar.py salidas/referencia.csv salidas/oficial.csv

Sensibilidad, sin tocar el archivo de supuestos:

    ... --set consumo_l_persona_dia=100 --set horas_efectivas_corte=36

## Vectores para el motor oficial en TypeScript

`motor/vectores/vectores.json` (lo genera `scripts/exporta_app.py`) trae entradas, supuestos y la salida esperada del motor de
referencia para cuatro conjuntos de supuestos, incluidas manzanas con varias zonas y fuera del programa. El motor de la app debe
reproducirlos: conteos de viviendas y horas, exactos. Los datos reales para la app están en
`app/public/datos/real/` (ver su `LEEME.md`).

## Qué falta

- La zona de cada manzana ya es real: `datos/zonas_siapa/manzana_zona.csv`. Los fixtures
  usan filas reales de ese archivo, no zonas inventadas.
- La implementación oficial hay que adaptarla: trabajar por manzana (no por colonia
  simulada), manejar los rangos mín–máx, y leer el calendario por fecha.
- Las 5 decisiones abiertas de la sección 10 de la especificación.
