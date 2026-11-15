# Viabilidad presupuestal

Criterio 5 del kit. Texto base para la sección de viabilidad del reporte (carril B). Las cifras
del priorizador salen de `resultados/resumen.md` (sección 6), que se regenera con
`python3 -m optimizador.analisis`; las de este documento son las de la semana del 9 al 15 de
noviembre de 2026 con el motor de referencia. Las fuentes van por su id en `datos/evidencia.csv`.

## 1. Alcance: qué cuesta y qué no

Este documento costea una sola cosa: operar con pipas los mismos viajes que el municipio ya hace.
No costea cisternas, ni las nuevas ni las que ya existen.

- **La propuesta no compra pipas ni cisternas.** El priorizador reparte los 63 viajes diarios que
  el municipio ya hace (sección 2). No agrega viajes ni infraestructura.
- **Las 10 ubicaciones de cisternas propuestas son un plan del municipio y no se costean.** No son
  cisternas instaladas, no hay un precio con fuente para construirlas ni operarlas, y quedan fuera
  de los cálculos del modelo (decisión 01). Su ubicación se analiza en
  `datos/HALLAZGOS_cisternas.md`.
- **Una cisterna no ahorra viajes de pipa.** Las cisternas se llenan con pipas cuando los vecinos
  reportan que están vacías (P006) y son de 10,000 L, un viaje completo (P007). Construir una
  cambia dónde se descarga el agua, no cuántos viajes hacen falta; por eso no se presenta como
  ahorro.
- **Las cisternas instaladas entran solo como comparación.** El baseline manda los mismos viajes
  por turnos entre las 47 cisternas que se pudieron ubicar, así que cuesta lo mismo que el
  priorizado (sección 4).
- **El priorizador decide a dónde van los viajes; no retira ni instala cisternas, y el modelo no
  simula cómo se rellenan.** No hay registro de los reportes ni de a dónde fueron los viajes
  (decisión 01). El modelo supone que los 63 viajes diarios están libres para repartirse. Si una
  parte ya está comprometida con llenar cisternas, la ventaja del priorizado sería menor.

## 2. La propuesta no pide más pipas

El priorizador no agrega viajes ni pipas: decide a dónde van los mismos 63 viajes diarios que el
municipio ya hace (565 viajes en los primeros nueve días del operativo de octubre; P004). Su
costo de operación es el de la herramienta (sección 5), no el del agua.

## 3. Costo de un viaje de pipa

El municipio no publica cuánto le cuesta un viaje: usa pipas propias y agua de sus pozos (P006,
P007). Como referencia se usa el precio de mercado (decisión 07):

| | Pesos por pipa de 10,000 L | Fuente |
|---|---:|---|
| **Tlaquepaque, empresas privadas (referencia)** | **1,200** | Milenio, 16 de mayo de 2025 (P012) |
| Tonalá, empresas privadas (cota baja) | 700 | Misma nota |
| Testimonio de una vecina (cota alta) | 2,000 | La Crónica, 15 de octubre de 2026 (P011) |

Telediario publicó las mismas cifras el 20 de mayo de 2025 (P013); es la misma fuente, no una
segunda. El precio sube con la distancia al punto de entrega.

## 4. Cuánto rinde cada peso

Con los mismos viajes, el costo es el mismo para cualquier regla de reparto; lo que cambia es
cuántas viviendas atiende. A 1,200 pesos por viaje, los 441 viajes de la semana cuestan
529,200 pesos.

| Costo por vivienda-día atendida | Cota mínima | Cota máxima |
|---|---:|---:|
| **Priorizado** | **24.0 pesos** | **24.0 pesos** |
| Baseline con necesidad, 47 cisternas (la comparación más conservadora) | 74.8 pesos | 33.2 pesos |
| Baseline por turnos, 47 cisternas | 116.8 pesos | 52.0 pesos |

Con el viaje a 700 pesos, el priorizado sale en 14.0 pesos por vivienda-día; a 2,000, en 40.0.
La razón contra cada baseline no depende del precio. En las esquinas adversas de la
sensibilidad del motor, cuando casi todas las zonas se quedan sin agua, la ventaja contra el
baseline con necesidad, 47 cisternas, baja a 1.2 veces con la cota mínima y a 1.1 con la máxima
(`resultados/resumen.md`, sección 3): el priorizado rinde más cuando el desabasto se concentra en
unas zonas y no en otras.

Leído desde la familia: 24 pesos es lo que costaría, a precio de mercado, el agua que recibe
cada vivienda atendida en un día (200 L). El municipio la entrega gratis.

## 5. Costo de operar la herramienta

| Componente | Costo | Evidencia |
|---|---|---|
| Cálculo | Ninguno adicional: Python con solo la biblioteca estándar, sin licencias. El plan de una semana se calcula en unos 3 segundos y las tablas del reporte en menos de un minuto, en una laptop | Medido en el repo |
| Datos | Gratuitos y públicos: Censo 2020 (INEGI), calendario y zonas del SIAPA, marginación (CONAPO), mapa de cisternas del municipio | `datos/FUENTES.md` |
| Publicación de la app | La app se exporta como sitio estático (`app/README.md`), que puede servirse desde un servidor web que el municipio ya tenga | Supuesto: no se cotizó hosting |
| Personal | La coordinación del operativo ya existe (Protección Civil, Agua Potable y Parques y Jardines; P004). La herramienta le entrega la lista de puntos del día; hay que capacitar a quien la use | No cuantificado |
| Mantenimiento | Actualizar el calendario cuando el SIAPA lo cambie y volver a calcular el plan cuando cambie un supuesto | `datos/HALLAZGOS_sensibilidad.md` |

## 6. Recursos del municipio

| Recurso | Cifra | Fuente |
|---|---|---|
| Presupuesto de egresos 2026 | 3,174 millones de pesos | La Crónica, 8 de diciembre de 2025 (P014) |
| Obras y acciones hidráulicas en la administración, incluido el abasto con pipas y cisternas | Más de 400 millones de pesos | La Crónica, 15 de julio de 2026 (P015) |
| Rehabilitación y equipamiento de pozos (21 pozos de las zonas que el municipio abastece directamente) | Más de 23.5 millones de pesos | La Crónica, 30 de agosto de 2026 (P016) |
| Pipas | 24 en julio; 32 en octubre, presentadas como meta | P007; `decisiones/referencias-y-prensa.md` |
| Cisternas comunitarias de 10,000 L | 55 en julio; 60 en octubre | P007; P003 |

Una semana del operativo a precio de mercado (529,200 pesos) equivale a cerca de 0.02% del
presupuesto anual de 2026. La herramienta no compite por ese presupuesto: hace que la misma
semana atienda más viviendas.

## 7. Lo que se declara

- El costo de un viaje es el precio de una pipa particular, no el costo del municipio, que no lo
  publica. Es un dato de mayo de 2025, sin ajustar por inflación, y la nota no dice cómo obtuvo
  los promedios (decisión 07).
- El costo por vivienda-día es otra forma de leer la ventaja del priorizado; no es un ahorro de
  presupuesto, porque los viajes son los mismos.
- Las cifras de inversión son las que declara el propio Ayuntamiento a la prensa; no se
  verificaron contra la cuenta pública.
- No se cotizó hosting ni capacitación.
- El alcance es la operación con pipas: las cisternas no se costean (sección 1).
- El baseline es estilizado: no es el reparto real del municipio, que responde a reportes de los
  vecinos (P006).
