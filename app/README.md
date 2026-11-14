# Aguanta · app (carril de Migue)

Next.js estático + MapLibre + deck.gl (hexágonos H3) + Recharts.

    npm install
    npm run dev                          # http://localhost:3000
    npm run build                        # exporta a out/ (Vercel: Root Directory = app)
    node scripts/verifica-vectores.ts    # cruce del motor oficial contra el de referencia

## Datos

La app lee **solo** `public/datos/real/` (los exporta `python3 scripts/exporta_app.py` desde la raíz; ver su LEEME.md).
Python exporta los datos; el **motor oficial** (`src/lib/motor.ts`, implementa `motor/ESPECIFICACION.md`) corre en el
navegador para recalcular lo interactivo: consumo, `f`, horas efectivas y calendario (vigente u original).

Cruce con el motor de Python: los 4 conjuntos de `motor/vectores/vectores.json` (2,128 renglones) y todo `estado.json`
(34,097 renglones) coinciden exactamente.

## Páginas

- `/panal` — hexágonos H3 (res. 8) que agrupan las manzanas reales. Color: % de viviendas sin agua (cota mínima);
  altura: personas. Capa de marginación aparte, cisternas, propuestas, supuestos y advertencias.
- `/mi-casa` — calculadora por vivienda con el calendario vigente.
- `/pipas` — salida del priorizador (`plan.json`) contra el baseline estilizado, por cota mínima o máxima.
- `/datos` — vigente vs original, sensibilidad a consumo y `f`, riesgo por zona, tabla de equidad por marginación,
  colonias de mayor riesgo, método y fuentes.

Reglas que la app respeta: siempre mínimo y máximo; marginación fuera de la severidad; el baseline es estilizado;
`orden_eleccion` no es una ruta; las 5 advertencias de `meta.json` se muestran en Panal y Datos.
