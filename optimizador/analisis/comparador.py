"""Comparador del priorizador: corre la rejilla de la decision 06 y arma las tablas de resultados/.

El estado de cada escenario lo da el motor de referencia; aqui el priorizador se usa como biblioteca.
No cambia el comando `python3 -m optimizador.priorizador` ni el contrato `plan` v2.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, replace
from pathlib import Path

from optimizador.priorizador.baseline import Cisterna, leer_cisternas, seleccionar, ubicar_cisternas
from optimizador.priorizador.entradas import (
    Necesidad,
    Parametros,
    leer_estado,
    leer_geocolonias,
    leer_ocupantes,
    leer_ubicaciones,
)
from optimizador.priorizador.plan import COTAS_ORDEN, Corrida, correr

GRADOS = ("Muy alto", "Alto", "Medio", "Bajo", "Muy bajo", "sin dato")
LARGO_AGEB = 13
CLAVES_SENSIBILIDAD = ("modo_racha", "radio_cobertura_m", "baseline_turnos", "baseline_cisternas")
# Las tres corridas del caso base que se comparan por grado y por fecha: nombre -> cambios a los parametros.
CORRIDAS_BASE = {
    "prio": ("priorizado", {}),
    "base_turnos": ("baseline", {"baseline_turnos": "todas", "baseline_cisternas": "todas"}),
    "base_con_necesidad": ("baseline", {"baseline_turnos": "con_necesidad", "baseline_cisternas": "todas"}),
}

Estados = dict  # cota -> fecha -> cvegeo -> Necesidad


@dataclass(frozen=True)
class Mundo:
    """Lo que no cambia entre escenarios del motor."""

    ubicaciones: dict[str, tuple[float, float]]
    ocupantes: dict[str, float]
    cisternas: list[Cisterna]
    fuera: list[tuple[str, str]]
    grado_ageb: dict[str, str]

    def grado(self, cvegeo: str) -> str:
        return self.grado_ageb.get(cvegeo[:LARGO_AGEB], "sin dato")


@dataclass(frozen=True)
class Escenario:
    nombre: str
    procedencia: str
    cambios: dict


def leer_grados(ruta: str) -> dict[str, str]:
    """CVE_AGEB -> grado de marginacion (GM_2020)."""
    with open(ruta, newline="", encoding="utf-8") as f:
        grados = {r["CVE_AGEB"]: r["GM_2020"].strip() for r in csv.DictReader(f)}
    raros = sorted(set(grados.values()) - set(GRADOS))
    if raros:
        raise ValueError(f"grados de marginacion desconocidos en {ruta}: {raros}")
    return grados


def cargar_mundo(ubicaciones: str, manzanas: str, colonias: str, cisternas: str, marginacion: str) -> Mundo:
    ub = leer_ubicaciones(ubicaciones)
    geocolonias = leer_geocolonias(colonias)
    ubicadas, fuera = ubicar_cisternas(leer_cisternas(cisternas), ub, geocolonias)
    return Mundo(ub, leer_ocupantes(manzanas), ubicadas, fuera, leer_grados(marginacion))


def leer_sensibilidad(ruta_supuestos: str) -> dict[str, list]:
    """Los valores de la rejilla salen de la seccion `sensibilidad` de supuestos.json."""
    with open(ruta_supuestos, encoding="utf-8") as f:
        sens = json.load(f)["sensibilidad"]
    return {k: list(sens[k]) for k in CLAVES_SENSIBILIDAD}


def leer_escenarios(ruta: str) -> list[Escenario]:
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    lista = [Escenario(e["nombre"], e["procedencia"], dict(e["cambios"])) for e in datos["escenarios"]]
    if not lista or lista[0].nombre != "base" or lista[0].cambios:
        raise ValueError(f"{ruta}: el primer escenario debe ser 'base', sin cambios")
    return lista


def leer_estados(ruta: str) -> Estados:
    return {cota: leer_estado(ruta, cota) for cota in COTAS_ORDEN}


def correr_regla(regla: str, estados: Estados, mundo: Mundo, p: Parametros) -> dict[str, Corrida]:
    """Corre una regla con las dos cotas. Al baseline se le aplica baseline_cisternas."""
    cisternas, _ = seleccionar(mundo.cisternas, mundo.fuera, p)
    return {
        cota: correr(regla, estados[cota], mundo.ubicaciones, mundo.ocupantes, cisternas,
                     replace(p, cota_para_ordenar=cota).validar())
        for cota in COTAS_ORDEN
    }


def veces(a: float, b: float) -> float | None:
    return None if b == 0 else a / b


def pct(parte: float, total: float) -> float | None:
    return None if total == 0 else 100 * parte / total


def comparar(prio: Corrida, base: Corrida) -> dict:
    sp, sb = prio.semana, base.semana
    return {
        "necesidad_viv_dia": sp["necesidad_total"],
        "prio_viv_dia": sp["viviendas_atendidas"],
        "prio_personas_dia": sp["personas_atendidas"],
        "prio_eficiencia_pct": sp["eficiencia_viviendas_pct"],
        "prio_mzas_sin_entrega": sp["manzanas_sin_entrega"],
        "base_viv_dia": sb["viviendas_atendidas"],
        "base_personas_dia": sb["personas_atendidas"],
        "base_viajes_vacios": sb["viajes_vacios"],
        "veces": veces(sp["viviendas_atendidas"], sb["viviendas_atendidas"]),
    }


def rejilla(estados: Estados, mundo: Mundo, p: Parametros, sens: dict[str, list]) -> list[dict]:
    """Cada regla se corre solo con los parametros que usa (decision 06): el priorizado con modo_racha y
    radio; el baseline con radio, baseline_turnos y baseline_cisternas. Luego se cruzan."""
    prio = {
        (racha, radio): correr_regla("priorizado", estados, mundo, replace(p, modo_racha=racha, radio_cobertura_m=radio))
        for racha in sens["modo_racha"]
        for radio in sens["radio_cobertura_m"]
    }
    base = {
        (radio, turnos, cist): correr_regla(
            "baseline", estados, mundo,
            replace(p, radio_cobertura_m=radio, baseline_turnos=turnos, baseline_cisternas=cist),
        )
        for radio in sens["radio_cobertura_m"]
        for turnos in sens["baseline_turnos"]
        for cist in sens["baseline_cisternas"]
    }
    return [
        {"modo_racha": racha, "radio_m": radio, "baseline_turnos": turnos, "baseline_cisternas": cist, "cota": cota,
         **comparar(prio[racha, radio][cota], base[radio, turnos, cist][cota])}
        for racha in sens["modo_racha"]
        for radio in sens["radio_cobertura_m"]
        for turnos in sens["baseline_turnos"]
        for cist in sens["baseline_cisternas"]
        for cota in COTAS_ORDEN
    ]


def escenarios_motor(
    escenarios: list[Escenario], estados_de: dict[str, Estados], mundo: Mundo, p: Parametros, sens: dict[str, list]
) -> list[dict]:
    """Parametros base del priorizador contra los 4 baselines, en cada escenario del motor."""
    filas = []
    for esc in escenarios:
        estados = estados_de[esc.nombre]
        prio = correr_regla("priorizado", estados, mundo, p)
        for turnos in sens["baseline_turnos"]:
            for cist in sens["baseline_cisternas"]:
                base = correr_regla("baseline", estados, mundo, replace(p, baseline_turnos=turnos, baseline_cisternas=cist))
                for cota in COTAS_ORDEN:
                    filas.append({"escenario": esc.nombre, "procedencia": esc.procedencia, "baseline_turnos": turnos,
                                  "baseline_cisternas": cist, "cota": cota, **comparar(prio[cota], base[cota])})
    return filas


def corridas_base(estados: Estados, mundo: Mundo, p: Parametros) -> dict[str, dict[str, Corrida]]:
    return {nombre: correr_regla(regla, estados, mundo, replace(p, **cambios))
            for nombre, (regla, cambios) in CORRIDAS_BASE.items()}


def _por_grado(pares, mundo: Mundo) -> dict[str, int]:
    total = dict.fromkeys(GRADOS, 0)
    for cvegeo, viviendas in pares:
        total[mundo.grado(cvegeo)] += viviendas
    return total


def equidad(estados: Estados, corridas: dict[str, dict[str, Corrida]], mundo: Mundo) -> list[dict]:
    """Viviendas-dia sin agua y atendidas por grado de marginacion de la AGEB, una fila por cota y grado."""
    filas = []
    for cota in COTAS_ORDEN:
        nec = _por_grado(((c, n.viviendas) for dia in estados[cota].values() for c, n in dia.items()), mundo)
        atendidas = {
            nombre: _por_grado(((c, k) for r in cs[cota].resultados for v in r.viajes for c, k in v.llenado.entregas), mundo)
            for nombre, cs in corridas.items()
        }
        total_nec = sum(nec.values())
        total_at = {nombre: sum(a.values()) for nombre, a in atendidas.items()}
        for g in GRADOS:
            if not nec[g] and not any(a[g] for a in atendidas.values()):
                continue
            fila = {"cota": cota, "grado": g, "necesidad_viv_dia": nec[g], "pct_de_la_necesidad": pct(nec[g], total_nec)}
            for nombre, a in atendidas.items():
                fila[f"{nombre}_viv_dia"] = a[g]
                fila[f"{nombre}_pct_de_lo_atendido"] = pct(a[g], total_at[nombre])
                fila[f"{nombre}_cobertura_pct"] = pct(a[g], nec[g])
            filas.append(fila)
    return filas


def cobertura_diaria(corridas: dict[str, dict[str, Corrida]]) -> list[dict]:
    filas = []
    for cota in COTAS_ORDEN:
        dias = {nombre: cs[cota].por_dia for nombre, cs in corridas.items()}
        for i, d in enumerate(dias["prio"]):
            fila = {"cota": cota, "fecha": d["fecha"], "necesidad_viv": d["necesidad_total"]}
            for nombre, por_dia in dias.items():
                if por_dia[i]["fecha"] != d["fecha"]:
                    raise ValueError(f"las fechas de {nombre} no coinciden con las del priorizado")
                fila[f"{nombre}_viv"] = por_dia[i]["viviendas_atendidas"]
                fila[f"{nombre}_cobertura_pct"] = por_dia[i]["cobertura_pct"]
            filas.append(fila)
    return filas


def calcular(estados_de: dict[str, Estados], escenarios: list[Escenario], mundo: Mundo, p: Parametros,
             sens: dict[str, list]) -> dict[str, list[dict]]:
    """Todas las tablas. `estados_de` va del nombre del escenario a su estado; el de 'base' es el del reporte."""
    base = estados_de["base"]
    corridas = corridas_base(base, mundo, p)
    return {
        "rejilla_priorizador": rejilla(base, mundo, p, sens),
        "escenarios_motor": escenarios_motor(escenarios, estados_de, mundo, p, sens),
        "equidad_marginacion": equidad(base, corridas, mundo),
        "cobertura_diaria": cobertura_diaria(corridas),
    }


def _texto(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def escribir_csv(ruta: Path, filas: list[dict]) -> None:
    columnas = list(filas[0])
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(columnas)
        for fila in filas:
            if list(fila) != columnas:
                raise ValueError(f"{ruta.name}: las filas no tienen las mismas columnas")
            w.writerow([_texto(fila[c]) for c in columnas])


def escribir_resultados(carpeta: Path, tablas: dict[str, list[dict]], contexto: dict) -> list[Path]:
    from .resumen import resumen

    carpeta.mkdir(parents=True, exist_ok=True)
    escritos = []
    for nombre, filas in tablas.items():
        escribir_csv(carpeta / f"{nombre}.csv", filas)
        escritos.append(carpeta / f"{nombre}.csv")
    with open(carpeta / "resumen.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(resumen(tablas, contexto))
    escritos.append(carpeta / "resumen.md")
    return escritos
