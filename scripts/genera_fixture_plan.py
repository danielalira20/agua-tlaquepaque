#!/usr/bin/env python3
"""
Genera fixtures/plan.fixture.json aplicando las secciones 5 a 8 de optimizador/ESPECIFICACION.md
(rama feat/priorizador-especificacion) sobre el universo del fixture: las 40 manzanas de
fixtures/manzanas.fixture.csv y una sola fecha.

PROVISIONAL: existe para que el contrato `plan` tenga un ejemplo con la forma y las cuentas
correctas. Cuando exista la implementación de referencia del priorizador (carril de Jass), el
fixture se regenera con ella y este script se borra.

    python3 scripts/genera_fixture_plan.py

Diferencias respecto a la corrida real, declaradas en el propio fixture:
  - el universo son 40 manzanas, no 4,871: un viaje solo puede encontrar vecinas dentro de esas 40
  - `viajes_por_dia` = 5 (no 63) para que el ejemplo sea legible
  - una sola fecha, así que `semana` es esa fecha
"""
import csv
import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FECHA = "2026-11-12"
PARAM = {"pipas": 32, "litros_por_viaje": 10000, "litros_por_hogar": 200, "viajes_por_dia": 5,
         "radio_cobertura_m": 300, "modo_racha": "desempate"}
HOGARES = PARAM["litros_por_viaje"] // PARAM["litros_por_hogar"]
R_TIERRA = 6371000.0


def haversine(lon1, lat1, lon2, lat2):
    p = math.pi / 180
    a = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return 2 * R_TIERRA * math.asin(math.sqrt(a))


def leer(ruta):
    with open(RAIZ / ruta, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def cargar():
    fix = {r["cvegeo"] for r in leer("fixtures/manzanas.fixture.csv")}
    cent = {r["cvegeo"]: r for r in leer("datos/manzanas_centroides.csv") if r["cvegeo"] in fix}
    colonia = {r["cvegeo"]: r["colonia"] for r in leer("datos/manzana_colonia.csv")}
    estado = {r["cvegeo"]: r for r in leer("fixtures/estado.fixture.csv") if r["fecha"] == FECHA}
    return cent, colonia, estado


def cisternas():
    """Cisternas del baseline: coordenada exacta, o centro de su colonia, o excluidas."""
    todas = leer("datos/cisternas_tlaquepaque.csv")
    mz = leer("datos/manzanas_centroides.csv")
    mc = {r["cvegeo"]: r for r in leer("datos/manzana_colonia.csv")}
    por_geocol = {}
    for r in mz:
        g = mc.get(r["cvegeo"], {}).get("geocol")
        if g:
            por_geocol.setdefault(int(g), []).append((float(r["lon"]), float(r["lat"])))
    # a algunas cisternas les quedó la colonia pero no el geocol: se recupera por nombre solo si es único
    nombres = {}
    for r in leer("datos/colonias_tlaquepaque.csv"):
        nombres.setdefault(r["colonia"], []).append(int(r["geocol"]))
    usadas, excluidas = [], []
    for c in sorted(todas, key=lambda r: r["id"]):
        if not c["geocol"] and c["colonia_capa"] and len(nombres.get(c["colonia_capa"], [])) == 1:
            c["geocol"] = str(nombres[c["colonia_capa"]][0])
        if c["tipo"] == "propuesta_municipio":
            continue
        if c["fuente_ubicacion"] == "coordenada_exacta" and c["lat"]:
            usadas.append({"id": c["id"], "tipo": c["tipo"], "ubicacion": "coordenada_exacta",
                           "lon": float(c["lon"]), "lat": float(c["lat"]), "colonia": c["colonia_capa"]})
        elif c["colonia_capa"] and c["geocol"] and int(float(c["geocol"])) in por_geocol:
            pts = por_geocol[int(float(c["geocol"]))]
            usadas.append({"id": c["id"], "tipo": c["tipo"], "ubicacion": "centro_de_colonia",
                           "lon": round(sum(p[0] for p in pts) / len(pts), 6),
                           "lat": round(sum(p[1] for p in pts) / len(pts), 6), "colonia": c["colonia_capa"]})
        else:
            excluidas.append({"id": c["id"], "motivo": "sin coordenada ni colonia"})
    return usadas, excluidas


def llenar(lon, lat, resto, cent, radio, cupo=HOGARES):
    """Un viaje estacionado en (lon, lat): de la manzana más cercana a la más lejana, hasta agotar el cupo."""
    vec = []
    for cve, r in cent.items():
        d = haversine(lon, lat, float(r["lon"]), float(r["lat"]))
        if d <= radio + 1e-6:
            vec.append((d, cve))
    reparto = {}
    for _, cve in sorted(vec):
        n = min(resto.get(cve, 0), cupo)
        if n > 0:
            reparto[cve] = n
            cupo -= n
        if cupo == 0:
            break
    return reparto


def corrida(regla, cota, cent, colonia, estado, cist):
    necesidad = {c: int(estado[c][f"viv_sin_agua_{cota}"]) for c in estado}
    horas = {c: float(estado[c][f"horas_sin_servicio_{cota}"]) for c in estado}
    peso = {c: horas[c] / 24 for c in estado}
    ocup = {c: float(cent[c]["ocupantes_prom"]) for c in cent}
    resto = dict(necesidad)
    viajes, atendidas_por_mz = [], {}
    for k in range(1, PARAM["viajes_por_dia"] + 1):
        if regla == "priorizado":
            cand = [c for c in cent if resto.get(c, 0) > 0]
            if not cand:
                break
            opciones = []
            for c in cand:
                rep = llenar(float(cent[c]["lon"]), float(cent[c]["lat"]), resto, cent, PARAM["radio_cobertura_m"])
                a = sum(rep.values())
                pond = sum(n * peso[m] for m, n in rep.items())
                opciones.append((-a, -pond, c, rep))
            _, _, centro, rep = sorted(opciones, key=lambda o: (o[0], o[1], o[2]))[0]
            punto = {"tipo": "pipa", "punto_id": None, "cvegeo_centro": centro, "colonia": colonia.get(centro, ""),
                     "lon": float(cent[centro]["lon"]), "lat": float(cent[centro]["lat"])}
        else:
            ci = cist[(k - 1) % len(cist)]
            rep = llenar(ci["lon"], ci["lat"], resto, cent, PARAM["radio_cobertura_m"])
            punto = {"tipo": "cisterna", "punto_id": ci["id"], "cvegeo_centro": None, "colonia": ci["colonia"],
                     "lon": ci["lon"], "lat": ci["lat"]}
        for m, n in rep.items():
            resto[m] -= n
            atendidas_por_mz[m] = atendidas_por_mz.get(m, 0) + n
        a = sum(rep.values())
        viajes.append({"orden_eleccion": k, **punto,
                       "manzanas_cubiertas": [{"cvegeo": m, "viviendas": n} for m, n in rep.items()],
                       "viviendas_objetivo": a, "litros": a * PARAM["litros_por_hogar"],
                       "personas_beneficiadas": round(sum(n * ocup[m] for m, n in rep.items()), 1),
                       "prioridad_score": round(sum(n * peso[m] for m, n in rep.items()), 2)})
    nec_total = sum(necesidad.values())
    atendidas = sum(v["viviendas_objetivo"] for v in viajes)
    ponderado = sum(n * peso[m] for m, n in atendidas_por_mz.items())
    cupo_total = PARAM["viajes_por_dia"] * HOGARES
    nec_con_centroide = sum(necesidad[m] for m in necesidad if m in cent)
    max_viv = min(cupo_total, nec_con_centroide)
    pesos = sorted((peso[m] for m in necesidad for _ in range(necesidad[m]) if m in cent), reverse=True)
    max_pond = sum(pesos[:cupo_total])
    sin_entrega = [m for m in necesidad if necesidad[m] > 0 and atendidas_por_mz.get(m, 0) == 0]
    resumen = {
        "necesidad_total": nec_total, "viviendas_atendidas": atendidas,
        "personas_atendidas": round(sum(n * ocup[m] for m, n in atendidas_por_mz.items()), 1),
        "valor_ponderado": round(ponderado, 2), "maximo_viviendas": max_viv, "maximo_ponderado": round(max_pond, 2),
        "eficiencia_viviendas_pct": round(100 * atendidas / max_viv, 1) if max_viv else 100.0,
        "eficiencia_ponderada_pct": round(100 * ponderado / max_pond, 1) if max_pond else 100.0,
        "cobertura_pct": round(100 * atendidas / nec_total, 1) if nec_total else 0.0,
        "viajes_usados": len(viajes), "viajes_sin_usar": PARAM["viajes_por_dia"] - len(viajes)}
    semana = {k: v for k, v in resumen.items()}
    semana["manzanas_sin_entrega"] = len(sin_entrega)
    semana["personas_sin_entrega"] = round(sum(necesidad[m] * ocup[m] for m in sin_entrega), 1)
    return {"regla": regla, "cota_para_ordenar": cota,
            "fechas": [{"fecha": FECHA, "viajes": viajes, "resumen": resumen}], "semana": semana}


def main():
    cent, colonia, estado = cargar()
    usadas, excluidas = cisternas()
    corridas = [corrida(r, c, cent, colonia, estado, usadas) for c in ("min", "max") for r in ("priorizado", "baseline")]
    comp = []
    for c in ("min", "max"):
        p = next(x for x in corridas if x["regla"] == "priorizado" and x["cota_para_ordenar"] == c)["semana"]
        b = next(x for x in corridas if x["regla"] == "baseline" and x["cota_para_ordenar"] == c)["semana"]
        comp.append({"cota_para_ordenar": c, "semana": {
            k: {"priorizado": p[k], "baseline": b[k], "diferencia": round(p[k] - b[k], 2)} for k in p}})
    plan = {
        "parametros": dict(PARAM, hogares_por_viaje=HOGARES, cota_para_ordenar="min"),
        "nota_fixture": "Universo de 40 manzanas, una fecha (2026-11-12) y 5 viajes por dia. Generado por "
                        "scripts/genera_fixture_plan.py con las secciones 5 a 8 de optimizador/ESPECIFICACION.md. "
                        "Con solo 5 viajes el baseline usa las 5 primeras cisternas por id, y con un universo de 40 "
                        "manzanas su resultado depende de cuales caen cerca de alguna: es un efecto del universo reducido, "
                        "no un resultado.",
        "baseline": {
            "descripcion": "Baseline estilizado: los mismos viajes repartidos por turnos entre las cisternas ya instaladas "
                           "(el viaje k va a la cisterna (k-1) mod N). No es el reparto real del municipio, que responde a "
                           "reportes ciudadanos y del que no hay registro.",
            "cisternas": usadas, "excluidas": excluidas},
        "corridas": corridas, "comparacion": comp, "propuesta_cisternas": None}
    ruta = RAIZ / "fixtures" / "plan.fixture.json"
    ruta.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cisternas del baseline: {len(usadas)} usadas, {len(excluidas)} excluidas")
    for c in corridas:
        s = c["semana"]
        print(c["regla"], c["cota_para_ordenar"], "| necesidad", s["necesidad_total"], "| atendidas", s["viviendas_atendidas"],
              "| max", s["maximo_viviendas"], "| efic", s["eficiencia_viviendas_pct"], "| usados", s["viajes_usados"])


if __name__ == "__main__":
    main()
