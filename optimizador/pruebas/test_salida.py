"""plan.json: forma del contrato v2 y valores de un escenario chico."""
import json
import os
import unittest

from optimizador.priorizador.plan import correr_todo
from optimizador.priorizador.salida import construir_plan
from optimizador.pruebas.apoyo import necesidad, parametros, ubicar
from optimizador.pruebas.test_baseline import cisterna

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "..", "fixtures", "plan.fixture.json")


def plan_chico():
    p = parametros(viajes_por_dia=2)
    ub = ubicar({"M1": 0, "M2": 1000, "M4": 5000})
    ocup = {"M1": 4.0, "M2": 3.0, "M3": 5.0, "M4": 2.0}
    estados = {
        "min": {"d1": necesidad({"M1": (30, 24), "M3": (6, 24)}), "d2": necesidad({"M1": (4, 48), "M2": (2, 24)})},
        "max": {"d1": necesidad({"M1": (40, 24), "M3": (6, 24)}), "d2": necesidad({"M1": (9, 48), "M2": (5, 24)})},
    }
    cis = [cisterna("C1", 0), cisterna("C2", 3000, "colonia")]
    corridas = correr_todo(estados, ub, ocup, cis, p)
    plan = construir_plan(p, corridas, cis, [("C9", "sin coordenada ni colonia")], ub, ocup, {"M1": "Centro"})
    return json.loads(json.dumps(plan))


def diferencias_de_forma(esperado, obtenido, ruta="plan"):
    """Lo que falta o cambia de tipo en `obtenido` respecto al fixture. Los campos extra se permiten."""
    if isinstance(esperado, dict):
        if not isinstance(obtenido, dict):
            return [f"{ruta}: se esperaba un objeto"]
        errores = []
        for k, v in esperado.items():
            if k == "nota_fixture":
                continue
            if k not in obtenido:
                errores.append(f"{ruta}.{k}: falta")
            else:
                errores += diferencias_de_forma(v, obtenido[k], f"{ruta}.{k}")
        return errores
    if isinstance(esperado, list):
        if not isinstance(obtenido, list):
            return [f"{ruta}: se esperaba una lista"]
        errores = []
        for i, (e, o) in enumerate(zip(esperado, obtenido)):
            errores += diferencias_de_forma(e, o, f"{ruta}[{i}]")
        return errores
    numero = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    if esperado is None:
        return [] if obtenido is None else [f"{ruta}: se esperaba null"]
    if numero(esperado):
        return [] if numero(obtenido) else [f"{ruta}: se esperaba un numero"]
    if type(esperado) is not type(obtenido):
        return [f"{ruta}: se esperaba {type(esperado).__name__}"]
    return []


class Contrato(unittest.TestCase):
    def test_la_salida_tiene_la_forma_del_fixture(self):
        with open(FIXTURE, encoding="utf-8") as f:
            fixture = json.load(f)
        plan = plan_chico()
        self.assertEqual(diferencias_de_forma(fixture, plan), [])
        self.assertEqual(
            [(c["regla"], c["cota_para_ordenar"]) for c in plan["corridas"]],
            [(c["regla"], c["cota_para_ordenar"]) for c in fixture["corridas"]],
        )


class Valores(unittest.TestCase):
    def setUp(self):
        self.plan = plan_chico()

    def test_viaje_del_priorizado(self):
        v = self.plan["corridas"][0]["fechas"][0]["viajes"][0]
        self.assertEqual(
            {k: v[k] for k in ("tipo", "punto_id", "cvegeo_centro", "colonia", "viviendas_objetivo", "litros", "personas_beneficiadas")},
            {"tipo": "pipa", "punto_id": None, "cvegeo_centro": "M1", "colonia": "Centro", "viviendas_objetivo": 10, "litros": 2000, "personas_beneficiadas": 40.0},
        )

    def test_viaje_del_baseline_apunta_a_una_cisterna(self):
        ids = {c["id"] for c in self.plan["baseline"]["cisternas"]}
        for corrida in self.plan["corridas"][1::2]:
            for fecha in corrida["fechas"]:
                for v in fecha["viajes"]:
                    self.assertEqual((v["tipo"], v["cvegeo_centro"]), ("cisterna", None))
                    self.assertIn(v["punto_id"], ids)
        self.assertEqual(self.plan["baseline"]["excluidas"], [{"id": "C9", "motivo": "sin coordenada ni colonia"}])

    def test_la_comparacion_es_priorizado_menos_baseline(self):
        for comp, (prio, base) in zip(self.plan["comparacion"], ((0, 1), (2, 3))):
            sp, sb = self.plan["corridas"][prio]["semana"], self.plan["corridas"][base]["semana"]
            v = comp["semana"]["viviendas_atendidas"]
            self.assertEqual((v["priorizado"], v["baseline"], v["diferencia"]),
                             (sp["viviendas_atendidas"], sb["viviendas_atendidas"], sp["viviendas_atendidas"] - sb["viviendas_atendidas"]))

    def test_la_semana_cuenta_las_manzanas_que_nunca_recibieron_agua(self):
        s = self.plan["corridas"][0]["semana"]
        # M3 no tiene ubicacion: nunca puede recibir agua.
        self.assertEqual((s["manzanas_sin_entrega"], s["personas_sin_entrega"]), (1, 30.0))
        self.assertEqual((s["necesidad_total"], s["viviendas_atendidas"]), (42, 26))
        self.assertIsNone(self.plan["propuesta_cisternas"])


if __name__ == "__main__":
    unittest.main()
