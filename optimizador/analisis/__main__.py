"""Corre el comparador de la decision 06 y escribe las tablas en optimizador/resultados/.

Uso, desde la raiz del repo:

    python3 -m optimizador.analisis
    python3 -m optimizador.analisis --resultados /tmp/prueba

Corre el motor de referencia una vez por escenario de escenarios_motor.json y el priorizador como biblioteca.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import time
from dataclasses import replace
from pathlib import Path

from optimizador.priorizador.baseline import seleccionar
from optimizador.priorizador.entradas import leer_supuestos

from .comparador import calcular, cargar_mundo, escribir_resultados, leer_escenarios, leer_estados, leer_sensibilidad


def _argumentos(argv) -> argparse.Namespace:
    a = argparse.ArgumentParser(prog="python3 -m optimizador.analisis")
    a.add_argument("--desde", default="2026-11-09")
    a.add_argument("--hasta", default="2026-11-15")
    a.add_argument("--calendario", default="motor/calendarios/vigente-2026-11-03.json")
    a.add_argument("--motor", default="motor/referencia.py")
    a.add_argument("--zonas", default="datos/zonas_siapa/manzana_zona.csv")
    a.add_argument("--manzanas", default="datos/manzanas_tlaquepaque.csv")
    a.add_argument("--ubicaciones", default="datos/manzanas_centroides.csv")
    a.add_argument("--colonias", default="datos/manzana_colonia.csv")
    a.add_argument("--cisternas", default="datos/cisternas_tlaquepaque.csv")
    a.add_argument("--marginacion", default="datos/marginacion_ageb_tlaquepaque.csv")
    a.add_argument("--supuestos", default="optimizador/supuestos.json")
    a.add_argument("--escenarios", default="optimizador/analisis/escenarios_motor.json")
    a.add_argument("--resultados", default="optimizador/resultados")
    return a.parse_args(argv)


def correr_motor(args: argparse.Namespace, cambios: dict, salida: Path) -> None:
    cmd = [sys.executable, args.motor, "--manzanas", args.manzanas, "--zonas", args.zonas, "--calendario", args.calendario,
           "--desde", args.desde, "--hasta", args.hasta, "--salida", str(salida)]
    for clave, valor in cambios.items():
        cmd += ["--set", f"{clave}={valor}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"el motor fallo con {cambios or 'los supuestos base'}:\n{r.stderr}")


def main(argv=None) -> None:
    args = _argumentos(argv)
    inicio = time.perf_counter()
    p = leer_supuestos(args.supuestos)
    sens = leer_sensibilidad(args.supuestos)
    escenarios = leer_escenarios(args.escenarios)
    mundo = cargar_mundo(args.ubicaciones, args.manzanas, args.colonias, args.cisternas, args.marginacion)

    estados_de = {}
    with tempfile.TemporaryDirectory() as tmp:
        for e in escenarios:
            ruta = Path(tmp) / f"{e.nombre}.csv"
            correr_motor(args, e.cambios, ruta)
            estados_de[e.nombre] = leer_estados(str(ruta))
            print(f"motor: {e.nombre} ({time.perf_counter() - inicio:.0f} s)")

    tablas = calcular(estados_de, escenarios, mundo, p, sens)
    contexto = {
        "desde": args.desde,
        "hasta": args.hasta,
        "calendario": Path(args.calendario).stem,
        "viajes_por_dia": p.viajes_por_dia,
        "hogares_por_viaje": p.hogares_por_viaje,
        "modo_racha": p.modo_racha,
        "radio": p.radio_cobertura_m,
        "sens": sens,
        "escenarios": escenarios,
        "n_cisternas": {c: len(seleccionar(mundo.cisternas, mundo.fuera, replace(p, baseline_cisternas=c))[0])
                        for c in sens["baseline_cisternas"]},
    }
    for ruta in escribir_resultados(Path(args.resultados), tablas, contexto):
        print(f"escrito {ruta}")
    print(f"listo en {time.perf_counter() - inicio:.0f} s")


if __name__ == "__main__":
    main()
