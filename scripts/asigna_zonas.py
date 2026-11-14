#!/usr/bin/env python3
"""
Asigna a cada manzana de Tlaquepaque su(s) zona(s) de racionamiento del SIAPA,
dejando claro de qué fuente salió y qué tan firme es.

FUENTES (datos/zonas_siapa/)
  portal_rotacion.topo.json     Polígonos del portal oficial del SIAPA. Cada colonia trae una
                                zona `z` que el portal calcula cruzando su polígono con el
                                mapa de zonas ("el cruce original del mapa"). Da geometría.
  lista_oficial_colonias.csv    Colonias por zona, extraídas del documento oficial del SIAPA.
                                Da el nombre, pero no la geometría.
  equivalencias_nombres.csv     Emparejamientos de nombres revisados A MANO, con su motivo.

REGLA, por polígono del portal
  1. Contraparte en la lista: nombre exacto (sin acentos ni puntuación) y municipio de la lista
     dentro de la etiqueta del polígono (el portal pone "Tlaquepaque y Tonalá" cuando una colonia
     cruza el límite). Si no, la tabla de equivalencias revisada a mano.
     NO se aceptan parecidos automáticos: existen colonias distintas con el mismo nombre
     (El Mirador de Tlaquepaque y El Mirador de Guadalajara) y otras casi iguales que no lo son.
  2. Con contraparte:
       portal sin zona          -> zona de la lista                    confianza media
       zonas idénticas/solapan  -> intersección de las dos             confianza alta
       sin zona en común        -> las DOS zonas, como rango, y se marca  CONFLICTO
                                   (no sabemos cuál fuente tiene razón; el motor trata las
                                   manzanas con varias zonas ensanchando el intervalo)
  3. Sin contraparte: la zona del portal, tal cual                      confianza baja
  4. Sin zona en ninguna fuente: fuera del programa                     confianza ninguna

Por manzana: se toma el polígono que contiene su centroide. Si hay dos o más, se toma la unión de
sus zonas y se marca `ambiguo`.

Uso:   python3 scripts/asigna_zonas.py
Requiere: pandas, geopandas, pyogrio (ver scripts/requirements.txt)
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ZS = RAIZ / "datos" / "zonas_siapa"
TQ = "San Pedro Tlaquepaque"


def norm(s):
    s = unicodedata.normalize("NFKD", str(s).lower()).encode("ascii", "ignore").decode()
    s = s.replace("*", " ").replace("/", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def municipios(etiqueta):
    return [m.strip() for m in re.split(r"\s+y\s+", str(etiqueta)) if m.strip()]


def zset(texto):
    return {z.strip() for z in str(texto or "").split(",") if z.strip()}


def zjoin(s):
    return ",".join(sorted(s, key=int))


def cargar_lista():
    off = pd.read_csv(ZS / "lista_oficial_colonias.csv", dtype=str)
    off["k"] = off.colonia_original.map(norm)
    por_clave = {}
    for r in off.itertuples():
        por_clave.setdefault((r.k, r.municipio), set()).add(r.zona)
    return off, por_clave


def cargar_equivalencias():
    eq = {}
    with open(ZS / "equivalencias_nombres.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            eq.setdefault(norm(r["nombre_portal"]), []).append((norm(r["nombre_lista"]), r["municipio_lista"], r["nombre_lista"]))
    return eq


def contraparte(poligono_k, munis_poligono, por_clave, equivalencias):
    """Devuelve (zonas_lista, tipo, nombre_lista) o (None, '', '')."""
    zonas, nombres = set(), []
    for m in munis_poligono:
        if (poligono_k, m) in por_clave:
            zonas |= por_clave[(poligono_k, m)]
            nombres.append(f"{poligono_k} ({m})")
    if zonas:
        return zonas, "exacto", "; ".join(nombres)
    if TQ in munis_poligono and poligono_k in equivalencias:
        for k, m, crudo in equivalencias[poligono_k]:
            if (k, m) in por_clave:
                zonas |= por_clave[(k, m)]
                nombres.append(crudo)
        if zonas:
            return zonas, "manual", "; ".join(nombres)
    return None, "", ""


def resolver_poligono(zp, zo):
    """Devuelve (zona_final, fuente, confianza, conflicto)."""
    if zo is None:
        return (zp, "portal_sin_lista", "baja", False) if zp else (set(), "ninguna", "ninguna", False)
    if not zp:
        return zo, "lista", "media", False
    inter = zp & zo
    if inter:
        return inter, "portal+lista", "alta", False
    return zp | zo, "lista_contra_portal", "conflicto", True


def main():
    off, por_clave = cargar_lista()
    equivalencias = cargar_equivalencias()
    col = gpd.read_file(ZS / "portal_rotacion.topo.json", layer="colonias").set_crs(4326, allow_override=True)
    col["pid"] = range(len(col))
    col["k"] = col.n.map(norm)
    col["z"] = col.z.fillna("").astype(str)

    cen = pd.read_csv(RAIZ / "datos" / "manzanas_centroides.csv", dtype={"cvegeo": str})
    pts = gpd.GeoDataFrame(cen, geometry=gpd.points_from_xy(cen.lon, cen.lat), crs=4326)
    j = gpd.sjoin(pts, col[["pid", "n", "m", "z", "k", "geometry"]], how="left", predicate="within")

    # resolución por polígono (una sola vez)
    res = {}
    usadas = set()
    for p in col[col.pid.isin(j.pid.dropna().astype(int).unique())].itertuples():
        mp = municipios(p.m)
        zo, tipo, nombre_lista = contraparte(p.k, mp, por_clave, equivalencias)
        zp = zset(p.z)
        zf, fuente, conf, confl = resolver_poligono(zp, zo)
        res[p.pid] = dict(poligono=p.n, municipio_poligono=p.m, zona_portal=zjoin(zp), zona_lista=zjoin(zo) if zo else "",
                          nombre_lista=nombre_lista, tipo_cruce=tipo, zf=zf, fuente=fuente, confianza=conf, conflicto=confl)
        if tipo == "manual":
            usadas.add(p.k)

    filas = []
    for cve, g in j.groupby("cvegeo", sort=True):
        base = g.iloc[0]
        pids = [int(x) for x in g.pid.dropna().unique()]
        d = dict(cvegeo=cve, pob=int(base.pob), viviendas=int(float(base.viviendas)),
                 sin_almacen_min=int(float(base.sin_almacen_min)), sin_almacen_max=int(float(base.sin_almacen_max)))
        if not pids:
            d.update(zona="", fuente="sin_poligono", confianza="sin_poligono", poligono_portal="", zona_portal="",
                     nombre_lista="", zona_lista="", tipo_cruce="", conflicto=False, ambiguo=False)
        else:
            rs = [res[p] for p in pids]
            zf = set().union(*[r["zf"] for r in rs])
            ambiguo = len(rs) > 1
            orden = ["conflicto", "baja", "media", "alta", "ninguna"]
            conf = rs[0]["confianza"] if not ambiguo else "ambiguo"
            if ambiguo and len({zjoin(r["zf"]) for r in rs}) == 1:
                conf = min((r["confianza"] for r in rs), key=orden.index)   # todos dan lo mismo: la menos firme
            d.update(zona=zjoin(zf), fuente=rs[0]["fuente"] if not ambiguo else "varios_poligonos", confianza=conf,
                     poligono_portal=" | ".join(r["poligono"] for r in rs), zona_portal=" | ".join(r["zona_portal"] for r in rs),
                     nombre_lista=" | ".join(r["nombre_lista"] for r in rs), zona_lista=" | ".join(r["zona_lista"] for r in rs),
                     tipo_cruce=",".join(sorted({r["tipo_cruce"] for r in rs if r["tipo_cruce"]})),
                     conflicto=any(r["conflicto"] for r in rs), ambiguo=ambiguo)
        filas.append(d)

    cols = ["cvegeo", "zona", "fuente", "confianza", "conflicto", "ambiguo", "poligono_portal", "zona_portal",
            "nombre_lista", "zona_lista", "tipo_cruce", "pob", "viviendas", "sin_almacen_min", "sin_almacen_max"]
    out = pd.DataFrame(filas)[cols]
    out.to_csv(ZS / "manzana_zona.csv", index=False)

    # pendientes de revision contra el PDF original
    por_nombre = {}
    for r in off.itertuples():
        por_nombre.setdefault(r.k, []).append((r.colonia_original, r.municipio, r.zona))
    cache = out.set_index("cvegeo")
    manz_por_pid = {}
    for cve, g in j.groupby("cvegeo", sort=True):
        for pid in {int(x) for x in g.pid.dropna().unique()}:
            manz_por_pid.setdefault(pid, []).append(cve)
    pend = []
    for pid, r in res.items():
        if r["tipo_cruce"]:
            continue
        k = norm(r["poligono"])
        homs = [h for h in por_nombre.get(k, [])]
        if r["zona_portal"]:
            tipo = "portal_sin_lista_con_homonimo" if homs else "portal_sin_lista"
        else:
            if not homs:
                continue
            tipo = "sin_zona_con_homonimo"
        sub = cache.loc[manz_por_pid[pid]]
        pend.append(dict(tipo=tipo, poligono=r["poligono"], municipio_poligono=r["municipio_poligono"],
                         zona_portal=r["zona_portal"],
                         homonimos_en_lista="; ".join(f"{a} ({m}, zona {z})" for a, m, z in homs),
                         manzanas=len(sub), personas=int(sub.pob.sum()), viv_sin_almacen_min=int(sub.sin_almacen_min.sum())))
    pd.DataFrame(pend).sort_values("personas", ascending=False).to_csv(ZS / "pendientes_revision.csv", index=False)

    # resumen por zona y confianza
    def clase(z):
        return z if z else "fuera del programa"
    r = out.assign(grupo=out.zona.map(clase)).groupby(["grupo", "confianza"]).agg(
        manzanas=("cvegeo", "size"), personas=("pob", "sum"), viviendas=("viviendas", "sum"),
        sin_almacen_min=("sin_almacen_min", "sum"), sin_almacen_max=("sin_almacen_max", "sum")).reset_index()
    r.to_csv(ZS / "resumen_zonas.csv", index=False)

    redundantes = []
    with open(ZS / "equivalencias_nombres.csv", newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            if norm(fila["nombre_portal"]) not in usadas:
                redundantes.append(fila["nombre_portal"])
    print(f"manzanas: {len(out)} | personas: {int(out.pob.sum()):,}")
    print("equivalencias manuales sin efecto (ya resueltas por nombre exacto o sin polígono):", sorted(set(redundantes)) or "ninguna")
    return 0


if __name__ == "__main__":
    sys.exit(main())
