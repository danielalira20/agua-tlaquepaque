# Especificación del motor de autonomía

Versión 0.1, borrador para aprobar. Es el único documento que mandan: la
implementación oficial (TypeScript, en la app) y la de referencia (Python,
`motor/referencia.py`) se escriben **a partir de esto**, no una de la otra.

Si una fórmula no está aquí, no existe. Si las dos implementaciones difieren, el
error está en una de ellas o en esta especificación, y se corrige aquí primero.

---

## 1. Qué calcula

Para cada manzana y cada fecha, entre cuántas y cuántas de sus viviendas se quedan
sin agua ese día, y cuántas tienen agua pero almacenada más tiempo del que conviene.

La manzana **no tiene una autonomía única**. Se parte en estratos de vivienda, porque
una vivienda sin tinaco no puede usar el tinaco del vecino.

## 2. Entradas

**Por manzana** (de `datos/manzanas_tlaquepaque.csv`):

| Símbolo | Columna | Significado |
|---|---|---|
| V | `viviendas` | Viviendas particulares habitadas |
| T | `viv_tinaco` | Viviendas con tinaco |
| C | `viv_cisterna` | Viviendas con cisterna o aljibe |
| o | `ocupantes_prom` | Ocupantes promedio por vivienda |

**Zona por manzana:** un conjunto de zonas del SIAPA, posiblemente vacío.
- `"4"` → una zona.
- `"3,4"` → la colonia abarca varias zonas (la lista oficial las marca con asterisco).
- `""` → fuera del programa de racionamiento. Esa manzana nunca tiene racionamiento.

**Calendario:** para cada zona, los días de la semana con racionamiento, con
**versión** y fecha de consulta (`motor/calendarios/`). Se expande a fechas
concretas: una fecha tiene racionamiento en una zona si su día de la semana está en
la lista de esa zona.

**Supuestos** (`motor/supuestos.json`, compartido por las dos implementaciones):

| Parámetro | Valor por defecto |
|---|---|
| `consumo_l_persona_dia` (c) | 50 |
| `tinaco_l` (Lt) | 1,100 |
| `cisterna_l` (Lc) | 5,000 |
| `horas_efectivas_corte` (he) | 24 |
| `u_horas_agua_guardada` (U) | 48 |
| `umbral_estado_parcial_pct` | 10 |
| `umbral_estado_mayoritario_pct` | 50 |

## 3. Estratos y rangos

Cada vivienda cae en uno de cuatro estratos:

| Estrato | Litros almacenados |
|---|---|
| `ambos` (tinaco y cisterna) | Lt + Lc |
| `solo_t` | Lt |
| `solo_c` | Lc |
| `ninguno` | 0 |

El Censo no cruza tinaco con cisterna, así que el número de viviendas con **ambos**,
`a`, solo se conoce en un intervalo:

```
T' = min(T, V)        C' = min(C, V)        (se recorta por si el dato viene inconsistente)
a_min = max(0, T' + C' - V)
a_max = min(T', C')
```

Dado `a`, los estratos son:

```
ambos = a      solo_t = T' - a      solo_c = C' - a      ninguno = V - T' - C' + a
```

**Propiedad que hace exacto el rango:** las banderas de "se queda sin agua" de cada
estrato dependen de la fecha y de los supuestos, **no de `a`**. Por eso el número de
viviendas sin agua es lineal en `a`, y su mínimo y su máximo ocurren siempre en
`a_min` o `a_max`. Basta evaluar esos dos extremos.

## 4. Horas sin servicio

Para una zona y una fecha `d`:

```
n = número de días consecutivos con racionamiento que terminan en d (incluyendo d)
H(d) = 0                          si n = 0
H(d) = he + (n - 1) * 24          si n >= 1
```

Es decir: el primer día de racionamiento dura `he` horas efectivas en la llave, y
cada día consecutivo adicional suma 24.

Una zona con racionamiento los 7 días no está soportada (el conteo no termina). Se
trata como error.

Si la manzana tiene **varias zonas**, se calcula `H` para cada una. Los resultados
finales toman el **mínimo** de los mínimos y el **máximo** de los máximos, de modo
que el intervalo se ensancha en lugar de escoger una zona arbitraria.

## 5. Viviendas sin agua

La autonomía de un estrato con `L` litros es:

```
aut(L) = L / (o * c) * 24        horas      (aut = 0 si L = 0)
```

Un estrato **se queda sin agua** en la fecha `d` si `aut < H(d)`, con desigualdad
estricta. Ejemplos de los bordes:
- `ninguno` tiene `aut = 0`, así que está sin agua siempre que `H > 0`.
- Si `H = 0` (no hay racionamiento) nadie está sin agua, ni siquiera `ninguno`.
- Si `aut = H` exactamente, el estrato todavía aguanta.

```
viv_sin_agua(a) = suma de las viviendas de los estratos con aut < H
viv_sin_agua_min = min sobre a en {a_min, a_max}
viv_sin_agua_max = max sobre a en {a_min, a_max}
```

## 6. Agua guardada y desinfección

Un estrato **tiene agua guardada** si aguanta (`aut >= H`), no es `ninguno`, y
además `H > U`. Es agua que lleva más de `U` horas almacenada y conviene desinfectar.

```
viv_agua_guardada_min / _max = igual que arriba, sobre los estratos con agua guardada
requiere_desinfeccion = viv_agua_guardada_max > 0
```

## 7. Salidas

Un renglón por manzana y por fecha:

| Campo | Definición |
|---|---|
| `cvegeo`, `fecha`, `dia` | Llave y día de la semana |
| `zona` | La que se usó, tal como entró |
| `horas_sin_servicio_min`, `_max` | `H` mínima y máxima entre las zonas de la manzana |
| `viv_sin_agua_min`, `_max` | Sección 5 |
| `pct_sin_agua_min`, `_max` | `100 * viv_sin_agua / V`, a un decimal |
| `personas_sin_agua_min`, `_max` | `viv_sin_agua * o`, a un decimal |
| `viv_agua_guardada_min`, `_max` | Sección 6 |
| `requiere_desinfeccion` | Sección 6 |
| `estado` | Según `pct_sin_agua_min` **sin redondear**: menor que 10 → `con_agua`; de 10 a 50 → `quiebre_parcial`; mayor que 50 → `quiebre_mayoritario` |
| `severidad` | `pct_sin_agua_min / 100`. **Sin peso de marginación todavía** (decisión abierta, ver sección 10) |

## 8. Casos resueltos a mano

Son las pruebas de `motor/test_referencia.py`. Cualquier implementación nueva debe
reproducirlos. Salvo que se diga otra cosa: o = 4, c = 50, Lt = 1,100, Lc = 5,000,
he = 24, U = 48.

| Caso | Entrada | H | Resultado esperado |
|---|---|---:|---|
| A | V=10, T=0, C=0 | 24 | sin agua = 10 (min y max) |
| B | V=10, T=10, C=0 | 24 | sin agua = 0. aut(tinaco) = 132 h |
| B2 | igual que B | 96 | sin agua = 0, agua guardada = 10 (porque 96 > U) |
| B3 | igual que B, pero c = 100 | 96 | sin agua = 10. aut(tinaco) = 66 h < 96 |
| C | V=10, T=6, C=0 | 96 | sin agua = 4 (los de `ninguno`). Los 6 con tinaco aguantan (132 h) |
| D | V=10, T=8, C=7, c=100 | 72 | a de 5 a 7. Sin agua = 3 en ambos extremos (pendiente 0) |
| E | V=10, T=6, C=6, c=100, Lt=Lc=1,000 | 72 | a de 2 a 6. Sin agua: **mín 4, máx 8**. Es el caso en que el mínimo cae en `a_max` |
| F | calendario vigente, zona 4, martes 10-nov-2026 | 96 | Cuatro días seguidos (sáb 7, dom 8, lun 9, mar 10): H = 24 + 3 × 24 |
| G | calendario vigente, zona 3, lunes 9-nov-2026 | 0 | No es día de racionamiento de la zona 3 |

El caso E es el que importa para probar que el rango está bien implementado: el
mínimo no está en el extremo "obvio".

## 9. Lo que el motor NO modela

Hay que declararlo en el reporte (Anexo F):

- **Un día de racionamiento equivale a cero agua en la llave.** El portal del SIAPA
  dice que es una baja de presión y no un corte total, con efecto desigual según la
  altura y la distancia. Es un supuesto, y `horas_efectivas_corte` y la sensibilidad
  son la forma de moverlo.
- La capacidad de tinaco y cisterna: el Censo dice si existen, no de cuántos litros.
- Que todas las viviendas de la manzana tienen los mismos ocupantes.
- Presión, calidad del agua en la llave y cloro. No hay datos públicos.
- El comportamiento de las familias (compras de garrafón, pipas, vecinos).
- Que el tinaco se llene completamente entre un racionamiento y el siguiente.

## 10. Decisiones abiertas

| # | Qué | Propuesta | Quién decide |
|---|---|---|---|
| 1 | Salida por **fecha** o por `dia_ciclo` | Por fecha, con `dia` como columna adicional | El grupo (cambia el contrato `estado`) |
| 2 | Valor de `horas_efectivas_corte` | 24 por defecto, con sensibilidad a 24, 36 y 48 | Tú y Jass |
| 3 | Manzanas con varias zonas | Ensanchar el intervalo (sección 4) | Tú |
| 4 | Peso de marginación en `severidad` | Cuando llegue el archivo de AGEB. Hoy sin peso | Tú y Jass |
| 5 | Desigualdad estricta en `aut < H` | Estricta | Tú |

## 11. Comparación entre implementaciones

```
python3 motor/referencia.py ...  > salidas/referencia.csv
(la app)                         > salidas/oficial.csv
python3 motor/comparar.py salidas/referencia.csv salidas/oficial.csv
```

`comparar.py` empareja por `cvegeo` y `fecha` y lista las diferencias columna por
columna. Los conteos de viviendas deben coincidir **exactamente**; los porcentajes y
las personas, con una tolerancia de 0.05.

**Regla de corte:** si el viernes al mediodía las dos no coinciden, gana la
implementación oficial y las diferencias que queden se documentan como limitaciones
conocidas.

La coincidencia entre las dos implementaciones **atrapa errores de programación, no
supuestos equivocados.** Si las dos asumen mal lo mismo, coinciden. Por eso el
análisis de sensibilidad y el contraste con las cisternas son pruebas aparte.
