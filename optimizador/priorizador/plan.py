"""Corre las cuatro corridas del contrato: priorizado y baseline, con cota minima y maxima."""
from __future__ import annotations

from dataclasses import dataclass, replace

from .asignacion import ResultadoDia, asignar_semana
from .baseline import Cisterna, asignar_semana_baseline
from .entradas import Necesidad, Parametros
from .metricas import metricas_dia, metricas_semana

COTAS_ORDEN = ("min", "max")
REGLAS_ORDEN = ("priorizado", "baseline")


@dataclass(frozen=True)
class Corrida:
    regla: str
    cota_para_ordenar: str
    resultados: list[ResultadoDia]
    por_dia: list[dict]
    semana: dict


def correr(
    regla: str,
    estado: dict[str, dict[str, Necesidad]],
    ubicaciones: dict[str, tuple[float, float]],
    ocupantes: dict[str, float],
    cisternas: list[Cisterna],
    p: Parametros,
) -> Corrida:
    if regla == "priorizado":
        resultados = asignar_semana(estado, ubicaciones, p)
    elif regla == "baseline":
        resultados = asignar_semana_baseline(estado, ubicaciones, cisternas, p)
    else:
        raise ValueError(f"regla desconocida: {regla!r}")
    por_dia = [metricas_dia(r, estado[r.fecha], ubicaciones, ocupantes, p) for r in resultados]
    semana = metricas_semana(resultados, estado, ocupantes, por_dia)
    return Corrida(regla, p.cota_para_ordenar, resultados, por_dia, semana)


def correr_todo(
    estados: dict[str, dict[str, dict[str, Necesidad]]],
    ubicaciones: dict[str, tuple[float, float]],
    ocupantes: dict[str, float],
    cisternas: list[Cisterna],
    p: Parametros,
) -> list[Corrida]:
    """`estados` va de cota a estado. Devuelve las corridas en el orden del contrato."""
    corridas = []
    for cota in COTAS_ORDEN:
        pc = replace(p, cota_para_ordenar=cota)
        for regla in REGLAS_ORDEN:
            corridas.append(correr(regla, estados[cota], ubicaciones, ocupantes, cisternas, pc))
    return corridas
