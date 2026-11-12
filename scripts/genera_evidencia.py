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

Dos columnas distintas, que no hay que confundir:
  - `arbitrada`: si el artículo pasó revisión por pares (si | no | vacío si no es un artículo)
  - `verificacion`: cuánto se leyó. fuente_primaria (texto completo o archivo original) ·
    resumen_oficial (solo el resumen de PubMed o del editor) · suplemento (solo el material suplementario,
    no el artículo) · solo_resumen (resumen de búsqueda) · norma · no_verificada
Las referencias que cuentan para las 5 del formato del reporte son arbitrada = si y
verificacion = fuente_primaria.
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import genera_fixture_plan as G  # noqa: E402

COLUMNAS = ["id", "fuente", "tipo", "descripcion", "valor", "unidad", "ubicacion_calidad", "colonia", "lon", "lat",
            "archivo", "cita", "url_o_doi", "arbitrada", "verificacion", "uso", "fecha_consulta", "nota"]
CONSULTA = "2026-11-11"
URL_MAPA = "https://www.google.com/maps/d/viewer?mid=1RDUyGrhgZPHMVaRZDfdnN0RZvI8HL6U"
MAPA = ("Gobierno de San Pedro Tlaquepaque (2026). Mapa público \"CISTERNAS TLAQUEPAQUE PUB\" [Google My Maps]. "
        "Gobierno de San Pedro Tlaquepaque.")
RUBINO = ("Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C. (2019). Bacterial contamination of drinking water in "
          "Guadalajara, Mexico. International Journal of Environmental Research and Public Health, 16(1), 67.")
RUBINO_DOI = "https://doi.org/10.3390/ijerph16010067"
MATSINHE = ("Matsinhe, N. P., Juízo, D. L., & Persson, K. M. (2014). The effects of intermittent supply and household storage "
            "in the quality of drinking water in Maputo. VATTEN, 70, 51–60.")
KUMPEL14 = ("Kumpel, E., & Nelson, K. L. (2014). Mechanisms affecting water quality in an intermittent piped water supply. "
            "Environmental Science & Technology, 48(5), 2766–2775.")
KUMPEL16 = ("Kumpel, E., & Nelson, K. L. (2016). Intermittent water supply: Prevalence, practice, and microbial water quality. "
            "Environmental Science & Technology, 50(2), 542–553.")
ERCUMEN = ("Ercumen, A., Arnold, B. F., Kumpel, E., Burt, Z., Ray, I., Nelson, K., & Colford, J. M. (2015). Upgrading a piped "
           "water supply from intermittent to continuous delivery and association with waterborne illness: A matched cohort "
           "study in urban India. PLOS Medicine, 12(10), e1001892.")
TAYLOR = ("Taylor, D. D. J., Slocum, A. H., & Whittle, A. J. (2018). Analytical scaling relations to evaluate leakage and "
          "intrusion in intermittent water supply systems. PLOS ONE, 13(5), e0196887.")
SOSA = ("Sosa-Moreno, A., Lee, G. O., Trostle, J. A., Levy, K., Coloma, J., & Eisenberg, J. N. S. (2025). How water intermittency "
        "and water perceptions influence household coping strategies in northwestern Ecuador. PLOS Water, 4(9), e0000439.")
WU = ("Wu, G., Cheng, J., Yang, F., & Riaz, N. (2023). Intermittent water supply and self-rated health in rural China's karst "
      "region. Frontiers in Public Health, 11, 1054730.")
LEIFELS = ("Leifels, M., Cheng, D., Cai, J., Nadhirah, N., Mohidin, A. F., Santillan, E., Woo, Y., Hill, E., Wu, S. W., Boon, N., "
           "Favere, J., Whittle, A. J., & Wuertz, S. (2025). Biofilm detachment significantly affects biological stability of "
           "drinking water during intermittent water supply in a pilot scale water distribution system. Scientific Reports, 15, 22408.")
VAIDYA = ("Vaidya, R., Kumar, K. R. S., Mohan Kumar, M. S., & Rao, L. (2023). Chlorine degradation in continuous and intermittent "
          "drinking water supply networks. Urban Water Journal, 20(1), 60–73.")
CR_J21 = "Gómez, R. (2026, 21 de julio). Reporta Tlaquepaque inversión de más de 320 mdp para atender fallas en la red hidráulica. La Crónica de Hoy."
U_J21 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/07/21/reporta-tlaquepaque-inversion-de-mas-de-320-mdp-para-atender-fallas-en-la-red-hidraulica/"
CR_J30 = "Gómez, R. (2026, 30 de julio). Invierte Tlaquepaque 11.7 mdp en rehabilitación de pozos ante fallas en el suministro del Siapa. La Crónica de Hoy."
U_J30 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/07/30/invierte-tlaquepaque-117-mdp-en-rehabilitacion-de-pozos-ante-fallas-en-el-suministro-del-siapa/"
CR_O14 = "Gómez, R. (2026, 14 de octubre). Refuerza Tlaquepaque abasto de agua con 32 pipas ante tandeos del SIAPA. La Crónica de Hoy."
U_O14 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/10/14/refuerza-tlaquepaque-abasto-de-agua-con-32-pipas-ante-tandeos-del-siapa/"
CR_O15 = "Gómez, R. (2026, 15 de octubre). Despliega Tlaquepaque 32 pipas; coloca 60 cisternas ante tandeos del SIAPA. La Crónica de Hoy."
U_O15 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/10/15/despliega-tlaquepaque-32-pipas-coloca-60-cisternas-ante-tandeos-del-siapa/"
CR_O22 = "Gómez, R. (2026, 22 de octubre). Distribuye Tlaquepaque 5.6 millones de litros de agua ante desabasto por tandeos. La Crónica de Hoy."
U_O22 = "https://www.cronica.com.mx/jalisco/guadalajara/2026/10/22/distribuye-tlaquepaque-56-millones-de-litros-de-agua-ante-desabasto-por-tandeos"
ABIERTA = "Texto completo leído el 11-nov en PMC (acceso abierto)."
ARB_FECHAS = "Revisión por pares: el registro de PMC trae fechas de recepción y aceptación ({}). "


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
    fp, ro, sup, norma, nov = "fuente_primaria", "resumen_oficial", "suplemento", "norma", "no_verificada"
    return [
        # --- Estudio de Guadalajara (Rubino 2019): arbitrado, leido completo ---
        fila(id="E001", fuente="estudio_rubino", tipo="valor",
             descripcion="Casas con cloro residual libre dentro de 0.2 a 1.5 mg/L", valor="35", unidad="% de las casas",
             cita=RUBINO, url_o_doi=RUBINO_DOI, arbitrada="si", verificacion=fp,
             uso="Contexto de calidad del agua en Guadalajara (Anexo E)",
             nota="Es decir, 65% fuera de norma. Piloto con 51 casas, muestra por conveniencia: no es representativo. "
                  + ARB_FECHAS.format("recibido 2018-12-03, aceptado 2018-12-22") + ABIERTA),
        fila(id="E002", fuente="estudio_rubino", tipo="valor",
             descripcion="Tinacos de azotea que excedieron el límite de coliformes totales", valor="la mitad",
             unidad="de los tinacos de azotea muestreados", cita=RUBINO, url_o_doi=RUBINO_DOI, arbitrada="si",
             verificacion=fp, uso="Sustento del riesgo del agua almacenada", nota="El estudio dice 'la mitad'. No se detectó E. coli."),
        fila(id="E003", fuente="estudio_rubino", tipo="valor", descripcion="Residentes que beben agua de la llave",
             valor="7", unidad="% de los residentes", cita=RUBINO, url_o_doi=RUBINO_DOI, arbitrada="si",
             verificacion=fp, uso="Contexto"),
        fila(id="E004", fuente="estudio_rubino", tipo="valor",
             descripcion="Casas con medición inicial de cloro / con remedición a las 120 horas", valor="51 / 10",
             unidad="casas", cita=RUBINO, url_o_doi=RUBINO_DOI, arbitrada="si", verificacion=fp,
             uso="Declarar el tamaño de la muestra",
             nota="Tensión a declarar: el estudio llama 'casi ubicuo' al almacenamiento; el Censo da 13.8% a 26.5% de "
                  "viviendas sin tinaco ni cisterna en Tlaquepaque. Miden cosas distintas con alcances distintos."),
        # --- Maputo (VATTEN): leido completo, pero la revista NO es arbitrada en sentido formal ---
        fila(id="E005", fuente="literatura", tipo="valor",
             descripcion="Caída del cloro libre residual durante el almacenamiento doméstico (de 0.167 a 0.061 mg/L)",
             valor="60", unidad="%", cita=MATSINHE, arbitrada="no", verificacion=fp,
             uso="Sustento del decaimiento del cloro en tinacos. NO cuenta entre las 5 referencias arbitradas",
             nota="Corrige el 85% que venía de un resumen. La revista VATTEN dice de sí misma: 'A referee system is not applied "
                  "in the formal meaning. All manuscripts are evaluated by the editor and sometimes also by colleagues' "
                  "(tidskriftenvatten.se/?p=71, consultado el 11-nov). Los valores absolutos no son comparables con México "
                  "(el agua entraba con 0.167 mg/L); lo comparable es el patrón de decaimiento."),
        fila(id="E006", fuente="literatura", tipo="valor",
             descripcion="Tiempo de retención del agua en tinacos domésticos (Tabla 4); mediana cercana a 2 días",
             valor="0.4 a 6.3", unidad="días", cita=MATSINHE, arbitrada="no", verificacion=fp,
             uso="Sustento del umbral U = 48 h (agua guardada). No arbitrada"),
        fila(id="E007", fuente="literatura", tipo="valor",
             descripcion="Consumo por persona con que el estudio calcula la demanda", valor="120", unidad="L/persona/día",
             cita=MATSINHE, arbitrada="no", verificacion=fp,
             uso="Sensibilidad del consumo: nuestro valor base es 50 L/persona/día. No arbitrada",
             nota="A 100 L el resultado del motor se multiplica por 2.2 (datos/HALLAZGOS_zonas.md)."),
        # --- Autoridades y normas ---
        fila(id="E008", fuente="literatura", tipo="cita_textual",
             descripcion="\"Where household storage is used to overcome intermittent supply, localized use of disinfectants to "
                         "reduce microbial proliferation may be warranted.\"",
             cita="World Health Organization (2017). Guidelines for drinking-water quality: Fourth edition incorporating the "
                  "first addendum (cap. 4). World Health Organization.",
             arbitrada="no", verificacion=fp, uso="Respaldo del campo requiere_desinfeccion",
             nota="Capítulos 4 y 7 leídos completos. Autoridad, no artículo arbitrado: cuenta como complemento."),
        fila(id="E009", fuente="literatura", tipo="valor",
             descripcion="Cloro residual libre permitido en agua para consumo humano", valor="0.2 a 1.5", unidad="mg/L",
             cita="Secretaría de Salud. NOM-127-SSA1-2021.", verificacion=norma,
             uso="Contexto. El motor no modela cloro: no hay datos públicos en la llave"),
        fila(id="E010", fuente="literatura", tipo="valor",
             descripcion="Tasa de decaimiento del cloro en redes intermitentes (hierro dúctil y fundido) frente a continuas",
             valor="1.5", unidad="veces mayor", cita=VAIDYA, url_o_doi="https://doi.org/10.1080/1573062X.2022.2139275",
             arbitrada="nd", verificacion=nov,
             uso="NO USAR. DESCARTADA el 12-nov: de pago, sin material suplementario, y nada del reporte depende de ella",
             nota="Autores y datos de la revista confirmados en Crossref (en línea nov-2022; volumen 20(1), enero 2023). El "
                  "texto y el resumen no se pudieron abrir (Taylor & Francis bloquea la descarga automática): el factor 1.5 y la "
                  "frase 'se sabe muy poco' no se confirmaron. Dani confirmó el 12-nov que solo está disponible de pago y que no "
                  "tiene suplementario, y decidió descartarla. El decaimiento del cloro no se modela; el contexto lo cubren Rubino y la OMS."),
        # --- Intermitencia: arbitrados ---
        fila(id="E011", fuente="literatura", tipo="valor",
             descripcion="A presiones menores de 10 psi se detectaron con frecuencia bacterias indicadoras aun con cloro residual "
                         "(intrusión o flujo inverso); entre 10 y 17 psi, contaminación periódica; con más de 17 psi y cloro "
                         "residual, pocos coliformes totales y ningún E. coli",
             valor="10 / 17", unidad="psi", cita=KUMPEL14, url_o_doi="https://doi.org/10.1021/es405054u", arbitrada="si",
             verificacion=ro, uso="Respaldo de por qué la baja presión del racionamiento es un riesgo, no solo una molestia",
             nota="Solo se leyó el resumen oficial (PubMed 24459990, 'Indexed for MEDLINE'); el texto completo está en ACS, "
                  "que bloquea la descarga automática. Estudio en Hubli-Dharwad, India, 11 sitios: los umbrales son de esa red. "
                  "El material suplementario (leído el 12-nov, ver E021 y E022) trae las gráficas de turbidez agrupadas con las mismas "
                  "categorías de presión (menos de 10, 10 a 17 y más de 17 psi), pero no reemplaza al texto principal."),
        fila(id="E012", fuente="literatura", tipo="valor",
             descripcion="El suministro intermitente atiende al menos esta cantidad de personas en el mundo", valor="300 millones",
             unidad="personas", cita=KUMPEL16, url_o_doi="https://doi.org/10.1021/acs.est.5b03973", arbitrada="si",
             verificacion=ro, uso="Contexto: la intermitencia no es un caso aislado",
             nota="Resumen oficial (PubMed 26670120, 'Indexed for MEDLINE'). Revisión. Taylor et al. (2018) dan cerca de mil "
                  "millones de personas con redes no siempre presurizadas: son definiciones distintas, no se contradicen. Según su "
                  "material suplementario (E023), la cifra sale de una base voluntaria que excluye a muchas empresas: es una cota inferior."),
        fila(id="E013", fuente="literatura", tipo="valor",
             descripcion="Agua almacenada que no cumplía las guías, con suministro continuo frente a intermitente: la calidad "
                         "empeoró en el almacenamiento en ambos grupos",
             valor="13 / 36", unidad="% de muestras (continuo / intermitente)", cita=ERCUMEN,
             url_o_doi="https://doi.org/10.1371/journal.pmed.1001892", arbitrada="si", verificacion=fp,
             uso="Respaldo de que el almacenamiento es un punto de deterioro aunque el suministro mejore",
             nota="Hubli-Dharwad, India; cohorte pareada de 3,922 hogares. " + ARB_FECHAS.format("recibido 2014-12-31, aceptado 2015-09-17") + ABIERTA),
        fila(id="E014", fuente="literatura", tipo="valor",
             descripcion="Hogares con al menos un caso reportado de fiebre tifoidea: con suministro continuo hubo menos que con intermitente",
             valor="42", unidad="% menos (razón de incidencia acumulada 0.58; IC95% 0.41 a 0.78)", cita=ERCUMEN,
             url_o_doi="https://doi.org/10.1371/journal.pmed.1001892", arbitrada="si", verificacion=fp,
             uso="Respaldo del costo en salud de la intermitencia",
             nota="Casos reportados por el cuidador, a menudo sin confirmación de laboratorio. Estudio observacional."),
        fila(id="E015", fuente="literatura", tipo="valor",
             descripcion="Sin asociación significativa entre suministro continuo y diarrea en menores de 5 años en general "
                         "(razón de prevalencia 0.93; IC95% 0.83 a 1.04). En hogares de menores ingresos, 37% menos diarrea "
                         "con sangre (0.63; 0.46 a 0.87)",
             valor="0.93 / 0.63", unidad="razón de prevalencia", cita=ERCUMEN,
             url_o_doi="https://doi.org/10.1371/journal.pmed.1001892", arbitrada="si", verificacion=fp,
             uso="DECLARAR EL LÍMITE: la evidencia no es uniforme. No afirmar que la intermitencia causa diarrea en general",
             nota="Los autores atribuyen la falta de efecto general a la contaminación por almacenamiento y a rutas no hídricas."),
        fila(id="E016", fuente="literatura", tipo="valor",
             descripcion="El consumo municipal con suministro continuo cumplía la recomendación citada de 50 litros por persona "
                         "al día; cerca de la mitad de los hogares con suministro intermitente no llegaba a ese nivel",
             valor="50", unidad="L/persona/día", cita=ERCUMEN, url_o_doi="https://doi.org/10.1371/journal.pmed.1001892",
             arbitrada="si", verificacion=fp, uso="Respaldo de 50 L/persona/día como nivel de referencia",
             nota="Los autores lo citan de otras fuentes: es un nivel de referencia, no una medición propia de ellos."),
        fila(id="E017", fuente="literatura", tipo="valor",
             descripcion="Cada día adicional por semana sin suministro se asoció con 30% más de probabilidad de tratar el agua "
                         "doméstica (razón de momios 1.30; IC95% 1.18 a 1.41) y 18% menos de depender de varias fuentes (0.82)",
             valor="1.30 / 0.82", unidad="razón de momios", cita=SOSA, url_o_doi="https://doi.org/10.1371/journal.pwat.0000439",
             arbitrada="si", verificacion=fp,
             uso="Respaldo de medir días sin servicio por semana y del costo de afrontamiento",
             nota="Tres comunidades del noroeste de Ecuador; encuesta y entrevistas. La revista es de PLOS (revisión por pares "
                  "por política editorial); el registro de PMC no trae fechas de recepción y aceptación. " + ABIERTA),
        fila(id="E018", fuente="literatura", tipo="valor",
             descripcion="El suministro intermitente aumentó 18.2% la probabilidad de salud 'regular' y redujo 58.8% la de salud "
                         "'excelente' autopercibida; el almacenamiento y los hábitos de agua son mecanismos",
             valor="18.2 / 58.8", unidad="% de cambio en la probabilidad", cita=WU,
             url_o_doi="https://doi.org/10.3389/fpubh.2023.1054730", arbitrada="si", verificacion=fp,
             uso="Respaldo de la salud autopercibida como consecuencia; el almacenamiento como mecanismo",
             nota="641 aldeas rurales de la zona kárstica de China: contexto lejano. " + ARB_FECHAS.format("recibido 2022-09-27, aceptado 2023-01-31") + ABIERTA),
        fila(id="E019", fuente="literatura", tipo="cita_textual",
             descripcion="\"Contaminants that accumulate while IWS are depressurized are flushed into customers' homes when "
                         "these systems become pressurized.\"",
             cita=TAYLOR, url_o_doi="https://doi.org/10.1371/journal.pone.0196887", arbitrada="si", verificacion=fp,
             uso="Respaldo del riesgo al restablecerse el servicio (el 'slug' de la OMS). El motor no lo modela",
             nota="Modelo analítico, no medición de campo. " + ARB_FECHAS.format("recibido 2018-01-23, aceptado 2018-04-21") + ABIERTA),
        fila(id="E020", fuente="literatura", tipo="valor",
             descripcion="Con suministro intermitente aumentaron las células totales e intactas frente al continuo, por "
                         "desprendimiento de biopelículas al reconectar el servicio",
             valor="", unidad="", cita=LEIFELS, url_o_doi="https://doi.org/10.1038/s41598-025-03535-1", arbitrada="si",
             verificacion=fp, uso="Apoyo del mecanismo, no de magnitudes",
             nota="Experimento a escala piloto (tubería de PVC de 90 m con monocloramina, 3 corridas de 30 días), no estudio de "
                  "campo. " + ARB_FECHAS.format("recibido 2025-02-10, aceptado 2025-05-21") + ABIERTA),
        # --- Material suplementario de Kumpel y Nelson (leido completo el 12-nov; NO es el articulo) ---
        fila(id="E021", fuente="literatura", tipo="valor",
             descripcion="Encuesta de hogares en Hubli-Dharwad (n = 1,951): con tinaco de azotea; con llaves dentro de tanques que se "
                         "sumergieron el último mes; con llaves a nivel del suelo o por debajo; y, de estos últimos, los que reportaron "
                         "que la calle se inundó por encima de su llave en el último mes",
             valor="35 / 8 / 17 / 62", unidad="% de hogares", cita=KUMPEL14, url_o_doi="https://doi.org/10.1021/es405054u",
             arbitrada="si", verificacion=sup,
             uso="Ejemplo de que un tinaco o una cisterna pueden ser un punto de contaminación cruzada si la llave se sumerge",
             nota="Material suplementario (S2), no el artículo. Datos de India: el Censo no registra la posición de las llaves, "
                  "así que no se puede estimar nada igual para Tlaquepaque."),
        fila(id="E022", fuente="literatura", tipo="valor",
             descripcion="La conductividad al restablecer el servicio fue significativamente mayor en 15 de 23 ciclos de suministro "
                         "(diferencia media de 121 µS/cm), lo que sugiere intrusión de agua subterránea; en las llaves de consumidores "
                         "se registró presión menor de 0 psi justo después de cortar el suministro",
             valor="15 de 23", unidad="ciclos de suministro", cita=KUMPEL14, url_o_doi="https://doi.org/10.1021/es405054u",
             arbitrada="si", verificacion=sup, uso="Respaldo del mecanismo de intrusión cuando la red se despresuriza",
             nota="Material suplementario (S2), no el artículo. Es una red de India con suministro muy corto; en Tlaquepaque el "
                  "SIAPA habla de baja presión, no de corte total."),
        fila(id="E023", fuente="literatura", tipo="valor",
             descripcion="Una empresa se clasificó como de suministro intermitente si su continuidad promedio reportada era de menos "
                         "de 24 horas al día. Los datos de la base IBNET los envían las empresas de forma voluntaria y excluyen a muchas",
             valor="<24", unidad="horas de servicio al día (promedio)", cita=KUMPEL16,
             url_o_doi="https://doi.org/10.1021/acs.est.5b03973", arbitrada="si", verificacion=sup,
             uso="Declarar que los 300 millones de E012 son una cota inferior, y que la definición es por horas al día",
             nota="Material suplementario, no el artículo. El calendario del SIAPA se expresa en días por semana con baja presión, "
                  "no en horas al día: no es la misma definición, así que no se debe decir que Tlaquepaque 'es un sistema intermitente' "
                  "con esta referencia."),
        # --- Prensa: notas completas leidas el 11-nov ---
        fila(id="P001", fuente="prensa", tipo="contexto", descripcion="Pipas del municipio",
             valor="32", unidad="pipas", cita=CR_O15, url_o_doi=U_O15, verificacion=fp,
             uso="Parámetro pipas del priorizador (se reporta, no restringe)",
             nota="Nota completa leída. El 14-oct la alcaldesa dijo 'Llegaremos a un estado de fuerza de 32 pipas. Arrancamos la "
                  "administración con dos pipas' (" + U_O14 + "): 32 es una meta; el 21-jul el municipio operaba 24 pipas."),
        fila(id="P002", fuente="prensa", tipo="contexto",
             descripcion="\"De acuerdo con el Gobierno municipal, cada vivienda atendida recibe un promedio de 200 litros de agua. "
                         "Las pipas tienen una capacidad de 10 mil litros y pueden abastecer hasta 50 hogares por viaje.\"",
             valor="200 / 10000 / 50", unidad="litros por vivienda / litros por pipa / hogares por viaje", cita=CR_O15,
             url_o_doi=U_O15, verificacion=fp, uso="litros_por_hogar, litros_por_viaje y hogares_por_viaje del priorizador",
             nota="Nota completa leída. Son cifras del gobierno municipal, no medidas de forma independiente."),
        fila(id="P003", fuente="prensa", tipo="contexto",
             descripcion="Cisternas colocadas en puntos estratégicos de colonias como Nueva Santa María, Buenos Aires, Francisco I. "
                         "Madero, Guayabitos, Fovissste Miravalle, Centro, El Álamo, Colonial Tlaquepaque, Súper Manzana, "
                         "Infonavit Revolución, Canal 58 y Jardines del Tapatío, entre otras",
             valor="60", unidad="cisternas", cita=CR_O15, url_o_doi=U_O15, verificacion=fp,
             uso="Contexto. El mapa del municipio trae 50 registros de cisterna y 10 propuestas",
             nota="Nota completa leída. La de 22-oct repite 60 y dice que reciben 'mantenimiento permanente'."),
        fila(id="P004", fuente="prensa", tipo="contexto",
             descripcion="En nueve días: más de 5.6 millones de litros a 28,296 hogares en más de 220 colonias, mediante 565 viajes "
                         "de pipas; 405 peticiones ciudadanas",
             valor="565 / 28296 / 405", unidad="viajes / hogares / peticiones", cita=CR_O22, url_o_doi=U_O22, verificacion=fp,
             uso="viajes_por_dia = 63 (565 / 9)",
             nota="Nota completa leída (el titular dice 5.6, no 56). 565 x 50 = 28,250, casi igual a los 28,296: los 'hogares "
                  "atendidos' parecen calculados con viajes x 50. 5.6 millones / 565 = 9,911 L por viaje. La nota no dice si los "
                  "565 viajes incluyen llenar cisternas."),
        fila(id="P005", fuente="prensa", tipo="contexto",
             descripcion="\"El agua distribuida proviene de los 22 pozos ubicados en el municipio\"", valor="22",
             unidad="pozos municipales", cita=CR_O22, url_o_doi=U_O22, verificacion=fp, uso="Contexto de la fuente del agua",
             nota="Nota completa leída. El 30-ago otra nota habla de 21 pozos de extracción: la cifra varía con la nota."),
        fila(id="P006", fuente="prensa", tipo="cita_textual",
             descripcion="Gregorio Lunar Salgado, director de Agua Potable y Alcantarillado: \"Las cisternas se llenan en cuanto "
                         "recibimos el reporte de las y los vecinos. En ese momento se programa la pipa y se abastecen de inmediato "
                         "para que las familias cuenten con agua para sus necesidades básicas\"",
             cita=CR_J30, url_o_doi=U_J30, verificacion=fp,
             uso="Fuente del supuesto del baseline: un viaje a una cisterna es un viaje de pipa, y el reparto real responde a reportes",
             nota="Nota completa leída. Es la fuente que faltaba: sostiene que las pipas llenan las cisternas y que el llenado es "
                  "por demanda, por eso el baseline del priorizador es estilizado."),
        fila(id="P007", fuente="prensa", tipo="contexto",
             descripcion="El Ayuntamiento opera 24 pipas y ha instalado 55 cisternas \"con capacidad de 10 mil litros cada una\", "
                         "con las que distribuyó aproximadamente 15 millones de litros provenientes de 22 pozos",
             valor="10000", unidad="L por cisterna", cita=CR_J21, url_o_doi=U_J21, verificacion=fp,
             uso="Capacidad de la cisterna comunitaria: sostiene el supuesto de 1 viaje = 10,000 L del baseline",
             nota="Nota completa leída (21-jul). Son 55 cisternas en julio y 60 en octubre."),
        fila(id="P008", fuente="prensa", tipo="contexto",
             descripcion="Las cisternas se instalarán en las zonas con mayores dificultades de abastecimiento; las pipas harán "
                         "recorridos para llevar agua a los domicilios y llenar los depósitos de las familias",
             cita=CR_O14, url_o_doi=U_O14, verificacion=fp,
             uso="Contexto: criterio declarado de ubicación de las cisternas, y atención a domicilio",
             nota="Nota completa leída. Es una declaración de la alcaldesa, no una descripción verificada de cómo se ubicaron."),
        fila(id="P009", fuente="prensa", tipo="contexto",
             descripcion="Mapa interactivo con la ubicación de las 60 cisternas, publicado por el Ayuntamiento en esta nota",
             cita=CR_O22, url_o_doi=U_O22, verificacion=fp, uso="Confirma que el mapa de cisternas es una publicación oficial",
             nota="El enlace de la nota trae el mismo identificador mid que usa el repo."),
        fila(id="P010", fuente="prensa", tipo="contexto",
             descripcion="Las solicitudes de pipa se reciben por TlaqueChat (WhatsApp), también para vecinos de la misma cuadra o "
                         "colonia que se registren con el personal operativo", cita=CR_O15, url_o_doi=U_O15, verificacion=fp,
             uso="Contexto del canal de solicitud (criterio 5 del reto)",
             nota="Los dos números de WhatsApp que publican las notas del 15 y del 22 de octubre difieren en un dígito: no citar el número."),
        fila(id="P011", fuente="prensa", tipo="contexto",
             descripcion="Una vecina de Alfredo Barba dice que algunos proveedores particulares de pipa cobran hasta dos mil pesos",
             valor="2000", unidad="MXN (testimonio)", cita=CR_O15, url_o_doi=U_O15, verificacion=fp,
             uso="Solo como orden de magnitud para el costo privado de una pipa (criterio 5)",
             nota="Es el testimonio de una persona citada por la nota, no un dato oficial ni un precio por viaje: Jass debe buscar un costo con fuente."),
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
