"""Distancias y cobertura de un punto de entrega (seccion 5 de ESPECIFICACION.md)."""
from __future__ import annotations

import math
from dataclasses import dataclass

RADIO_TIERRA_M = 6_371_000.0
TOLERANCIA_M = 1e-6
METROS_POR_GRADO = 2 * math.pi * RADIO_TIERRA_M / 360
_HOLGURA_CELDA = 1.05


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Distancia en metros entre dos puntos (lon, lat)."""
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * RADIO_TIERRA_M * math.asin(math.sqrt(h))


def vecinas_por_manzana(
    ubicaciones: dict[str, tuple[float, float]], radio_m: float
) -> dict[str, list[tuple[float, str]]]:
    """Para cada manzana, las que estan a `radio_m` o menos, incluida ella a 0 m.

    Cada lista va ordenada por (distancia, cvegeo). Una rejilla evita comparar todas contra
    todas, y cada distancia se calcula una sola vez para que la relacion sea simetrica.
    """
    if not ubicaciones:
        return {}
    lat_max = max(abs(lat) for _, lat in ubicaciones.values())
    alto = _HOLGURA_CELDA * radio_m / METROS_POR_GRADO
    ancho = _HOLGURA_CELDA * radio_m / (METROS_POR_GRADO * math.cos(math.radians(lat_max)))
    celdas: dict[tuple[int, int], list[str]] = {}
    for cvegeo, (lon, lat) in ubicaciones.items():
        celdas.setdefault((math.floor(lon / ancho), math.floor(lat / alto)), []).append(cvegeo)

    vecinas = {c: [(0.0, c)] for c in ubicaciones}
    for (i, j), propias in celdas.items():
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                otras = celdas.get((i + di, j + dj))
                if not otras:
                    continue
                for p in propias:
                    for q in otras:
                        if p < q:
                            d = haversine_m(ubicaciones[p], ubicaciones[q])
                            if d <= radio_m + TOLERANCIA_M:
                                vecinas[p].append((d, q))
                                vecinas[q].append((d, p))
    for lista in vecinas.values():
        lista.sort()
    return vecinas


def vecinas_de_punto(
    punto: tuple[float, float], ubicaciones: dict[str, tuple[float, float]], radio_m: float
) -> list[tuple[float, str]]:
    """Manzanas a `radio_m` o menos de un punto que no es manzana, ordenadas por (distancia, cvegeo)."""
    cerca = []
    for c, u in ubicaciones.items():
        d = haversine_m(punto, u)
        if d <= radio_m + TOLERANCIA_M:
            cerca.append((d, c))
    cerca.sort()
    return cerca


@dataclass(frozen=True)
class Llenado:
    """Lo que entrega un viaje: (cvegeo, viviendas) en orden de cercania."""

    entregas: tuple[tuple[str, int], ...]
    atendidas: int
    ponderado: float


def llenar(
    vecinas_centro: list[tuple[float, str]],
    resto: dict[str, int],
    peso: dict[str, float],
    cupo: int,
) -> Llenado:
    """Reparte un viaje de la manzana mas cercana a la mas lejana hasta agotar el cupo."""
    entregas = []
    atendidas = 0
    ponderado = 0.0
    for _, m in vecinas_centro:
        if cupo == 0:
            break
        n = min(resto.get(m, 0), cupo)
        if n <= 0:
            continue
        entregas.append((m, n))
        atendidas += n
        ponderado += n * peso[m]
        cupo -= n
    return Llenado(tuple(entregas), atendidas, ponderado)
