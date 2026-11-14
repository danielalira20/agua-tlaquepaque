"""Construccion de escenarios pequenos para las pruebas (seccion 10 de ESPECIFICACION.md)."""
from __future__ import annotations

from optimizador.priorizador.cobertura import METROS_POR_GRADO
from optimizador.priorizador.entradas import Necesidad, Parametros

LON = -103.3


def parametros(**cambios) -> Parametros:
    """Valores de los casos a mano: 10 hogares por viaje, radio de 300 m, cota minima, desempate."""
    base = dict(
        pipas=32,
        viajes_por_dia=1,
        litros_por_viaje=2000,
        litros_por_hogar=200,
        radio_cobertura_m=300,
        cota_para_ordenar="min",
        modo_racha="desempate",
    )
    base.update(cambios)
    return Parametros(**base).validar()


def ubicar(posiciones: dict[str, float]) -> dict[str, tuple[float, float]]:
    """Manzanas sobre un mismo meridiano, a la posicion en metros indicada."""
    return {c: (LON, metros / METROS_POR_GRADO) for c, metros in posiciones.items()}


def necesidad(valores: dict[str, tuple[int, float]]) -> dict[str, Necesidad]:
    """cvegeo -> (viviendas sin agua, horas sin servicio)."""
    return {c: Necesidad(v, h) for c, (v, h) in valores.items()}
