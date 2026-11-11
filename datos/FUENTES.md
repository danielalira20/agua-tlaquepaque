# Procedencia de los datos

Esta tabla alimenta directamente la indicación 3 del kit: nombre, institución, año,
cobertura, qué se tomó y para qué.

## `manzanas_tlaquepaque.csv` y `manzanas_tlaquepaque.geojson`

| Campo | Valor |
|---|---|
| **Dataset del catálogo** | 01 — Inventario de viviendas y servicios básicos por AGEB |
| **Nombre exacto** | Principales resultados por AGEB y manzana urbana, Censo de Población y Vivienda 2020 |
| **Institución** | INEGI |
| **Año** | 2020 (publicado 2021) |
| **Cobertura** | Manzana urbana, entidad 14 Jalisco, recortado al municipio 098 San Pedro Tlaquepaque |
| **Qué se tomó** | POBTOT, TVIVHAB, PROM_OCUP, VPH_AGUADV, VPH_AGUAFV, VPH_TINACO, VPH_CISTER, VPH_DRENAJ |
| **Para qué** | Describir el problema y alimentar el motor de autonomía |

**Geometría:**

| Campo | Valor |
|---|---|
| **Producto** | Marco Geoestadístico 2020, capa de manzanas (`14m`) |
| **Institución** | INEGI |
| **CRS original** | MEXICO_ITRF_2008_LCC (Lambert Conformal Conic) |
| **CRS de salida** | EPSG:4326 |
| **Llave de unión** | `CVEGEO`, 16 caracteres: entidad + municipio + localidad + AGEB + manzana |

**Cobertura del cruce:** 4,863 de 4,871 manzanas del censo quedaron con polígono
(99.8%), equivalentes a 587,874 de 588,419 personas (99.9%). Ocho manzanas del
censo no tienen polígono en el Marco Geoestadístico.

**Procesamiento aplicado:** simplificación de 2 metros con preservación de
topología, coordenadas redondeadas a 6 decimales, y cálculo de área y centroide en
el CRS proyectado antes de reproyectar. El archivo resultante pesa 3.3 MB.

## `manzanas_centroides.csv`

Los mismos atributos sin geometría, más `lon`, `lat` y `area_m2`. Sirve para
calcular el radio de cobertura de las pipas sin cargar los polígonos.

---

## `manzana_colonia.csv` y `colonias_tlaquepaque.csv`

**El puente que faltaba.** El calendario de tandeo viene por **colonia** y el censo
viene por **manzana**, y el INEGI no publica colonias. Sin este cruce, el calendario
no se puede unir con el modelo y el motor se queda sin insumo.

| Campo | Valor |
|---|---|
| **Producto** | Información Sociodemográfica por colonia, Jalisco 2020. Colonias INE 2024 |
| **Institución** | IIEG Jalisco |
| **Cobertura** | 6,624 colonias en Jalisco; 276 en San Pedro Tlaquepaque |
| **CRS original** | EPSG:32613 (UTM 13N) |
| **Método** | Unión espacial: el centroide de cada manzana cae dentro de un polígono de colonia |

**Cobertura del cruce:** 4,841 de 4,863 manzanas quedaron con colonia (99.5%),
equivalentes a 585,921 de 587,874 personas (99.7%). Se alcanzaron 218 de las 276
colonias; las 58 restantes no tienen manzanas urbanas con datos del censo.

**Archivos:**

- `manzana_colonia.csv` — una fila por manzana: `cvegeo`, `geocol`, `colonia`, `cp`
- `colonias_tlaquepaque.csv` — una fila por colonia, con su población, viviendas,
  número de manzanas, total sin almacenamiento y el nombre normalizado

> **Advertencia del propio IIEG:** la capa se construyó con el marco de colonias del
> INE, y el instituto señala que no puede asegurarse que sea equivalente a la capa de
> colonias que usan en la práctica los municipios. Hay que declararlo en el reporte.

### El problema de los nombres, y cómo se resuelve

Los nombres del calendario no empatan textualmente con los de la capa. De diez
nombres de prueba, tres fallaron:

| En el calendario | En la capa |
|---|---|
| Barrio de Santiago | De Santiago |
| Villas El Tapatio | Villas del Tapatío |
| Tateposco | Real de Tateposco (por confirmar) |

Para eso está **`scripts/match_colonias.py`**. Normaliza acentos, mayúsculas y
palabras de ruido ("col", "fracc", "barrio", "infonavit"), y clasifica cada nombre
en `exacto`, `probable`, `revisar` o `sin_match`.

```
python3 scripts/match_colonias.py nombres_del_calendario.txt > cruce.csv
```

**Todo lo que salga como `revisar` o `sin_match` se revisa a mano.** El script
acota el trabajo, no lo sustituye.

> **Actualización (zonas del SIAPA).** El SIAPA no raciona por colonia sino por **zona
> (1 a 7)**, y esa zona sí se usa en el motor. Este cruce manzana → colonia sigue
> sirviendo para nombrar y reportar, pero la zona de cada manzana sale de
> `zonas_siapa/` (siguiente sección), que no depende de esta capa de colonias del IIEG.

## `zonas_siapa/` y `../motor/calendarios/`

| Campo | Valor |
|---|---|
| **Fuente 1: polígonos** | Portal oficial `rotaciondeserviciosiapa.jalisco.gob.mx`, archivo `/geo/rotacion-siapa.topo.json`: 2,303 polígonos de colonias, cada uno con una zona calculada por "cruce original del mapa", y 7 polígonos de zona |
| **Fuente 2: lista** | `lista_oficial_colonias.csv`: colonias por zona del documento oficial del SIAPA (661 filas, 115 de Tlaquepaque). Documento oficial: `zonas_siapa/colonias_siapa.pdf` (`/pdf/colonias_siapa.pdf` del portal, descargado el 11-nov-2026). El archivo del equipo se verificó contra el PDF: las 115 colonias de Tlaquepaque coinciden en nombre y zona |
| **Fuente 3: calendarios** | Portal, `/api/ajustes.php` (vigente, 3-nov-2026) y `/data/colonias-ajustes.json` (original, 15-oct-2026) |
| **Institución** | SIAPA / Gobierno de Jalisco |
| **Consultado** | 11-nov-2026 |
| **Para qué** | Saber qué días racionan a cada manzana: une el Censo con el calendario |

El método, la regla de cruce, los niveles de confianza y lo que queda por revisar están
en `zonas_siapa/LEEME.md`. El resultado es `zonas_siapa/manzana_zona.csv`.

**Cobertura del programa: se reporta como rango.** 462,194 personas (78.6% de
Tlaquepaque) viven en manzanas con zona; 368,111 (62.6%) tienen respaldo de la lista
oficial y 94,083 (16.0%) dependen solo del portal.

## `cisternas_tlaquepaque.csv` y `contraste_cisternas.csv`

| Campo | Valor |
|---|---|
| **Fuente** | Mapa público "CISTERNAS TLAQUEPAQUE PUB", Google My Maps |
| **Institución** | Gobierno de San Pedro Tlaquepaque |
| **Año** | 2026 |
| **Qué se tomó** | Ubicación y domicilio de cisternas comunitarias, puntos del SIAPA y 10 ubicaciones propuestas |
| **Para qué** | Contrastar el modelo contra decisiones reales del municipio. Es la evidencia propia que sustituye a la encuesta |

**Capas del mapa:** `MUNICIPAL 1.kmz` (59 placemarks, cisternas del municipio),
`SIAPA.kmz` (3), `PROPUESTAS` (10), más dos capas de polígonos que no se usaron
(`SIAPA TLQ` con 8 y `DIVISIÓN TERRITORIAL TLQ` con 233 secciones del INE).

**Procesamiento:** se descargó el KML, se eliminaron 12 duplicados exactos, se
recuperó la colonia desde el domicilio postal para las 14 cisternas sin
coordenada, y se ubicaron por unión espacial las que sí la tienen. Quedaron 47
cisternas ubicadas de 50, y 3 sin resolver que están declaradas.

Los resultados del contraste están en `HALLAZGOS_cisternas.md`.

## ⚠️ Advertencia sobre dos campos derivados

`litros_almacen_est` y `horas_autonomia_50Lpd` **son indicativos y no deben usarse
tal cual en el motor.**

Están calculados sumando el almacenamiento de toda la manzana y dividiendo entre su
población total. Eso supone, sin decirlo, que **el agua se comparte entre viviendas**,
y esa suposición contradice la tesis del proyecto: una vivienda sin tinaco no puede
usar el tinaco de su vecino.

El efecto es visible. La manzana `1409800012610023` tiene 29 tinacos y 22 cisternas
para 113 personas, y el campo le asigna 602 horas de autonomía, es decir 25 días.
Ninguna vivienda de esa manzana aguanta 25 días.

**Lo que el motor sí debe usar** son los insumos crudos, que están completos y
correctos:

    viviendas, viv_tinaco, viv_cisterna, pob, ocupantes_prom

y calcular la autonomía **por estrato de vivienda dentro de la manzana**:

| Estrato | Litros disponibles |
|---|---|
| Con tinaco y cisterna | capacidad de ambos |
| Solo tinaco | capacidad del tinaco |
| Solo cisterna | capacidad de la cisterna |
| Sin almacenamiento | cero: se queda sin agua al momento del corte |

El resultado por manzana no es un número de horas, sino **qué proporción de sus
viviendas se queda sin agua en cada día del ciclo**. Esa es justo la distinción que
hace distinto a este proyecto, y perderla en un promedio la anularía.

**Nota sobre el traslape:** el censo no cruza tinaco con cisterna, así que el tamaño
de cada estrato solo se conoce en rango. Por eso `sin_almacen_min` y
`sin_almacen_max` vienen como cotas y no como un dato único.

## Supuestos de capacidad, pendientes de decidir

| Supuesto | Valor usado | Estado |
|---|---|---|
| Capacidad de tinaco | 1,100 L | Tamaño residencial común. Sin fuente citada aún |
| Capacidad de cisterna | 5,000 L | **Estimado, sin fuente. Probablemente generoso** |
| Consumo por persona | 50 L/día | Nivel básico OMS. Reportar también a 100 |
