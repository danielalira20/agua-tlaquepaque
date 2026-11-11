# Auditoría del proyecto contra el kit

Estado revisado: primera versión sobre `dev` en `56f473d`; **actualizada el miércoles 11 de
noviembre de 2026 sobre `dev` en `6402f2a`**, después de cruzar zonas del SIAPA, procesar la
marginación por AGEB y cerrar el contrato `plan`. Entrega: a más tardar el domingo 15 de noviembre.

El kit tiene 7 indicaciones generales y 5 criterios de éxito del Reto 01. Esta
auditoría los recorre uno por uno, dice qué evidencia existe hoy en el repo y qué
falta. También incorpora el **formato oficial del reporte científico**, que no
habíamos leído y que impone límites que cambian cómo hay que escribirlo.

Semáforo: 🟢 cubierto con evidencia · 🟡 parcial · 🔴 sin cubrir o con riesgo.

---

## 0. Lectura rápida

De las 12 casillas, **4 están en verde, 5 en amarillo y 3 en rojo**. Varias se repiten
(los criterios 2, 3 y 4 son las indicaciones 5, 2 y 4 dichas de otra forma), así que
siguen siendo **seis problemas distintos**:

| # | Problema | Casillas | Gravedad |
|---|---|---|---|
| 1 | El reporte tiene un límite de 2,000 palabras en total | I6, entregable RC | 🔴 cambia cómo se escribe |
| 2 | Falta la viabilidad institucional y presupuestal | C5 | 🔴 sin dueño ni datos |
| 3 | Las tres áreas de conocimiento no están escritas | I4, C4 | 🔴 |
| 4 | El dataset 01 del catálogo puede no ser el que usamos | I3 | 🟡 mitigado: quedan #17 y #02. Falta preguntar a SOLACYT |
| 5 | El prototipo usa datos simulados y el priorizador no tiene código | I5, C2 | 🟡 hay motor, contratos y especificación |
| 6 | La delimitación espera el voto de Magui y tiene cifras con rango | I1 | 🟡 |

La caracterización del problema con datos de Jalisco (C1) es nuestro punto fuerte.

### Qué cambió el 11 de noviembre

| Casilla | Antes | Ahora | Por qué |
|---|:---:|:---:|---|
| I2, C3 (≥ 2 datasets) | 🟡 | 🟢 | El #17 ya se usa a dos niveles (municipal y AGEB). El #02 está verificado como respaldo, así que aunque el #01 se cuestionara quedan dos. Condición: citar el #02 con un uso concreto |
| I5, C2 (prototipo) | 🟡 | 🟡 | Ya hay motor de referencia con 34 pruebas, contratos con fixtures y la especificación del priorizador. La app sigue simulada y falta el código del priorizador |
| I1 (delimitación) | 🟡 | 🟡 | Jass y Migue votaron B. Falta Magui. Las cifras se corrigieron (ver la advertencia 1) |

### Cuatro advertencias nuevas para el reporte

Salieron de los datos de hoy y cambian lo que se puede afirmar:

1. **La cobertura del programa es un rango.** 63% a 79% de la población de Tlaquepaque: el 63%
   tiene respaldo de la lista oficial del SIAPA y el 16% restante sale solo de los polígonos del
   portal. El PDF oficial no nombra esas colonias (`datos/zonas_siapa/LEEME.md`).
2. **No se puede decir que "el riesgo se concentra en los más pobres".** Dentro del programa, el 50%
   de las viviendas sin tinaco ni cisterna está en AGEB de marginación "Muy bajo"
   (`datos/HALLAZGOS_marginacion.md`). Sí se puede decir que el índice oficial mide el tubo y no el
   almacenamiento. Hay que presentar exposición y vulnerabilidad social como dos dimensiones.
3. **"Sin agua" va con el supuesto de corte total.** El portal del SIAPA dice que el racionamiento es
   baja de presión. El valor por defecto `f = 0` es la cota alta, no una medición, y a 50 L/persona/día
   casi no cambia el resultado, pero a 100 L lo multiplica por 2.2 (`motor/ESPECIFICACION.md`, sección 9).
4. **El baseline del priorizador es estilizado**: los mismos viajes repartidos por turnos entre las
   cisternas instaladas, no el reparto real del municipio, del que no hay registro.

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
| Anexo D | Supuestos y análisis de sensibilidad (consumo, tinaco, U, horas de corte, fracción `f` que sigue llegando) |
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
> repartir los mismos viajes de pipa según esa necesidad, en lugar de repartirlos
> entre las cisternas ya instaladas, atiende a más viviendas sin agua.

Tiene que ser positiva, deseable, factible y viable. Esta lo es, siempre que el
priorizador de Jass produzca el número que la sostiene.

---

## 2. Matriz de las 12 casillas

### Las 7 indicaciones generales

| # | Indicación | Estado | Evidencia en el repo | Falta | Dueño sugerido |
|---|---|:---:|---|---|---|
| I1 | Delimitar: zona, por qué, quién usa, indicador | 🟡 | Municipio fijado; usuarios definidos (coordinación de pipas y familias); razones documentadas. Opción B recomendada (colonias dentro del programa, zonas 3 a 6): 462,194 personas (78.6%), de las cuales 368,111 (62.6%) con respaldo de la lista oficial. Jass y Migue votaron B | **Falta el voto de Magui.** El indicador no está escrito en una frase. Propuesta: *personas-día sin agua por semana* (semana del 9 al 15 de noviembre: 210,116 a 490,320 con el calendario vigente) | Magui |
| I2 | ≥ 2 datasets del catálogo | 🟢 | #17 a dos niveles: municipal (Tlaquepaque "Muy bajo", lugar 2,424 de 2,469) y AGEB (214 AGEB cruzadas con las manzanas por `CVE_AGEB`). #01 usado a fondo. #02 (CNGMD 2023) verificado como respaldo | La sección 3 sigue: preguntar a SOLACYT por el #01. Citar el #02 con un uso concreto en el reporte | Magui |
| I3 | Demostrar cómo se usó cada dataset | 🟡 | `datos/FUENTES.md` documenta procedencia, cobertura y procesamiento de manzanas, colonias, zonas y calendarios del SIAPA, marginación y cisternas | No es la tabla del Anexo B. Falta la cita exacta de cada uno y la extracción del #02, que todavía no está en el repo | Magui |
| I4 | Tres áreas de conocimiento | 🔴 | Hay material de las tres (ver abajo) | **No está escrito en ningún lado** | Dani |
| I5 | Prototipo funcionando; lo simulado, declarado | 🟡 | `app/` compila (8 páginas estáticas). **`motor/` tiene especificación y una implementación de referencia en Python con 34 pruebas.** Los contratos `calendario`, `zonas`, `manzanas`, `estado` y `plan` están actualizados con fixtures. Jass tiene la especificación del priorizador en su rama | La app sigue con datos simulados y calendario simulado, distinto del oficial. Falta adaptar el motor oficial en TypeScript, y **el priorizador no tiene código** | Migue, Dani, Jass |
| I6 | Fuentes citadas y uso de IA declarado | 🟡 | `decisiones/verificacion-citas.md` verifica tres citas; `datos/evidencia.csv` registra cada fuente con su nivel de verificación | La bibliografía en APA ya está consolidada (`decisiones/referencias-y-prensa.md`). Falta la declaración de IA | Dani |
| I7 | Revisar los criterios de éxito | 🟢 | Este documento | Repetirlo el sábado con el reporte ya escrito | Todos |

### Los 5 criterios de éxito del Reto 01

| # | Criterio | Estado | Evidencia | Falta | Dueño sugerido |
|---|---|:---:|---|---|---|
| C1 | Caracterizar el problema con datos específicos de Jalisco | 🟢 | Censo 2020 por manzana; contraste de cisternas (rank mediano 62 contra 125 sobre todo el municipio; **37 contra 59 restringido al programa**); marginación oficial "Muy bajo" contra 13.8 a 26.5% de viviendas sin almacenamiento; calendario y zonas oficiales del SIAPA (verificados contra su PDF) | Pasarlo a 280 palabras de resultados, con las cuatro advertencias de la sección 0 | Magui |
| C2 | Solución funcional o prototipada | 🟡 | Igual que I5 | Igual que I5 | Migue |
| C3 | ≥ 2 datasets oficiales verificables | 🟢 | Igual que I2 | Igual que I2 | Magui |
| C4 | Tres áreas de conocimiento | 🔴 | Igual que I4 | Igual que I4 | Dani |
| C5 | **Viabilidad con el contexto institucional y presupuestal de un municipio real** | 🔴 | Solo contexto: 32 pipas, 60 cisternas según la prensa (el mapa del municipio trae 50 más 10 propuestas), 565 viajes en 9 días, 200 L por hogar, TlaqueChat como canal | **Costo por viaje de pipa, presupuesto municipal, costo de operar la herramienta, quién la adopta.** Nada de eso está investigado y no hay propuesta de Jass en el repo | Jass |

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
| **En contra** | Son productos distintos. No pude confirmar si el Inventario trae tinaco y cisterna. Su presentación lista vialidad, mobiliario y servicios urbanos, y no nombra tinaco ni cisterna. (Una versión anterior de este documento decía "redes de agua y drenaje": no es lo que dice la presentación) |
| **Si se interpreta en contra** | Perdemos uno de los dos datasets obligatorios, y el que sostiene todo el proyecto |

### Qué hacer, de menor a mayor esfuerzo

1. **Preguntar a SOLACYT** (`contacto@solacyt.org` o WhatsApp +52 33 1073 3731, con el número de equipo): *"¿El producto 'Principales resultados por AGEB y manzana urbana, Censo 2020' cuenta como el dataset 01 del catálogo?"* Es un mensaje y puede resolver el tema hoy.
2. **Citar con precisión.** En el Anexo B poner el nombre exacto del producto, no solo "dataset 01", y explicar la relación con el Inventario.
3. **Margen de seguridad con un tercer dataset del catálogo** que usemos de verdad. El #02 (agua potable y saneamiento por municipio, CNGMD 2023, INEGI) **ya está verificado**: es utilizable (el año del censo es 2023, la información es de 2022) y trae, para Tlaquepaque, que hay dos operadores (la administración municipal fuera de la cabecera, con pipas, y el SIAPA en la cabecera), tomas con y sin medidor, y montos de cobro sin dato. Sirve para el contexto institucional de C5. Así, aunque el #01 se cuestionara, quedarían #17 y #02. **Falta versionar la extracción de Tlaquepaque y citarlo en el Anexo B.**

El #17 no tiene este problema: el catálogo lo describe como "marginación y rezago
social **por municipio**", y el archivo municipal de CONAPO es exactamente eso. Además ya
se usa a nivel AGEB.

---

## 4. Referencias arbitradas: ya hay 6 leídas completas

Actualizado el 11 de noviembre. El formato exige al menos 5 arbitradas. El detalle, con las
fechas de recepción y aceptación de cada artículo, las afirmaciones que sostiene y sus límites, está en
`decisiones/referencias-y-prensa.md`; el registro, en `datos/evidencia.csv`.

| Referencia | Estado |
|---|---|
| Rubino et al. (2019), Guadalajara. *Int. J. Environ. Res. Public Health, 16*(1), 67 | ✅ Arbitrada, texto completo |
| Ercumen et al. (2015), Hubli-Dharwad. *PLOS Medicine, 12*(10), e1001892 | ✅ Arbitrada, texto completo |
| Taylor, Slocum y Whittle (2018). *PLOS ONE, 13*(5), e0196887 | ✅ Arbitrada, texto completo |
| Sosa-Moreno et al. (2025). *PLOS Water, 4*(9), e0000439 | ✅ Arbitrada, texto completo |
| Wu et al. (2023). *Frontiers in Public Health, 11*, 1054730 | ✅ Arbitrada, texto completo |
| Leifels et al. (2025). *Scientific Reports, 15*, 22408 | ✅ Arbitrada, texto completo |
| Kumpel y Nelson (2014). *Environ. Sci. Technol., 48*(5), 2766–2775 | 🟡 Arbitrada (MEDLINE). **Solo resumen oficial**: confirma los umbrales de 10 y 17 psi |
| Kumpel y Nelson (2016). *Environ. Sci. Technol., 50*(2), 542–553 | 🟡 Igual: solo resumen oficial |
| Matsinhe et al. (2014). *VATTEN, 70*, 51–60 | ⚠️ **No es arbitrada** (la revista dice que no aplica un sistema de arbitraje formal). Citable como fuente científica, no cuenta entre las 5 |
| Vaidya et al. (2023). *Urban Water Journal, 20*(1), 60–73 | ⚠️ Autores confirmados. **Sin abrir**: el factor 1.5 sigue sin poder usarse |
| Abernethy et al. (Flint). arXiv:1707.01591 | ⚠️ Preprint. No se usó |
| OMS, *Guidelines for Drinking-water Quality*, 4.ª ed., cap. 4 | Leída. **Autoridad, no arbitrada.** Complemento |
| NOM-127-SSA1-2021 | Norma. Complemento |

**El requisito de 5 se cumple con margen**, pero el presupuesto de palabras manda: 5 referencias APA
ocupan unas 170 palabras de las 190 que da el formato. Propuesta para el cuerpo: Rubino, Ercumen, Taylor,
Sosa-Moreno, Kumpel y Nelson 2014 y la OMS (183 palabras); el resto, en los anexos.

**Una advertencia de contenido:** Ercumen no encontró asociación significativa entre suministro continuo y
diarrea en general. El reporte no debe afirmar que la intermitencia causa diarrea.

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
| **ET** Entregable técnico | 🟡 | Hay repo con datos, contratos con fixtures, scripts reproducibles (`asigna_zonas`, `recalcular_hallazgos`, `procesa_imu`, `extrae_lista_pdf`), el motor de referencia y las especificaciones. Falta el README de reproducción, el motor oficial en TypeScript y el código del priorizador |
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
`app/`, las 60 cisternas inventadas de la app (las reales, 50 más 10 propuestas, están en `datos/`), el calendario de
noviembre de la app, el aviso por WhatsApp, y el supuesto de que un día de
racionamiento equivale a cero agua (`f = 0`, aprobado como cota alta; ver la advertencia 3).
El baseline del priorizador y el fixture del plan también son estilizados o provisionales.

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
| **Mié 11** | Votar la delimitación (✅ Jass y Migue; falta Magui). Preguntar a SOLACYT por el dataset 01. Magui pasa a `dev`. Juntar credenciales para el Anexo A | Todos |
| **Jue 12** | ✅ *Adelantado el 11:* calendario por fecha y zonas reales en el repo, motor de referencia contra datos reales, marginación por AGEB, contrato `plan`. **Referencias arbitradas: verificadas el 11** (ver sección 4). **Sigue pendiente:** Jass investiga costo de pipa y presupuesto municipal, con fuente, y preguntar al SIAPA por las colonias que su PDF no nombra | Dani, Jass, Magui |
| **Vie 13** | Priorizador sobre el motor real. App con datos reales. Escribir RC secciones 1 a 3 | Jass, Migue, Dani |
| **Sáb 14** | RC secciones 4 a 6, infografía, manual, pitch y video. Contar palabras del reporte completo | Todos |
| **Dom 15** | Repasar las 12 casillas en voz alta. Subir **antes del mediodía** | Todos |

El eslabón más frágil es **el viernes**: el motor real alimenta al priorizador, que
alimenta al comparador de la app, que alimenta el video, y todo eso antes de que
se pueda escribir la sección de resultados.
