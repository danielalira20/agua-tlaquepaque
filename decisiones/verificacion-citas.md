# Verificación de las tres citas dudosas

Las tres venían de un resumen de búsqueda, no de la fuente primaria. **Las tres
tenían algo mal.** Ninguna debe usarse como estaba redactada.

Dos se pudieron leer en su fuente original. La tercera se resolvió por atribución.

---

## 1. Maputo: "caída de 85% del cloro en 2 a 3 días" ❌ INCORRECTO

**Fuente real:** Matsinhe, N.P.; Juízo, D.L.; Persson, K.M. (2014). *The Effects of
Intermittent Supply and Household Storage in the Quality of Drinking Water in
Maputo.* VATTEN – Journal of Water Management and Research 70:51–60, Lund.
PDF leído completo.

**Lo que dice textualmente:**

> "the average free residual chlorine levels downstream household tanks showed a
> decrease (Figure 3) of about **60 %** during storage (from 0.167 to 0.061 mg/l)."

**Es 60%, no 85%.** Y el artículo no asocia esa caída a un plazo de "2 a 3 días".

### Pero el paper trae tres cosas mejores

**a) Tiempos de retención reales en tinacos domésticos** (Tabla 4): entre **0.4 y
6.3 días**, con mediana cercana a 2 días. **Esto sí sostiene el umbral U = 48 h**,
y mucho mejor que el dato falso que teníamos.

**b) Un supuesto de consumo que contradice el nuestro.** El estudio calcula la
demanda con **120 litros por persona al día**, no 50. Refuerza lo que ya habíamos
detectado: el análisis de sensibilidad sobre el consumo no es trámite, decide quién
aparece en el mapa.

**c) Una frase de cierre citable:**

> "The intermittent operation of the distribution network is therefore inadequate to
> guarantee safe drinking water."

### Cuidado al usarlo

Los valores absolutos de Maputo no son comparables con México: el agua **entraba**
al tinaco con 0.167 mg/L, que ya está por debajo del mínimo de 0.2 mg/L de la
NOM-127. Lo comparable es **el patrón de decaimiento**, no los niveles.

---

## 2. OMS: "el agua de sistemas intermitentes debe considerarse siempre como potencialmente contaminada" ❌ NO EXISTE

Se leyeron completos los capítulos 4 y 7 de las *Guidelines for Drinking-water
Quality*, 4.ª edición con primer apéndice. **La frase no aparece.** La búsqueda de
"always be considered" y variantes devuelve cero resultados.

**Lo que sí dice, textual (capítulo 4):**

> "Where water is supplied intermittently, the resulting low water pressure will
> allow the ingress of contaminated water into the system through breaks, cracks,
> joints and pinholes. Intermittent supplies are not desirable but are very common
> in many countries and are **frequently associated with contamination**. The control
> of water quality in intermittent supplies represents a significant challenge, as
> the risks of infiltration and backflow increase significantly. (…) Where
> contaminants enter the pipes in an intermittent supply, the charging of the system
> when supply is restored may increase risks to consumers, as a concentrated
> **'slug' of contaminated water** can be expected to flow through the system. **Where
> household storage is used to overcome intermittent supply, localized use of
> disinfectants to reduce microbial proliferation may be warranted.**"

### El texto real es mejor que el inventado, por dos razones

**a) La última frase respalda nuestro diseño.** La OMS dice explícitamente que donde
se usa almacenamiento doméstico para sobrellevar el suministro intermitente, puede
justificarse la desinfección localizada. Eso es exactamente el campo
`requiere_desinfeccion` y el aviso por WhatsApp, avalados por la guía de la OMS.

**b) Describe un mecanismo que no habíamos modelado:** el "slug", el tapón de agua
contaminada que recorre la red cuando se restablece el servicio. El riesgo no es
solo durante el corte, sino **en el momento del regreso del agua**. Vale la pena
mencionarlo en el reporte aunque no se modele.

---

## 3. "La revisión de 2026 dice que se sabe muy poco sobre el decaimiento de cloro en redes intermitentes" ⚠️ MAL ATRIBUIDO

La afirmación es real, pero **no es de la revisión de 2026.**

| | |
|---|---|
| **Dónde está la frase** | Chlorine degradation in continuous and intermittent drinking water supply networks. *Urban Water Journal*, 20(1), **2022**. doi:10.1080/1573062X.2022.2139275 |
| **Qué es la de 2026** | Effects of intermittent water supply on disinfection by-product formation and water quality deterioration: A review. *Cleaner Water*, 6, 100228, 2026. Trata de subproductos de desinfección, otro tema |

**Dato extra del artículo de 2022, útil para el motor:** la tasa de decaimiento de
cloro en redes intermitentes con tubería de hierro dúctil y fundido resultó
**1.5 veces mayor** que en redes continuas.

**Limitación:** ninguno de los dos se pudo leer en texto completo (ScienceDirect
responde 403 a peticiones automatizadas). La atribución viene de fuentes
secundarias. **Antes de citarla en el reporte hay que abrir el artículo de 2022 y
confirmar la frase.** Si no se confirma, se quita: no es una cita que haga falta.

---

## Bonus: el estudio de Guadalajara ✅ CONFIRMADO, y es más rico de lo que creíamos

*Bacterial Contamination of Drinking Water in Guadalajara, Mexico.* Leído completo
en PMC6339170. Todo lo que habíamos dicho se confirma, y hay más:

| Hallazgo | Valor |
|---|---|
| Casas con medición inicial de cloro | **51** |
| Casas con remedición | 10, a las **120 horas** |
| Tinacos de azotea que excedieron el límite de coliformes totales | **la mitad** |
| Casas con cloro residual dentro de 0.2–1.5 mg/L | **solo 35%** |
| Residentes que beben agua de la llave | **7%** |
| E. coli detectada | ninguna |

**Es la mejor cita del proyecto:** es local, es revisada por pares, mide exactamente
la cadena que modelamos, y confirma el rango de la NOM-127 con un dato propio de
Guadalajara: **el 65% de las casas estaba fuera de norma.**

Una tensión que hay que declarar: el estudio describe el almacenamiento doméstico
como "casi ubicuo" en la ZMG, mientras que nuestro análisis del Censo encuentra
entre 13.8% y 26.5% de viviendas sin tinaco ni cisterna en Tlaquepaque. El estudio
es un piloto con muestra por conveniencia de 51 casas; el Censo cubre 158,135
viviendas. No se contradicen: miden cosas distintas con alcances distintos.

---

## Qué hacer con esto

| Cita | Acción |
|---|---|
| Maputo 85% | **Corregir a 60%**, y usar además los tiempos de retención de 0.4 a 6.3 días como sustento de U = 48 h |
| Frase de la OMS | **Sustituir** por el texto literal del capítulo 4. Agregar el mecanismo del "slug" |
| Revisión 2026 | **Reatribuir** al artículo de 2022, y confirmarlo antes de usarlo. Si no, quitarlo |
| Consumo de 50 L/p/día | Contrastarlo con los **120 L/p/día** de Maputo en el análisis de sensibilidad |
| k del decaimiento | Considerar el factor **1.5×** de redes intermitentes, pendiente de confirmar |

---

## Actualización del 11 de noviembre

Las acciones de la tabla anterior se cerraron o cambiaron. Detalle y fuentes en
`referencias-y-prensa.md`.

| Cita | Resultado |
|---|---|
| Maputo (Matsinhe 2014) | El 60% se confirmó y quedó corregido en `datos/evidencia.csv`. Pero VATTEN **no es arbitrada** ("A referee system is not applied in the formal meaning"): se cita como fuente científica, no entre las 5 arbitradas |
| OMS, texto literal del capítulo 4 | Registrado tal cual (renglón E008) |
| *Urban Water Journal* | Autores confirmados: Vaidya, Kumar, Mohan Kumar y Rao, volumen 20(1), 2023. **El texto sigue sin abrirse**; el factor 1.5 se marca NO USAR |
| Kumpel y Nelson 2014 | El resumen oficial de PubMed confirma los umbrales de 10 y 17 psi |
| Consumo de 120 L (Maputo) | Registrado para la sensibilidad (renglón E007) |
