// Fuente unica del cuerpo del reporte cientifico. De aqui salen el .docx (genera_reporte.js) y el conteo de palabras.
// Marcas dentro del texto: **negrita**, *cursiva*. Los campos entre corchetes de la portada estan POR COMPLETAR.
// Limite del formato oficial: 1,500 a 2,000 palabras en total (portada, titulos y bibliografia incluidos); resumen de 300 a 450.

const POR_COMPLETAR = "[por completar]";

module.exports = {
  portada: {
    concurso: "Hackathon Jalisco Internacional 2026",
    reto: "Reto 01 · Ciudades Inteligentes",
    titulo: "Aguanta: quién se queda sin agua en el racionamiento de Tlaquepaque y a dónde enviar las pipas",
    campos: [
      ["Número de proyecto", POR_COMPLETAR],
      ["Autores", "Daniela Lira, [nombre completo de Jass], [nombre completo de Magui], [nombre completo de Migue]"],
      ["Asesor", POR_COMPLETAR],
      ["Escuela", POR_COMPLETAR],
      ["Nivel", POR_COMPLETAR],
      ["Categoría", POR_COMPLETAR],
      ["Sede", POR_COMPLETAR],
    ],
    logo: "", // el logotipo es una imagen: no cuenta palabras
  },

  resumen: [
    "Cuando el SIAPA raciona el agua, el mismo corte no pega igual en todas las casas: la que tiene tinaco o cisterna resiste varios días; la que no, se queda sin agua desde el primero. Los indicadores oficiales no ven esa diferencia porque miden la conexión a la red: en San Pedro Tlaquepaque solo 0.57% de los ocupantes carece de agua entubada (CONAPO, 2021), pero entre 13.8% y 26.5% de las viviendas no tiene tinaco ni cisterna (INEGI, 2021), la proporción más alta de los cuatro municipios con calendario de racionamiento.",
    "**Aguanta** es un prototipo funcional que convierte esos datos públicos en decisiones. Su motor cruza el Censo 2020 de 4,871 manzanas con el calendario oficial del SIAPA y calcula, por manzana y por día, cuántas viviendas agotan su reserva. Su priorizador dirige los viajes de pipa que el municipio ya realiza hacia donde más viviendas están sin agua. Una aplicación web lo entrega a las familias y a la coordinación municipal de pipas.",
    "En la semana del 9 al 15 de noviembre de 2026, en las colonias dentro del programa, el modelo estima entre 58,906 y 128,460 viviendas-día sin agua, bajo el supuesto de corte total. Con los mismos 441 viajes semanales, el reparto priorizado atiende 22,050 viviendas-día: de 2.2 a 4.9 veces lo que logra un reparto por turnos entre las cisternas instaladas, y de 1.4 a 3.1 veces frente a una referencia más exigente. No requiere una sola pipa adicional.",
    "Cada cifra se reporta con cota mínima y máxima, porque el Censo no cruza tinaco con cisterna. La sensibilidad, con 36 escenarios y 600 simulaciones, mostró que el orden exacto de las manzanas depende de los supuestos, pero que un núcleo de 186 permanece entre las más críticas en al menos 90% de ellas. El motor se verificó con dos implementaciones independientes que coinciden en 34,097 de 34,097 resultados, y todo el análisis es reproducible.",
  ],

  figura1: {
    archivo: "figuras/figura1_prototipo.png",
    pie: "**Figura 1.** El prototipo con datos reales: Mi casa, Mapa de hoy y Plan de pipas.",
  },

  secciones: [
    { titulo: "1. Introducción", nivel: 1, parrafos: [] },
    { titulo: "1.1 Justificación", nivel: 2, parrafos: [
      "Desde el 15 de octubre de 2026, el SIAPA rota el suministro de más de 600 colonias metropolitanas en siete zonas; el calendario vigente desde el 3 de noviembre deja a algunas con rachas de cuatro días seguidos (Anexo B). El organismo lo describe como baja de presión, pero para una vivienda sin dónde guardar agua el efecto es inmediato. El municipio responde con pipas y cisternas comunitarias que se llenan cuando los vecinos reportan: reacciona, no anticipa.",
    ] },
    { titulo: "1.2 Problema", nivel: 2, parrafos: [
      "En Tlaquepaque, entre 21,775 y 41,879 viviendas (13.8% a 26.5%) carecen de tinaco y cisterna: de 77,618 a 157,259 personas sin reserva. Es la proporción más alta de los cuatro municipios del calendario en ambas cotas (Guadalajara: 3.1% a 9.3%), aunque el rango de Tonalá se traslapa. Hoy no se sabe qué manzanas se quedan sin agua cada día ni a dónde enviar primero las pipas.",
      "**Delimitación.** Colonias de Tlaquepaque dentro del programa (zonas 3 a 6): 462,194 habitantes, 78.6% del municipio (62.6% con respaldo de la lista oficial; Anexo B). **Usuarios:** las familias y la coordinación municipal de pipas. **Indicador:** viviendas-día y personas-día sin agua por semana.",
    ] },
    { titulo: "1.3 Hipótesis", nivel: 2, parrafos: [
      "Durante el racionamiento, la falta de agua se concentra en las viviendas sin almacenamiento, que los indicadores de cobertura no distinguen; dirigir los mismos viajes de pipa hacia donde más viviendas agotan su reserva atiende a más viviendas que repartirlos por turnos entre las cisternas instaladas.",
    ] },
    { titulo: "1.4 Objetivos", nivel: 2, parrafos: [
      "**General.** Estimar, por manzana y por día, cuántas viviendas se quedan sin agua durante el racionamiento y priorizar con ello el reparto de pipas.",
      "**Específicos.** Caracterizar el riesgo con datos oficiales; construir y verificar el motor y el priorizador; medir su ventaja y su sensibilidad; entregar un prototipo y evaluar su viabilidad municipal.",
    ] },

    { titulo: "2. Contexto teórico", nivel: 1, parrafos: [
      "Cuando la red pierde presión, los contaminantes acumulados entran a las casas al restablecerse el servicio (Taylor et al., 2018). El agua guardada también se deteriora: en una cohorte de India, 36% de las muestras de agua almacenada incumplía las guías con suministro intermitente, contra 13% con continuo, y hubo más hogares con tifoidea, aunque sin diferencia significativa en diarrea (Ercumen et al., 2015). En Guadalajara, 65% de las casas de un estudio piloto tenía el cloro residual fuera de norma y la mitad de los tinacos excedió el límite de coliformes (Rubino et al., 2019). La intermitencia reduce la salud autopercibida (Wu et al., 2023) y cada día adicional sin servicio por semana obliga a los hogares a adaptarse (Sosa-Moreno et al., 2025). De ahí las dos salidas del modelo: quién se queda sin agua y quién debe desinfectar la que guardó.",
    ] },

    { titulo: "3. Metodología", nivel: 1, parrafos: [
      "**Datos.** Dos datasets del catálogo del reto: el Censo 2020 por manzana (INEGI, 2021), con viviendas, ocupantes, tinaco y cisterna, y los índices de marginación (CONAPO, 2021). Se complementan con el calendario y las zonas del portal del SIAPA y el mapa municipal de cisternas (Anexo B).",
      "**Motor de autonomía.** Cada manzana se divide en estratos según tenga tinaco, cisterna, ambos o nada. La autonomía de un estrato es su volumen entre el consumo de sus ocupantes; si dura menos que las horas acumuladas sin servicio, sus viviendas se quedan sin agua ese día. Como el Censo no cruza tinaco con cisterna, cada resultado es un intervalo entre una cota mínima y una máxima. El caso base supone 50 L por persona al día, tinaco de 1,100 L, cisterna de 5,000 L y cero suministro en día de racionamiento: la cota alta del daño, no una medición. También marca las viviendas con agua guardada más de 48 horas, que conviene desinfectar.",
      "**Priorizador.** Un algoritmo voraz asigna cada uno de los 63 viajes diarios (10,000 L; 200 L por hogar) al punto que cubre más viviendas sin agua en un radio de 300 m. Se compara con una referencia estilizada: los mismos viajes repartidos por turnos entre las 47 cisternas instaladas que pudieron ubicarse.",
      "**Verificación.** El motor tiene dos implementaciones independientes (Python y TypeScript) que coinciden en 34,097 de 34,097 resultados, y 109 pruebas automáticas. La sensibilidad combina 36 escenarios y 600 simulaciones Monte Carlo sobre consumo, capacidad, horas de corte y suministro residual (Anexo D). El modelo se contrastó con las cisternas que el municipio ya instaló (Anexo E).",
      "Convergen tres áreas: ciencia de datos, ingeniería hidráulica y salud pública (Anexo C). El Anexo F describe el prototipo y lo que simula; el Anexo G, el uso de inteligencia artificial.",
    ] },

    { titulo: "4. Resultados", nivel: 1, parrafos: [
      "**El riesgo que el índice no ve.** Dentro del programa, entre 17,420 y 34,429 viviendas no tienen dónde guardar agua. El grado de marginación que más concentra es «muy bajo» (50.2% con la cota mínima; 32.8% con la máxima): el índice oficial no las señala. Las zonas 5 y 6 reúnen entre 63.0% y 72.6%.",
      "**Quién se queda sin agua.** En la semana del 9 al 15 de noviembre, el modelo estima entre 58,906 y 128,460 viviendas-día sin agua (210 mil a 490 mil personas-día); el cambio de calendario del 3 de noviembre multiplicó las personas-día por 1.5. El orden exacto de las manzanas no resiste el cambio de supuestos (correlación de rangos mediana de 0.65), pero un núcleo de 186 manzanas (3.8% del total) concentra 54% de las viviendas-día sin agua y permanece entre las 250 más críticas en al menos 90% de las simulaciones. El Sauz es la primera colonia en todas y no tiene cisterna instalada ni propuesta. Las colonias con cisterna municipal ocupan lugares de mayor riesgo (mediana: 37) que las demás (59): el modelo coincide con el criterio municipal y señala lo que falta.",
    ] },
    { figura: { archivo: "figuras/figura2_reparto.png", pie: "**Figura 2.** Viviendas-día atendidas en la semana con los mismos 441 viajes." } },
    { parrafos: [
      "**Las mismas pipas, más viviendas.** Con 441 viajes, el reparto priorizado atiende 22,050 viviendas-día; el reparto por turnos, entre 4,532 y 10,177 (Figura 2): una ventaja de 2.2 a 4.9 veces. Frente a una referencia más exigente, que solo visita cisternas con necesidad ese día, es de 1.4 a 3.1, y en el escenario más adverso baja a 1.1. A precio de pipa particular (1,200 pesos por viaje), cada vivienda-día atendida cuesta 24 pesos, contra 33 a 117. Aun así, las pipas alcanzan cada día para entre 16% y 41% de las viviendas sin agua.",
    ] },

    { titulo: "5. Análisis y discusiones", nivel: 1, parrafos: [
      "Tres rasgos distinguen a Aguanta de un mapa de riesgo convencional. **Anticipa:** parte del calendario oficial, no de reportes. **Declara su incertidumbre:** cada cifra lleva dos cotas y se sabe qué conclusiones resisten otros supuestos. **Está verificado:** dos motores independientes, pruebas automáticas y contraste con decisiones reales del municipio.",
      "La ventaja depende de la referencia y del escenario: si casi todo el municipio se queda sin agua, cualquier reparto encuentra a quién atender. La marginación no pesa en la prioridad, y tiene un costo: con la cota máxima, las AGEB de marginación «muy alta» no reciben viajes, aunque «alta» y «muy alta» juntas reciben más que con turnos.",
      "**Viabilidad.** La propuesta no pide más pipas ni licencias: usa datos gratuitos, calcula el plan semanal en segundos y se publica como sitio estático. Una semana del operativo a precio de mercado (529,200 pesos) equivale a cerca de 0.02% del presupuesto municipal de 2026 (Anexo H). La adoptaría, con capacitación, la coordinación que ya opera las pipas.",
      "**Límites.** La referencia es estilizada, porque no hay registro público del reparto real; las capacidades de almacenamiento son supuestos y el Censo es de 2020.",
    ] },
    { titulo: "5.1 Trabajo a futuro", nivel: 2, parrafos: [
      "Con la bitácora de viajes y los reportes vecinales del municipio se contrastaría el reparto real, se evaluaría ponderar la marginación y se extendería el modelo a los otros tres municipios del calendario.",
    ] },

    { titulo: "6. Conclusión", nivel: 1, parrafos: [
      "El racionamiento no se reparte parejo: se concentra en las viviendas sin tinaco ni cisterna, que los indicadores de cobertura no distinguen. Con dos datasets oficiales y el calendario del SIAPA, Aguanta lo anticipa por manzana y por día, y muestra que las mismas pipas pueden atender de 1.4 a 4.9 veces las viviendas de un reparto de referencia. La hipótesis se sostiene en todos los escenarios probados, con menor ventaja cuando el desabasto es general. Cada cifra declara su incertidumbre y puede reproducirse.",
    ] },
  ],

  bibliografia: [
    "Consejo Nacional de Población. (2021). *Índices de marginación 2020* [Conjunto de datos]. CONAPO. https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372",
    "Ercumen, A., Arnold, B. F., Kumpel, E., Burt, Z., Ray, I., Nelson, K., & Colford, J. M. (2015). Upgrading a piped water supply from intermittent to continuous delivery and association with waterborne illness: A matched cohort study in urban India. *PLOS Medicine, 12*(10), e1001892. https://doi.org/10.1371/journal.pmed.1001892",
    "Instituto Nacional de Estadística y Geografía. (2021). *Censo de Población y Vivienda 2020: Principales resultados por AGEB y manzana urbana* [Conjunto de datos]. INEGI. https://www.inegi.org.mx/programas/ccpv/2020/",
    "Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C. (2019). Bacterial contamination of drinking water in Guadalajara, Mexico. *International Journal of Environmental Research and Public Health, 16*(1), 67. https://doi.org/10.3390/ijerph16010067",
    "Sosa-Moreno, A., Lee, G. O., Trostle, J. A., Levy, K., Coloma, J., & Eisenberg, J. N. S. (2025). How water intermittency and water perceptions influence household coping strategies in northwestern Ecuador. *PLOS Water, 4*(9), e0000439. https://doi.org/10.1371/journal.pwat.0000439",
    "Taylor, D. D. J., Slocum, A. H., & Whittle, A. J. (2018). Analytical scaling relations to evaluate leakage and intrusion in intermittent water supply systems. *PLOS ONE, 13*(5), e0196887. https://doi.org/10.1371/journal.pone.0196887",
    "Wu, G., Cheng, J., Yang, F., & Riaz, N. (2023). Intermittent water supply and self-rated health in rural China's karst region. *Frontiers in Public Health, 11*, 1054730. https://doi.org/10.3389/fpubh.2023.1054730",
  ],
};
