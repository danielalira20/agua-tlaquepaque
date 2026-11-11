# Dataset 17 — Marginación (CONAPO): municipal y AGEB

## Estado: completo. Se obtuvieron los dos niveles que sirven.

| Nivel | Formato | ¿Se obtuvo? |
|---|---|---|
| Entidad federativa 2020 | `.xlsx` | Sí |
| **Municipio 2020** | `.xlsx` | **Sí** |
| **AGEB urbana 2020** | `.zip` | **Sí** (descargado a mano el 11-nov-2026; `datos/raw/IMU_2020.zip`, no se versiona) |
| Colonia 2020 | `.zip` | No hace falta |

Procesamiento: `python3 scripts/procesa_imu.py`. Llave: los primeros 13 caracteres del `cvegeo`
de cada manzana son la `CVE_AGEB`; no se empatan nombres. Salidas: `marginacion_ageb_tlaquepaque.csv`
(214 AGEB, 678,283 personas) y `marginacion_vs_riesgo.csv`.

**Cobertura del cruce:** 213 de las 214 AGEB del IMU tienen manzanas. 9 manzanas del Censo
(415 personas, 0.1%) caen en AGEB que el IMU no trae y quedan como "sin dato".

**Orientación del índice.** `IM_2020` más alto significa **menos** marginación: el grado "Muy bajo"
promedia 124.9 y el "Muy alto" 110.7. Se usa siempre el grado `GM_2020`. Comprobación con el
propio indicador de agua: el 14.8% de los ocupantes de las AGEB "Muy alto" no tiene agua entubada
(`OVSAE`), contra 0.05% en las "Muy bajo".

## El hallazgo del nivel AGEB: el riesgo de almacenamiento NO sigue a la marginación

Viviendas sin tinaco ni cisterna (cota mínima), por grado de marginación de su AGEB, **dentro del programa
de racionamiento**:

| Grado | Personas | % de la población | Viv. sin almacenamiento | % de las viviendas | **% del riesgo** | Con tinaco | Con cisterna |
|---|---:|---:|---:|---:|---:|---:|---:|
| Muy alto | 4,503 | 1.0% | 292 | 27.4% | 1.7% | 49% | 34% |
| Alto | 98,157 | 21.2% | 3,037 | 13.2% | 17.4% | 67% | 29% |
| Medio | 153,156 | 33.1% | 1,937 | 5.1% | 11.1% | 76% | 38% |
| Bajo | 108,311 | 23.4% | 3,395 | 11.1% | 19.5% | 79% | 52% |
| **Muy bajo** | 97,772 | 21.2% | **8,743** | **28.7%** | **50.2%** | 62% | 30% |

**La mitad del riesgo está en las AGEB menos marginadas.** La correlación entre el índice y el
porcentaje de viviendas sin almacenamiento por manzana es +0.10: ligeramente en el sentido
contrario al que esperábamos. Las colonias con más viviendas sin almacenamiento son casi todas
de marginación "Muy bajo": Villa Fontana, Parques de Sta. Cruz del Valle, Haciendas del Real, Las
Terrazas, Parques del Bosque, Geo Villas Los Olivos III, y la mayor parte de El Sauz.
Hipótesis, no verificada: son fraccionamientos de vivienda reciente que se construyeron sin tinaco.
La marginación "Alto" y "Muy alto" suma 22% de la población del programa y 19% del riesgo, es decir, no
hay sobrerrepresentación.

### Qué significa y qué no

- **No contradice el hallazgo principal.** El Sauz y las zonas 5 y 6 siguen siendo donde más viviendas
  no tienen cómo aguantar el racionamiento. Lo que cambia es el argumento de equidad.
- **Sí contradice una frase fácil de escribir:** "el riesgo se concentra en los más pobres". Con
  este índice no es cierto, y el reporte no debe decirlo.
- **El índice mide privación estructural** (educación, salud, vivienda, internet), **no la capacidad
  de resistir un corte de agua.** Un hogar sin tinaco en un fraccionamiento de marginación "Muy bajo"
  puede comprar pipa o garrafones; uno en una AGEB "Alto" tiene más probabilidad de no poder.
  No tenemos datos de cómo se defienden. Hay que decir que son dos dimensiones distintas:
  **exposición** (cuánto aguantas) y **vulnerabilidad social** (cuánto te cuesta no aguantar).

### Consecuencia para la decisión abierta 4 (peso de marginación en `severidad`)

Ponderar `severidad` por marginación **bajaría de prioridad a El Sauz**, que es nuestro
hallazgo número uno, y subiría zonas con poco riesgo de almacenamiento. Opciones:

1. **Sin peso (propuesta actual, recomendada para `severidad`).** `severidad` sigue siendo exposición pura.
   La marginación va en el mapa y en la tabla como **capa aparte**, con la lectura de arriba.
2. **Peso aditivo en el priorizador de Jass**, no en el motor: `personas × horas × (1 + α·vulnerabilidad)`
   con sensibilidad a α. Así el motor queda limpio y el priorizador decide cuánto pesa lo social.
3. **Peso multiplicativo puro.** No lo recomiendo: borra a El Sauz del primer lugar.

La decisión es de Dani y de Jass.

---

## El hallazgo del nivel municipal

El archivo municipal sí se obtuvo, y dice algo que conviene al reporte.

| Municipio | Población | Grado de marginación | Lugar estatal | Lugar nacional |
|---|---:|---|---:|---:|
| Guadalajara | 1,385,629 | Muy bajo | 125 de 125 | 2,456 de 2,469 |
| Zapopan | 1,476,491 | Muy bajo | 124 | 2,454 |
| **San Pedro Tlaquepaque** | **687,127** | **Muy bajo** | **123** | **2,424** |
| Tonalá | 569,913 | Muy bajo | 119 | 2,378 |

*(Número alto significa menos marginado.)*

**Oficialmente, Tlaquepaque es uno de los municipios menos marginados de México.**
Lugar 2,424 de 2,469. Y el indicador de agua del propio índice lo confirma:

> **OVSAE, ocupantes en viviendas sin agua entubada: 0.57%**

Es decir, para el índice oficial de vulnerabilidad, en Tlaquepaque prácticamente
nadie tiene problema de agua.

### Y aquí está el contraste

| Fuente | Qué mide | Resultado |
|---|---|---|
| CONAPO, OVSAE | Viviendas **sin tubo** | 0.57% |
| Nuestro análisis | Viviendas **sin dónde guardar** | **13.8% a 26.5%** |

Entre 21,775 y 41,879 de las 158,135 viviendas de Tlaquepaque no tienen tinaco ni
cisterna. El índice oficial no las ve, porque **mide el tubo, no el almacenamiento.**

Es la tesis del proyecto confirmada por el propio instrumento oficial: cuando el
agua llega por turnos, tener tubo deja de significar tener agua, y ningún índice
de marginación vigente capta esa diferencia.

### Un segundo argumento: el nivel municipal no discrimina

Los cuatro municipios del calendario del SIAPA son "Muy bajo" y están pegados entre
sí (lugares 119 a 125 de 125). **El índice municipal no sirve para priorizar dentro
de la zona de estudio.** Por eso se usa el archivo a nivel AGEB: es el único que
permite distinguir entre colonias de un mismo municipio.

---

## Cómo queda el requisito obligatorio del kit

El dataset 17 es uno de los dos obligatorios y ya se usa a **dos niveles**: el municipal, en la
caracterización del problema (el índice oficial no ve el almacenamiento), y el AGEB, para el cruce
con el riesgo y, si se decide, el peso del priorizador. Se cita completo en el reporte: CONAPO, Índice de
marginación urbana por AGEB 2020, estimaciones con base en el Censo de Población y Vivienda 2020.

## Archivos

- `marginacion_municipal.csv` — los cuatro municipios del calendario del SIAPA con
  sus indicadores, índice, grado y lugar
- `marginacion_ageb_tlaquepaque.csv` — las 214 AGEB de Tlaquepaque con sus once indicadores, índice y grado
- `marginacion_vs_riesgo.csv` — el riesgo de almacenamiento por grado, para todo Tlaquepaque y dentro del programa
