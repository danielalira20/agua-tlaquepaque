# Decisiones de Fase 0

Cada integrante escribe su propia propuesta para las 4 decisiones que hay que
cerrar antes de programar. Después se comparan en la junta y se elige.

    propuesta-dani.md
    propuesta-jass.md      (pendiente)
    propuesta-magui.md     (pendiente)
    propuesta-migue.md     (pendiente)

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
