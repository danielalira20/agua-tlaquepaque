#!/usr/bin/env python3
"""
Compara el almacenamiento de agua de los cuatro municipios que cubre el calendario del SIAPA, con la MISMA medida
que usa el proyecto: viviendas sin tinaco ni cisterna, con cota minima y maxima calculadas POR MANZANA.

    python3 scripts/compara_municipios.py                 # baja el archivo de INEGI
    python3 scripts/compara_municipios.py --zip RUTA.zip  # usa uno ya descargado

Fuente: INEGI, Censo de Poblacion y Vivienda 2020, Principales resultados por AGEB y manzana urbana, Jalisco.
Salida: datos/comparacion_municipios.csv

Por que por manzana y no con los totales del municipio: el Censo no cruza tinaco con cisterna. Con los totales de
Tlaquepaque los tinacos mas las cisternas (195,044) superan a las viviendas (172,717), y la cota minima de viviendas
sin almacenamiento saldria 0. Por manzana las cotas son mucho mas estrechas.

Seleccion de manzanas: las que traen valor numerico en poblacion, viviendas, tinaco, cisterna y ocupantes, y mas de 0
viviendas. INEGI enmascara con '*' los valores de 1 o 2. Para Tlaquepaque este criterio da exactamente las 4,871
manzanas de datos/manzanas_tlaquepaque.csv. Se reporta que parte de la poblacion cubre en cada municipio.
Solo es la parte URBANA (manzanas); no incluye localidades rurales.
"""
import argparse
import io
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
URL = "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_14_cpv2020_csv.zip"
MUNICIPIOS = {"039": "Guadalajara", "098": "San Pedro Tlaquepaque", "101": "Tonalá", "120": "Zapopan"}
COLS = ["POBTOT", "TVIVHAB", "VPH_TINACO", "VPH_CISTER", "PROM_OCUP"]


def leer_censo(ruta_zip):
    if ruta_zip is None:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        datos = urllib.request.urlopen(req, timeout=300).read()
        zf = zipfile.ZipFile(io.BytesIO(datos))
    else:
        zf = zipfile.ZipFile(ruta_zip)
    nombre = next(n for n in zf.namelist() if n.endswith("conjunto_de_datos_ageb_urbana_14_cpv2020.csv"))
    with zf.open(nombre) as fh:
        return pd.read_csv(fh, dtype=str, encoding="latin-1", low_memory=False)


def comparar(d):
    num = lambda s: pd.to_numeric(s, errors="coerce")
    filas = []
    for mun, nombre in MUNICIPIOS.items():
        m = d[(d.MUN == mun) & (d.MZA != "000")].copy()
        for c in COLS:
            m[c] = num(m[c])
        pob_total = m.POBTOT.sum()
        ok = m.dropna(subset=COLS)
        ok = ok[ok.TVIVHAB > 0]
        v = ok.TVIVHAB
        t = ok.VPH_TINACO.clip(upper=v)
        c = ok.VPH_CISTER.clip(upper=v)
        smin = (v - t - c).clip(lower=0)            # todos los que tienen ambos son los que traslapan al maximo
        smax = v - pd.concat([t, c], axis=1).max(axis=1)  # tinaco y cisterna en viviendas distintas, al maximo
        filas.append({
            "municipio": nombre, "manzanas": len(ok), "poblacion": int(ok.POBTOT.sum()),
            "cobertura_poblacion_pct": round(100 * ok.POBTOT.sum() / pob_total, 1), "viviendas": int(v.sum()),
            "sin_almacen_min": int(smin.sum()), "sin_almacen_max": int(smax.sum()),
            "pct_sin_almacen_min": round(100 * smin.sum() / v.sum(), 1), "pct_sin_almacen_max": round(100 * smax.sum() / v.sum(), 1),
            "pct_con_tinaco": round(100 * t.sum() / v.sum(), 1), "pct_con_cisterna": round(100 * c.sum() / v.sum(), 1),
            "personas_en_manzanas_con_mayoria_sin_almacen_min": int(ok.POBTOT[(smin / v) > 0.5].sum()),
            "personas_en_manzanas_con_mayoria_sin_almacen_max": int(ok.POBTOT[(smax / v) > 0.5].sum())})
    return pd.DataFrame(filas)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--zip", help="archivo de INEGI ya descargado")
    a = p.parse_args(argv)
    df = comparar(leer_censo(a.zip))
    df.to_csv(RAIZ / "datos" / "comparacion_municipios.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
