# 06 · Rejilla del comparador: qué se corre y qué tablas salen

Estado: Aceptada

## Contexto

Las cifras del priorizador salen hoy de corridas sueltas del comando, a mano. Para el
reporte hace falta un solo comando que produzca todas las tablas, siempre iguales, y que
responda tres preguntas:

1. Cuánto cambia la ventaja del priorizado cuando cambian sus propios parámetros (radio,
   racha) y el baseline contra el que se compara.
2. Si la comparación más conservadora (baseline con necesidad, cota máxima: 1.4 veces) se
   sostiene cuando el motor supone que los tinacos aguantan menos. La sensibilidad del
   motor (`datos/HALLAZGOS_sensibilidad.md`) midió la ventaja solo contra el baseline por
   turnos (2.6 a 4.9 veces en Monte Carlo); contra el baseline con necesidad no se midió.
3. A quién llegan los viajes según el grado de marginación de su AGEB. Es la condición de
   la opción A de la decisión abierta 4 del motor (`decisiones/README.md`): la marginación
   no pesa en la prioridad, así que la equidad se mide aparte, con las dos cotas.

Restricción: `scripts/exporta_app.py` y la app usan el comando
`python3 -m optimizador.priorizador` y el contrato `plan` v2. Ninguno de los dos cambia.

## Opciones

- **Cruce completo** de los parámetros del priorizador con los escenarios del motor: 36
  combinaciones por escenario, cada una con 4 corridas. La mayoría de esas celdas no se
  usaría en el reporte.
- **Rejilla del priorizador sobre el estado base, más unos pocos escenarios del motor con
  los parámetros base.**
- **Solo el caso base.** No responde las preguntas 1 ni 2.

## Decisión

La segunda opción. Un módulo aparte, `python3 -m optimizador.analisis`, corre el motor de
referencia (`motor/referencia.py`) y el priorizador como biblioteca, y escribe en
`optimizador/resultados/`:

| Archivo | Qué contiene |
|---|---|
| `rejilla_priorizador.csv` | Estado base. `modo_racha` (desempate, peso, no) × radio (200, 300 y 500 m) × `baseline_turnos` (todas, con_necesidad) × `baseline_cisternas` (todas, exactas): 36 combinaciones, con las dos cotas |
| `escenarios_motor.csv` | El caso base y las tres esquinas de la sensibilidad del motor (favorable, adversa y adversa extrema), con los parámetros base del priorizador y los 4 baselines, con las dos cotas |
| `equidad_marginacion.csv` | Estado y parámetros base: viviendas-día sin agua y atendidas por grado de marginación, priorizado contra los dos baselines de 47 cisternas, con las dos cotas |
| `cobertura_diaria.csv` | Estado base: por fecha, viviendas sin agua y atendidas, con las dos cotas |
| `resumen.md` | Las tablas que van al reporte y lo que se declara |

Detalles:

- **Cada regla se corre solo con los parámetros que usa.** El priorizado depende de la
  cota, `modo_racha` y el radio; el baseline, de la cota, el radio, `baseline_turnos` y
  `baseline_cisternas`. La rejilla son 9 corridas del priorizado y 12 del baseline por
  cota (42 en total) en lugar de 144, con el mismo resultado. Una prueba lo comprueba.
- **Las esquinas del motor son las de Dani** (`ESQUINAS` en `scripts/sensibilidad_orden.py`).
  Se copian a `optimizador/analisis/escenarios_motor.json` porque ese script usa numpy y
  pandas, y este carril solo la biblioteca estándar. Una prueba falla si las dos copias
  dejan de coincidir.
- **El grado de marginación de una manzana es el de su AGEB:** los primeros 13 caracteres
  del `cvegeo` contra `CVE_AGEB` de `datos/marginacion_ageb_tlaquepaque.csv`. Las manzanas
  cuya AGEB no está en el índice van como «sin dato».
- **Salida determinista:** sin fecha de corrida, con orden y decimales fijos, para que dos
  corridas den archivos idénticos y el diff de git muestre solo cambios reales.

## Por qué

1. Responde las tres preguntas sin el cruce completo, que multiplica las corridas sin dar
   celdas que el reporte vaya a usar.
2. No repite la sensibilidad del motor: Dani ya midió el orden de las manzanas y la
   ventaja contra el baseline por turnos en 36 escenarios y 600 simulaciones. Aquí solo
   se agrega lo que falta: los 4 baselines en las esquinas.
3. La tabla de equidad cumple la condición de la opción A sin cambiar la regla del
   priorizador.
4. El comando y el contrato quedan iguales, así que `exporta_app.py` y la app no cambian.

## Cuándo revisar esta decisión

Si el reporte necesita una celda que no está (por ejemplo, el radio de 500 m en una
esquina del motor), se agrega esa combinación, no el cruce completo.

## Qué se declara

- Toda razón «X veces el baseline» dice contra qué baseline y con qué cota. La comparación
  más conservadora es la del baseline con necesidad con la cota máxima.
- El baseline es estilizado: el municipio llena las cisternas cuando los vecinos lo
  reportan (`decisiones/referencias-y-prensa.md`, nota del 30 de julio) y de ese reparto no
  hay registro.
- Con la cota máxima, el priorizado puede dejar sin entregas a los grupos pequeños de
  manzanas de las AGEB «Muy alto». La tabla de equidad dice cuánto.
- El plan de cada día se recalcula cuando cambia un supuesto: el resultado agregado es
  robusto, los puntos de entrega no (`datos/HALLAZGOS_sensibilidad.md`).
- Las cifras usan el motor de referencia; se recalculan con el oficial.
