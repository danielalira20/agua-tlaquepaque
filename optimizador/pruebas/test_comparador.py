"""Comparador (decision 06): rejilla por regla, equidad por grado, esquinas del motor y salida determinista."""
import ast
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from optimizador.analisis import comparador as C
from optimizador.priorizador.baseline import Cisterna, seleccionar
from optimizador.priorizador.entradas import leer_supuestos
from optimizador.priorizador.plan import correr_todo
from optimizador.pruebas.apoyo import necesidad, parametros, ubicar

RAIZ = Path(__file__).resolve().parents[2]
A, B, S = "1409800010001", "1409800010002", "1409800010003"  # la AGEB S no esta en el indice: "sin dato"
POSICIONES = {A + "001": 0, A + "002": 200, B + "001": 2000, S + "001": 5000}
SENS = {
    "modo_racha": ["desempate", "no"],
    "radio_cobertura_m": [300, 2500],
    "baseline_turnos": ["todas", "con_necesidad"],
    "baseline_cisternas": ["todas", "exactas"],
}


def mundo_chico() -> C.Mundo:
    ub = ubicar(POSICIONES)
    cisternas = [
        Cisterna("C1@municipal", "cisterna_municipal", ub[A + "001"], "exacta", "Alfa"),
        Cisterna("C2@municipal", "cisterna_municipal", ub[S + "001"], "colonia", "Sigma"),
    ]
    return C.Mundo(ub, dict.fromkeys(POSICIONES, 4.0), cisternas, [], {A: "Muy bajo", B: "Alto"})


def estados_chicos() -> dict:
    def dia(k):
        return necesidad({A + "001": (10 * k, 24), A + "002": (5 * k, 48), B + "001": (8 * k, 24), S + "001": (3 * k, 24)})

    return {"min": {"d1": dia(1), "d2": dia(1)}, "max": {"d1": dia(2), "d2": dia(2)}}


class Rejilla(unittest.TestCase):
    def test_correr_cada_regla_por_separado_da_lo_mismo_que_la_corrida_completa(self):
        mundo, estados, p = mundo_chico(), estados_chicos(), parametros(viajes_por_dia=2)
        filas = C.rejilla(estados, mundo, p, SENS)
        self.assertEqual(len(filas), 2 * 2 * 2 * 2 * 2)
        self.assertGreater(len({f["base_viv_dia"] for f in filas}), 1, "el escenario no distingue los baselines")
        for f in filas:
            pf = replace(p, modo_racha=f["modo_racha"], radio_cobertura_m=f["radio_m"],
                         baseline_turnos=f["baseline_turnos"], baseline_cisternas=f["baseline_cisternas"]).validar()
            cisternas, _ = seleccionar(mundo.cisternas, mundo.fuera, pf)
            completas = {(c.regla, c.cota_para_ordenar): c
                         for c in correr_todo(estados, mundo.ubicaciones, mundo.ocupantes, cisternas, pf)}
            esperado = C.comparar(completas["priorizado", f["cota"]], completas["baseline", f["cota"]])
            self.assertEqual({k: f[k] for k in esperado}, esperado, f)

    def test_los_valores_base_estan_en_la_rejilla(self):
        p = leer_supuestos(str(RAIZ / "optimizador" / "supuestos.json"))
        sens = C.leer_sensibilidad(str(RAIZ / "optimizador" / "supuestos.json"))
        for clave in C.CLAVES_SENSIBILIDAD:
            self.assertIn(getattr(p, clave), sens[clave], clave)

    def test_sin_baseline_no_hay_razon(self):
        self.assertIsNone(C.veces(5, 0))
        self.assertEqual(C._texto(None), "")
        self.assertEqual(C._texto(1 / 3), "0.33")


class Equidad(unittest.TestCase):
    def setUp(self):
        self.mundo, self.estados = mundo_chico(), estados_chicos()
        self.corridas = C.corridas_base(self.estados, self.mundo, parametros(viajes_por_dia=2))
        self.filas = C.equidad(self.estados, self.corridas, self.mundo)

    def test_viviendas_sin_agua_por_grado(self):
        nec = {(f["cota"], f["grado"]): f["necesidad_viv_dia"] for f in self.filas}
        self.assertEqual(nec["min", "Muy bajo"], (10 + 5) * 2)
        self.assertEqual(nec["min", "Alto"], 8 * 2)
        self.assertEqual(nec["min", "sin dato"], 3 * 2)
        self.assertEqual(nec["max", "Alto"], 16 * 2)
        self.assertNotIn(("min", "Medio"), nec, "un grado sin viviendas ni entregas no lleva renglon")

    def test_lo_atendido_por_grado_suma_lo_de_la_semana(self):
        for cota in ("min", "max"):
            for nombre, cs in self.corridas.items():
                filas = [f for f in self.filas if f["cota"] == cota]
                total = sum(f[f"{nombre}_viv_dia"] for f in filas)
                self.assertEqual(total, cs[cota].semana["viviendas_atendidas"], (cota, nombre))
                if total:
                    self.assertAlmostEqual(sum(f[f"{nombre}_pct_de_lo_atendido"] for f in filas), 100.0)

    def test_un_grado_desconocido_se_rechaza(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "imu.csv"
            ruta.write_text("CVE_AGEB,GM_2020\n1409800010001,Regular\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                C.leer_grados(str(ruta))


class Escenarios(unittest.TestCase):
    def test_las_esquinas_son_las_de_la_sensibilidad_del_motor(self):
        fuente = (RAIZ / "scripts" / "sensibilidad_orden.py").read_text(encoding="utf-8")
        (nodo,) = [n for n in ast.parse(fuente).body
                   if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "ESQUINAS" for t in n.targets)]
        de_dani = {f"esquina_{k}": (cambios, proc) for k, (cambios, proc) in ast.literal_eval(nodo.value).items()}
        escenarios = C.leer_escenarios(str(RAIZ / "optimizador" / "analisis" / "escenarios_motor.json"))
        self.assertEqual(escenarios[0], C.Escenario("base", "decision", {}))
        self.assertEqual({e.nombre: (e.cambios, e.procedencia) for e in escenarios[1:]}, de_dani)


class Salida(unittest.TestCase):
    def test_dos_corridas_escriben_archivos_identicos(self):
        mundo, estados, p = mundo_chico(), estados_chicos(), parametros(viajes_por_dia=2)
        escenarios = [C.Escenario("base", "decision", {}), C.Escenario("esquina_x", "sin_fuente", {"tinaco_l": 450})]
        estados_de = {"base": estados, "esquina_x": estados}
        ctx = {"desde": "d1", "hasta": "d2", "calendario": "prueba", "viajes_por_dia": p.viajes_por_dia,
               "hogares_por_viaje": p.hogares_por_viaje, "modo_racha": p.modo_racha, "radio": p.radio_cobertura_m,
               "sens": SENS, "escenarios": escenarios, "n_cisternas": {"todas": 2, "exactas": 1}}
        contenidos = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                rutas = C.escribir_resultados(Path(tmp), C.calcular(estados_de, escenarios, mundo, p, SENS), ctx)
                contenidos.append({r.name: r.read_bytes() for r in rutas})
        self.assertEqual(contenidos[0], contenidos[1])
        self.assertEqual(sorted(contenidos[0]), ["cobertura_diaria.csv", "equidad_marginacion.csv", "escenarios_motor.csv",
                                                 "rejilla_priorizador.csv", "resumen.md"])
        self.assertIn("comparación más conservadora", contenidos[0]["resumen.md"].decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
