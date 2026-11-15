# Decisiones de Fase 0

Cada integrante escribe su propia propuesta para las 4 decisiones que hay que
cerrar antes de programar. Después se comparan en la junta y se elige.

    propuesta-dani.md
    propuesta-jass.md      (no se escribió aparte: las decisiones del carril B están en
                           `optimizador/docs/decisiones/`, 01 a 07)
    propuesta-magui.md     (pendiente)
    propuesta-migue.md

## Las 4 decisiones

1. **La evidencia propia.** Se cancela la encuesta. Qué la sustituye y cómo se
   declara en el reporte. El contrato `mediciones` pasa a ser `evidencia`.
2. **`estado.schema.json`.** El enum de estados y el umbral de horas a partir del
   cual el agua guardada se marca.
3. **Granularidad del ciclo.** Por dia o por hora.
4. **`plan.schema.json`.** Cual es la unidad de salida del priorizador: manzana,
   colonia o punto de entrega.

## Regla que aplica salga lo que salga

Cuando se cambia un contrato, **su fixture se actualiza en el mismo commit**. Los
fixtures son lo que impide que dos carriles se separen sin que nadie lo note.

## Resolución de la decisión 4 (11-nov-2026)

**Aprobada: opción C** (decidir por punto de entrega, justificar por manzana).
Propuesta de Dani; a favor Migue y Jass. Jass la vota con tres cambios, que el contrato
`plan.schema.json` (v2) ya recoge:

1. **El baseline son 50 cisternas, no 60.** Las 10 propuestas no son cobertura. De las 50, 35
   tienen coordenada exacta, 12 se ubican en el centro de su colonia y 3 quedan fuera
   (CIST014, CIST021, CIST022).
2. **`orden_del_dia` y la ruta quedan fuera de la primera versión.** No hay datos de calles ni de
   tiempos. Queda `orden_eleccion`, que no es una ruta.
3. **El radio de 300 m es un parámetro declarado**, con sensibilidad a 200 y 500 m.

Cambia además lo que yo había propuesto para el baseline: en lugar de comparar "solo cisternas"
contra "cisternas + pipas", se comparan **los mismos viajes con dos reglas** (a las cisternas
instaladas por turnos, o por necesidad). Así la diferencia sale de la regla y no de tener más
recursos. Es un baseline **estilizado**, no el reparto real del municipio, del que no hay registro.
Detalle en `optimizador/ESPECIFICACION.md`, sección 7 (rama `feat/priorizador-especificacion`).

Pendiente: `propuesta_cisternas` queda reservada en el contrato y sin calcular.

## Resolución de la decisión 1 (11-nov-2026)

**Aprobada: se cancela la encuesta.** Propuesta de Dani; a favor Migue. No hay voto de Jass ni de
Magui registrado en el repo sobre esta decisión.

La evidencia propia sale de dos cosas que no dependen de conseguir gente que responda: el contraste
contra las cisternas que el municipio ya colocó, y el análisis de sensibilidad. El contrato
`mediciones` pasa a ser `evidencia` (`contratos/evidencia.schema.json`, v2) y el registro vive en
`datos/evidencia.csv`: 60 renglones de cisternas (50 más 10 propuestas), valores de literatura y
datos de prensa, cada uno con su cita y su nivel de verificación (`fuente_primaria`, `solo_resumen`,
`norma` o `no_verificada`).

Ese campo es lo que impide citar algo que no se leyó. Tras la revisión del 11-nov (ver
`referencias-y-prensa.md`) hay 6 referencias arbitradas leídas completas, 2 con resumen oficial, las notas
de prensa leídas completas, y 1 sin verificar: el factor 1.5 de decaimiento del cloro, marcado NO USAR.

**Resultado del análisis de sensibilidad (12-nov-2026)**, que es lo que sustituye a la encuesta (`datos/HALLAZGOS_sensibilidad.md`):
la hipótesis de la propuesta, que el orden de las manzanas casi no cambia entre los extremos, **no se sostiene** para el orden
individual de cada manzana (rho de Spearman mediano 0.65 con los rangos de la decisión). Sí se sostienen conclusiones más
específicas: un núcleo de 186 manzanas que queda entre las 250 más críticas en el 90% de las simulaciones, El Sauz como
primera colonia en todas, y una ventaja del priorizador que se sostiene en todos los escenarios probados, aunque su tamaño depende de la cota y del baseline (de 1.1 a 6.4 veces; ver `datos/HALLAZGOS_sensibilidad.md`). Lo que decide todo es cuántos días
aguanta un tinaco, y eso el Censo no lo dice.

**Lo único que no se puede hacer** sigue siendo lo que dice la propuesta: quitar la encuesta en silencio
y aun así escribir "validamos". En el reporte va una línea que diga qué se hizo en su lugar y por qué.

## Resolución de la delimitación (12-nov-2026)

**Aprobada: opción B**, las colonias de Tlaquepaque dentro del programa de racionamiento (zonas 3 a 6).
Propuesta de Dani; a favor Jass, Migue y Magui (4 de 4). Razones: sigue siendo un solo municipio con calendario
publicado, incluye a El Sauz y casi todo el riesgo (las zonas 5 y 6 concentran el 72.6% con la cota mínima y el 63.0% con la máxima), y el portal ya trae la zona
de cada colonia.

Cifras con su advertencia: 462,194 personas en el programa (78.6%); 368,111 (62.6%) con respaldo de la lista
oficial del SIAPA y 94,083 (16.0%) solo por el polígono del portal. Se reporta como rango de 63% a 79%. Detalle en
`datos/zonas_siapa/LEEME.md` y `datos/HALLAZGOS_zonas.md`.

## Resolución de la decisión abierta 4 del motor: marginación en `severidad` (12-nov-2026)

**Aprobada: opción A.** `severidad` queda **sin peso de marginación**: es exposición pura. La marginación (CONAPO,
nivel AGEB) va como **capa aparte** en el mapa y en las tablas. Confirmada por Dani; a favor Jass.

Por qué: el grado "Muy bajo" concentra la mayor parte del riesgo de almacenamiento (50.2% con la cota mínima, 32.8% con la
máxima), así que ponderar por marginación movería viajes de ahí a las AGEB "Alto" (17.4% con la cota mínima, 22.1% con la
máxima) y sacaría a El Sauz del primer lugar. Además
se perdería el argumento más limpio del priorizador: alcanza el 100% del máximo posible con los mismos viajes.
Detalle en `datos/HALLAZGOS_marginacion.md`.

**Condición, para que la equidad se vea medida y no supuesta:** el comparador del priorizador (carril de Jass) agrega
una tabla de viviendas-día atendidas por grado de marginación, priorizado contra baseline, **con las dos cotas**.
Un cálculo preliminar de Dani con los datos reales de la semana del 9 al 15 de noviembre muestra un costo que hay que
declarar: con la cota máxima el priorizado atiende 0 de las 2,091 viviendas-día en AGEB "Muy alto" (el baseline
atiende 661), porque maximizar viviendas atendidas ignora los bolsones pequeños. Con la cota mínima la cobertura de
"Muy alto" es 26.8%, contra 32.9% del baseline. Queda como sensibilidad opcional un escenario con una reserva mínima de
viajes para las AGEB Alto y Muy alto.
