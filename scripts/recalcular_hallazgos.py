#!/usr/bin/env python3
"""
Recalcula las cifras del proyecto con la zona real de cada manzana.

Reemplaza a las cifras provisionales que salieron de cruzar solo con los polígonos
del portal. Todo lo que se cita en HALLAZGOS_zonas.md sale de aquí.

    python3 scripts/recalcular_hallazgos.py

Entradas:  datos/manzanas_tlaquepaque.csv, datos/zonas_siapa/manzana_zona.csv,
           datos/manzana_colonia.csv, datos/contraste_cisternas.csv,
           motor/calendarios/*.json, motor/supuestos.json
Salidas:   datos/zonas_siapa/riesgo_por_zona.csv
           datos/contraste_cisternas_programa.csv
           datos/zonas_siapa/motor_semana.csv   (sensibilidad del motor, una semana)
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "motor"))
import referencia as R  # noqa: E402

D = RAIZ / "datos"
RESPALDO_LISTA = {"alta", "media", "conflicto"}  # la lista oficial confirma o aporta la zona


def cargar():
    m = pd.read_csv(D / "manzanas_tlaquepaque.csv", dtype={"cvegeo": str})
    z = pd.read_csv(D / "zonas_siapa" / "manzana_zona.csv", dtype=str, keep_default_na=False)
    z = z[["cvegeo", "zona", "confianza"]]
    m = m.merge(z, on="cvegeo", how="left")
    m["zona"] = m["zona"].fillna("")
    m["confianza"] = m["confianza"].fillna("sin_geometria")  # 8 manzanas del Censo sin polígono en el Marco
    m["en_programa"] = m["zona"] != ""
    m["respaldo_lista"] = m["confianza"].isin(RESPALDO_LISTA) & m["en_programa"]
    return m


def grupo_de_zona(zona):
    if zona == "":
        return "fuera"
    zs = set(zona.split(","))
    if zs <= {"3", "4"}:
        return "zonas 3-4"
    if zs <= {"5", "6"}:
        return "zonas 5-6"
    return "mixtas"


def cobertura(m):
    # base: las 4,863 manzanas con geometría (587,874 personas). Las 8 sin geometría no se pueden ubicar
    tot = m.loc[m.confianza != "sin_geometria", "pob"].sum()
    prog = m.loc[m.en_programa, "pob"].sum()
    lista = m.loc[m.respaldo_lista, "pob"].sum()
    print("== Cobertura del programa ==")
    print(f"manzanas del Censo {len(m)} ({int((m.confianza=='sin_geometria').sum())} sin geometría); "
          f"personas con geometría {tot:,} de {m['pob'].sum():,}")
    print(f"en programa: {prog:,} ({100*prog/tot:.1f}%)")
    print(f"  con respaldo de la lista oficial: {lista:,} ({100*lista/tot:.1f}%)")
    print(f"  solo portal: {prog-lista:,} ({100*(prog-lista)/tot:.1f}%)")


def riesgo_por_zona(m):
    p = m[m.en_programa].copy()
    p["grupo"] = p["zona"].map(grupo_de_zona)
    p["respaldo"] = p["respaldo_lista"].map({True: "lista", False: "solo_portal"})
    filas = []
    for nivel, claves in (("zona", ["zona"]), ("grupo", ["grupo"]), ("zona_respaldo", ["zona", "respaldo"])):
        g = p.groupby(claves).agg(manzanas=("cvegeo", "size"), pob=("pob", "sum"),
                                  viviendas=("viviendas", "sum"),
                                  sin_almacen_min=("sin_almacen_min", "sum"),
                                  sin_almacen_max=("sin_almacen_max", "sum")).reset_index()
        g.insert(0, "nivel", nivel)
        filas.append(g)
    out = pd.concat(filas, ignore_index=True)
    out.to_csv(D / "zonas_siapa" / "riesgo_por_zona.csv", index=False)
    total = p["sin_almacen_min"].sum()
    print("\n== Viviendas sin tinaco ni cisterna dentro del programa (cota mínima) ==")
    print(f"total: {total:,}  (cota máxima {p['sin_almacen_max'].sum():,})")
    g = out[out.nivel == "grupo"].copy()
    g["pct_del_riesgo"] = (100 * g.sin_almacen_min / total).round(1)
    print(g[["grupo", "manzanas", "pob", "sin_almacen_min", "sin_almacen_max", "pct_del_riesgo"]].to_string(index=False))
    zr = out[out.nivel == "zona_respaldo"].pivot(index="zona", columns="respaldo", values="sin_almacen_min").fillna(0).astype(int)
    print("\npor zona y respaldo (cota mínima):")
    print(zr.to_string())
    return total


def contraste(m):
    mc = pd.read_csv(D / "manzana_colonia.csv", dtype=str)
    mc = mc.dropna(subset=["geocol"])
    mc["geocol"] = mc["geocol"].astype(int)
    cc = pd.read_csv(D / "contraste_cisternas.csv")
    cc["geocol"] = cc["geocol"].astype(int)
    x = m.merge(mc[["cvegeo", "geocol"]], on="cvegeo", how="left")
    x["sa_prog"] = x["sin_almacen_min"].where(x.en_programa, 0)
    x["sa_lista"] = x["sin_almacen_min"].where(x.respaldo_lista, 0)
    x["pob_prog"] = x["pob"].where(x.en_programa, 0)
    g = x.groupby("geocol").agg(pob=("pob", "sum"), pob_programa=("pob_prog", "sum"),
                                sin_almacen_min=("sin_almacen_min", "sum"),
                                sin_almacen_programa=("sa_prog", "sum"),
                                sin_almacen_lista=("sa_lista", "sum")).reset_index()
    g = g.merge(cc[["geocol", "colonia", "n_cisternas", "n_propuestas"]], on="geocol", how="left")
    g["pct_pob_en_programa"] = (100 * g.pob_programa / g.pob).round(1)
    g["tiene_cisterna"] = g.n_cisternas.fillna(0) > 0

    def rank(col, base):
        r = pd.Series(float("nan"), index=g.index)
        r[base] = g.loc[base, col].rank(ascending=False, method="min")
        return r

    g["rank_riesgo_total"] = rank("sin_almacen_min", g.sin_almacen_min > 0)
    g["rank_riesgo_programa"] = rank("sin_almacen_programa", g.sin_almacen_programa > 0)
    g["rank_riesgo_lista"] = rank("sin_almacen_lista", g.sin_almacen_lista > 0)
    g = g.sort_values("rank_riesgo_programa", na_position="last")
    g.to_csv(D / "contraste_cisternas_programa.csv", index=False)

    print("\n== Contraste con las cisternas, por colonia (IIEG) ==")
    for nombre, col in (("todas las colonias (cifra anterior)", "rank_riesgo_total"),
                        ("solo riesgo dentro del programa", "rank_riesgo_programa"),
                        ("solo riesgo con respaldo de la lista oficial", "rank_riesgo_lista")):
        b = g[g[col].notna()]
        con = b[b.tiene_cisterna][col].median()
        sin = b[~b.tiene_cisterna][col].median()
        print(f"{nombre}: {len(b)} colonias | rank mediano con cisterna {con:.0f} ({int(b.tiene_cisterna.sum())}) "
              f"| sin cisterna {sin:.0f} ({int((~b.tiene_cisterna).sum())})")
    top = g[g.rank_riesgo_programa <= 20]
    print(f"\nde las 20 colonias de mayor riesgo dentro del programa: {int(top.tiene_cisterna.sum())} con cisterna, "
          f"{int((~top.tiene_cisterna).sum())} sin")
    print(top[["rank_riesgo_programa", "colonia", "pob_programa", "pct_pob_en_programa", "sin_almacen_programa",
               "sin_almacen_lista", "n_cisternas", "n_propuestas"]].to_string(index=False))
    fuera = g[(g.sin_almacen_min > 0) & (g.sin_almacen_programa == 0) & (g.rank_riesgo_total <= 30)]
    print("\ncolonias entre las 30 de mayor riesgo total que NO reciben racionamiento:")
    print(fuera[["rank_riesgo_total", "colonia", "pob", "sin_almacen_min", "n_cisternas", "n_propuestas"]].to_string(index=False))
    prop = g[g.n_propuestas.fillna(0) > 0]
    print("\ncolonias con cisterna propuesta (rank dentro del programa; vacío = fuera del programa o sin riesgo):")
    print(prop[["colonia", "rank_riesgo_programa", "sin_almacen_programa", "pct_pob_en_programa"]].to_string(index=False))


def motor(m):
    rows = list(m.assign(viviendas=m.viviendas.astype(float)).astype(str).to_dict("records"))
    zonas = {r["cvegeo"]: r["zona"] for r in rows}
    fechas = R.rango_fechas("2026-11-09", "2026-11-15")
    salida = []

    def corre(etiqueta, calendario, cambios):
        sup = R.cargar_supuestos(RAIZ / "motor" / "supuestos.json", cambios)
        esquema = R.leer_json(RAIZ / "motor" / "calendarios" / calendario)["esquema"]
        tot_min = tot_max = viv_min = viv_max = 0.0
        for f in R.procesar(rows, zonas, esquema, fechas, sup):
            tot_min += f["personas_sin_agua_min"]
            tot_max += f["personas_sin_agua_max"]
            viv_min += f["viv_sin_agua_min"]
            viv_max += f["viv_sin_agua_max"]
        salida.append({"escenario": etiqueta, "calendario": calendario.replace(".json", ""),
                       "cambios": " ".join(cambios), "personas_dia_sin_agua_min": round(tot_min),
                       "personas_dia_sin_agua_max": round(tot_max), "viv_dia_sin_agua_min": int(viv_min),
                       "viv_dia_sin_agua_max": int(viv_max)})

    v, o = "vigente-2026-11-03.json", "original-2026-10-15.json"
    corre("base vigente", v, [])
    corre("base original", o, [])
    for c in (100, 150):
        corre(f"consumo {c} L", v, [f"consumo_l_persona_dia={c}"])
    for c in (50, 100, 150):
        for f in (0.25, 0.5):
            corre(f"consumo {c} L, f={f}", v, [f"consumo_l_persona_dia={c}", f"fraccion_suministro_en_racionamiento={f}"])
    for he in (36, 48):
        corre(f"horas efectivas {he}", v, [f"horas_efectivas_corte={he}"])
    df = pd.DataFrame(salida)
    df.to_csv(D / "zonas_siapa" / "motor_semana.csv", index=False)
    print("\n== Motor, semana 9 al 15 de noviembre de 2026 (personas-día sin agua) ==")
    print(df.to_string(index=False))


if __name__ == "__main__":
    m = cargar()
    cobertura(m)
    riesgo_por_zona(m)
    contraste(m)
    motor(m)
