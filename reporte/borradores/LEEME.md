# Borradores apartados

Esta carpeta guarda texto que **no entra al reporte tal como está**. No se borró para no perder el trabajo; se aparta hasta corregirlo.

## `CRITERIO_5_VIABILIDAD_PRESUPUESTAL_magui.md`

El Criterio 5 del reporte se redacta a partir de `optimizador/docs/viabilidad-presupuestal.md` (Jass), cuyas cifras salen de `optimizador/resultados/` y de `datos/evidencia.csv` y se regeneran con `python3 -m optimizador.analisis`.

Este borrador se aparta porque varias cifras no tienen fuente en el repo ni salen de ninguna corrida del modelo, y el reporte las presentaría como "verificadas":

| Cifra del borrador | Qué pasa |
|---|---|
| "~$60,000 MXN diarios" y "$5.4 millones en 90 días" | No aparece en ninguna fuente. El repo solo tiene el precio de una pipa **particular** (1,200 pesos; P012), que no es el costo del municipio |
| "Costo por viaje entre $800 y $1,200 (combustible, salario y amortización)" | La fuente (Milenio, P012) da precios de empresas privadas; no desglosa combustible ni salario. El municipio no publica su costo |
| "$45,000 MXN por cisterna instalada" y "$450,000 en total" | Sin cotización ni fuente |
| "Cada cisterna sustituye 1.8 viajes de pipa semanales" y "25 semanas de recuperación" | Sin fuente ni cálculo en el repo; el periodo de recuperación depende de las dos cifras anteriores |
| "Reduce más de 30% el kilometraje ocioso" | El modelo no calcula rutas ni kilómetros, solo qué cisternas reciben los viajes |
| "Entre 1.4× y 5.6× más viviendas protegidas" | La cifra es correcta **solo para el escenario base** (`optimizador/resultados/resumen.md`, tabla de viviendas-día atendidas). Falta decir que depende del baseline y de los supuestos: en las esquinas adversas de la sensibilidad la ventaja contra el baseline con necesidad baja a 1.2× o 1.1× (sección 3) |
| "32 camiones pipa", "63 viajes = 2 por pipa" | 32 pipas es la meta anunciada en octubre; 32 × 2 = 64, no 63 |

Lo que sí coincide con el repo: 22,050 viviendas-día en la semana (priorizado) y El Sauz con 11,889 personas y 2,950 viviendas sin almacenamiento (`datos/contraste_cisternas_programa.csv`).

Si Magui quiere conservar la parte de cisternas comunitarias (payback), necesita una cotización o fuente para el costo por cisterna y para los viajes que sustituye, y declararlo como estimación.
