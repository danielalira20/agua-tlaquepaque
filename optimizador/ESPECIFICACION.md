# Especificación del priorizador de pipas

Versión 0.7. Es el documento que manda: cualquier implementación (hoy la de referencia
en Python; la app no tiene priorizador propio y lee el `plan.json` que ese programa
calcula) se escribe **a partir de esto**, no una de la otra.

Si una regla no está aquí, no existe. Si una implementación difiere de un caso resuelto a
mano de la sección 10, el error está en la implementación.

Las decisiones de diseño y sus razones están en `docs/decisiones/`.

---

## 1. Qué decide

Para cada fecha, **a dónde van los viajes de pipa del día**. Cada viaje se estaciona en una
manzana (el centro) y entrega agua a las viviendas sin agua de esa manzana y de las
vecinas, de la más cercana a la más lejana, hasta agotar su capacidad o llegar al radio
de cobertura.

El objetivo es **atender a la mayor cantidad posible de viviendas sin agua**. Entre
opciones que atienden a las mismas viviendas, va primero quien lleva más tiempo sin agua
(la racha). El modo de usar la racha es un parámetro (sección 4). El resultado se compara contra un reparto de referencia
(baseline estilizado, sección 7) con **los mismos viajes**.

## 2. Entradas

| Entrada | Archivo | Campos que se usan |
|---|---|---|
| Estado | salida del motor (`contratos/estado.schema.json`) | `cvegeo`, `fecha`, `viv_sin_agua_min`, `viv_sin_agua_max`, `horas_sin_servicio_min`, `horas_sin_servicio_max` |
| Ubicación | `datos/manzanas_centroides.csv` | `cvegeo`, `lon`, `lat` |
| Ocupantes | `datos/manzanas_tlaquepaque.csv` | `cvegeo`, `ocupantes_prom` (trae las 4,871 manzanas, también las que no tienen centroide) |
| Colonia | `datos/manzana_colonia.csv` | `cvegeo`, `colonia` (solo para mostrar) |
| Cisternas | `datos/cisternas_tlaquepaque.csv` | solo para el baseline (sección 7): `id`, `tipo`, `fuente_ubicacion`, `lon`, `lat`, `colonia_capa`, `geocol` |
| Colonia por manzana | `datos/manzana_colonia.csv` | `geocol` y `colonia`, para ubicar cisternas por colonia |
| Parámetros | `supuestos.json` | sección 3 |

- Las fechas que se procesan son las que trae el estado.
- Una manzana que está en el estado pero no tiene centroide **no puede ser centro ni
  recibir agua**. Su necesidad sí cuenta en el total. Hoy son 8 manzanas sin geometría.
- `cvegeo` se lee siempre como texto (16 caracteres).

## 3. Parámetros

| Parámetro | Por defecto | Significado |
|---|---|---|
| `viajes_por_dia` | 63 | Viajes disponibles cada fecha |
| `litros_por_viaje` | 10,000 | Capacidad de un viaje |
| `litros_por_hogar` | 200 | Lo que recibe cada vivienda atendida |
| `radio_cobertura_m` | 300 | Distancia máxima entre el centro y una manzana atendida |
| `cota_para_ordenar` | `min` | Qué cota del estado se usa (`min` o `max`) |
| `modo_racha` | `desempate` | Cómo pesa el tiempo sin servicio: `desempate`, `peso` o `no` (sección 4) |
| `baseline_cisternas` | `todas` | Qué cisternas usa el baseline: `todas` (47) o solo `exactas` (35) |
| `baseline_turnos` | `todas` | Por qué cisternas pasan los turnos: `todas` o `con_necesidad` (sección 7) |

Valor derivado:

```
hogares_por_viaje = floor(litros_por_viaje / litros_por_hogar)      → 50
```

`pipas` (32) se reporta, pero no restringe el cálculo: lo que restringe son los viajes. 32
es la meta que anunció la alcaldesa el 14 de octubre; en julio eran 24
(`decisiones/referencias-y-prensa.md`, notas del 21 de julio y del 14 de octubre).

## 4. Necesidad y peso por manzana y fecha

Para la manzana `m` en la fecha `d`, según `cota_para_ordenar`:

```
necesidad(m, d) = viv_sin_agua_<cota>(m, d)                 viviendas sin agua
horas(m, d)     = horas_sin_servicio_<cota>(m, d)

peso(m, d)      = horas(m, d) / 24                          días seguidos sin servicio
```

- Con el valor por defecto del motor (`horas_efectivas_corte` = 24), `horas = 24 · n`
  para `n` días seguidos de racionamiento, así que `peso = n`.

`modo_racha` decide cómo se usa el peso al comparar dos viajes (sección 6):

| Modo | Qué compara primero | Qué compara después | Para qué |
|---|---|---|---|
| `desempate` (por defecto) | Viviendas atendidas | Valor ponderado por racha | Atender al máximo de viviendas; entre iguales, a quien lleva más días |
| `peso` | Valor ponderado por racha | Viviendas atendidas | Escenario de equidad: puede atender menos viviendas para llegar a las que llevan más días |
| `no` | Viviendas atendidas | — | Referencia sin racha |

La decisión y su evidencia están en `docs/decisiones/04-horizonte-dias.md`.
- Si `necesidad > 0`, se espera `horas > 0`. Si no, es un error de entrada.
- La cota mínima va con la cota mínima: no se mezclan `viv_sin_agua_min` con
  `horas_sin_servicio_max`.

## 5. Cobertura de un punto

La distancia entre dos manzanas es la distancia de **haversine** entre sus centroides,
con radio terrestre `R = 6,371,000 m`. Una manzana está dentro del radio si
`distancia <= radio_cobertura_m + 1e-6` (la tolerancia evita errores de redondeo en el
borde).

`llenar(c, resto)` simula un viaje estacionado en la manzana `c`:

```
vecinas = manzanas con centroide y distancia(c, m) <= radio, incluida c (distancia 0)
ordenar vecinas por (distancia, cvegeo)
cupo = hogares_por_viaje
para cada m en ese orden:
    n_m = min(resto(m), cupo)
    cupo = cupo - n_m
    si cupo = 0: terminar
atendidas(c) = suma de n_m
ponderado(c) = suma de n_m · peso(m, d)
```

El reparto dentro del radio va **de la más cercana a la más lejana**, no de la más
necesitada: refleja que la gente camina al punto. Quién llega primero es quien vive más
cerca.

## 6. Asignación diaria

Cada fecha se resuelve sola. Lo que se atendió un día no reduce la necesidad del
siguiente: una entrega de 200 L dura un día.

```
resto(m) = necesidad(m, d) para toda m
para k = 1 .. viajes_por_dia:
    candidatas = manzanas con centroide y resto(m) > 0
    si no hay candidatas: los viajes k .. viajes_por_dia quedan sin usar; terminar
    para cada candidata c: calcular llenar(c, resto), atendidas(c) y ponderado(c)
    elegir c* con la mayor clave según modo_racha:
        desempate:  (atendidas, ponderado)
        peso:       (ponderado, atendidas)
        no:         (atendidas)
        si sigue el empate: cvegeo menor (orden de texto)
    restar a resto(m) lo que atendió el viaje
    registrar el viaje con orden_eleccion = k
```

- **Solo pueden ser centro las manzanas que tienen viviendas sin agua.** La pipa se
  estaciona donde está la necesidad.
- **Un mismo centro puede recibir varios viajes** si le sigue quedando necesidad.
- **Es un algoritmo voraz:** elige el mejor viaje en cada paso. No garantiza por
  construcción el mejor reparto posible del día, así que la sección 8 lo compara contra
  el máximo posible. Es determinista y se puede verificar a mano. La decisión está en
  `docs/decisiones/05-algoritmo-voraz.md`.
- Un viaje que atiende menos de `hogares_por_viaje` viviendas entrega solo
  `n · litros_por_hogar`. El resto del tanque no se cuenta como entregado.

## 7. Baseline estilizado

**No es lo que hace el municipio.** Según el director de Agua Potable, las cisternas se
llenan cuando llega el reporte de los vecinos (La Crónica, 30 de julio; `datos/evidencia.csv`,
P006), y no hay registro de a dónde fueron las pipas. El baseline es un
reparto de referencia con las mismas reglas físicas que el priorizado, para medir cuánto
aporta elegir el destino por necesidad. En el reporte se llama **baseline estilizado**.
La decisión está en `docs/decisiones/01-baseline-cisternas.md`.

Usa los mismos `viajes_por_dia`, la misma capacidad, el mismo radio y el mismo llenado
(sección 5). Solo cambia **dónde se estaciona cada viaje**: en una cisterna instalada.

### Qué cisternas entran

Las de tipo `cisterna_municipal` y `cisterna_siapa`. Las 3 del SIAPA se incluyen y se
declaran. Las 10 propuestas no cuentan.

Cada cisterna se ubica con la primera regla que aplique:

1. **Exacta:** `fuente_ubicacion = coordenada_exacta` y la coordenada cae dentro del
   rectángulo de los centroides del municipio, con un margen de 0.02°.
2. **Por colonia:** si `colonia_capa` no está vacía. La colonia es `geocol` si viene, o la
   única colonia con ese nombre en `manzana_colonia.csv`. El punto es el promedio de los
   centroides de sus manzanas, sumados con `math.fsum` (suma exacta) para que el punto sea
   el mismo con cualquier versión de Python.
3. Si ninguna aplica, la cisterna queda fuera.

Con los datos actuales: 35 exactas, 12 por colonia y 3 fuera (CIST014, CIST021 y CIST022),
igual que `datos/HALLAZGOS_cisternas.md`. Con `baseline_cisternas = exactas` solo entran
las 35.

### Turnos

Cada cisterna se identifica con `id@tipo` (`CIST001@municipal`, `SIAPA001@siapa`). La clave
se adoptó cuando el archivo repetía ids entre el municipio y el SIAPA; ya son únicos, pero
se conserva porque no cambia el resultado y `plan.json` la usa. Las cisternas se ordenan por
esa clave. En la fecha con índice `i` (0 para la primera), el
viaje `k` va a la cisterna `(i · viajes_por_dia + k − 1) mod N`. Los turnos siguen de un
día al otro, así que el punto de arranque rota y ninguna cisterna recibe siempre el viaje
extra.

`baseline_turnos` decide qué cisternas forman los `N` turnos de cada fecha:

| Valor | Turnos | Qué mide |
|---|---|---|
| `todas` (por defecto) | Todas las cisternas que entran | Reparto parejo sin ver el calendario. Es la cota alta de la ventaja del priorizado |
| `con_necesidad` | Solo las que, al empezar el día, tienen viviendas sin agua dentro del radio | Como si se supiera qué zona está sin agua. La ventaja que queda sale solo de elegir dónde |

Si no queda ninguna cisterna en los turnos, todos los viajes del día quedan sin usar.

### Cada viaje

Se llena desde el punto de la cisterna: las manzanas con viviendas sin agua a `radio` o
menos de ese punto, ordenadas por (distancia, cvegeo), con `llenar` de la sección 5. Si
no hay ninguna, el viaje cuenta como usado y **vacío**. En la salida, `punto_id` es la
clave `id@tipo`, `cvegeo_centro` es `null` y `lon`, `lat` son el punto de la cisterna. La
colonia de la cisterna es `colonia_capa` o, si viene vacía, la de la manzana más cercana.

Las cisternas que no entran se reportan con su motivo: `sin coordenada ni colonia`,
`coordenada fuera del municipio`, `colonia ambigua`, `colonia no encontrada`,
`colonia sin manzanas ubicadas` o, con `baseline_cisternas = exactas`,
`sensibilidad: solo cisternas con coordenada exacta`.

## 8. Métricas

Por fecha:

| Métrica | Definición |
|---|---|
| `necesidad_total` | Suma de `necesidad(m, d)` sobre todas las manzanas |
| `viviendas_atendidas` | Suma de lo que atendieron los viajes |
| `personas_atendidas` | Suma de `n_m · ocupantes_prom(m)`: personas-día sin agua evitadas |
| `valor_ponderado` | Suma de `n_m · peso(m, d)` |
| `maximo_viviendas` | `min(viajes_por_dia · hogares_por_viaje, necesidad de las manzanas con centroide)` |
| `maximo_ponderado` | Suma de los `viajes_por_dia · hogares_por_viaje` pesos más altos, contando cada vivienda sin agua con el peso de su manzana |
| `eficiencia_viviendas_pct` | `100 · viviendas_atendidas / maximo_viviendas` (100 si el máximo es 0) |
| `eficiencia_ponderada_pct` | `100 · valor_ponderado / maximo_ponderado` (100 si el máximo es 0) |
| `cobertura_pct` | `100 · viviendas_atendidas / necesidad_total` (0 si no hay necesidad) |
| `viajes_usados`, `viajes_sin_usar` | Sección 6 |
| `viajes_vacios` | Viajes usados que no atendieron a nadie (solo pasa en el baseline) |

En la semana: la suma de cada métrica, más

| Métrica | Definición |
|---|---|
| `manzanas_sin_entrega` | Manzanas con `necesidad > 0` en al menos una fecha y ningún viaje que las atendiera en toda la semana |
| `personas_sin_entrega` | Suma en esas manzanas de `max_d necesidad(m, d) · ocupantes_prom(m)` |

Los dos máximos **ignoran la geografía**: suponen que cualquier viaje podría llegar a
cualquier vivienda. Son una cota superior, así que el mejor reparto real está entre lo
que logra el algoritmo y ese máximo. Si la eficiencia es 100%, el algoritmo es óptimo
para esa métrica.

La comparación es la diferencia **priorizado − baseline** de cada métrica, con la cota
mínima y con la máxima.

`manzanas_sin_entrega` se mide por manzana, no por vivienda: el modelo no sigue a cada
vivienda de un día al siguiente.

## 9. Salidas

`salidas/plan.json`, con la forma de `contratos/plan.schema.json` v2. Una sola corrida del
comando produce todo:

| Parte | Contenido |
|---|---|
| `parametros` | Los de la sección 3 y `hogares_por_viaje`. `cota_para_ordenar` es la configurada; las corridas usan las dos |
| `baseline` | Descripción, cisternas usadas (`id`, `tipo`, `ubicacion`: `coordenada_exacta` o `centro_de_colonia`, `lon`, `lat`, `colonia`) y excluidas con su motivo |
| `corridas` | Cuatro, en este orden: priorizado y baseline con cota mínima, luego priorizado y baseline con cota máxima. Cada una con sus fechas (viajes y resumen) y la semana |
| `comparacion` | Por cota, cada métrica de la semana como `{priorizado, baseline, diferencia}`, con diferencia = priorizado − baseline |
| `propuesta_cisternas` | `null`: reservado para una versión posterior |

Cada viaje:

| Campo | Priorizado | Baseline |
|---|---|---|
| `tipo` | `pipa` | `cisterna` |
| `punto_id` | `null` | `id@tipo` de la cisterna |
| `cvegeo_centro` | manzana donde se estaciona | `null` |
| `lon`, `lat` | centroide de esa manzana | punto de la cisterna |
| `colonia` | la de la manzana | la de la cisterna |
| `manzanas_cubiertas` | `[{cvegeo, viviendas}]` de la más cercana a la más lejana | igual |
| `viviendas_objetivo` | viviendas sin agua de ese día que recibe el viaje; 0 si va vacío | igual |
| `litros` | `viviendas_objetivo × litros_por_hogar` | igual |
| `personas_beneficiadas`, `prioridad_score` | suma de viviendas × ocupantes; suma de viviendas × peso | igual |

- `orden_eleccion` es el orden en que se eligieron los viajes. **No es una ruta**: no hay
  datos de calles ni de tiempos.
- Además del contrato, la salida trae `parametros.baseline_cisternas`,
  `parametros.baseline_turnos` y `viajes_vacios` en cada resumen. No están en el
  contrato v2: se acordó con Dani declararlos aquí y no cambiar `contratos/`. Quien lea
  `plan.json` puede ignorarlos.
- `pruebas/test_salida.py` compara la forma de la salida contra
  `fixtures/plan.fixture.json`: si el contrato cambia, esa prueba falla.

## 10. Casos resueltos a mano

Salvo que el caso diga otra cosa: `litros_por_viaje` = 2,000 (para que
`hogares_por_viaje` = 10 y las cuentas sean cortas), `litros_por_hogar` = 200,
`radio_cobertura_m` = 300, `cota_para_ordenar` = `min`, `modo_racha` = `desempate`,
`ocupantes_prom` = 4 en todas las manzanas y una sola fecha.

Las manzanas se colocan sobre un mismo meridiano, a la posición en metros que indica el
caso: `lat = metros / 111,194.93`, `lon` fija. Así la distancia de haversine entre dos
de ellas es exactamente la diferencia de posiciones.

| Caso | Manzanas: posición (m), necesidad, horas | Viajes | Resultado esperado |
|---|---|---|---|
En la tabla, «atendidas / ponderado» de cada candidata.

| Caso | Manzanas: posición (m), necesidad, horas | Viajes | Resultado esperado |
|---|---|---|---|
| **A.** Un viaje no alcanza | M1: 0, 30, 24 | 1 | Centro M1. Atiende 10 de M1: 10 / 10, 40 personas, 2,000 L |
| **B.** El radio es tope y se llena de cerca a lejos | M1: 0, 4, 24 · M2: 100, 3, 24 · M3: 400, 5, 24 | 1 | M1 = 7 (M3 queda fuera), M2 = 10, M3 = 8. Gana **M2**: atiende M2 3, M1 4, M3 3 (a 300 m, en el borde). Queda 2 en M3 |
| **C.** La racha desempata | M1: 0, 10, 24 · M2: 1000, 10, 96 | 1 | M1 = 10 / 10, M2 = 10 / 40. Empate en atendidas: gana **M2** con `desempate` y con `peso`. Con `no` gana **M1** por cvegeo |
| **D.** Atendidas contra racha | M1: 0, 10, 24 · M2: 1000, 4, 96 | 1 | M1 = 10 / 10, M2 = 4 / 16. Con `desempate` gana **M1** (10 viviendas). Con `peso` gana **M2** (4 viviendas). Con `no` gana **M1**. Con 2 viajes, el segundo va a la otra manzana en los tres modos |
| **E.** Varios viajes al mismo centro | M1: 0, 25, 24 | 4 | Viajes a M1: 10, 10 y 5 (el tercero lleva 1,000 L). El cuarto queda sin usar |
| **F.** Día sin racionamiento | M1: 0, 0, 0 · M2: 500, 0, 0 | 3 | Ningún viaje. 3 sin usar. Cobertura 0. Eficiencias 100 (los máximos son 0) |
| **G.** La cota cambia el orden | M1: 0, min 2 · máx 12, 24 · M2: 1000, 6, 24 | 1 | Cota mínima: M1 = 2, M2 = 6, gana **M2**. Cota máxima: M1 = 10 (12 recortado al cupo), M2 = 6, gana **M1** |
| **H.** Los días son independientes | M1: 0, 10 el día 1 y 10 el día 2, horas 24 y 48 | 1 por día | Día 1: M1 atiende 10 / 10. Día 2: M1 atiende 10 / 20 |
| **I.** Comparación contra el máximo | Las de D | 1 | `maximo_viviendas` = min(10, 14) = 10. `maximo_ponderado` = 4 · 4 + 6 · 1 = 22. Con `desempate`: eficiencias 100% y 45.5%. Con `peso`: 40% y 72.7% |

### Baseline

Mismos valores por defecto. Cada cisterna se coloca en el meridiano igual que las
manzanas.

| Caso | Escenario | Viajes | Resultado esperado |
|---|---|---|---|
| **J.** Los turnos siguen de un día al otro | Cisternas C1, C2, C3 a 0, 5,000 y 10,000 m, cada una con una manzana de 30 viviendas sin agua en su punto. Tres fechas | 2 por día | Día 1: C1, C2. Día 2: C3, C1. Día 3: C2, C3 |
| **K.** Viaje vacío | Cisterna C1 a 0 m. M1 a 1,000 m con 10 viviendas sin agua | 1 | Baseline: atiende 0, `viajes_vacios` = 1. Priorizado con la misma necesidad: atiende 10 en M1 |
| **L.** Se llena desde el punto de la cisterna | Cisterna a 50 m. M1 a 0 m (4), M2 a 200 m (8), M3 a 400 m (5) | 1 | Distancias 50, 150 y 350 m: M3 queda fuera. Atiende M1 4 y M2 6 |
| **M.** Turnos con necesidad | C1 a 0 m y C2 a 5,000 m. M1 a 100 m con 30 viviendas sin agua | 2 | Con `todas`: C1 atiende 10, C2 atiende 0. Con `con_necesidad`: C1 y C1, 10 cada uno |

### Lo que muestran los casos

Los casos D e I muestran el costo de cada modo, y hay que declararlo en el reporte. Con
`peso`, el priorizador puede atender a menos viviendas para llegar a las que llevan más
días sin agua; con `desempate` no pierde ninguna vivienda, pero la racha solo cuenta
entre opciones iguales.

## 11. Lo que el priorizador NO modela

Hay que declararlo en el reporte:

- Rutas, tráfico, tiempo de traslado y recarga de las pipas: solo cuenta viajes por día.
- Que cada viaje pueda hacerse con las pipas disponibles en un día (se toma el promedio de
  prensa). 32 pipas es una meta; en julio eran 24.
- Que la gente sin agua efectivamente llegue al punto. El radio es un supuesto de
  distancia caminable, en línea recta.
- Que una vivienda guarde agua de la entrega para el día siguiente.
- Las solicitudes reales por TlaqueChat y a dónde fueron las pipas de verdad.
- **El reparto real.** El baseline es estilizado: según la prensa, el llenado de
  cisternas responde a reportes ciudadanos, y no hay registro de a dónde fueron los 565
  viajes.
- **Que cada viaje a una cisterna sea un viaje de pipa completo es un supuesto, con
  respaldo.** Las cisternas comunitarias son de 10,000 L (La Crónica, 21 de julio; P007) y
  se llenan con una pipa que se programa cuando llega un reporte (30 de julio; P006). La
  prensa no dice si los 565 viajes incluyen esos llenados. Cada viaje a una cisterna se
  trata como un viaje de pipa: 10,000 L, unos 50 hogares. Los 28,296 hogares que reporta el municipio coinciden casi con 565 × 50 =
  28,250: es una cifra derivada de los viajes, no medida.
- **Una cisterna es un almacén.** En el baseline, un viaje a una cisterna sin viviendas
  sin agua cerca ese día cuenta como perdido, aunque en la realidad el agua quedaría
  guardada para el siguiente día de racionamiento de esa zona. Esto favorece al
  priorizado: con `baseline_turnos = todas` su ventaja es una cota alta, y
  `con_necesidad` es la comparación más conservadora.
- **La ubicación de 12 cisternas** es el centro de su colonia, no su punto real. La
  sensibilidad con `baseline_cisternas = exactas` usa solo las 35 con coordenada.
- **La marginación no entra en la prioridad** (opción A de la decisión abierta 4 del motor,
  `decisiones/README.md`). La equidad se mide aparte: `resultados/equidad_marginacion.csv`
  compara, por grado de marginación de la AGEB, lo que atiende el priorizado contra el
  baseline, con las dos cotas. Como maximiza viviendas atendidas, el priorizado puede dejar
  sin entregas a los grupos pequeños de manzanas de AGEB «Muy alto», sobre todo con la cota
  máxima: cuánto, en `resultados/resumen.md`, sección 4.
- **La ventaja depende de los supuestos del motor.** Cuando casi todas las zonas se quedan
  sin agua (las esquinas adversas de la sensibilidad del motor), cualquier reparto encuentra
  a quién atender y la ventaja contra el baseline con necesidad se achica: ver
  `resultados/resumen.md`, sección 3. Toda razón «X veces» dice contra qué baseline, con qué
  cota y en qué escenario.

## 12. Decisiones abiertas

Todas están resueltas; se dejan aquí con su resolución.

| # | Qué | Resolución | Quién decide |
|---|---|---|---|
| 1 | Baseline | **Acordada con Dani:** baseline estilizado, mismos viajes por turnos entre las cisternas (sección 7) | Jass y Dani |
| 2 | Modo de la racha | **Resuelta:** `desempate` por defecto; `peso` como escenario de equidad (decisión 04) | Jass |
| 3 | Si un centro puede estar en una manzana sin necesidad | **Resuelta:** no; solo pueden ser centro las manzanas con viviendas sin agua (sección 6) | Jass |
| 4 | Campos extra de `plan.json` (`viajes_vacios`, `baseline_cisternas`, `baseline_turnos`) | **Resuelta con Dani:** se declaran en la sección 9 y no se agregan al contrato v2 | Jass y Dani |
| 5 | Dónde vive la implementación oficial (Python o TypeScript) | **Resuelta en los hechos:** la de referencia en Python genera `plan.json` (`scripts/exporta_app.py`) y la app lo lee ya calculado; no hay priorizador en TypeScript | Jass y Migue |

## 13. Implementaciones

La de referencia está en `priorizador/` (Python, solo biblioteca estándar):

| Módulo | Secciones |
|---|---|
| `entradas.py` | 2, 3 y 4: lee supuestos, estado, ubicaciones, ocupantes y colonias |
| `cobertura.py` | 5: haversine, vecinas dentro del radio (con una rejilla) y `llenar` |
| `asignacion.py` | 6: el voraz diario con los tres modos de racha |
| `metricas.py` | 8: métricas por fecha y por semana, con los máximos posibles |
| `baseline.py` | 7: ubicación de cisternas y reparto por turnos |
| `plan.py` | Las cuatro corridas: priorizado y baseline, con cota mínima y máxima |
| `salida.py` | 9: `plan.json` con la forma del contrato v2 y la comparación |
| `__main__.py` | Corre todo: `python3 -m optimizador.priorizador --estado <csv del motor>` |

El comparador (`analisis/`, decisión 06) usa esta implementación como biblioteca para
armar las tablas de `resultados/`: no cambia el comando ni la salida.

Las pruebas están en `pruebas/`: los casos A a I en `test_casos.py` y propiedades
generales con datos al azar en `test_propiedades.py`, y los casos J a M en
`test_baseline.py`. La app no tiene una versión en TypeScript del priorizador: lee el
`plan.json` ya calculado. Si algún día se porta, debe pasar los mismos casos.
