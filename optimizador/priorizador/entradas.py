"""Lectura de entradas y parametros del priorizador (secciones 2 y 3 de ESPECIFICACION.md)."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass

COTAS = ("min", "max")
MODOS_RACHA = ("desempate", "peso", "no")
BASELINE_CISTERNAS = ("todas", "exactas")
BASELINE_TURNOS = ("todas", "con_necesidad")
CAMPOS_PARAMETROS = (
    "pipas",
    "viajes_por_dia",
    "litros_por_viaje",
    "litros_por_hogar",
    "radio_cobertura_m",
    "cota_para_ordenar",
    "modo_racha",
    "baseline_cisternas",
    "baseline_turnos",
)


@dataclass(frozen=True)
class Parametros:
    """Valores de supuestos.json que usa el calculo."""

    pipas: int
    viajes_por_dia: int
    litros_por_viaje: float
    litros_por_hogar: float
    radio_cobertura_m: float
    cota_para_ordenar: str
    modo_racha: str
    baseline_cisternas: str = "todas"
    baseline_turnos: str = "todas"

    @property
    def hogares_por_viaje(self) -> int:
        return int(self.litros_por_viaje // self.litros_por_hogar)

    def validar(self) -> "Parametros":
        if self.cota_para_ordenar not in COTAS:
            raise ValueError(f"cota_para_ordenar debe ser una de {COTAS}: {self.cota_para_ordenar!r}")
        if self.modo_racha not in MODOS_RACHA:
            raise ValueError(f"modo_racha debe ser uno de {MODOS_RACHA}: {self.modo_racha!r}")
        if self.baseline_cisternas not in BASELINE_CISTERNAS:
            raise ValueError(f"baseline_cisternas debe ser uno de {BASELINE_CISTERNAS}: {self.baseline_cisternas!r}")
        if self.baseline_turnos not in BASELINE_TURNOS:
            raise ValueError(f"baseline_turnos debe ser uno de {BASELINE_TURNOS}: {self.baseline_turnos!r}")
        if self.viajes_por_dia < 0:
            raise ValueError("viajes_por_dia no puede ser negativo")
        if self.litros_por_hogar <= 0 or self.hogares_por_viaje < 1:
            raise ValueError("un viaje debe alcanzar para al menos un hogar")
        if self.radio_cobertura_m <= 0:
            raise ValueError("radio_cobertura_m debe ser positivo")
        return self

    def como_dict(self) -> dict:
        return {**asdict(self), "hogares_por_viaje": self.hogares_por_viaje}


@dataclass(frozen=True)
class Necesidad:
    """Viviendas sin agua de una manzana en una fecha y las horas que lleva sin servicio."""

    viviendas: int
    horas: float

    @property
    def peso(self) -> float:
        return self.horas / 24


def leer_supuestos(ruta: str, cambios: dict[str, str] | None = None) -> Parametros:
    """Lee supuestos.json. `cambios` sobrescribe valores, como el --set del motor."""
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    for clave, texto in (cambios or {}).items():
        if clave not in CAMPOS_PARAMETROS:
            raise ValueError(f"parametro desconocido: {clave}")
        actual = datos.get(clave, "")
        datos[clave] = texto if isinstance(actual, str) else type(actual)(texto)
    try:
        return Parametros(**{c: datos[c] for c in CAMPOS_PARAMETROS if c in datos}).validar()
    except TypeError as e:
        raise ValueError(f"faltan parametros en {ruta}: {e}") from None


def leer_estado(ruta: str, cota: str) -> dict[str, dict[str, Necesidad]]:
    """Devuelve fecha -> cvegeo -> Necesidad, solo con manzanas que tienen viviendas sin agua.

    Toda fecha del archivo aparece en el resultado, aunque quede vacia.
    """
    if cota not in COTAS:
        raise ValueError(f"cota debe ser una de {COTAS}: {cota!r}")
    col_viv, col_horas = f"viv_sin_agua_{cota}", f"horas_sin_servicio_{cota}"
    estado: dict[str, dict[str, Necesidad]] = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        faltan = {"cvegeo", "fecha", col_viv, col_horas} - set(lector.fieldnames or [])
        if faltan:
            raise ValueError(f"faltan columnas en {ruta}: {sorted(faltan)}")
        for fila in lector:
            dia = estado.setdefault(fila["fecha"], {})
            viviendas = int(float(fila[col_viv]))
            if viviendas <= 0:
                continue
            horas = float(fila[col_horas])
            if horas <= 0:
                raise ValueError(
                    f"{fila['cvegeo']} {fila['fecha']}: {viviendas} viviendas sin agua con {horas} horas sin servicio"
                )
            if fila["cvegeo"] in dia:
                raise ValueError(f"{fila['cvegeo']} {fila['fecha']}: renglon repetido")
            dia[fila["cvegeo"]] = Necesidad(viviendas, horas)
    return dict(sorted(estado.items()))


def leer_ubicaciones(ruta: str) -> dict[str, tuple[float, float]]:
    """cvegeo -> (lon, lat) del centroide."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return {r["cvegeo"]: (float(r["lon"]), float(r["lat"])) for r in csv.DictReader(f)}


def leer_ocupantes(ruta: str) -> dict[str, float]:
    """cvegeo -> ocupantes promedio por vivienda."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return {r["cvegeo"]: float(r["ocupantes_prom"]) for r in csv.DictReader(f)}


def leer_colonias(ruta: str) -> dict[str, str]:
    """cvegeo -> nombre de la colonia (puede ser vacio)."""
    return {c: nombre for c, (_, nombre) in leer_geocolonias(ruta).items()}


def leer_geocolonias(ruta: str) -> dict[str, tuple[str, str]]:
    """cvegeo -> (geocol, nombre de la colonia). Cualquiera de los dos puede ser vacio."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return {r["cvegeo"]: (r["geocol"].strip(), r["colonia"].strip()) for r in csv.DictReader(f)}
