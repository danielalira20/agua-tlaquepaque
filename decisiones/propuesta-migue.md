# Propuesta de Migue — las 4 decisiones de Fase 0

Voto a favor de la propuesta de Dani en las 4 decisiones. Este documento agrega lo
que encontré al correr los datos reales de `datos/manzanas_tlaquepaque.csv` y lo que
hay que corregir en los contratos antes de programar.

Todas las cifras de abajo se pueden reproducir con el script del final.

---

## 🔴 Hallazgo 1 · Con este calendario, el promedio por manzana sale casi todo verde

### Lo que dicen los datos

| Dato | Valor |
|---|---|
| Mediana de `horas_autonomia_50Lpd` | **324 h (≈13 días)** |
| Manzanas con más de 7 días de autonomía | **3,907 de 4,871 (80%)** |
| Manzanas con menos de 24 h | **80** |
| Manzanas con menos de 48 h | **155** |

Y el calendario: la zona 3 suspende **miércoles y sábado**, la zona 4 **lunes y
jueves**. Ninguna zona pasa más de **1 día seguido** sin servicio.

### Por qué importa

1. **El umbral U = 48 h casi nunca se activa.** La propuesta de Dani lo justifica con
   "el intervalo típico de 3 días", pero este calendario no tiene intervalos de 3
   días: el tinaco se rellena al día siguiente. Con U = 48 h, `agua_guardada` sale
   vacío en casi todo el mapa.
2. **El promedio por manzana esconde la tesis.** `horas_autonomia_50Lpd` reparte los
   litros de las casas con cisterna entre todas las de la manzana. Si la mitad tiene
   cisterna de 5,000 L, la manzana "aguanta 10 días" y la otra mitad, que no tiene
   nada, desaparece. Hay **279 manzanas** con al menos 20% de viviendas sin
   almacenamiento que salen con más de 7 días de autonomía; ahí quedan escondidas
   **al menos 10,348 personas**.

Nuestra tesis es "el mismo corte, dos realidades". El cálculo actual las mezcla en
una sola.

### Propuesta

**Separar cada manzana en dos grupos en lugar de promediar:**

| Grupo | Cuántas personas | Qué le pasa |
|---|---|---|
| Sin almacenamiento | `pob × pct_sin_almacen` (rango min–max) | Se queda sin agua **cada día de suspensión** |
| Con almacenamiento | El resto | Aguanta; su riesgo es el agua guardada |

En todo Tlaquepaque eso da **entre 77,639 y 157,349 personas sin almacenamiento**.

**Métrica central:** `personas sin respaldo × días de suspensión por semana`. Sale
directo del Censo y del calendario, sin supuestos de litros, y se defiende sola.
Los litros (1,100 / 5,000 L) solo afectan al grupo con almacenamiento.

**Parámetro nuevo: `horas_efectivas_corte`** (24 / 36 / 48 h, en configuración,
igual que U). La red tarda horas en recuperar presión, así que un día de suspensión
dura más de 24 h en la llave. Sin este parámetro, U nunca se cruza; con él, el
análisis de sensibilidad tiene algo que mover. Se declara como supuesto.

---

## 🔴 Hallazgo 2 · Sigue sin resolverse el cruce manzana → colonia → zona

`sector_tandeo` dice "PENDIENTE" en `manzanas.schema.json` y
`calendario_tlaquepaque.json` tiene 10 colonias de las ~111. El Censo no trae
colonia, así que sin una capa de polígonos de colonias el motor no sabe qué día le
toca agua a cada manzana.

- **Plan A:** capa de colonias (IIEG, municipio o datos abiertos) y cruce espacial
  con los centroides de las manzanas.
- **Plan B (si no aparece la capa el miércoles):** asignar zona por AGEB, usando la
  colonia mayoritaria de cada AGEB. Se declara como aproximación.

Es el bloqueo más importante del proyecto y hoy no tiene dueño ni fecha.

---

## 🟡 Hallazgo 3 · Inconsistencias en el repo

| Dónde | Qué está mal | Arreglo |
|---|---|---|
| Todos los contratos | `cvegeo` dice `string(13)`; el dato real tiene **16 caracteres** (`140980001338A013`) | Cambiar a `string(16)` |
| `estado.schema.json` y su fixture | Siguen con `fuente_riesgosa` | Aplicar la escalera de la opción C |
| `plan.schema.json` | Sigue con `calendario_optimizado` (reordenar el tandeo del SIAPA, que ya quitamos) y asigna por `cvegeo` | Aplicar la opción C de Dani (punto de entrega) |
| `mediciones.schema.json` y su fixture | Siguen siendo la encuesta | Renombrar a `evidencia` |
| `README.md`, `manzanas.schema.json`, tabla de supuestos | Dicen "calibrar con la encuesta" y "pregunta 3" | Cambiar por "análisis de sensibilidad" |
| `README.md` | Habla de "en qué hora del ciclo" y de la cadena red → tinaco → llave | Alinear con día y con el reenfoque |
| Delimitación | "Al menos 58,938 personas" es solo la cota baja | Escribir **"entre 58,938 y 92,069 personas"** (manzanas con más de la mitad sin almacenamiento, cota min y max) |
| Cobertura | No dice cuántas manzanas faltan | Declarar que las 4,871 manzanas son las que el INEGI no enmascaró y suman **588,419 personas** |

Recordatorio de la regla del repo: cada contrato se cambia **junto con su fixture**,
en el mismo commit.

---

## Mi voto en las 4 decisiones

| # | Decisión | Voto | Comentario |
|---|---|---|---|
| 1 | Cancelar encuesta; contraste con 60 cisternas + sensibilidad | ✅ A favor | Falta conseguir las **coordenadas** de las 60 cisternas del mapa del municipio. Hay que asignarle dueño, porque puede costar trabajo extraerlas |
| 2 | Escalera de estados (opción C), U = 48 h | ✅ A favor, con ajuste | Agregar los dos grupos por manzana y `horas_efectivas_corte` (Hallazgo 1). Sin eso, `agua_guardada` sale vacío |
| 3 | Día en el contrato, horas en el cálculo | ✅ A favor | Encaja con el mapa: selector de 7 días, ~34 mil renglones, carga instantánea |
| 4 | Punto de entrega, con `propuesta_cisternas` | ✅ A favor | Para que dé tiempo: algoritmo **glotón** (elegir el punto que cubre más personas en riesgo, repetir hasta agotar viajes) en vez de optimización formal. Se puede mejorar después si sobra tiempo |

---

## Lo que necesita la app (carril de Migue)

Para que el mapa y el panel lateral funcionen, `estado` debería traer además:

- `personas_sin_respaldo_min` y `personas_sin_respaldo_max`
- `zona` y `colonia`

Y un archivo de geometría (`manzanas.geojson` o centroides lat/lon por `cvegeo`). La
app agrupa en hexágonos H3 para la vista general y muestra colonia y manzanas al dar
clic.

---

## Cómo reproducir las cifras

```bash
python3 - <<'EOF'
import pandas as pd
d = pd.read_csv('datos/manzanas_tlaquepaque.csv', dtype={'cvegeo': str})
h = d.horas_autonomia_50Lpd
print('cvegeo largo:', d.cvegeo.str.len().unique())
print('mediana autonomia h:', h.median())
print('<24h:', (h < 24).sum(), ' <48h:', (h < 48).sum(), ' >168h:', (h > 168).sum())
print('pob total:', d.pob.sum())
print('pob en mzas >50% sin almacen (min, max):',
      d.loc[d.pct_sin_almacen_min > 50, 'pob'].sum(),
      d.loc[d.pct_sin_almacen_max > 50, 'pob'].sum())
print('personas sin almacen (min, max):',
      round((d.pob * d.pct_sin_almacen_min / 100).sum()),
      round((d.pob * d.pct_sin_almacen_max / 100).sum()))
mix = (d.pct_sin_almacen_min >= 20) & (h > 168)
print('mzas mixtas escondidas:', mix.sum(),
      ' personas:', round((d.pob * d.pct_sin_almacen_min / 100)[mix].sum()))
EOF
```
