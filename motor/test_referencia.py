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


class SuministroParcial(unittest.TestCase):
    """Parámetro f: fracción del suministro normal que llega durante el racionamiento."""

    def test_H_la_mitad_del_suministro_salva_al_tinaco(self):
        self.assertEqual(calc(10, 10, 0, 96, consumo_l_persona_dia=100)[:2], (10, 10))
        self.assertAlmostEqual(R.autonomia_h(1100, 4, 100, 0.5), 132.0)
        self.assertEqual(calc(10, 10, 0, 96, consumo_l_persona_dia=100,
                              fraccion_suministro_en_racionamiento=0.5)[:2], (0, 0))

    def test_I_un_cuarto_no_alcanza(self):
        self.assertAlmostEqual(R.autonomia_h(1100, 4, 100, 0.25), 88.0)
        self.assertEqual(calc(10, 10, 0, 96, consumo_l_persona_dia=100,
                              fraccion_suministro_en_racionamiento=0.25)[:2], (10, 10))

    def test_J_sin_almacenamiento_sigue_sin_agua(self):
        self.assertEqual(calc(10, 0, 0, 24, fraccion_suministro_en_racionamiento=0.5)[:2], (10, 10))

    def test_con_f_cero_todo_queda_igual(self):
        self.assertEqual(calc(10, 6, 0, 96, fraccion_suministro_en_racionamiento=0.0), calc(10, 6, 0, 96))

    def test_f_fuera_de_rango_es_error(self):
        for malo in (1.0, 1.5, -0.1):
            with self.assertRaises(ValueError):
                calc(10, 6, 0, 96, fraccion_suministro_en_racionamiento=malo)

    def test_mas_suministro_nunca_aumenta_las_viviendas_sin_agua(self):
        rnd = random.Random(5)
        for _ in range(1500):
            V = rnd.randint(1, 60)
            T, C = rnd.randint(0, V), rnd.randint(0, V)
            H = float(rnd.choice([24, 48, 72, 96, 120]))
            previo = (10**9, 10**9)
            for f in (0.0, 0.25, 0.5, 0.75, 0.9):
                smin, smax, _, _ = R.calcular_manzana(V, T, C, 3.7, [H], dict(SUP, consumo_l_persona_dia=100,
                                                      fraccion_suministro_en_racionamiento=f))
                self.assertLessEqual(smin, previo[0])
                self.assertLessEqual(smax, previo[1])
                previo = (smin, smax)

    def test_equivale_al_consumo_neto(self):
        """c con fraccion f da lo mismo que c * (1 - f) con f = 0 (sección 5)."""
        rnd = random.Random(9)
        for _ in range(1500):
            V = rnd.randint(1, 60)
            T, C = rnd.randint(0, V), rnd.randint(0, V)
            o = rnd.uniform(1.5, 6)
            H = float(rnd.choice([24, 48, 72, 96, 120]))
            c, f = rnd.choice([50, 100, 150]), rnd.choice([0.25, 0.5])
            con_f = R.calcular_manzana(V, T, C, o, [H], dict(SUP, consumo_l_persona_dia=c,
                                                             fraccion_suministro_en_racionamiento=f))
            neto = R.calcular_manzana(V, T, C, o, [H], dict(SUP, consumo_l_persona_dia=c * (1 - f)))
            self.assertEqual(con_f, neto, (V, T, C, o, H, c, f))


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


class TestContratos(unittest.TestCase):
    """Los contratos y los fixtures no se pueden desfasar de lo que el motor escribe."""

    RAIZ = AQUI.parent

    @staticmethod
    def _json(ruta):
        import json
        with open(ruta, encoding="utf-8") as fh:
            return json.load(fh)

    def test_estado_contrato_igual_a_salida_del_motor(self):
        import json
        contrato = self._json(self.RAIZ / "contratos" / "estado.schema.json")
        self.assertEqual(list(contrato["campos"].keys()), R.COLUMNAS)
        with open(self.RAIZ / "fixtures" / "estado.fixture.csv", encoding="utf-8") as fh:
            self.assertEqual(next(csv.reader(fh)), R.COLUMNAS)

    def test_estado_fixture_se_regenera_igual(self):
        with tempfile.TemporaryDirectory() as d:
            salida = Path(d) / "s.csv"
            R.main(["--manzanas", str(self.RAIZ / "fixtures" / "manzanas.fixture.csv"),
                    "--zonas", str(self.RAIZ / "fixtures" / "zonas.fixture.csv"),
                    "--calendario", str(AQUI / "calendarios" / "vigente-2026-11-03.json"),
                    "--desde", "2026-11-09", "--hasta", "2026-11-15", "--salida", str(salida)])
            self.assertEqual(salida.read_text(encoding="utf-8"),
                             (self.RAIZ / "fixtures" / "estado.fixture.csv").read_text(encoding="utf-8"))

    def test_zonas_fixture_son_reales_y_estan_en_el_calendario(self):
        with open(self.RAIZ / "fixtures" / "zonas.fixture.csv", encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh))
        self.assertEqual([c for c in filas[0].keys()][:2], ["cvegeo", "zona"])
        for f in filas:
            self.assertEqual(len(f["cvegeo"]), 16)
            for z in R.parsear_zonas(f["zona"]):
                self.assertIn(z, VIGENTE)

    def test_calendarios_con_version_y_vigencia(self):
        for nombre in ["original-2026-10-15.json", "vigente-2026-11-03.json"]:
            cal = R.leer_json(AQUI / "calendarios" / nombre)
            for k in ["version", "vigente_desde", "vigente_hasta", "fuente", "actualizado_por_siapa", "consultado", "esquema"]:
                self.assertIn(k, cal, f"{nombre} no tiene {k}")
            for zona, dias in cal["esquema"].items():
                self.assertTrue(set(dias) <= set(R.DIAS))
                self.assertLess(len(dias), 7)


    def test_plan_fixture_cuadra_con_su_contrato(self):
        import json
        contrato = self._json(self.RAIZ / "contratos" / "plan.schema.json")
        plan = self._json(self.RAIZ / "fixtures" / "plan.fixture.json")
        self.assertEqual(set(plan.keys()) - {"nota_fixture"}, set(contrato["estructura"].keys()) - set())
        self.assertNotIn("orden_del_dia", json.dumps(plan))
        self.assertNotIn("ruta", json.dumps(list(plan.keys())))
        par = plan["parametros"]
        self.assertEqual(par["radio_cobertura_m"], 300)
        self.assertEqual(par["hogares_por_viaje"], par["litros_por_viaje"] // par["litros_por_hogar"])
        b = plan["baseline"]
        self.assertEqual(len(b["cisternas"]) + len(b["excluidas"]), 50)  # 50 cisternas; las 10 propuestas no cuentan
        self.assertEqual(sorted(e["id"] for e in b["excluidas"]), ["CIST014", "CIST021", "CIST022"])
        self.assertTrue(all(c["ubicacion"] in ("coordenada_exacta", "centro_de_colonia") for c in b["cisternas"]))
        self.assertTrue(all(-104 < c["lon"] < -103 and 20 < c["lat"] < 21 for c in b["cisternas"]))
        self.assertEqual({(c["regla"], c["cota_para_ordenar"]) for c in plan["corridas"]},
                         {("priorizado", "min"), ("priorizado", "max"), ("baseline", "min"), ("baseline", "max")})
        for corrida in plan["corridas"]:
            for dia in corrida["fechas"]:
                self.assertLessEqual(len(dia["viajes"]), par["viajes_por_dia"])
                for v in dia["viajes"]:
                    self.assertLessEqual(v["viviendas_objetivo"], par["hogares_por_viaje"])
                    self.assertEqual(v["litros"], v["viviendas_objetivo"] * par["litros_por_hogar"])
                    self.assertEqual(sum(m["viviendas"] for m in v["manzanas_cubiertas"]), v["viviendas_objetivo"])
                    self.assertEqual(v["tipo"], "pipa" if corrida["regla"] == "priorizado" else "cisterna")
                r = dia["resumen"]
                self.assertEqual(r["viviendas_atendidas"], sum(v["viviendas_objetivo"] for v in dia["viajes"]))
                self.assertLessEqual(r["viviendas_atendidas"], r["maximo_viviendas"])
                self.assertEqual(r["viajes_usados"] + r["viajes_sin_usar"], par["viajes_por_dia"])
        for c in plan["comparacion"]:
            for k, v in c["semana"].items():
                self.assertAlmostEqual(v["diferencia"], v["priorizado"] - v["baseline"], places=1, msg=k)

    def test_plan_fixture_se_regenera_igual(self):
        import subprocess
        antes = (self.RAIZ / "fixtures" / "plan.fixture.json").read_text(encoding="utf-8")
        subprocess.run([sys.executable, "-I", str(self.RAIZ / "scripts" / "genera_fixture_plan.py")], check=True,
                       capture_output=True)
        self.assertEqual((self.RAIZ / "fixtures" / "plan.fixture.json").read_text(encoding="utf-8"), antes)


    def test_cisternas_con_id_unico(self):
        with open(self.RAIZ / "datos" / "cisternas_tlaquepaque.csv", newline="", encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh))
        ids = [f["id"] for f in filas]
        self.assertEqual(len(filas), 60)
        self.assertEqual(len(ids), len(set(ids)), "hay ids de cisterna repetidos")
        self.assertEqual(sorted(f["id"] for f in filas if f["tipo"] == "cisterna_siapa"), ["SIAPA001", "SIAPA002", "SIAPA003"])
        # una fila 'coordenada_exacta' debe traer una coordenada dentro de Tlaquepaque, no un valor vacio como (-180, 90)
        for f in filas:
            if f["fuente_ubicacion"] == "coordenada_exacta":
                self.assertTrue(-104 < float(f["lon"]) < -103 and 20 < float(f["lat"]) < 21, f["id"])
        plan = self._json(self.RAIZ / "fixtures" / "plan.fixture.json")
        pid = [c["id"] for c in plan["baseline"]["cisternas"]]
        self.assertEqual(len(pid), len(set(pid)), "el baseline del plan tiene ids repetidos")


    def _csv(self, ruta):
        with open(ruta, newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))

    def test_evidencia_contrato_fixture_y_datos(self):
        contrato = self._json(self.RAIZ / "contratos" / "evidencia.schema.json")
        datos = self._csv(self.RAIZ / "datos" / "evidencia.csv")
        fixture = self._csv(self.RAIZ / "fixtures" / "evidencia.fixture.csv")
        self.assertEqual(list(datos[0].keys()), list(contrato["campos"].keys()))
        self.assertEqual(list(fixture[0].keys()), list(contrato["campos"].keys()))
        self.assertFalse((self.RAIZ / "contratos" / "mediciones.schema.json").exists())
        self.assertFalse((self.RAIZ / "fixtures" / "mediciones.fixture.csv").exists())
        ids = [d["id"] for d in datos]
        self.assertEqual(len(ids), len(set(ids)))
        por_id = {d["id"]: d for d in datos}
        for f in fixture:  # el fixture son renglones reales del registro, no inventados
            self.assertEqual(f, por_id[f["id"]], f["id"])
        fuentes = {"cisternas_municipio", "estudio_rubino", "imdec", "prensa", "literatura"}
        ver = {"fuente_primaria", "resumen_oficial", "solo_resumen", "norma", "no_verificada"}
        for d in datos:
            self.assertIn(d["fuente"], fuentes, d["id"])
            self.assertIn(d["tipo"], {"ubicacion", "valor", "cita_textual", "contexto"}, d["id"])
            self.assertIn(d["verificacion"], ver, d["id"])
            self.assertIn(d["arbitrada"], {"si", "no", "nd", ""}, d["id"])
            if d["arbitrada"] == "si":  # un articulo arbitrado se identifica por DOI y no puede estar sin leer
                self.assertTrue(d["url_o_doi"].startswith("https://doi.org/"), d["id"])
                self.assertIn(d["verificacion"], {"fuente_primaria", "resumen_oficial"}, d["id"])
            if d["verificacion"] == "resumen_oficial":
                self.assertEqual(d["arbitrada"], "si", d["id"])
            self.assertTrue(d["cita"], f"{d['id']} no tiene cita")
            if d["verificacion"] == "solo_resumen":
                self.assertTrue(d["url_o_doi"], f"{d['id']}: solo_resumen sin enlace para abrirlo")
            if d["verificacion"] == "no_verificada":
                self.assertTrue(d["nota"] or d["uso"], d["id"])

    def test_evidencia_cisternas_coinciden_con_el_baseline_del_plan(self):
        datos = self._csv(self.RAIZ / "datos" / "evidencia.csv")
        cist = [d for d in datos if d["fuente"] == "cisternas_municipio"]
        self.assertEqual(len(cist), 60)
        reales = [d for d in cist if not d["id"].startswith("PROP")]
        self.assertEqual(len(reales), 50)  # las 10 propuestas no cuentan como cobertura
        calidad = {}
        for d in reales:
            calidad[d["ubicacion_calidad"]] = calidad.get(d["ubicacion_calidad"], 0) + 1
            if d["ubicacion_calidad"] == "coordenada_exacta":
                self.assertTrue(-104 < float(d["lon"]) < -103 and 20 < float(d["lat"]) < 21, d["id"])
            else:
                self.assertEqual((d["lon"], d["lat"]), ("", ""), d["id"])
        self.assertEqual(calidad, {"coordenada_exacta": 35, "centro_de_colonia": 12, "sin_ubicar": 3})
        plan = self._json(self.RAIZ / "fixtures" / "plan.fixture.json")
        en_baseline = {c["id"] for c in plan["baseline"]["cisternas"]}
        self.assertEqual(en_baseline, {d["id"] for d in reales if d["ubicacion_calidad"] != "sin_ubicar"})
        self.assertEqual({e["id"] for e in plan["baseline"]["excluidas"]},
                         {d["id"] for d in reales if d["ubicacion_calidad"] == "sin_ubicar"})

    def test_evidencia_se_regenera_igual(self):
        import subprocess
        rutas = [self.RAIZ / "datos" / "evidencia.csv", self.RAIZ / "fixtures" / "evidencia.fixture.csv"]
        antes = [r.read_text(encoding="utf-8") for r in rutas]
        subprocess.run([sys.executable, "-I", str(self.RAIZ / "scripts" / "genera_evidencia.py")], check=True, capture_output=True)
        self.assertEqual([r.read_text(encoding="utf-8") for r in rutas], antes)


    def test_hay_al_menos_5_referencias_arbitradas_leidas(self):
        datos = self._csv(self.RAIZ / "datos" / "evidencia.csv")
        leidas = {d["cita"] for d in datos if d["arbitrada"] == "si" and d["verificacion"] == "fuente_primaria"}
        self.assertGreaterEqual(len(leidas), 5, "el formato del reporte exige al menos 5 referencias arbitradas")
        # Matsinhe (VATTEN) no es arbitrada y no debe contarse; el factor 1.5 sin verificar no se puede usar
        self.assertFalse(any("Matsinhe" in c for c in leidas))
        e010 = next(d for d in datos if d["id"] == "E010")
        self.assertEqual(e010["verificacion"], "no_verificada")
        self.assertTrue(e010["uso"].startswith("NO USAR"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
