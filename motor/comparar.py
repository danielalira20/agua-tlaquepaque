#!/usr/bin/env python3
"""
Compara dos salidas del motor (referencia contra oficial), renglón por renglón.

    python3 motor/comparar.py salidas/referencia.csv salidas/oficial.csv [--tol 0.05]

Empareja por (cvegeo, fecha). Los conteos de viviendas y las horas deben coincidir
EXACTAMENTE; los porcentajes, personas y severidad, con tolerancia.
Termina con código 1 si hay diferencias, para poder usarlo en una prueba.
"""
import argparse
import csv
import sys

EXACTAS = ["viv_sin_agua_min", "viv_sin_agua_max", "viv_agua_guardada_min", "viv_agua_guardada_max",
           "horas_sin_servicio_min", "horas_sin_servicio_max", "estado", "requiere_desinfeccion"]
TOLERANCIA = ["pct_sin_agua_min", "pct_sin_agua_max", "personas_sin_agua_min", "personas_sin_agua_max", "severidad"]


def leer(ruta):
    with open(ruta, newline="", encoding="utf-8") as fh:
        return {(r["cvegeo"], r["fecha"]): r for r in csv.DictReader(fh)}


def norm(col, v):
    v = (v or "").strip()
    if col == "requiere_desinfeccion":
        return v.lower() in ("true", "1", "si")
    if col == "estado":
        return v
    return float(v) if v != "" else float("nan")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--tol", type=float, default=0.05)
    p.add_argument("--mostrar", type=int, default=10)
    x = p.parse_args(argv)
    A, B = leer(x.a), leer(x.b)
    solo_a, solo_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))
    comunes = sorted(set(A) & set(B))
    difs = []
    por_col = {}
    for k in comunes:
        for col in EXACTAS + TOLERANCIA:
            if col not in A[k] or col not in B[k]:
                continue
            va, vb = norm(col, A[k][col]), norm(col, B[k][col])
            if col in EXACTAS:
                malo = va != vb
            else:
                malo = abs(va - vb) > x.tol
            if malo:
                difs.append((k, col, va, vb))
                por_col[col] = por_col.get(col, 0) + 1
    print(f"renglones en A: {len(A)} | en B: {len(B)} | comunes: {len(comunes)}")
    print(f"solo en A: {len(solo_a)} | solo en B: {len(solo_b)}")
    print(f"diferencias: {len(difs)} en {len({d[0] for d in difs})} renglones")
    for col, n in sorted(por_col.items(), key=lambda t: -t[1]):
        print(f"   {col}: {n}")
    for k, col, va, vb in difs[: x.mostrar]:
        print(f"   {k[0]} {k[1]} {col}: A={va} B={vb}")
    ok = not difs and not solo_a and not solo_b
    print("COINCIDEN" if ok else "NO COINCIDEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
