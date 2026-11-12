# Almacenamiento de agua en los cuatro municipios del calendario del SIAPA

Verifica la afirmación del README de que San Pedro Tlaquepaque es "el municipio con menos almacenamiento de los
cuatro que cubre el calendario de tandeo del SIAPA". **Es cierta, en proporción**, con matices.

Se genera con `python3 scripts/compara_municipios.py` (baja el archivo de INEGI). Resultado: `comparacion_municipios.csv`.

**Fuente:** INEGI, Censo de Población y Vivienda 2020, *Principales resultados por AGEB y manzana urbana*, Jalisco.
**Medida:** viviendas sin tinaco ni cisterna, con cota mínima y máxima calculadas **por manzana**, la misma del proyecto.

## Resultado

| Municipio | Viviendas | Sin tinaco ni cisterna (mín a máx) | % de las viviendas | Con tinaco | Con cisterna |
|---|---:|---:|---:|---:|---:|
| **San Pedro Tlaquepaque** | 158,135 | 21,775 a 41,879 | **13.8% a 26.5%** | **72.8%** | **39.9%** |
| Tonalá | 129,832 | 11,074 a 26,381 | 8.5% a 20.3% | 78.2% | 44.7% |
| Zapopan | 383,368 | 20,452 a 55,049 | 5.3% a 14.4% | 82.3% | 68.4% |
| Guadalajara | 372,066 | 11,701 a 34,744 | 3.1% a 9.3% | 89.1% | 47.9% |

## Qué se puede decir

- **Tlaquepaque tiene la mayor proporción de viviendas sin tinaco ni cisterna**, con las dos cotas, y también el
  menor porcentaje de viviendas con tinaco (72.8%) y con cisterna (39.9%).
- **Con el mismo ordenamiento, Guadalajara queda muy por debajo** (a lo sumo 9.3%, contra al menos 13.8% de Tlaquepaque).

## Matices que hay que declarar

1. **Los intervalos se traslapan.** El de Tlaquepaque (13.8% a 26.5%) se traslapa con el de Tonalá (8.5% a 20.3%) y apenas
   con el de Zapopan (5.3% a 14.4%). Es primero en la cota mínima y en la máxima, pero el Censo no permite afirmarlo con certeza.
2. **Es la proporción, no la cantidad.** Con la cota máxima, **Zapopan tiene más viviendas sin almacenamiento** (55,049)
   que Tlaquepaque (41,879), y con la cota mínima son casi iguales (20,452 contra 21,775). También hay más personas en
   manzanas donde más de la mitad no tiene almacenamiento en Zapopan (63,836 a 95,700) que en Tlaquepaque (58,938 a 92,069).
   El argumento para elegir Tlaquepaque es la proporción y el calendario publicado, no que sea el municipio con más
   viviendas en riesgo.
3. **El Censo enmascara con `*` los valores de 1 o 2**, y esas manzanas se excluyen. La población cubierta es 86.7% en
   Tlaquepaque y entre 88.5% y 92.9% en los otros tres, así que Tlaquepaque queda algo menos representado. No sabemos en qué
   dirección sesga.
4. **Solo es la parte urbana** (manzanas); no incluye localidades rurales.
5. **Con los totales del municipio no se puede hacer esta comparación**: en Tlaquepaque los tinacos más las cisternas (195,044)
   superan a las viviendas (172,717), y la cota mínima saldría 0. Por eso se usan las cotas por manzana.

## Cómo se comprobó que el método es el del proyecto

Con este criterio, Tlaquepaque da exactamente lo que ya tiene el repo en `manzanas_tlaquepaque.csv`: 4,871 manzanas, 588,419
personas, 158,135 viviendas, 21,775 a 41,879 sin almacenamiento y 58,938 a 92,069 personas en manzanas con más de la mitad
sin almacenamiento. Una prueba lo fija (`motor/test_referencia.py`).
