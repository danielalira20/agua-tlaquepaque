# Especificación del priorizador de pipas

Versión 0.1, borrador. Es el documento que manda: cualquier implementación (la de
referencia en Python y, si se acuerda, una en TypeScript dentro de la app) se escribe
**a partir de esto**, no una de la otra.

Si una regla no está aquí, no existe. Si una implementación difiere de un caso resuelto a
mano de la sección 10, el error está en la implementación.

Las decisiones de diseño y sus razones están en `docs/decisiones/`.

---

## 1. Qué decide

Para cada fecha, **a dónde van los viajes de pipa del día**. Cada viaje se estaciona en una
manzana (el centro) y entrega agua a las viviendas sin agua de esa manzana y de las
vecinas, de la más cercana a la más lejana, hasta agotar su capacidad o llegar al radio
de cobertura.

El objetivo es atender primero a quien más lo necesita: más viviendas sin agua, y que
llevan más tiempo así. El resultado se compara contra un reparto de referencia
(baseline, sección 7) con **los mismos viajes**.

## 2. Entradas

| Entrada | Archivo | Campos que se usan |
|---|---|---|
| Estado | salida del motor (`contratos/estado.schema.json`) | `cvegeo`, `fecha`, `viv_sin_agua_min`, `viv_sin_agua_max`, `horas_sin_servicio_min`, `horas_sin_servicio_max` |
| Ubicación | `datos/manzanas_centroides.csv` | `cvegeo`, `lon`, `lat`, `ocupantes_prom` |
| Colonia | `datos/manzana_colonia.csv` | `cvegeo`, `colonia` (solo para mostrar) |
| Cisternas | `datos/cisternas_tlaquepaque.csv` | solo para el baseline (sección 7) |
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
| `usar_racha` | `true` | Si el tiempo sin servicio pesa en la prioridad |

Valor derivado:

```
hogares_por_viaje = floor(litros_por_viaje / litros_por_hogar)      → 50
```

`pipas` (32) se reporta, pero no restringe el cálculo: lo que restringe son los viajes.

## 4. Necesidad y peso por manzana y fecha

Para la manzana `m` en la fecha `d`, según `cota_para_ordenar`:

```
necesidad(m, d) = viv_sin_agua_<cota>(m, d)                 viviendas sin agua
horas(m, d)     = horas_sin_servicio_<cota>(m, d)

peso(m, d) = horas(m, d) / 24     si usar_racha
           = 1                    si no
```

- Con el valor por defecto del motor (`horas_efectivas_corte` = 24), `horas = 24 · n`
  para `n` días seguidos de racionamiento, así que `peso = n`: una vivienda en su cuarto
  día seguido sin agua vale cuatro veces lo que una en su primer día.
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
valor(c) = suma de n_m · peso(m, d)
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
    para cada candidata c: calcular llenar(c, resto) y valor(c)
    elegir c* con mayor valor(c)
        desempate 1: más viviendas atendidas
        desempate 2: cvegeo menor (orden de texto)
    restar a resto(m) lo que atendió el viaje
    registrar el viaje con orden_eleccion = k
```

- **Solo pueden ser centro las manzanas que tienen viviendas sin agua.** La pipa se
  estaciona donde está la necesidad.
- **Un mismo centro puede recibir varios viajes** si le sigue quedando necesidad.
- **Es un algoritmo voraz:** elige el mejor viaje en cada paso, sin garantizar el mejor
  reparto posible del día. Es determinista y se puede verificar a mano.
- Un viaje que atiende menos de `hogares_por_viaje` viviendas entrega solo
  `n · litros_por_hogar`. El resto del tanque no se cuenta como entregado.

## 7. Baseline

**Pendiente de la decisión 01** (`docs/decisiones/`), en revisión con Dani. Propuesta:

- Los **mismos** `viajes_por_dia`, con las mismas reglas de las secciones 5 y 6, pero el
  centro no se elige por necesidad: los viajes van a las **cisternas que ya colocó el
  municipio**, por turnos y en orden de `id` (el viaje `k` va a la cisterna
  `(k − 1) mod N`).
- El punto de cada cisterna es su coordenada. Las que solo tienen colonia se ubican en
  el promedio de los centroides de las manzanas de esa colonia. Las 3 que no se pudieron
  ubicar quedan fuera. Las 10 propuestas no cuentan.
- Si alrededor de una cisterna no hay viviendas sin agua dentro del radio, el viaje se
  cuenta como usado y sin atender a nadie. Eso es justo lo que se quiere medir: cuánto
  coincide la ubicación actual con la necesidad.

Así la diferencia entre baseline y priorizado sale de **la regla**, no de tener más
recursos.

## 8. Métricas

Por fecha:

| Métrica | Definición |
|---|---|
| `necesidad_total` | Suma de `necesidad(m, d)` sobre todas las manzanas |
| `viviendas_atendidas` | Suma de lo que atendieron los viajes |
| `personas_atendidas` | Suma de `n_m · ocupantes_prom(m)`: personas-día sin agua evitadas |
| `valor_ponderado` | Suma de `n_m · peso(m, d)` |
| `cobertura_pct` | `100 · viviendas_atendidas / necesidad_total` (0 si no hay necesidad) |
| `viajes_usados`, `viajes_sin_usar` | Sección 6 |

En la semana: la suma de cada métrica, más

| Métrica | Definición |
|---|---|
| `manzanas_sin_entrega` | Manzanas con `necesidad > 0` en al menos una fecha y ningún viaje que las atendiera en toda la semana |
| `personas_sin_entrega` | Suma en esas manzanas de `max_d necesidad(m, d) · ocupantes_prom(m)` |

La comparación es la diferencia **priorizado − baseline** de cada métrica, con la cota
mínima y con la máxima.

`manzanas_sin_entrega` se mide por manzana, no por vivienda: el modelo no sigue a cada
vivienda de un día al siguiente.

## 9. Salidas

`salidas/plan.json`. La forma definitiva la fija `contratos/plan.schema.json` en la rama
`feat/plan-contrato`. Mientras tanto, los nombres siguen la opción C de la decisión 4 del
equipo (`decisiones/propuesta-dani.md`):

```
{
  "parametros": { ...los valores de la sección 3 que se usaron },
  "fechas": [{
    "fecha": "2026-11-09",
    "viajes": [{
      "orden_eleccion": 1,
      "tipo": "pipa",
      "cvegeo_centro": "...",
      "colonia": "...",
      "manzanas_cubiertas": [{"cvegeo": "...", "viviendas": 12}],
      "viviendas_objetivo": 50,
      "litros": 10000,
      "personas_beneficiadas": 186.0,
      "prioridad_score": 150.0
    }],
    "resumen": { ...métricas por fecha de la sección 8 }
  }],
  "semana": { ...métricas de la semana }
}
```

- `viviendas_objetivo` cuenta solo viviendas sin agua ese día, nunca el total de la
  manzana.
- `orden_eleccion` es el orden en que el algoritmo eligió los viajes. **No es una ruta**:
  no hay datos de calles ni de tiempos.

## 10. Casos resueltos a mano

Salvo que el caso diga otra cosa: `litros_por_viaje` = 2,000 (para que
`hogares_por_viaje` = 10 y las cuentas sean cortas), `litros_por_hogar` = 200,
`radio_cobertura_m` = 300, `cota_para_ordenar` = `min`, `usar_racha` = `true`,
`ocupantes_prom` = 4 en todas las manzanas y una sola fecha.

Las manzanas se colocan sobre un mismo meridiano, a la posición en metros que indica el
caso: `lat = metros / 111,194.93`, `lon` fija. Así la distancia de haversine entre dos
de ellas es exactamente la diferencia de posiciones.

| Caso | Manzanas: posición (m), necesidad, horas | Viajes | Resultado esperado |
|---|---|---|---|
| **A.** Un viaje no alcanza | M1: 0, 30, 24 | 1 | Centro M1. Atiende 10 de M1. Valor 10, 40 personas, 2,000 L |
| **B.** El radio es tope y se llena de cerca a lejos | M1: 0, 4, 24 · M2: 100, 3, 24 · M3: 400, 5, 24 | 1 | Valores: M1 = 7 (M3 queda fuera), M2 = 10, M3 = 8. Gana **M2**: atiende M2 3, M1 4, M3 3 (a 300 m, en el borde). Queda 2 en M3 |
| **C.** La racha decide | M1: 0, 10, 24 · M2: 1000, 10, 96 | 1 | Con racha: M1 = 10, M2 = 40, gana **M2**. Sin racha: empate en valor y en viviendas, gana **M1** por cvegeo |
| **D.** La racha puede preferir menos viviendas | M1: 0, 10, 24 · M2: 1000, 4, 96 | 1 | M1 = 10, M2 = 16: gana **M2** y atiende 4 viviendas, no 10. Con 2 viajes: el segundo va a M1 (10). Sin racha y 1 viaje: gana M1 |
| **E.** Varios viajes al mismo centro | M1: 0, 25, 24 | 4 | Viajes a M1: 10, 10 y 5 (el tercero lleva 1,000 L). El cuarto queda sin usar |
| **F.** Día sin racionamiento | M1: 0, 0, 0 · M2: 500, 0, 0 | 3 | Ningún viaje. 3 sin usar. Cobertura 0 |
| **G.** La cota cambia el orden | M1: 0, min 2 · máx 12, 24 · M2: 1000, 6, 24 | 1 | Cota mínima: M1 = 2, M2 = 6, gana **M2**. Cota máxima: M1 = 10 (12 recortado al cupo), M2 = 6, gana **M1** |
| **H.** Los días son independientes | M1: 0, 10 el día 1 y 10 el día 2, horas 24 y 48 | 1 por día | Día 1: M1 atiende 10, valor 10. Día 2: M1 atiende 10 otra vez, valor 20 |

El caso D es la consecuencia buscada de usar la racha, y hay que declararla en el
reporte: con pocos viajes, el priorizador puede atender a menos viviendas para llegar a
las que llevan más días sin agua. La sensibilidad `usar_racha = false` muestra cuánto
cambia el resultado.

## 11. Lo que el priorizador NO modela

Hay que declararlo en el reporte:

- Rutas, tráfico, tiempo de traslado y recarga de las pipas: solo cuenta viajes por día.
- Que cada viaje pueda hacerse con las 32 pipas en un día (se toma el promedio de prensa).
- Que la gente sin agua efectivamente llegue al punto. El radio es un supuesto de
  distancia caminable, en línea recta.
- Que una vivienda guarde agua de la entrega para el día siguiente.
- Las solicitudes reales por TlaqueChat y a dónde fueron las pipas de verdad.
- La capacidad real de las cisternas comunitarias (decisión 01).
- La marginación: `severidad` del motor aún no la incluye, porque falta el archivo por
  AGEB.

## 12. Decisiones abiertas

| # | Qué | Propuesta | Quién decide |
|---|---|---|---|
| 1 | Baseline | Mismos viajes, centros en las cisternas actuales (sección 7) | Jass y Dani |
| 2 | Forma del peso de la racha | Lineal: `horas / 24` | Jass |
| 3 | Si un centro puede estar en una manzana sin necesidad | No | Jass |
| 4 | Forma definitiva de `plan.json` | Sección 9, en `feat/plan-contrato` | Jass, Dani y Migue |
| 5 | Dónde vive la implementación oficial (Python o TypeScript) | Por acordar | Jass y Migue |

## 13. Implementaciones

La de referencia vive en `priorizador/` (Python, solo biblioteca estándar) y sus pruebas
en `pruebas/`, empezando por los casos de la sección 10. Si se acuerda portarla a la app,
la versión en TypeScript debe pasar los mismos casos.
