#!/usr/bin/env python3
"""
Empata los nombres de colonia del calendario de tandeo del SIAPA contra la capa
oficial de colonias del IIEG, y de ahi contra las manzanas del censo.

El problema que resuelve: el calendario viene por nombre de colonia escrito a
mano ("Villas El Tapatio") y la capa trae otro ("Villas del Tapatio"). Sin este
puente, el calendario no se puede unir con el modelo.

Uso:
    python3 scripts/match_colonias.py nombres_del_calendario.txt
    python3 scripts/match_colonias.py --demo

Entrada: un nombre de colonia por linea.
Salida : CSV a stdout con  entrada, match, geocol, score, estado
         estado = exacto | probable | revisar | sin_match

Revisa a mano todo lo que salga como 'revisar' o 'sin_match'.
"""
import sys, csv, re, difflib, unicodedata, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
CAPA = BASE / "datos" / "colonias_tlaquepaque.csv"

def norm(s):
    s = unicodedata.normalize("NFKD", str(s).lower()).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    # ruido comun en los nombres de colonia
    s = re.sub(r"\b(col|colonia|fracc|fraccionamiento|barrio|unidad habitacional|infonavit)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def cargar():
    with open(CAPA, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def match(nombre, capa):
    n = norm(nombre)
    idx = {}
    for r in capa:
        idx.setdefault(norm(r["colonia"]), r)
    if n in idx:
        return idx[n], 1.0, "exacto"
    cand = difflib.get_close_matches(n, list(idx), n=1, cutoff=0.6)
    if not cand:
        return None, 0.0, "sin_match"
    score = difflib.SequenceMatcher(None, n, cand[0]).ratio()
    estado = "probable" if score >= 0.85 else "revisar"
    return idx[cand[0]], score, estado

def main():
    capa = cargar()
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        nombres = ["El Alamo", "Las Juntas", "Villas El Tapatio",
                   "Barrio de Santiago", "Tateposco", "San Pedrito",
                   "Colonia Que No Existe"]
    elif len(sys.argv) > 1:
        nombres = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    else:
        nombres = [l.strip() for l in sys.stdin if l.strip()]

    w = csv.writer(sys.stdout)
    w.writerow(["entrada", "match", "geocol", "pob", "manzanas", "score", "estado"])
    resumen = {}
    for nom in nombres:
        r, sc, est = match(nom, capa)
        resumen[est] = resumen.get(est, 0) + 1
        w.writerow([nom, r["colonia"] if r else "", r["geocol"] if r else "",
                    r["pob"] if r else "", r["manzanas"] if r else "",
                    round(sc, 2), est])
    print("", file=sys.stderr)
    for k in ("exacto", "probable", "revisar", "sin_match"):
        if k in resumen:
            print(f"  {k:10} {resumen[k]}", file=sys.stderr)

if __name__ == "__main__":
    main()
