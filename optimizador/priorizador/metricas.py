"""Metricas por fecha y por semana (seccion 8 de ESPECIFICACION.md)."""
from __future__ import annotations

from .asignacion import ResultadoDia
from .entradas import Necesidad, Parametros

SUMABLES = (
    "necesidad_total",
    "viviendas_atendidas",
    "personas_atendidas",
    "valor_ponderado",
    "maximo_viviendas",
    "maximo_ponderado",
    "viajes_usados",
    "viajes_sin_usar",
)


def _pct(parte: float, total: float, si_total_cero: float) -> float:
    return si_total_cero if total == 0 else 100 * parte / total


def _ocupantes(ocupantes: dict[str, float], cvegeo: str) -> float:
    try:
        return ocupantes[cvegeo]
    except KeyError:
        raise ValueError(f"{cvegeo}: no hay ocupantes_prom") from None


def _porcentajes(m: dict) -> dict:
    m["cobertura_pct"] = _pct(m["viviendas_atendidas"], m["necesidad_total"], 0.0)
    m["eficiencia_viviendas_pct"] = _pct(m["viviendas_atendidas"], m["maximo_viviendas"], 100.0)
    m["eficiencia_ponderada_pct"] = _pct(m["valor_ponderado"], m["maximo_ponderado"], 100.0)
    return m


def metricas_dia(
    res: ResultadoDia,
    necesidad: dict[str, Necesidad],
    ubicaciones: dict[str, tuple[float, float]],
    ocupantes: dict[str, float],
    p: Parametros,
) -> dict:
    cupo_total = p.viajes_por_dia * p.hogares_por_viaje
    entregas = [e for v in res.viajes for e in v.llenado.entregas]

    # Los maximos ignoran la geografia: cualquier viaje podria llegar a cualquier vivienda.
    alcanzables = sorted(
        ((n.peso, n.viviendas) for c, n in necesidad.items() if n.viviendas > 0 and c in ubicaciones),
        reverse=True,
    )
    maximo_ponderado = 0.0
    quedan = cupo_total
    for peso, viviendas in alcanzables:
        if quedan == 0:
            break
        tomadas = min(viviendas, quedan)
        maximo_ponderado += tomadas * peso
        quedan -= tomadas

    return _porcentajes(
        {
            "fecha": res.fecha,
            "necesidad_total": sum(n.viviendas for n in necesidad.values()),
            "viviendas_atendidas": sum(n for _, n in entregas),
            "personas_atendidas": sum(n * _ocupantes(ocupantes, m) for m, n in entregas),
            "valor_ponderado": sum(v.llenado.ponderado for v in res.viajes),
            "maximo_viviendas": min(cupo_total, sum(v for _, v in alcanzables)),
            "maximo_ponderado": maximo_ponderado,
            "viajes_usados": len(res.viajes),
            "viajes_sin_usar": res.viajes_sin_usar,
        }
    )


def metricas_semana(
    resultados: list[ResultadoDia],
    estado: dict[str, dict[str, Necesidad]],
    ocupantes: dict[str, float],
    por_dia: list[dict],
) -> dict:
    total = _porcentajes({k: sum(d[k] for d in por_dia) for k in SUMABLES})

    atendidas = {m for r in resultados for v in r.viajes for m, _ in v.llenado.entregas}
    maxima: dict[str, int] = {}
    for dia in estado.values():
        for c, n in dia.items():
            if n.viviendas > maxima.get(c, 0):
                maxima[c] = n.viviendas
    sin_entrega = sorted(c for c in maxima if c not in atendidas)
    total["manzanas_sin_entrega"] = len(sin_entrega)
    total["personas_sin_entrega"] = sum(maxima[c] * _ocupantes(ocupantes, c) for c in sin_entrega)
    return total
