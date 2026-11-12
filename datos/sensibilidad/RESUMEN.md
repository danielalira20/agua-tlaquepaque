# Resumen de la sensibilidad (generado)

**Generado por `scripts/resume_sensibilidad.py` a partir de `scripts/sensibilidad_orden.py`. No se edita a mano.** La interpretación está en `../HALLAZGOS_sensibilidad.md`.

Ocupantes por vivienda (mediana del Censo): 3.77.

## 1. Escenarios (un supuesto a la vez, esquinas, calendario, zonas)

`rango`: `decision` = del equipo; `literatura` = de una referencia; `sin_fuente` = ilustrativo, sin fuente en el repo; `censo` = incertidumbre propia del Censo.

| escenario | rango | viv-día sin agua (mín) | rho | solape top-250 | cobertura top-250 | solape top-10 colonias | lugar El Sauz | zonas 5-6 (%) | Muy bajo (%) | grado mayor | priorizado ÷ baseline | solape atendidas | orden estable | concl. B estable |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| base | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| consumo_l_persona_dia=50 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| consumo_l_persona_dia=60 | decision | 63,799 | 0.900 | 0.936 | 0.994 | 1 | 1 | 70.4 | 46.5 | Muy bajo | 4.59 | 0.759 | no | sí |
| consumo_l_persona_dia=75 | decision | 81,729 | 0.728 | 0.852 | 0.978 | 0.7 | 1 | 62.7 | 36.8 | Muy bajo | 4.20 | 0.590 | no | sí |
| consumo_l_persona_dia=100 | decision | 118,390 | 0.615 | 0.740 | 0.939 | 0.7 | 1 | 55.3 | 28.9 | Muy bajo | 3.39 | 0.192 | no | no |
| consumo_l_persona_dia=120 | literatura | 141,700 | 0.600 | 0.708 | 0.924 | 0.7 | 1 | 54.9 | 29.4 | Muy bajo | 3.15 | 0.143 | no | no |
| consumo_l_persona_dia=150 | sin_fuente | 171,823 | 0.553 | 0.616 | 0.892 | 0.7 | 1 | 51.9 | 26.9 | Medio | 2.72 | 0.124 | no | no |
| tinaco_l=750 | decision | 79,468 | 0.740 | 0.856 | 0.981 | 0.7 | 1 | 63.4 | 37.7 | Muy bajo | 4.24 | 0.637 | no | sí |
| tinaco_l=900 | decision | 64,887 | 0.885 | 0.928 | 0.991 | 1 | 1 | 69.8 | 45.7 | Muy bajo | 4.52 | 0.759 | no | sí |
| tinaco_l=1100 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| tinaco_l=450 | sin_fuente | 143,889 | 0.596 | 0.704 | 0.920 | 0.7 | 1 | 54.7 | 29.3 | Muy bajo | 3.10 | 0.142 | no | no |
| tinaco_l=600 | sin_fuente | 106,883 | 0.633 | 0.740 | 0.945 | 0.7 | 1 | 57.8 | 30.9 | Muy bajo | 3.53 | 0.276 | no | no |
| tinaco_l=1500 | sin_fuente | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| tinaco_l=2500 | sin_fuente | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| cisterna_l=2500 | sin_fuente | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| cisterna_l=3500 | sin_fuente | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| cisterna_l=7500 | sin_fuente | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| cisterna_l=10000 | sin_fuente | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| horas_efectivas_corte=24 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| horas_efectivas_corte=36 | decision | 60,787 | 0.960 | 0.968 | 0.998 | 1 | 1 | 71.3 | 48.8 | Muy bajo | 4.69 | 0.866 | sí | sí |
| horas_efectivas_corte=48 | decision | 66,712 | 0.860 | 0.912 | 0.990 | 0.9 | 1 | 69.0 | 44.5 | Muy bajo | 4.46 | 0.745 | no | sí |
| fraccion_suministro_en_racionamiento=0.0 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| fraccion_suministro_en_racionamiento=0.25 | decision | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| fraccion_suministro_en_racionamiento=0.5 | decision | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| fraccion_suministro_en_racionamiento=0.75 | sin_fuente | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| u_horas_agua_guardada=24 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| u_horas_agua_guardada=48 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| u_horas_agua_guardada=72 | decision | 58,906 | 1.000 | 1.000 | 1.000 | 1 | 1 | 72.0 | 50.4 | Muy bajo | 4.87 | 1.000 | sí | sí |
| esquina_favorable | decision | 58,622 | 0.995 | 1.000 | 1.000 | 1 | 1 | 72.1 | 50.6 | Muy bajo | 4.88 | 0.945 | sí | sí |
| esquina_adversa | decision | 222,608 | 0.493 | 0.540 | 0.836 | 0.7 | 1 | 50.3 | 26.0 | Medio | 2.28 | 0.110 | no | no |
| esquina_adversa_extrema | sin_fuente | 262,220 | 0.456 | 0.496 | 0.807 | 0.7 | 2 | 50.8 | 26.7 | Medio | 2.21 | 0.104 | no | no |
| calendario_original | decision | 39,472 | 0.982 | 0.928 | 0.995 | 1 | 1 | 76.1 | 53.0 | Muy bajo | 6.38 | 0.841 | sí | sí |
| zonas_solo_lista | decision | 49,667 | 0.671 | 0.836 | 0.935 | 1 | 1 | 73.0 | 50.8 | Muy bajo | 5.58 | 0.851 | no | sí |
| zonas_conflicto_portal | decision | 59,122 | 0.997 | 1.000 | 1.000 | 1 | 1 | 71.7 | 50.2 | Muy bajo | 4.87 | 0.986 | sí | sí |
| zonas_conflicto_lista | decision | 59,035 | 0.998 | 1.000 | 1.000 | 1 | 1 | 72.3 | 50.3 | Muy bajo | 4.87 | 1.000 | sí | sí |
| lente_cota_maxima | censo | 128,460 | 0.580 | 0.724 | 0.927 | 0.7 | 1 | 63.7 | 29.6 | Muy bajo |  |  | no | sí |

## 2. Barrido fino: dónde cambia el orden

| parametro | valor | viv-día sin agua (mín) | rho | solape top-250 | cobertura top-250 | zonas 5-6 (%) | Muy bajo (%) | lugar El Sauz |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| consumo_l_persona_dia | 50 | 58,906 | 1.000 | 1.000 | 1.000 | 72.0 | 50.4 | 1 |
| consumo_l_persona_dia | 55 | 60,167 | 0.972 | 0.988 | 1.000 | 71.5 | 49.3 | 1 |
| consumo_l_persona_dia | 60 | 63,799 | 0.900 | 0.936 | 0.994 | 70.4 | 46.5 | 1 |
| consumo_l_persona_dia | 65 | 69,445 | 0.818 | 0.876 | 0.987 | 67.5 | 42.8 | 1 |
| consumo_l_persona_dia | 70 | 75,332 | 0.764 | 0.868 | 0.986 | 64.8 | 39.5 | 1 |
| consumo_l_persona_dia | 75 | 81,729 | 0.728 | 0.852 | 0.978 | 62.7 | 36.8 | 1 |
| consumo_l_persona_dia | 80 | 88,628 | 0.693 | 0.828 | 0.969 | 61.6 | 34.8 | 1 |
| consumo_l_persona_dia | 85 | 96,509 | 0.662 | 0.772 | 0.954 | 60.2 | 33.1 | 1 |
| consumo_l_persona_dia | 90 | 104,430 | 0.640 | 0.752 | 0.946 | 58.4 | 31.5 | 1 |
| consumo_l_persona_dia | 95 | 111,643 | 0.624 | 0.748 | 0.943 | 56.6 | 30.0 | 1 |
| consumo_l_persona_dia | 100 | 118,390 | 0.615 | 0.740 | 0.939 | 55.3 | 28.9 | 1 |
| tinaco_l | 600 | 106,883 | 0.633 | 0.740 | 0.945 | 57.8 | 30.9 | 1 |
| tinaco_l | 650 | 95,813 | 0.665 | 0.780 | 0.955 | 60.4 | 33.3 | 1 |
| tinaco_l | 700 | 86,639 | 0.701 | 0.824 | 0.973 | 61.9 | 35.2 | 1 |
| tinaco_l | 750 | 79,468 | 0.740 | 0.856 | 0.981 | 63.4 | 37.7 | 1 |
| tinaco_l | 800 | 73,739 | 0.778 | 0.864 | 0.986 | 65.5 | 40.4 | 1 |
| tinaco_l | 850 | 68,971 | 0.824 | 0.876 | 0.987 | 67.8 | 43.1 | 1 |
| tinaco_l | 900 | 64,887 | 0.885 | 0.928 | 0.991 | 69.8 | 45.7 | 1 |
| tinaco_l | 950 | 61,880 | 0.937 | 0.960 | 0.997 | 71.1 | 48.0 | 1 |
| tinaco_l | 1000 | 60,167 | 0.972 | 0.988 | 1.000 | 71.5 | 49.3 | 1 |
| tinaco_l | 1050 | 59,246 | 0.994 | 1.000 | 1.000 | 71.8 | 50.1 | 1 |
| tinaco_l | 1100 | 58,906 | 1.000 | 1.000 | 1.000 | 72.0 | 50.4 | 1 |

## 3. Monte Carlo

Familia A: consumo 50 a 100 L, tinaco 750 a 1,100 L y U de 24 a 72 h (los rangos de la decisión 1). Familia B: además cisterna 2,500 a 10,000 L, horas efectivas 24 a 48 y fracción `f` de 0 a 0.5. Sorteos uniformes con semilla fija.

### Familia A (300 sorteos)

| métrica | media | p5 | mediana | p95 | mínimo |
|---|---|---|---|---|---|
| rho (orden, manzanas con riesgo) | 0.682 | 0.590 | 0.647 | 0.856 | 0.566 |
| solape del top-250 | 0.787 | 0.688 | 0.764 | 0.912 | 0.628 |
| cobertura del riesgo, top-100 del base | 0.969 | 0.929 | 0.973 | 0.995 | 0.918 |
| cobertura del riesgo, top-250 del base | 0.955 | 0.913 | 0.950 | 0.990 | 0.896 |
| solape del top-10 de colonias | 0.747 | 0.700 | 0.700 | 0.905 | 0.700 |
| parte del riesgo en zonas 5 y 6 (%) | 59.8 | 54.5 | 59.1 | 69.0 | 52.6 |
| parte del riesgo en AGEB Muy bajo (%) | 33.9 | 28.6 | 32.2 | 44.5 | 27.5 |
| cobertura del núcleo robusto | 0.987 | 0.971 | 0.992 | 0.995 | 0.960 |
| priorizador: veces el baseline (n=60) | 3.72 | 2.99 | 3.57 | 4.44 | 2.88 |
| priorizador: solape de manzanas atendidas | 0.368 | 0.141 | 0.285 | 0.735 | 0.133 |

- Criterio de orden estable cumplido en **2.7%** de los sorteos; conclusión B estable en **30.7%**.
- Lugar de El Sauz: {1: 300}.
- Grado con mayor parte del riesgo: {'Muy bajo': 296, 'Medio': 4}.

### Familia B (300 sorteos)

| métrica | media | p5 | mediana | p95 | mínimo |
|---|---|---|---|---|---|
| rho (orden, manzanas con riesgo) | 0.771 | 0.576 | 0.741 | 0.998 | 0.536 |
| solape del top-250 | 0.845 | 0.672 | 0.852 | 1.000 | 0.600 |
| cobertura del riesgo, top-100 del base | 0.979 | 0.936 | 0.989 | 1.000 | 0.895 |
| cobertura del riesgo, top-250 del base | 0.968 | 0.906 | 0.980 | 1.000 | 0.873 |
| solape del top-10 de colonias | 0.830 | 0.700 | 0.800 | 1.000 | 0.700 |
| parte del riesgo en zonas 5 y 6 (%) | 63.6 | 53.8 | 63.6 | 72.1 | 51.5 |
| parte del riesgo en AGEB Muy bajo (%) | 38.7 | 27.7 | 38.0 | 50.6 | 26.4 |
| cobertura del núcleo robusto | 0.983 | 0.971 | 0.986 | 0.995 | 0.934 |
| priorizador: veces el baseline (n=60) | 4.09 | 2.95 | 4.24 | 4.88 | 2.62 |
| priorizador: solape de manzanas atendidas | 0.498 | 0.144 | 0.543 | 0.799 | 0.118 |

- Criterio de orden estable cumplido en **27.7%** de los sorteos; conclusión B estable en **58.3%**.
- Lugar de El Sauz: {1: 300}.
- Grado con mayor parte del riesgo: {'Muy bajo': 286, 'Medio': 14}.

## 4. Qué supuesto mueve más el orden

Correlación de rangos (Spearman) entre cada parámetro y cada resultado, sobre los sorteos de Monte Carlo. Con consumo y fracción `f` el signo es opuesto porque lo que cuenta es el consumo neto `c × (1 − f)`.

| familia | parametro | rango_bajo | rango_alto | con rho | con cobertura top-250 | con zonas 5-6 | con Muy bajo | con viv-día | con solape atendidas |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | consumo_l_persona_dia | 50 | 100 | -0.87 | -0.867 | -0.859 | -0.826 | 0.871 | -0.855 |
| A | tinaco_l | 750 | 1100 | 0.484 | 0.486 | 0.475 | 0.445 | -0.485 | 0.674 |
| A | u_horas_agua_guardada | 24 | 72 | 0.002 | 0.001 | 0.008 | 0.019 | -0.002 | -0.286 |
| B | consumo_l_persona_dia | 50 | 100 | -0.633 | -0.641 | -0.642 | -0.64 | 0.643 | -0.635 |
| B | tinaco_l | 750 | 1100 | 0.27 | 0.267 | 0.268 | 0.262 | -0.275 | 0.187 |
| B | u_horas_agua_guardada | 24 | 72 | 0.082 | 0.086 | 0.089 | 0.088 | -0.09 | 0.203 |
| B | cisterna_l | 2500 | 10000 | 0.064 | 0.052 | 0.048 | 0.041 | -0.045 | -0.128 |
| B | horas_efectivas_corte | 24 | 48 | -0.258 | -0.27 | -0.256 | -0.269 | 0.246 | -0.282 |
| B | fraccion_suministro_en_racionamiento | 0 | 0.5 | 0.596 | 0.601 | 0.611 | 0.607 | -0.614 | 0.645 |

## 5. La autonomía del tinaco, en días

`tinaco / (ocupantes × consumo × (1 − f))` con 3.77 ocupantes. La racha de racionamiento más larga del calendario vigente es de 4 días (zonas 4 y 5), y de 3 en las zonas 3 y 6. Sobre los 600 sorteos de Monte Carlo:

| autonomía del tinaco (días) | sorteos | rho medio | cobertura top-250 | zonas 5-6 (%) | Muy bajo (%) |
|---|---:|---:|---:|---:|---:|
| 2 a 3 | 123 | 0.600 | 0.925 | 54.5 | 28.8 |
| 3 a 4 | 210 | 0.651 | 0.950 | 58.7 | 32.0 |
| 4 a 5 | 151 | 0.765 | 0.979 | 64.8 | 39.3 |
| 5 a 6 | 56 | 0.903 | 0.994 | 69.7 | 46.3 |
| 6 o más | 60 | 0.988 | 1.000 | 71.8 | 50.1 |

Caso base: 5.8 días. Consumo 100 L: 2.9 días. Consumo 100 L y tinaco de 750 L: 2.0 días.

## 6. El núcleo robusto

Manzanas que quedan entre las 250 de mayor riesgo en al menos el 90% de los sorteos de la familia A: **186**. Concentran 31,734 viviendas-día sin agua del caso base (de 40,701 en las 437 manzanas que aparecen en algún top-250). 169 de ellas están en el top-250 del caso base.

Por zona y por grado de marginación:

| zona | manzanas | viv-día base |
|---|---:|---:|
| 5 | 65 | 11,124 |
| 6 | 62 | 14,679 |
| 4 | 51 | 4,641 |
| 3 | 8 | 1,290 |

| grado_marginacion | manzanas | viv-día base |
|---|---:|---:|
| Muy bajo | 81 | 19,558 |
| Alto | 50 | 4,365 |
| Bajo | 41 | 6,491 |
| Medio | 12 | 1,156 |
| Muy alto | 2 | 164 |

Las diez colonias con más manzanas en el núcleo:

| colonia | manzanas | viv-día base |
|---|---:|---:|
| El Sauz | 28 | 8,850 |
| Fovissste Miravalle | 24 | 2,956 |
| San Martin de Las Flores de Abajo | 21 | 1,989 |
| Parques de Sta. Cruz del Valle | 11 | 2,564 |
| Villa Fontana | 10 | 3,464 |
| Haciendas del Real | 10 | 1,911 |
| Balcones de Santa María | 8 | 1,221 |
| San Martin de Las Flores de Arriba | 6 | 568 |
| Miraflores | 5 | 717 |
| Guayabitos | 5 | 256 |

