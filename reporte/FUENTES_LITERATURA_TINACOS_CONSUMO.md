# Fuentes Verificadas y Respaldo de Supuestos: Almacenamiento y Consumo
*(Alineado estrictamente con `datos/evidencia.csv`, `decisiones/referencias-y-prensa.md` y `datos/HALLAZGOS_sensibilidad.md`)*

---

## 1. El Supuesto del Tinaco: Tamaño y Procedencia

El Censo de Población y Vivienda 2020 de INEGI registra únicamente si la vivienda dispone de tinaco o cisterna (`VPH_TINACO`, `VPH_CISTER`), pero **no registra su capacidad en litros**. Ante esta ausencia de datos censales, el modelo adopta capacidades estándar declaradas como supuestos:

* **Capacidad base de tinaco ($L_t$):** **1,100 litros**, correspondiente al modelo unifamiliar estándar más comercializado en México (Rotoplas).
* **Rango de sensibilidad:** **750 a 1,100 litros** (con exploraciones adversas desde 450 L en el Anexo D). El tinaco de 750 L corresponde al formato compacto para viviendas pequeñas o restricciones de losa.
* **Capacidad de cisterna ($L_c$):** **5,000 litros** (rango exploratorio de 2,500 a 10,000 L). Se declara como supuesto sin fuente censal.

> **Declaración metodológica rigurosa:** La capacidad del depósito no proviene de un censo ni de una muestra empírica local. Por ello, el análisis de sensibilidad (`datos/HALLAZGOS_sensibilidad.md`) evaluó 36 escenarios y 600 simulaciones de Monte Carlo variando el tamaño del tinaco, demostrando que aunque el orden de manzanas individuales es altamente sensible a este parámetro (rho mediano de 0.65), el *Núcleo Robusto de 186 manzanas* y la prioridad de *El Sauz* se mantienen firmes en más del 90% de los casos.

---

## 2. El Supuesto del Consumo: Niveles y Racionalidad

* **Consumo base ($c$):** **50 litros/persona/día**. Corresponde al nivel básico de emergencia fijado por las directrices internacionales de la Organización Mundial de la Salud (OMS, 2017) y citado como nivel de referencia por Ercumen et al. (2015).
* **Rango de sensibilidad:** **50 a 100 litros/persona/día** (con exploraciones extremas de 120 L procedentes del estudio de Maputo de Matsinhe et al., 2014, y 150 L).
* **Matiz de sensibilidad (crítico para el reporte):** El caso base de 50 L/hab/día junto con el tinaco de 1,100 L representa **el extremo más cómodo y favorable del modelo** (un tinaco dura 5.8 días para una familia mediana de 3.77 ocupantes, resistiendo cualquier racha del SIAPA). Al incrementar el consumo a 100 L/hab/día, la autonomía cae a 2.9 días y las viviendas con tinaco comienzan a quedarse sin agua antes del restablecimiento del servicio, incrementando severamente la población en riesgo.

---

## 3. Bibliografía Científica Arbitrada Verificada (Formato APA)
*(Las 6 referencias arbitradas leídas completas en texto primario que sustentan el proyecto)*

1. **Ercumen, A., Arnold, B. F., Kumpel, E., Burt, Z., Ray, I., Nelson, K., & Colford, J. M.** (2015). Upgrading a piped water supply from intermittent to continuous delivery and association with waterborne illness: A matched cohort study in urban India. *PLOS Medicine, 12*(10), e1001892. https://doi.org/10.1371/journal.pmed.1001892 *(Evidencia de deterioro biológico durante el almacenamiento intermitente; referencia de consumo de 50 L/hab/día).*
2. **Leifels, M., Cheng, D., Cai, J., Nadhirah, N., Mohidin, A. F., Santillan, E., Woo, Y., Hill, E., Wu, S. W., Boon, N., Favere, J., Whittle, A. J., & Wuertz, S.** (2025). Biofilm detachment significantly affects biological stability of drinking water during intermittent water supply in a pilot scale water distribution system. *Scientific Reports, 15*, 22408. https://doi.org/10.1038/s41598-025-03535-1 *(Mecanismo de desprendimiento de biopelículas bacterianas al reiniciar el flujo en redes intermitentes).*
3. **Rubino, F., Corona, Y., Jiménez Pérez, J. G., & Smith, C.** (2019). Bacterial contamination of drinking water in Guadalajara, Mexico. *International Journal of Environmental Research and Public Health, 16*(1), 67. https://doi.org/10.3390/ijerph16010067 *(Estudio empírico en la ZMG: 65% de hogares fuera de norma en cloro residual y 50% de tinacos con coliformes).*
4. **Sosa-Moreno, A., Lee, G. O., Trostle, J. A., Levy, K., Coloma, J., & Eisenberg, J. N. S.** (2025). How water intermittency and water perceptions influence household coping strategies in northwestern Ecuador. *PLOS Water, 4*(9), e0000439. https://doi.org/10.1371/journal.pwat.0000439 *(Sustento para medir el riesgo en días sin servicio por semana).*
5. **Taylor, D. D. J., Slocum, A. H., & Whittle, A. J.** (2018). Analytical scaling relations to evaluate leakage and intrusion in intermittent water supply systems. *PLOS ONE, 13*(5), e0196887. https://doi.org/10.1371/journal.pone.0196887 *(Mecanismo analítico de intrusión de contaminantes durante la despresurización de la red).*
6. **Wu, G., Cheng, J., Yang, F., & Riaz, N.** (2023). Intermittent water supply and self-rated health in rural China's karst region. *Frontiers in Public Health, 11*, 1054730. https://doi.org/10.3389/fpubh.2023.1054730 *(Impacto del suministro intermitente y el almacenamiento prolongado en la salud percibida).*

### Fuentes Complementarias de Respaldo Sanitario y Operativo
* **Kumpel, E., & Nelson, K. L.** (2014). Mechanisms affecting water quality in an intermittent piped water supply. *Environmental Science & Technology, 48*(5), 2766–2775. https://doi.org/10.1021/es405054u *(Riesgo bacteriano en baja presión aun en presencia de cloro).*
* **Matsinhe, N. P., Juízo, D. L., & Persson, K. M.** (2014). The effects of intermittent supply and household storage in the quality of drinking water in Maputo. *VATTEN – Journal of Water Management and Research, 70*, 51–60. *(Tiempos de retención domiciliaria reales de 0.4 a 6.3 días, mediana cercana a 2 días; sustento de U = 48 h).*
* **Organización Mundial de la Salud (OMS).** (2017). *Guidelines for drinking-water quality: Fourth edition incorporating the first addendum*. World Health Organization, Geneva. *(Capítulos 4 y 7: recomendación de desinfección química domiciliaria ante almacenamiento intermitente).*
* **Secretaría de Salud.** (2021). *NOM-127-SSA1-2021, Agua para uso y consumo humano. Límites permisibles de la calidad del agua*. Diario Oficial de la Federación, México. *(Límite de cloro residual libre: 0.2 a 1.5 mg/L).*
