# 4. Resultados
*(Texto listo para incorporar en la Sección 4 del Formato Oficial de Reporte Científico de SOLACYT)*
*Extensión controlada: ~287 palabras (presupuesto: 280). Se cuenta el cuerpo, sin el título ni esta nota.*

---

Se evaluó el priorizador con la semana del 9 al 15 de noviembre de 2026 (motor de referencia). Ambos disponen de los mismos 441 viajes de pipa (63 diarios, 50 hogares cada uno). El baseline es estilizado: reparte esos viajes por turnos entre las 47 cisternas instaladas que pudieron ubicarse; su variante «con necesidad» visita solo las que tienen viviendas sin agua cerca ese día. Toda cifra va con la cota mínima y la máxima, que equivalen a 58,906 y 128,460 viviendas-día sin agua.

Con los mismos viajes, el priorizado atiende 22,050 viviendas-día. El baseline por turnos atiende 4,532 con la cota mínima y 10,177 con la máxima: el priorizado lo supera entre 2.2 y 4.9 veces. Contra el baseline con necesidad, la comparación más exigente, la ventaja es de 3.1 veces con la cota mínima y de 1.4 con la máxima; en las esquinas adversas de la sensibilidad del motor (consumo de 100 a 150 L y tinacos menores) baja a 1.2 y 1.1. Cada día, los viajes cubren 34.2% a 40.5% de las viviendas sin agua con la cota mínima y 16.1% a 18.3% con la máxima.

La marginación no pesa en la prioridad. En las AGEB de marginación «Muy alto», el priorizado atiende 261 de 973 viviendas-día con la cota mínima (baseline por turnos: 320) y ninguna de 2,091 con la máxima (661). En cambio, las AGEB «Alto» y «Muy alto» juntas reciben 5,796 viviendas-día contra 1,752 con la cota mínima, y 8,728 contra 2,763 con la máxima.

A 1,200 pesos por viaje (precio de una pipa particular; Milenio, 2025), los 441 viajes cuestan 529,200 pesos: 24.0 pesos por vivienda-día atendida con el priorizado, contra 33.2 a 116.8 con los baselines de 47 cisternas.

---

## Trazabilidad (no va en el reporte)

Todas las cifras salen de `optimizador/resultados/resumen.md`, que se regenera con `python3 -m optimizador.analisis`.

| Cifra | Dónde |
|---|---|
| 441 viajes, 63 diarios, 50 hogares, 47 cisternas | Encabezado y sección 1; `optimizador/ESPECIFICACION.md`, sección 7 |
| 58,906 y 128,460 viviendas-día sin agua; 22,050; 4,532; 10,177; 2.2× y 4.9× | Sección 1 |
| 3.1× y 1.4× (baseline con necesidad, 47 cisternas) | Sección 1 |
| 1.2× y 1.1× en esquinas adversas | Sección 3 (`esquina_adversa` y `esquina_adversa_extrema`); consumo y tinaco de cada esquina, al pie de la sección 3 |
| 34.2% a 40.5% y 16.1% a 18.3% de cobertura diaria | Sección 5 |
| 261 de 973; 320; 0 de 2,091; 661; 5,796 contra 1,752; 8,728 contra 2,763 | Sección 4 |
| 1,200 pesos por viaje; 529,200; 24.0; 33.2 a 116.8 | Sección 6; precio: P012 de `datos/evidencia.csv` (Milenio, 16 de mayo de 2025) |
