# Datos reales para la app

Generados por `scripts/exporta_app.py` (`python3 scripts/exporta_app.py`). **No se editan a mano**: se regeneran.
Reemplazan a los datos simulados de `app/public/datos/` (`colonias.json`, `calendario.json`), que siguen ahi
mientras la app no cambie; nada de esta carpeta los toca.

Ventana: **2026-11-09 a 2026-11-15**; la app abre en **2026-11-12** si hoy no cae en la ventana. Calendario: **vigente**.
Para otra ventana: `python3 scripts/exporta_app.py --desde AAAA-MM-DD --hasta AAAA-MM-DD [--dia-inicial AAAA-MM-DD]`.
Sin argumentos se exporta la semana de referencia del reporte.

## Archivos

| Archivo | Qué es |
|---|---|
| `meta.json` | Ventana, calendario usado, supuestos del motor, conteos, fuentes y advertencias. **Mostrar las advertencias en la app** |
| `manzanas.json` | 4,871 manzanas. El orden es la llave de posicion de `estado.json` |
| `estado.json` | Salida del motor por fecha, en columnas alineadas con `manzanas.json` (el elemento `i` de cada arreglo es la manzana `i`) |
| `calendarios.json` | `vigente` y `original`, con la forma del `Calendario` que ya usa la app (`version`, `consultado`, `esquema`, `dias`), mas `vigente_desde` y `vigente_hasta` |
| `cisternas.json` | 60 registros: 50 cisternas y 10 propuestas del municipio |
| `plan.json` | Salida del priorizador (`contratos/plan.schema.json` v2) |

## `manzanas.json`

Arreglo de objetos: `cvegeo` (16 caracteres, **siempre texto**), `colonia` y `geocol` (capa del IIEG; vacio en 22
manzanas), `zona` (`"4"`, `"3,4"` si abarca varias, `""` si esta **fuera del programa**), `zona_confianza`
(`alta`, `media`, `baja`, `conflicto`, `ambiguo`, `ninguna`, `sin_poligono`, `sin_geometria`), `en_programa`, `lon`/`lat`
(centroide; `null` en las 8 manzanas sin geometria), `viviendas`, `pob`, `ocupantes_prom`, `viv_tinaco`,
`viv_cisterna`, `sin_almacen_min`/`sin_almacen_max` (cotas: el Censo no cruza tinaco con cisterna),
`grado_marginacion` (`Muy alto` a `Muy bajo` o `sin dato`; **mas alto = mas marginacion**; es una capa aparte, no entra
en `severidad`), `nucleo_robusto` (`true` en las 186 manzanas que quedan entre las 250 de mayor riesgo en al menos el 90% de
los 300 sorteos de la familia A de `datos/sensibilidad/`; es la parte del orden que **no depende de los supuestos**. Sale de
`datos/sensibilidad/manzanas_robustas.csv`; `false` si nunca entro al top 250).

## `estado.json`

`fechas` es una lista con un objeto por fecha: `fecha`, `dia` y arreglos de largo 4,871: `viv_sin_agua_min/max`,
`viv_agua_guardada_min/max`, `horas_sin_servicio_min/max`, `estado` (0 con agua, 1 quiebre parcial, 2 quiebre
mayoritario) y `requiere_desinfeccion` (0/1). El porcentaje y las personas se derivan:
`pct = 100 * viv_sin_agua / viviendas` y `personas = viv_sin_agua * ocupantes_prom`. El estado se calcula con
`pct_min` **sin redondear** (menor de 10, de 10 a 50, mayor de 50). Siempre hay un **minimo y un maximo**: nunca
mostrar un solo numero sin decir que es una cota.

## `plan.json`

Cuatro corridas: priorizado y baseline, con cota minima y con cota maxima, y su comparacion. Cada viaje trae
`lon`/`lat` del punto, las manzanas cubiertas y las viviendas atendidas. **El baseline es estilizado**: los mismos viajes
repartidos por turnos entre las cisternas instaladas; no es lo que hace hoy el municipio. `orden_eleccion` no es una ruta.

## Advertencias que la app debe decir

1. Un dia de racionamiento se modela como **cero agua** (`f = 0`), la cota alta del dano. El portal del SIAPA dice que
   es una baja de presion.
2. Las zonas salen de dos fuentes que no siempre coinciden: el 16% de la poblacion tiene zona solo por el poligono del
   portal. Ver `zona_confianza`.
3. El Censo es de 2020 y no dice la capacidad de tinacos y cisternas (se asumen 1,100 y 5,000 L).
4. El calendario del SIAPA ya cambio una vez y puede volver a cambiar.

## Para el motor oficial en TypeScript

`motor/vectores/vectores.json` trae las entradas, los supuestos y la salida esperada del motor de referencia para
cuatro conjuntos de supuestos. El motor de la app debe reproducirlos: los conteos de viviendas y las horas, exactos. La
formula esta en `motor/ESPECIFICACION.md`.
