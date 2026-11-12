#!/usr/bin/env python3
"""
Pruebas del analisis de sensibilidad del orden de las manzanas (scripts/sensibilidad_orden.py).
Necesita numpy y pandas (scripts/requirements.txt), a diferencia de test_referencia.py, que usa solo la biblioteca estandar.

    python3 motor/test_sensibilidad.py
"""
import csv
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(AQUI))
import sensibilidad_orden as S  # noqa: E402


def leer(ruta):
    with open(ruta, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class TestFuncionesDeOrden(unittest.TestCase):
    def test_spearman(self):
        a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(S.spearman(a, a), 1.0)
        self.assertAlmostEqual(S.spearman(a, a[::-1]), -1.0)
        self.assertAlmostEqual(S.spearman(a, a * 10 + 3), 1.0)          # solo importa el orden
        self.assertTrue(math.isnan(S.spearman(a, np.ones(5))))            # constante: no hay orden
        # con empates: se promedian los rangos
        self.assertAlmostEqual(S.spearman(np.array([1, 1, 2, 3.0]), np.array([1, 1, 2, 3.0])), 1.0)

    def test_top_k_solo_positivos_y_desempate_determinista(self):
        v = np.array([0.0, 5.0, 5.0, 3.0, 0.0, 5.0])
        orden = np.arange(len(v))
        self.assertEqual(list(S.top_k(v, 3, orden)), [1, 2, 5])           # empate en 5: gana el indice menor
        self.assertEqual(list(S.top_k(v, 10, orden)), [1, 2, 5, 3])       # los ceros no entran
        self.assertEqual(len(S.top_k(np.zeros(4), 2, np.arange(4))), 0)

    def test_riesgo_por_colonia_ignora_las_vacias(self):
        s = S.riesgo_por_colonia(np.array([1.0, 2.0, 4.0, 8.0]), np.array(["a", "a", "", "b"]))
        self.assertEqual(list(s.index), ["b", "a"])
        self.assertEqual(list(s.values), [8.0, 3.0])


class TestPropiedadesDelMotor(unittest.TestCase):
    """Propiedades que el motor debe cumplir sin importar los datos: si fallan, hay un error de codigo."""

    @classmethod
    def setUpClass(cls):
        cls.mundo = S.Mundo(submuestra=10)
        cls.base = S.correr(cls.mundo)

    def total(self, cambios, clave="viv_min"):
        return float(S.correr(self.mundo, cambios)[clave].sum())

    def test_el_minimo_nunca_supera_al_maximo(self):
        self.assertTrue((self.base["viv_min"] <= self.base["viv_max"]).all())
        self.assertTrue((self.base["gua_min"] <= self.base["gua_max"]).all())

    def test_monotonia_de_cada_supuesto(self):
        b = self.base["viv_min"].sum()
        for clave in ("viv_min", "viv_max"):
            consumo = [self.total({"consumo_l_persona_dia": c}, clave) for c in (50, 75, 100, 150)]
            self.assertEqual(consumo, sorted(consumo), f"mas consumo no puede dejar a menos viviendas sin agua ({clave})")
            tinaco = [self.total({"tinaco_l": t}, clave) for t in (450, 750, 1100, 2500)]
            self.assertEqual(tinaco, sorted(tinaco, reverse=True), f"un tinaco mas grande no puede dejar a mas viviendas sin agua ({clave})")
            cist = [self.total({"cisterna_l": c}, clave) for c in (2500, 5000, 10000)]
            self.assertEqual(cist, sorted(cist, reverse=True))
            horas = [self.total({"horas_efectivas_corte": h}, clave) for h in (24, 36, 48)]
            self.assertEqual(horas, sorted(horas))
            f = [self.total({"fraccion_suministro_en_racionamiento": x}, clave) for x in (0.0, 0.25, 0.5, 0.75)]
            self.assertEqual(f, sorted(f, reverse=True))
        self.assertEqual(self.total({}), b)

    def test_u_no_cambia_a_quien_se_queda_sin_agua_solo_al_agua_guardada(self):
        a, b = S.correr(self.mundo, {"u_horas_agua_guardada": 24}), S.correr(self.mundo, {"u_horas_agua_guardada": 72})
        self.assertTrue((a["viv_min"] == b["viv_min"]).all())
        self.assertTrue((a["viv_max"] == b["viv_max"]).all())
        self.assertGreater(a["gua_min"].sum(), b["gua_min"].sum())        # mas U, menos agua marcada como guardada

    def test_el_estado_base_es_el_conocido(self):
        mundo = S.Mundo(submuestra=1)
        base = S.correr(mundo)
        self.assertEqual(int(base["viv_min"].sum()), 58906)
        self.assertEqual(int(base["viv_max"].sum()), 128460)

    def test_calendario_original_deja_menos_viviendas_sin_agua_que_el_vigente(self):
        orig = S.correr(self.mundo, calendario="original")["viv_min"].sum()
        self.assertLess(orig, self.base["viv_min"].sum())


class TestCorridaRapida(unittest.TestCase):
    def test_es_determinista_y_el_base_es_perfecto(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            S.main(["--rapido", "--salida", a])
            S.main(["--rapido", "--salida", b])
            for n in ("escenarios.csv", "montecarlo.csv", "barrido_fino.csv", "manzanas_robustas.csv", "importancia.csv"):
                self.assertEqual((Path(a) / n).read_text(encoding="utf-8"), (Path(b) / n).read_text(encoding="utf-8"), n)
            base = next(f for f in leer(Path(a) / "escenarios.csv") if f["escenario"] == "base")
            self.assertEqual(float(base["rho_min"]), 1.0)
            self.assertEqual(float(base["solape_top250"]), 1.0)
            self.assertEqual(float(base["cobertura_top250"]), 1.0)
            self.assertEqual(base["orden_estable"], "True")


class TestResultadosVersionados(unittest.TestCase):
    """Los CSV de datos/sensibilidad/ (corrida completa)."""

    @classmethod
    def setUpClass(cls):
        d = RAIZ / "datos" / "sensibilidad"
        cls.esc = leer(d / "escenarios.csv")
        cls.mc = leer(d / "montecarlo.csv")
        cls.fino = leer(d / "barrido_fino.csv")
        cls.rob = leer(d / "manzanas_robustas.csv")
        cls.imp = leer(d / "importancia.csv")

    def test_estructura(self):
        self.assertEqual(len(self.esc), len(S.lista_escenarios()) + 1)   # mas el lente de la cota maxima
        self.assertEqual(self.esc[-1]["escenario"], "lente_cota_maxima")
        self.assertEqual(self.esc[0]["escenario"], "base")
        self.assertEqual(sum(1 for f in self.mc if f["familia"] == "A"), 300)
        self.assertEqual(sum(1 for f in self.mc if f["familia"] == "B"), 300)
        for f in self.esc + self.mc:
            for c in ("rho_min", "rho_max"):
                self.assertTrue(-1.0 <= float(f[c]) <= 1.0, (f.get("escenario"), c))
            for c in ("solape_top100", "solape_top250", "solape_top500", "cobertura_top250"):
                self.assertTrue(0.0 <= float(f[c]) <= 1.0 + 1e-9, (f.get("escenario"), c))

    def test_barrido_fino_incluye_el_valor_base(self):
        for param, valores in S.BARRIDO_FINO.items():
            filas = [f for f in self.fino if f["parametro"] == param]
            self.assertEqual([int(f["valor"]) for f in filas], valores)
        base = next(f for f in self.fino if f["parametro"] == "consumo_l_persona_dia" and f["valor"] == "50")
        self.assertEqual(float(base["rho_positivos_min"]), 1.0)

    def test_el_base_coincide_con_lo_conocido(self):
        base = self.esc[0]
        self.assertEqual(int(float(base["viv_dia_min"])), 58906)
        self.assertEqual(int(float(base["viv_dia_max"])), 128460)
        self.assertEqual(float(base["rho_min"]), 1.0)

    def test_sorteos_dentro_de_los_rangos_declarados(self):
        for f in self.mc:
            for p, (lo, hi) in S.MC_RANGOS[f["familia"]].items():
                self.assertTrue(lo <= float(f[f"p_{p}"]) <= hi, (f["familia"], f["sorteo"], p))
        # la familia A no toca lo que no esta en el rango de la decision 1
        a = next(f for f in self.mc if f["familia"] == "A")
        self.assertNotIn("p_cisterna_l", {k for k, v in a.items() if v != ""})

    def test_los_barridos_de_la_decision_estan_todos(self):
        nombres = {f["escenario"] for f in self.esc}
        for p, valores, proc in S.BARRIDOS:
            for v in valores:
                self.assertIn(f"{p}={v}", nombres)

    def test_manzanas_robustas(self):
        self.assertTrue(all(len(r["cvegeo"]) == 16 for r in self.rob))
        self.assertEqual(len({r["cvegeo"] for r in self.rob}), len(self.rob))
        for r in self.rob:
            for c in ("frec_top250_A", "frec_top250_B"):
                self.assertTrue(0.0 <= float(r[c]) <= 1.0, (r["cvegeo"], c))
            self.assertEqual(r["nucleo_robusto"] == "True", float(r["frec_top250_A"]) >= 0.90)
        self.assertEqual(sum(1 for r in self.rob if r["en_top250_base"] == "True"), 250)
        self.assertGreater(sum(1 for r in self.rob if r["nucleo_robusto"] == "True"), 0)
        # ordenadas de mas a menos frecuentes
        fr = [float(r["frec_top250_A"]) for r in self.rob]
        self.assertEqual(fr, sorted(fr, reverse=True))
        for f in self.mc:
            self.assertTrue(0.0 <= float(f["cobertura_nucleo"]) <= 1.0 + 1e-9)

    def test_importancia_de_los_supuestos(self):
        a = {r["parametro"]: float(r["spearman_con_rho_orden"]) for r in self.imp if r["familia"] == "A"}
        b = {r["parametro"]: float(r["spearman_con_rho_orden"]) for r in self.imp if r["familia"] == "B"}
        self.assertLess(a["consumo_l_persona_dia"], -0.5)       # mas consumo, mas desorden
        self.assertGreater(a["tinaco_l"], 0.2)                  # tinaco mas grande, mas orden
        self.assertGreater(abs(a["consumo_l_persona_dia"]), abs(a["tinaco_l"]))   # el consumo pesa mas que el tinaco en el rango de la decision 1
        # U solo cambia el agua guardada: no puede mover el orden por viviendas sin agua (lo que queda es ruido del sorteo)
        self.assertLess(abs(a["u_horas_agua_guardada"]), 0.2)
        self.assertLess(abs(b["u_horas_agua_guardada"]), 0.2)
        # lo que importa es el consumo NETO c * (1 - f): mas fraccion que sigue llegando equivale a menos consumo
        self.assertGreater(b["fraccion_suministro_en_racionamiento"], 0.3)
        self.assertLess(b["consumo_l_persona_dia"], -0.3)

    def test_los_criterios_declarados_no_cambiaron(self):
        # si alguien los mueve despues de ver los resultados, esta prueba obliga a justificarlo
        self.assertEqual((S.UMBRAL_RHO, S.UMBRAL_COBERTURA, S.UMBRAL_PRIORIZADOR, S.TOL_ZONAS_PP), (0.90, 0.90, 2.0, 10.0))


if __name__ == "__main__":
    unittest.main(verbosity=1)
