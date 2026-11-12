#!/usr/bin/env python3
"""
Sensibilidad del ORDEN de las manzanas a los supuestos del motor (decision 1 de decisiones/propuesta-dani.md):

    "Si el orden de prioridad de las manzanas casi no cambia entre los extremos, entonces la conclusion no depende
     de los supuestos."

    python3 scripts/sensibilidad_orden.py                    # corrida completa (unos minutos)
    python3 scripts/sensibilidad_orden.py --rapido           # version chica, para las pruebas

Que se mide, para cada escenario frente al caso base (motor/supuestos.json, calendario vigente, zonas base):

  1. El orden de las manzanas. Riesgo de una manzana = viviendas-dia sin agua en la semana (cota minima y cota maxima).
       - rho de Spearman contra el orden base (con empates promediados)
       - solape del top-k: de las k manzanas de mayor riesgo en el base, cuantas siguen entre las k de mayor riesgo
       - cobertura del riesgo: del riesgo total del escenario, que fraccion captura el top-k del BASE frente a su propio
         top-k. No depende de como se rompan los empates: es lo que se pierde por decidir con el orden del base.
  2. Las conclusiones del proyecto: parte del riesgo que cae en las zonas 5 y 6, lugar de El Sauz entre las colonias,
     solape del top-10 de colonias, parte del riesgo en AGEB de marginacion Muy bajo.
  3. El priorizador de Jass corrido sobre cada escenario: viviendas-dia atendidas, cuantas veces el baseline, y solape
     de las manzanas atendidas.

Ademas produce, a partir de Monte Carlo:
  - manzanas_robustas.csv: con que frecuencia cada manzana queda entre las 250 de mayor riesgo. El "nucleo robusto" son las que
    quedan en al menos el 90% de los sorteos de la familia A (los rangos de la decision 1): es la parte del orden que NO depende de
    los supuestos.
  - importancia.csv: que supuesto mueve mas el orden (correlacion de rangos entre cada parametro y rho, y con la parte de zonas 5 y 6).

Escenarios: barridos de un parametro a la vez (OAT), esquinas, variantes de zonas y calendario, un barrido fino de consumo y
tinaco (para ubicar el punto donde cambia el orden), y Monte Carlo con semilla fija. Todo es determinista.

Nota de transparencia: los criterios se fijaron antes de la corrida completa, pero despues de una corrida de prueba sobre una
submuestra del 10% de las manzanas. Despues de esa prueba se cambio UNA cosa: el rho se calcula solo entre manzanas con riesgo
positivo (antes, sobre todas). Es el cambio conservador: baja el rho, no lo sube.

CRITERIOS DE ROBUSTEZ (fijados ANTES de ver los resultados; son convenciones nuestras, no un estandar):
  - Orden estable:        rho >= 0.90 (Spearman entre las manzanas con riesgo positivo en el base o en el escenario; incluir
                          las de riesgo cero, que son las mismas en todos los escenarios, inflaria la correlacion)
                          y cobertura del riesgo del top-250 >= 0.90
  - Conclusion B estable: zonas 5 y 6 dentro de +-10 puntos porcentuales de su valor base; El Sauz entre las 3 primeras
                          colonias; el grado Muy bajo sigue siendo el de mayor parte del riesgo
  - Priorizador estable:  atiende al menos 2 veces lo que el baseline con la cota minima
"""
import argparse
import csv
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "motor"))
import exporta_app as X  # noqa: E402
import referencia as R  # noqa: E402

SEMILLA = 20261112
VENTANA = ("2026-11-09", "2026-11-15")
K_TOP = (100, 250, 500)
UMBRAL_RHO, UMBRAL_COBERTURA, UMBRAL_PRIORIZADOR, TOL_ZONAS_PP = 0.90, 0.90, 2.0, 10.0

# Rangos de los barridos y de Monte Carlo, con su procedencia
#   decision : de las decisiones del equipo (decisiones/propuesta-dani.md, motor/ESPECIFICACION.md sec. 10)
#   literatura: valores que aparecen en las referencias (datos/evidencia.csv)
#   sin_fuente: rango ilustrativo; el repo no tiene una fuente (declararlo)
BARRIDOS = [
    ("consumo_l_persona_dia", [50, 60, 75, 100], "decision"),
    ("consumo_l_persona_dia", [120], "literatura"),     # Maputo (E007)
    ("consumo_l_persona_dia", [150], "sin_fuente"),
    ("tinaco_l", [750, 900, 1100], "decision"),
    ("tinaco_l", [450, 600, 1500, 2500], "sin_fuente"),
    ("cisterna_l", [2500, 3500, 7500, 10000], "sin_fuente"),
    ("horas_efectivas_corte", [24, 36, 48], "decision"),
    ("fraccion_suministro_en_racionamiento", [0.0, 0.25, 0.5], "decision"),
    ("fraccion_suministro_en_racionamiento", [0.75], "sin_fuente"),
    ("u_horas_agua_guardada", [24, 48, 72], "decision"),
]
ESQUINAS = {
    "favorable": ({"consumo_l_persona_dia": 50, "tinaco_l": 1100, "fraccion_suministro_en_racionamiento": 0.5, "horas_efectivas_corte": 24}, "decision"),
    "adversa": ({"consumo_l_persona_dia": 100, "tinaco_l": 750, "fraccion_suministro_en_racionamiento": 0.0, "horas_efectivas_corte": 48}, "decision"),
    "adversa_extrema": ({"consumo_l_persona_dia": 150, "tinaco_l": 450, "cisterna_l": 2500, "fraccion_suministro_en_racionamiento": 0.0,
                         "horas_efectivas_corte": 48}, "sin_fuente"),
}
# Monte Carlo: A = solo los rangos de la decision 1; B = todo lo incierto
MC_RANGOS = {
    "A": {"consumo_l_persona_dia": (50, 100), "tinaco_l": (750, 1100), "u_horas_agua_guardada": (24, 72)},
    "B": {"consumo_l_persona_dia": (50, 100), "tinaco_l": (750, 1100), "u_horas_agua_guardada": (24, 72),
          "cisterna_l": (2500, 10000), "horas_efectivas_corte": (24, 48), "fraccion_suministro_en_racionamiento": (0.0, 0.5)},
}
VARIANTES_ZONAS = ["solo_lista", "conflicto_portal", "conflicto_lista"]
BARRIDO_FINO = {"consumo_l_persona_dia": list(range(50, 101, 5)), "tinaco_l": list(range(600, 1101, 50))}


class Mundo:
    """Datos fijos de la corrida: manzanas, zonas y calendarios."""

    def __init__(self, submuestra=1):
        todas = X.cargar_manzanas()
        self.man = todas[::submuestra]
        self.n = len(self.man)
        self.idx = {m["cvegeo"]: i for i, m in enumerate(self.man)}
        self.filas = [{"cvegeo": m["cvegeo"], "viviendas": m["viviendas"], "viv_tinaco": m["viv_tinaco"],
                       "viv_cisterna": m["viv_cisterna"], "ocupantes_prom": m["ocupantes_prom"]} for m in self.man]
        self.ocup = np.array([m["ocupantes_prom"] for m in self.man])
        self.orden = np.arange(self.n)  # desempate determinista: el orden del archivo (por cvegeo)
        self.colonia = np.array([m["colonia"] for m in self.man])
        self.grado = np.array([m["grado_marginacion"] for m in self.man])
        self.fechas = R.rango_fechas(*VENTANA)
        self.sup_base = R.leer_json(RAIZ / "motor" / "supuestos.json")
        self.cal = {"vigente": R.leer_json(RAIZ / "motor" / "calendarios" / "vigente-2026-11-03.json")["esquema"],
                    "original": R.leer_json(RAIZ / "motor" / "calendarios" / "original-2026-10-15.json")["esquema"]}
        zon = {r["cvegeo"]: r for r in X.leer("datos/zonas_siapa/manzana_zona.csv")}
        base = {m["cvegeo"]: m["zona"] for m in self.man}
        self.zonas = {"base": base}
        for nombre in VARIANTES_ZONAS:
            z = dict(base)
            for c in base:
                r = zon.get(c)
                if not r:
                    continue
                conf = r["confianza"]
                if nombre == "solo_lista":
                    if conf == "baja":
                        z[c] = ""
                    elif conf == "conflicto":
                        z[c] = r["zona_lista"]
                elif nombre == "conflicto_portal" and conf == "conflicto":
                    z[c] = r["zona_portal"]
                elif nombre == "conflicto_lista" and conf == "conflicto":
                    z[c] = r["zona_lista"]
            self.zonas[nombre] = z


def correr(mundo, cambios=None, calendario="vigente", zonas="base", estado_csv=None):
    """Corre el motor de referencia y devuelve el riesgo semanal por manzana (arreglos alineados con mundo.man)."""
    sup = dict(mundo.sup_base, **(cambios or {}))
    acc = {k: np.zeros(mundo.n) for k in ("viv_min", "viv_max", "gua_min", "gua_max")}
    filas_csv = []
    for r in R.procesar(mundo.filas, mundo.zonas[zonas], mundo.cal[calendario], mundo.fechas, sup):
        i = mundo.idx[r["cvegeo"]]
        acc["viv_min"][i] += r["viv_sin_agua_min"]
        acc["viv_max"][i] += r["viv_sin_agua_max"]
        acc["gua_min"][i] += r["viv_agua_guardada_min"]
        acc["gua_max"][i] += r["viv_agua_guardada_max"]
        if estado_csv is not None:
            filas_csv.append(r)
    if estado_csv is not None:
        with open(estado_csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=R.COLUMNAS)
            w.writeheader()
            w.writerows(filas_csv)
    acc["zonas"] = mundo.zonas[zonas]
    acc["sup"] = sup
    return acc


def spearman(a, b):
    ra, rb = pd.Series(a).rank(method="average"), pd.Series(b).rank(method="average")
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(ra.corr(rb))


def top_k(valores, k, orden):
    """Indices de las k manzanas de mayor riesgo POSITIVO, con desempate determinista."""
    idx = np.lexsort((orden, -valores))[:k]
    return idx[valores[idx] > 0]


def riesgo_por_colonia(valores, colonias):
    s = pd.Series(valores).groupby(colonias).sum()
    s = s[s.index != ""]
    return s.sort_values(ascending=False, kind="stable")


def parte_zonas_5_6(valores, zonas, mundo):
    total = valores.sum()
    if total == 0:
        return float("nan")
    grupo = np.array([bool(zonas[m["cvegeo"]]) and set(zonas[m["cvegeo"]].split(",")) <= {"5", "6"} for m in mundo.man])
    return float(valores[grupo].sum() / total)


def metricas(mundo, base, esc):
    out = {"viv_dia_min": float(esc["viv_min"].sum()), "viv_dia_max": float(esc["viv_max"].sum()),
           "personas_dia_min": float((esc["viv_min"] * mundo.ocup).sum()), "gua_dia_min": float(esc["gua_min"].sum())}
    out["rho_min"] = spearman(base["viv_min"], esc["viv_min"])
    pos = (base["viv_min"] > 0) | (esc["viv_min"] > 0)
    out["rho_positivos_min"] = spearman(base["viv_min"][pos], esc["viv_min"][pos])
    out["manzanas_con_riesgo"] = int(pos.sum())
    out["rho_max"] = spearman(base["viv_max"], esc["viv_max"])
    out["rho_guardada"] = spearman(base["gua_min"], esc["gua_min"])
    for k in K_TOP:
        tb, te = top_k(base["viv_min"], k, mundo.orden), top_k(esc["viv_min"], k, mundo.orden)
        k_ef = len(tb)
        out[f"solape_top{k}"] = len(set(tb) & set(te)) / k_ef if k_ef else float("nan")
        propio = esc["viv_min"][te].sum()
        out[f"cobertura_top{k}"] = float(esc["viv_min"][tb].sum() / propio) if propio > 0 else float("nan")
    cb, ce = riesgo_por_colonia(base["viv_min"], mundo.colonia), riesgo_por_colonia(esc["viv_min"], mundo.colonia)
    out["solape_top10_colonias"] = len(set(cb.index[:10]) & set(ce.index[:10])) / 10
    out["lugar_el_sauz"] = int(list(ce.index).index("El Sauz")) + 1 if "El Sauz" in ce.index and ce["El Sauz"] > 0 else None
    out["parte_zonas_5_6_pct"] = round(100 * parte_zonas_5_6(esc["viv_min"], esc["zonas"], mundo), 2)
    tot = esc["viv_min"].sum()
    por_grado = {g: float(esc["viv_min"][mundo.grado == g].sum() / tot) if tot else float("nan") for g in X.GRADOS}
    out["parte_muy_bajo_pct"] = round(100 * por_grado["Muy bajo"], 2)
    out["grado_mayor_riesgo"] = max(por_grado, key=lambda g: (por_grado[g] if por_grado[g] == por_grado[g] else -1))
    return out


def evaluar_criterios(m, base_m):
    orden_ok = bool(m["rho_positivos_min"] >= UMBRAL_RHO and m["cobertura_top250"] >= UMBRAL_COBERTURA)
    b_ok = bool(abs(m["parte_zonas_5_6_pct"] - base_m["parte_zonas_5_6_pct"]) <= TOL_ZONAS_PP
                and m["lugar_el_sauz"] is not None and m["lugar_el_sauz"] <= 3 and m["grado_mayor_riesgo"] == "Muy bajo")
    return orden_ok, b_ok


def correr_priorizador(mundo, esc_runner, base_sets=None):
    """Corre el motor guardando el estado y luego el priorizador de Jass. Devuelve metricas y los conjuntos de manzanas."""
    with tempfile.TemporaryDirectory() as tmp:
        estado, plan = Path(tmp) / "estado.csv", Path(tmp) / "plan.json"
        esc_runner(estado)
        subprocess.run([sys.executable, "-m", "optimizador.priorizador", "--estado", str(estado), "--salida", str(plan)],
                       cwd=RAIZ, check=True, capture_output=True)
        p = json.loads(plan.read_text(encoding="utf-8"))
    comp = {c["cota_para_ordenar"]: c["semana"]["viviendas_atendidas"] for c in p["comparacion"]}
    prio_min = next(c for c in p["corridas"] if c["regla"] == "priorizado" and c["cota_para_ordenar"] == "min")
    eficiencia = prio_min["semana"]["eficiencia_viviendas_pct"]
    cubiertas = {mc["cvegeo"] for d in prio_min["fechas"] for v in d["viajes"] for mc in v["manzanas_cubiertas"]}
    centros = {v["cvegeo_centro"] for d in prio_min["fechas"] for v in d["viajes"]}
    out = {"prio_atendidas_min": comp["min"]["priorizado"], "base_atendidas_min": comp["min"]["baseline"],
           "prio_veces_baseline_min": round(comp["min"]["priorizado"] / comp["min"]["baseline"], 2) if comp["min"]["baseline"] else None,
           "prio_atendidas_max": comp["max"]["priorizado"], "base_atendidas_max": comp["max"]["baseline"],
           "prio_eficiencia_pct": eficiencia}
    if base_sets is not None:
        out["solape_manzanas_atendidas"] = round(len(cubiertas & base_sets["cubiertas"]) / len(cubiertas | base_sets["cubiertas"]), 4)
        out["solape_centros"] = round(len(centros & base_sets["centros"]) / len(centros | base_sets["centros"]), 4)
    return out, {"cubiertas": cubiertas, "centros": centros}


def lista_escenarios():
    esc = [("base", "base", "", None, "decision", {}, "vigente", "base")]
    for param, valores, procedencia in BARRIDOS:
        for v in valores:
            esc.append((f"{param}={v}", "barrido", param, v, procedencia, {param: v}, "vigente", "base"))
    for nombre, (cambios, proc) in ESQUINAS.items():
        esc.append((f"esquina_{nombre}", "esquina", "", None, proc, cambios, "vigente", "base"))
    esc.append(("calendario_original", "calendario", "calendario", "original", "decision", {}, "original", "base"))
    for z in VARIANTES_ZONAS:
        esc.append((f"zonas_{z}", "zonas", "zonas", z, "decision", {}, "vigente", z))
    return esc


def mc_muestras(n, familia):
    rng = random.Random(SEMILLA + (0 if familia == "A" else 1))
    out = []
    for _ in range(n):
        out.append({p: round(rng.uniform(lo, hi), 4) for p, (lo, hi) in MC_RANGOS[familia].items()})
    return out


def escribir(ruta, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    campos = []
    for f in filas:
        for k in f:
            if k not in campos:
                campos.append(k)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for f in filas:
            w.writerow({k: ("" if v is None or (isinstance(v, float) and v != v) else (round(v, 4) if isinstance(v, float) else v))
                        for k, v in f.items()})


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--muestras", type=int, default=300, help="sorteos de Monte Carlo por familia")
    p.add_argument("--priorizador-n", type=int, default=60, help="sorteos de Monte Carlo (por familia) donde tambien se corre el priorizador")
    p.add_argument("--rapido", action="store_true", help="version chica: submuestra de manzanas y pocos sorteos (para las pruebas)")
    p.add_argument("--salida", default=str(RAIZ / "datos" / "sensibilidad"))
    a = p.parse_args(argv)
    if a.rapido:
        a.muestras, a.priorizador_n = 6, 0
    mundo = Mundo(submuestra=10 if a.rapido else 1)
    salida = Path(a.salida)
    hacer_prio = not a.rapido

    base = correr(mundo)
    base_m = metricas(mundo, base, base)
    base_prio, base_sets = (correr_priorizador(mundo, lambda e: correr(mundo, estado_csv=e)) if hacer_prio else ({}, None))

    filas = []
    for (nombre, familia, param, valor, proc, cambios, cal, zon) in lista_escenarios():
        esc = correr(mundo, cambios, cal, zon)
        m = metricas(mundo, base, esc)
        orden_ok, b_ok = evaluar_criterios(m, base_m)
        fila = {"escenario": nombre, "familia": familia, "parametro": param, "valor": valor, "procedencia_del_rango": proc, **m,
                "orden_estable": orden_ok, "conclusion_b_estable": b_ok}
        if hacer_prio:
            pm, _ = correr_priorizador(mundo, lambda e, c=cambios, k=cal, z=zon: correr(mundo, c, k, z, estado_csv=e), base_sets)
            fila.update(pm)
            fila["priorizador_estable"] = bool(pm["prio_veces_baseline_min"] is not None and pm["prio_veces_baseline_min"] >= UMBRAL_PRIORIZADOR)
        filas.append(fila)
    # el orden segun la cota MAXIMA frente al de la cota minima: es la incertidumbre propia del Censo (cuantos tienen ambos)
    lente = dict(base)
    lente["viv_min"] = base["viv_max"]
    m = metricas(mundo, base, lente)
    filas.append({"escenario": "lente_cota_maxima", "familia": "lente", "parametro": "", "valor": "max", "procedencia_del_rango": "censo", **m,
                  "orden_estable": bool(m["rho_positivos_min"] >= UMBRAL_RHO and m["cobertura_top250"] >= UMBRAL_COBERTURA),
                  "conclusion_b_estable": evaluar_criterios(m, base_m)[1]})
    escribir(salida / "escenarios.csv", filas)

    fino = []
    for param, valores in BARRIDO_FINO.items():
        for v in valores:
            esc = correr(mundo, {param: v})
            m = metricas(mundo, base, esc)
            fino.append({"parametro": param, "valor": v, **m})
    escribir(salida / "barrido_fino.csv", fino)

    mc = []
    arreglos = {"A": [], "B": []}
    for familia in ("A", "B"):
        for j, cambios in enumerate(mc_muestras(a.muestras, familia)):
            esc = correr(mundo, cambios)
            arreglos[familia].append(esc["viv_min"])
            m = metricas(mundo, base, esc)
            orden_ok, b_ok = evaluar_criterios(m, base_m)
            fila = {"familia": familia, "sorteo": j, **{f"p_{k}": v for k, v in cambios.items()}, **m,
                    "orden_estable": orden_ok, "conclusion_b_estable": b_ok}
            if hacer_prio and j < a.priorizador_n:
                pm, _ = correr_priorizador(mundo, lambda e, c=cambios: correr(mundo, c, estado_csv=e), base_sets)
                fila.update(pm)
            mc.append(fila)
    # nucleo robusto: manzanas que quedan entre las K de mayor riesgo en casi todos los sorteos
    K = 250
    frec = {}
    for fam, arrs in arreglos.items():
        cuenta = np.zeros(mundo.n)
        for v in arrs:
            cuenta[top_k(v, K, mundo.orden)] += 1
        frec[fam] = cuenta / max(len(arrs), 1)
    tb = top_k(base["viv_min"], K, mundo.orden)
    rango_base = np.full(mundo.n, np.nan)
    rango_base[np.lexsort((mundo.orden, -base["viv_min"]))[: int((base["viv_min"] > 0).sum())]] = np.arange(1, int((base["viv_min"] > 0).sum()) + 1)
    sel = sorted(set(np.flatnonzero((frec["A"] > 0) | (frec["B"] > 0))) | set(tb))
    robustas = []
    for i in sel:
        m_ = mundo.man[i]
        robustas.append({"cvegeo": m_["cvegeo"], "colonia": m_["colonia"], "zona": m_["zona"], "grado_marginacion": m_["grado_marginacion"],
                         "viviendas": m_["viviendas"], "viv_dia_min_base": float(base["viv_min"][i]),
                         "rango_base": None if np.isnan(rango_base[i]) else int(rango_base[i]), "en_top250_base": bool(i in set(tb)),
                         "frec_top250_A": round(float(frec["A"][i]), 4), "frec_top250_B": round(float(frec["B"][i]), 4),
                         "nucleo_robusto": bool(frec["A"][i] >= 0.90)})
    robustas.sort(key=lambda r: (-r["frec_top250_A"], -r["frec_top250_B"], r["cvegeo"]))
    escribir(salida / "manzanas_robustas.csv", robustas)
    nucleo = np.array([r["nucleo_robusto"] for r in robustas])
    idx_nucleo = np.array([mundo.idx[r["cvegeo"]] for r, n in zip(robustas, nucleo) if n], dtype=int)
    for fam, arrs in arreglos.items():
        for fila, v in zip([f for f in mc if f["familia"] == fam], arrs):
            tk = top_k(v, len(idx_nucleo), mundo.orden) if len(idx_nucleo) else np.array([], dtype=int)
            propio = v[tk].sum()
            fila["cobertura_nucleo"] = float(v[idx_nucleo].sum() / propio) if propio > 0 else float("nan")
    escribir(salida / "montecarlo.csv", mc)

    # que supuesto mueve mas el orden
    imp = []
    for fam in ("A", "B"):
        d = [f for f in mc if f["familia"] == fam]
        for p_ in MC_RANGOS[fam]:
            x = np.array([f[f"p_{p_}"] for f in d], dtype=float)
            fila = {"familia": fam, "parametro": p_, "rango_bajo": MC_RANGOS[fam][p_][0], "rango_alto": MC_RANGOS[fam][p_][1]}
            for nombre, col in (("rho_orden", "rho_positivos_min"), ("cobertura_top250", "cobertura_top250"), ("parte_zonas_5_6", "parte_zonas_5_6_pct"),
                                ("parte_muy_bajo", "parte_muy_bajo_pct"), ("viv_dia_min", "viv_dia_min")):
                fila[f"spearman_con_{nombre}"] = spearman(x, np.array([f[col] for f in d], dtype=float))
            if hacer_prio:
                dp = [f for f in d if "solape_manzanas_atendidas" in f]
                fila["spearman_con_solape_manzanas_atendidas"] = spearman(np.array([f[f"p_{p_}"] for f in dp], dtype=float),
                                                                        np.array([f["solape_manzanas_atendidas"] for f in dp], dtype=float))
            imp.append(fila)
    escribir(salida / "importancia.csv", imp)
    print(f"nucleo robusto: {int(nucleo.sum())} manzanas (frecuencia >= 90% en el top-{K} de la familia A)")
    print(f"escenarios: {len(filas)} | Monte Carlo: {len(mc)} sorteos | base: {base_m['viv_dia_min']:.0f} viv-dia (min), "
          f"zonas 5-6 {base_m['parte_zonas_5_6_pct']}%, El Sauz lugar {base_m['lugar_el_sauz']}")
    return filas, mc


if __name__ == "__main__":
    main()
