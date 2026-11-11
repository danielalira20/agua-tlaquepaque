"""Forma provisional de plan.json (seccion 9 de ESPECIFICACION.md)."""
from __future__ import annotations

import json
import os

from .asignacion import ResultadoDia
from .entradas import Parametros


def _redondear(metricas: dict) -> dict:
    return {k: round(v, 2) if isinstance(v, float) else v for k, v in metricas.items()}


def construir_plan(
    p: Parametros,
    resultados: list[ResultadoDia],
    por_dia: list[dict],
    semana: dict,
    ocupantes: dict[str, float],
    colonias: dict[str, str],
) -> dict:
    fechas = []
    for res, resumen in zip(resultados, por_dia):
        viajes = []
        for v in res.viajes:
            ll = v.llenado
            viaje = {
                "orden_eleccion": v.orden_eleccion,
                "tipo": v.tipo,
                "cvegeo_centro": v.cvegeo_centro,
                "colonia": colonias.get(v.cvegeo_centro, ""),
                "manzanas_cubiertas": [{"cvegeo": m, "viviendas": n} for m, n in ll.entregas],
                "viviendas_objetivo": ll.atendidas,
                "litros": ll.atendidas * p.litros_por_hogar,
                "personas_beneficiadas": round(sum(n * ocupantes[m] for m, n in ll.entregas), 2),
                "prioridad_score": round(ll.ponderado, 4),
            }
            if v.punto_id:
                viaje["punto_id"] = v.punto_id
            viajes.append(viaje)
        resumen = {k: v for k, v in resumen.items() if k != "fecha"}
        fechas.append({"fecha": res.fecha, "viajes": viajes, "resumen": _redondear(resumen)})
    return {"parametros": p.como_dict(), "fechas": fechas, "semana": _redondear(semana)}


def escribir_json(ruta: str, datos: dict) -> None:
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write("\n")
