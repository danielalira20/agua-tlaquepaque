# Decisiones de Fase 0

Cada integrante escribe su propia propuesta para las 4 decisiones que hay que
cerrar antes de programar. Después se comparan en la junta y se elige.

    propuesta-dani.md
    propuesta-jass.md      (pendiente)
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

**Lo único que no se puede hacer** sigue siendo lo que dice la propuesta: quitar la encuesta en silencio
y aun así escribir "validamos". En el reporte va una línea que diga qué se hizo en su lugar y por qué.
