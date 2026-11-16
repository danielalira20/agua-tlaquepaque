# Guía de edición de videos · Aguanta

> **Para quién es:** para cualquier compañero del equipo, o para la IA que use, que vaya a editar los videos de demo de Aguanta (Hackathon Jalisco Internacional 2026 · Reto 01 Ciudades Inteligentes · Equipo #15).
> **Regla de oro:** los 5 videos son **una serie**. Mismos colores, mismas letras, misma voz, mismo ritmo. Usa `Inicio_editado_v3.mp4` como referencia de estilo.

---

## 0. Instrucciones para la IA que edite (léelas antes de empezar)

1. Lee esta guía completa antes de tocar un video. Se edita **un video a la vez**, en este orden: Inicio ✅ → MiCasa → Mapa → PlanDePipas → ComoFunciona.
2. Usa el motor que ya existe en `reporte/videos/editor/` (sección 6). **No inventes otro estilo ni otra paleta.** Si necesitas una pieza nueva (un tipo de tarjeta, por ejemplo), agrégala a `motor2.py` respetando los colores y las fuentes de la sección 2.
3. **La narración va de corrido y la serie NO lleva tarjeta final** (ver 3 y 4). El guion de cada video viene en la sección 5. La columna **"voz"** es lo que lee el TTS, con los números escritos en palabras. La columna **"subtítulo"** es lo que se ve en pantalla, con los números en cifras. Pásalas tal cual a `guion_<video>.json`.
4. **No inventes cifras.** Todos los números salen de la app (datos reales de la semana del 9 al 15 de nov de 2026). Los marcados con ⚠️ se leyeron de capturas pequeñas: confírmalos en la grabación a resolución completa antes de renderizar. Si un número de la grabación no coincide con esta guía, gana la grabación, y se corrige la guía.
5. Antes del render final, saca siempre una **previsualización** (`previsualizar_continuo(...)`) y revísala: textos cortados, recuadros fuera de lugar, glifos que salen como cuadritos (ver 2.3).
6. Al terminar, saca una hoja de contactos (un cuadro cada ~4 s) del MP4 final y revísala completa antes de entregarlo.
7. Salida: `reporte/videos/editados/<Nombre>_editado.mp4` (1920×1080, 30 fps, H.264 + AAC).

---

## 1. Qué estamos contando (contexto en 30 segundos)

- Desde el **15 de octubre de 2026** el SIAPA raciona el agua (**tandeo**) en **627 colonias** del área metropolitana de Guadalajara.
- En Tlaquepaque, entre **13.8 % y 26.5 %** de las viviendas no tienen **ni tinaco ni cisterna**. Para ellas, el primer día de corte ya es un día sin agua.
- **Aguanta** cruza el **Censo 2020 (INEGI, por manzana)** con el **calendario oficial del SIAPA** para saber, manzana por manzana, quién se queda sin agua cada día.
- Tiene **una puerta para cada quien**: familias (*Mi casa*), quien coordina pipas (*Mapa de hoy* y *Plan de pipas*) y el jurado (*Cómo funciona*).
- Cada número trae su etiqueta: **Dato real**, **Estimado** o **Simulado**.

Fuentes que se citan en pantalla: INEGI Censo 2020 por manzana (dataset 01 del reto), CONAPO Índice de Marginación Urbana 2020 (dataset 17), portal y calendario del SIAPA, y el mapa de cisternas del Ayuntamiento de Tlaquepaque.

---

## 2. Identidad visual

### 2.1 Colores (exactos, no cambiar)

| Uso | Nombre en código | RGB | HEX |
|---|---|---|---|
| Fondo, degradado (inicio) | `NAVY1` | (9, 20, 42) | `#09142A` |
| Fondo, degradado (fin) | `NAVY2` | (20, 50, 92) | `#14325C` |
| Texto principal | `BLANCO` | (246, 242, 234) | `#F6F2EA` |
| Énfasis / palabra de impacto / segundo número | `NARANJA` | (240, 138, 93) | `#F08A5D` |
| Etiquetas superiores, recuadros "informativos", primer paso | `CELESTE` | (142, 197, 255) | `#8EC5FF` |
| Texto secundario, créditos, fuentes | `GRIS` | (160, 176, 204) | `#A0B0CC` |
| Relleno de iconos / tarjetas oscuras | `TARJETA_OSCURA` | (14, 34, 66) | `#0E2242` |
| Chip "Dato real" | (verde) | (110, 220, 150) | `#6EDC96` |

- **Fondo:** degradado navy en diagonal, con un brillo suave arriba a la derecha y una retícula de hexágonos casi invisible (blanco al 3–4 %). Ya lo hace `fondo()`.
- **La app nunca va a pantalla completa "cruda".** Siempre va dentro de una tarjeta con esquinas redondeadas y sombra sobre el fondo navy.
- **Dos tonos por frase:** la parte informativa en BLANCO y la palabra de impacto en NARANJA. Ejemplo: "El mismo corte de agua / **no le pega igual.**"
- Los recuadros que resaltan algo en la app son NARANJA cuando señalan un problema o un dato de riesgo, y CELESTE cuando señalan una función o algo neutro.

### 2.2 Tipografía

| Uso | Fuente | Archivo | Tamaños usados (px a 1080p) |
|---|---|---|---|
| Títulos, números grandes, leyendas | Bricolage Grotesque Bold | `fonts/Bricolage-Bold.ttf` | 300 (contador), 190 (rango), 116–120 (título), 56–80 (frases) |
| Subtítulos, etiquetas, chips | Atkinson Hyperlegible Bold | `fonts/Atkinson-Bold.ttf` | 32 (subtítulo), 36–38 (etiqueta superior) |
| Créditos, notas de fuente | Atkinson Hyperlegible Regular | `fonts/Atkinson-Regular.ttf` | 22–32 |

- Las **leyendas grandes sobre la app** van en MAYÚSCULAS y a dos tonos: "CENSO 2020 + **CALENDARIO DEL SIAPA**".
- Las **etiquetas superiores** (encima de un número) van en MAYÚSCULAS, CELESTE y pequeñas: "EN LAS ZONAS CON TANDEO".

### 2.3 Glifos que NO existen en Atkinson
Atkinson no tiene `→`, `●` ni `×`. Si los usas se ven como cuadritos. Para "veces" escribe `x` o la palabra "veces"; los puntos de color se dibujan con `ImageDraw.ellipse`.

### 2.4 Mascota
`app/public/mascota/tlacuache.webp` (el tlacuache con mapa). Solo aparece en la **portada de apertura del video 1** (a la derecha del título, entrando con un pequeño rebote con `pegar(...)`). Los videos no llevan tarjeta final.

---

## 3. Estilo de edición (inspirado en `reporte/videos/inspo/Agro.mov`)

El video NO es "la grabación con zoom". Es un video explicativo donde la app aparece, se va y vuelve. Mezcla estos tipos de toma ("beats"):

| Tipo de beat | Qué se ve | Cuándo usarlo | Función en `motor2.py` |
|---|---|---|---|
| **Apertura / pregunta (la voz la lee)** | Fondo navy + frase grande a dos tonos que entra palabra por palabra, mientras la voz la dice. Es lo primero que se ve: debe pegar fuerte. | Abrir el video (portada del video 1: "El mismo corte de agua no le pega igual a todas las casas.") y, si hace falta, una pregunta retórica a media narración. | `b_apertura` en `hacer_inicio.py`, `texto_animado` |
| **Dato fuera de la app** | La app desaparece. Un número enorme con contador que sube, etiqueta superior CELESTE, frase abajo y chip de fuente ("Dato real · INEGI, Censo 2020"). | Cada vez que la voz dice una cifra importante. Al menos 2 por video. | `contador`, `texto_animado`, `chip` |
| **Comparación** | Dos números lado a lado (BLANCO contra NARANJA) o dos barras. | "Por turnos" contra "priorizado", 0 % contra 73–82 %, etc. | `texto_animado` + barras con `ImageDraw` |
| **App con zoom** | Tarjeta con la app; la cámara viaja con suavizado hacia el elemento que menciona la voz y lo enmarca con un recuadro brillante. | Para mostrar dónde se hace algo en la app. | `pantalla`, `camara`, `recuadro`, `a_pantalla` |
| **App con encabezado** | App más pequeña (`layout="head"`) y un encabezado arriba a la izquierda: "Para la familia: **qué días te quedas sin agua.**" | Para presentar cada sección o puerta. | `encabezado` + `pantalla(..., "head")` |
| **App + dato al lado** | App a la izquierda (`layout="left"`) y un callout grande a la derecha (nombre, número, frase). | Cuando un dato de la app merece destacarse sin salir de ella (ej. El Sauz). | `pantalla(..., "left")` + `texto_animado` |
| **Leyenda grande sobre la app** | Franja inferior de la tarjeta con texto en MAYÚSCULAS a dos tonos. | El "titular" de lo que se ve. | `leyenda_grande` |
| **Entrada 3D** | La tarjeta entra inclinada (~16°) y se endereza. | Solo una vez por video, en la primera aparición de la app. | `pantalla(..., inclinacion=...)` |
| **Pasos numerados** | Hexágonos con número, título y dos líneas, que aparecen sincronizados con cada frase. | Listas de 3–4 ideas. | ver `b_pasos` en `hacer_inicio.py` |

**Ritmo y reglas:**
- **No hay tomas mudas ni tarjeta final.** Cada beat dura exactamente lo que dura su voz y el corte cae en la pausa natural entre frases (lo calcula `montar_continuo`). Un beat rara vez pasa de 9 s; si pasa, pártelo en dos tomas con la misma narración.
- **El video termina en la última toma con un fundido a azul marino (0.8 s)**, sin cierre propio: el siguiente video de la serie arranca con su propia apertura.
- Transición entre beats: disolvencia de **0.3 s** (`XFADE`). No usar barridos ni efectos.
- **Un solo recuadro a la vez.** Si hay que resaltar 3 cosas, se resaltan en secuencia.
- Las palabras entran con un deslizamiento corto hacia arriba (0.4 s, desfase de 0.06 s por palabra).
- **Subtítulos siempre**, abajo al centro, Atkinson Bold 32 con contorno oscuro (`subtitulo`). Los pone `montar` automáticamente desde el guion.
- Sin música. Solo la voz.
- La grabación se acelera o se desacelera para caber en el beat (`Fuente.cuadro`, nunca más lento que 0.45×). Si una toma necesita mucho más tiempo que la grabación, congela un cuadro (rango de 0.1 s en `Fuente`).

**Siempre hay que tapar o cortar:**
- La barra de grabación de la Mac (aparece al final de casi todas las grabaciones).
- El botón "N" de Next.js abajo a la izquierda (`Fuente.cuadro` ya lo tapa) y el tooltip `localhost:3000/...` (encuadra la cámara para que quede fuera, es decir, con y < 1620 en px de la fuente).
- Cuadros negros o en blanco, transiciones con glitch, páginas de WhatsApp y diálogos del sistema.
- Cuadros donde el mapa todavía está cargando.

---

## 4. La voz

- **Motor:** Kokoro (kokoro-onnx 0.6.1), voz **`ef_dora`**, idioma **`es-419`**, velocidad **1.0**, 24 kHz.
- **Mezcla final:** normalizada a −16 LUFS en dos pasadas y en modo lineal (sin bombeo ni saltos de volumen), AAC 192k. Ya lo hace `montar_continuo`.
- **La narración se lee de corrido, por pasajes.** Cada pasaje (2–4 frases relacionadas) se sintetiza en UNA sola llamada, para que la entonación fluya como una lectura real. Las frases sueltas de 2 s suenan planas y entrecortadas: evítalas. `voz.py` quita el silencio de los bordes de cada pasaje, y localiza dónde empieza y termina cada frase con los silencios reales del audio (`marcas.json`). Entre pasajes hay 0.4 s de pausa; dentro de un pasaje, la pausa natural de la voz (0.2–0.5 s). Nunca más de ~0.5 s de silencio seguido.
- Para que una enumeración suene natural, escríbela como una sola oración con dos puntos y comas ("Tiene una puerta para cada quien: las familias…, quien coordina…, y el jurado…") y pasa el texto completo en `"texto"` del pasaje.
- **Números en palabras en la columna "voz"** (Kokoro lee mal las cifras): "seiscientas veintisiete", "diecisiete mil".
- Las cifras largas se redondean al hablar y van exactas en el subtítulo: voz "entre diecisiete mil y treinta y cuatro mil", subtítulo "entre 17,420 y 34,429".
- "3D" se escribe "tres de" en la voz.
- Cada **clave** es una frase que corresponde a una toma; las claves se agrupan en pasajes (`"_pasajes"` en el guion). Si varias tomas comparten una oración (como Medimos / Anticipamos / Actuamos), pártela en claves `a`, `b`, `c` para sincronizar cada aparición.
- Si una toma queda muy corta (menos de ~2 s) para su animación, alarga la frase (agrega una idea real, nunca relleno) en lugar de agregar silencio.
- Después de generar la voz, **escúchala**. Si una palabra suena rara, reescríbela en la columna "voz" (por ejemplo, agrega comas para dar pausas) y vuelve a generar solo esa clave.

---

## 5. Guion y estructura de cada video

Todos los tiempos de la grabación son aproximados (±0.5 s): verifícalos extrayendo cuadros.
Coordenadas de la fuente: 2930×1758 px.

---

### Video 1 · Inicio ✅ (terminado: referencia de estilo)

**Archivo:** `editados/Inicio_editado_v3.mp4` · 68 s · Script: `editor/hacer_inicio.py` · Guion: `editor/guion_inicio.json`
Abre con la portada de la tesis (fondo navy, "TANDEO EN SAN PEDRO TLAQUEPAQUE" en CELESTE, el título en tres líneas BLANCO / NARANJA / BLANCO y la mascota a la derecha) y termina en la toma de "¿Qué tan firmes?" con fundido. Sin tarjeta final.

**Mapa de la grabación `Inicio.mov` (34.6 s):** 0–1.5 portada · 2–4.6 tres puertas · 5–7.9 Mi casa (paso 1) · 11.8–14 Mapa (antes de 11.8 está cargando) · 17–17.1 Cómo funciona (arriba) · 20–27.6 cifras + Medimos/Anticipamos/Actuamos · 28.2–31.8 panel "¿Qué tan firmes?" · ≥33 barra de grabación (cortar).

**Pasajes de voz:** A = N0 · B = N1, N2, N3 · C = NQ, N4 · D = N5–N8 (una sola oración) · E = N9, N10 · F = N11a, N11b, N11c, N12.

| # | Beat | Qué se ve | Voz |
|---|---|---|---|
| 1 | Apertura | Portada: etiqueta + título en 3 líneas que entran palabra por palabra + la mascota con rebote | N0 |
| 2 | 627 | Dato fuera de la app: contador hasta **627**, "colonias con **tandeo**", etiqueta "DESDE EL 15 DE OCTUBRE" | N1 |
| 3 | 1 de cada 4 | 4 casitas dibujadas; la 4.ª en naranja y vacía ("sin tinaco ni cisterna"); luego "Día 1 de corte = **un día sin agua.**" | N2, N3 |
| 4 | Pregunta | La voz lee: "¿Quién se queda / **sin agua hoy?**" (frase grande a dos tonos) | NQ |
| 5 | Portada de la app | Entrada 3D, zoom a los hexágonos; leyendas "CENSO 2020 + **CALENDARIO DEL SIAPA**" y luego "MANZANA **POR MANZANA**" | N4 |
| 6 | Puertas | Encabezado "Una puerta **para cada quien.**"; las 3 puertas se resaltan en secuencia | N5 |
| 7 | Familias | Encabezado + zoom al buscador de colonia | N6 |
| 8 | Municipio | Encabezado + zoom al grupo naranja del mapa | N7 |
| 9 | Jurado | Encabezado + zoom a "Motor oficial = motor de referencia"; leyenda "34,097 DE 34,097 **IGUALES**" | N8 |
| 10 | Casas | Dato fuera de la app: **17,420 – 34,429** "casas sin **tinaco ni cisterna**" + chip "Dato real · INEGI, Censo 2020" | N9 |
| 10 | El Sauz | App a la izquierda (tarjeta El Sauz resaltada) + callout "El Sauz / **11,889** / personas…" | N10 |
| 12 | Pasos | 3 hexágonos: **Medimos / Anticipamos / Actuamos** | N11a, N11b, N11c |
| 13 | Firmes | Zoom a "Dato real · Estimado · Simulado"; leyenda "CADA CIFRA, **CON SU ETIQUETA**"; fundido final | N12 |

| Clave | Voz (TTS) | Subtítulo |
|---|---|---|
| N0 | El mismo corte de agua no le pega igual a todas las casas. | (ninguno: ya está escrito en la portada) |
| N1 | Desde octubre, el SIAPA raciona el agua en seiscientas veintisiete colonias del área metropolitana de Guadalajara. | Desde octubre, el SIAPA raciona el agua en 627 colonias del área metropolitana de Guadalajara. |
| N2 | En Tlaquepaque, entre catorce y veintiséis de cada cien casas no tienen tinaco ni cisterna. | En Tlaquepaque, entre 14 y 26 de cada 100 casas no tienen tinaco ni cisterna. |
| N3 | Para ellas, el primer día de corte ya es un día sin agua. | Para ellas, el primer día de corte ya es un día sin agua. |
| NQ | ¿Y quién se queda sin agua hoy? | ¿Y quién se queda sin agua hoy? |
| N4 | Aguanta cruza el Censo con el calendario oficial del SIAPA, para saber, manzana por manzana, quién se queda sin agua cada día. | Aguanta cruza el Censo con el calendario oficial del SIAPA para saber, manzana por manzana, quién se queda sin agua cada día. |
| N5 | Tiene una puerta para cada quien: | Tiene una puerta para cada quien: |
| N6 | las familias saben qué días se quedan sin agua, | las familias saben qué días se quedan sin agua, |
| N7 | quien coordina las pipas ve dónde se secan las casas hoy, | quien coordina las pipas ve dónde se secan las casas hoy, |
| N8 | y el jurado puede revisar cómo se calcula cada número. | y el jurado puede revisar cómo se calcula cada número. |
| N9 | Todo, con datos reales: entre diecisiete mil y treinta y cuatro mil casas sin dónde guardar agua, en las zonas con tandeo. | Todo con datos reales: entre 17,420 y 34,429 casas sin dónde guardar agua en las zonas con tandeo. |
| N10 | Y El Sauz, la colonia de mayor riesgo: once mil ochocientas ochenta y nueve personas, casi todas sin dónde guardar agua. | Y El Sauz, la colonia de mayor riesgo: 11,889 personas, casi todas sin dónde guardar agua. |
| N11a | Medimos quién tiene tinaco o cisterna. | Medimos quién tiene tinaco o cisterna. |
| N11b | Anticipamos qué día se seca cada casa. | Anticipamos qué día se seca cada casa. |
| N11c | Y actuamos: a dónde mandar primero las mismas pipas. | Y actuamos: a dónde mandar primero las mismas pipas. |
| N12 | Y cada número dice qué tan firme es: dato real, estimado o simulado. | Y cada número dice qué tan firme es: dato real, estimado o simulado. |

---

### Video 2 · Mi casa ("¿Cuánto aguanta tu casa?")

**Para quién:** familias. **Duración objetivo:** 55–65 s. **Salida:** `editados/MiCasa_editado.mp4`
**Decisión del equipo:** se narra el caso grabado (**Artesanos**, colonia fuera del programa de racionamiento) tal cual, y al final se cuenta rápido el **otro caso, El Sauz** (colonia de mayor riesgo, casi sin tinacos), solo con tarjetas de datos, porque no está grabado.

**Mapa de la grabación `MiCasa.mov` (58.4 s):**
- 0–2.3 transición con glitch → **cortar**
- 2.5–6.5 Paso 1 "¿En qué colonia vives?": escribe y elige **Artesanos**
- 7–10.5 Paso 2 "¿Cómo guardas agua en casa?": Nada / Tinaco (calculamos 1,100 L) / Cisterna / Los dos → elige **Tinaco**
- 12–14.5 Paso 3 "¿Cuántas personas viven en tu casa?": contador → **3 personas** ⚠️ (en un cuadro se ve 4; el resultado dice 3), botón "Ver mi resultado"
- 15–23.5 Resultado: "Tu casa en Artesanos · **Tu colonia no está en el programa de racionamiento**", "Tu semana" (gotas por día), "Si te quedas sin agua": cisterna comunitaria (enlace al Mapa de hoy), **pide una pipa por TlaqueChat** (botón "Escribir a TlaqueChat"), **cloro al agua guardada** (2 gotas por litro, reposar 30 min ⚠️), "Que no te agarre desprevenido · Avísale a tus vecinos · Compartir por WhatsApp"
- 24–34.5 negro, blanco, página de WhatsApp y diálogo del sistema → **cortar todo**
- 35–37 resultado otra vez (sirve de relleno) · ~37.5–39.5 página "Compartir en WhatsApp" → **cortar**
- 41–49 panel "**Ajustar el cálculo**": consumo por persona de **50 → 75 L/día**; "Qué supone este cálculo · 3 puntos"
- 50–51.5 resultado con "Ajustar · 75 L por persona"
- 52–57 "Empezar de nuevo" (paso 1) → opcional · ≥57 barra de grabación → **cortar**
- ⚠️ El número de TlaqueChat se ve en la grabación: no lo leas en voz ni lo pongas en grande hasta confirmar que es el oficial.

**Estructura:**

| # | Beat | Qué se ve | Voz |
|---|---|---|---|
| 1 | Apertura | La voz lee la pregunta: "¿Cuánto aguanta / **tu casa?**" (entrada 3D de la app detrás, en cuanto termina) | M0 |
| 2 | Intro | Entrada 3D de la app en el paso 1; encabezado "Mi casa: **tres preguntas, una respuesta.**" | M1 |
| 3 | Colonia | Zoom al buscador mientras escribe "Artesanos"; recuadro CELESTE | M2 |
| 4 | Almacenamiento | Zoom a las 4 opciones; recuadro en "Tinaco"; chip "Calculamos 1,100 L" | M3 |
| 5 | Personas | Zoom al contador; recuadro | M4 |
| 6 | Resultado | App con zoom a "Tu colonia no está en el programa de racionamiento"; leyenda "ARTESANOS: **SIN RACIONAMIENTO**" | M5 |
| 7 | Si te quedas sin agua | `layout="head"`, encabezado "Si te quedas sin agua: **qué hacer.**"; 3 recuadros en secuencia (cisterna comunitaria → TlaqueChat → cloro) | M6a, M6b, M6c |
| 8 | Vecinos | Zoom a "Avísale a tus vecinos · Compartir por WhatsApp" (NO mostrar la página de WhatsApp) | M7 |
| 9 | Ajustar | App a la izquierda con el panel "Ajustar el cálculo"; a la derecha, número grande **50 → 75** "litros por persona al día" | M8 |
| 10 | El Sauz | Dato fuera de la app: "EL SAUZ · ZONA 6 ⚠️" + contador **11,889** "personas, casi todas **sin dónde guardar agua**" + chip "Dato real · INEGI, Censo 2020" | M9, M10 |
| 11 | Contraste | Comparación lado a lado: casa con tinaco (BLANCO, "aguanta días") contra casa sin nada (NARANJA, "Día 1 = sin agua"); reutiliza las casitas de `b_uno_de_cuatro` | M11 |

| Clave | Voz (TTS) | Subtítulo |
|---|---|---|
| M0 | ¿Cuánto aguanta tu casa? | (ninguno: ya está escrito en pantalla) |
| M1 | Para las familias, Aguanta responde una sola pregunta: cuánto aguanta tu casa. | Para las familias, Aguanta responde una sola pregunta: ¿cuánto aguanta tu casa? |
| M2 | Primero, eliges tu colonia. | Primero, eliges tu colonia. |
| M3 | Luego, cómo guardas el agua: nada, tinaco, cisterna, o los dos. | Luego, cómo guardas el agua: nada, tinaco, cisterna o los dos. |
| M4 | Y cuántas personas viven contigo. | Y cuántas personas viven contigo. |
| M5 | En Artesanos hay buena noticia: la colonia no está en el programa de racionamiento. | En Artesanos hay buena noticia: la colonia no está en el programa de racionamiento. |
| M6a | Aun así, te dice qué hacer si te quedas sin agua: dónde está la cisterna comunitaria más cercana, | Aun así, te dice qué hacer si te quedas sin agua: dónde está la cisterna comunitaria más cercana, |
| M6b | cómo pedir una pipa por TlaqueChat, | cómo pedir una pipa por TlaqueChat |
| M6c | y cómo clorar el agua que guardas. | y cómo clorar el agua que guardas. |
| M7 | Y puedes avisarle a tus vecinos por WhatsApp. | Y puedes avisarle a tus vecinos por WhatsApp. |
| M8 | Si en tu casa se gasta más, cambias los litros por persona, y el cálculo se ajusta al instante. | Si en tu casa se gasta más, cambias los litros por persona y el cálculo se ajusta al instante. |
| M9 | Pero en El Sauz, la colonia de mayor riesgo, la historia es otra. | Pero en El Sauz, la colonia de mayor riesgo, la historia es otra. |
| M10 | Ahí viven casi doce mil personas, y casi ninguna tiene dónde guardar agua. | Ahí viven 11,889 personas, y casi ninguna tiene dónde guardar agua. |
| M11 | Sin tinaco ni cisterna, el primer día de corte ya es un día sin agua. Por eso Aguanta les dice qué días prepararse. | Sin tinaco ni cisterna, el primer día de corte ya es un día sin agua. Por eso Aguanta les dice qué días prepararse. |

---

### Video 3 · Mapa de hoy ("¿Dónde se secan las casas hoy?")

**Para quién:** coordinación de pipas / municipio. **Duración objetivo:** 50–60 s. **Salida:** `editados/Mapa_editado.mp4`

**Mapa de la grabación `Mapa.mov` (43.9 s):**
- 0–1.5 mapa del sábado 14 (9,215 – 18,474 viviendas)
- 2–4.5 página "Cómo funciona" (se coló) → **cortar**
- 5–7 jueves 12 (7,909 – 17,699) con hexágonos en 3D naranjas
- 7.5–9.5 panel "La Ladrillera, San Clemente, Vista Hermosa": **0 %**, "Zona fuera del programa"
- 10–12 panel "Las Terrazas, Lomas del Cuatro, Prado de La Luna · Zona 5": **0 %**
- 12.5–14.5 panel "**El Sauz, Lomas del Tesoro, Loma Bonita Ejidal · Zona 6**": **73 – 82 %** de las casas sin agua este día ⚠️
- 15–19 viernes 13: **8,548 – 17,255** viviendas sin agua · **28,596 – 61,321** personas · **372** manzanas con 10 % o más de casas secas · "Más del día: **63.9 – 72.6 %** del riesgo de almacenamiento está en las zonas 5 y 6"
- 20–21 vista 3D muy inclinada · 22.5–29 vista 2D con zoom (hexágonos de colores)
- 30–31 tooltip sobre un hexágono
- 32.5–39 panel "**Ajustar supuestos**": tinaco 1,100 L, consumo 50 → 75 L/día, agua que llega 0 → 25 %, horas efectivas 24 h; "un tinaco aguanta **5.8 días**" → **5.1 días** (casa de 3.8 personas) ⚠️; "Volver al caso base"
- 40–42 mapa final · ≥42.5 barra de grabación → **cortar**

**Estructura:**

| # | Beat | Qué se ve | Voz |
|---|---|---|---|
| 1 | Apertura | La voz lee la pregunta: "¿Dónde se secan / **las casas hoy?**" | P0 |
| 2 | Intro | Entrada 3D del mapa (jueves 12, hexágonos naranjas); leyenda "HEXÁGONO **POR HEXÁGONO**" | P1 |
| 3 | Días | Zoom al selector de días (Lun–Dom); recuadro CELESTE | P2 |
| 4 | Viernes | Dato fuera de la app: etiqueta "VIERNES 13 DE NOVIEMBRE", **8,548 – 17,255** "casas **sin agua**"; debajo, más chico, "28,596 – 61,321 personas" + chip "Estimado" | P3 |
| 5 | Zonas 5 y 6 | Dato fuera de la app: **64 – 73 %** "del riesgo, en las **zonas 5 y 6**" | P4 |
| 6 | Tocar hexágono | App con zoom al panel de detalle | P5 |
| 7 | El Sauz contra Las Terrazas | Comparación: izquierda "Las Terrazas · Zona 5 · **0 %**" (BLANCO), derecha "El Sauz · Zona 6 · **73–82 %**" (NARANJA); "de las casas sin agua este día" | P6, P7 |
| 8 | 3D | Vista 3D inclinada → 2D con zoom; leyenda "INCLÍNALO, **ACÉRCATE**" | P8 |
| 9 | Supuestos | App a la izquierda con "Ajustar supuestos"; a la derecha contador **5.8 → 5.1** "días que aguanta un tinaco"; fundido final | P9, P10 |

| Clave | Voz (TTS) | Subtítulo |
|---|---|---|
| P0 | ¿Dónde se secan las casas hoy? | (ninguno: ya está escrito en pantalla) |
| P1 | El mapa de hoy muestra, hexágono por hexágono, cuántas casas se quedan sin agua cada día. | El mapa de hoy muestra, hexágono por hexágono, cuántas casas se quedan sin agua cada día. |
| P2 | Eliges el día, y el mapa cambia con el calendario del SIAPA. | Eliges el día, y el mapa cambia con el calendario del SIAPA. |
| P3 | El viernes trece, entre ocho mil quinientas y diecisiete mil casas se quedan sin agua. | El viernes 13, entre 8,548 y 17,255 casas se quedan sin agua. |
| P4 | Y casi tres cuartas partes del riesgo están en las zonas cinco y seis. | Y entre 64 y 73 % del riesgo está en las zonas 5 y 6. |
| P5 | Al tocar un hexágono, ves sus colonias y cómo guardan el agua. | Al tocar un hexágono, ves sus colonias y cómo guardan el agua. |
| P6 | En Las Terrazas, ese día, ninguna casa se queda sin agua. | En Las Terrazas, ese día, ninguna casa se queda sin agua. |
| P7 | En El Sauz, entre setenta y tres y ochenta y dos de cada cien. | En El Sauz, entre 73 y 82 de cada 100. |
| P8 | Puedes verlo en tres de, y acercarte a cada colonia. | Puedes verlo en 3D y acercarte a cada colonia. |
| P9 | Y si cambian los supuestos, el resultado se recalcula: con más consumo, un tinaco pasa de aguantar cinco punto ocho días a cinco punto uno. | Y si cambian los supuestos, el resultado se recalcula: con más consumo, un tinaco pasa de aguantar 5.8 días a 5.1. |
| P10 | Así, quien coordina sabe dónde mirar primero. | Así, quien coordina sabe dónde mirar primero. |

---

### Video 4 · Plan de pipas ("Las mismas pipas, otro orden")

**Para quién:** coordinación de pipas / municipio. **Duración objetivo:** 50–60 s. **Salida:** `editados/PlanDePipas_editado.mp4`

**Mapa de la grabación `PlanDePipas.mov` (34.5 s):**
- 0–7 jueves 12: "**63 viajes · 15 colonias**"; "Las mismas 63 pipas, dos repartos"; "Primero donde más casas están secas: **3,150**"; "Por turnos entre cisternas: **828 – 1,891**"; "Hoy, priorizar llega a **1.7 – 3.8 veces** las casas del reparto por turnos"; "En la semana, priorizar **22,050** casas · por turnos **4,532 – 10,177** casas · cada casa cuenta una vez por día"
- 8–13 baja por la lista "**Paradas de hoy (15)**": Cerro del Cuatro, Guadalupe Ejidal, Francisco I. Madero, Francisco I. Madero 2a Sección, Buenos Aires, Lomas del Cuatro, Guayabitos, Lomas de Santa María, Fovissste Miravalle, Terralta, Las Terrazas, Parques de Sta. Cruz del Valle, La Llave
- 14 miércoles 11: 1.8 – 3.9 veces ⚠️ · 16 viernes 13: 2.1 – 7.0 veces ⚠️ · 18 sábado 14: 2.5 – 6.0 veces ⚠️ · 20–34 domingo 15: **3.2 – 8.0 veces** ⚠️, con el selector "Seguro secas / Posiblemente secas" (verifica qué modo está activo en cada cuadro)
- ≥33.5 barra de grabación → **cortar**

**Estructura:**

| # | Beat | Qué se ve | Voz |
|---|---|---|---|
| 1 | Apertura | La voz lee: "Las mismas pipas. / **Otro orden.**" (frase grande a dos tonos) | Q0 |
| 2 | 63 | Dato fuera de la app: contador **63** "viajes de pipa **al día**" | Q1 |
| 3 | Dos repartos | Entrada 3D del plan; zoom a "Las mismas 63 pipas, dos repartos" | Q2 |
| 4 | Comparación | Fuera de la app, dos barras: "Por turnos **828 – 1,891**" (barra gris/blanca) contra "Priorizando **3,150**" (barra naranja), "casas atendidas el jueves 12" | Q3 |
| 5 | Veces | Número enorme: **1.7 – 3.8** "veces más casas" (usa la palabra "veces", no el signo ×) | Q4 |
| 6 | Paradas | `layout="head"`, encabezado "El plan dice **a dónde ir.**"; scroll de la lista de 15 paradas, con recuadros en las 2 primeras | Q5 |
| 7 | Cada día | App con el selector de días; recuadro que salta de día en día; chip con el rango de cada día | Q6 |
| 8 | Semana | Dato fuera de la app: **22,050** contra **4,532 – 10,177** "casas en la semana" + nota GRIS "cada casa cuenta una vez por día" + chip "Estimado"; cierra con fundido | Q7, Q8 |

| Clave | Voz (TTS) | Subtítulo |
|---|---|---|
| Q0 | Las mismas pipas. Otro orden. | (ninguno: ya está escrito en pantalla) |
| Q1 | El municipio ya opera sesenta y tres viajes de pipa al día. | El municipio ya opera 63 viajes de pipa al día. |
| Q2 | Hoy se reparten por turnos entre cisternas. Aguanta propone otro orden: primero, donde más casas están secas. | Hoy se reparten por turnos entre cisternas. Aguanta propone otro orden: primero, donde más casas están secas. |
| Q3 | El jueves doce, por turnos, llegan a entre ochocientas y mil novecientas casas. Priorizando, a tres mil ciento cincuenta. | El jueves 12, por turnos, llegan a entre 828 y 1,891 casas. Priorizando, a 3,150. |
| Q4 | Con las mismas pipas, entre una punto siete y tres punto ocho veces más casas. | Con las mismas pipas, entre 1.7 y 3.8 veces más casas. |
| Q5 | Y el plan dice exactamente a dónde ir: quince paradas, colonia por colonia. | Y el plan dice exactamente a dónde ir: 15 paradas, colonia por colonia. |
| Q6 | Cada día cambia el calendario, y cambia el plan. | Cada día cambia el calendario, y cambia el plan. |
| Q7 | En la semana, priorizar llega a veintidós mil casas. Por turnos, a entre cuatro mil quinientas y diez mil. | En la semana, priorizar llega a 22,050 casas. Por turnos, a entre 4,532 y 10,177. |
| Q8 | Sin comprar una sola pipa más. | Sin comprar una sola pipa más. |

---

### Video 5 · Cómo funciona ("¿De dónde sale cada número?")

**Para quién:** jurado. **Duración objetivo:** 60–70 s. **Salida:** `editados/ComoFunciona_editado.mp4` (es el último de la serie: cierra con el tagline general).

**Mapa de la grabación `ComoFunciona.mov` (47.9 s):**
- 0–1.5 mapa (se coló) → **cortar**
- 2.5–4.5 arriba: "Cómo calculamos cuánta agua te queda", "a partir de **4,871 manzanas reales**", "Motor oficial = motor de referencia · **34,097 de 34,097** renglones iguales (TypeScript contra Python)", "De la red a tu llave, en cuatro pasos" (1 El agua llega por turnos · 2 Cada casa guarda lo que puede · 3 La reserva se gasta · 4 Las pipas van a donde más se seca)
- 5–9 baja: tarjetas **588,419** personas en Tlaquepaque (462,194 dentro del programa) · Dato real; **21,775 – 41,879** viviendas sin tinaco ni cisterna en todo el municipio · Dato real; **210,113 – 490,323** personas-día sin agua en la semana del 9 al 15 de nov · Estimado
- 10–14 abre "La cuenta paso a paso · 5 puntos"
- 15–22 gráficas: "El calendario vigente deja sin agua a **×1.5** más personas que el original"; "Lo que más mueve el resultado es el consumo neto" (con tooltip)
- 25–29 "Las zonas 5 y 6 concentran entre **63.0 % y 72.6 %** de las casas sin tinaco ni cisterna"; "La marginación se muestra aparte: no entra en el cálculo ni en la prioridad de las pipas"
- 30–33 "**El Sauz encabeza la lista** de colonias con más casas sin tinaco ni cisterna"; lista de colonias
- 35–41 "De dónde salen los datos": **01** INEGI Censo 2020 por manzana · **17** CONAPO marginación urbana por AGEB 2020 · SIAPA portal de rotación y lista oficial (2026-11-11) · Gobierno de Tlaquepaque, mapa de cisternas (59 cisternas y 16 propuestas ⚠️)
- 42.5–44 "Qué tener en cuenta al leer estos números · **5 avisos**" (abierto)
- 45–47 regresa arriba · ≥47 barra de grabación → **cortar**

**Estructura:**

| # | Beat | Qué se ve | Voz |
|---|---|---|---|
| 1 | Apertura | La voz lee la pregunta: "¿De dónde sale / **cada número?**" | C0 |
| 2 | 4,871 | Dato fuera de la app: contador **4,871** "manzanas **reales**" + chip "Dato real · INEGI, Censo 2020" | C1 |
| 3 | Cuatro pasos | Entrada 3D de la app arriba; zoom a los 4 pasos, cada tarjeta se resalta con su frase | C2a, C2b, C2c, C2d |
| 4 | Rangos | Leyenda grande "MÍNIMO **– MÁXIMO**" sobre la tarjeta 21,775 – 41,879 | C3 |
| 5 | Semana | Dato fuera de la app: **210,113 – 490,323** "personas-día **sin agua**" + chip "Estimado" | C4 |
| 6 | ×1.5 | Número enorme **1.5 veces** "más personas sin agua con el **calendario vigente**"; después, la gráfica con zoom | C5 |
| 7 | Zonas 5 y 6 | App con zoom a la gráfica de barras; leyenda "ZONAS 5 Y 6: **63 – 73 %**" | C6 |
| 8 | El Sauz | App con zoom a "El Sauz encabeza la lista" | C7 |
| 9 | Motor | Dato fuera de la app: **34,097 / 34,097** "renglones **iguales**", "TypeScript contra Python" | C8 |
| 10 | Fuentes | `layout="head"`, encabezado "De dónde salen **los datos.**"; recuadros en secuencia: 01 INEGI, 17 CONAPO, SIAPA, cisternas | C9 |
| 11 | Avisos | Zoom a "Qué tener en cuenta · 5 avisos"; cierra con fundido | C10 |

| Clave | Voz (TTS) | Subtítulo |
|---|---|---|
| C0 | ¿De dónde sale cada número? | (ninguno: ya está escrito en pantalla) |
| C1 | Todo se calcula en tu navegador, a partir de cuatro mil ochocientas setenta y una manzanas reales del Censo. | Todo se calcula en tu navegador, a partir de 4,871 manzanas reales del Censo. |
| C2a | El agua llega por turnos. | El agua llega por turnos. |
| C2b | Cada casa guarda lo que puede. | Cada casa guarda lo que puede. |
| C2c | La reserva se gasta. | La reserva se gasta. |
| C2d | Y las pipas van a donde más se seca. | Y las pipas van a donde más se seca. |
| C3 | Como el Censo no cruza tinacos y cisternas, cada cifra sale como rango: un mínimo y un máximo. | Como el Censo no cruza tinacos y cisternas, cada cifra sale como rango: un mínimo y un máximo. |
| C4 | En la semana del nueve al quince de noviembre, entre doscientas diez mil y cuatrocientas noventa mil personas-día sin agua. | En la semana del 9 al 15 de noviembre, entre 210,113 y 490,323 personas-día sin agua. |
| C5 | El calendario vigente deja sin agua a una punto cinco veces más personas que el original. | El calendario vigente deja sin agua a 1.5 veces más personas que el original. |
| C6 | Las zonas cinco y seis concentran entre sesenta y tres y setenta y tres por ciento de las casas sin tinaco ni cisterna. | Las zonas 5 y 6 concentran entre 63.0 % y 72.6 % de las casas sin tinaco ni cisterna. |
| C7 | Y El Sauz encabeza la lista de colonias. | Y El Sauz encabeza la lista de colonias. |
| C8 | El motor oficial y el de referencia dan lo mismo: treinta y cuatro mil noventa y siete renglones iguales. | El motor oficial y el de referencia dan lo mismo: 34,097 renglones iguales. |
| C9 | Los datos vienen del Censo del INEGI, del índice de marginación de CONAPO, del calendario del SIAPA y del mapa de cisternas del Ayuntamiento. | Los datos vienen del Censo del INEGI, del índice de marginación de CONAPO, del calendario del SIAPA y del mapa de cisternas del Ayuntamiento. |
| C10 | Y la app te dice qué tener en cuenta al leer cada número. | Y la app te dice qué tener en cuenta al leer cada número. |

---

## 6. Cómo producir un video (paso a paso técnico)

### 6.1 Requisitos (una sola vez)
```bash
# Python 3.10+ y ffmpeg instalado en el PATH
pip install pillow numpy soundfile kokoro-onnx
# Modelos de voz → reporte/videos/editor/modelos/
curl -L -o reporte/videos/editor/modelos/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o reporte/videos/editor/modelos/voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
Los modelos pesan unos 300 MB y **no se suben a git** (agrega `reporte/videos/editor/modelos/`, `cuadros_*/` y `voz_*/` al `.gitignore`).

### 6.2 Archivos de `reporte/videos/editor/`
| Archivo | Qué es |
|---|---|
| `motor2.py` | El motor de estilo: fondo, tarjeta de app, cámara, 3D, recuadros, texto animado, contadores, chips, subtítulos, montaje con narración continua y previsualización. |
| `voz.py` | Genera la narración por pasajes (una llamada por pasaje), recorta silencios y guarda `marcas.json` con el inicio y fin de cada frase. |
| `hacer_inicio.py` | Video 1 completo. **Cópialo como plantilla** para los demás (`hacer_micasa.py`, etc.). |
| `guion_inicio.json` | Guion del video 1. Formato: `"_pasajes": [{"id": "A", "claves": ["N0"], "texto": "(opcional: texto completo del pasaje)"}]` y, por cada clave, `{"voz": "...", "sub": "..."}` (`"sub": ""` si el texto ya está en pantalla). |
| `fonts/` | Bricolage Grotesque y Atkinson Hyperlegible en TTF (licencia OFL). |

### 6.3 Flujo para un video nuevo (ejemplo con MiCasa)
1. **Guion:** crea `guion_micasa.json` con las claves de la sección 5 (columnas voz y sub) y agrúpalas en `"_pasajes"` (2–4 frases relacionadas cada uno; copia el formato de `guion_inicio.json`).
2. **Voz:** `python voz.py guion_micasa.json voz_micasa` → escucha los `.wav` de cada pasaje, revisa en `marcas.json` que cada frase quedó donde debe y que ninguna pausa pasa de ~0.5 s.
3. **Medir la grabación:** extrae cuadros sueltos y dibújales una cuadrícula para leer coordenadas en px de la fuente (2930×1758):
   ```bash
   ffmpeg -ss 16 -i ../MiCasa.mov -frames:v 1 medir_16.jpg
   ```
   (con PIL, dibuja líneas cada 200 px con su número; así se sacan las cajas `(x0, y0, x1, y1)` para `recuadro` y los encuadres `(x, y, w, h)` para `camara`, siempre en proporción 5:3).
4. **Script:** copia `hacer_inicio.py` → `hacer_micasa.py`. Cambia `SRC`, los tramos de `Fuente` (usa solo tramos limpios, sección 5), escribe una función por beat y arma la lista `beats` (cada beat lleva `"voz": [claves]`; no hay tomas mudas: la duración de la toma sale de su voz).
5. **Previsualizar:** `previsualizar_continuo(beats, "voz_micasa", G, [(indice_beat, fraccion), ...], "rev.jpg")` y revisa la imagen.
6. **Render:** `python hacer_micasa.py` → `../editados/MiCasa_editado.mp4` con `montar_continuo(beats, "voz_micasa", G, salida)` (tarda 1–3 min).
7. **Revisar:** hoja de contactos de todo el video (un cuadro cada 4 s) y una vista completa con audio.

### 6.4 Referencia rápida de `motor2.py`
- `Fuente(src, ini, fin, carpeta)` → `.cuadro(t, dur)`: cuadro de la grabación ajustado a la duración del beat (ya tapa el botón N).
- `camara([(u, (x, y, w, h)), ...], t/d)`: encuadre con suavizado entre keyframes (u de 0 a 1).
- `pantalla(img, cuadro, cam, layout="full"|"head"|"left", inclinacion=grados)`: dibuja la tarjeta de la app.
- `a_pantalla(caja_fuente, cam, layout)`: convierte una caja de la grabación a coordenadas de salida (para `recuadro`).
- `recuadro(img, caja, t, t_in, color)`: marco brillante que aparece en `t_in`.
- `texto_animado(img, [[(texto, color), ...], ...], fuente(TIT, tam), t, t_in, y=..., x=None→centrado)`
- `contador(valor, t, t_in, dur)` + `miles(n)` → "17,420".
- `encabezado(img, [[(...)]], t)` · `leyenda_grande(img, [(...)], t, t_in, layout)` · `chip(img, texto, x|None, y, t, t_in, color)` · `pegar(img, rgba, cx, cy, t, t_in, ancho)`
- `montar_continuo(beats, voz_dir, guion, salida)`: coloca los pasajes de voz sin cortarlos, hace que cada toma dure lo que dura su voz (los cortes caen en las pausas), pone subtítulos y disolvencias de 0.3 s, normaliza a −16 LUFS lineal, cierra con fundido y codifica (libx264 veryfast, CRF 18; AAC 192k). `previsualizar_continuo(...)` hace lo mismo pero solo saca cuadros sueltos. (`montar` y `previsualizar` son la versión vieja con tomas mudas: no usar.)
- Dentro de un beat, `m["CLAVE"]` da el segundo en que empieza esa frase y `m["CLAVE_fin"]` el segundo en que termina: úsalos para sincronizar recuadros y textos con la voz.

---

## 7. Lista de revisión antes de entregar un video

- [ ] Se ven las piezas de la serie: apertura que pegue fuerte, 2 datos fuera de la app, zooms con recuadro y 1 entrada 3D. **Sin tarjeta final.**
- [ ] Colores y fuentes exactamente los de la sección 2. Ningún glifo sale como cuadrito.
- [ ] Cada cifra en pantalla coincide con la app (y con el subtítulo). Los ⚠️ están verificados.
- [ ] No se ven: barra de grabación de la Mac, botón N, tooltip `localhost`, cuadros negros, WhatsApp ni diálogos del sistema.
- [ ] Los subtítulos no tapan nada importante y no se salen de la pantalla.
- [ ] La voz se oye clara y pareja (−16 LUFS) y no hay cortes bruscos de audio.
- [ ] El video cierra con fundido a azul marino en la última toma (sin tarjeta ni mascota de cierre).
- [ ] **Audio fluido:** ninguna pausa mayor a ~0.5 s, ningún clic al inicio o fin de frases, volumen parejo de principio a fin (LRA bajo). Escucha el video completo con audífonos.
- [ ] Los créditos ("Equipo #15 · Hackathon Jalisco Internacional 2026" y "Voz generada con inteligencia artificial") van en la descripción de la entrega, ya que el video no lleva tarjeta final.
- [ ] 1920×1080, 30 fps, MP4 en `reporte/videos/editados/`.
