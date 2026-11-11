"""Asignacion diaria de viajes con el algoritmo voraz (seccion 6 de ESPECIFICACION.md)."""
from __future__ import annotations

from dataclasses import dataclass

from .cobertura import Llenado, llenar, vecinas_por_manzana
from .entradas import Necesidad, Parametros


@dataclass(frozen=True)
class Viaje:
    orden_eleccion: int
    cvegeo_centro: str
    llenado: Llenado


@dataclass(frozen=True)
class ResultadoDia:
    fecha: str
    viajes: tuple[Viaje, ...]
    viajes_sin_usar: int


def clave(modo_racha: str, llenado: Llenado) -> tuple:
    """Orden de comparacion entre dos viajes candidatos segun modo_racha."""
    if modo_racha == "desempate":
        return (llenado.atendidas, llenado.ponderado)
    if modo_racha == "peso":
        return (llenado.ponderado, llenado.atendidas)
    if modo_racha == "no":
        return (llenado.atendidas,)
    raise ValueError(f"modo_racha desconocido: {modo_racha!r}")


def asignar_dia(
    fecha: str,
    necesidad: dict[str, Necesidad],
    ubicaciones: dict[str, tuple[float, float]],
    p: Parametros,
) -> ResultadoDia:
    """Elige los viajes de una fecha. Los empates finales los gana el cvegeo menor."""
    secas = {c: n for c, n in necesidad.items() if n.viviendas > 0 and c in ubicaciones}
    # Basta con vecinas que tienen viviendas sin agua: las demas no reciben nada.
    vecinas = vecinas_por_manzana({c: ubicaciones[c] for c in secas}, p.radio_cobertura_m)
    resto = {c: n.viviendas for c, n in secas.items()}
    peso = {c: n.peso for c, n in secas.items()}
    orden = sorted(secas)
    cache: dict[str, Llenado] = {}
    viajes: list[Viaje] = []

    for k in range(1, p.viajes_por_dia + 1):
        mejor = None
        mejor_clave = None
        for c in orden:
            if resto[c] <= 0:
                continue
            llenado = cache.get(c)
            if llenado is None:
                llenado = cache[c] = llenar(vecinas[c], resto, peso, p.hogares_por_viaje)
            k_c = clave(p.modo_racha, llenado)
            if mejor is None or k_c > mejor_clave:
                mejor, mejor_clave = c, k_c
        if mejor is None:
            return ResultadoDia(fecha, tuple(viajes), p.viajes_por_dia - k + 1)

        llenado = cache[mejor]
        viajes.append(Viaje(k, mejor, llenado))
        for m, n in llenado.entregas:
            resto[m] -= n
        # Un cambio en m altera el llenado de todo centro que tiene a m dentro del radio.
        for m, _ in llenado.entregas:
            for _, c in vecinas[m]:
                cache.pop(c, None)

    return ResultadoDia(fecha, tuple(viajes), 0)


def asignar_semana(
    estado: dict[str, dict[str, Necesidad]],
    ubicaciones: dict[str, tuple[float, float]],
    p: Parametros,
) -> list[ResultadoDia]:
    """Cada fecha se resuelve por separado, en orden."""
    return [asignar_dia(f, estado[f], ubicaciones, p) for f in sorted(estado)]
