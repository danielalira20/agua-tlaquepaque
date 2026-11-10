# Propuesta de Dani — las 4 decisiones de Fase 0

Documento para la junta de cierre de contratos. Una sección por decisión. Cada una
trae las opciones reales, qué nos pasa si elegimos mal, la recomendación y lo que
queda escrito como supuesto declarado.

Al final hay una sección de **riesgos que cruzan las cuatro decisiones**. Esa es la
que no hay que saltarse: ahí está el único punto donde el proyecto puede incumplir
un requisito obligatorio del kit sin que nadie se dé cuenta.

---

## Decisión 1 · La evidencia propia: se cancela la encuesta

**Decisión: no hacemos encuesta.** La evidencia propia sale de dos cosas que no
dependen de conseguir gente que responda.

### Por qué se cancela

**El kit no la pide.** Revisadas las 7 indicaciones generales y los 5 criterios de
éxito del Reto 01, ninguno pide prueba con usuarios. El que sí la pide es el
**Reto 04** (Educación): *"muestra evidencia de que les sirve: una prueba con
usuarios, una encuesta corta o una revisión de accesibilidad"*. El Reto 01 pide otra
cosa: *"análisis de viabilidad que contemple el contexto institucional y
presupuestal de un municipio real"*.

**Y hay una razón más fuerte que "no es obligatoria": una encuesta contestada por la
gente equivocada es peor que ninguna encuesta.** Si quienes responden no viven en las
zonas 3 y 4 de Tlaquepaque, los datos no describen a la población que delimitamos, y
meterlos al reporte sería un error metodológico que el jurado puede señalar. Con el
tiempo y el alcance que tenemos, la probabilidad de llegar a residentes de esas
colonias en tres días es baja.

Más vale no tener evidencia propia que tener evidencia que no describe a nadie.

### Qué la reemplaza

**A. Contraste contra las 60 cisternas que el municipio ya colocó.**

Tlaquepaque publicó un mapa interactivo con la ubicación de sus 60 cisternas
comunitarias. Eso habilita una prueba mejor que una encuesta:

> ¿Las cisternas que el municipio ya colocó coinciden con donde nuestro modelo dice
> que está el riesgo?

Las dos respuestas posibles son un resultado:

| Resultado | Qué significa |
|---|---|
| **Coinciden** | El modelo reproduce el juicio de quien ya opera el sistema. Queda calibrado contra decisiones reales |
| **No coinciden** | Estas son las manzanas de alto riesgo que hoy no tienen cisterna cerca. Eso **es** la propuesta |

Es validación contra decisiones que alguien ya tomó con presupuesto y camiones, no
contra lo que unas cuantas personas contestaron en un formulario.

**B. Análisis de sensibilidad en lugar de calibración.**

Los supuestos inciertos son la capacidad del tinaco (750 a 1,100 L), el consumo por
persona (50 a 100 L/día) y el umbral U (24 a 72 h). Ante parámetros inciertos, la
respuesta correcta no es muestrear veinte personas: es demostrar que el resultado
aguanta todo el rango plausible.

Si el orden de prioridad de las manzanas casi no cambia entre los extremos, entonces
**la conclusión no depende de los supuestos**. Eso es más fuerte que calibrar con una
muestra chica, y se calcula sin salir del repo.

### Qué se pierde y con qué se cubre

| Se pierde | Se cubre con |
|---|---|
| Calibrar los litros del tinaco | Literatura citada más el análisis de sensibilidad |
| El área de economía (gasto en garrafones) | El análisis de costo del operativo de pipas, que ya se hace para el criterio 5. Queda **mejor**: es dinero público verificable |
| La cita humana para el pitch | Cobertura de prensa y el estudio de Guadalajara |

### El contrato cambia de nombre y de contenido

`mediciones.schema.json` pasa a ser **`evidencia.schema.json`**. Ya no carga
respuestas de encuesta, sino renglones de evidencia de distinto origen:

- `fuente`: `cisternas_municipio` | `estudio_rubino` | `imdec` | `prensa`
- Las ubicaciones de las 60 cisternas, para el contraste
- Los valores de literatura usados en la calibración, cada uno con su cita

### Lo único que no se puede hacer

Quitarla en silencio y aun así escribir "validamos". En el reporte va una línea
diciendo qué se hizo en su lugar y por qué. Eso es defendible; lo otro no.

### Efecto en el plan

Esto **quita** trabajo, no lo agrega:

- Se libera la tarea de Fase 0 de tener la encuesta lista y publicada.
- Se libera la tarea de difundirla en grupos de colonias.
- **"Encuesta publicada el martes" sale del mapa de bloqueos.**
- La Fase 3 cambia "validar con la encuesta" por "sensibilidad más contraste con
  las cisternas".

---

## Decisión 2 · `estado.schema.json`: el enum y el umbral

### El problema del enum que tenemos hoy

El enum del plan v2 es `segura | agua_guardada_desinfectar | sin_agua | fuente_riesgosa`.
Tiene dos defectos que van a estorbar:

**Defecto 1: mezcla tres ejes distintos en una sola lista.** `sin_agua` habla de
cantidad, `agua_guardada_desinfectar` habla de calidad, y `fuente_riesgosa` habla de
conducta. Una manzana puede estar sin agua **y** con gente yendo a otra fuente al
mismo tiempo. Un enum plano obliga a inventar una prioridad entre categorías que no
compiten entre sí.

**Defecto 2, y este es el serio: `fuente_riesgosa` afirma algo que no podemos
sostener.** Nosotros no sabemos a dónde va la gente cuando no le llega el agua. Lo
estamos infiriendo. Si un jurado pregunta "¿cómo saben que recurren a una fuente
riesgosa?", la respuesta honesta es "no lo sabemos, lo suponemos". Ese es un hoyo
innecesario, porque el dato que **sí** tenemos es igual de fuerte.

### Opciones

**Opción A — dejar el enum del v2.** Rápido, pero cargamos con los dos defectos.

**Opción B — dos campos ortogonales** (`tiene_agua` y `calidad`). Correcto
conceptualmente, pero obliga a Migue a pintar dos dimensiones en un mapa, y en una
demo de 15 minutos dos dimensiones se leen peor que una.

**Opción C (recomendada) — una escalera de severidad con precedencia explícita, y
los números crudos conservados en campos aparte.** Migue pinta un color por manzana,
nadie pierde información, y ningún nombre afirma lo que no podemos probar.

```
estado  (se asigna el peor que aplique, en este orden)

  1. sin_agua_sin_respaldo   se le acabó el almacenamiento Y la mayoría de las
                             viviendas de la manzana no tiene dónde guardar
  2. sin_agua                se le acabó antes del siguiente turno
  3. agua_guardada           tiene agua, pero lleva más de U horas almacenada
  4. con_agua                recibió agua hace poco
```

Campos que acompañan y que conservan todo lo demás:
`horas_restantes`, `horas_guardada`, `rango_autonomia` (`<12h` / `12-48h` / `>48h`),
`pct_sin_almacen_min`, `pct_sin_almacen_max`, `severidad`.

**Por qué `sin_agua_sin_respaldo` es mejor que `fuente_riesgosa`:** dice exactamente
lo que el Censo nos permite afirmar — que no tienen dónde guardar — y deja la
inferencia sobre a dónde van para el texto del reporte, donde puede ir acompañada de
la literatura y del contraste con las cisternas. El nombre de una categoría no debe contener una
hipótesis.

### El umbral U

Es el número que define cuándo el agua pasa de `con_agua` a `agua_guardada`.

| Anclaje | Qué dice | Estado |
|---|---|---|
| Estudio de Guadalajara (51 casas) | Remidieron cloro a las **120 horas** | Citable, con enlace |
| Estudio de Maputo (VATTEN 2014) | Caída de ~60% del cloro durante almacenamiento, y tiempos de retención de **0.4 a 6.3 días** en tinacos | ✅ **verificado en la fuente** (ver `verificacion-citas.md`) |
| NOM-127-SSA1-2021 | Cloro residual libre entre 0.2 y 1.5 mg/L | Norma mexicana, citable |

**Recomendación: U = 48 horas, como parámetro de configuración, no como número
escrito en el código.** Y reportar sensibilidad a 24, 48 y 72 horas.

Razones: 120 horas es más largo que casi cualquier intervalo de tandeo, así que casi
ninguna manzana se marcaría y el estado sería inútil. 48 horas cae dentro del rango
de Maputo y es menor al intervalo típico de 3 días, así que discrimina. Y si la cita
de Maputo no se confirma, 48 sigue siendo defendible como supuesto declarado con
análisis de sensibilidad, que es exactamente lo que el kit pide cuando algo es
estimado.

> **Requisito de implementación:** U vive en un archivo de configuración. Si está
> escrito dentro del código, el análisis de sensibilidad se vuelve tres reescrituras
> en lugar de un ciclo, y el jueves no va a haber tiempo.

---

## Decisión 3 · `dia_ciclo` contra hora

### La respuesta corta es día, y la razón es honestidad con los datos

El calendario del SIAPA publica **días de suspensión por zona**, no horas de corte.
Si el contrato pide hora, alguien va a tener que inventar la hora. Eso es
exactamente el tipo de decimal que un jurado experto pregunta primero y que no
podemos defender.

### Comparación

| | Por día | Por hora |
|---|---|---|
| ¿Lo sostiene el calendario? | **Sí** | No. Hay que inventar la hora de corte |
| Renglones de `estado` | 4,871 × 7 = **34,097** | 4,871 × 168 = 818,328 |
| Mapa en el navegador | Instantáneo | Pesado, hay que agregar |
| Explicarlo en 15 minutos | Un selector de 7 días | Hay que justificar la hora inventada |
| Demo | Buena: se ve la colonia cambiar día a día | Más vistosa, pero apoyada en un supuesto frágil |

### La forma de no perder nada

**El motor calcula internamente en horas** — la autonomía es una cantidad continua y
así debe computarse. **El contrato y la interfaz exponen días.** No se pierde
precisión analítica y no se fabrica lo que el calendario no dice.

El ciclo es **semanal** porque las zonas suspenden en días fijos de la semana, así
que `dia_ciclo` con valores `lunes` a `domingo` describe el ciclo completo y se repite.

### Compatibilidad hacia adelante

Si aparece el horario con horas (puede estar en la fuente oficial del SIAPA, aún no
lo confirmamos), se agrega un campo opcional `hora_inicio_corte` en
`calendario.json`. Ese campo **refina el cálculo de autonomía** sin cambiar la
granularidad de `estado`. Así, si el dato aparece el miércoles, se aprovecha sin
rehacer nada.

### Un caso borde que vale como hallazgo

Si una manzana tiene autonomía mayor a 7 días, nunca entra en `sin_agua` dentro del
ciclo. **Eso no es un error: es el resultado.** Son las viviendas para las que el
tandeo es invisible. Enseñar las dos cosas lado a lado — la manzana que no se entera
y la que se queda seca el segundo día — es el argumento central del proyecto en una
sola imagen.

---

## Decisión 4 · `plan.schema.json`: la unidad de salida del priorizador

Esta es la que está peor definida hoy y la que más afecta a dos personas a la vez,
porque determina lo que programa Jass **y** lo que dibuja Migue.

### La realidad física que tiene que caber en el contrato

| Dato | Valor | Fuente |
|---|---|---|
| Pipas | 32 | Prensa, octubre 2026 |
| Capacidad por viaje | 10,000 L | Prensa |
| Litros por hogar | ~200 L | Prensa |
| Hogares por viaje | ~50 | Prensa |
| Viajes en 9 días | 565 (≈63 al día, ≈2 por pipa) | Prensa |
| Cisternas comunitarias | 60, ya colocadas | Prensa |
| Canal de solicitud actual | TlaqueChat (WhatsApp) | Prensa |
| Viviendas por manzana (promedio) | ≈37 | Censo, cálculo propio |

Un dato importante que sale de ahí: **una pipa cubre ~50 hogares, y una manzana
promedio tiene ~37 viviendas.** Un viaje equivale aproximadamente a una manzana y
media. Las escalas son compatibles.

### Opciones

**Opción A — asignar por manzana.** Empata perfecto con el modelo y con el mapa.
Pero una pipa no "atiende una manzana": se estaciona en un punto y surte a quien
llega o recorre una ruta. Decir "manda la pipa a la manzana 014" no es una
instrucción que un coordinador pueda ejecutar.

**Opción B — asignar por colonia.** Es como opera el municipio y como se publica el
calendario. Pero es demasiado grueso: una colonia tiene decenas de manzanas con
autonomías muy distintas, y asignar por colonia tira a la basura justo la
resolución por manzana que es nuestra aportación.

**Opción C (recomendada) — decidir por punto de entrega, justificar por manzana.**

```
asignacion_pipas = [{
  dia,
  tipo: "pipa" | "cisterna",
  punto_id,
  colonia,
  cvegeo_centro,                  manzana donde se estaciona
  manzanas_cubiertas: [cvegeo],   las que quedan dentro del radio
  viviendas_objetivo,
  litros,
  viajes,
  personas_beneficiadas,
  prioridad_score,
  orden_del_dia                   para que sea una ruta, no una lista
}]
```

Lo que gana cada quien:

- **Jass** optimiza sobre algo ejecutable y reporta impacto con resolución de manzana.
- **Migue** dibuja "la pipa se para aquí y cubre estas manzanas", que se lee
  muchísimo mejor que un color suelto.
- **El pitch** pasa de "aquí hay rojo" a "hoy, 32 pipas, estos 63 puntos, en este
  orden". Eso suena a herramienta operativa, que es exactamente lo que pide el
  criterio 5 del reto.

**Radio de cobertura:** hace falta un número. Sin datos de rutas, se usa un radio
caminable de **300 metros** o, en su defecto, manzanas adyacentes. Es un supuesto y
se declara.

### El baseline: las 60 cisternas que ya están puestas

Sin baseline bien definido, el delta de impacto no significa nada.

**Lo que no podemos hacer:** afirmar que el reparto actual de pipas es inequitativo.
**No tenemos el registro de a dónde fueron las 565 pipas**, y decirlo sin dato es
exactamente el tipo de afirmación que hunde un proyecto en preguntas.

**Lo que sí tenemos, y es mejor que cualquier supuesto:** las **60 cisternas
comunitarias ya colocadas**, con ubicación pública. Esas cisternas **son** el mapa de
prioridades actual del municipio, revelado por sus propias decisiones. El baseline
deja de ser inventado y pasa a ser observado.

La comparación queda así:

| | Qué mide |
|---|---|
| **Cobertura actual** | Personas-hora sin agua considerando solo las 60 cisternas donde están hoy |
| **Cobertura priorizada** | Las mismas 60 cisternas más las pipas asignadas por riesgo |

Y por separado, claramente etiquetado como **escenario hipotético**, se puede mostrar
qué pasaría si las solicitudes por TlaqueChat se concentraran en las zonas con menos
marginación. Eso ilustra el riesgo de un sistema por demanda **sin acusar a nadie de
nada**.

> **Acción barata que sigue valiendo:** pedir por transparencia el registro de viajes
> de pipa de octubre y noviembre. Es un correo. Si llega, el baseline de pipas
> también deja de ser supuesto.

### Dos horizontes, no uno

El contrato debe soportar dos decisiones distintas, y la segunda sale casi gratis:

1. **`asignacion_pipas`** — decisión **diaria**: a dónde van las pipas hoy.
2. **`propuesta_cisternas`** — decisión **estructural**: dónde convendría colocar
   cisternas permanentes, dado el patrón de autonomía.

La segunda es más valiosa para el municipio que la primera, porque resuelve el
problema en lugar de administrarlo, y se calcula con el mismo modelo. Dejarla fuera
del contrato ahora significa no poder agregarla el viernes.

### Función objetivo

```
minimizar   Σ (personas × horas_sin_agua × peso_vulnerabilidad)

sujeto a    Σ litros ≤ pipas × viajes_por_dia × 10,000
            cada punto cubre manzanas dentro del radio
            las 60 cisternas están en ubicaciones ya dadas
```

`peso_vulnerabilidad` viene del dataset 17 (marginación, CONAPO).

---

## Riesgos que cruzan las cuatro decisiones

### 🔴 Riesgo 1 — Podemos incumplir un requisito obligatorio sin notarlo

Los dos datasets obligatorios del catálogo son el **01** (INEGI, viviendas por
manzana) y el **17** (CONAPO, marginación). El 01 ya está usado a fondo.

**Pero el 17, tal como está el plan hoy, se usa en un solo lugar: el
`peso_vulnerabilidad` de la función objetivo de Jass.** Si el priorizador se
retrasa, se simplifica o termina sin pesos, **perdemos uno de los dos datasets
obligatorios** y lo descubrimos cuando ya no hay tiempo. El kit es explícito:
*"Mencionar la fuente sin usar sus datos no cuenta."*

**Mitigación: usar el dataset 17 en dos lugares independientes.**

1. En la **caracterización del problema** (sección de Magui): quiénes viven en las
   manzanas sin almacenamiento, cruzando marginación con el Censo. Esto no depende
   de que el optimizador funcione.
2. En el **peso de la función objetivo** (Jass), como ya está previsto.

Con eso, el requisito se cumple aunque el carril de Jass se complique.

> **Nota técnica:** la marginación de CONAPO se publica **por AGEB**, no por manzana.
> El peso se aplica al AGEB y lo heredan sus manzanas. Hay que decirlo en el
> reporte, no esconderlo. (Verificar la unidad exacta al descargarlo.)

### 🟡 Riesgo 2 — Supuestos que se vuelven invisibles

Cada decisión de arriba mete al menos un supuesto. Si viven dispersos en el código,
el sábado nadie los recuerda y el reporte queda incompleto justo en lo que el kit
pide declarar.

**Mitigación: un solo archivo `supuestos.md` en la raíz del repo**, con una línea
por supuesto: qué es, qué valor tiene, de dónde salió y qué tan sensible es el
resultado. Se llena conforme se decide, no al final.

Lista inicial:

| Supuesto | Valor | Origen |
|---|---|---|
| Capacidad de tinaco | 1,100 L | Tamaño residencial común. Se calibra con la pregunta 3 |
| Capacidad de cisterna | 5,000 L | Estimado. Sin fuente aún |
| Consumo por persona | 50 L/día | Nivel básico OMS. Reportar también a 100 |
| Umbral U de agua guardada | 48 h | Literatura. Sensibilidad a 24/48/72 |
| Radio de cobertura de pipa | 300 m | Supuesto nuestro |
| Baseline de cobertura | Las 60 cisternas ya colocadas | Ubicación publicada por el municipio |
| Traslape tinaco/cisterna | Desconocido | Por eso todo va en rango min–max |

### 🟡 Riesgo 3 — Las tres citas sin verificar

Maputo (85% en 2-3 días), la frase atribuida a la OMS y la revisión de 2026 siguen
sin confirmarse contra la fuente primaria. **La de Maputo es la que sostiene el
umbral U = 48 h.** Si no se confirma, U sigue siendo defendible por sensibilidad,
pero el argumento pierde fuerza. Verificarlas es una tarea de una hora y hay que
hacerla antes de que entren al reporte.

### 🟡 Riesgo 4 — Divergencia silenciosa entre carriles

El escenario que más miedo debería darnos: Dani programa un enum, Jass lee otro, y
nos enteramos el jueves durante la integración, que es la única parte secuencial del
plan.

**Mitigación barata: los fixtures son la prueba.** Si el fixture de `estado` tiene
exactamente los valores del enum acordado, y Jass desarrolla contra ese fixture, la
divergencia es imposible. **Por eso los fixtures se actualizan en el mismo commit en
que se cambia un contrato, nunca después.**

---

## Resumen de lo que propongo

| # | Decisión | Propuesta |
|---|---|---|
| 1 | Evidencia propia | **Se cancela la encuesta.** En su lugar: contraste contra las 60 cisternas ya colocadas y análisis de sensibilidad. `mediciones` pasa a ser `evidencia` |
| 2 | Enum de estado | Escalera de 4 niveles con `sin_agua_sin_respaldo` en vez de `fuente_riesgosa`. U = 48 h como configuración, con sensibilidad |
| 3 | Granularidad | Día en el contrato y la interfaz, horas en el cálculo interno. Campo opcional de hora para el futuro |
| 4 | Salida del plan | Punto de entrega como unidad de decisión, manzanas cubiertas como justificación. **Baseline observado: las 60 cisternas actuales.** Agregar `propuesta_cisternas` |

Y lo que pido que no se nos pase: **usar el dataset 17 en dos lugares**, y abrir
`supuestos.md` hoy.
