# 03 · Radio de cobertura de un punto de entrega

Estado: Propuesta

## Contexto

Una pipa no "atiende una manzana": se estaciona en un punto y la gente llega con sus
recipientes. Hay que definir hasta qué distancia se considera que una vivienda puede
recibir agua de ese punto. No hay datos de rutas ni de la distancia que la gente camina
de verdad, así que es un supuesto.

## Opciones

- **Radio fijo de 300 m**, propuesto por Dani en la decisión 4 del equipo.
- **Manzanas adyacentes**, que depende de la geometría y no de una distancia.
- **Radio como cobertura completa:** todas las viviendas dentro del radio cuentan como
  atendidas.
- **Radio como tope:** el radio solo limita hasta dónde se puede llegar; quién se atiende
  lo decide la capacidad del viaje.

## Decisión

**300 m como tope**, no como cobertura. El agua de un viaje se reparte primero entre las
viviendas sin agua de la manzana donde se estaciona la pipa y después entre las vecinas,
de la más cercana a la más lejana, hasta agotar los 10,000 L o llegar a 300 m. Se corre
con 200 y 500 m como sensibilidad.

## Por qué

En 300 m caben muchas más viviendas de las que alcanza un viaje. Estimación preliminar
con una muestra aleatoria de 400 manzanas y distancia aproximada entre centroides:

| Radio | Manzanas vecinas (mediana) | Percentil 10 | Percentil 90 |
|---|---:|---:|---:|
| 200 m | 10 | 4 | 18 |
| 300 m | 20 | 10 | 36 |
| 500 m | 50 | 27 | 84 |

Con unas 30 a 37 viviendas por manzana, 300 m abarca cientos de viviendas, y un viaje
alcanza para unos 50 hogares. Si el radio contara como cobertura completa, inflaría el
impacto. Como tope, el límite real lo pone la capacidad de la pipa.

`priorizador/cobertura.py` recalcula estas cifras con todas las manzanas.

## Qué se declara

- Que 300 m es un supuesto de distancia caminable, sin datos de rutas.
- Que la distancia se mide en línea recta entre centroides de manzana.
- La sensibilidad a 200 y 500 m.
