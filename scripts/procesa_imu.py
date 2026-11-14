#!/usr/bin/env python3
"""
Procesa el índice de marginación urbana a nivel AGEB (CONAPO, 2020) para Tlaquepaque y lo cruza con las
manzanas, el riesgo de almacenamiento y las zonas del SIAPA.

    python3 scripts/procesa_imu.py

Entrada:  datos/raw/IMU_2020.zip   (se baja a mano: ver datos/raw/LEEME.md)
Salidas:  datos/marginacion_ageb_tlaquepaque.csv   una fila por AGEB de Tlaquepaque
          datos/marginacion_vs_riesgo.csv          riesgo por grado de marginación

Llave: CVE_AGEB (13 caracteres) = los primeros 13 de cada cvegeo de manzana. No se empatan nombres.

Orientación del índice: IM_2020 MÁS ALTO = MENOS marginación (el grado "Muy bajo" promedia 124.9 y el
"Muy alto" 110.7). Se usa siempre el grado GM_2020 y no el signo del índice.
"""
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / "datos"
ORDEN = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo"]
NUM = ["POB_TOTAL", "P6A14NAE", "SBASC", "PSDSS", "OVSDE", "OVSEE", "OVSAE", "OVPT", "OVSREF", "OVSINT",
       "OVSCEL", "OVHAC", "IM_2020", "IMN_2020"]


def lee_imu():
    zip_ = D / "raw" / "IMU_2020.zip"
    if not zip_.exists():
        sys.exit(f"falta {zip_}: ver datos/raw/LEEME.md")
    with zipfile.ZipFile(zip_) as z:
        xls = next(n for n in z.namelist() if n.lower().endswith(".xls"))
        datos = z.read(xls)
    df = pd.read_excel(io.BytesIO(datos), sheet_name="IMU_2020", dtype=str)
    t = df[(df.ENT == "14") & (df.MUN == "098")].copy()
    for c in NUM:
        t[c] = pd.to_numeric(t[c], errors="coerce")
    return t


def main():
    t = lee_imu()
    cols = ["CVE_AGEB", "NOM_LOC", "AGEB"] + NUM + ["GM_2020"]
    t[cols].sort_values("CVE_AGEB").to_csv(D / "marginacion_ageb_tlaquepaque.csv", index=False)
    print(f"AGEB de Tlaquepaque: {len(t)}, población {int(t.POB_TOTAL.sum()):,}")

    m = pd.read_csv(D / "manzanas_tlaquepaque.csv", dtype={"cvegeo": str})
    m["CVE_AGEB"] = m.cvegeo.str[:13]
    z = pd.read_csv(D / "zonas_siapa" / "manzana_zona.csv", dtype=str, keep_default_na=False)[["cvegeo", "zona"]]
    m = m.merge(z, on="cvegeo", how="left").fillna({"zona": ""})
    j = m.merge(t[["CVE_AGEB", "GM_2020"]], on="CVE_AGEB", how="left")
    sin = j[j.GM_2020.isna()]
    print(f"manzanas sin AGEB en el IMU: {len(sin)} ({int(sin.pob.sum()):,} personas); "
          f"AGEB del IMU sin manzanas: {len(set(t.CVE_AGEB) - set(m.CVE_AGEB))}")
    j["GM_2020"] = j.GM_2020.fillna("sin dato")
    j["en_programa"] = j.zona != ""

    def resumen(df, nombre):
        g = df.groupby("GM_2020").agg(manzanas=("cvegeo", "size"), pob=("pob", "sum"), viviendas=("viviendas", "sum"),
                                      viv_tinaco=("viv_tinaco", "sum"), viv_cisterna=("viv_cisterna", "sum"),
                                      sin_almacen_min=("sin_almacen_min", "sum"),
                                      sin_almacen_max=("sin_almacen_max", "sum"))
        g = g.reindex([x for x in ORDEN + ["sin dato"] if x in g.index])
        g["pct_pob"] = (100 * g.pob / g.pob.sum()).round(1)
        g["pct_sin_almacen_min"] = (100 * g.sin_almacen_min / g.viviendas).round(1)
        g["pct_del_riesgo_min"] = (100 * g.sin_almacen_min / g.sin_almacen_min.sum()).round(1)
        g["pct_con_tinaco"] = (100 * g.viv_tinaco / g.viviendas).round(1)
        g["pct_con_cisterna"] = (100 * g.viv_cisterna / g.viviendas).round(1)
        g.insert(0, "base", nombre)
        return g.reset_index()

    out = pd.concat([resumen(j, "todo Tlaquepaque"), resumen(j[j.en_programa], "dentro del programa")])
    out.to_csv(D / "marginacion_vs_riesgo.csv", index=False)
    print(out.to_string(index=False))
    v = j[j.viviendas > 0].assign(p=lambda d: d.sin_almacen_min / d.viviendas)
    v = v.merge(t[["CVE_AGEB", "IM_2020"]], on="CVE_AGEB")
    print(f"\ncorrelación entre IM_2020 y % sin almacenamiento por manzana: {v[['IM_2020', 'p']].corr().iloc[0, 1]:.3f} "
          "(positiva = a menos marginación, más manzanas sin almacenamiento)")


if __name__ == "__main__":
    main()
