# 02 · Cota mínima o máxima para ordenar

Estado: Propuesta

## Contexto

El motor no entrega un solo número de viviendas sin agua por manzana y fecha, sino un
intervalo (`viv_sin_agua_min` a `viv_sin_agua_max`). Es así porque el Censo 2020 no cruza
tinaco con cisterna: solo se sabe que las viviendas con ambos están entre
`max(0, T + C − V)` y `min(T, C)`. El priorizador necesita un número para decidir qué
manzanas van primero.

## Opciones

- **Cota mínima.** Solo cuenta las viviendas que están sin agua con cualquier combinación
  posible de tinaco y cisterna.
- **Cota máxima.** Cuenta también las que podrían estar sin agua.
- **Punto medio.** No tiene respaldo: el Censo no dice que el valor real esté a la mitad.

## Decisión

Se ordena con la **cota mínima**. Se corre también con la **cota máxima** como
sensibilidad, y el impacto se reporta como intervalo.

## Por qué

1. Con la cota mínima, cada viaje va a viviendas que **seguro** están sin agua. Nadie
   puede objetar que la pipa fue a donde quizá no hacía falta.
2. Es coherente con el resto del proyecto, que reporta toda cifra como intervalo.
3. El cuello de botella existe con cualquiera de las dos cotas, así que la elección no
   cambia la conclusión. Con el calendario vigente, 50 L por persona al día y `f = 0`,
   la semana del 9 al 15 de noviembre tiene entre 7,781 y 9,215 viviendas sin agua al
   día con la cota mínima, y entre 17,255 y 19,510 con la máxima. Los viajes disponibles
   cubren unos 3,150 hogares al día (63 viajes × 50 hogares).

Cifras preliminares: salen de `motor/referencia.py` sobre el commit 29fb0ad. Se recalculan
con la implementación oficial.

## Qué se declara

- Que el orden de atención usa la cota mínima y por qué.
- El impacto con las dos cotas, como intervalo.
