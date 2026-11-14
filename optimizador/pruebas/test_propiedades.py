"""Propiedades que deben cumplirse en cualquier escenario, con datos al azar."""
import random
import unittest

from optimizador.priorizador.asignacion import asignar_dia
from optimizador.priorizador.cobertura import haversine_m
from optimizador.priorizador.metricas import metricas_dia
from optimizador.pruebas.apoyo import necesidad, parametros


def escenario(semilla: int):
    azar = random.Random(semilla)
    n = azar.randint(1, 60)
    ub = {f"m{i:02d}": (-103.30 + azar.uniform(0, 0.012), 20.60 + azar.uniform(0, 0.012)) for i in range(n)}
    val = {c: (azar.choice([0, 0, 1, 3, 8, 15, 40]), azar.choice([24, 48, 72, 96])) for c in ub}
    sin_ubicacion = {"x01": (azar.randint(0, 20), 24)}
    return ub, necesidad({**val, **sin_ubicacion})


class Propiedades(unittest.TestCase):
    def test_invariantes(self):
        for semilla in range(40):
            ub, nec = escenario(semilla)
            for modo in ("desempate", "peso", "no"):
                p = parametros(viajes_por_dia=random.Random(semilla).randint(0, 12), modo_racha=modo, radio_cobertura_m=400)
                res = asignar_dia("d", nec, ub, p)
                ctx = (semilla, modo)
                self.assertEqual(len(res.viajes) + res.viajes_sin_usar, p.viajes_por_dia, ctx)

                entregado = {}
                for v in res.viajes:
                    self.assertGreater(v.llenado.atendidas, 0, ctx)
                    self.assertLessEqual(v.llenado.atendidas, p.hogares_por_viaje, ctx)
                    for m, n in v.llenado.entregas:
                        self.assertIn(m, ub, ctx)
                        self.assertLessEqual(haversine_m(ub[v.cvegeo_centro], ub[m]), p.radio_cobertura_m + 1e-6, ctx)
                        entregado[m] = entregado.get(m, 0) + n
                for m, total in entregado.items():
                    self.assertLessEqual(total, nec[m].viviendas, ctx)

                if res.viajes_sin_usar:
                    alcanzable = sum(n.viviendas for c, n in nec.items() if c in ub)
                    self.assertEqual(sum(entregado.values()), alcanzable, ctx)

                m = metricas_dia(res, nec, ub, {c: 4.0 for c in nec}, p)
                self.assertLessEqual(m["eficiencia_viviendas_pct"], 100 + 1e-9, ctx)
                self.assertLessEqual(m["eficiencia_ponderada_pct"], 100 + 1e-9, ctx)
                self.assertEqual(asignar_dia("d", nec, ub, p), res, "determinista")


if __name__ == "__main__":
    unittest.main()
