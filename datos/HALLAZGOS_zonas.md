# Hallazgos con la zona real de cada manzana

Se regenera con `python3 scripts/recalcular_hallazgos.py`. Reemplaza las cifras
provisionales que salieron de cruzar solo con los polígonos del portal.

Fuentes y método de las zonas: `zonas_siapa/LEEME.md`. Todo lo de abajo hereda su
advertencia principal: **las dos fuentes de zonas no coinciden del todo, y por eso la
cobertura del programa es un rango.**

## 1. Cuánta gente recibe racionamiento: un rango, no un número

Base: 4,863 manzanas con geometría, 587,874 personas.

| | Personas | % |
|---|---:|---:|
| Dentro del programa de racionamiento | 462,194 | 78.6% |
| …con respaldo de la lista oficial (alta + media + conflicto) | 368,111 | 62.6% |
| …solo por el polígono del portal (la colonia no está en la lista) | 94,083 | 16.0% |
| Fuera del programa según las dos fuentes | 123,777 + 1,903 sin polígono | 21.4% |

**Se reporta entre 63% y 79%.** La cifra anterior de 76% (444,443 personas) era solo de
polígonos y no debe usarse.

## 2. Dónde está el riesgo

Viviendas sin tinaco ni cisterna **dentro del programa**: **17,420** (cota mínima) a
**34,429** (cota máxima). El Censo no cruza tinaco con cisterna, por eso es un rango.

| Zonas | Manzanas | Personas | Sin almacenamiento (mín) | Sin almacenamiento (máx) | % del riesgo (mín) |
|---|---:|---:|---:|---:|---:|
| 5 y 6 | 1,714 | 214,177 | **12,642** | 21,699 | **72.6%** |
| 3 y 4 | 2,004 | 244,296 | 4,371 | 12,195 | 25.1% |
| Mixtas | 43 | 3,721 | 407 | 535 | 2.3% |

Por zona y por respaldo de la fuente (cota mínima):

| Zona | Con lista oficial | Solo portal |
|---|---:|---:|
| 6 | 5,023 | 1,631 |
| 5 | 5,197 | 376 |
| 4 | 1,933 | 535 |
| 3 | 1,844 | 50 |
| 5,6 | 379 | 36 |
| 3,5 | 0 | 314 |
| 4,6 | 93 | 0 |
| 3,4 | 9 | 0 |

**La conclusión se sostiene:** casi tres cuartas partes del riesgo (con la cota mínima; **63.0% con la máxima**,
21,699 de 34,429) están en las zonas 5 y 6 con cualquiera de las dos fuentes. Con solo la lista oficial, las zonas 5 y 6 tienen
10,599 de las 14,478 viviendas respaldadas (73.2%); el portal suma 2,942 viviendas más
(2,043 de ellas en zonas 5 y 6), para un total de 17,420 y 72.6%.
`riesgo_por_zona.csv` trae el detalle completo. Ojo: es el riesgo de **almacenamiento** (Censo), que no depende de
ningún supuesto. Las viviendas **sin agua del motor** sí dependen del consumo y del tinaco: con los supuestos de la
decisión 1 las zonas 5 y 6 tienen en promedio 59.8% (nunca menos de 52.6% en esos sorteos). Ver `HALLAZGOS_sensibilidad.md`.

## 3. Contraste con las cisternas del municipio, restringido al programa

El contraste original comparaba contra todas las colonias, hubiera o no racionamiento.
Una cisterna en una colonia que el SIAPA no raciona no se explica por el calendario, así
que se repite el contraste solo con el riesgo **dentro del programa**.

| Rank mediano de riesgo | Con cisterna | Sin cisterna |
|---|---:|---:|
| Todas las colonias (237) | 62 | 125 |
| Solo riesgo dentro del programa (107 colonias) | **37** (28 colonias) | **59** (79) |
| Solo riesgo con respaldo de la lista (69 colonias) | **24** (24) | **38** (45) |

El resultado se mantiene con las tres bases: las colonias con cisterna están, en
mediana, en mejor posición de riesgo que las que no la tienen.

**De las 20 colonias de mayor riesgo dentro del programa, 9 tienen cisterna y 11 no.**
El Sauz sigue siendo la primera (2,950 de 3,546 viviendas), sin cisterna y sin propuesta.

**Cuatro de las quince primeras dependen solo del portal:** Parques del Bosque,
Geo Villas Los Olivos III, Miraflores y Miravalle. Hay que decirlo cuando se citen.

### Algo que cambia la lectura anterior

Cinco colonias de las 30 de mayor riesgo por almacenamiento **no reciben racionamiento
según ninguna de las dos fuentes**:

| Colonia | Rank (todo el municipio) | Personas | Sin almacenamiento | Cisternas |
|---|---:|---:|---:|---:|
| Parques de La Victoria | 3 | 5,305 | 1,198 | **1** |
| Parques del Palmar | 6 | 3,597 | 854 | 0 |
| Paseos del Prado | 13 | 2,955 | 530 | 0 |
| Artesanos | 24 | 5,536 | 189 | 0 |
| Felipe Ángeles | 25 | 4,263 | 184 | 1 |

Antes se hablaba de tres colonias fuera (La Victoria, Palmar y Paseos del Prado); con las 30
primeras salen cinco. Dos lecturas, y hay que decidir cuál contar:

- **El riesgo por almacenamiento no es lo mismo que el riesgo por racionamiento.** Estas
  colonias tienen poca capacidad pero, si de verdad no las raciona el SIAPA, no se quedan
  sin agua por el calendario.
- **O el programa abarca más que la lista.** Se verificó que el PDF oficial no nombra a estas colonias
  (ni a Parques del Bosque ni a Geo Villas), y que el archivo del equipo es
  fiel al PDF. Parques de La Victoria tiene cisterna municipal pese a estar fuera del programa:
  el municipio la puso por otro motivo o el programa la incluye sin nombrarla.

### Propuestas de cisterna

De las 10 ubicaciones propuestas, 7 están en colonias dentro del programa con riesgo
(Nueva Santa María, rank 15; Lomas del Cuatro, 32; Los Santibáñez, 39; El Órgano, 42;
Lomas del Tapatío, 55; Los Puestos, 59; Santa María, 86) y 3 en colonias sin riesgo
registrado dentro del programa (otra Santa María con 0 viviendas sin almacenamiento,
Jardines de San Martín con 8.9% de su población en el programa, Canal 58 con 0%).
Ninguna está en las 14 primeras.

## 4. El motor, una semana (9 al 15 de noviembre de 2026)

Personas-día sin agua, sumando las 7 fechas. Cota mínima a cota máxima.

| Escenario | Mín | Máx |
|---|---:|---:|
| **Calendario vigente (3-nov), 50 L, f = 0** | **210,116** | **490,320** |
| Calendario original (15-oct) | 138,992 | 321,280 |
| 100 L/persona/día | 457,643 | 690,917 |
| 150 L/persona/día | 661,437 | 863,585 |
| 50 L, f = 0.25 | 208,426 | 489,369 |
| 50 L, f = 0.5 | 208,426 | 489,369 |
| 100 L, f = 0.25 | 310,684 | 565,382 |
| 100 L, f = 0.5 | 210,116 | 490,320 |
| 150 L, f = 0.25 | 512,353 | 739,185 |
| 150 L, f = 0.5 | 310,684 | 565,382 |
| Horas efectivas 36 | 219,821 | 496,422 |
| Horas efectivas 48 | 247,540 | 516,185 |

Cómo leerlo:

1. **El cambio del 3 de noviembre pesa:** el calendario vigente deja 1.5 veces más
   personas-día sin agua que el original (210,116 contra 138,992 en la cota mínima).
2. **A 50 L/persona/día, el resultado casi no depende de `f`.** Con ese consumo y 4
   ocupantes un tinaco aguanta 132 h, más que cualquier racionamiento del calendario, así
   que se quedan sin agua casi solo las viviendas sin almacenamiento, y esas se quedan sin
   agua mientras `f < 1`.
3. **Lo que sí mueve el resultado es el consumo.** A 100 L/persona/día el número se
   multiplica por 2.2 y a 150 por 3.1. La elección de 50 L debe justificarse y la
   sensibilidad va en el reporte.
4. **Un chequeo interno:** 100 L con `f = 0.5` da exactamente lo mismo que 50 L con
   `f = 0` (210,116), como dice la especificación: solo importa el consumo neto
   `c × (1 − f)`.
5. El rango entre mínimo y máximo (210,116 a 490,320) es la incertidumbre del Censo
   sobre cuántas viviendas tienen tinaco *y* cisterna. No se achica sin otro dato.

## 5. Lo que sigue sin saberse

1. Si las colonias que el PDF oficial no nombra pero el mapa sí ubica en una zona (el 16% `baja`)
   reciben racionamiento. La lista ya está verificada contra el PDF; esto solo lo responde el SIAPA.
2. Si los polígonos sin zona que comparten nombre con colonias de otro municipio (ver
   `zonas_siapa/pendientes_revision.csv`) son la misma colonia.
3. Si un día de racionamiento es cero agua o baja de presión (`f`).
4. Hasta cuándo rige el calendario vigente. El portal dice que se podrá ajustar.
