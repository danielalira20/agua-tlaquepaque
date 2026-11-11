"""Baseline estilizado: los mismos viajes, por turnos entre las cisternas instaladas (seccion 7)."""
from __future__ import annotations

import csv
from dataclasses import dataclass

from .asignacion import ResultadoDia, Viaje
from .cobertura import haversine_m, llenar, vecinas_de_punto
from .entradas import Necesidad, Parametros

TIPOS_CISTERNA = ("cisterna_municipal", "cisterna_siapa")
MARGEN_GRADOS = 0.02


@dataclass(frozen=True)
class Cisterna:
    """`id` es unico: el id del archivo mas el tipo, porque el SIAPA y el municipio repiten ids."""

    id: str
    tipo: str
    punto: tuple[float, float]
    ubicacion: str
    cvegeo_cercana: str


def leer_cisternas(ruta: str) -> list[dict]:
    """Renglones de cisternas instaladas; las propuestas se descartan."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["tipo"] in TIPOS_CISTERNA]


def clave_cisterna(fila: dict) -> str:
    """CIST001@municipal o CIST001@siapa."""
    return f"{fila['id']}@{fila['tipo'].replace('cisterna_', '')}"


def _geocol(texto: str) -> str:
    texto = texto.strip()
    return str(int(float(texto))).zfill(6) if texto else ""


def ubicar_cisternas(
    filas: list[dict],
    ubicaciones: dict[str, tuple[float, float]],
    geocolonias: dict[str, tuple[str, str]],
) -> tuple[list[Cisterna], list[str]]:
    """Ubica cada cisterna en su coordenada exacta o en el centro de su colonia.

    Devuelve las cisternas ubicadas, ordenadas por clave, y las claves de las que quedan fuera.
    """
    claves = [clave_cisterna(r) for r in filas]
    repetidas = sorted({c for c in claves if claves.count(c) > 1})
    if repetidas:
        raise ValueError(f"cisternas repetidas: {repetidas}")
    lons = [u[0] for u in ubicaciones.values()]
    lats = [u[1] for u in ubicaciones.values()]
    caja = (min(lons) - MARGEN_GRADOS, max(lons) + MARGEN_GRADOS, min(lats) - MARGEN_GRADOS, max(lats) + MARGEN_GRADOS)

    manzanas_de: dict[str, list[str]] = {}
    geocols_de_nombre: dict[str, set[str]] = {}
    for cvegeo, (geocol, nombre) in geocolonias.items():
        if geocol and cvegeo in ubicaciones:
            manzanas_de.setdefault(geocol, []).append(cvegeo)
        if geocol and nombre:
            geocols_de_nombre.setdefault(nombre, set()).add(geocol)

    ubicadas: list[Cisterna] = []
    fuera: list[str] = []
    for r in sorted(filas, key=clave_cisterna):
        punto, como = None, ""
        if r["fuente_ubicacion"] == "coordenada_exacta" and r["lon"].strip() and r["lat"].strip():
            lon, lat = float(r["lon"]), float(r["lat"])
            if caja[0] <= lon <= caja[1] and caja[2] <= lat <= caja[3]:
                punto, como = (lon, lat), "exacta"
        if punto is None and r["colonia_capa"].strip():
            geocol = _geocol(r["geocol"])
            if not geocol:
                candidatas = geocols_de_nombre.get(r["colonia_capa"].strip(), set())
                geocol = next(iter(candidatas)) if len(candidatas) == 1 else ""
            mzs = manzanas_de.get(geocol)
            if mzs:
                punto = (
                    sum(ubicaciones[m][0] for m in mzs) / len(mzs),
                    sum(ubicaciones[m][1] for m in mzs) / len(mzs),
                )
                como = "colonia"
        if punto is None:
            fuera.append(clave_cisterna(r))
            continue
        cercana = min(ubicaciones, key=lambda c: (haversine_m(punto, ubicaciones[c]), c))
        ubicadas.append(Cisterna(clave_cisterna(r), r["tipo"], punto, como, cercana))
    return ubicadas, fuera


def seleccionar(cisternas: list[Cisterna], p: Parametros) -> list[Cisterna]:
    if p.baseline_cisternas == "exactas":
        return [c for c in cisternas if c.ubicacion == "exacta"]
    return list(cisternas)


def asignar_dia_baseline(
    fecha: str,
    indice_fecha: int,
    necesidad: dict[str, Necesidad],
    ubicaciones: dict[str, tuple[float, float]],
    cisternas: list[Cisterna],
    p: Parametros,
) -> ResultadoDia:
    """El viaje k de la fecha con indice i va a la cisterna (i * viajes_por_dia + k - 1) mod N.

    Con baseline_turnos = con_necesidad, los turnos solo pasan por las cisternas que al empezar
    el dia tienen viviendas sin agua dentro del radio.
    """
    secas = {c: n for c, n in necesidad.items() if n.viviendas > 0 and c in ubicaciones}
    ub_secas = {c: ubicaciones[c] for c in secas}
    resto = {c: n.viviendas for c, n in secas.items()}
    peso = {c: n.peso for c, n in secas.items()}
    vecinas = {c.id: vecinas_de_punto(c.punto, ub_secas, p.radio_cobertura_m) for c in cisternas}
    turnos = [c for c in cisternas if vecinas[c.id]] if p.baseline_turnos == "con_necesidad" else list(cisternas)
    if not turnos:
        return ResultadoDia(fecha, (), p.viajes_por_dia)
    inicio = indice_fecha * p.viajes_por_dia

    viajes = []
    for k in range(1, p.viajes_por_dia + 1):
        cis = turnos[(inicio + k - 1) % len(turnos)]
        llenado = llenar(vecinas[cis.id], resto, peso, p.hogares_por_viaje)
        for m, n in llenado.entregas:
            resto[m] -= n
        viajes.append(Viaje(k, cis.cvegeo_cercana, llenado, tipo="cisterna", punto_id=cis.id))
    return ResultadoDia(fecha, tuple(viajes), 0)


def asignar_semana_baseline(
    estado: dict[str, dict[str, Necesidad]],
    ubicaciones: dict[str, tuple[float, float]],
    cisternas: list[Cisterna],
    p: Parametros,
) -> list[ResultadoDia]:
    return [
        asignar_dia_baseline(f, i, estado[f], ubicaciones, cisternas, p)
        for i, f in enumerate(sorted(estado))
    ]
