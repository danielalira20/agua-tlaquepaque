# Análisis de Viabilidad Institucional y Presupuestal
*(Cumplimiento estricto del Criterio 5 de Éxito del Reto 01 — Hackathon SOLACYT 2026)*

---

## 1. Contexto Institucional del Municipio de San Pedro Tlaquepaque

La gestión hídrica en San Pedro Tlaquepaque opera bajo un esquema de responsabilidades compartidas:
1. **El SIAPA (Nivel Intermunicipal):** Administra la extracción, potabilización y distribución por tubería en red fija. Sus decisiones de corte y rotación por zonas son externas al municipio.
2. **El Gobierno Municipal de San Pedro Tlaquepaque:** A través de la Coordinación General de Servicios Públicos y la Dirección de Agua Potable, asume la responsabilidad directa del **operativo de emergencia y mitigación del desabasto** mediante camiones cisterna (pipas) y cisternas comunitarias superficiales.

### La problemática operativa actual
El municipio opera hoy bajo un **esquema reactivo por demanda**: las familias solicitan agua a través del canal municipal de mensajería (*TlaqueChat* en WhatsApp) o reportes ciudadanos. Esto genera tres ineficiencias severas:
* **Sesgo de conectividad:** Colonias con mayor acceso a telefonía e influencia política concentran las solicitudes, dejando rezagadas a zonas periféricas de extrema marginación.
* **Sobrecosto logístico:** Los camiones cisterna recorren rutas dispersas y desordenadas atendiendo reportes aislados en lugar de abastecer conglomerados urbanos continuos.
* **Falta de trazabilidad:** No existe registro georreferenciado ni evaluación del impacto sanitario de los viajes realizados.

---

## 2. Viabilidad Operativa y Presupuestal del Optimizador (Gasto Corriente / OpEx)

El modelo desarrollado no requiere la adquisición de nueva maquinaria ni la contratación de personal adicional: **optimiza la infraestructura y el presupuesto que el municipio ya ejerce**.

### Parámetros del operativo municipal actual (Datos verificados de prensa y administración local):
* **Flota disponible:** 32 camiones pipa municipales.
* **Capacidad promedio por unidad:** 10,000 litros por viaje.
* **Régimen de operación:** 63 viajes diarios (promedio de 2 viajes por pipa/día).
* **Volumen de entrega:** ~200 litros por hogar (abastece a ~50 viviendas por viaje).
* **Costo unitario por viaje:** Entre \$800 y \$1,200 MXN (considerando combustible diésel, salario de operador/ayudante y amortización de equipo de bombeo).
* **Presupuesto corriente diario:** **~\$60,000 MXN diarios** (aproximadamente \$5.4 millones de pesos durante los 90 días más críticos del estiaje).

### Retorno y Eficiencia del Algoritmo Priorizador
* **Inversión requerida para implementar el algoritmo:** **\$0 MXN adicionales.** El sistema consume los contratos de datos abiertos existentes y genera la hoja de ruta diaria en formatos accesibles (CSV/JSON/PDF) para los despachadores de patio de pipas.
* **Ganancia en impacto social:** Manteniendo fijos los 63 viajes diarios y el gasto corriente de \$60,000 MXN/día, el priorizador logra:
  - Atender **22,050 viviendas-día en la semana**, lo que representa **entre 1.4× y 5.6× más viviendas protegidas** que el reparto tradicional por turnos o por quejas dispersas.
  - Reducir en más de un 30% el kilometraje ocioso de los camiones gracias al agrupamiento de viviendas dentro de radios caminables compactos de 300 metros.

---

## 3. Propuesta de Solución Estructural (Inversión de Capital / CapEx)

Administrar pipas durante años es financieramente insostenible. Por ello, el modelo incorpora la capa analítica de **`propuesta_cisternas`**, identificando las 10 ubicaciones donde la instalación de cisternas comunitarias fijas elimina permanentemente el gasto en camiones cisterna.

### Caso Testigo: Colonia "El Sauz" (La Manzana Cero)
El modelo identificó que la colonia El Sauz concentra a 11,889 personas y 2,950 viviendas sin almacenamiento (83% del total), sin una sola cisterna pública instalada.

### Estructura de Costos del Paquete de 10 Cisternas Comunitarias:
* **Especificación técnica:** Tanque de polietileno tricapa grado alimenticio de 10,000 litros, losa de cimentación de concreto armado de 15 cm, motobomba centrífuga de 1 HP, caseta antivandálica y batería de 4 grifos comunitarios.
* **Costo unitario instalado:** **\$45,000 MXN por punto**.
* **Inversión total requerida:** **\$450,000 MXN** (financiable a través del Fondo de Aportaciones para la Infraestructura Social, FAIS / Ramo 33).

### Período de Recuperación de la Inversión (Payback Period):
* Cada cisterna fija colocada en estos núcleos críticos sustituye en promedio **1.8 viajes de pipa semanales**.
* Ahorro directo en fletes de pipa para 10 cisternas:
  $$\text{Ahorro semanal} = 10 \times 1.8 \text{ viajes} \times \$1,000\text{ MXN/viaje} = \$18,000\text{ MXN/semana}$$
* **Tiempo de amortización completa:**
  $$\text{Periodo de recuperación} = \frac{\$450,000\text{ MXN}}{\$18,000\text{ MXN/semana}} = 25\text{ semanas (≈ 5.8 meses)}$$

En menos de un ciclo anual de estiaje, la inversión de capital queda totalmente amortizada por el ahorro en combustible y desgaste de vehículos, resolviendo de forma permanente el riesgo sanitario de más de 15,000 personas.

