#!/usr/bin/env python3
"""
Implementación de REFERENCIA del motor de autonomía.

Sigue motor/ESPECIFICACION.md y nada más. Existe para comparar contra la
implementación oficial (TypeScript, en la app): si las dos coinciden, se atrapan
errores de programación. No atrapa supuestos equivocados.

Solo usa la biblioteca estándar.

Uso:
    python3 motor/referencia.py \\
        --manzanas datos/manzanas_tlaquepaque.csv \\
        --zonas    fixtures/zonas.fixture.csv \\
        --calendario motor/calendarios/vigente-2026-11-03.json \\
        --desde 2026-11-09 --hasta 2026-11-15 \\
        --salida salidas/referencia.csv

Sensibilidad (cambia un supuesto sin tocar el archivo):
    ... --set consumo_l_persona_dia=100 --set horas_efectivas_corte=36
"""
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]  # weekday(): 0 = lunes

COLUMNAS = [
    "cvegeo", "fecha", "dia", "zona",
    "horas_sin_servicio_min", "horas_sin_servicio_max",
    "viv_sin_agua_min", "viv_sin_agua_max",
    "pct_sin_agua_min", "pct_sin_agua_max",
    "personas_sin_agua_min", "personas_sin_agua_max",
    "viv_agua_guardada_min", "viv_agua_guardada_max",
    "requiere_desinfeccion", "estado", "severidad",
]


def leer_json(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def dia_semana(fecha):
    return DIAS[fecha.weekday()]


def horas_sin_servicio(dias_zona, fecha, horas_efectivas):
    """Sección 4. Horas acumuladas de racionamiento al final de `fecha`."""
    n = 0
    f = fecha
    while dia_semana(f) in dias_zona:
        n += 1
        f -= dt.timedelta(days=1)
        if n > 7:
            raise ValueError("zona con racionamiento los 7 dias: no soportada")
    return 0 if n == 0 else horas_efectivas + (n - 1) * 24


def autonomia_h(litros, ocupantes, consumo):
    """Sección 5. Horas que aguanta un estrato con `litros` almacenados."""
    if litros <= 0:
        return 0.0
    if ocupantes <= 0 or consumo <= 0:
        raise ValueError("ocupantes y consumo deben ser positivos")
    return litros / (ocupantes * consumo) * 24


def rango_ambos(V, T, C):
    """Sección 3. Intervalo de viviendas con tinaco Y cisterna."""
    T = min(T, V)
    C = min(C, V)
    return T, C, max(0, T + C - V), min(T, C)


def evaluar(V, T, C, ocupantes, H, sup):
    """
    Secciones 3, 5 y 6 para UNA sola H. Devuelve [(sin_agua, agua_guardada), ...],
    uno por cada extremo de `a` (a_min y a_max). Para un mismo `a` siempre se cumple
    sin_agua + agua_guardada <= V.
    """
    lt, lc = sup["tinaco_l"], sup["cisterna_l"]
    c, U = sup["consumo_l_persona_dia"], sup["u_horas_agua_guardada"]
    aut = {
        "ambos": autonomia_h(lt + lc, ocupantes, c),
        "solo_t": autonomia_h(lt, ocupantes, c),
        "solo_c": autonomia_h(lc, ocupantes, c),
        "ninguno": 0.0,
    }
    T, C, a_min, a_max = rango_ambos(V, T, C)
    pares = []
    for a in (a_min, a_max):
        estratos = {"ambos": a, "solo_t": T - a, "solo_c": C - a, "ninguno": V - T - C + a}
        sin = sum(n for k, n in estratos.items() if aut[k] < H)
        guard = sum(n for k, n in estratos.items() if k != "ninguno" and aut[k] >= H and H > U)
        pares.append((sin, guard))
    return pares


def calcular_manzana(V, T, C, ocupantes, horas, sup):
    """
    `horas` es la lista de H(d), una por zona de la manzana (una sola [0.0] si esta
    fuera del programa). Devuelve (sin_min, sin_max, guardada_min, guardada_max).
    """
    pares = [p for H in horas for p in evaluar(V, T, C, ocupantes, H, sup)]
    sin = [p[0] for p in pares]
    guard = [p[1] for p in pares]
    return min(sin), max(sin), min(guard), max(guard)


def clasificar(pct_min, sup):
    """Sección 7. Se decide con el porcentaje SIN redondear."""
    if pct_min < sup["umbral_estado_parcial_pct"]:
        return "con_agua"
    if pct_min <= sup["umbral_estado_mayoritario_pct"]:
        return "quiebre_parcial"
    return "quiebre_mayoritario"


def parsear_zonas(texto):
    return [z.strip() for z in str(texto or "").split(",") if z.strip()]


def horas_de_zonas(zonas, esquema, fecha, horas_efectivas):
    if not zonas:
        return [0.0]
    horas = []
    for z in zonas:
        if z not in esquema:
            raise ValueError(f"zona {z!r} no esta en el calendario")
        horas.append(float(horas_sin_servicio(set(esquema[z]), fecha, horas_efectivas)))
    return horas


def procesar(manzanas, zonas_por_cve, esquema, fechas, sup):
    for m in manzanas:
        V = int(round(float(m["viviendas"])))
        if V <= 0:
            continue
        T = int(round(float(m["viv_tinaco"] or 0)))
        C = int(round(float(m["viv_cisterna"] or 0)))
        o = float(m["ocupantes_prom"])
        zona_txt = zonas_por_cve.get(m["cvegeo"], "")
        zonas = parsear_zonas(zona_txt)
        for f in fechas:
            horas = horas_de_zonas(zonas, esquema, f, sup["horas_efectivas_corte"])
            smin, smax, gmin, gmax = calcular_manzana(V, T, C, o, horas, sup)
            pmin = 100 * smin / V
            yield {
                "cvegeo": m["cvegeo"], "fecha": f.isoformat(), "dia": dia_semana(f), "zona": zona_txt,
                "horas_sin_servicio_min": min(horas), "horas_sin_servicio_max": max(horas),
                "viv_sin_agua_min": smin, "viv_sin_agua_max": smax,
                "pct_sin_agua_min": round(pmin, 1), "pct_sin_agua_max": round(100 * smax / V, 1),
                "personas_sin_agua_min": round(smin * o, 1), "personas_sin_agua_max": round(smax * o, 1),
                "viv_agua_guardada_min": gmin, "viv_agua_guardada_max": gmax,
                "requiere_desinfeccion": gmax > 0,
                "estado": clasificar(pmin, sup),
                "severidad": round(pmin / 100, 4),
            }


def cargar_supuestos(ruta, cambios):
    sup = leer_json(ruta)
    for par in cambios or []:
        clave, _, valor = par.partition("=")
        if clave not in sup:
            raise SystemExit(f"supuesto desconocido: {clave}")
        sup[clave] = float(valor)
    return sup


def rango_fechas(desde, hasta):
    d0, d1 = dt.date.fromisoformat(desde), dt.date.fromisoformat(hasta)
    return [d0 + dt.timedelta(days=i) for i in range((d1 - d0).days + 1)]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manzanas", required=True)
    p.add_argument("--zonas", help="CSV cvegeo,zona. Sin este archivo, ninguna manzana tiene racionamiento")
    p.add_argument("--calendario", default=str(BASE / "calendarios" / "vigente-2026-11-03.json"))
    p.add_argument("--supuestos", default=str(BASE / "supuestos.json"))
    p.add_argument("--desde", default="2026-11-09")
    p.add_argument("--hasta", default="2026-11-15")
    p.add_argument("--set", action="append", help="clave=valor, sobrescribe un supuesto")
    p.add_argument("--salida", help="archivo CSV; por omisión, la salida estándar")
    a = p.parse_args(argv)

    sup = cargar_supuestos(a.supuestos, a.set)
    cal = leer_json(a.calendario)
    esquema = cal["esquema"]
    fechas = rango_fechas(a.desde, a.hasta)

    with open(a.manzanas, newline="", encoding="utf-8") as fh:
        manzanas = list(csv.DictReader(fh))
    zonas = {}
    if a.zonas:
        with open(a.zonas, newline="", encoding="utf-8") as fh:
            zonas = {r["cvegeo"]: r["zona"] for r in csv.DictReader(fh)}
    sin_zona = sum(1 for m in manzanas if m["cvegeo"] not in zonas)

    out = open(a.salida, "w", newline="", encoding="utf-8") if a.salida else sys.stdout
    w = csv.DictWriter(out, fieldnames=COLUMNAS)
    w.writeheader()
    n = 0
    for fila in procesar(manzanas, zonas, esquema, fechas, sup):
        w.writerow(fila)
        n += 1
    if a.salida:
        out.close()
    print(f"calendario: {cal.get('version')} | manzanas: {len(manzanas)} | fechas: {len(fechas)} | "
          f"renglones: {n} | manzanas sin zona asignada (tratadas como fuera del programa): {sin_zona}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
