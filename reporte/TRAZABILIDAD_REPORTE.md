# Reporte científico: trazabilidad y lista de cierre

El reporte es `REPORTE_CIENTIFICO.docx`. Su texto vive en un solo lugar, `fuente/contenido.js`; de ahí salen el Word,
la copia en texto (`REPORTE_CIENTIFICO.md`) y el conteo de palabras.

```
node reporte/fuente/cuenta_palabras.js    # conteo por sección; falla si se sale de los límites
node reporte/fuente/figura2_reparto.js    # regenera la Figura 2 desde optimizador/resultados/ (necesita playwright)
node reporte/fuente/genera_reporte.js     # escribe el .docx y el .md (necesita el paquete docx)
```

## 1. Formato oficial

| Regla | Estado |
|---|---|
| 1,500 a 2,000 palabras en total, con portada, títulos y bibliografía | **1,968** contando los campos por completar (margen de 32 para los nombres reales) |
| Resumen de 300 a 450 palabras | **318** |
| Arial 12, interlineado 1.5, dos columnas después del resumen | Sí (los pies de figura van en Arial 10) |
| Estructura: portada, resumen, 1 (1.1 a 1.4), 2, 3, 4, 5 (5.1), 6, 7, anexos | Sí. Los anexos A a H **todavía no están armados** |
| Al menos 5 referencias arbitradas, en APA y orden alfabético | 5 arbitradas leídas completas (Ercumen, Rubino, Sosa-Moreno, Taylor, Wu) más los 2 datasets del catálogo |

## 2. Por completar antes de entregar (resaltado en amarillo en el Word)

- Logotipo del concurso, número de proyecto, nombres completos, asesor, escuela, nivel, categoría y sede.
- **Volver a contar las palabras en Word** con los datos reales: el límite incluye la portada.
- Anexos A (credenciales, obligatorio), B y C (ya existen, con correcciones pendientes), D, E, F, G y H.
- La Figura 1 muestra la interfaz del PR #11 (`refactor/app`) con las correcciones de `fix/revision-refactor`.
  Si esa interfaz no se mezcla, hay que rehacer las capturas.
- El repositorio es privado: el reporte dice "reproducible", no "público". Si se abre, puede decirlo.

## 3. Dónde responde cada criterio del reto

| Criterio o indicación | Dónde se responde |
|---|---|
| C1. Caracterizar con datos de Jalisco | 1.2 y 4 (primeros dos párrafos) |
| C2 / I5. Prototipo funcional; lo simulado, declarado | Resumen, Figura 1, 3 (remite al Anexo F) |
| C3 / I2 / I3. Dos datasets del catálogo y cómo se usaron | 3, "Datos" (remite al Anexo B); bibliografía |
| C4 / I4. Tres áreas de conocimiento | 3, último párrafo (remite al Anexo C); 2 sostiene la de salud |
| C5. Viabilidad institucional y presupuestal | 5, "Viabilidad" (remite al Anexo H) y costo por vivienda-día en 4 |
| I1. Zona, por qué, quién lo usa, indicador | 1.2, "Delimitación", "Usuarios", "Indicador" |
| I6. Fuentes citadas y uso de IA declarado | 7 y 3 (remite al Anexo G) |

## 4. De dónde sale cada cifra

| Cifra | Fuente en el repo |
|---|---|
| 0.57% sin agua entubada (OVSAE) | `datos/marginacion_municipal.csv` |
| 13.8% a 26.5%; 21,775 a 41,879 viviendas; Guadalajara 3.1% a 9.3%; traslape con Tonalá | `datos/comparacion_municipios.md` |
| 77,618 a 157,259 personas sin reserva | `app/public/datos/real/manzanas.json` (viviendas sin almacenamiento × ocupantes) |
| 4,871 manzanas; 462,194 habitantes (78.6%); 62.6% con respaldo de la lista | `app/public/datos/real/meta.json`; `datos/zonas_siapa/LEEME.md` |
| Más de 600 colonias; siete zonas; rachas de cuatro días | `datos/zonas_siapa/LEEME.md` (612 nombres únicos); `datos/HALLAZGOS_sensibilidad.md` |
| Las cisternas se llenan cuando los vecinos reportan | `datos/evidencia.csv`, P006 (cita textual) |
| 17,420 a 34,429 viviendas sin almacenamiento en el programa; «muy bajo» 50.2% y 32.8%; zonas 5 y 6, 63.0% a 72.6% | `manzanas.json`; `datos/HALLAZGOS_marginacion.md` |
| 58,906 a 128,460 viviendas-día; 210 mil a 490 mil personas-día | `motor/test_referencia.py` (lo comprueba); `estado.json` |
| Calendario del 3 de noviembre: 1.5 veces las personas-día | `datos/HALLAZGOS_zonas.md` (210,116 contra 138,992; 490,320 contra 321,280) |
| Correlación de rangos mediana 0.65; 36 escenarios; 600 simulaciones | `datos/sensibilidad/RESUMEN.md`, `escenarios.csv`, `montecarlo.csv` |
| Núcleo de 186 manzanas, 3.8% del total, 54% de las viviendas-día; El Sauz primera en todas | `datos/HALLAZGOS_sensibilidad.md`; `datos/sensibilidad/manzanas_robustas.csv` |
| El Sauz sin cisterna ni propuesta; mediana 37 contra 59 | `datos/contraste_cisternas_programa.csv`; `datos/HALLAZGOS_cisternas.md` |
| 441 viajes; 63 diarios; 10,000 L; 200 L por hogar; radio de 300 m; 47 cisternas | `optimizador/ESPECIFICACION.md`; `optimizador/supuestos.json` |
| 22,050; 4,532 a 10,177; 2.2 a 4.9 veces; 1.4 a 3.1; 1.1 en el escenario más adverso | `optimizador/resultados/resumen.md`, secciones 1 y 3 |
| 1,200 pesos por viaje; 24 pesos contra 33 a 117; 529,200 pesos; 0.02% | `optimizador/docs/viabilidad-presupuestal.md`; `datos/evidencia.csv`, P012 y P014 |
| 16% a 41% de cobertura diaria | `optimizador/resultados/resumen.md`, sección 5 (34.2% a 40.5% y 16.1% a 18.3%) |
| «Muy alta» sin viajes con la cota máxima; «alta» y «muy alta» juntas reciben más | `optimizador/resultados/resumen.md`, sección 4 |
| 34,097 de 34,097 resultados; 109 pruebas | `app/scripts/verifica-vectores.ts`; 42 + 17 + 50 pruebas de `motor/` y `optimizador/` |
| Plan semanal en segundos; sitio estático | `optimizador/docs/viabilidad-presupuestal.md`, sección 4 |
| 36% contra 13%; tifoidea; sin diferencia en diarrea | `datos/evidencia.csv`, E013 a E015 |
| 65% fuera de norma; la mitad de los tinacos | `datos/evidencia.csv`, E001 y E002 |

## 5. Decisiones de redacción que conviene conocer

- **"Sin agua" siempre va con su supuesto.** El resumen y la metodología dicen que es corte total, la cota alta del daño.
- **La ventaja se da por referencia.** 2.2 a 4.9 veces es contra el reparto por turnos; 1.4 a 3.1 contra el que solo visita
  cisternas con necesidad; 1.1 es el peor escenario. Son las referencias con las 47 cisternas.
- **No se afirma que el riesgo esté en los más pobres.** Se dice lo contrario: el grado que más concentra es «muy bajo».
- **El SIAPA y la prensa van al Anexo B y al H**, no a la bibliografía, para que quepan las 5 arbitradas y los 2 datasets.
- **Kumpel y Nelson, Matsinhe y la OMS quedaron fuera del cuerpo.** Van en el Anexo C.
