"""Arma resultados/resumen.md: las tablas del comparador que van al reporte (decision 06).

Toda cifra sale de las tablas; el texto fijo es solo lo que se declara.
"""
from __future__ import annotations

from optimizador.priorizador.plan import COTAS_ORDEN

NOMBRE_COTA = {"min": "mínima", "max": "máxima"}


def _miles(v) -> str:
    return "—" if v is None else f"{v:,.0f}"


def _veces(v) -> str:
    return "—" if v is None else f"{v:.1f}×"


def _pct(v) -> str:
    return "—" if v is None else f"{v:.1f}%"


def _pesos(v, decimales: int = 0) -> str:
    return "—" if v is None else f"{v:,.{decimales}f} pesos"


def _baseline(turnos: str, cist: str, n: dict[str, int]) -> str:
    regla = "por turnos" if turnos == "todas" else "con necesidad"
    cuales = f"{n[cist]} cisternas" if cist == "todas" else f"{n[cist]} exactas"
    return f"{regla}, {cuales}"


def _tabla(encabezado: list[str], filas: list[list[str]], texto: int = 1) -> list[str]:
    """`texto` es cuantas columnas, desde la izquierda, son texto y se alinean a la izquierda."""
    alineacion = ["---"] * texto + ["---:"] * (len(encabezado) - texto)
    lineas = ["| " + " | ".join(encabezado) + " |", "|" + "|".join(alineacion) + "|"]
    return lineas + ["| " + " | ".join(f) + " |" for f in filas] + [""]


def _una(filas: list[dict], **campos) -> dict:
    halladas = [f for f in filas if all(f[k] == v for k, v in campos.items())]
    if len(halladas) != 1:
        raise ValueError(f"se esperaba una fila con {campos} y hay {len(halladas)}")
    return halladas[0]


def _minimo(filas: list[dict]) -> dict | None:
    con_valor = [f for f in filas if f["veces"] is not None]
    return min(con_valor, key=lambda f: f["veces"]) if con_valor else None


def _caso_base(tablas: dict, ctx: dict, combos: list[tuple[str, str]]) -> list[str]:
    base = [f for f in tablas["rejilla_priorizador"] if f["modo_racha"] == ctx["modo_racha"] and f["radio_m"] == ctx["radio"]]
    fila = lambda **k: _una(base, **k)  # noqa: E731
    filas = [
        ["Viviendas-día sin agua"] + [_miles(fila(cota=c, baseline_turnos=combos[0][0], baseline_cisternas=combos[0][1])["necesidad_viv_dia"]) for c in COTAS_ORDEN],
        ["**Priorizado**"] + [f"**{_miles(fila(cota=c, baseline_turnos=combos[0][0], baseline_cisternas=combos[0][1])['prio_viv_dia'])}**" for c in COTAS_ORDEN],
    ]
    for t, c in combos:
        celdas = []
        for cota in COTAS_ORDEN:
            f = fila(cota=cota, baseline_turnos=t, baseline_cisternas=c)
            celdas.append(f"{_miles(f['base_viv_dia'])} ({_veces(f['veces'])})")
        filas.append([f"Baseline {_baseline(t, c, ctx['n_cisternas'])}"] + celdas)
    lineas = ["## 1. Caso base", "",
              f"`modo_racha = {ctx['modo_racha']}`, radio de {ctx['radio']} m. Viviendas-día atendidas en la semana "
              "y, entre paréntesis, cuántas veces lo del baseline.", ""]
    lineas += _tabla(["", "Cota mínima", "Cota máxima"], filas)
    m = _minimo(base)
    if m:
        vs = [f["veces"] for f in base if f["veces"] is not None]
        lineas += [f"Con los mismos viajes, el priorizado atiende entre {_veces(min(vs))} y {_veces(max(vs))} lo del baseline. "
                   f"La comparación más conservadora es **{_veces(m['veces'])}** (baseline "
                   f"{_baseline(m['baseline_turnos'], m['baseline_cisternas'], ctx['n_cisternas'])}, cota {NOMBRE_COTA[m['cota']]}).", ""]
    return lineas


def _rejilla(tablas: dict, ctx: dict) -> list[str]:
    rej = tablas["rejilla_priorizador"]
    filas = []
    for racha in ctx["sens"]["modo_racha"]:
        for radio in ctx["sens"]["radio_cobertura_m"]:
            sub = [f for f in rej if f["modo_racha"] == racha and f["radio_m"] == radio]
            pmin, pmax = (next(f for f in sub if f["cota"] == c) for c in COTAS_ORDEN)
            vs = [f["veces"] for f in sub if f["veces"] is not None]
            marca = " (base)" if (racha, radio) == (ctx["modo_racha"], ctx["radio"]) else ""
            filas.append([
                f"`{racha}`{marca}", f"{radio} m", _miles(pmin["prio_viv_dia"]), _miles(pmax["prio_viv_dia"]),
                _pct(min(pmin["prio_eficiencia_pct"], pmax["prio_eficiencia_pct"])),
                f"{_miles(pmin['prio_mzas_sin_entrega'])} / {_miles(pmax['prio_mzas_sin_entrega'])}",
                f"{_veces(min(vs))} a {_veces(max(vs))}" if vs else "—",
            ])
    lineas = ["## 2. Sensibilidad del priorizador", "",
              "Estado base. Cada renglón cambia la racha o el radio; la última columna es el rango contra los 4 baselines "
              "con las dos cotas. La eficiencia es contra el máximo de viviendas que se podían atender ese día.", ""]
    return lineas + _tabla(["modo_racha", "Radio", "Priorizado, cota mín.", "Priorizado, cota máx.", "Eficiencia mínima",
                            "Manzanas sin entrega (mín. / máx.)", "Veces el baseline"], filas, texto=2)


def _escenarios(tablas: dict, ctx: dict, combos: list[tuple[str, str]]) -> list[str]:
    esc = tablas["escenarios_motor"]
    filas = []
    for e in ctx["escenarios"]:
        for cota in COTAS_ORDEN:
            sub = [f for f in esc if f["escenario"] == e.nombre and f["cota"] == cota]
            celdas = [_veces(_una(sub, baseline_turnos=t, baseline_cisternas=c)["veces"]) for t, c in combos]
            filas.append([f"`{e.nombre}`", e.procedencia, NOMBRE_COTA[cota], _miles(sub[0]["necesidad_viv_dia"]),
                          _miles(sub[0]["prio_viv_dia"]), *celdas])
    lineas = ["## 3. Escenarios del motor", "",
              "Parámetros base del priorizador. Los escenarios son el caso base y las esquinas de la sensibilidad del motor "
              "(`datos/HALLAZGOS_sensibilidad.md`); la procedencia del rango es la que les da ese análisis.", ""]
    lineas += _tabla(["Escenario", "Procedencia", "Cota", "Viviendas-día sin agua", "Priorizado",
                      *[f"Veces: {_baseline(t, c, ctx['n_cisternas'])}" for t, c in combos]], filas, texto=3)
    m = _minimo(esc)
    if m:
        lineas += [f"En los {len(ctx['escenarios'])} escenarios, la comparación más baja es **{_veces(m['veces'])}** "
                   f"(`{m['escenario']}`, baseline {_baseline(m['baseline_turnos'], m['baseline_cisternas'], ctx['n_cisternas'])}, "
                   f"cota {NOMBRE_COTA[m['cota']]}).", ""]
    cambios = [f"- `{e.nombre}`: " + ", ".join(f"`{k} = {v}`" for k, v in e.cambios.items()) for e in ctx["escenarios"] if e.cambios]
    return lineas + (["Cambios de cada esquina respecto a `motor/supuestos.json`:", ""] + cambios + [""] if cambios else [])


def _equidad(tablas: dict) -> list[str]:
    eq = tablas["equidad_marginacion"]
    filas = [[f["grado"], NOMBRE_COTA[f["cota"]], _pct(f["pct_de_la_necesidad"]), _pct(f["prio_pct_de_lo_atendido"]),
              _pct(f["prio_cobertura_pct"]), _pct(f["base_turnos_cobertura_pct"]), _pct(f["base_con_necesidad_cobertura_pct"])]
             for f in eq]
    lineas = ["## 4. Equidad por grado de marginación", "",
              "Estado y parámetros base. Grado de marginación de la AGEB de cada manzana (CONAPO 2020). La cobertura es "
              "la parte de las viviendas-día sin agua de ese grado que recibe agua. Los baselines son los de 47 cisternas.", ""]
    lineas += _tabla(["Grado", "Cota", "% de las viviendas-día sin agua", "% de lo que atiende el priorizado",
                      "Cobertura: priorizado", "Cobertura: baseline por turnos", "Cobertura: baseline con necesidad"], filas, texto=2)
    for cota in COTAS_ORDEN:
        ma = [f for f in eq if f["cota"] == cota and f["grado"] == "Muy alto"]
        if ma:
            f = ma[0]
            lineas.append(f"- Cota {NOMBRE_COTA[cota]}: el priorizado atiende {_miles(f['prio_viv_dia'])} de las "
                          f"{_miles(f['necesidad_viv_dia'])} viviendas-día sin agua de AGEB «Muy alto»; el baseline por turnos, "
                          f"{_miles(f['base_turnos_viv_dia'])}.")
        juntos = [f for f in eq if f["cota"] == cota and f["grado"] in ("Alto", "Muy alto")]
        if juntos:
            lineas.append(f"- Cota {NOMBRE_COTA[cota]}, «Alto» y «Muy alto» juntos: el priorizado atiende "
                          f"{_miles(sum(f['prio_viv_dia'] for f in juntos))} viviendas-día; el baseline por turnos, "
                          f"{_miles(sum(f['base_turnos_viv_dia'] for f in juntos))}.")
    return lineas + [""]


def _cobertura(tablas: dict) -> list[str]:
    partes = []
    for cota in COTAS_ORDEN:
        vals = [f["prio_cobertura_pct"] for f in tablas["cobertura_diaria"] if f["cota"] == cota]
        partes.append(f"entre {_pct(min(vals))} y {_pct(max(vals))} con la cota {NOMBRE_COTA[cota]}")
    return ["## 5. Cobertura diaria", "",
            f"Cada día, el priorizado cubre {partes[0]}, y {partes[1]}, de las viviendas sin agua. "
            "Los viajes no alcanzan para todas: por eso importa a dónde van. Detalle por fecha en `cobertura_diaria.csv`.", ""]


def _costo(tablas: dict, ctx: dict, combos: list[tuple[str, str]]) -> list[str]:
    filas_c = tablas["costo_por_vivienda"]
    ref = ctx["costos"]["referencia"]

    def una(costo, cota, turnos="", cist=""):
        regla = "priorizado" if not turnos else "baseline"
        return _una(filas_c, costo_viaje_mxn=costo, cota=cota, regla=regla, baseline_turnos=turnos, baseline_cisternas=cist)

    filas = [["**Priorizado**", *[f"**{_pesos(una(ref, c)['costo_por_viv_dia_mxn'], 1)}**" for c in COTAS_ORDEN],
              _miles(una(ref, "min")["viajes"])]]
    for t, c in combos:
        filas.append([f"Baseline {_baseline(t, c, ctx['n_cisternas'])}",
                      *[_pesos(una(ref, cota, t, c)["costo_por_viv_dia_mxn"], 1) for cota in COTAS_ORDEN],
                      " / ".join(_miles(una(ref, cota, t, c)["viajes"]) for cota in COTAS_ORDEN)])
    prio = una(ref, "min")
    lineas = ["## 6. Costo por vivienda-día atendida", "",
              f"Decisión 07. Con el viaje de pipa a {_pesos(ref)} (precio de una pipa particular de 10,000 L en Tlaquepaque), "
              f"los {_miles(prio['viajes'])} viajes de la semana del priorizado cuestan {_pesos(prio['costo_viajes_mxn'])}. "
              "El costo por vivienda-día es el costo de los viajes usados entre las viviendas-día atendidas; un viaje vacío "
              "del baseline cuenta, porque la pipa sale igual.", ""]
    lineas += _tabla(["", "Cota mínima", "Cota máxima", "Viajes usados (mín. / máx.)"], filas)
    otros = [v for v in ctx["costos"]["valores"] if v != ref]
    if otros:
        partes = []
        for v in otros:
            vmin, vmax = (_pesos(una(v, c)["costo_por_viv_dia_mxn"], 1) for c in COTAS_ORDEN)
            cuanto = f"{vmin} con las dos cotas" if vmin == vmax else f"{vmin} con la cota mínima y {vmax} con la máxima"
            partes.append(f"con {_pesos(v)} por viaje, el priorizado sale en {cuanto}")
        lineas += ["Con otros precios: " + "; ".join(partes) + ". La razón entre el priorizado y cada baseline "
                   "no cambia con el precio, porque los viajes son los mismos.", ""]
    return lineas


DECLARAR = [
    "Toda razón «X veces el baseline» dice contra qué baseline y con qué cota. La más conservadora es la del baseline "
    "con necesidad con la cota máxima.",
    "El baseline es estilizado: los mismos viajes repartidos por turnos entre las cisternas instaladas. No es lo que hace "
    "hoy el municipio, que llena las cisternas cuando los vecinos lo reportan (`decisiones/referencias-y-prensa.md`), y de "
    "ese reparto no hay registro.",
    "La marginación no pesa en la prioridad (opción A de la decisión abierta 4 del motor). Con la cota máxima, el priorizado "
    "puede dejar sin entregas a los grupos pequeños de manzanas de AGEB «Muy alto»: la sección 4 dice cuánto.",
    "El plan de cada día se recalcula cuando cambia un supuesto: el resultado agregado es robusto, los puntos de entrega no "
    "(`datos/HALLAZGOS_sensibilidad.md`).",
    "El costo de un viaje es el precio de una pipa particular de 10,000 L en Tlaquepaque (Milenio, 16 de mayo de 2025), "
    "no el costo del municipio, que no lo publica; no se ajustó por inflación (decisión 07). El costo por vivienda-día es "
    "otra forma de leer la ventaja del priorizado: no es un ahorro de presupuesto, porque los viajes son los mismos.",
    "Las cifras usan el estado del motor de referencia; se recalculan con el de la implementación oficial.",
]


def resumen(tablas: dict, ctx: dict) -> str:
    combos = [(t, c) for t in ctx["sens"]["baseline_turnos"] for c in ctx["sens"]["baseline_cisternas"]]
    lineas = [
        "# Resultados del priorizador", "",
        "Generado por `python3 -m optimizador.analisis` según la decisión 06 "
        "(`optimizador/docs/decisiones/06-rejilla-comparador.md`). No se edita a mano: se vuelve a generar.", "",
        f"Semana del {ctx['desde']} al {ctx['hasta']}, calendario `{ctx['calendario']}`, estado del motor de referencia. "
        f"{ctx['viajes_por_dia']} viajes de pipa al día, de {ctx['hogares_por_viaje']} hogares cada uno, los mismos para el "
        "priorizado y para el baseline estilizado. Toda cifra va con la cota mínima y la máxima de viviendas sin agua, "
        "porque el Censo no cruza tinaco con cisterna.", "",
    ]
    lineas += _caso_base(tablas, ctx, combos)
    lineas += _rejilla(tablas, ctx)
    lineas += _escenarios(tablas, ctx, combos)
    lineas += _equidad(tablas)
    lineas += _cobertura(tablas)
    lineas += _costo(tablas, ctx, combos)
    lineas += ["## Lo que se declara", ""] + [f"- {d}" for d in DECLARAR] + [""]
    return "\n".join(lineas)
