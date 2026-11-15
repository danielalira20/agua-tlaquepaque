# Anexo C: Convergencia de Tres Áreas del Conocimiento
*(Cumplimiento estricto de la Indicación 4 y el Criterio 4 de Éxito del Reto 01)*

El proyecto no constituye un desarrollo tecnológico aislado, sino una solución interdisciplinaria donde convergen de manera orgánica tres campos del saber científico y técnico:

```mermaid
flowchart TD
    CC["1. Ciencias de la Computación\ny Ciencia de Datos"]
    SP["2. Salud Pública y\nEpidemiología"]
    IH["3. Ingeniería Hidráulica y\nPolíticas Públicas"]
    
    CC --- SOL["Agua Tlaquepaque:\nSistema Predictivo y\nOptimizador Logístico"]
    SP --- SOL
    IH --- SOL
```

---

### 1. Ciencias de la Computación y Ciencia de Datos
* **Aporte a la solución:**
  - **Algoritmos de Optimización Combinatoria:** Implementación de un algoritmo voraz (*greedy algorithm*) geográfico que resuelve el problema de asignación espacial de la flota municipal de pipas bajo restricciones de capacidad física (10,000 L/viaje), número de viajes disponibles por jornada (63 viajes al día) y radios caminables de cobertura (300 m).
  - **Simulación Estadística y Análisis de Sensibilidad:** Ejecución de 36 escenarios deterministas y 600 simulaciones estocásticas de Monte Carlo con semilla controlada para identificar el *Núcleo Robusto de 186 manzanas críticas*, superando la incertidumbre de parámetros no observados en el Censo.
  - **Ingeniería de Datos Espaciales:** Procesamiento de microdatos a escala de manzana urbana (4,871 unidades), geocodificación de centroides, análisis de intersección topológica y visualización geoespacial jerárquica mediante indexación hexagonal Uber H3 en arquitectura web moderna (Next.js / TypeScript).

### 2. Salud Pública y Epidemiología
* **Aporte a la solución:**
  - **Dinámica del Cloro Residual y Deterioro Biológico:** Integración del umbral sanitario oficial de la **NOM-127-SSA1-2021** (cloro residual libre entre 0.2 y 1.5 mg/L). Modelado del tiempo de almacenamiento crítico ($U = 48\text{ horas}$), sustentado en las mediciones de retención en depósitos domésticos de Matsinhe et al. (2014, mediana de retención cercana a 2 días) y contrastado con la evidencia local de Guadalajara reportada por Rubino et al. (2019; PMC6339170), donde el 65% de los hogares analizados incumplió la norma de cloro libre y el 50% de los tinacos presentó coliformes.
  - **Mecanismos de Contaminación en Redes Intermitentes:** Consideración de los riesgos microbiológicos asociados a la despresurización de tuberías y el arrastre de sedimentos contaminados (*slug*) documentados por Taylor et al. (2018) y las directrices de la Organización Mundial de la Salud (OMS, 2017).
  - **Protocolos de Cloración Domiciliaria:** Generación de alertas preventivas personalizadas para la ciudadanía en el módulo *Mi Casa*, indicando el momento en que el agua almacenada requiere desinfección química domiciliaria según las recomendaciones sanitarias de la OMS.

### 3. Ingeniería Hidráulica y Políticas Públicas
* **Aporte a la solución:**
  - **Mecánica de Redes de Suministro Intermitente:** Análisis del esquema de rotación y tandeo del SIAPA abastecido por la Planta Miravalle. Modelación de la duración de corte declarada como supuesto operativo (*horas efectivas de corte* de 24 a 48 h) y de la fracción de suministro residual en baja presión ($f = 0$ a $0.5$).
  - **Balance Hídrico y Autonomía por Estratos:** Cálculo de la tasa de agotamiento de volumen en función del dimensionamiento físico de depósitos domiciliarios (750 a 1,100 L en tinacos; 2,500 a 5,000 L en cisternas) y del consumo per cápita bajo racionamiento (50 a 100 L/hab/día).
  - **Economía Urbana y Gestión de Servicios Públicos:** Evaluación de la viabilidad presupuestal del operativo municipal (`optimizador/docs/viabilidad-presupuestal.md`), demostrando cómo una regla de asignación algorítmica rinde entre 1.4× y 5.6× más viviendas atendidas con los mismos recursos y viajes que el municipio ya realiza, sin demandar incremento en el gasto corriente.
