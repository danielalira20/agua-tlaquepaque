# 05 · Algoritmo voraz con comparación contra el máximo

Estado: Aceptada

## Contexto

Cada día hay que elegir los centros de unos 63 viajes entre cientos de manzanas con
viviendas sin agua. Encontrar el reparto exacto que maximiza las viviendas atendidas es un
problema de optimización combinatoria: con un solver (programación entera) se puede
resolver, pero agrega dependencias y es difícil de verificar a mano.

## Opciones

- **Voraz:** en cada paso se elige el viaje que más atiende, se descuenta y se repite.
- **Solver exacto:** programación entera con `pulp` u OR-Tools.

## Decisión

**Voraz**, y en las métricas se compara contra el **máximo posible**: lo que se
lograría si cualquier viaje pudiera llegar a cualquier vivienda (sección 8 de
`ESPECIFICACION.md`).

## Por qué

1. Con el estado real (cota mínima, `modo_racha = desempate`, 9 y 13
   de noviembre), el voraz llena los 63 viajes y atiende 3,150 viviendas, que es
   exactamente el máximo posible. Para esa métrica es óptimo: un solver no podría
   atender más.
2. Con la racha como peso, el voraz queda en 90.1% y 95.1% del máximo ponderado. Ese
   máximo ignora la geografía y es generoso, así que el óptimo real está todavía más
   cerca.
3. Es determinista, usa solo la biblioteca estándar y se puede comprobar con los casos
   resueltos a mano.
4. La comparación contra el máximo convierte "no garantiza el óptimo" en una cifra:
   cuánto se aleja del mejor resultado posible.

Las cifras salieron primero de un prototipo y la implementación de referencia
(`python3 -m optimizador.priorizador`) las reproduce exactamente; con ella, el voraz llega
al 100% del máximo de viviendas en las siete fechas del 9 al 15 de noviembre. Usan el
estado del motor de referencia; se recalculan cuando esté el estado oficial.

## Cuándo revisar esta decisión

Si con la implementación de referencia la eficiencia en viviendas baja claramente de
100% en algún escenario de la sensibilidad, vale la pena probar un solver exacto en ese
escenario.

## Qué se declara

- Que el reparto se calcula con un algoritmo voraz.
- La eficiencia contra el máximo posible en cada escenario.
