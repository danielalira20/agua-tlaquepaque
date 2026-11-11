# Contraste: las cisternas del municipio contra el modelo

Esta es la evidencia propia que sustituye a la encuesta cancelada. En vez de
preguntarle a unas cuantas personas qué opinan, contrastamos el modelo contra
**decisiones que el municipio ya tomó con presupuesto y camiones.**

**Fuente:** mapa público "CISTERNAS TLAQUEPAQUE PUB", publicado por el Gobierno de
San Pedro Tlaquepaque en Google My Maps.

## La pregunta

> ¿Las cisternas que el municipio ya colocó coinciden con donde el modelo dice que
> está el riesgo?

Las dos respuestas posibles son un resultado: si coinciden, el modelo reproduce el
juicio de quien opera el sistema; si no, señala lo que falta.

## Actualización con las zonas reales del SIAPA

Esta versión original comparaba contra **todas** las colonias. Ya con la zona de cada
manzana (`zonas_siapa/`), el contraste se repitió dejando solo el riesgo que está
**dentro del programa de racionamiento**. Las cifras y el método están en
`HALLAZGOS_zonas.md`, sección 3; el detalle por colonia en `contraste_cisternas_programa.csv`.

| | Antes (237 colonias) | Solo dentro del programa (107) | Solo con respaldo de la lista oficial (69) |
|---|---:|---:|---:|
| Rank mediano **con** cisterna | 62 | 37 | 24 |
| Rank mediano **sin** cisterna | 125 | 59 | 38 |
| De las 20 de mayor riesgo, con cisterna / sin | 8 / 12 | 9 / 11 | — |

**La conclusión 1 se mantiene con las tres bases. La 2 también:** El Sauz sigue siendo
la primera, sin cisterna ni propuesta. Cambia una cosa: cinco colonias de las 30 de mayor
riesgo por almacenamiento no reciben racionamiento según las dos fuentes (entre ellas
Parques de La Victoria, que sí tiene cisterna municipal). Y cuatro de las quince primeras
dependen solo del polígono del portal. La tabla de abajo es la versión sobre todo el
municipio y se conserva por transparencia.

## Resultado: coinciden en lo general, y discrepan en lo específico

**1. El municipio sí está siguiendo el gradiente de riesgo.**

| | Rank mediano de riesgo |
|---|---|
| Colonias **con** cisterna | **62** |
| Colonias **sin** cisterna | **125** |

De 237 colonias con datos del censo, donde 1 es la de mayor riesgo. Las colonias
que recibieron cisterna están, en mediana, al doble de riesgo que las que no.
**El modelo coincide con el criterio del municipio.** Es consistente con él, no una
prueba de que ambos estén bien (ver limitación 7), pero sin que nadie haya tenido que
responder una encuesta.

**2. Pero doce de las veinte colonias de mayor riesgo no tienen ninguna.**

De las 20 colonias con más viviendas sin almacenamiento, 8 tienen cisterna y
**12 no**.

| Colonia | Población | Viviendas | Sin almacenamiento | Cisternas | Propuestas |
|---|---:|---:|---:|---:|---:|
| **El Sauz** | 11,889 | 3,546 | **2,950** | **0** | **0** |
| Villa Fontana | 8,163 | 2,510 | 1,298 | 1 | 0 |
| Parques de La Victoria | 5,305 | 1,487 | 1,198 | 1 | 0 |
| Fovissste Miravalle | 7,733 | 2,190 | 1,168 | 2 | 0 |
| **Balcones de Santa María** | 6,211 | 2,150 | **980** | **0** | **0** |
| **Parques del Palmar** | 3,597 | 1,182 | **854** | **0** | **0** |
| **Parques de Sta. Cruz del Valle** | 6,888 | 2,004 | **818** | **0** | **0** |
| **San Martin de Las Flores de Abajo** | 10,017 | 2,391 | **700** | **0** | **0** |

**El Sauz es el hallazgo.** Es la colonia número uno en riesgo de todo el
municipio: 2,950 de sus 3,546 viviendas, el 83%, no tienen tinaco ni cisterna.
Ahí viven 11,889 personas. **No tiene ninguna cisterna, y tampoco está entre las
diez que el municipio propuso.**

**3. Las diez propuestas nuevas no siguen el gradiente.**

El mapa incluye una capa de 10 ubicaciones propuestas. Su rank mediano de riesgo
es **76 de 237**, y ninguna está entre las quince colonias de mayor riesgo.

| Propuesta | Colonia | Rank | Viviendas sin almacenamiento |
|---|---|---:|---:|
| Calle Sta Mónica 11 | Nueva Santa María | 18 | 261 |
| José Bañales & Mezquite | Lomas del Cuatro | 39 | 111 |
| Hilario Reyes 16 | Los Santibáñez | 49 | 84 |
| ... | ... | ... | ... |
| Santos Degollado & Matamoros | Santa María | 144 | **0** |

La última propuesta está en una colonia donde el censo no registra **ninguna**
vivienda sin almacenamiento.

## Lo que esto le da al proyecto

No es un mapa de quejas ni una opinión: es una comparación contra decisiones
reales. Y el mensaje para el municipio no acusa a nadie, porque **la primera
conclusión le da la razón**: su criterio actual sí apunta al riesgo. Lo que
aporta la herramienta es la segunda parte, que es ordenar lo que sigue.

## Limitaciones, declaradas

1. **El mapa puede estar incompleto o desactualizado.** La prensa reporta 60
   cisternas; del mapa salen 50 registros únicos de cisterna tras eliminar
   duplicados. No sabemos si faltan o si la prensa contó distinto.
2. **14 de las 50 cisternas no traen coordenada.** Se ubicaron a nivel de colonia
   a partir del domicilio postal del propio mapa. Por eso **todo el contraste se
   hace a nivel colonia, no a nivel manzana.**
3. **Tres cisternas no se pudieron ubicar** (CIST014, CIST021, CIST022) por falta
   de datos suficientes. CIST022 venía con coordenadas (-180, 90), que son un valor
   vacío y no una ubicación, y estaba marcada como `coordenada_exacta`; se corrigió a
   `sin_coordenada` con `revisar=True`. Cualquier uso de las coordenadas debe excluir
   las filas `sin_coordenada`. Quedan fuera del análisis y están marcadas en el archivo.
4. **Una ubicación es inferida:** CIST020, cuyo domicilio es "Villa Fontana Norte
   #235", se asignó a la colonia Villa Fontana por el nombre de la calle. Está
   marcada con `revisar=True`.
5. **El ranking usa `sin_almacen_min`**, la cota conservadora, porque el censo no
   cruza tinaco con cisterna.
6. **La capa de colonias es la del INE vía IIEG.** El propio IIEG advierte que
   puede no coincidir con la que usan en la práctica los municipios.
7. **Coincidencia no es causa.** No conocemos los criterios con que el municipio
   eligió las ubicaciones; pueden incluir factores que el censo no ve, como
   disponibilidad de terreno, seguridad o acceso para la pipa.

## Archivos

- `cisternas_tlaquepaque.csv` — 60 registros: 50 cisternas y 10 propuestas, con
  tipo, domicilio, coordenada cuando existe, colonia asignada y cómo se asignó
- `contraste_cisternas.csv` — las 237 colonias con su riesgo, su rank, cuántas
  cisternas tiene y cuántas propuestas
- `contraste_cisternas_programa.csv` — lo mismo, con el riesgo dentro del programa y con
  respaldo de la lista oficial, y el porcentaje de la población en el programa
