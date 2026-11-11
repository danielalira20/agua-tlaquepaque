"""Forma de plan.json."""
import unittest

from optimizador.priorizador.asignacion import asignar_semana
from optimizador.priorizador.metricas import metricas_dia, metricas_semana
from optimizador.priorizador.salida import construir_plan
from optimizador.pruebas.apoyo import necesidad, parametros, ubicar


class Plan(unittest.TestCase):
    def setUp(self):
        self.p = parametros(viajes_por_dia=2)
        self.ub = ubicar({"M1": 0, "M2": 1000})
        self.ocup = {"M1": 4.0, "M2": 3.0, "M3": 5.0}
        self.estado = {
            "d1": necesidad({"M1": (30, 24), "M3": (6, 24)}),
            "d2": necesidad({"M1": (4, 48), "M2": (2, 24)}),
        }
        self.res = asignar_semana(self.estado, self.ub, self.p)
        self.por_dia = [metricas_dia(r, self.estado[r.fecha], self.ub, self.ocup, self.p) for r in self.res]
        self.semana = metricas_semana(self.res, self.estado, self.ocup, self.por_dia)

    def test_campos_de_cada_viaje(self):
        plan = construir_plan(self.p, self.res, self.por_dia, self.semana, self.ocup, {"M1": "Centro"})
        v = plan["fechas"][0]["viajes"][0]
        self.assertEqual(
            v,
            {
                "orden_eleccion": 1,
                "tipo": "pipa",
                "cvegeo_centro": "M1",
                "colonia": "Centro",
                "manzanas_cubiertas": [{"cvegeo": "M1", "viviendas": 10}],
                "viviendas_objetivo": 10,
                "litros": 2000,
                "personas_beneficiadas": 40.0,
                "prioridad_score": 10.0,
            },
        )
        self.assertEqual(plan["parametros"]["hogares_por_viaje"], 10)

    def test_la_semana_cuenta_las_manzanas_que_nunca_recibieron_agua(self):
        # M3 no tiene ubicacion: nunca puede recibir agua. M2 y M1 si reciben el dia 2.
        self.assertEqual(self.semana["manzanas_sin_entrega"], 1)
        self.assertEqual(self.semana["personas_sin_entrega"], 6 * 5.0)
        self.assertEqual(self.semana["necesidad_total"], 36 + 6)
        self.assertEqual(self.semana["viviendas_atendidas"], 20 + 6)


if __name__ == "__main__":
    unittest.main()
