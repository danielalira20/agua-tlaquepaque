"""Lectura de supuestos y del estado del motor."""
import json
import os
import tempfile
import unittest

from optimizador.priorizador.entradas import leer_estado, leer_supuestos

SUPUESTOS = {
    "_nota": "x",
    "pipas": 32,
    "litros_por_viaje": 10000,
    "litros_por_hogar": 200,
    "viajes_por_dia": 63,
    "radio_cobertura_m": 300,
    "cota_para_ordenar": "min",
    "modo_racha": "desempate",
    "sensibilidad": {},
}
ENCABEZADO = "cvegeo,fecha,horas_sin_servicio_min,horas_sin_servicio_max,viv_sin_agua_min,viv_sin_agua_max\n"


class Archivos(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def escribir(self, nombre, texto):
        ruta = os.path.join(self.dir.name, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        return ruta


class Supuestos(Archivos):
    def test_lee_y_deriva_hogares_por_viaje(self):
        p = leer_supuestos(self.escribir("s.json", json.dumps(SUPUESTOS)))
        self.assertEqual(p.hogares_por_viaje, 50)
        self.assertEqual(p.modo_racha, "desempate")

    def test_set_cambia_valores_con_su_tipo(self):
        p = leer_supuestos(self.escribir("s.json", json.dumps(SUPUESTOS)), {"radio_cobertura_m": "500", "modo_racha": "peso"})
        self.assertEqual((p.radio_cobertura_m, p.modo_racha), (500, "peso"))

    def test_rechaza_valores_invalidos(self):
        ruta = self.escribir("s.json", json.dumps(SUPUESTOS))
        for cambios in ({"modo_racha": "otro"}, {"cota_para_ordenar": "media"}, {"radio_cobertura_m": "0"}, {"no_existe": "1"}):
            with self.assertRaises(ValueError, msg=cambios):
                leer_supuestos(ruta, cambios)


class Estado(Archivos):
    def test_lee_la_cota_pedida_y_omite_las_manzanas_con_agua(self):
        ruta = self.escribir("e.csv", ENCABEZADO + "0001,2026-11-09,24,48,3,7\n0002,2026-11-09,0,0,0,0\n0003,2026-11-10,0,0,0,0\n")
        minimo = leer_estado(ruta, "min")
        self.assertEqual(list(minimo), ["2026-11-09", "2026-11-10"])
        self.assertEqual(minimo["2026-11-10"], {})
        self.assertEqual((minimo["2026-11-09"]["0001"].viviendas, minimo["2026-11-09"]["0001"].peso), (3, 1))
        maximo = leer_estado(ruta, "max")
        self.assertEqual((maximo["2026-11-09"]["0001"].viviendas, maximo["2026-11-09"]["0001"].peso), (7, 2))

    def test_cvegeo_se_lee_como_texto(self):
        ruta = self.escribir("e.csv", ENCABEZADO + "0001,2026-11-09,24,24,1,1\n")
        self.assertIn("0001", leer_estado(ruta, "min")["2026-11-09"])

    def test_error_si_hay_viviendas_sin_agua_y_cero_horas(self):
        ruta = self.escribir("e.csv", ENCABEZADO + "0001,2026-11-09,0,0,3,3\n")
        with self.assertRaises(ValueError):
            leer_estado(ruta, "min")

    def test_error_si_faltan_columnas(self):
        ruta = self.escribir("e.csv", "cvegeo,fecha\n0001,2026-11-09\n")
        with self.assertRaises(ValueError):
            leer_estado(ruta, "min")


if __name__ == "__main__":
    unittest.main()
