# Auditoría del proyecto contra el kit

Estado revisado: rama `dev` en `56f473d`, miércoles 11 de noviembre de 2026.
Entrega: a más tardar el domingo 15 de noviembre.

El kit tiene 7 indicaciones generales y 5 criterios de éxito del Reto 01. Esta
auditoría los recorre uno por uno, dice qué evidencia existe hoy en el repo y qué
falta. También incorpora el **formato oficial del reporte científico**, que no
habíamos leído y que impone límites que cambian cómo hay que escribirlo.

Semáforo: 🟢 cubierto con evidencia · 🟡 parcial · 🔴 sin cubrir o con riesgo.

---

## 0. Lectura rápida

De las 12 casillas, 2 están en verde, 7 en amarillo y 3 en rojo. Pero varias se
repiten (los criterios 2, 3 y 4 son las indicaciones 5, 2 y 4 dichas de otra forma),
así que en realidad son **seis problemas distintos**:

| # | Problema | Casillas | Gravedad |
|---|---|---|---|
| 1 | El reporte tiene un límite de 2,000 palabras en total | I6, entregable RC | 🔴 cambia cómo se escribe |
| 2 | Falta la viabilidad institucional y presupuestal | C5 | 🔴 sin dueño ni datos |
| 3 | Las tres áreas de conocimiento no están escritas | I4, C4 | 🔴 |
| 4 | El dataset 01 del catálogo puede no ser el que usamos | I2, I3, C3 | 🟡 riesgo de interpretación |
| 5 | El prototipo usa datos simulados y no hay motor ni optimizador en el repo | I5, C2 | 🟡 |
| 6 | La delimitación está pendiente de votación y sin indicador formal | I1 | 🟡 |

La caracterización del problema con datos de Jalisco (C1) es nuestro punto fuerte.

---

## 1. Lo que no sabíamos: el formato del reporte

El kit remite a un "Formato Propuesto" (`https://bit.ly/4fRr2VM`). Lleva a
`Formato_Reporte_Avanzado_Cientifico.docx`. Sus reglas, textuales:

| Regla | Detalle |
|---|---|
| **Extensión** | Mínimo 1,500 y máximo **2,000 palabras, incluyendo referencias, bibliografía, títulos y portada**. Los anexos no cuentan |
| **Resumen** | Entre 300 y 450 palabras, "ni más, ni menos" |
| **Tipografía** | Arial 12, interlineado 1.5, "respetando el orden y la estructura de esta plantilla". Se recomienda a dos columnas después del resumen |
| **Estructura** | Portada · Resumen · 1 Introducción (1.1 Justificación, 1.2 Problema, 1.3 Hipótesis o supuesto metodológico, 1.4 Objetivos) · 2 Contexto teórico · 3 Metodología · 4 Resultados · 5 Análisis y discusiones (5.1 Trabajo a futuro) · 6 Conclusión · 7 Bibliografía · Anexos |
| **Bibliografía** | Formato APA, orden alfabético, **al menos 5 referencias arbitradas**. "Las referencias que no sean confiables serán descartadas y cuestionadas durante la evaluación" |
| **Obligatorio** | **Anexo A: credenciales escolares de los expositores e identificación del asesor.** Foto del equipo |
| **Portada** | Logotipo del concurso, número de proyecto (el nuestro), autores, asesor, escuela, nivel, categoría, sede |

### Qué implica

**El reporte es corto.** Dos mil palabras no alcanzan para caracterizar el problema,
explicar el método, citar cada dataset, justificar tres áreas, presentar tablas de
sensibilidad y la viabilidad. La salida legítima es el **Anexo**, que no cuenta para
el límite. Estrategia:

- El cuerpo cuenta la historia en prosa: problema, método, resultado clave y conclusión.
- Todo lo que sea tabla, fórmula o detalle va a anexos, y el cuerpo los cita.

| Va al anexo (no cuenta palabras) | Qué contiene |
|---|---|
| Anexo A (obligatorio) | Credenciales escolares y de la asesora o asesor |
| Anexo B | **Tabla de citación de datasets**: nombre, institución, año, cobertura, qué se tomó y para qué |
| Anexo C | Las tres áreas de conocimiento y qué aportó cada una |
| Anexo D | Supuestos y análisis de sensibilidad (consumo, tinaco, U, horas de corte) |
| Anexo E | Contrastes: cisternas del municipio y marginación oficial |
| Anexo F | Descripción del prototipo, qué está simulado y qué falta |
| Anexo G | Declaración de uso de IA |

> Una lectura estricta del kit ("aquí explicas cómo usaste cada dataset y qué aportó
> cada área") podría exigir eso en el cuerpo. La salida: en la Metodología va un
> párrafo breve que nombra los datasets y las áreas, y remite al anexo para el detalle.

### Presupuesto de palabras propuesto

| Sección | Palabras |
|---|---:|
| Portada y títulos | 60 |
| Resumen | 310 |
| 1. Introducción (1.1 a 1.4) | 290 |
| 2. Contexto teórico | 190 |
| 3. Metodología | 330 |
| 4. Resultados | 280 |
| 5. Análisis y discusiones | 170 |
| 6. Conclusión | 90 |
| 7. Bibliografía (≥ 5 referencias APA) | 190 |
| **Total** | **1,910** |

Deja 90 palabras de margen. **Hay que contar con el contador de Word, sobre el
documento completo,** porque el límite incluye portada y referencias.

### La hipótesis: hay que formularla

La plantilla pide una hipótesis o un supuesto metodológico. Es un proyecto de
ingeniería aplicada, y la plantilla lo admite: "puede plantearse como un enunciado
que engloba la problemática". Una formulación candidata, para discutir:

> En las colonias de Tlaquepaque dentro del programa de racionamiento, las
> viviendas sin almacenamiento concentran la exposición a quedarse sin agua, y
> priorizar el reparto de pipas por viviendas sin respaldo reduce las
> personas-día sin agua frente a un reparto sin ese criterio, con la misma flota.

Tiene que ser positiva, deseable, factible y viable. Esta lo es, siempre que el
priorizador de Jass produzca el número que la sostiene.

---

## 2. Matriz de las 12 casillas

### Las 7 indicaciones generales

| # | Indicación | Estado | Evidencia en el repo | Falta | Dueño sugerido |
|---|---|:---:|---|---|---|
| I1 | Delimitar: zona, por qué, quién usa, indicador | 🟡 | Municipio fijado; usuarios definidos (coordinación de pipas y familias); razones documentadas | **Votación A/B/C pendiente.** El indicador no está escrito en una frase. Propuesta: *personas-día sin agua por semana* | Magui |
| I2 | ≥ 2 datasets del catálogo | 🟡 | #17 municipal obtenido (el catálogo lo pide "por municipio"). #01 usado a fondo | Ver sección 3: el #01 del catálogo puede no ser lo que usamos. #17 a nivel AGEB pendiente de bajar | Magui |
| I3 | Demostrar cómo se usó cada dataset | 🟡 | `datos/FUENTES.md` documenta procedencia, cobertura y procesamiento | No es la tabla del Anexo B. Falta el uso concreto del #17 y la cita exacta de cada uno | Magui |
| I4 | Tres áreas de conocimiento | 🔴 | Hay material de las tres (ver abajo) | **No está escrito en ningún lado** | Dani |
| I5 | Prototipo funcionando; lo simulado, declarado | 🟡 | `app/` compila (8 páginas estáticas) | Datos simulados. Calendario simulado y distinto del oficial. **No hay código en `motor/` ni `optimizador/`** | Migue, Dani, Jass |
| I6 | Fuentes citadas y uso de IA declarado | 🟡 | `decisiones/verificacion-citas.md` verifica tres citas | No hay bibliografía consolidada en APA. No hay declaración de IA | Dani |
| I7 | Revisar los criterios de éxito | 🟢 | Este documento | Repetirlo el sábado con el reporte ya escrito | Todos |

### Los 5 criterios de éxito del Reto 01

| # | Criterio | Estado | Evidencia | Falta | Dueño sugerido |
|---|---|:---:|---|---|---|
| C1 | Caracterizar el problema con datos específicos de Jalisco | 🟢 | Censo 2020 por manzana; contraste de cisternas (rank mediano 62 contra 125); marginación oficial "Muy bajo" contra 13.8 a 26.5% de viviendas sin almacenamiento; calendario oficial del SIAPA | Pasarlo a 280 palabras de resultados | Magui |
| C2 | Solución funcional o prototipada | 🟡 | Igual que I5 | Igual que I5 | Migue |
| C3 | ≥ 2 datasets oficiales verificables | 🟡 | Igual que I2 | Igual que I2 | Magui |
| C4 | Tres áreas de conocimiento | 🔴 | Igual que I4 | Igual que I4 | Dani |
| C5 | **Viabilidad con el contexto institucional y presupuestal de un municipio real** | 🔴 | Solo contexto: 32 pipas, 60 cisternas, 565 viajes en 9 días, 200 L por hogar, TlaqueChat como canal | **Costo por viaje de pipa, presupuesto municipal, costo de operar la herramienta, quién la adopta.** Nada de eso está investigado y no hay propuesta de Jass en el repo | Jass |

### Las tres áreas: el material ya existe

| Área | Qué aportó | Dónde está |
|---|---|---|
| Ciencia de datos y programación | Cruce de Censo, marco geoestadístico, colonias y zonas; motor por estrato; priorizador; app | `datos/`, `scripts/`, `app/` |
| Ingeniería sanitaria y calidad del agua | Intrusión por baja presión, decaimiento del cloro en almacenamiento, norma de cloro residual | `decisiones/verificacion-citas.md` |
| Salud pública | Riesgo por agua almacenada, recomendaciones de desinfección, vulnerabilidad | OMS cap. 4, estudio de Guadalajara, marginación |
| Economía y políticas públicas *(opcional)* | Costo del operativo de pipas, viabilidad presupuestal municipal | **No investigado** (es la brecha de C5) |

Basta con redactarlo. Las tres primeras ya están.

---

## 3. El dataset 01: el riesgo de interpretación

El catálogo lo define así:

> **#01 · Inventario de viviendas y servicios básicos por AGEB · INEGI** ·
> Cobertura de agua, drenaje y electricidad a nivel manzana en municipios de
> Jalisco · Consulta: `inegi.org.mx/app/mapa/inv`

El enlace de consulta es el **Inventario Nacional de Viviendas 2020**. Lo que
nosotros usamos es otro producto del mismo Censo: *Principales resultados por AGEB
y manzana urbana, Censo de Población y Vivienda 2020*. De ahí salen `VPH_TINACO`,
`VPH_CISTER`, `VPH_AGUADV`, `VPH_DRENAJ` y `VPH_C_ELEC`.

| | |
|---|---|
| **A favor** | Mismo Censo 2020, mismo nivel (manzana), misma institución, y cubre exactamente "agua, drenaje y electricidad". Un jurado razonable lo aceptaría |
| **En contra** | Son productos distintos. No pude confirmar si el Inventario trae tinaco y cisterna. Según la búsqueda, el Inventario describe servicios del entorno de la manzana (redes de agua y drenaje, alumbrado, transporte) y se genera a partir del Censo |
| **Si se interpreta en contra** | Perdemos uno de los dos datasets obligatorios, y el que sostiene todo el proyecto |

### Qué hacer, de menor a mayor esfuerzo

1. **Preguntar a SOLACYT** (`contacto@solacyt.org` o WhatsApp +52 33 1073 3731, con el número de equipo): *"¿El producto 'Principales resultados por AGEB y manzana urbana, Censo 2020' cuenta como el dataset 01 del catálogo?"* Es un mensaje y puede resolver el tema hoy.
2. **Citar con precisión.** En el Anexo B poner el nombre exacto del producto, no solo "dataset 01", y explicar la relación con el Inventario.
3. **Margen de seguridad con un tercer dataset del catálogo** que usemos de verdad. El #02 (agua potable y saneamiento por municipio, CNGMD 2023, INEGI) es el más barato y sirve para el contexto institucional de C5. Así, aunque el #01 se cuestionara, quedarían #17 y #02.

El #17 no tiene este problema: el catálogo lo describe como "marginación y rezago
social **por municipio**", y el archivo municipal de CONAPO es exactamente eso.

---

## 4. Referencias arbitradas: hoy hay 2 leídas, hacen falta 5

El formato exige al menos 5 arbitradas. Estado real:

| Referencia | Estado |
|---|---|
| Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C. (2019). Bacterial contamination of drinking water in Guadalajara, Mexico. *Int. J. Environ. Res. Public Health, 16*(1), 67. https://doi.org/10.3390/ijerph16010067 | ✅ Leída completa. Arbitrada |
| Matsinhe, N. P., Juízo, D. L., & Persson, K. M. (2014). The effects of intermittent supply and household storage in the quality of drinking water in Maputo. *VATTEN, 70*, 51–60 | ✅ Leída completa. Confirmar que la revista es arbitrada |
| Kumpel, E., & Nelson, K. L. (2014). Mechanisms affecting water quality in an intermittent piped water supply. *Environmental Science & Technology*. doi:10.1021/es405054u | ⚠️ **Solo vista por resumen de búsqueda.** Abrir, confirmar el umbral de 10 a 17 psi y completar volumen y páginas |
| Kumpel, E., & Nelson, K. L. (2016). Intermittent water supply: prevalence, practice, and microbial water quality. *Environmental Science & Technology*. doi:10.1021/acs.est.5b03973 | ⚠️ Igual: abrir antes de citar |
| Chlorine degradation in continuous and intermittent drinking water supply networks. *Urban Water Journal, 20*(1), 2022. doi:10.1080/1573062X.2022.2139275 | ⚠️ La frase "se sabe muy poco" y el factor 1.5 vienen de un resumen. Confirmar o quitar |
| Abernethy et al. (Flint). arXiv:1707.01591 | ⚠️ Es un preprint. Solo cuenta si se confirma versión publicada |
| OMS, *Guidelines for Drinking-water Quality*, 4.ª ed., cap. 4 | Leída. **Autoridad, no arbitrada.** Complemento |
| NOM-127-SSA1-2021 | Norma. Complemento |

**Para llegar a 5 arbitradas hay que abrir tres artículos más.** Es trabajo de una
tarde y no se puede dejar al sábado: sin la fuente primaria no hay cita.

---

## 5. Los seis entregables

Todos van en carpetas de Drive separadas (RC, INFO, MU, ET, PITCH, VIDEO), con
permiso de lectura para cualquiera con el enlace, y con los identificadores gráficos
del Hackathon. La carpeta oficial de logos existe y tiene 8 archivos.

| Entregable | Estado | Qué falta |
|---|:---:|---|
| **RC** Reporte científico | 🔴 | Todo. El material existe, pero está en documentos del equipo y en el repo, no en el formato. Ver secciones 1 y 4 |
| **INFO** Infografía | 🔴 | Formato libre. Necesita los números finales de resultados |
| **MU** Manual de usuario | 🔴 | Cómo se usa el software **y sus limitaciones**. Se puede adelantar con la app actual |
| **ET** Entregable técnico | 🟡 | Hay repo con datos, contratos, scripts y app. Falta README de reproducción y el código del motor y del optimizador |
| **PITCH** 8 diapositivas | 🔴 | Máximo 8. Incluir declaración de IA y lo simulado |
| **VIDEO** | 🔴 | Demostración del software funcionando, en YouTube. No se puede grabar sin la app con datos reales |

### La declaración de uso de IA

La convocatoria permite el uso de IA "siempre que su utilización se declare de
manera clara durante la presentación del proyecto". Es una obligación **del reporte
y del pitch**, independiente de quién firme los commits del repositorio. Hay que
decir qué se hizo con IA (análisis de datos, redacción de apoyo, código) y qué
verificó el equipo por su cuenta.

### Lo simulado hay que decirlo

El kit lo exige textualmente. Hoy es simulado: los hexágonos y las cifras de
`app/`, las 60 cisternas de la app (las reales están en `datos/`), el calendario de
noviembre de la app, el aviso por WhatsApp, y el supuesto de que un día de
racionamiento equivale a cero agua.

---

## 6. Administrativo: lo que no puedo verificar desde aquí

Cualquiera de estos descalifica, "incluso después de haberse realizado el evento".

| Requisito | Fuente | Quién lo confirma |
|---|---|---|
| Estatus **FINALISTA** en la plataforma (pago validado y póster subido) | Convocatoria VII | Magui |
| Equipo de **3 a 4** estudiantes, cada uno en un solo equipo | Convocatoria II y V | Todos |
| Todos **estudiantes de preparatoria o universidad**, o egresados con menos de un año | Convocatoria II.1 | Todos |
| **Asesor o asesora mayor de edad** | Convocatoria II.3 | Dani |
| Categoría **B · Hackathon** (preparatoria o universidad) | Convocatoria III | Dani |
| **Anexo A**: credenciales escolares de los expositores e identificación del asesor | Formato del reporte | **Todos, esta semana** |
| Foto del equipo | Formato del reporte | Todos |
| Número de proyecto en la portada | Plataforma | Magui |
| Video publicado en YouTube y carpeta de Drive con permisos | Kit | Migue, Magui |

Una fecha sin confirmar por escrito: el kit dice que la presentación virtual es el
20 y 21 de noviembre, y la página del Hackathon dice 11 y 12 de diciembre.

---

## 7. Ruta propuesta hasta la entrega

| Día | Qué | Responsables |
|---|---|---|
| **Mié 11** | Votar la delimitación. Preguntar a SOLACYT por el dataset 01. Magui pasa a `dev`. Juntar credenciales para el Anexo A | Todos |
| **Jue 12** | Calendario por fecha y zonas reales en el repo. Motor contra datos reales. Abrir las 3 referencias pendientes. Jass investiga costo de pipa y presupuesto municipal | Dani, Jass, Magui |
| **Vie 13** | Priorizador sobre el motor real. App con datos reales. Escribir RC secciones 1 a 3 | Jass, Migue, Dani |
| **Sáb 14** | RC secciones 4 a 6, infografía, manual, pitch y video. Contar palabras del reporte completo | Todos |
| **Dom 15** | Repasar las 12 casillas en voz alta. Subir **antes del mediodía** | Todos |

El eslabón más frágil es **el viernes**: el motor real alimenta al priorizador, que
alimenta al comparador de la app, que alimenta el video, y todo eso antes de que
se pueda escribir la sección de resultados.
