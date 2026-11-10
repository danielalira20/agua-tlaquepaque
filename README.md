# Agua Tlaquepaque — Hackathon Jalisco Internacional 2026, Reto 01

**Tesis.** La ciudad planea el tandeo como un problema de litros y horarios. Es un problema
de salud. Modelamos la cadena red → tinaco → llave para decir en qué manzana, y en qué hora
del ciclo, el agua deja de ser segura, y repartimos las pipas por riesgo sanitario con la
misma agua.

**Delimitación.** San Pedro Tlaquepaque, el municipio con menos almacenamiento de los cuatro
que cubre el calendario de tandeo del SIAPA. Al menos 58,938 personas viven en manzanas donde
más de la mitad de las viviendas no tiene tinaco ni cisterna.

**Por qué Tlaquepaque y no El Salto o Tlajomulco.** El calendario oficial de tandeo (627
colonias, 15-oct-2026 a marzo-2027) solo cubre Guadalajara, Zapopan, Tlaquepaque y Tonalá.
Sin calendario el modelo no puede anticipar, solo reaccionar, y reaccionar ya es un mapa de
quejas. Además el SIAPA pidió al Congreso desincorporar a El Salto y Juanacatlán en mayo de 2026.

## Estructura

    contratos/    Los 5 contratos congelados. No se tocan sin avisar al equipo.
    datos/        Datos reales. manzanas_tlaquepaque.csv ya está completo.
    fixtures/     Datos falsos con la forma correcta. Sirven para trabajar sin esperar a nadie.
    motor/        Dani. Lee manzanas + calendario, escribe estado.parquet
    optimizador/  Jass. Lee estado.parquet, escribe plan.json
    app/          Migue. Next.js. Lee todo lo anterior.

## Quién depende de quién

    Magui  → calendario_tlaquepaque.json      bloquea a Dani y a Migue
    Dani   → estado.parquet con datos reales  bloquea a Jass
    Jass   → plan.json                        bloquea el comparador de Migue
    Migue  → app desplegada                   bloquea el video

Mientras tanto, los tres trabajan contra `fixtures/` y nadie espera a nadie.

## Supuestos que hay que declarar en el reporte

1. Censo 2020: seis años de antigüedad.
2. El censo dice si hay tinaco, no de cuántos litros. Asumimos 1,100 L por tinaco y
   5,000 L por cisterna. La encuesta remota sirve para calibrarlo.
3. Consumo de 50 L/persona/día, el nivel básico de la OMS, no el consumo normal.
   Reportar también a 100 L/p/d para mostrar sensibilidad.
4. El censo no cruza tinaco con cisterna: por eso toda cifra de "sin almacenamiento"
   va como rango (min y max), nunca como un solo número.
5. Valores de 1 y 2 viviendas vienen enmascarados por INEGI. El 0 es un cero real.

## Umbral oficial

NOM-127-SSA1-2021: cloro residual libre entre 0.2 y 1.5 mg/L. Por debajo de 0.2 el agua
deja de cumplir la norma. Ese es el corte del estado `sin_cloro`.

## Datasets del catálogo usados

| # | Dataset | Institución | Para qué |
|---|---------|-------------|----------|
| 01 | Principales resultados por AGEB y manzana urbana, Censo 2020 | INEGI | Almacenamiento, agua entubada, población por manzana |
| 17 | Índices de marginación | CONAPO | Priorizar con equidad |

Completar con los demás conforme se usen. Mencionar la fuente sin usar sus datos no cuenta.
