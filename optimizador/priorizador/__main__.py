"""Corre el priorizador sobre un estado del motor y escribe plan.json.

Uso, desde la raiz del repo:

    python3 -m optimizador.priorizador --estado salidas/referencia.csv
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --set modo_racha=peso
    python3 -m optimizador.priorizador --estado salidas/referencia.csv --regla baseline
"""
from __future__ import annotations

import argparse
import time

from .asignacion import asignar_semana
from .baseline import asignar_semana_baseline, leer_cisternas, seleccionar, ubicar_cisternas
from .entradas import leer_estado, leer_geocolonias, leer_ocupantes, leer_supuestos, leer_ubicaciones
from .metricas import metricas_dia, metricas_semana
from .salida import construir_plan, escribir_json


def _argumentos() -> argparse.Namespace:
    a = argparse.ArgumentParser(prog="python3 -m optimizador.priorizador")
    a.add_argument("--estado", required=True, help="CSV de salida del motor")
    a.add_argument("--supuestos", default="optimizador/supuestos.json")
    a.add_argument("--ubicaciones", default="datos/manzanas_centroides.csv")
    a.add_argument("--manzanas", default="datos/manzanas_tlaquepaque.csv", help="de aqui sale ocupantes_prom")
    a.add_argument("--colonias", default="datos/manzana_colonia.csv")
    a.add_argument("--cisternas", default="datos/cisternas_tlaquepaque.csv")
    a.add_argument("--regla", choices=("priorizado", "baseline"), default="priorizado")
    a.add_argument("--salida", help="por defecto salidas/plan.json o salidas/baseline.json")
    a.add_argument("--set", action="append", default=[], metavar="CLAVE=VALOR", help="cambia un supuesto")
    return a.parse_args()


def main() -> None:
    args = _argumentos()
    cambios = dict(s.split("=", 1) for s in args.set)
    inicio = time.perf_counter()

    p = leer_supuestos(args.supuestos, cambios)
    estado = leer_estado(args.estado, p.cota_para_ordenar)
    ubicaciones = leer_ubicaciones(args.ubicaciones)
    ocupantes = leer_ocupantes(args.manzanas)
    geocolonias = leer_geocolonias(args.colonias)
    colonias = {c: nombre for c, (_, nombre) in geocolonias.items()}
    salida = args.salida or ("salidas/plan.json" if args.regla == "priorizado" else "salidas/baseline.json")

    if args.regla == "baseline":
        ubicadas, fuera = ubicar_cisternas(leer_cisternas(args.cisternas), ubicaciones, geocolonias)
        cisternas = seleccionar(ubicadas, p)
        exactas = sum(1 for c in cisternas if c.ubicacion == "exacta")
        print(f"baseline con {len(cisternas)} cisternas ({exactas} exactas, {len(cisternas) - exactas} por colonia), "
              f"turnos={p.baseline_turnos}; fuera: {', '.join(fuera) or 'ninguna'}")
        resultados = asignar_semana_baseline(estado, ubicaciones, cisternas, p)
    else:
        resultados = asignar_semana(estado, ubicaciones, p)
    por_dia = [metricas_dia(r, estado[r.fecha], ubicaciones, ocupantes, p) for r in resultados]
    semana = metricas_semana(resultados, estado, ocupantes, por_dia)
    escribir_json(salida, construir_plan(p, resultados, por_dia, semana, ocupantes, colonias))

    print(f"regla={args.regla} cota={p.cota_para_ordenar} modo_racha={p.modo_racha} radio={p.radio_cobertura_m} m "
          f"viajes={p.viajes_por_dia} x {p.hogares_por_viaje} hogares")
    print(f"{'fecha':<11}{'necesidad':>10}{'atendidas':>10}{'personas':>10}{'cobert%':>9}{'efic_viv%':>10}{'efic_pond%':>11}{'sin_usar':>9}{'vacios':>8}")
    for d in por_dia:
        print(f"{d['fecha']:<11}{d['necesidad_total']:>10}{d['viviendas_atendidas']:>10}{d['personas_atendidas']:>10.0f}"
              f"{d['cobertura_pct']:>9.1f}{d['eficiencia_viviendas_pct']:>10.1f}{d['eficiencia_ponderada_pct']:>11.1f}{d['viajes_sin_usar']:>9}{d['viajes_vacios']:>8}")
    print(f"semana: {semana['viviendas_atendidas']} viviendas-dia atendidas, {semana['personas_atendidas']:.0f} personas-dia, "
          f"{semana['manzanas_sin_entrega']} manzanas sin ninguna entrega ({semana['personas_sin_entrega']:.0f} personas)")
    print(f"escrito {salida} en {time.perf_counter() - inicio:.1f} s")


if __name__ == "__main__":
    main()
