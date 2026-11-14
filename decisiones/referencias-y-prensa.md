# Referencias arbitradas y notas de prensa: lo que se verificó

Revisión del 11 de noviembre de 2026. Cierra los dos pendientes que dejaba la auditoría del kit:
tener al menos 5 referencias arbitradas bien definidas, y confirmar las notas de prensa de las que
sale el supuesto de los viajes de pipa.

El registro completo, renglón por renglón, está en `datos/evidencia.csv` (contrato
`contratos/evidencia.schema.json`). Este documento lo explica.

## 0. Resumen

| | Antes | Ahora |
|---|---|---|
| Referencias arbitradas **leídas completas** | 1 (Rubino) y una dudosa (Matsinhe) | **6**: Rubino, Ercumen, Taylor, Sosa-Moreno, Wu y Leifels |
| Arbitradas con resumen oficial | 0 | 2: Kumpel y Nelson 2014 y 2016. Además se leyó el **material suplementario** de ambas (no son los artículos) |
| Matsinhe 2014 (Maputo) | "confirmar que sea arbitrada" | **No es arbitrada.** La revista lo dice de sí misma. Sigue siendo citable, pero no cuenta entre las 5 |
| Chlorine degradation (*Urban Water Journal*) | Sin autores, "viene de un resumen" | Autores y datos confirmados. El texto y el resumen siguen sin abrirse y el artículo es **solo de pago**: **descartada** (decisión de Dani, 12-nov) |
| Notas de prensa leídas completas | 0 (solo resúmenes de búsqueda) | 6 de La Crónica de Hoy (21-jul, 30-jul, 30-ago, 14-oct, 15-oct y 22-oct). La de Milenio no se pudo abrir |
| ¿Las pipas rellenan las cisternas? | Sin fuente | **Sí, con cita textual de un funcionario** (sección 3) |

## 1. Las referencias arbitradas

### Cómo se verificó cada cosa

- **Datos bibliográficos** (autores, revista, volumen, páginas, año): Crossref y el XML de PubMed
  Central. No salen de memoria.
- **Que sea arbitrada:** las fechas de *recibido* y *aceptado* que el propio registro de PMC trae
  de cada artículo, o la indexación en MEDLINE. Para VATTEN, su propia página de política.
- **Cuánto se leyó:** texto completo en XML de PMC (acceso abierto), o solo el resumen oficial de
  PubMed. ACS, Taylor & Francis, MDPI y Milenio bloquean la descarga automática y **no se esquivó**.

### Las que cuentan (arbitradas, leídas completas)

| Referencia (APA) | Revisión por pares | Qué sostiene | Límite que hay que declarar |
|---|---|---|---|
| Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C. (2019). Bacterial contamination of drinking water in Guadalajara, Mexico. *International Journal of Environmental Research and Public Health, 16*(1), 67. https://doi.org/10.3390/ijerph16010067 | Recibido 3-dic-2018, aceptado 22-dic-2018 | **Es la local.** Solo 35% de las casas tenía cloro dentro de 0.2 a 1.5 mg/L (65% fuera de norma); la mitad de los tinacos de azotea excedió el límite de coliformes; 7% bebe de la llave; no se detectó *E. coli* | Piloto con 51 casas, muestra por conveniencia. No es representativo |
| Ercumen, A., Arnold, B. F., Kumpel, E., Burt, Z., Ray, I., Nelson, K., & Colford, J. M. (2015). Upgrading a piped water supply from intermittent to continuous delivery and association with waterborne illness: A matched cohort study in urban India. *PLOS Medicine, 12*(10), e1001892. https://doi.org/10.1371/journal.pmed.1001892 | Recibido 31-dic-2014, aceptado 17-sep-2015 | 3,922 hogares. El agua almacenada empeoró en ambos grupos (13% fuera de guía con suministro continuo, 36% con intermitente). 42% menos hogares con tifoidea con suministro continuo. Cita el nivel de 50 L/persona/día como referencia | **Sin asociación significativa con la diarrea en general** (razón de prevalencia 0.93). Solo en hogares de menores ingresos hubo 37% menos diarrea con sangre. Casos reportados por el cuidador. Observacional |
| Taylor, D. D. J., Slocum, A. H., & Whittle, A. J. (2018). Analytical scaling relations to evaluate leakage and intrusion in intermittent water supply systems. *PLOS ONE, 13*(5), e0196887. https://doi.org/10.1371/journal.pone.0196887 | Recibido 23-ene-2018, aceptado 21-abr-2018 | "Contaminants that accumulate while IWS are depressurized are flushed into customers' homes when these systems become pressurized": respalda el "slug" de la OMS | Modelo analítico, no medición de campo |
| Sosa-Moreno, A., Lee, G. O., Trostle, J. A., Levy, K., Coloma, J., & Eisenberg, J. N. S. (2025). How water intermittency and water perceptions influence household coping strategies in northwestern Ecuador. *PLOS Water, 4*(9), e0000439. https://doi.org/10.1371/journal.pwat.0000439 | Revista de PLOS; el registro de PMC no trae fechas | Cada día adicional por semana sin suministro: 30% más de probabilidad de tratar el agua (razón de momios 1.30) y 18% menos de depender de varias fuentes. Respalda medir **días sin servicio por semana** | Tres comunidades de Ecuador |
| Wu, G., Cheng, J., Yang, F., & Riaz, N. (2023). Intermittent water supply and self-rated health in rural China's karst region. *Frontiers in Public Health, 11*, 1054730. https://doi.org/10.3389/fpubh.2023.1054730 | Recibido 27-sep-2022, aceptado 31-ene-2023 | La intermitencia reduce la salud autopercibida y el almacenamiento es un mecanismo | 641 aldeas rurales de China: contexto lejano |
| Leifels, M., Cheng, D., Cai, J., Nadhirah, N., Mohidin, A. F., Santillan, E., Woo, Y., Hill, E., Wu, S. W., Boon, N., Favere, J., Whittle, A. J., & Wuertz, S. (2025). Biofilm detachment significantly affects biological stability of drinking water during intermittent water supply in a pilot scale water distribution system. *Scientific Reports, 15*, 22408. https://doi.org/10.1038/s41598-025-03535-1 | Recibido 10-feb-2025, aceptado 21-may-2025 | Con suministro intermitente se desprenden biopelículas al reconectar el servicio | Experimento piloto con monocloramina, no estudio de campo. Apoya el mecanismo, no las magnitudes |

### Arbitradas, pero solo con resumen oficial

| Referencia | Qué dice su resumen | Cómo citarla |
|---|---|---|
| Kumpel, E., & Nelson, K. L. (2014). Mechanisms affecting water quality in an intermittent piped water supply. *Environmental Science & Technology, 48*(5), 2766–2775. https://doi.org/10.1021/es405054u | Con menos de 10 psi se detectaron bacterias indicadoras con frecuencia **aun con cloro residual**; entre 10 y 17 psi, contaminación periódica; con más de 17 psi y cloro, pocos coliformes totales y ningún *E. coli* | Solo por lo que el resumen dice. Los umbrales son de una red en Hubli-Dharwad, India. Es lo que respalda que la baja presión del racionamiento sea un riesgo |
| Kumpel, E., & Nelson, K. L. (2016). Intermittent water supply: Prevalence, practice, and microbial water quality. *Environmental Science & Technology, 50*(2), 542–553. https://doi.org/10.1021/acs.est.5b03973 | El suministro intermitente atiende "al menos 300 millones de personas" | Contexto. Taylor y colaboradores dan cerca de mil millones con una definición más amplia: no se contradicen |

Los dos están indexados en MEDLINE. **Los artículos son de pago y no se pudieron conseguir.** Lo que sí se
leyó completo el 12-nov es su **material suplementario** (*Supporting Information*), que no es el artículo y por eso
no sube su nivel a "leído completo" (en el registro, verificación `suplemento`). Aporta tres datos citables, siempre
indicando que vienen del suplemento:

| Dato | Registro | Límite |
|---|---|---|
| Kumpel 2014: de 1,951 hogares encuestados en Hubli-Dharwad, 35% tenía tinaco de azotea; 8% tenía llaves dentro de tanques sumergidos el último mes; 17% tenía llaves a nivel del suelo o por debajo, y 62% de ellos reportó que la calle se inundó por encima de su llave | E021 | India. El Censo no registra la posición de las llaves |
| Kumpel 2014: la conductividad al restablecer el servicio fue mayor en 15 de 23 ciclos (121 µS/cm de diferencia media), lo que sugiere intrusión de agua subterránea; presión menor de 0 psi en las llaves justo después de cortar el suministro | E022 | Red de India con suministro muy corto; en Tlaquepaque el SIAPA habla de baja presión, no de corte total |
| Kumpel 2016: una empresa es "intermitente" si su continuidad promedio es menor de **24 horas al día**; la base IBNET es voluntaria y excluye a muchas empresas, así que los 300 millones son una **cota inferior** | E023 | La definición es por horas al día; el calendario del SIAPA es por días a la semana. No decir que Tlaquepaque "es un sistema intermitente" con esta referencia |

Una advertencia de lectura: los 300 millones y los umbrales de 10 y 17 psi siguen respaldados solo por el
resumen oficial. El suplemento de 2014 trae las gráficas de turbidez agrupadas con esas mismas categorías de presión,
pero no reemplaza al texto principal.

### Las que NO cuentan, y por qué

| Referencia | Estado |
|---|---|
| Matsinhe, N. P., Juízo, D. L., & Persson, K. M. (2014). VATTEN, *70*, 51–60 | **No arbitrada.** La página de VATTEN dice: *"A referee system is not applied in the formal meaning. All manuscripts are evaluated by the editor and sometimes also by colleagues."* Se leyó completa y sus datos son buenos (caída de 60% del cloro, retención de 0.4 a 6.3 días, consumo de 120 L), pero se cita como fuente científica, no como arbitrada |
| Vaidya, R., Kumar, K. R. S., Mohan Kumar, M. S., & Rao, L. (2023). Chlorine degradation in continuous and intermittent drinking water supply networks. *Urban Water Journal, 20*(1), 60–73 | Datos confirmados en Crossref (en línea nov-2022; número de enero 2023). **No se pudo abrir ni el resumen** (Taylor & Francis bloquea) y el artículo es **solo de pago** (confirmado por Dani el 12-nov). El factor 1.5 y la frase "se sabe muy poco" **siguen sin confirmar y no deben usarse**. **Descartada por decisión de Dani el 12-nov** (tampoco tiene material suplementario). Ninguna afirmación del reporte depende de ella: el decaimiento del cloro en Tlaquepaque no se modela, y el contexto lo cubren Rubino (medición local) y la OMS |
| OMS (2017), *Guidelines for drinking-water quality*, 4.ª ed. con primer apéndice | Autoridad, no artículo arbitrado. Se leyeron los capítulos 4 y 7 |
| NOM-127-SSA1-2021 | Norma |
| Abernethy et al. (Flint) | Preprint, no se usó |

### Cuáles poner en el reporte

El formato da unas 190 palabras a la bibliografía. Contadas con el formato APA, sin el título:

| Conjunto | Palabras |
|---|---:|
| 5 arbitradas (Rubino, Ercumen, Taylor, Sosa-Moreno, Wu) | 170 |
| Las mismas 5 más la OMS | 187 |
| 6 arbitradas | 194 |

**Propuesta para el cuerpo del reporte (183 palabras):** Rubino, Ercumen, Taylor, Sosa-Moreno,
Kumpel y Nelson 2014, y la OMS. Cada una sostiene una afirmación distinta:

| Afirmación del reporte | Referencia |
|---|---|
| En Guadalajara el agua almacenada y la de la llave ya se salen de norma | Rubino 2019 |
| La baja presión de un suministro intermitente es un riesgo, aun con cloro | Kumpel y Nelson 2014 |
| Al restablecerse el servicio llega el agua contaminada acumulada | Taylor 2018 (y la OMS) |
| El almacenamiento deteriora el agua y la intermitencia cuesta salud | Ercumen 2015 |
| Medir días sin servicio por semana tiene sentido y la gente se defiende con costo | Sosa-Moreno 2025 |
| Desinfectar donde se almacena puede ser necesario | OMS |

Wu 2023, Leifels 2025, Kumpel y Nelson 2016 y Matsinhe 2014 van en los anexos, que no cuentan para el
límite de palabras. **Aviso:** una de las cinco del cuerpo (Kumpel 2014) solo se leyó en resumen; si se
prefiere que las cinco sean de texto completo, se cambia por Wu 2023 (170 palabras en total).

### Lo que NO se puede afirmar con estas referencias

- Que el suministro intermitente causa diarrea en general: Ercumen no lo encontró.
- Que los umbrales de presión de Kumpel (10 y 17 psi) aplican a Tlaquepaque: son de una red de India.
- Que el decaimiento del cloro en Tlaquepaque sea como el de Maputo: solo es comparable el patrón.
- Magnitudes de la intrusión: Taylor es un modelo y Leifels un experimento.

## 2. Qué se pudo y qué no se pudo abrir

| Fuente | Resultado |
|---|---|
| PMC (texto completo en XML) | Abierto. Fuente de 6 artículos |
| PubMed (resúmenes) | Abierto |
| Crossref (metadatos) | Abierto, tras permitir el dominio |
| La Crónica de Hoy | Abierto, tras permitir el dominio |
| ACS (Kumpel y Nelson), Taylor & Francis (*Urban Water Journal*), MDPI, Milenio | **Bloquean la descarga automática (403). No se esquivó** |
| escholarship.org | Respondió 202 sin contenido; no se insistió |

**Los tres artículos pendientes (Kumpel y Nelson 2014 y 2016, y *Urban Water Journal*) son de pago y no vale la
pena comprarlos**: el reporte se sostiene sin ellos. *Urban Water Journal* queda descartada. Si alguien del equipo tiene acceso por su escuela o universidad,
sirve para subir a Kumpel 2014 a "leído completo"; si no, se cita por lo que dice su resumen oficial y su
suplemento, que es lo que ya está verificado. La alternativa de costo cero para el cuerpo del reporte es cambiar
Kumpel 2014 por Wu 2023, que sí está leído completo (170 palabras en total).

## 3. Las notas de prensa

Todas son de **La Crónica de Hoy** (Ricardo Gómez), leídas completas. Las cifras son del **gobierno
municipal**, no medidas por un tercero.

| Nota | Qué establece |
|---|---|
| 21-jul-2026 | El Ayuntamiento opera **24 pipas** y ha instalado **55 cisternas "con capacidad de 10 mil litros cada una"**, con las que distribuyó aproximadamente 15 millones de litros de 22 pozos |
| **30-jul-2026** | Gregorio Lunar Salgado, director de Agua Potable y Alcantarillado: *"Las cisternas se llenan en cuanto recibimos el reporte de las y los vecinos. En ese momento se programa la pipa y se abastecen de inmediato"*. Un pozo se usa "para llenar las pipas que abastecen a las colonias aledañas" |
| 14-oct-2026 | La alcaldesa: *"Llegaremos a un estado de fuerza de 32 pipas. Arrancamos la administración con dos pipas."* Las cisternas irán a las zonas con más dificultad y las pipas harán recorridos a domicilio y llenarán los depósitos de las familias |
| 15-oct-2026 | 32 pipas y 60 cisternas. *"Cada vivienda atendida recibe un promedio de 200 litros. Las pipas tienen una capacidad de 10 mil litros y pueden abastecer hasta 50 hogares por viaje."* Lista de colonias con cisterna. Solicitudes por TlaqueChat |
| 22-oct-2026 | En nueve días, **más de 5.6 millones de litros a 28,296 hogares en más de 220 colonias, con 565 viajes**; 405 peticiones; 60 cisternas con "mantenimiento permanente". Publica el enlace del **mapa de cisternas** (el mismo identificador que usa el repo) |

### Lo que esto resuelve

La pregunta de Jass, ¿hay fuente de que las pipas llenan las cisternas?, **sí la hay**, y de primera mano:
la nota del 30 de julio. También respalda dos supuestos de su baseline:

- **Capacidad de la cisterna comunitaria: 10,000 L** (nota del 21-jul), igual a un viaje de pipa.
- **El reparto real responde a reportes**, no a un calendario fijo. Por eso el baseline sigue siendo
  *estilizado* (los mismos viajes repartidos por turnos) y no hay que presentarlo como "lo que hace
  hoy el municipio".

### Discrepancias que hay que declarar

| Dato | Variación |
|---|---|
| Pipas | 24 en julio; 32 en octubre, que el 14-oct la alcaldesa presentó como **meta** ("llegaremos a"). Por eso `pipas` se reporta pero no restringe el priorizador |
| Cisternas | 55 en julio, 60 en octubre; el mapa trae 50 registros y 10 propuestas |
| Pozos | 22 en julio y octubre; 21 "de extracción" en la nota del 30-ago |
| Hogares atendidos | 565 viajes por 50 = 28,250, casi igual a los 28,296: la cifra de hogares parece **calculada**, no medida |
| Litros por viaje | 5.6 millones entre 565 viajes = 9,911 L por viaje, consistente con 10,000 |
| ¿Los 565 viajes incluyen llenar cisternas? | La nota no lo dice |
| Teléfono de TlaqueChat | Las notas del 15 y del 22 publican números que difieren en un dígito. No citar el número |

### Para el criterio de viabilidad (C5) de Jass

La nota del 15-oct recoge el testimonio de una vecina: algunos proveedores particulares de pipa "cobran
hasta dos mil pesos". Es **un testimonio, no un precio por viaje ni un dato oficial**. Sirve solo como
orden de magnitud: el costo de un viaje, con fuente, sigue pendiente. Las notas también traen inversiones
en pozos: 23.5 millones de pesos en rehabilitación (30-ago-2026), más de 320 millones en la red
hidráulica (21-jul-2026).

### Pendiente

La nota de Milenio ("Tlaquepaque instala 55 cisternas públicas…") no se pudo abrir. Sus datos coinciden con
los de La Crónica del 21 y del 30 de julio, así que no hace falta para sostener nada. No se cita.
