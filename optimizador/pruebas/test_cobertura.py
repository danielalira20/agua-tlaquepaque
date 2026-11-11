"""Distancias, rejilla de vecinas y llenado de un viaje."""
import random
import unittest

from optimizador.priorizador.cobertura import haversine_m, llenar, vecinas_por_manzana
from optimizador.pruebas.apoyo import ubicar


class Distancias(unittest.TestCase):
    def test_sobre_un_meridiano_la_distancia_es_la_diferencia_de_posiciones(self):
        ub = ubicar({"a": 0, "b": 100, "c": 300, "d": 1000})
        self.assertAlmostEqual(haversine_m(ub["a"], ub["b"]), 100, places=4)
        self.assertAlmostEqual(haversine_m(ub["b"], ub["d"]), 900, places=4)
        self.assertAlmostEqual(haversine_m(ub["a"], ub["c"]), 300, places=4)


class Vecinas(unittest.TestCase):
    def test_la_rejilla_da_lo_mismo_que_comparar_todas_contra_todas(self):
        azar = random.Random(7)
        ub = {f"m{i:03d}": (-103.30 + azar.uniform(0, 0.03), 20.60 + azar.uniform(0, 0.03)) for i in range(300)}
        for radio in (200, 300, 500):
            vecinas = vecinas_por_manzana(ub, radio)
            for c in ub:
                fuerza_bruta = sorted(
                    (0.0 if q == c else haversine_m(ub[c], ub[q]), q)
                    for q in ub
                    if q == c or haversine_m(ub[c], ub[q]) <= radio + 1e-6
                )
                self.assertEqual([q for _, q in vecinas[c]], [q for _, q in fuerza_bruta], (radio, c))

    def test_incluye_a_la_propia_manzana_primero_y_es_simetrica(self):
        vecinas = vecinas_por_manzana(ubicar({"a": 0, "b": 250, "c": 600}), 300)
        self.assertEqual(vecinas["a"][0], (0.0, "a"))
        self.assertEqual([q for _, q in vecinas["b"]], ["b", "a"])
        self.assertEqual([q for _, q in vecinas["c"]], ["c"])

    def test_el_borde_del_radio_cuenta_como_dentro(self):
        vecinas = vecinas_por_manzana(ubicar({"a": 0, "b": 300}), 300)
        self.assertIn("b", [q for _, q in vecinas["a"]])


class Llenar(unittest.TestCase):
    def test_respeta_el_cupo_el_orden_y_salta_las_que_no_tienen_necesidad(self):
        vecinas = [(0.0, "a"), (50.0, "b"), (80.0, "c"), (90.0, "d")]
        resto = {"a": 2, "b": 0, "c": 5, "d": 9}
        peso = {"a": 1, "b": 1, "c": 2, "d": 3}
        ll = llenar(vecinas, resto, peso, 10)
        self.assertEqual(ll.entregas, (("a", 2), ("c", 5), ("d", 3)))
        self.assertEqual(ll.atendidas, 10)
        self.assertEqual(ll.ponderado, 2 + 10 + 9)
        self.assertEqual(resto, {"a": 2, "b": 0, "c": 5, "d": 9}, "llenar no modifica resto")


if __name__ == "__main__":
    unittest.main()
