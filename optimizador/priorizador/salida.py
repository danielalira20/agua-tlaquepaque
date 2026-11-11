"""plan.json con la forma de contratos/plan.schema.json v2 (seccion 9 de ESPECIFICACION.md)."""
from __future__ import annotations

import json
import os

from .asignacion import Viaje
from .baseline import Cisterna
from .entradas import Parametros
from .plan import Corrida

UBICACION_CONTRATO = {"exacta": "coordenada_exacta", "colonia": "centro_de_colonia"}
DESCRIPCION_BASELINE = (
    "Baseline estilizado: los mismos viajes repartidos por turnos entre las cisternas instaladas. "
    "No es el reparto real del municipio, que responde a reportes ciudadanos y del que no hay registro."
)


def _redondear(metricas: dict) -> dict:
    return {k: round(v, 2) if isinstance(v, float) else v for k, v in metricas.items()}


def _viaje(
    v: Viaje,
    p: Parametros,
    ubicaciones: dict[str, tuple[float, float]],
    cisternas: dict[str, Cisterna],
    ocupantes: dict[str, float],
    colonias: dict[str, str],
) -> dict:
    ll = v.llenado
    if v.tipo == "cisterna":
        cis = cisternas[v.punto_id]
        (lon, lat), colonia, centro, punto = cis.punto, cis.colonia, None, v.punto_id
    else:
        (lon, lat), colonia, centro, punto = ubicaciones[v.cvegeo_centro], colonias.get(v.cvegeo_centro, ""), v.cvegeo_centro, None
    return {
        "orden_eleccion": v.orden_eleccion,
        "tipo": v.tipo,
        "punto_id": punto,
        "cvegeo_centro": centro,
        "colonia": colonia,
        "lon": lon,
        "lat": lat,
        "manzanas_cubiertas": [{"cvegeo": m, "viviendas": n} for m, n in ll.entregas],
        "viviendas_objetivo": ll.atendidas,
        "litros": int(ll.atendidas * p.litros_por_hogar),
        "personas_beneficiadas": round(sum(n * ocupantes[m] for m, n in ll.entregas), 2),
        "prioridad_score": round(ll.ponderado, 4),
    }


def comparar(priorizado: dict, baseline: dict) -> dict:
    """{metrica: {priorizado, baseline, diferencia}} con diferencia = priorizado - baseline."""
    numericas = [k for k, v in priorizado.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return {
        k: {
            "priorizado": _redondear({"x": priorizado[k]})["x"],
            "baseline": _redondear({"x": baseline[k]})["x"],
            "diferencia": round(priorizado[k] - baseline[k], 2),
        }
        for k in numericas
        if k in baseline
    }


def construir_plan(
    p: Parametros,
    corridas: list[Corrida],
    cisternas: list[Cisterna],
    excluidas: list[tuple[str, str]],
    ubicaciones: dict[str, tuple[float, float]],
    ocupantes: dict[str, float],
    colonias: dict[str, str],
) -> dict:
    por_id = {c.id: c for c in cisternas}
    salida_corridas = []
    for c in corridas:
        fechas = []
        for res, resumen in zip(c.resultados, c.por_dia):
            fechas.append(
                {
                    "fecha": res.fecha,
                    "viajes": [_viaje(v, p, ubicaciones, por_id, ocupantes, colonias) for v in res.viajes],
                    "resumen": _redondear({k: v for k, v in resumen.items() if k != "fecha"}),
                }
            )
        salida_corridas.append(
            {"regla": c.regla, "cota_para_ordenar": c.cota_para_ordenar, "fechas": fechas, "semana": _redondear(c.semana)}
        )

    comparacion = []
    for cota in dict.fromkeys(c.cota_para_ordenar for c in corridas):
        por_regla = {c.regla: c for c in corridas if c.cota_para_ordenar == cota}
        if "priorizado" in por_regla and "baseline" in por_regla:
            comparacion.append(
                {
                    "cota_para_ordenar": cota,
                    "semana": comparar(por_regla["priorizado"].semana, por_regla["baseline"].semana),
                }
            )

    return {
        "parametros": p.como_dict(),
        "baseline": {
            "descripcion": DESCRIPCION_BASELINE,
            "cisternas": [
                {
                    "id": c.id,
                    "tipo": c.tipo,
                    "ubicacion": UBICACION_CONTRATO[c.ubicacion],
                    "lon": c.punto[0],
                    "lat": c.punto[1],
                    "colonia": c.colonia,
                }
                for c in cisternas
            ],
            "excluidas": [{"id": i, "motivo": m} for i, m in excluidas],
        },
        "corridas": salida_corridas,
        "comparacion": comparacion,
        "propuesta_cisternas": None,
    }


def escribir_json(ruta: str, datos: dict) -> None:
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write("\n")
