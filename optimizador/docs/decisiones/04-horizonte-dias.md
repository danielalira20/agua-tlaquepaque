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

**(a) con racha, usando la racha como desempate.** Se reparte cada fecha por separado. Al
elegir cada viaje, primero se busca atender al mayor número de viviendas sin agua; entre
opciones que atienden a las mismas, va primero la que lleva más días seguidos sin
servicio (`peso = horas_sin_servicio / 24`, sección 4 de `ESPECIFICACION.md`).

La racha como **peso** (`modo_racha = peso`) se reporta como escenario de equidad, y sin
racha (`modo_racha = no`) como referencia.

## Por qué

1. **La opción (b) no cambia el resultado con los datos que hay.** Planear la semana solo
   mejora algo si lo que se hace un día afecta al siguiente. Aquí nada pasa de un día a
   otro: la entrega dura un día, las viviendas en riesgo no tienen dónde guardar agua y
   los viajes se reponen cada día. Lo mejor de la semana es la suma de lo mejor de cada día.
2. **La racha como peso tiene un costo real.** Con un prototipo sobre el estado real
   (cota mínima, 63 viajes de 50 hogares), el 9 de noviembre la racha como peso atiende
   2,794 viviendas en lugar de 3,150 (11% menos) para llegar antes a las que llevan más
   días. El 13 de noviembre atiende 3,067 (3% menos).
3. **Como desempate no cuesta nada.** Atiende las 3,150 viviendas, el máximo posible, en
   los dos días, y aun así favorece a quien lleva más días cuando hay opciones iguales.
4. Elegir entre atender a más gente o atender primero a quien lleva más tiempo es una
   decisión de política pública, no algo que los datos resuelvan: no se sabe cuánto daño
   extra causa cada día adicional. Por eso el modo es un parámetro y el reporte muestra
   los dos.

Las cifras son preliminares: salen de un prototipo desechable con dos fechas. Se
recalculan con la implementación de referencia.

La semana sigue presente en los resultados: además de las personas-día sin agua evitadas,
se reporta cuántas viviendas no recibieron ninguna entrega en los siete días.

## Cuándo revisar esta decisión

Si aparece un dato de cuánta agua guardan en cubetas o tambos las viviendas sin tinaco ni
cisterna, una entrega podría durar más de un día y la opción (b) empezaría a aportar.

## Qué se declara

- Que el reparto es diario y no planea a varios días, y por qué.
- Que la racha usa las horas sin servicio del calendario vigente del SIAPA.
- El costo en viviendas atendidas de usar la racha como peso.
