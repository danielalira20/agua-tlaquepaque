# 01 · Baseline: con qué se compara el priorizador

Estado: Aceptada (acordada con Dani el 11 de noviembre; cifras y fuentes actualizadas el 12 de noviembre)

## Contexto

Para decir cuánto mejora el priorizador hace falta compararlo contra algo. No hay registro
de a dónde fueron los 565 viajes de pipa, y el llenado de cisternas responde a reportes
ciudadanos, es decir, a la demanda: según el director de Agua Potable, las cisternas se llenan
en cuanto llega el reporte de los vecinos y en ese momento se programa la pipa (La Crónica,
30 de julio; `datos/evidencia.csv`, P006). Lo único observado es dónde están las cisternas
que instalaron el municipio y el SIAPA.

## Opciones

- **Solo cisternas contra cisternas más pipas** (propuesta inicial de la decisión 4 del
  equipo). El priorizado siempre gana porque suma recursos: el resultado no dice nada de
  la regla.
- **Mismos viajes, regla distinta.** Los mismos viajes diarios van a las cisternas
  instaladas en un caso y a donde está la necesidad en el otro.

## Decisión

**Mismos viajes, regla distinta**, con un **baseline estilizado**: los 63 viajes diarios
se reparten por turnos entre las cisternas instaladas (sección 7 de
`ESPECIFICACION.md`).

- Entran 47 cisternas: 35 con coordenada exacta y 12 ubicadas en el centro de su colonia.
  Incluye las 3 del SIAPA. Quedan fuera las 3 que no se pudieron ubicar (CIST014, CIST021
  y CIST022) y las 10 propuestas.
- Cada cisterna se identifica como `id@tipo` (`CIST001@municipal`). Se decidió así porque el
  archivo repetía los ids CIST001 y CIST003 entre el municipio y el SIAPA. Dani ya los hizo
  únicos (las del SIAPA son SIAPA001 a SIAPA003; `datos/HALLAZGOS_cisternas.md`, limitación 4),
  así que la clave ya no hace falta, pero se conserva como defensa: no cambia el resultado y
  `plan.json`, `scripts/exporta_app.py` y la app ya la usan.
- Los turnos siguen de un día al otro, así que el punto de arranque rota y ninguna
  cisterna recibe siempre el viaje extra.
- Un viaje a una cisterna sin viviendas sin agua en 300 m cuenta como usado y vacío.
- Sensibilidad:
  - **Solo las 35 exactas** (`baseline_cisternas = exactas`).
  - **Turnos solo entre cisternas con necesidad cerca ese día**
    (`baseline_turnos = con_necesidad`).

## Por qué

1. Con los mismos viajes, la diferencia sale de **la regla**, no de tener más pipas.
2. Las cisternas instaladas son la única decisión observada sobre dónde poner agua.
3. El baseline por turnos mezcla dos efectos: no saber qué zona está sin agua cada día y
   la ubicación de las cisternas. La variante `con_necesidad` quita el primero, así que
   la ventaja que queda sale solo de elegir dónde.

## Lo que se encontró

Estado del motor de referencia, semana del 9 al 15 de noviembre, viviendas-día atendidas.
Las cifras salen de `resultados/resumen.md`, que genera el comparador (decisión 06):

| | Cota mínima | Cota máxima |
|---|---:|---:|
| **Priorizado** | **22,050** | **22,050** |
| Baseline por turnos, 47 cisternas | 4,532 (4.9×) | 10,177 (2.2×) |
| Baseline por turnos, 35 exactas | 3,952 (5.6×) | 9,473 (2.3×) |
| Baseline con necesidad, 47 cisternas | 7,078 (3.1×) | 15,920 (1.4×) |
| Baseline con necesidad, 35 exactas | 5,454 (4.0×) | 14,197 (1.6×) |

Con los mismos viajes, el priorizado atiende entre **1.4 y 5.6 veces** más viviendas-día,
según la cota y el baseline. La comparación más conservadora (con necesidad, cota máxima)
da 1.4 veces. En las esquinas adversas de la sensibilidad del motor, cuando casi todas las
zonas se quedan sin agua, esa comparación baja a 1.1 veces (`resultados/resumen.md`,
sección 3). Dos razones de la ventaja en el caso base:

- **El calendario.** En promedio, cada día solo el 40% de las cisternas (entre 34% y 45%)
  tiene viviendas sin agua a 300 m (cota mínima): las demás están en zonas que ese día no
  tienen racionamiento.
- **La ubicación.** 35 de las 47 cisternas están junto a manzanas de las zonas 3 y 4,
  mientras que el riesgo está sobre todo en las zonas 5 y 6: 72.6% con la cota mínima y
  63.0% con la máxima (`decisiones/README.md`, resolución de la delimitación).
  10 cisternas no tienen ninguna vivienda sin agua a 300 m en toda la semana.

Cifras preliminares: se recalculan con el estado oficial.

## Qué se declara

- Que es un **baseline estilizado** y no el reparto real del municipio.
- Que tratar cada viaje a una cisterna como un viaje de pipa (10,000 L, unos 50 hogares) es
  un supuesto, con respaldo: las cisternas comunitarias son de 10,000 L (La Crónica, 21 de
  julio; P007) y se llenan con una pipa que se programa cuando llega un reporte (30 de julio;
  P006). La prensa no dice si los 565 viajes incluyen esos llenados (22 de octubre; P004).
  Las notas están leídas completas en `decisiones/referencias-y-prensa.md` y con su URL en
  `datos/evidencia.csv`.
- Que los 28,296 hogares que reporta el municipio coinciden con 565 × 50 = 28,250: es una
  cifra derivada, no medida.
- Que la cisterna es un almacén y el baseline no lo modela: favorece al priorizado.
- Que 3 cisternas son del SIAPA y 12 están ubicadas por el centro de su colonia.
