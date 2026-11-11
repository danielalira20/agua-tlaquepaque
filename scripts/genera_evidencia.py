#!/usr/bin/env python3
"""
Genera datos/evidencia.csv (el registro de evidencia propia, contrato `evidencia`) y su fixture.

    python3 scripts/genera_evidencia.py

Reemplaza a la encuesta cancelada (decisión 1). Cada renglón es una pieza de evidencia con su
procedencia y su nivel de verificación:

  - las cisternas del municipio (50 cisternas + 10 propuestas), con la calidad de su ubicación
    calculada con la MISMA regla que el baseline del priorizador (genera_fixture_plan.cisternas)
  - valores de literatura y normas, cada uno con su cita. Solo entran los que se leyeron en la
    fuente primaria o están marcados como no verificados
  - datos de prensa, marcados como "solo_resumen" mientras no se abra el artículo

La columna `verificacion` es lo que impide citar algo que no se leyó:
  fuente_primaria · solo_resumen · norma · no_verificada
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import genera_fixture_plan as G  # noqa: E402

COLUMNAS = ["id", "fuente", "tipo", "descripcion", "valor", "unidad", "ubicacion_calidad", "colonia", "lon", "lat",
            "archivo", "cita", "url_o_doi", "verificacion", "uso", "fecha_consulta", "nota"]
CONSULTA = "2026-11-11"
URL_MAPA = "https://www.google.com/maps/d/viewer?mid=1RDUyGrhgZPHMVaRZDfdnN0RZvI8HL6U"
MAPA = ("Gobierno de San Pedro Tlaquepaque (2026). Mapa público \"CISTERNAS TLAQUEPAQUE PUB\" [Google My Maps]. "
        "Gobierno de San Pedro Tlaquepaque.")
RUBINO = ("Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C. (2019). Bacterial contamination of drinking water in "
          "Guadalajara, Mexico. International Journal of Environmental Research and Public Health, 16(1), 67.")
RUBINO_DOI = "https://doi.org/10.3390/ijerph16010067"
MATSINHE = ("Matsinhe, N. P., Juízo, D. L., & Persson, K. M. (2014). The effects of intermittent supply and household storage "
            "in the quality of drinking water in Maputo. VATTEN, 70, 51–60.")
CRONICA15 = ("Crónica Jalisco (2026, 15 de octubre). Despliega Tlaquepaque 32 pipas y coloca 60 cisternas ante tandeos del SIAPA.")
URL15 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/10/15/despliega-tlaquepaque-32-pipas-coloca-60-cisternas-ante-tandeos-del-siapa/"
CRONICA22 = "Crónica Jalisco (2026, 22 de octubre). Reporte del Gobierno de Tlaquepaque sobre el abasto de agua por tandeos."
URL22 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/10/22/distribuye-tlaquepaque-56-millones-de-litros-de-agua-ante-desabasto-por-tandeos"
MILENIO = "Milenio. Tlaquepaque instala 55 cisternas públicas de agua limpia."
URLMIL = "https://www.milenio.com/comunidad/tlaquepaque-instala-55-cisternas-publicas-agua-limpia"
RESUMEN = "Solo se leyó el resumen de la búsqueda del 11-nov. Abrir el artículo antes de citarlo."


def fila(**k):
    f = {c: "" for c in COLUMNAS}
    f.update(k)
    f["fecha_consulta"] = f["fecha_consulta"] or CONSULTA
    return f


def cisternas():
    usadas, excluidas = G.cisternas()
    calidad = {c["id"]: c["ubicacion"] for c in usadas}
    for e in excluidas:
        calidad[e["id"]] = "sin_ubicar"
    filas = []
    with open(RAIZ / "datos" / "cisternas_tlaquepaque.csv", newline="", encoding="utf-8") as fh:
        for c in csv.DictReader(fh):
            prop = c["tipo"] == "propuesta_municipio"
            if prop:
                q = "coordenada_exacta" if c["lat"] else "sin_ubicar"
                desc, uso = "Ubicación propuesta por el municipio", "Contraste. No cuenta como cobertura ni entra al baseline"
            else:
                q = calidad[c["id"]]
                desc = "Cisterna comunitaria del " + ("SIAPA" if c["tipo"] == "cisterna_siapa" else "municipio")
                uso = "Contraste con el riesgo y baseline del priorizador" if q != "sin_ubicar" else "Contraste. Sin ubicar: queda fuera del baseline"
            filas.append(fila(
                id=c["id"], fuente="cisternas_municipio", tipo="ubicacion", descripcion=desc, ubicacion_calidad=q,
                colonia=c["colonia_capa"], lon=c["lon"] if q == "coordenada_exacta" else "",
                lat=c["lat"] if q == "coordenada_exacta" else "", archivo="datos/cisternas_tlaquepaque.csv",
                cita=MAPA, url_o_doi=URL_MAPA, verificacion="fuente_primaria", uso=uso,
                nota=("Revisar: ubicación inferida o incompleta" if c["revisar"] == "True" else "")))
    return filas


def literatura_y_prensa():
    return [
        fila(id="E001", fuente="estudio_rubino", tipo="valor",
             descripcion="Casas con cloro residual libre dentro de 0.2 a 1.5 mg/L", valor="35", unidad="% de las casas",
             cita=RUBINO, url_o_doi=RUBINO_DOI, verificacion="fuente_primaria",
             uso="Contexto de calidad del agua en Guadalajara (Anexo E)",
             nota="Es decir, 65% fuera de norma. Piloto con 51 casas, muestra por conveniencia: no es representativo."),
        fila(id="E002", fuente="estudio_rubino", tipo="valor",
             descripcion="Tinacos de azotea que excedieron el límite de coliformes totales", valor="la mitad",
             unidad="de los tinacos de azotea muestreados", cita=RUBINO, url_o_doi=RUBINO_DOI,
             verificacion="fuente_primaria", uso="Sustento del riesgo del agua almacenada",
             nota="El estudio dice 'la mitad'. No se detectó E. coli."),
        fila(id="E003", fuente="estudio_rubino", tipo="valor", descripcion="Residentes que beben agua de la llave",
             valor="7", unidad="% de los residentes", cita=RUBINO, url_o_doi=RUBINO_DOI,
             verificacion="fuente_primaria", uso="Contexto"),
        fila(id="E004", fuente="estudio_rubino", tipo="valor",
             descripcion="Casas con medición inicial de cloro / con remedición a las 120 horas", valor="51 / 10",
             unidad="casas", cita=RUBINO, url_o_doi=RUBINO_DOI, verificacion="fuente_primaria",
             uso="Declarar el tamaño de la muestra",
             nota="Tensión a declarar: el estudio llama 'casi ubicuo' al almacenamiento; el Censo da 13.8% a 26.5% de "
                  "viviendas sin tinaco ni cisterna en Tlaquepaque. Miden cosas distintas con alcances distintos."),
        fila(id="E005", fuente="literatura", tipo="valor",
             descripcion="Caída del cloro libre residual durante el almacenamiento doméstico (de 0.167 a 0.061 mg/L)",
             valor="60", unidad="%", cita=MATSINHE, verificacion="fuente_primaria",
             uso="Sustento del decaimiento del cloro en tinacos",
             nota="Corrige el 85% que venía de un resumen. Los valores absolutos no son comparables con México "
                  "(el agua entraba con 0.167 mg/L); lo comparable es el patrón de decaimiento. Confirmar que VATTEN es arbitrada."),
        fila(id="E006", fuente="literatura", tipo="valor",
             descripcion="Tiempo de retención del agua en tinacos domésticos (Tabla 4); mediana cercana a 2 días",
             valor="0.4 a 6.3", unidad="días", cita=MATSINHE, verificacion="fuente_primaria",
             uso="Sustento del umbral U = 48 h (agua guardada)"),
        fila(id="E007", fuente="literatura", tipo="valor",
             descripcion="Consumo por persona con que el estudio calcula la demanda", valor="120", unidad="L/persona/día",
             cita=MATSINHE, verificacion="fuente_primaria",
             uso="Sensibilidad del consumo: nuestro valor base es 50 L/persona/día",
             nota="A 100 L el resultado del motor se multiplica por 2.2 (datos/HALLAZGOS_zonas.md)."),
        fila(id="E008", fuente="literatura", tipo="cita_textual",
             descripcion="\"Where household storage is used to overcome intermittent supply, localized use of disinfectants to "
                         "reduce microbial proliferation may be warranted.\"",
             cita="World Health Organization (2017). Guidelines for drinking-water quality: Fourth edition incorporating the "
                  "first addendum (cap. 4). World Health Organization.",
             verificacion="fuente_primaria", uso="Respaldo del campo requiere_desinfeccion",
             nota="Capítulos 4 y 7 leídos completos. Autoridad, no artículo arbitrado: cuenta como complemento, no como "
                  "una de las 5 referencias arbitradas."),
        fila(id="E009", fuente="literatura", tipo="valor",
             descripcion="Cloro residual libre permitido en agua para consumo humano", valor="0.2 a 1.5", unidad="mg/L",
             cita="Secretaría de Salud. NOM-127-SSA1-2021.", verificacion="norma",
             uso="Contexto. El motor no modela cloro: no hay datos públicos en la llave"),
        fila(id="E010", fuente="literatura", tipo="valor",
             descripcion="Tasa de decaimiento del cloro en redes intermitentes (hierro dúctil y fundido) frente a continuas",
             valor="1.5", unidad="veces mayor",
             cita="Chlorine degradation in continuous and intermittent drinking water supply networks. Urban Water Journal, 20(1), 2022.",
             url_o_doi="https://doi.org/10.1080/1573062X.2022.2139275", verificacion="no_verificada",
             uso="NO USAR hasta abrir el artículo",
             nota="Viene de un resumen. Faltan los autores y confirmar el factor y la frase 'se sabe muy poco'. Si no se confirma, se quita."),
        fila(id="P001", fuente="prensa", tipo="contexto", descripcion="Pipas desplegadas por el municipio", valor="32",
             unidad="pipas", cita=CRONICA15, url_o_doi=URL15, verificacion="solo_resumen",
             uso="Parámetro pipas del priorizador (se reporta, no restringe)",
             nota=RESUMEN + " Una nota del 14 de octubre habla de 32 como meta."),
        fila(id="P002", fuente="prensa", tipo="contexto",
             descripcion="Capacidad de una pipa y hogares que abastece por viaje", valor="10000 / 50",
             unidad="litros / hogares", cita=CRONICA15, url_o_doi=URL15, verificacion="solo_resumen",
             uso="litros_por_viaje, hogares_por_viaje del priorizador (200 L por hogar es 10,000 / 50)", nota=RESUMEN),
        fila(id="P003", fuente="prensa", tipo="contexto", descripcion="Cisternas colocadas por el municipio", valor="60",
             unidad="cisternas", cita=CRONICA15, url_o_doi=URL15, verificacion="solo_resumen",
             uso="Contexto. El mapa del municipio trae 50 registros de cisterna y 10 propuestas",
             nota=RESUMEN + " Las cifras de cisternas varían según la nota (julio: 55)."),
        fila(id="P004", fuente="prensa", tipo="contexto",
             descripcion="Viajes de pipa en los primeros 9 días del operativo; hogares atendidos; solicitudes",
             valor="565 / 28296 / 405", unidad="viajes / hogares / solicitudes", cita=CRONICA22, url_o_doi=URL22,
             verificacion="solo_resumen", uso="viajes_por_dia = 63 (565 / 9)",
             nota=RESUMEN + " 565 x 50 = 28,250, casi igual a los 28,296: los 'hogares atendidos' se calculan con "
                  "viajes x 50, no se miden."),
        fila(id="P005", fuente="prensa", tipo="contexto", descripcion="Las cisternas se abastecen con agua de pozos municipales",
             valor="22", unidad="pozos municipales", cita=MILENIO, url_o_doi=URLMIL, verificacion="solo_resumen",
             uso="Supuesto: un viaje a una cisterna equivale a un viaje de pipa", nota=RESUMEN),
        fila(id="P006", fuente="prensa", tipo="contexto",
             descripcion="El llenado de las cisternas se hace conforme se reciben reportes de la ciudadanía",
             cita="Funcionario municipal citado en prensa (nota no identificada).", verificacion="no_verificada",
             uso="El baseline del priorizador es estilizado porque el reparto real responde a reportes",
             nota="Identificar la nota original antes de citar."),
    ]


def main():
    filas = cisternas() + literatura_y_prensa()
    with open(RAIZ / "datos" / "evidencia.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)
    # fixture: una cisterna de cada calidad, una del SIAPA, una propuesta, y todos los renglones que no son cisternas
    elegidas = {"CIST001", "CIST003", "CIST022", "PROP001"} | {f["id"] for f in filas if f["tipo"] != "ubicacion"}
    siapa = next(f["id"] for f in filas if f["descripcion"].endswith("SIAPA"))
    elegidas.add(siapa)
    fix = [f for f in filas if f["id"] in elegidas]
    with open(RAIZ / "fixtures" / "evidencia.fixture.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(fix)
    print(f"datos/evidencia.csv: {len(filas)} renglones; fixture: {len(fix)}")
    for q in ("coordenada_exacta", "centro_de_colonia", "sin_ubicar"):
        print(" ", q, sum(1 for f in filas if f["ubicacion_calidad"] == q and not f["id"].startswith("PROP")))


if __name__ == "__main__":
    main()
