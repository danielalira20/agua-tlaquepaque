# 01 · Baseline: con qué se compara el priorizador

Estado: Aceptada (acordada con Dani el 11 de noviembre)

## Contexto

Para decir cuánto mejora el priorizador hace falta compararlo contra algo. No hay registro
de a dónde fueron los 565 viajes de pipa, y según la prensa el llenado de cisternas
responde a reportes ciudadanos, es decir, a la demanda. Lo único observado es dónde están
las cisternas que instalaron el municipio y el SIAPA.

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
- Cada cisterna se identifica como `id@tipo`, porque el archivo repite los ids CIST001 y
  CIST003 entre el municipio y el SIAPA.
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

Estado del motor de referencia, semana del 9 al 15 de noviembre, viviendas-día atendidas:

| | Cota mínima | Cota máxima |
|---|---:|---:|
| **Priorizado** | **22,050** | **22,050** |
| Baseline por turnos, 47 cisternas | 4,465 (4.9× menos) | 10,038 (2.2×) |
| Baseline por turnos, 35 exactas | 3,928 (5.6×) | 9,542 (2.3×) |
| Baseline con necesidad, 47 cisternas | 7,128 (3.1×) | 15,771 (1.4×) |
| Baseline con necesidad, 35 exactas | 5,454 (4.0×) | 14,208 (1.6×) |

Con los mismos viajes, el priorizado atiende entre **1.4 y 5.6 veces** más viviendas-día,
según la cota y el baseline. La comparación más conservadora (con necesidad, cota máxima)
da 1.4 veces. Dos razones:

- **El calendario.** Cada día solo el 40% de las cisternas tiene viviendas sin agua a 300 m
  (cota mínima): las demás están en zonas que ese día no tienen racionamiento.
- **La ubicación.** 35 de las 47 cisternas están junto a manzanas de las zonas 3 y 4,
  mientras que el 72.6% del riesgo está en las zonas 5 y 6 (`datos/HALLAZGOS_zonas.md`).
  10 cisternas no tienen ninguna vivienda sin agua a 300 m en toda la semana.

Cifras preliminares: se recalculan con el estado oficial.

## Qué se declara

- Que es un **baseline estilizado** y no el reparto real del municipio.
- Que tratar cada viaje a una cisterna como un viaje de pipa (10,000 L, unos 50 hogares) es
  un supuesto. La prensa dice que el llenado es con agua de pozos municipales conforme
  llegan reportes, pero no que los 565 viajes incluyan rellenar cisternas. Fuentes
  revisadas por Dani: Crónica (15 y 22 de octubre) y Milenio; falta agregarlas con su URL a
  `datos/FUENTES.md`.
- Que los 28,296 hogares que reporta el municipio coinciden con 565 × 50 = 28,250: es una
  cifra derivada, no medida.
- Que la cisterna es un almacén y el baseline no lo modela: favorece al priorizado.
- Que 3 cisternas son del SIAPA y 12 están ubicadas por el centro de su colonia.
