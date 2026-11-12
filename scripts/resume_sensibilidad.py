#!/usr/bin/env python3
"""
Genera datos/sensibilidad/RESUMEN.md: todas las tablas del analisis de sensibilidad, calculadas desde los CSV de
scripts/sensibilidad_orden.py. El documento que interpreta los resultados (datos/HALLAZGOS_sensibilidad.md) cita estas tablas.

    python3 scripts/resume_sensibilidad.py

Ademas de resumir, calcula la "autonomia del tinaco en dias":  tinaco_l / (ocupantes * consumo * (1 - f))  con la mediana de
ocupantes del Censo (3.77). Es el numero que decide si una vivienda con tinaco aguanta una racha de racionamiento: lo que cuenta
en el motor es la combinacion de los tres supuestos, no cada uno por separado.
"""
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / "datos" / "sensibilidad"
sys.path.insert(0, str(RAIZ / "scripts"))
import exporta_app as X  # noqa: E402

OCUPANTES_MEDIANA = statistics.median(m["ocupantes_prom"] for m in X.cargar_manzanas())


def md(df, formatos=None):
    formatos = formatos or {}
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---:" if pd.api.types.is_numeric_dtype(df[c]) else "---" for c in cols) + "|"]
    for _, r in df.iterrows():
        celdas = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)) and v != v:
                celdas.append("")
            elif c in formatos:
                celdas.append(formatos[c].format(v))
            elif isinstance(v, (float, np.floating)):
                celdas.append(f"{v:,.3f}".rstrip("0").rstrip(".") if abs(v) < 1000 else f"{v:,.0f}")
            elif isinstance(v, (bool, np.bool_)):
                celdas.append("sí" if v else "no")
            else:
                celdas.append(str(v))
        out.append("| " + " | ".join(celdas) + " |")
    return "\n".join(out)


def autonomia_dias(tinaco, consumo, f):
    return tinaco / (OCUPANTES_MEDIANA * consumo * (1 - f))


def resumen_mc(d, nombre):
    def fila(etq, s, fmt="{:.3f}"):
        return {"métrica": etq, "media": fmt.format(s.mean()), "p5": fmt.format(s.quantile(.05)), "mediana": fmt.format(s.median()),
                "p95": fmt.format(s.quantile(.95)), "mínimo": fmt.format(s.min())}
    filas = [fila("rho (orden, manzanas con riesgo)", d.rho_positivos_min), fila("solape del top-250", d.solape_top250),
             fila("cobertura del riesgo, top-100 del base", d.cobertura_top100), fila("cobertura del riesgo, top-250 del base", d.cobertura_top250),
             fila("solape del top-10 de colonias", d.solape_top10_colonias), fila("parte del riesgo en zonas 5 y 6 (%)", d.parte_zonas_5_6_pct, "{:.1f}"),
             fila("parte del riesgo en AGEB Muy bajo (%)", d.parte_muy_bajo_pct, "{:.1f}"), fila("cobertura del núcleo robusto", d.cobertura_nucleo)]
    p = d[d.prio_veces_baseline_min.notna()]
    if len(p):
        filas += [fila(f"priorizador: veces el baseline (n={len(p)})", p.prio_veces_baseline_min, "{:.2f}"),
                  fila("priorizador: solape de manzanas atendidas", p.solape_manzanas_atendidas)]
    return f"### Familia {nombre} ({len(d)} sorteos)\n\n" + md(pd.DataFrame(filas))


def main():
    e = pd.read_csv(D / "escenarios.csv")
    f = pd.read_csv(D / "barrido_fino.csv")
    mc = pd.read_csv(D / "montecarlo.csv")
    imp = pd.read_csv(D / "importancia.csv")
    rob = pd.read_csv(D / "manzanas_robustas.csv", dtype={"cvegeo": str})
    out = ["# Resumen de la sensibilidad (generado)", "",
           "**Generado por `scripts/resume_sensibilidad.py` a partir de `scripts/sensibilidad_orden.py`. No se edita a mano.** "
           "La interpretación está en `../HALLAZGOS_sensibilidad.md`.", "",
           f"Ocupantes por vivienda (mediana del Censo): {OCUPANTES_MEDIANA:.2f}.", ""]

    cols = {"escenario": "escenario", "procedencia_del_rango": "rango", "viv_dia_min": "viv-día sin agua (mín)", "rho_positivos_min": "rho",
            "solape_top250": "solape top-250", "cobertura_top250": "cobertura top-250", "solape_top10_colonias": "solape top-10 colonias",
            "lugar_el_sauz": "lugar El Sauz", "parte_zonas_5_6_pct": "zonas 5-6 (%)", "parte_muy_bajo_pct": "Muy bajo (%)",
            "grado_mayor_riesgo": "grado mayor", "prio_veces_baseline_min": "priorizado ÷ baseline", "solape_manzanas_atendidas": "solape atendidas",
            "orden_estable": "orden estable", "conclusion_b_estable": "concl. B estable"}
    t = e[list(cols)].rename(columns=cols)
    out += ["## 1. Escenarios (un supuesto a la vez, esquinas, calendario, zonas)", "",
            "`rango`: `decision` = del equipo; `literatura` = de una referencia; `sin_fuente` = ilustrativo, sin fuente en el repo; `censo` = incertidumbre propia del Censo.", "",
            md(t, {"viv-día sin agua (mín)": "{:,.0f}", "rho": "{:.3f}", "solape top-250": "{:.3f}", "cobertura top-250": "{:.3f}",
                   "zonas 5-6 (%)": "{:.1f}", "Muy bajo (%)": "{:.1f}", "priorizado ÷ baseline": "{:.2f}", "solape atendidas": "{:.3f}"}), ""]

    out += ["## 2. Barrido fino: dónde cambia el orden", "",
            md(f[["parametro", "valor", "viv_dia_min", "rho_positivos_min", "solape_top250", "cobertura_top250", "parte_zonas_5_6_pct", "parte_muy_bajo_pct", "lugar_el_sauz"]]
               .rename(columns={"viv_dia_min": "viv-día sin agua (mín)", "rho_positivos_min": "rho", "solape_top250": "solape top-250", "cobertura_top250": "cobertura top-250",
                                "parte_zonas_5_6_pct": "zonas 5-6 (%)", "parte_muy_bajo_pct": "Muy bajo (%)", "lugar_el_sauz": "lugar El Sauz"}),
               {"viv-día sin agua (mín)": "{:,.0f}", "rho": "{:.3f}", "solape top-250": "{:.3f}", "cobertura top-250": "{:.3f}", "zonas 5-6 (%)": "{:.1f}", "Muy bajo (%)": "{:.1f}"}), ""]

    out += ["## 3. Monte Carlo", "",
            "Familia A: consumo 50 a 100 L, tinaco 750 a 1,100 L y U de 24 a 72 h (los rangos de la decisión 1). Familia B: además cisterna 2,500 a 10,000 L, "
            "horas efectivas 24 a 48 y fracción `f` de 0 a 0.5. Sorteos uniformes con semilla fija.", ""]
    for fam in ("A", "B"):
        d = mc[mc.familia == fam]
        out += [resumen_mc(d, fam), "",
                f"- Criterio de orden estable cumplido en **{100 * d.orden_estable.mean():.1f}%** de los sorteos; conclusión B estable en **{100 * d.conclusion_b_estable.mean():.1f}%**.",
                f"- Lugar de El Sauz: {d.lugar_el_sauz.value_counts().sort_index().to_dict()}.",
                f"- Grado con mayor parte del riesgo: {d.grado_mayor_riesgo.value_counts().to_dict()}.", ""]

    out += ["## 4. Qué supuesto mueve más el orden", "",
            "Correlación de rangos (Spearman) entre cada parámetro y cada resultado, sobre los sorteos de Monte Carlo. Con consumo y fracción `f` el signo es "
            "opuesto porque lo que cuenta es el consumo neto `c × (1 − f)`.", "",
            md(imp.rename(columns={"spearman_con_rho_orden": "con rho", "spearman_con_cobertura_top250": "con cobertura top-250", "spearman_con_parte_zonas_5_6": "con zonas 5-6",
                                   "spearman_con_parte_muy_bajo": "con Muy bajo", "spearman_con_viv_dia_min": "con viv-día", "spearman_con_solape_manzanas_atendidas": "con solape atendidas"}),
               {"rango_bajo": "{:g}", "rango_alto": "{:g}"}), ""]

    # autonomia del tinaco
    m = mc.copy()
    for c, v in (("p_tinaco_l", 1100), ("p_consumo_l_persona_dia", 50), ("p_fraccion_suministro_en_racionamiento", 0.0)):
        m[c] = m[c].fillna(v)
    m["autonomia_dias"] = autonomia_dias(m.p_tinaco_l, m.p_consumo_l_persona_dia, m.p_fraccion_suministro_en_racionamiento)
    bins = [0, 2, 3, 4, 5, 6, 100]
    etiquetas = ["menos de 2", "2 a 3", "3 a 4", "4 a 5", "5 a 6", "6 o más"]
    m["tramo"] = pd.cut(m.autonomia_dias, bins=bins, labels=etiquetas, right=False)
    g = m.groupby("tramo", observed=True).agg(sorteos=("rho_positivos_min", "size"), rho_medio=("rho_positivos_min", "mean"), cobertura_top250=("cobertura_top250", "mean"),
                                              zonas_5_6=("parte_zonas_5_6_pct", "mean"), muy_bajo=("parte_muy_bajo_pct", "mean")).reset_index()
    out += ["## 5. La autonomía del tinaco, en días", "",
            f"`tinaco / (ocupantes × consumo × (1 − f))` con {OCUPANTES_MEDIANA:.2f} ocupantes. La racha de racionamiento más larga del calendario vigente es de 4 días "
            "(zonas 4 y 5), y de 3 en las zonas 3 y 6. Sobre los 600 sorteos de Monte Carlo:", "",
            md(g.rename(columns={"tramo": "autonomía del tinaco (días)", "rho_medio": "rho medio", "cobertura_top250": "cobertura top-250", "zonas_5_6": "zonas 5-6 (%)", "muy_bajo": "Muy bajo (%)"}),
               {"rho medio": "{:.3f}", "cobertura top-250": "{:.3f}", "zonas 5-6 (%)": "{:.1f}", "Muy bajo (%)": "{:.1f}"}), "",
            f"Caso base: {autonomia_dias(1100, 50, 0):.1f} días. Consumo 100 L: {autonomia_dias(1100, 100, 0):.1f} días. Consumo 100 L y tinaco de 750 L: {autonomia_dias(750, 100, 0):.1f} días.", ""]

    # nucleo robusto
    nuc = rob[rob.nucleo_robusto]
    tot_base = rob.viv_dia_min_base.sum()
    out += ["## 6. El núcleo robusto", "",
            f"Manzanas que quedan entre las 250 de mayor riesgo en al menos el 90% de los sorteos de la familia A: **{len(nuc)}**. Concentran {nuc.viv_dia_min_base.sum():,.0f} viviendas-día "
            f"sin agua del caso base (de {rob.viv_dia_min_base.sum():,.0f} en las {len(rob)} manzanas que aparecen en algún top-250). "
            f"{int(nuc.en_top250_base.sum())} de ellas están en el top-250 del caso base.", "",
            "Por zona y por grado de marginación:", "",
            md(nuc.groupby("zona").agg(manzanas=("cvegeo", "size"), viv_dia_min_base=("viv_dia_min_base", "sum")).reset_index().sort_values("manzanas", ascending=False)
               .rename(columns={"viv_dia_min_base": "viv-día base"}), {"viv-día base": "{:,.0f}"}), "",
            md(nuc.groupby("grado_marginacion").agg(manzanas=("cvegeo", "size"), viv_dia_min_base=("viv_dia_min_base", "sum")).reset_index().sort_values("manzanas", ascending=False)
               .rename(columns={"viv_dia_min_base": "viv-día base"}), {"viv-día base": "{:,.0f}"}), "",
            "Las diez colonias con más manzanas en el núcleo:", "",
            md(nuc[nuc.colonia != ""].groupby("colonia").agg(manzanas=("cvegeo", "size"), viv_dia_min_base=("viv_dia_min_base", "sum")).reset_index()
               .sort_values(["manzanas", "viv_dia_min_base"], ascending=False).head(10).rename(columns={"viv_dia_min_base": "viv-día base"}), {"viv-día base": "{:,.0f}"}), ""]
    (D / "RESUMEN.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{D / 'RESUMEN.md'}: {len(out)} bloques")


if __name__ == "__main__":
    main()
