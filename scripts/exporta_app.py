#!/usr/bin/env python3
"""
Exporta los datos REALES para la app (Next.js estatica) y los vectores de prueba del motor en TypeScript.

    python3 scripts/exporta_app.py                                   # semana de referencia del reporte
    python3 scripts/exporta_app.py --desde 2026-11-16 --hasta 2026-11-22  # cualquier otra semana
    python3 scripts/exporta_app.py --desde ... --hasta ... --dia-inicial 2026-11-19

Sin argumentos exporta la semana de referencia del reporte (9 al 15 de noviembre de 2026), que abre en el
jueves 12, el dia que usan el reporte y sus figuras. Con otra ventana, la app abre en el dia de hoy si cae dentro
de la ventana; si no, en --dia-inicial; y si no se da, en el primer dia. La ventana no puede empezar antes de que
entrara en vigor el calendario vigente (motor/calendarios/vigente-2026-11-03.json).

Corre el motor de referencia (motor/referencia.py) y el priorizador de referencia (optimizador/) sobre las
4,871 manzanas y escribe, en app/public/datos/real/:

    meta.json         ventana, calendario usado, supuestos, conteos, fuentes y advertencias
    manzanas.json     una fila por manzana: ubicacion, viviendas, tinaco, cisterna, zona, marginacion
    estado.json       salida del motor por fecha, en columnas alineadas con manzanas.json
    calendarios.json  calendario vigente y original, expandidos a fechas, con la forma que ya usa la app
    cisternas.json    las 50 cisternas (35 exactas, 12 por colonia, 3 sin ubicar) y las 10 propuestas
    plan.json         salida del priorizador (contrato plan v2): priorizado y baseline, cota minima y maxima
    LEEME.md          que es cada archivo y cada campo

y en motor/vectores/vectores.json los casos para comparar el motor oficial (TypeScript) contra el de
referencia: entradas, supuestos y la salida esperada.

NO toca los archivos simulados que la app lee hoy (colonias.json, calendario.json): escribe en real/.
Todo es determinista: correrlo dos veces da archivos identicos.
"""
import argparse
import csv
import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "motor"))
import referencia as R  # noqa: E402

DESTINO = RAIZ / "app" / "public" / "datos" / "real"
VECTORES = RAIZ / "motor" / "vectores" / "vectores.json"
GRADOS = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo"]
# Conjuntos de supuestos de los vectores: cada uno ejercita una rama distinta del motor
# Semana que usan el reporte cientifico y sus figuras: lo que se exporta sin argumentos.
SEMANA_REFERENCIA = {"desde": "2026-11-09", "hasta": "2026-11-15", "dia_inicial": "2026-11-12"}
CALENDARIO_VIGENTE = "vigente-2026-11-03.json"
CONJUNTOS_VECTORES = {
    "base": {},
    "consumo_100": {"consumo_l_persona_dia": 100},
    "consumo_100_f_050": {"consumo_l_persona_dia": 100, "fraccion_suministro_en_racionamiento": 0.5},
    "horas_36_u_72": {"horas_efectivas_corte": 36, "u_horas_agua_guardada": 72},
}


def leer(ruta):
    with open(RAIZ / ruta, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def volcar(ruta, obj, indent=None):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    txt = json.dumps(obj, ensure_ascii=False, indent=indent, separators=(",", ":") if indent is None else None)
    ruta.write_text(txt + "\n", encoding="utf-8")


def entero(x):
    return int(round(float(x or 0)))


def cargar_manzanas():
    base = leer("datos/manzanas_tlaquepaque.csv")
    cent = {r["cvegeo"]: r for r in leer("datos/manzanas_centroides.csv")}
    col = {r["cvegeo"]: r for r in leer("datos/manzana_colonia.csv")}
    zon = {r["cvegeo"]: r for r in leer("datos/zonas_siapa/manzana_zona.csv")}
    grado = {r["CVE_AGEB"]: r["GM_2020"] for r in leer("datos/marginacion_ageb_tlaquepaque.csv")}
    filas = []
    for m in base:
        c = m["cvegeo"]
        z = zon.get(c, {})
        zona = z.get("zona", "")
        filas.append({
            "cvegeo": c,
            "colonia": col.get(c, {}).get("colonia", ""),
            "geocol": col.get(c, {}).get("geocol", ""),
            "zona": zona,
            "zona_confianza": z.get("confianza", "sin_geometria"),
            "en_programa": zona != "",
            "lon": float(cent[c]["lon"]) if c in cent else None,
            "lat": float(cent[c]["lat"]) if c in cent else None,
            "viviendas": entero(m["viviendas"]),
            "pob": entero(m["pob"]),
            "ocupantes_prom": float(m["ocupantes_prom"]),
            "viv_tinaco": entero(m["viv_tinaco"]),
            "viv_cisterna": entero(m["viv_cisterna"]),
            "sin_almacen_min": entero(m["sin_almacen_min"]),
            "sin_almacen_max": entero(m["sin_almacen_max"]),
            "grado_marginacion": grado.get(c[:13], "sin dato"),
        })
    return filas


def marcar_nucleo_robusto(manzanas):
    """Agrega `nucleo_robusto` (true/false) a cada manzana, desde datos/sensibilidad/manzanas_robustas.csv.

    Es un paso aparte de cargar_manzanas() a proposito: ese CSV es una SALIDA de scripts/sensibilidad_orden.py, que a su vez
    importa cargar_manzanas(). Si se leyera adentro, una primera corrida de la sensibilidad dependeria de si misma.
    El nucleo son las manzanas que quedan entre las 250 de mayor riesgo en al menos el 90% de los 300 sorteos de la familia A
    (los rangos de la decision 1). Una manzana que no esta en el CSV nunca entro al top 250 en ningun sorteo: no es nucleo.
    Devuelve cuantas son.
    """
    nucleo = {r["cvegeo"] for r in leer("datos/sensibilidad/manzanas_robustas.csv") if r["nucleo_robusto"] == "True"}
    ajenas = nucleo - {m["cvegeo"] for m in manzanas}
    if ajenas:
        raise ValueError(f"manzanas_robustas.csv trae {len(ajenas)} manzanas que no estan en el Censo (CSV desactualizado): "
                         f"{sorted(ajenas)[:3]}")
    for m in manzanas:
        m["nucleo_robusto"] = m["cvegeo"] in nucleo
    return len(nucleo)


def calendario_expandido(archivo, fechas):
    cal = R.leer_json(RAIZ / "motor" / "calendarios" / archivo)
    dias = []
    for f in fechas:
        d = R.dia_semana(f)
        dias.append({"fecha": f.isoformat(), "dia": d,
                     "zonas_sin_servicio": sorted(int(z) for z, ds in cal["esquema"].items() if d in ds)})
    out = {k: v for k, v in cal.items()}
    out["dias"] = dias
    return out


def correr_motor_y_priorizador(desde, hasta, tmp):
    estado = Path(tmp) / "estado.csv"
    plan = Path(tmp) / "plan.json"
    R.main(["--manzanas", str(RAIZ / "datos" / "manzanas_tlaquepaque.csv"),
            "--zonas", str(RAIZ / "datos" / "zonas_siapa" / "manzana_zona.csv"),
            "--calendario", str(RAIZ / "motor" / "calendarios" / CALENDARIO_VIGENTE),
            "--desde", desde, "--hasta", hasta, "--salida", str(estado)])
    subprocess.run([sys.executable, "-m", "optimizador.priorizador", "--estado", str(estado), "--salida", str(plan)],
                   cwd=RAIZ, check=True, capture_output=True)
    return estado, plan


def construir_estado(estado_csv, manzanas, fechas):
    idx = {m["cvegeo"]: i for i, m in enumerate(manzanas)}
    n = len(manzanas)
    cols = ["viv_sin_agua_min", "viv_sin_agua_max", "viv_agua_guardada_min", "viv_agua_guardada_max",
            "horas_sin_servicio_min", "horas_sin_servicio_max", "estado", "requiere_desinfeccion"]
    por_fecha = {f.isoformat(): {c: [0] * n for c in cols} for f in fechas}
    codigo = {"con_agua": 0, "quiebre_parcial": 1, "quiebre_mayoritario": 2}
    with open(estado_csv, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = por_fecha[r["fecha"]]
            i = idx[r["cvegeo"]]
            for c in ("viv_sin_agua_min", "viv_sin_agua_max", "viv_agua_guardada_min", "viv_agua_guardada_max"):
                d[c][i] = int(r[c])
            d["horas_sin_servicio_min"][i] = int(float(r["horas_sin_servicio_min"]))
            d["horas_sin_servicio_max"][i] = int(float(r["horas_sin_servicio_max"]))
            d["estado"][i] = codigo[r["estado"]]
            d["requiere_desinfeccion"][i] = 1 if r["requiere_desinfeccion"] == "True" else 0
    return {"orden": "mismo orden que manzanas.json", "estado_codigo": {"0": "con_agua", "1": "quiebre_parcial", "2": "quiebre_mayoritario"},
            "fechas": [{"fecha": f.isoformat(), "dia": R.dia_semana(f), **por_fecha[f.isoformat()]} for f in fechas]}


def construir_cisternas(plan):
    usadas = {c["id"].split("@")[0] + "@" + c["tipo"].replace("cisterna_", "") if "@" not in c["id"] else c["id"]: c
             for c in plan["baseline"]["cisternas"]}
    out = []
    for c in leer("datos/cisternas_tlaquepaque.csv"):
        prop = c["tipo"] == "propuesta_municipio"
        clave = c["id"] + "@" + {"cisterna_municipal": "municipal", "cisterna_siapa": "siapa"}.get(c["tipo"], "")
        u = usadas.get(clave) or usadas.get(c["id"])
        if prop:
            ub, lon, lat = ("coordenada_exacta", float(c["lon"]), float(c["lat"])) if c["lat"] else ("sin_ubicar", None, None)
        elif u:
            ub, lon, lat = u["ubicacion"], u["lon"], u["lat"]
        else:
            ub, lon, lat = "sin_ubicar", None, None
        out.append({"id": c["id"], "tipo": c["tipo"], "colonia": c["colonia_capa"], "ubicacion": ub, "lon": lon, "lat": lat,
                    "cuenta_como_cobertura": (not prop) and ub != "sin_ubicar"})
    return out


def construir_vectores(manzanas, fechas, sup_base):
    """Casos para comparar el motor oficial contra el de referencia. Seleccion determinista."""
    orden = sorted(manzanas, key=lambda m: m["cvegeo"])
    elegidas = orden[::80]
    ids = {m["cvegeo"] for m in elegidas}
    for criterio in (lambda m: "," in m["zona"], lambda m: m["zona"] == "", lambda m: m["viviendas"] <= 3):
        extra = [m for m in orden if criterio(m) and m["cvegeo"] not in ids][:5]
        elegidas += extra
        ids |= {m["cvegeo"] for m in extra}
    elegidas = sorted(elegidas, key=lambda m: m["cvegeo"])
    entradas = [{k: m[k] for k in ("cvegeo", "zona", "viviendas", "viv_tinaco", "viv_cisterna", "ocupantes_prom")} for m in elegidas]
    zonas = {m["cvegeo"]: m["zona"] for m in elegidas}
    filas_ref = [{"cvegeo": m["cvegeo"], "viviendas": m["viviendas"], "viv_tinaco": m["viv_tinaco"],
                  "viv_cisterna": m["viv_cisterna"], "ocupantes_prom": m["ocupantes_prom"]} for m in elegidas]
    esquema = R.leer_json(RAIZ / "motor" / "calendarios" / CALENDARIO_VIGENTE)["esquema"]
    conjuntos = {}
    for nombre, cambios in CONJUNTOS_VECTORES.items():
        sup = dict(sup_base, **cambios)
        salida = []
        for r in R.procesar(filas_ref, zonas, esquema, fechas, sup):
            salida.append({k: r[k] for k in ("cvegeo", "fecha", "horas_sin_servicio_min", "horas_sin_servicio_max", "viv_sin_agua_min",
                                             "viv_sin_agua_max", "viv_agua_guardada_min", "viv_agua_guardada_max", "estado")})
        conjuntos[nombre] = {"supuestos": sup, "salida": salida}
    return {
        "descripcion": "Vectores para el motor oficial (TypeScript). Cada conjunto trae los supuestos y la salida esperada de la implementacion de "
                       "referencia (motor/referencia.py) para las mismas entradas. Los conteos de viviendas deben coincidir EXACTAMENTE; las "
                       f"horas tambien. Calendario: motor/calendarios/{CALENDARIO_VIGENTE}. Especificacion: motor/ESPECIFICACION.md.",
        "calendario": CALENDARIO_VIGENTE.removesuffix(".json"), "fechas": [f.isoformat() for f in fechas],
        "casos": {"entradas": len(entradas), "con_varias_zonas": sum(1 for m in elegidas if "," in m["zona"]),
                  "fuera_del_programa": sum(1 for m in elegidas if m["zona"] == "")},
        "entradas": entradas, "conjuntos": conjuntos}


LEEME = """# Datos reales para la app

Generados por `scripts/exportar_app.py` (`python3 scripts/exporta_app.py`). **No se editan a mano**: se regeneran.
Reemplazan a los datos simulados de `app/public/datos/` (`colonias.json`, `calendario.json`), que siguen ahi
mientras la app no cambie; nada de esta carpeta los toca.

Ventana: **{desde} a {hasta}**; la app abre en **{dia_inicial}** si hoy no cae en la ventana. Calendario: **{calendario}**.
Para otra ventana: `python3 scripts/exporta_app.py --desde AAAA-MM-DD --hasta AAAA-MM-DD [--dia-inicial AAAA-MM-DD]`.
Sin argumentos se exporta la semana de referencia del reporte.

## Archivos

| Archivo | Qué es |
|---|---|
| `meta.json` | Ventana, calendario usado, supuestos del motor, conteos, fuentes y advertencias. **Mostrar las advertencias en la app** |
| `manzanas.json` | 4,871 manzanas. El orden es la llave de posicion de `estado.json` |
| `estado.json` | Salida del motor por fecha, en columnas alineadas con `manzanas.json` (el elemento `i` de cada arreglo es la manzana `i`) |
| `calendarios.json` | `vigente` y `original`, con la forma del `Calendario` que ya usa la app (`version`, `consultado`, `esquema`, `dias`), mas `vigente_desde` y `vigente_hasta` |
| `cisternas.json` | 60 registros: 50 cisternas y 10 propuestas del municipio |
| `plan.json` | Salida del priorizador (`contratos/plan.schema.json` v2) |

## `manzanas.json`

Arreglo de objetos: `cvegeo` (16 caracteres, **siempre texto**), `colonia` y `geocol` (capa del IIEG; vacio en 22
manzanas), `zona` (`"4"`, `"3,4"` si abarca varias, `""` si esta **fuera del programa**), `zona_confianza`
(`alta`, `media`, `baja`, `conflicto`, `ambiguo`, `ninguna`, `sin_poligono`, `sin_geometria`), `en_programa`, `lon`/`lat`
(centroide; `null` en las 8 manzanas sin geometria), `viviendas`, `pob`, `ocupantes_prom`, `viv_tinaco`,
`viv_cisterna`, `sin_almacen_min`/`sin_almacen_max` (cotas: el Censo no cruza tinaco con cisterna),
`grado_marginacion` (`Muy alto` a `Muy bajo` o `sin dato`; **mas alto = mas marginacion**; es una capa aparte, no entra
en `severidad`), `nucleo_robusto` (`true` en las 186 manzanas que quedan entre las 250 de mayor riesgo en al menos el 90% de
los 300 sorteos de la familia A de `datos/sensibilidad/`; es la parte del orden que **no depende de los supuestos**. Sale de
`datos/sensibilidad/manzanas_robustas.csv`; `false` si nunca entro al top 250).

## `estado.json`

`fechas` es una lista con un objeto por fecha: `fecha`, `dia` y arreglos de largo 4,871: `viv_sin_agua_min/max`,
`viv_agua_guardada_min/max`, `horas_sin_servicio_min/max`, `estado` (0 con agua, 1 quiebre parcial, 2 quiebre
mayoritario) y `requiere_desinfeccion` (0/1). El porcentaje y las personas se derivan:
`pct = 100 * viv_sin_agua / viviendas` y `personas = viv_sin_agua * ocupantes_prom`. El estado se calcula con
`pct_min` **sin redondear** (menor de 10, de 10 a 50, mayor de 50). Siempre hay un **minimo y un maximo**: nunca
mostrar un solo numero sin decir que es una cota.

## `plan.json`

Cuatro corridas: priorizado y baseline, con cota minima y con cota maxima, y su comparacion. Cada viaje trae
`lon`/`lat` del punto, las manzanas cubiertas y las viviendas atendidas. **El baseline es estilizado**: los mismos viajes
repartidos por turnos entre las cisternas instaladas; no es lo que hace hoy el municipio. `orden_eleccion` no es una ruta.

## Advertencias que la app debe decir

1. Un dia de racionamiento se modela como **cero agua** (`f = 0`), la cota alta del dano. El portal del SIAPA dice que
   es una baja de presion.
2. Las zonas salen de dos fuentes que no siempre coinciden: el 16% de la poblacion tiene zona solo por el poligono del
   portal. Ver `zona_confianza`.
3. El Censo es de 2020 y no dice la capacidad de tinacos y cisternas (se asumen 1,100 y 5,000 L).
4. El calendario del SIAPA ya cambio una vez y puede volver a cambiar.

## Para el motor oficial en TypeScript

`motor/vectores/vectores.json` trae las entradas, los supuestos y la salida esperada del motor de referencia para
cuatro conjuntos de supuestos. El motor de la app debe reproducirlos: los conteos de viviendas y las horas, exactos. La
formula esta en `motor/ESPECIFICACION.md`.
"""


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--desde", default=SEMANA_REFERENCIA["desde"])
    p.add_argument("--hasta", default=SEMANA_REFERENCIA["hasta"])
    p.add_argument("--dia-inicial", default=None, help="dia con el que abre la app si hoy no cae en la ventana")
    p.add_argument("--destino", default=str(DESTINO), help="carpeta de salida (por omision, la de la app)")
    p.add_argument("--vectores", default=str(VECTORES), help="archivo de vectores del motor")
    a = p.parse_args(argv)
    destino, vectores = Path(a.destino), Path(a.vectores)
    fechas = R.rango_fechas(a.desde, a.hasta)
    if not fechas:
        raise SystemExit(f"--hasta ({a.hasta}) es anterior a --desde ({a.desde})")
    vigente = R.leer_json(RAIZ / "motor" / "calendarios" / CALENDARIO_VIGENTE)
    if a.desde < vigente["vigente_desde"]:
        raise SystemExit(f"El calendario vigente rige desde el {vigente['vigente_desde']}: no se puede exportar desde el {a.desde}. "
                         "Para fechas anteriores hay que agregar ese calendario en motor/calendarios/.")
    if vigente.get("vigente_hasta") and a.hasta > vigente["vigente_hasta"]:
        raise SystemExit(f"El calendario vigente rige hasta el {vigente['vigente_hasta']}: no se puede exportar hasta el {a.hasta}.")
    dia_inicial = a.dia_inicial
    if dia_inicial is None:
        es_referencia = (a.desde, a.hasta) == (SEMANA_REFERENCIA["desde"], SEMANA_REFERENCIA["hasta"])
        dia_inicial = SEMANA_REFERENCIA["dia_inicial"] if es_referencia else a.desde
    if dia_inicial not in {f.isoformat() for f in fechas}:
        raise SystemExit(f"--dia-inicial ({dia_inicial}) no esta entre {a.desde} y {a.hasta}")
    manzanas = cargar_manzanas()
    n_nucleo = marcar_nucleo_robusto(manzanas)
    sup = R.leer_json(RAIZ / "motor" / "supuestos.json")

    with tempfile.TemporaryDirectory() as tmp:
        estado_csv, plan_json = correr_motor_y_priorizador(a.desde, a.hasta, tmp)
        estado = construir_estado(estado_csv, manzanas, fechas)
        plan = json.loads(plan_json.read_text(encoding="utf-8"))

    cal = {"vigente": calendario_expandido(CALENDARIO_VIGENTE, fechas),
           "original": calendario_expandido("original-2026-10-15.json", fechas)}
    cist = construir_cisternas(plan)
    en_prog = [m for m in manzanas if m["en_programa"]]
    meta = {
        "formato": 1, "simulado": False, "ventana": {"desde": a.desde, "hasta": a.hasta, "fechas": len(fechas), "dia_inicial": dia_inicial},
        "calendario_usado": cal["vigente"]["version"], "supuestos": sup,
        "conteos": {"manzanas": len(manzanas), "manzanas_en_programa": len(en_prog),
                    "manzanas_nucleo_robusto": n_nucleo,
                    "personas": sum(m["pob"] for m in manzanas), "personas_en_programa": sum(m["pob"] for m in en_prog),
                    "personas_en_programa_con_respaldo_de_la_lista": sum(m["pob"] for m in en_prog if m["zona_confianza"] in ("alta", "media", "conflicto")),
                    "cisternas": sum(1 for c in cist if not c["id"].startswith("PROP")), "propuestas": sum(1 for c in cist if c["id"].startswith("PROP"))},
        "fuentes": ["INEGI, Censo 2020 (manzana)", "SIAPA, portal de rotacion y lista oficial de colonias (11-nov-2026)",
                    "CONAPO, indice de marginacion urbana por AGEB 2020", "Gobierno de San Pedro Tlaquepaque, mapa de cisternas (2026)"],
        "advertencias": ["Un dia de racionamiento se modela como cero agua (f = 0): es la cota alta del dano, no una medicion.",
                         "Las zonas salen de dos fuentes que no siempre coinciden; el 16% de la poblacion tiene zona solo por el poligono del portal.",
                         "Censo 2020; el Censo no dice la capacidad de tinacos ni cisternas.",
                         "El calendario del SIAPA puede volver a cambiar.",
                         "El baseline del priorizador es estilizado: no es el reparto real del municipio."]}
    destino.mkdir(parents=True, exist_ok=True)
    volcar(destino / "meta.json", meta, indent=2)
    volcar(destino / "manzanas.json", manzanas)
    volcar(destino / "estado.json", estado)
    volcar(destino / "calendarios.json", cal)
    volcar(destino / "cisternas.json", cist)
    volcar(destino / "plan.json", plan)
    (destino / "LEEME.md").write_text(LEEME.replace("scripts/exportar_app.py", "scripts/exporta_app.py")
                                      .format(desde=a.desde, hasta=a.hasta, dia_inicial=dia_inicial, calendario=cal["vigente"]["version"]),
                                      encoding="utf-8")
    volcar(vectores, construir_vectores(manzanas, fechas, sup), indent=None)
    for f in sorted(destino.iterdir()) + [vectores]:
        try:
            nombre = f.resolve().relative_to(RAIZ)
        except ValueError:
            nombre = f
        print(f"{nombre}  {f.stat().st_size / 1024:.0f} KB")

if __name__ == "__main__":
    main()
