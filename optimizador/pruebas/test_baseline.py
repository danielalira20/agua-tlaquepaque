"""Baseline estilizado: casos J a L de ESPECIFICACION.md y ubicacion de cisternas."""
import unittest

from optimizador.priorizador.asignacion import asignar_dia
from optimizador.priorizador.baseline import (
    Cisterna,
    asignar_dia_baseline,
    asignar_semana_baseline,
    seleccionar,
    ubicar_cisternas,
)
from optimizador.priorizador.metricas import metricas_dia
from optimizador.pruebas.apoyo import LON, necesidad, parametros, ubicar


def cisterna(id_, metros, ubicacion="exacta"):
    (punto,) = ubicar({id_: metros}).values()
    return Cisterna(id_, "cisterna_municipal", punto, ubicacion, f"colonia-{id_}")


class CasosBaseline(unittest.TestCase):
    def test_J_los_turnos_siguen_de_un_dia_al_otro(self):
        ub = ubicar({"M1": 0, "M2": 5000, "M3": 10000})
        cis = [cisterna("C1", 0), cisterna("C2", 5000), cisterna("C3", 10000)]
        estado = {f: necesidad({"M1": (30, 24), "M2": (30, 24), "M3": (30, 24)}) for f in ("d1", "d2", "d3")}
        dias = asignar_semana_baseline(estado, ub, cis, parametros(viajes_por_dia=2))
        self.assertEqual([[v.punto_id for v in d.viajes] for d in dias], [["C1", "C2"], ["C3", "C1"], ["C2", "C3"]])
        self.assertTrue(all(v.tipo == "cisterna" for d in dias for v in d.viajes))

    def test_K_viaje_sin_necesidad_en_el_radio_cuenta_vacio(self):
        ub = ubicar({"M1": 1000})
        nec = necesidad({"M1": (10, 24)})
        p = parametros()
        base = asignar_dia_baseline("d", 0, nec, ub, [cisterna("C1", 0)], p)
        self.assertEqual(base.viajes[0].llenado.atendidas, 0)
        self.assertEqual(metricas_dia(base, nec, ub, {"M1": 4.0}, p)["viajes_vacios"], 1)
        prio = asignar_dia("d", nec, ub, p)
        self.assertEqual(prio.viajes[0].llenado.atendidas, 10)

    def test_L_se_llena_desde_el_punto_de_la_cisterna(self):
        ub = ubicar({"M1": 0, "M2": 200, "M3": 400})
        nec = necesidad({"M1": (4, 24), "M2": (8, 24), "M3": (5, 24)})
        res = asignar_dia_baseline("d", 0, nec, ub, [cisterna("C1", 50)], parametros())
        self.assertEqual(res.viajes[0].llenado.entregas, (("M1", 4), ("M2", 6)))

    def test_M_con_necesidad_salta_las_cisternas_sin_viviendas_secas_cerca(self):
        ub = ubicar({"M1": 100})
        nec = necesidad({"M1": (30, 24)})
        cis = [cisterna("C1", 0), cisterna("C2", 5000)]
        todas = asignar_dia_baseline("d", 0, nec, ub, cis, parametros(viajes_por_dia=2))
        self.assertEqual([(v.punto_id, v.llenado.atendidas) for v in todas.viajes], [("C1", 10), ("C2", 0)])
        con = asignar_dia_baseline("d", 0, nec, ub, cis, parametros(viajes_por_dia=2, baseline_turnos="con_necesidad"))
        self.assertEqual([(v.punto_id, v.llenado.atendidas) for v in con.viajes], [("C1", 10), ("C1", 10)])

    def test_M_con_necesidad_sin_cisternas_activas_deja_los_viajes_sin_usar(self):
        res = asignar_dia_baseline(
            "d", 0, necesidad({"M1": (5, 24)}), ubicar({"M1": 0}), [cisterna("C1", 5000)],
            parametros(viajes_por_dia=2, baseline_turnos="con_necesidad"),
        )
        self.assertEqual((res.viajes, res.viajes_sin_usar), ((), 2))

    def test_sin_cisternas_todos_los_viajes_quedan_sin_usar(self):
        res = asignar_dia_baseline("d", 0, necesidad({"M1": (5, 24)}), ubicar({"M1": 0}), [], parametros(viajes_por_dia=3))
        self.assertEqual((res.viajes, res.viajes_sin_usar), ((), 3))


def fila(id_, fuente="sin_coordenada", lon="", lat="", capa="", geocol="", tipo="cisterna_municipal"):
    return {"id": id_, "tipo": tipo, "fuente_ubicacion": fuente, "lon": lon, "lat": lat, "colonia_capa": capa, "geocol": geocol}


class Ubicacion(unittest.TestCase):
    def setUp(self):
        self.ub = ubicar({"a1": 0, "a2": 200, "b1": 2000, "c1": 4000})
        self.geo = {"a1": ("000001", "Alfa"), "a2": ("000001", "Alfa"), "b1": ("000002", "Beta"), "c1": ("000003", "Beta")}

    def test_reglas_de_ubicacion(self):
        lat_b1 = self.ub["b1"][1]
        filas = [
            fila("C01", "coordenada_exacta", str(LON), str(lat_b1)),
            fila("C02", "coordenada_exacta", "-180.0", "90.0"),
            fila("C03", capa="Alfa", geocol="1.0"),
            fila("C04", capa="Alfa"),
            fila("C05", capa="Beta"),
            fila("C06", geocol="2.0"),
            fila("C07"),
        ]
        ubicadas, fuera = ubicar_cisternas(filas, self.ub, self.geo)
        por_id = {c.id: c for c in ubicadas}
        self.assertEqual(sorted(por_id), ["C01@municipal", "C03@municipal", "C04@municipal"])
        self.assertEqual(
            fuera,
            [
                ("C02@municipal", "coordenada fuera del municipio"),
                ("C05@municipal", "colonia ambigua"),
                ("C06@municipal", "sin coordenada ni colonia"),
                ("C07@municipal", "sin coordenada ni colonia"),
            ],
        )
        self.assertEqual(por_id["C01@municipal"].ubicacion, "exacta")
        self.assertEqual(por_id["C01@municipal"].colonia, "Beta", "sin colonia_capa, la de la manzana mas cercana")
        self.assertEqual(por_id["C03@municipal"].colonia, "Alfa")
        self.assertEqual(por_id["C03@municipal"].ubicacion, "colonia")
        self.assertAlmostEqual(por_id["C03@municipal"].punto[1], (self.ub["a1"][1] + self.ub["a2"][1]) / 2)
        self.assertEqual(por_id["C04@municipal"].punto, por_id["C03@municipal"].punto)

    def test_el_centro_de_colonia_no_depende_de_la_version_de_python(self):
        # Diez manzanas en el mismo punto: el centro debe ser ese punto, exacto. Con sum(), Python 3.10 y 3.11
        # dan 0.09999999999999999 y Python 3.12+ da 0.1; math.fsum da 0.1 en todas, y asi plan.json no cambia
        # segun quien lo genere (scripts/exporta_app.py lo compara byte por byte).
        ub = {f"g{i}": (0.1, 20.6) for i in range(10)}
        geo = {c: ("000009", "Gamma") for c in ub}
        ubicadas, fuera = ubicar_cisternas([fila("C09", capa="Gamma", geocol="9.0")], ub, geo)
        self.assertEqual(fuera, [])
        self.assertEqual(ubicadas[0].punto, (0.1, 20.6))

    def test_el_mismo_id_en_municipio_y_siapa_son_dos_cisternas(self):
        lat_a, lat_c = str(self.ub["a1"][1]), str(self.ub["c1"][1])
        filas = [
            fila("C01", "coordenada_exacta", str(LON), lat_a),
            fila("C01", "coordenada_exacta", str(LON), lat_c, tipo="cisterna_siapa"),
        ]
        ubicadas, _ = ubicar_cisternas(filas, self.ub, self.geo)
        self.assertEqual([(c.id, c.colonia) for c in ubicadas], [("C01@municipal", "Alfa"), ("C01@siapa", "Beta")])

    def test_error_si_una_cisterna_esta_repetida_con_el_mismo_tipo(self):
        with self.assertRaises(ValueError):
            ubicar_cisternas([fila("C01", capa="Alfa"), fila("C01", capa="Alfa")], self.ub, self.geo)

    def test_seleccionar_solo_exactas(self):
        cis = [cisterna("C1", 0), cisterna("C2", 100, "colonia")]
        usadas, fuera = seleccionar(cis, [("C9", "sin coordenada ni colonia")], parametros())
        self.assertEqual(([c.id for c in usadas], fuera), (["C1", "C2"], [("C9", "sin coordenada ni colonia")]))
        usadas, fuera = seleccionar(cis, [("C9", "sin coordenada ni colonia")], parametros(baseline_cisternas="exactas"))
        self.assertEqual([c.id for c in usadas], ["C1"])
        self.assertEqual([i for i, _ in fuera], ["C2", "C9"])


if __name__ == "__main__":
    unittest.main()
