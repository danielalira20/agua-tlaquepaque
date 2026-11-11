#!/usr/bin/env python3
"""
Pruebas de la implementación de referencia. Los casos A a G están resueltos a mano
en motor/ESPECIFICACION.md, sección 8. Cualquier implementación nueva debe
reproducirlos.

    python3 motor/test_referencia.py
"""
import csv
import datetime as dt
import random
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import referencia as R  # noqa: E402

SUP = {"consumo_l_persona_dia": 50, "tinaco_l": 1100, "cisterna_l": 5000, "horas_efectivas_corte": 24,
       "u_horas_agua_guardada": 48, "umbral_estado_parcial_pct": 10, "umbral_estado_mayoritario_pct": 50}
VIGENTE = R.leer_json(AQUI / "calendarios" / "vigente-2026-11-03.json")["esquema"]


def calc(V, T, C, H, o=4, **cambios):
    sup = dict(SUP, **cambios)
    return R.calcular_manzana(V, T, C, o, H if isinstance(H, list) else [float(H)], sup)


class CasosResueltosAMano(unittest.TestCase):
    def test_A_sin_almacenamiento(self):
        self.assertEqual(calc(10, 0, 0, 24)[:2], (10, 10))

    def test_B_con_tinaco_aguanta(self):
        self.assertAlmostEqual(R.autonomia_h(1100, 4, 50), 132.0)
        self.assertEqual(calc(10, 10, 0, 24), (0, 0, 0, 0))

    def test_B2_agua_guardada(self):
        self.assertEqual(calc(10, 10, 0, 96), (0, 0, 10, 10))

    def test_B3_consumo_alto_agota_el_tinaco(self):
        self.assertAlmostEqual(R.autonomia_h(1100, 4, 100), 66.0)
        self.assertEqual(calc(10, 10, 0, 96, consumo_l_persona_dia=100)[:2], (10, 10))

    def test_C_manzana_mixta(self):
        sin_min, sin_max, g_min, g_max = calc(10, 6, 0, 96)
        self.assertEqual((sin_min, sin_max), (4, 4))
        self.assertEqual((g_min, g_max), (6, 6))

    def test_D_traslape_con_pendiente_cero(self):
        self.assertEqual(R.rango_ambos(10, 8, 7), (8, 7, 5, 7))
        self.assertEqual(calc(10, 8, 7, 72, consumo_l_persona_dia=100)[:2], (3, 3))

    def test_E_el_minimo_cae_en_a_max(self):
        r = calc(10, 6, 6, 72, consumo_l_persona_dia=100, tinaco_l=1000, cisterna_l=1000)
        self.assertEqual(r[:2], (4, 8))

    def test_F_cuatro_dias_seguidos_zona_4(self):
        martes = dt.date(2026, 11, 10)
        self.assertEqual(R.dia_semana(martes), "martes")
        self.assertEqual(R.horas_sin_servicio(set(VIGENTE["4"]), martes, 24), 96)

    def test_G_zona_3_no_tiene_racionamiento_el_lunes(self):
        self.assertEqual(R.horas_sin_servicio(set(VIGENTE["3"]), dt.date(2026, 11, 9), 24), 0)


class Bordes(unittest.TestCase):
    def test_sin_racionamiento_nadie_esta_sin_agua(self):
        self.assertEqual(calc(10, 0, 0, 0), (0, 0, 0, 0))

    def test_igualdad_exacta_todavia_aguanta(self):
        # aut = 132 h; con H = 132 el estrato aguanta (desigualdad estricta)
        self.assertEqual(calc(10, 10, 0, 132)[:2], (0, 0))
        self.assertEqual(calc(10, 10, 0, 133)[:2], (10, 10))

    def test_zona_con_siete_dias_es_error(self):
        with self.assertRaises(ValueError):
            R.horas_sin_servicio(set(R.DIAS), dt.date(2026, 11, 10), 24)

    def test_multizona_ensancha_el_intervalo(self):
        # lunes 9-nov: zona 4 lleva 3 dias seguidos (H = 72); zona 3 no tiene racionamiento (H = 0)
        f = dt.date(2026, 11, 9)
        H = R.horas_de_zonas(["3", "4"], VIGENTE, f, 24)
        self.assertEqual(H, [0.0, 72.0])
        self.assertEqual(calc(10, 0, 0, H)[:2], (0, 10))

    def test_fuera_del_programa(self):
        self.assertEqual(R.horas_de_zonas([], VIGENTE, dt.date(2026, 11, 10), 24), [0.0])

    def test_zona_desconocida_es_error(self):
        with self.assertRaises(ValueError):
            R.horas_de_zonas(["9"], VIGENTE, dt.date(2026, 11, 10), 24)

    def test_dato_inconsistente_se_recorta(self):
        # T mayor que V no debe producir viviendas negativas
        r = calc(10, 15, 0, 24)
        self.assertTrue(0 <= r[0] <= r[1] <= 10)

    def test_estado_umbrales(self):
        self.assertEqual(R.clasificar(9.99, SUP), "con_agua")
        self.assertEqual(R.clasificar(10.0, SUP), "quiebre_parcial")
        self.assertEqual(R.clasificar(50.0, SUP), "quiebre_parcial")
        self.assertEqual(R.clasificar(50.01, SUP), "quiebre_mayoritario")


class Propiedades(unittest.TestCase):
    def test_invariantes_en_datos_aleatorios(self):
        rnd = random.Random(2026)
        for _ in range(3000):
            V = rnd.randint(1, 80)
            T, C = rnd.randint(0, V), rnd.randint(0, V)
            o = rnd.uniform(1, 8)
            H = rnd.choice([0, 24, 48, 72, 96, 120, 168])
            sup = dict(SUP, consumo_l_persona_dia=rnd.choice([30, 50, 75, 100, 150]))
            smin, smax, gmin, gmax = R.calcular_manzana(V, T, C, o, [float(H)], sup)
            self.assertTrue(0 <= smin <= smax <= V, (V, T, C, H, smin, smax))
            self.assertTrue(0 <= gmin <= gmax <= V)
            # por cada extremo de `a`, sin agua + agua guardada no pasa de V
            for sin, guard in R.evaluar(V, T, C, o, float(H), sup):
                self.assertLessEqual(sin + guard, V)
            # los que no tienen nada siempre estan sin agua si hay racionamiento
            Tp, Cp = min(T, V), min(C, V)
            ninguno_min = V - Tp - Cp + max(0, Tp + Cp - V)
            if H > 0:
                self.assertGreaterEqual(smin, ninguno_min)

    def test_mas_consumo_nunca_reduce_las_viviendas_sin_agua(self):
        rnd = random.Random(7)
        for _ in range(1500):
            V = rnd.randint(1, 60)
            T, C = rnd.randint(0, V), rnd.randint(0, V)
            H = float(rnd.choice([24, 48, 72, 96, 120]))
            previo = (-1, -1)
            for c in (30, 50, 75, 100, 150, 250):
                smin, smax, _, _ = R.calcular_manzana(V, T, C, 3.7, [H], dict(SUP, consumo_l_persona_dia=c))
                self.assertGreaterEqual(smin, previo[0])
                self.assertGreaterEqual(smax, previo[1])
                previo = (smin, smax)

    def test_el_rango_es_exacto_comparando_con_fuerza_bruta(self):
        """Evalua TODOS los valores posibles de a, no solo los extremos."""
        rnd = random.Random(11)
        aut = lambda L, c: R.autonomia_h(L, 3.7, c)
        for _ in range(800):
            V = rnd.randint(1, 40)
            T, C = rnd.randint(0, V), rnd.randint(0, V)
            H = float(rnd.choice([24, 72, 96, 120]))
            c = rnd.choice([50, 100, 150])
            Tp, Cp, a_min, a_max = R.rango_ambos(V, T, C)
            valores = []
            for a in range(a_min, a_max + 1):
                e = {"ambos": (a, aut(6100, c)), "t": (Tp - a, aut(1100, c)), "c": (Cp - a, aut(5000, c)),
                     "n": (V - Tp - Cp + a, 0.0)}
                valores.append(sum(n for n, au in e.values() if au < H))
            smin, smax, _, _ = R.calcular_manzana(V, T, C, 3.7, [H], dict(SUP, consumo_l_persona_dia=c))
            self.assertEqual((smin, smax), (min(valores), max(valores)), (V, T, C, H, c))


class HumoDeLaLineaDeComandos(unittest.TestCase):
    def test_fixture_completo(self):
        raiz = AQUI.parent
        with tempfile.TemporaryDirectory() as d:
            salida = Path(d) / "s.csv"
            rc = R.main(["--manzanas", str(raiz / "fixtures" / "manzanas.fixture.csv"),
                         "--zonas", str(raiz / "fixtures" / "zonas.fixture.csv"),
                         "--desde", "2026-11-09", "--hasta", "2026-11-15", "--salida", str(salida)])
            self.assertEqual(rc, 0)
            with open(salida, encoding="utf-8") as fh:
                filas = list(csv.DictReader(fh))
            self.assertEqual(len(filas), 40 * 7)
            self.assertEqual(list(filas[0].keys()), R.COLUMNAS)
            self.assertTrue(all(int(f["viv_sin_agua_min"]) <= int(f["viv_sin_agua_max"]) for f in filas))


if __name__ == "__main__":
    unittest.main(verbosity=1)
