"""Casos resueltos a mano de la seccion 10 de ESPECIFICACION.md."""
import unittest

from optimizador.priorizador.asignacion import asignar_dia, asignar_semana
from optimizador.priorizador.metricas import metricas_dia
from optimizador.pruebas.apoyo import necesidad, parametros, ubicar

OCUPANTES = {c: 4.0 for c in ("M1", "M2", "M3")}


def resolver(posiciones, valores, **cambios):
    p = parametros(**cambios)
    nec = necesidad(valores)
    ub = ubicar(posiciones)
    res = asignar_dia("d", nec, ub, p)
    return res, metricas_dia(res, nec, ub, OCUPANTES, p)


def centros(res):
    return [v.cvegeo_centro for v in res.viajes]


class CasosAMano(unittest.TestCase):
    def test_A_un_viaje_no_alcanza(self):
        res, m = resolver({"M1": 0}, {"M1": (30, 24)})
        (v,) = res.viajes
        self.assertEqual(v.cvegeo_centro, "M1")
        self.assertEqual(v.llenado.entregas, (("M1", 10),))
        self.assertEqual(v.llenado.ponderado, 10)
        self.assertEqual(m["personas_atendidas"], 40)
        self.assertEqual(v.llenado.atendidas * 200, 2000)

    def test_B_radio_tope_y_llenado_de_cerca_a_lejos(self):
        res, _ = resolver({"M1": 0, "M2": 100, "M3": 400}, {"M1": (4, 24), "M2": (3, 24), "M3": (5, 24)})
        (v,) = res.viajes
        self.assertEqual(v.cvegeo_centro, "M2")
        self.assertEqual(v.llenado.entregas, (("M2", 3), ("M1", 4), ("M3", 3)))

    def test_C_la_racha_desempata(self):
        pos, val = {"M1": 0, "M2": 1000}, {"M1": (10, 24), "M2": (10, 96)}
        self.assertEqual(centros(resolver(pos, val)[0]), ["M2"])
        self.assertEqual(centros(resolver(pos, val, modo_racha="peso")[0]), ["M2"])
        self.assertEqual(centros(resolver(pos, val, modo_racha="no")[0]), ["M1"])

    def test_D_atendidas_contra_racha(self):
        pos, val = {"M1": 0, "M2": 1000}, {"M1": (10, 24), "M2": (4, 96)}
        self.assertEqual(centros(resolver(pos, val)[0]), ["M1"])
        self.assertEqual(centros(resolver(pos, val, modo_racha="peso")[0]), ["M2"])
        self.assertEqual(centros(resolver(pos, val, modo_racha="no")[0]), ["M1"])
        for modo, esperado in (("desempate", ["M1", "M2"]), ("peso", ["M2", "M1"]), ("no", ["M1", "M2"])):
            self.assertEqual(centros(resolver(pos, val, modo_racha=modo, viajes_por_dia=2)[0]), esperado, modo)

    def test_E_varios_viajes_al_mismo_centro(self):
        res, m = resolver({"M1": 0}, {"M1": (25, 24)}, viajes_por_dia=4)
        self.assertEqual(centros(res), ["M1", "M1", "M1"])
        self.assertEqual([v.llenado.atendidas for v in res.viajes], [10, 10, 5])
        self.assertEqual(res.viajes[2].llenado.atendidas * 200, 1000)
        self.assertEqual(res.viajes_sin_usar, 1)
        self.assertEqual([v.orden_eleccion for v in res.viajes], [1, 2, 3])

    def test_F_dia_sin_racionamiento(self):
        res, m = resolver({"M1": 0, "M2": 500}, {"M1": (0, 0), "M2": (0, 0)}, viajes_por_dia=3)
        self.assertEqual(res.viajes, ())
        self.assertEqual(res.viajes_sin_usar, 3)
        self.assertEqual(m["cobertura_pct"], 0)
        self.assertEqual(m["eficiencia_viviendas_pct"], 100)
        self.assertEqual(m["eficiencia_ponderada_pct"], 100)

    def test_G_la_cota_cambia_el_orden(self):
        pos = {"M1": 0, "M2": 1000}
        res_min, _ = resolver(pos, {"M1": (2, 24), "M2": (6, 24)}, cota_para_ordenar="min")
        res_max, _ = resolver(pos, {"M1": (12, 24), "M2": (6, 24)}, cota_para_ordenar="max")
        self.assertEqual(centros(res_min), ["M2"])
        self.assertEqual(centros(res_max), ["M1"])
        self.assertEqual(res_max.viajes[0].llenado.atendidas, 10)

    def test_H_los_dias_son_independientes(self):
        p = parametros()
        estado = {"d1": necesidad({"M1": (10, 24)}), "d2": necesidad({"M1": (10, 48)})}
        d1, d2 = asignar_semana(estado, ubicar({"M1": 0}), p)
        self.assertEqual((d1.viajes[0].llenado.atendidas, d1.viajes[0].llenado.ponderado), (10, 10))
        self.assertEqual((d2.viajes[0].llenado.atendidas, d2.viajes[0].llenado.ponderado), (10, 20))

    def test_I_comparacion_contra_el_maximo(self):
        pos, val = {"M1": 0, "M2": 1000}, {"M1": (10, 24), "M2": (4, 96)}
        _, m = resolver(pos, val)
        self.assertEqual(m["maximo_viviendas"], 10)
        self.assertEqual(m["maximo_ponderado"], 22)
        self.assertAlmostEqual(m["eficiencia_viviendas_pct"], 100)
        self.assertAlmostEqual(m["eficiencia_ponderada_pct"], 100 * 10 / 22)
        _, m = resolver(pos, val, modo_racha="peso")
        self.assertAlmostEqual(m["eficiencia_viviendas_pct"], 40)
        self.assertAlmostEqual(m["eficiencia_ponderada_pct"], 100 * 16 / 22)


if __name__ == "__main__":
    unittest.main()
