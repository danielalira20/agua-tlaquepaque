# Aguanta · app (carril de Migue)

Next.js estático + MapLibre + deck.gl (hexágonos H3) + Recharts. Un hexágono representa una colonia.

    npm install
    npm run datos     # regenera public/datos/*.json (SIMULADOS, con la forma de los contratos)
    npm run dev       # http://localhost:3000
    npm run build     # exporta a out/ (listo para Vercel o cualquier hosting estático)

Datos reales (manzanas, estado, calendarios, cisternas y plan): `public/datos/real/`, ver su `LEEME.md`. Se regeneran con `python3 scripts/exporta_app.py`; los simulados siguen en `public/datos/` hasta que la app cambie.

Páginas: `/` inicio · `/panal` mapa por fecha · `/mi-casa` calculadora por vivienda · `/pipas` priorizador del día · `/datos` gráficas, método, datasets y supuestos.

Lógica del modelo en `src/lib/modelo.ts`: autonomía por estrato de vivienda (sin almacenamiento / tinaco / cisterna), nunca promediando la colonia; calendario por fecha y zona; priorizador glotón. Cuando lleguen `estado.parquet` y `plan.json` reales, se reemplaza lo que genera `scripts/genera-datos.mjs`.
