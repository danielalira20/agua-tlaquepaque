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
