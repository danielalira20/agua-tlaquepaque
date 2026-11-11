# 04 · Horizonte: día por día con racha

Estado: Propuesta

## Contexto

Una entrega de 200 L cubre aproximadamente un día de un hogar (3.7 personas × 50 L ≈
185 L). Una vivienda sin almacenamiento en la zona 4, que tiene cuatro días seguidos de
racionamiento, necesita una entrega cada uno de esos días. Hay que decidir si el
priorizador decide cada día por separado o planea la semana completa.

## Opciones

- **(a) Día por día.** Cada fecha se reparte según quién está sin agua ese día.
- **(b) Semana completa.** Se optimizan los siete días a la vez.
- **(a) con racha.** Se decide día por día, pero la prioridad aumenta con los días
  seguidos que la manzana lleva sin agua.

## Decisión

**(a) con racha.** Se reparte cada fecha por separado. La prioridad de una manzana
considera cuántas viviendas tiene sin agua y cuánto tiempo llevan así, con el dato
`horas_sin_servicio` que ya entrega el motor. La fórmula exacta se fija en
`ESPECIFICACION.md`.

## Por qué

1. **La opción (b) no cambia el resultado con los datos que hay.** Planear la semana solo
   mejora algo si lo que se hace un día afecta al siguiente. Aquí nada pasa de un día a
   otro: la entrega dura un día, las viviendas en riesgo no tienen dónde guardar agua y
   los viajes se reponen cada día. Lo mejor de la semana es la suma de lo mejor de cada día.
2. **La racha sí cambia el reparto.** Entre dos manzanas con las mismas viviendas sin agua,
   se atiende primero la que lleva más días así. Conecta con la tesis: a más tiempo sin
   agua, más riesgo para la salud.
3. Se puede probar con casos resueltos a mano y no necesita bibliotecas externas.

La semana sigue presente en los resultados: además de las personas-día sin agua evitadas,
se reporta cuántas viviendas no recibieron ninguna entrega en los siete días.

## Cuándo revisar esta decisión

Si aparece un dato de cuánta agua guardan en cubetas o tambos las viviendas sin tinaco ni
cisterna, una entrega podría durar más de un día y la opción (b) empezaría a aportar.

## Qué se declara

- Que el reparto es diario y no planea a varios días, y por qué.
- Que la racha usa las horas sin servicio del calendario vigente del SIAPA.
