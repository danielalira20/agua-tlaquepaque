# Resultados del priorizador

Generado por `python3 -m optimizador.analisis` según la decisión 06 (`optimizador/docs/decisiones/06-rejilla-comparador.md`). No se edita a mano: se vuelve a generar.

Semana del 2026-11-09 al 2026-11-15, calendario `vigente-2026-11-03`, estado del motor de referencia. 63 viajes de pipa al día, de 50 hogares cada uno, los mismos para el priorizado y para el baseline estilizado. Toda cifra va con la cota mínima y la máxima de viviendas sin agua, porque el Censo no cruza tinaco con cisterna.

## 1. Caso base

`modo_racha = desempate`, radio de 300 m. Viviendas-día atendidas en la semana y, entre paréntesis, cuántas veces lo del baseline.

|  | Cota mínima | Cota máxima |
|---|---:|---:|
| Viviendas-día sin agua | 58,906 | 128,460 |
| **Priorizado** | **22,050** | **22,050** |
| Baseline por turnos, 47 cisternas | 4,532 (4.9×) | 10,177 (2.2×) |
| Baseline por turnos, 35 exactas | 3,952 (5.6×) | 9,473 (2.3×) |
| Baseline con necesidad, 47 cisternas | 7,078 (3.1×) | 15,920 (1.4×) |
| Baseline con necesidad, 35 exactas | 5,454 (4.0×) | 14,197 (1.6×) |

Con los mismos viajes, el priorizado atiende entre 1.4× y 5.6× lo del baseline. La comparación más conservadora es **1.4×** (baseline con necesidad, 47 cisternas, cota máxima).

## 2. Sensibilidad del priorizador

Estado base. Cada renglón cambia la racha o el radio; la última columna es el rango contra los 4 baselines con las dos cotas. La eficiencia es contra el máximo de viviendas que se podían atender ese día.

| modo_racha | Radio | Priorizado, cota mín. | Priorizado, cota máx. | Eficiencia mínima | Manzanas sin entrega (mín. / máx.) | Veces el baseline |
|---|---|---:|---:|---:|---:|---:|
| `desempate` | 200 m | 22,050 | 22,050 | 100.0% | 701 / 1,986 | 1.9× a 9.2× |
| `desempate` (base) | 300 m | 22,050 | 22,050 | 100.0% | 501 / 1,928 | 1.4× a 5.6× |
| `desempate` | 500 m | 22,050 | 22,050 | 100.0% | 386 / 1,842 | 1.2× a 3.7× |
| `peso` | 200 m | 20,673 | 22,050 | 93.8% | 533 / 1,986 | 1.9× a 8.6× |
| `peso` | 300 m | 21,373 | 22,050 | 96.9% | 407 / 1,928 | 1.4× a 5.4× |
| `peso` | 500 m | 21,724 | 22,050 | 98.5% | 332 / 1,842 | 1.2× a 3.6× |
| `no` | 200 m | 22,050 | 22,050 | 100.0% | 753 / 2,420 | 1.9× a 9.2× |
| `no` | 300 m | 22,050 | 22,050 | 100.0% | 625 / 2,365 | 1.4× a 5.6× |
| `no` | 500 m | 22,050 | 22,050 | 100.0% | 561 / 2,284 | 1.2× a 3.7× |

## 3. Escenarios del motor

Parámetros base del priorizador. Los escenarios son el caso base y las esquinas de la sensibilidad del motor (`datos/HALLAZGOS_sensibilidad.md`); la procedencia del rango es la que les da ese análisis.

| Escenario | Procedencia | Cota | Viviendas-día sin agua | Priorizado | Veces: por turnos, 47 cisternas | Veces: por turnos, 35 exactas | Veces: con necesidad, 47 cisternas | Veces: con necesidad, 35 exactas |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `base` | decision | mínima | 58,906 | 22,050 | 4.9× | 5.6× | 3.1× | 4.0× |
| `base` | decision | máxima | 128,460 | 22,050 | 2.2× | 2.3× | 1.4× | 1.6× |
| `esquina_favorable` | decision | mínima | 58,622 | 22,050 | 4.9× | 5.6× | 3.1× | 4.1× |
| `esquina_favorable` | decision | máxima | 128,299 | 22,050 | 2.2× | 2.3× | 1.4× | 1.6× |
| `esquina_adversa` | decision | mínima | 222,608 | 22,050 | 2.3× | 2.4× | 1.2× | 1.3× |
| `esquina_adversa` | decision | máxima | 265,724 | 22,050 | 2.0× | 2.1× | 1.1× | 1.2× |
| `esquina_adversa_extrema` | sin_fuente | mínima | 262,220 | 22,050 | 2.2× | 2.3× | 1.2× | 1.3× |
| `esquina_adversa_extrema` | sin_fuente | máxima | 312,593 | 22,050 | 1.9× | 2.0× | 1.1× | 1.1× |

En los 4 escenarios, la comparación más baja es **1.1×** (`esquina_adversa_extrema`, baseline con necesidad, 47 cisternas, cota máxima).

Cambios de cada esquina respecto a `motor/supuestos.json`:

- `esquina_favorable`: `consumo_l_persona_dia = 50`, `tinaco_l = 1100`, `fraccion_suministro_en_racionamiento = 0.5`, `horas_efectivas_corte = 24`
- `esquina_adversa`: `consumo_l_persona_dia = 100`, `tinaco_l = 750`, `fraccion_suministro_en_racionamiento = 0.0`, `horas_efectivas_corte = 48`
- `esquina_adversa_extrema`: `consumo_l_persona_dia = 150`, `tinaco_l = 450`, `cisterna_l = 2500`, `fraccion_suministro_en_racionamiento = 0.0`, `horas_efectivas_corte = 48`

## 4. Equidad por grado de marginación

Estado y parámetros base. Grado de marginación de la AGEB de cada manzana (CONAPO 2020). La cobertura es la parte de las viviendas-día sin agua de ese grado que recibe agua. Los baselines son los de 47 cisternas.

| Grado | Cota | % de las viviendas-día sin agua | % de lo que atiende el priorizado | Cobertura: priorizado | Cobertura: baseline por turnos | Cobertura: baseline con necesidad |
|---|---|---:|---:|---:|---:|---:|
| Muy alto | mínima | 1.7% | 1.2% | 26.8% | 32.9% | 33.8% |
| Alto | mínima | 18.5% | 25.1% | 50.7% | 13.1% | 18.8% |
| Medio | mínima | 10.6% | 8.7% | 30.8% | 23.3% | 30.4% |
| Bajo | mínima | 18.8% | 22.0% | 43.9% | 7.5% | 12.9% |
| Muy bajo | mínima | 50.4% | 43.0% | 31.9% | 1.7% | 4.7% |
| sin dato | mínima | 0.1% | 0.0% | 6.6% | 0.0% | 0.0% |
| Muy alto | máxima | 1.6% | 0.0% | 0.0% | 31.6% | 35.8% |
| Alto | máxima | 25.0% | 39.6% | 27.2% | 6.5% | 11.5% |
| Medio | máxima | 27.4% | 37.5% | 23.5% | 15.5% | 23.2% |
| Bajo | máxima | 16.3% | 10.7% | 11.3% | 6.7% | 10.4% |
| Muy bajo | máxima | 29.6% | 12.1% | 7.1% | 1.5% | 3.0% |
| sin dato | máxima | 0.1% | 0.0% | 2.3% | 0.0% | 0.0% |

- Cota mínima: el priorizado atiende 261 de las 973 viviendas-día sin agua de AGEB «Muy alto»; el baseline por turnos, 320.
- Cota mínima, «Alto» y «Muy alto» juntos: el priorizado atiende 5,796 viviendas-día; el baseline por turnos, 1,752.
- Cota máxima: el priorizado atiende 0 de las 2,091 viviendas-día sin agua de AGEB «Muy alto»; el baseline por turnos, 661.
- Cota máxima, «Alto» y «Muy alto» juntos: el priorizado atiende 8,728 viviendas-día; el baseline por turnos, 2,763.

## 5. Cobertura diaria

Cada día, el priorizado cubre entre 34.2% y 40.5% con la cota mínima, y entre 16.1% y 18.3% con la cota máxima, de las viviendas sin agua. Los viajes no alcanzan para todas: por eso importa a dónde van. Detalle por fecha en `cobertura_diaria.csv`.

## 6. Costo por vivienda-día atendida

Decisión 07. Con el viaje de pipa a 1,200 pesos (precio de una pipa particular de 10,000 L en Tlaquepaque), los 441 viajes de la semana del priorizado cuestan 529,200 pesos. El costo por vivienda-día es el costo de los viajes usados entre las viviendas-día atendidas; un viaje vacío del baseline cuenta, porque la pipa sale igual.

|  | Cota mínima | Cota máxima | Viajes usados (mín. / máx.) |
|---|---:|---:|---:|
| **Priorizado** | **24.0 pesos** | **24.0 pesos** | 441 |
| Baseline por turnos, 47 cisternas | 116.8 pesos | 52.0 pesos | 441 / 441 |
| Baseline por turnos, 35 exactas | 133.9 pesos | 55.9 pesos | 441 / 441 |
| Baseline con necesidad, 47 cisternas | 74.8 pesos | 33.2 pesos | 441 / 441 |
| Baseline con necesidad, 35 exactas | 97.0 pesos | 37.3 pesos | 441 / 441 |

Con otros precios: con 700 pesos por viaje, el priorizado sale en 14.0 pesos con las dos cotas; con 2,000 pesos por viaje, el priorizado sale en 40.0 pesos con las dos cotas. La razón entre el priorizado y cada baseline no cambia con el precio, porque los viajes son los mismos.

## Lo que se declara

- Toda razón «X veces el baseline» dice contra qué baseline y con qué cota. La más conservadora es la del baseline con necesidad con la cota máxima.
- El baseline es estilizado: los mismos viajes repartidos por turnos entre las cisternas instaladas. No es lo que hace hoy el municipio, que llena las cisternas cuando los vecinos lo reportan (`decisiones/referencias-y-prensa.md`), y de ese reparto no hay registro.
- La marginación no pesa en la prioridad (opción A de la decisión abierta 4 del motor). Con la cota máxima, el priorizado puede dejar sin entregas a los grupos pequeños de manzanas de AGEB «Muy alto»: la sección 4 dice cuánto.
- El plan de cada día se recalcula cuando cambia un supuesto: el resultado agregado es robusto, los puntos de entrega no (`datos/HALLAZGOS_sensibilidad.md`).
- El costo de un viaje es el precio de una pipa particular de 10,000 L en Tlaquepaque (Milenio, 16 de mayo de 2025), no el costo del municipio, que no lo publica; no se ajustó por inflación (decisión 07). El costo por vivienda-día es otra forma de leer la ventaja del priorizado: no es un ahorro de presupuesto, porque los viajes son los mismos.
- Las cifras usan el estado del motor de referencia; se recalculan con el de la implementación oficial.
