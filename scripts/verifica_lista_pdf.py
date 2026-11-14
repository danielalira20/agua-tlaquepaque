#!/usr/bin/env python3
"""
Compara la lista de colonias que extrajo el equipo (lista_oficial_colonias.csv) contra la que sale del PDF
oficial (lista_oficial_pdf.csv). Termina con error si las colonias de Tlaquepaque no coinciden en nombre y zona.

    python3 scripts/verifica_lista_pdf.py
"""
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

Z = Path(__file__).resolve().parent.parent / "datos" / "zonas_siapa"


def norm(s):
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9 ]", "", s.upper().replace("*", "")).strip()


def tlaquepaque(df):
    d = df[df.municipio.str.contains("laquepaque", case=False)]
    return {(z, norm(n)) for z, n in zip(d.zona.astype(str), d.colonia)}


pdf = pd.read_csv(Z / "lista_oficial_pdf.csv", dtype=str)
equipo = pd.read_csv(Z / "lista_oficial_colonias.csv", dtype=str)
a, b = tlaquepaque(pdf), tlaquepaque(equipo)
print(f"Tlaquepaque: PDF {len(a)} | archivo del equipo {len(b)} | iguales {len(a & b)}")
dud = pdf[(pdf.nombre_dudoso == "1")]
print(f"nombres dudosos en el PDF (otros municipios, no se usan): {len(dud)}; de Tlaquepaque: "
      f"{int(dud.municipio.str.contains('laquepaque').sum())}")
if a != b:
    print("solo en el PDF:", sorted(a - b))
    print("solo en el archivo del equipo:", sorted(b - a))
    sys.exit(1)
print("OK: la lista del equipo coincide con el PDF oficial para Tlaquepaque")
