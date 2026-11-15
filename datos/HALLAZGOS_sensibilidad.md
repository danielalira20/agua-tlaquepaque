# Sensibilidad del orden de las manzanas a los supuestos del motor

Cumple la promesa de la decisión 1 (`decisiones/propuesta-dani.md`): en lugar de calibrar con una encuesta, demostrar cuánto
depende el resultado de los supuestos. Se corre con `python3 scripts/sensibilidad_orden.py` y se resume con
`python3 scripts/resume_sensibilidad.py`. Todas las tablas están en `sensibilidad/RESUMEN.md`; los datos, en `sensibilidad/`.
Es el material del **Anexo D** del reporte.

## 0. Veredicto

La decisión 1 decía: *"Si el orden de prioridad de las manzanas casi no cambia entre los extremos, entonces la conclusión no
depende de los supuestos."* **El orden individual de las manzanas sí cambia.** Pero varias conclusiones importantes no dependen
de los supuestos. Hay que decir las dos cosas.

| | ¿Aguanta los supuestos? |
|---|---|
| **El orden de cada manzana** | **No.** Con los rangos de la decisión 1, el rho de Spearman mediano contra el caso base es 0.65. Solo el 2.7% de los sorteos cumple el criterio de orden estable |
| **El núcleo de las más críticas** | **Sí.** 186 manzanas (3.8% de las 4,871) quedan entre las 250 de mayor riesgo en al menos el 90% de los sorteos. Con ellas se cubre entre 96.0% y 99.6% de lo que cubriría la mejor selección de ese tamaño bajo cada sorteo de la familia A |
| **El Sauz como colonia número uno** | **Sí.** Primero en los 600 sorteos y en 35 de 36 escenarios (segundo en el más extremo) |
| **Que Muy bajo sea el grado con más riesgo** | **Casi siempre.** 582 de 600 sorteos y 33 de 36 escenarios. Cede ante Medio solo cuando el tinaco aguanta entre 2.0 y 3.3 días, y aun ahí es la excepción (15 de los 123 sorteos con menos de 3 días) |
| **Que las zonas 5 y 6 sean la mayoría del riesgo** | **Sí, pero no "casi tres cuartas partes".** Siempre más del 50% (mínimo 50.3%), pero su parte baja de 72% a unos 60% cuando el tinaco aguanta menos |
| **La ventaja del priorizador** | **Sí, pero su tamaño depende de la cota y del baseline.** Con la cota mínima y contra el reparto por turnos, atiende entre 2.2 y 6.4 veces lo que el baseline en los 35 escenarios donde se corrió (entre 2.6 y 4.9 en las 120 simulaciones de Monte Carlo). Con la cota máxima baja a 1.9 a 2.2 veces en los cuatro escenarios del motor, y contra un reparto que solo visita las cisternas con necesidad ese día queda entre 1.1 y 3.1 (`optimizador/resultados/resumen.md`, sección 3). Eficiencia de 99.4% a 100% |
| **Dónde se estacionan las pipas** | **No.** Solo el 37% de las manzanas atendidas coincide en promedio con el caso base (familia A) |

## 1. Qué se hizo

**Medida.** Riesgo de una manzana = viviendas-día sin agua en la semana (cota mínima y máxima). El caso base es `motor/supuestos.json`,
el calendario vigente y las zonas base. El orden total se compara con **rho de Spearman** (entre manzanas con riesgo positivo), con
el **solape del top-k** y con la **cobertura del riesgo**: de lo que cubriría la mejor selección de 250 manzanas bajo un escenario, qué
fracción cubre el top-250 del caso base. Esta última no depende de cómo se rompan los empates.

**Escenarios.** 36 en total:
- Un supuesto a la vez: consumo, tinaco, cisterna, horas efectivas del corte, fracción `f` y U.
- Tres esquinas: favorable, adversa y adversa extrema.
- El calendario original del 15 de octubre.
- Tres variantes de las zonas: solo las colonias que están en la lista oficial del SIAPA, y los conflictos resueltos con la zona del portal o con
  la de la lista.
- El orden con la cota máxima, que es la incertidumbre propia del Censo.

Además, un barrido fino de consumo y tinaco, y **Monte Carlo con semilla fija** (600 sorteos): la familia A usa exactamente los rangos de la
decisión 1 (consumo 50 a 100 L, tinaco 750 a 1,100 L y U de 24 a 72 h), y la familia B suma cisterna, horas efectivas y `f`.

**Procedencia de los rangos.**

| Supuesto | Rango principal | Procedencia |
|---|---|---|
| Consumo | 50 a 100 L/persona/día | Decisión 1. 120 L viene del estudio de Maputo (VATTEN, no arbitrado); 150 L no tiene fuente |
| Tinaco | 750 a 1,100 L | Decisión 1. 450, 600, 1,500 y 2,500 L **no tienen fuente en el repo** |
| Cisterna | 2,500 a 10,000 L | **Sin fuente**: rango ilustrativo |
| Horas efectivas | 24 a 48 | Decisión abierta 2 |
| Fracción `f` | 0 a 0.5 | Decisión abierta 6 (0.75 no tiene fuente) |
| U | 24 a 72 h | Decisión 1 |

**Criterios fijados antes de la corrida completa** (son convenciones nuestras): orden estable si rho ≥ 0.90 **y** cobertura del top-250 ≥ 0.90;
conclusión B estable si las zonas 5 y 6 quedan dentro de ±10 puntos porcentuales de su valor base, El Sauz entre las 3 primeras colonias y Muy bajo
sigue siendo el grado con más riesgo; priorizador estable si atiende al menos 2 veces el baseline. Una prueba (`motor/test_sensibilidad.py`) impide
moverlos en silencio.

**Transparencia.** Los criterios se fijaron después de una corrida de prueba sobre el 10% de las manzanas. Después de esa prueba se cambió una sola
cosa: el rho se calcula solo entre manzanas con riesgo positivo (antes, sobre todas, lo que lo habría inflado por el bloque de manzanas con riesgo cero).
Es el cambio conservador: baja el rho.

## 2. Por qué cambia el orden: cuántos días aguanta un tinaco

El motor cuenta como "sin agua" a las viviendas sin almacenamiento siempre, y a las que tienen tinaco solo si el tinaco no aguanta la racha. La autonomía es
`tinaco / (ocupantes × consumo × (1 − f))`. Con 50 L/persona/día y 3.77 ocupantes (la mediana del Censo) un tinaco de 1,100 L aguanta 5.8 días, más que
cualquier racha del calendario (4 días en las zonas 4 y 5; 3 en las 3 y 6). Con 100 L aguanta 2.9 días y las viviendas con solo tinaco empiezan a quedarse sin agua.
El orden deja de depender únicamente de cuántas viviendas no tienen almacenamiento y pasa a depender también de cuántas tienen un tinaco corto.

Sobre los 600 sorteos de Monte Carlo, agrupados por esa autonomía:

| Autonomía del tinaco (días) | Sorteos | rho medio | Cobertura top-250 | Zonas 5 y 6 (%) | Muy bajo (%) |
|---|---:|---:|---:|---:|---:|
| 6 o más | 60 | 0.988 | 1.000 | 71.8 | 50.1 |
| 5 a 6 | 56 | 0.903 | 0.994 | 69.7 | 46.3 |
| 4 a 5 | 151 | 0.765 | 0.979 | 64.8 | 39.3 |
| 3 a 4 | 210 | 0.651 | 0.950 | 58.7 | 32.0 |
| 2 a 3 | 123 | 0.600 | 0.925 | 54.5 | 28.8 |

**Es un precipicio, no una pendiente.** Barrido fino (rho; cobertura del top-250):

| Consumo (L) | 50 | 55 | 60 | 65 | 75 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| rho | 1.000 | 0.972 | 0.900 | 0.818 | 0.728 | 0.615 |
| Cobertura top-250 | 1.00 | 1.00 | 0.99 | 0.99 | 0.98 | 0.94 |

| Tinaco (L) | 1,100 | 1,050 | 1,000 | 900 | 800 | 750 | 600 |
|---|---:|---:|---:|---:|---:|---:|---:|
| rho | 1.000 | 0.994 | 0.972 | 0.885 | 0.778 | 0.740 | 0.633 |
| Cobertura top-250 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.98 | 0.95 |

**Esto es lo único que no sabemos y que más mueve el resultado.** El Censo dice si hay tinaco, no de cuántos litros, y no sabemos cuánta agua gasta una
familia durante el racionamiento. Lo que más reduciría la incertidumbre es una fuente con el volumen típico de un tinaco y el consumo en la ZMG.
El caso base está en el extremo cómodo de los rangos (50 L, 1,100 L).

### Qué importa y qué no

Correlación de rangos entre cada supuesto y el rho del orden (Monte Carlo, `sensibilidad/RESUMEN.md`, sección 4):

| Supuesto | Familia A | Familia B | Lectura |
|---|---:|---:|---|
| Consumo | −0.87 | −0.63 | El que más pesa |
| Fracción `f` | | +0.60 | **Equivale a bajar el consumo**: lo que cuenta es `c × (1 − f)` |
| Tinaco | +0.48 | +0.27 | Pesa menos que el consumo en el rango de la decisión 1 |
| Horas efectivas | | −0.26 | Más horas de corte, más desorden |
| Cisterna | | +0.06 | **No importa**: una cisterna de 2,500 L ya aguanta más que cualquier racha |
| U | 0.00 | +0.08 | **No cambia el orden por viviendas sin agua** |

Un matiz sobre `f`: con 50 L casi no importa (rho 0.995 con `f` entre 0.25 y 0.75), porque las viviendas sin almacenamiento se quedan sin agua mientras `f < 1` y los
tinacos aguantan. En cuanto el consumo sube, `f` pesa mucho, porque reduce el consumo neto.

**U sí importa para otra cosa:** no cambia quién se queda sin agua, pero sí cuántas viviendas se marcan para desinfección (viviendas-día con agua guardada más de U horas):
**201,878 con U = 24 h, 121,130 con 48 h y 40,839 con 72 h**. El orden por agua guardada cambia (rho 0.99 con 24 h y 0.68 con 72 h). El umbral de 48 h
tiene respaldo en el estudio de Maputo (tiempos de retención de 0.4 a 6.3 días), pero esa referencia no es arbitrada.

## 3. Lo que sí aguanta

**El Sauz.** Primera colonia en los 600 sorteos y en 35 de 36 escenarios; segunda en la esquina adversa extrema (consumo 150 L, tinaco 450 L, cisterna 2,500 L).

**El núcleo robusto de 186 manzanas.** Quedan entre las 250 de mayor riesgo en al menos el 90% de los sorteos de la familia A. 169 de ellas están en el top-250 del caso base.
Concentran 31,734 viviendas-día sin agua del caso base: **el 54% del total (58,906) en solo el 3.8% de las manzanas**. Si se eligen esas 186 manzanas, se cubre entre
96.0% y 99.6% de lo que cubriría la mejor selección de 186 bajo cada sorteo de la familia A (93.4% a 99.6% en la B). Por zona: 65 en la zona 5, 62 en la 6, 51 en la 4 y 8 en
la 3. Por colonia, la que más pone es **El Sauz, con 28 manzanas y 8,850 viviendas-día**, seguida de Fovissste Miravalle (24), San Martín de las Flores de Abajo (21),
Parques de Santa Cruz del Valle (11), Villa Fontana (10) y Haciendas del Real (10). La lista completa, con la frecuencia de cada manzana, está en `sensibilidad/manzanas_robustas.csv`.

**El beneficio agregado del priorizador.** Con las mismas 63 pipas, atiende 22,050 viviendas-día en todos los escenarios (es el tope de capacidad: 63 viajes × 50 hogares × 7 días),
excepto con el calendario original (18,114, porque hay menos necesidad). Frente al baseline estilizado por turnos (47 cisternas) y **con la cota mínima**, atiende **entre 2.2 veces (esquina adversa extrema) y 6.4 veces (calendario original)** en los 35 escenarios donde se corrió.
En las 120 simulaciones de Monte Carlo donde se corrió, entre 2.6 y 4.9 veces, también con la cota mínima (`prio_veces_baseline_min`).
**Esas razones no valen para la cota máxima ni para otros baselines.** Con la cota máxima, el caso base da 2.2 veces y la esquina adversa extrema 1.9. Contra el reparto que solo visita las cisternas con necesidad ese día, da 3.1 (cota mínima) y 1.4 (máxima) en el caso base, y 1.1 con la cota máxima en las esquinas adversas (`optimizador/resultados/resumen.md`, sección 3). El criterio de estabilidad del priorizador (`UMBRAL_PRIORIZADOR`, 2.0 veces) solo se evaluó con la cota mínima; con la máxima, la esquina adversa extrema (1.9) no lo cumpliría. La razón baja cuando el tinaco aguanta menos porque el baseline atiende más (de 4,532 a 6,508 viviendas-día con 100 L), no porque el priorizador atienda menos.

**Zonas, calendario y cota.**
- *Calendario original contra vigente:* el orden casi no cambia (rho 0.98, cobertura 0.995).
- *Conflictos entre fuentes de zonas* (El Tapatío, San Juan, un pedazo de El Sauz): resolverlos con la zona del portal o con la de la lista da rho de 0.997 y 0.998. No importan.
- *Solo las colonias que están en la lista oficial:* el orden cambia (rho 0.67) porque salen del programa las colonias solo del portal (el 16% de la población). Aun así la cobertura del
  top-250 es 0.935, las zonas 5 y 6 siguen en 73.0% y el priorizador atiende 5.6 veces el baseline.
- *La cota máxima del Censo:* el orden por la cota máxima difiere del de la mínima casi tanto como el de los supuestos (rho 0.58; cobertura 0.93). Es la incertidumbre propia del Censo, que no cruza
  tinaco con cisterna, y no se reduce con ningún supuesto.

## 4. Lo que NO aguanta, y qué hacer

**El orden individual.** Con los rangos de la decisión 1, rho mediano 0.65 (p5 0.59, p95 0.86). Con la cota mínima y los supuestos del caso base el orden es muy distinto del que saldría con 100 L.
**No hay que presentar un ranking de manzanas como si fuera un dato.** Hay que presentar el núcleo robusto, y los intervalos.

**Dónde se estacionan las pipas.** El solape de las manzanas atendidas con las del caso base es en promedio 0.37 en la familia A (p5 0.14) y 0.50 en la B. El plan concreto cambia mucho con los supuestos,
aunque su desempeño agregado no. Recomendación: los puntos fijos (una propuesta de cisternas permanentes) deben salir del núcleo robusto; los viajes diarios se recalculan cuando cambia un supuesto.

**La parte del riesgo en cada zona y grado.** Ver la sección siguiente.

## 5. Corrección a cifras ya publicadas por el equipo

Esta revisión mostró que dos cifras que repetimos eran de **una sola cota**. Las dos conclusiones se sostienen, pero hay que decir las dos cotas y que el 72% y el 50% corresponden al caso base más favorable.

| Cifra | Cota mínima (la que se citó) | Cota máxima |
|---|---:|---:|
| Parte del riesgo de almacenamiento en las zonas 5 y 6 (Censo, dentro del programa) | 72.6% | **63.0%** |
| Parte del riesgo de almacenamiento en AGEB de marginación Muy bajo | 50.2% | **32.8%** (sigue siendo el grado con más) |
| Alto y Muy alto juntos | 19.1% | 23.5% |

Hay que distinguir dos medidas. El **riesgo de almacenamiento** (viviendas sin tinaco ni cisterna, del Censo) no depende de ningún supuesto, solo de la cota. Las **viviendas sin agua del motor** sí dependen del
consumo y del tinaco: en el caso base coinciden con las primeras (71.95% y 50.4%), y con los supuestos de la familia A bajan a unos 60% (media 59.8) y 34% (media 33.9).

Y un hallazgo adicional sobre la marginación: la relación entre el índice y el porcentaje de viviendas sin almacenamiento **no es monótona**. Con la cota mínima, Muy alto y Muy bajo tienen los porcentajes más altos
(27.4% y 28.7%); con la máxima, Muy alto 46.9%, Muy bajo 37.1%, Alto 33.1%, Medio 23.5% y Bajo 19.7%. La correlación de rangos con el índice es −0.01 con la cota mínima y −0.24 con la máxima (con la máxima, a más
marginación, algo más de viviendas sin almacenamiento). Sigue siendo cierto que **no se puede decir que el riesgo se concentre en los más pobres** (Alto y Muy alto tienen 19% a 23.5% del riesgo con 22% de la
población), pero tampoco que no tenga relación.

## 6. Redacción propuesta para el Anexo D y el reporte

> **Sensibilidad.** El Censo dice si una vivienda tiene tinaco o cisterna, pero no de cuántos litros, y no conocemos el consumo durante el racionamiento. Corrimos 36 escenarios y 600 simulaciones
> con rangos de consumo (50 a 100 L/persona/día), tinaco (750 a 1,100 L) y umbral de agua guardada (24 a 72 h). El orden exacto de las manzanas depende de cuántos días aguanta un tinaco: con 6 días o más
> es casi idéntico al caso base; con menos de 4, cambia sustancialmente. Por eso no presentamos un ranking de manzanas, sino un **núcleo de 186 manzanas** (el 3.8% del total, con el 54% de las viviendas-día
> sin agua del caso base) que permanece entre las 250 más críticas en al menos el 90% de las simulaciones. El Sauz es la primera colonia en todas. El priorizador atiende entre 2.6 y 4.9 veces lo que un reparto por turnos entre
> las cisternas instaladas en las 120 simulaciones en que se corrió, con la cota mínima (con la máxima, el caso base da 2.2 veces, y contra un reparto que solo visita las cisternas con necesidad, de 1.1 a 3.1 según el escenario), pero **los puntos donde se estacionan las pipas dependen de los supuestos**, por lo que el plan debe recalcularse al cambiar un supuesto. Los resultados se reportan siempre
> con cota mínima y máxima.

**Lo que no se puede decir:** "el orden de las manzanas no depende de los supuestos"; "las zonas 5 y 6 concentran tres cuartas partes del riesgo" sin decir que es la cota mínima y el caso base; "la mitad del riesgo está en las AGEB menos
marginadas" sin la cota máxima; que el consumo es de 50 L sin decir que es el extremo cómodo.

## 7. Límites

- Los supuestos son **iguales para todas las manzanas** (un solo tamaño de tinaco, un solo consumo). En realidad varían, y esa variación entre viviendas no se modela.
- Los ocupantes son el promedio de la manzana. En las 63 manzanas con más de 5.5 ocupantes por vivienda, un tinaco de 1,100 L deja de alcanzar para una racha de 4 días ya con 50 L.
- Los rangos de 450, 600, 1,500, 2,500 L de tinaco, 2,500 a 10,000 L de cisterna, 150 L de consumo y 0.75 de `f` **no tienen fuente en el repo**: son ilustrativos. Los sorteos son uniformes, una elección que no tiene justificación empírica.
- Los umbrales de los criterios son convenciones. El resultado no cambia con ellos: la tabla de la sección 2 muestra la gradación completa.
- Las manzanas con zona de confianza baja (el 16% de la población, solo por el polígono del portal) son una incertidumbre aparte: la variante "solo lista" la mide, pero no hay forma de saber cuál es la correcta (ver `zonas_siapa/LEEME.md`).
- El calendario es periódico: cualquier ventana de siete días da el mismo resultado (se comprobó con el 16 al 22 de noviembre y con una semana de miércoles a martes).
- La sensibilidad del propio priorizador (radio de cobertura, modo de racha, cota para ordenar, baseline) es del carril de Jass (`optimizador/supuestos.json`); aquí solo se mide su respuesta a los supuestos del motor.
- Pendiente de Jass: la tabla de viviendas-día atendidas por grado de marginación con las dos cotas (decisión de marginación, opción A).

## 8. Reproducir

    python3 scripts/sensibilidad_orden.py          # unos 9 minutos; escribe datos/sensibilidad/
    python3 scripts/resume_sensibilidad.py          # escribe datos/sensibilidad/RESUMEN.md
    python3 motor/test_sensibilidad.py              # pruebas (necesita numpy y pandas)

| Archivo | Qué es |
|---|---|
| `sensibilidad/escenarios.csv` | Un renglón por escenario, con todas las métricas y las del priorizador |
| `sensibilidad/barrido_fino.csv` | Consumo de 50 a 100 L y tinaco de 600 a 1,100 L, en pasos |
| `sensibilidad/montecarlo.csv` | 300 sorteos de la familia A y 300 de la B, con sus parámetros |
| `sensibilidad/manzanas_robustas.csv` | Frecuencia de cada manzana entre las 250 de mayor riesgo, y el núcleo robusto |
| `sensibilidad/importancia.csv` | Qué supuesto mueve más cada resultado |
| `sensibilidad/RESUMEN.md` | Todas las tablas, generadas |
