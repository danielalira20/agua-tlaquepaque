# 07 · Costo de un viaje de pipa

Estado: Aceptada

## Contexto

El criterio 5 del kit pide viabilidad presupuestal. El priorizador no agrega viajes: cambia a
dónde van los mismos 63 viajes de cada día. Para decir cuánto vale eso en pesos hace falta el
costo de un viaje.

El municipio no publica cuánto le cuesta un viaje: opera pipas propias y las llena con agua de
pozos municipales (`datos/evidencia.csv`, P006 y P007). En la búsqueda del 12 de noviembre
tampoco apareció un contrato público con precio por viaje de pipa en el área metropolitana, ni
una tarifa de pipa del SIAPA.

## Opciones

- **Precio de una pipa particular de 10,000 L en Tlaquepaque**, publicado por la prensa.
- **Estimar el costo del municipio** (combustible, operador, mantenimiento, agua del pozo):
  cada componente sería un supuesto sin fuente.
- **No poner pesos.** El reporte se quedaría sin cifra para el criterio 5.

## Decisión

**Precio de referencia: 1,200 pesos por viaje de 10,000 L**, el promedio para Tlaquepaque de
las empresas privadas que publicó Milenio el 16 de mayo de 2025 (P012). **Sensibilidad: 700
y 2,000 pesos**: 700 es el de Tonalá en la misma nota, y 2,000 es lo que una vecina dice que
cobran algunos proveedores (La Crónica, 15 de octubre de 2026; P011).

Los valores viven en `supuestos.json` (`costo_viaje_mxn` y su sensibilidad). El comparador
(decisión 06) calcula, para el priorizado y cada baseline, con las dos cotas:

```
costo por vivienda-día atendida = costo_viaje_mxn × viajes usados ÷ viviendas-día atendidas
```

Un viaje vacío del baseline cuenta como usado: la pipa sale aunque no encuentre a quién
atender.

## Por qué

1. Es la única cifra publicada por municipio y para la capacidad de un viaje (10,000 L).
2. El priorizado y el baseline usan los mismos viajes, así que cuestan lo mismo. Lo que cambia
   es cuántas viviendas atiende cada peso, y esa razón no depende del precio: es igual con 700
   que con 2,000.
3. Es lo que pagaría una familia por su cuenta, así que también dice cuánto vale el servicio
   que el municipio da gratis.

## Qué se declara

- Es el precio de una pipa particular, no el costo del municipio, que no publica el suyo.
- El dato es de mayo de 2025 y no se ajustó por inflación. La nota no dice cómo obtuvo los
  promedios ni cuántas empresas consultó. Telediario repitió las mismas cifras el 20 de mayo de
  2025 (P013): es la misma fuente, no una segunda.
- El precio sube con la distancia al punto de entrega.
- El costo por vivienda-día es una forma de leer la misma ventaja del priorizado en pesos; no
  es un ahorro de presupuesto, porque los viajes son los mismos.
