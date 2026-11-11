"""Corre el priorizador y el baseline con cota minima y maxima, y escribe plan.json.

Uso, desde la raiz del repo:

    python3 -m optimizador.priorizador --estado salidas/referencia.csv
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set modo_racha=peso
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set baseline_turnos=con_necesidad --detalle
"""
from __future__ import annotations

import argparse
import time

from .baseline import leer_cisternas, seleccionar, ubicar_cisternas
from .entradas import leer_estado, leer_geocolonias, leer_ocupantes, leer_supuestos, leer_ubicaciones
from .plan import COTAS_ORDEN, correr_todo
from .salida import construir_plan, escribir_json


def _argumentos() -> argparse.Namespace:
    a = argparse.ArgumentParser(prog="python3 -m optimizador.priorizador")
    a.add_argument("--estado", required=True, help="CSV de salida del motor")
    a.add_argument("--supuestos", default="optimizador/supuestos.json")
    a.add_argument("--ubicaciones", default="datos/manzanas_centroides.csv")
    a.add_argument("--manzanas", default="datos/manzanas_tlaquepaque.csv", help="de aqui sale ocupantes_prom")
    a.add_argument("--colonias", default="datos/manzana_colonia.csv")
    a.add_argument("--cisternas", default="datos/cisternas_tlaquepaque.csv")
    a.add_argument("--salida", default="salidas/plan.json")
    a.add_argument("--set", action="append", default=[], metavar="CLAVE=VALOR", help="cambia un supuesto")
    a.add_argument("--detalle", action="store_true", help="imprime cada fecha de cada corrida")
    return a.parse_args()


def _imprimir(plan: dict, corridas, detalle: bool) -> None:
    p = plan["parametros"]
    usadas = plan["baseline"]["cisternas"]
    exactas = sum(1 for c in usadas if c["ubicacion"] == "coordenada_exacta")
    print(f"modo_racha={p['modo_racha']} radio={p['radio_cobertura_m']} m viajes={p['viajes_por_dia']} x "
          f"{p['hogares_por_viaje']} hogares | baseline: {len(usadas)} cisternas ({exactas} exactas), "
          f"turnos={p['baseline_turnos']}, fuera: {', '.join(e['id'] for e in plan['baseline']['excluidas']) or 'ninguna'}")
    print(f"{'regla':<11}{'cota':<5}{'viv-dia':>9}{'personas-dia':>14}{'cobert%':>9}{'efic_viv%':>10}{'vacios':>8}{'mzas_sin_entrega':>18}")
    for c in corridas:
        s = c.semana
        print(f"{c.regla:<11}{c.cota_para_ordenar:<5}{s['viviendas_atendidas']:>9}{s['personas_atendidas']:>14.0f}"
              f"{s['cobertura_pct']:>9.1f}{s['eficiencia_viviendas_pct']:>10.1f}{s['viajes_vacios']:>8}{s['manzanas_sin_entrega']:>18}")
        if detalle:
            for d in c.por_dia:
                print(f"    {d['fecha']} atendidas={d['viviendas_atendidas']} de {d['necesidad_total']} "
                      f"efic_pond={d['eficiencia_ponderada_pct']:.1f}% vacios={d['viajes_vacios']}")
    for comp in plan["comparacion"]:
        v = comp["semana"]["viviendas_atendidas"]
        veces = v["priorizado"] / v["baseline"] if v["baseline"] else float("inf")
        print(f"cota {comp['cota_para_ordenar']}: el priorizado atiende {v['diferencia']:+} viviendas-dia ({veces:.1f}x el baseline)")


def main() -> None:
    args = _argumentos()
    cambios = dict(s.split("=", 1) for s in args.set)
    inicio = time.perf_counter()

    p = leer_supuestos(args.supuestos, cambios)
    estados = {cota: leer_estado(args.estado, cota) for cota in COTAS_ORDEN}
    ubicaciones = leer_ubicaciones(args.ubicaciones)
    ocupantes = leer_ocupantes(args.manzanas)
    geocolonias = leer_geocolonias(args.colonias)
    colonias = {c: nombre for c, (_, nombre) in geocolonias.items()}
    ubicadas, fuera = ubicar_cisternas(leer_cisternas(args.cisternas), ubicaciones, geocolonias)
    cisternas, excluidas = seleccionar(ubicadas, fuera, p)

    corridas = correr_todo(estados, ubicaciones, ocupantes, cisternas, p)
    plan = construir_plan(p, corridas, cisternas, excluidas, ubicaciones, ocupantes, colonias)
    escribir_json(args.salida, plan)
    _imprimir(plan, corridas, args.detalle)
    print(f"escrito {args.salida} en {time.perf_counter() - inicio:.1f} s")


if __name__ == "__main__":
    main()
