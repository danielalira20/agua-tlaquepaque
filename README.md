# Agua Tlaquepaque — Hackathon Jalisco Internacional 2026, Reto 01

**Tesis.** La ciudad planea el tandeo como un problema de litros y horarios. Es un problema
de salud. Modelamos la cadena red → tinaco → llave para decir en qué manzana, y qué día
del calendario, el agua deja de ser segura, y repartimos las pipas por riesgo sanitario con la
misma agua.

**Delimitación.** San Pedro Tlaquepaque, el municipio con menos almacenamiento de los cuatro
que cubre el calendario de tandeo del SIAPA. Entre 58,938 y 92,069 personas (cota mínima y máxima:
el Censo no cruza tinaco con cisterna) viven en manzanas donde más de la mitad de las viviendas no
tiene tinaco ni cisterna. El censo trae 4,871 manzanas y 588,419 personas.

**Delimitación aprobada (opción B, 12-nov-2026, 4 de 4):** las colonias de Tlaquepaque **dentro del
programa de racionamiento** del SIAPA (zonas 3 a 6). Son 462,194 personas (78.6%); entre el 63% y el 79% de la
población según la fuente de zonas, porque la lista oficial y el portal no coinciden del todo (ver
`datos/zonas_siapa/LEEME.md`). Se reportan resultados por zona y las zonas 3 y 4 quedan como caso de estudio.
Indicador: **personas-día sin agua por semana**.

**Por qué Tlaquepaque y no El Salto o Tlajomulco.** El calendario oficial de racionamiento
(siete zonas, versión original del 15-oct-2026 y vigente del 3-nov-2026) solo cubre Guadalajara, Zapopan, Tlaquepaque y Tonalá.
Sin calendario el modelo no puede anticipar, solo reaccionar, y reaccionar ya es un mapa de
quejas. Además el SIAPA pidió al Congreso desincorporar a El Salto y Juanacatlán en mayo de 2026.

## Estructura

    contratos/    Los contratos congelados. No se tocan sin avisar al equipo. Cada uno cambia con su fixture.
    datos/        Datos reales. manzanas_tlaquepaque.csv ya está completo.
    fixtures/     Datos falsos con la forma correcta. Sirven para trabajar sin esperar a nadie.
    motor/        Dani. Lee manzanas + zonas + calendario, escribe estado (por manzana y fecha)
    optimizador/  Jass. Lee estado.parquet, escribe plan.json
    app/          Migue. Next.js. Lee todo lo anterior.

## Quién depende de quién

    Magui  → zonas_siapa/manzana_zona.csv     bloquea a Dani y a Migue (hecho: ver datos/zonas_siapa/LEEME.md)
    Dani   → estado con datos reales          bloquea a Jass
    Jass   → plan.json                        bloquea el comparador de Migue
    Migue  → app desplegada                   bloquea el video

Mientras tanto, los tres trabajan contra `fixtures/` y nadie espera a nadie.

## Supuestos que hay que declarar en el reporte

1. Censo 2020: seis años de antigüedad.
2. El censo dice si hay tinaco, no de cuántos litros. Asumimos 1,100 L por tinaco y
   5,000 L por cisterna. Se cubre con análisis de sensibilidad y con el contraste contra las
   cisternas del municipio, no con encuesta.
3. Consumo de 50 L/persona/día, el nivel básico de la OMS, no el consumo normal.
   Reportar también a 100 y 150 L/p/d para mostrar sensibilidad.
4. El censo no cruza tinaco con cisterna: por eso toda cifra de "sin almacenamiento"
   va como rango (min y max), nunca como un solo número.
5. Valores de 1 y 2 viviendas vienen enmascarados por INEGI. El 0 es un cero real.
6. Un día de racionamiento equivale a **cero agua** por defecto (`f = 0`). El portal del SIAPA
   dice que es una baja de presión y no un corte total; la sensibilidad a `f` = 0, 0.25 y 0.5
   lo cubre (decisión abierta 6 de `motor/ESPECIFICACION.md`).
7. La zona de cada manzana sale de dos fuentes que no siempre coinciden. La cobertura del
   programa se reporta como rango (63% a 79% de la población), con nivel de confianza por
   manzana. Ver `datos/zonas_siapa/LEEME.md`.

## Umbral oficial

NOM-127-SSA1-2021: cloro residual libre entre 0.2 y 1.5 mg/L. Solo es contexto: no hay datos
públicos de cloro en la llave, así que el motor no lo modela. Lo que sí marca es
`requiere_desinfeccion`: agua almacenada más de 48 h.

## Datasets del catálogo usados

| # | Dataset | Institución | Para qué |
|---|---------|-------------|----------|
| 01 | Principales resultados por AGEB y manzana urbana, Censo 2020 | INEGI | Almacenamiento, agua entubada, población por manzana |
| 17 | Índices de marginación | CONAPO | Priorizar con equidad |

Completar con los demás conforme se usen. Mencionar la fuente sin usar sus datos no cuenta.
