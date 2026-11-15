# Correcciones del 14-nov-2026 (Magui)

Qué se cambió, por qué, y qué queda pendiente. Todo sale de la lista de correcciones
que juntó el equipo después del merge del PR #10 (`docs/reporte-resultados-analisis`).

## 1. Secciones del reporte corregidas

| Archivo | Qué cambió |
|---|---|
| `reporte/01_CARACTERIZACION_PROBLEMA.md` | Cifras con **las dos cotas** (sin tinaco ni cisterna: 21,775 a 41,879 viviendas, 13.8% a 26.5% de 158,135; 77,618 a 157,259 personas). 462,194 personas en el programa (78.6%). Zonas 5 y 6: 72.6% (cota mínima) a 63.0% (cota máxima) del riesgo dentro del programa. Se declara que el rango de Tonalá (8.5% a 20.3%) **se traslapa** con el de Tlaquepaque. El racionamiento se llama como lo llama el SIAPA: **"baja de presión"**, no corte total |
| `reporte/ANEXO_B_PROCEDENCIA_DATASETS.md` | Salvedad del Dataset 01. El mapa de cisternas del municipio (Google My Maps) **no trae capacidad ni estado de operación**: solo ubicación |
| `reporte/ANEXO_C_AREAS_CONOCIMIENTO.md` | Se quitaron conceptos que el modelo no implementa ("ventanas de servicio", "recuperación de presión"). U = 48 h se atribuye a Matsinhe 2014 (Maputo) y el contexto local a Rubino 2019 |
| `reporte/FUENTES_LITERATURA_TINACOS_CONSUMO.md` | Se quitaron las referencias que no se pudieron verificar. Quedan las 6 arbitradas leídas completas (Rubino 2019, Ercumen 2015, Taylor 2018, Wu 2023, Leifels 2025, Sosa-Moreno 2025), más Kumpel y Nelson 2014/2016 (solo resumen/suplemento), Matsinhe 2014 y OMS 2017. Tinaco de 1,100 L y 750 L se declaran **supuestos comerciales**, no dato medido. 50 L/persona/día es el extremo **cómodo** de la sensibilidad |

`reporte/LEEME.md` ya no las marca como "pendiente de corrección".

## 2. Corrección en el registro de evidencia (S001 y P017)

**Síntoma:** `motor/test_referencia.py` fallaba con `AssertionError: '' != 'si' : S001`.

**Causa:** el commit `c60be31` (app `/mi-casa`) agregó dos renglones con
`verificacion = resumen_oficial`. Según `contratos/evidencia.schema.json`, ese nivel es
**solo para artículos arbitrados** de los que se leyó el resumen de PubMed o del editor.
Ninguno de los dos es un artículo.

| Renglón | Antes | Ahora | Razón |
|---|---|---|---|
| S001, cloro (CDC, *How to Make Water Safe in an Emergency*) | `resumen_oficial` | `fuente_primaria` | Es una guía de una agencia, no un artículo. La nota del renglón trae detalle de la propia página (dosis para 5–6% y 8.25%) |
| P017, TlaqueChat (La Crónica, 14-oct) | `resumen_oficial` | `solo_resumen` | La nota del renglón dice "visto en el resultado de búsqueda, falta leer la nota completa": eso es exactamente `solo_resumen` |

Se cambió en `scripts/genera_evidencia.py` y se regeneraron `datos/evidencia.csv` y
`fixtures/evidencia.fixture.csv` con el script (no a mano). Siguen 101 renglones y las
cisternas no cambian (35 coordenada exacta, 12 centro de colonia, 3 sin ubicar).
**No se tocó ningún contrato.**

## 3. Cómo comprobarlo

```
python -m pip install -r scripts/requirements.txt   # numpy, pandas, geopandas... (test_sensibilidad los necesita)
python scripts/genera_evidencia.py
python -m unittest discover -s motor -p "test_*.py"
```

Resultado el 14-nov: **59 pruebas, OK** (42 de `test_referencia.py` + las de sensibilidad).

## 4. Pendientes (para Migue)

1. **S001:** confirmar que se leyó la página del CDC completa. Si no, bajarla a `solo_resumen`.
2. **P017 / número de TlaqueChat:** con `solo_resumen` no se puede citar (regla del contrato).
   Además, `decisiones/referencias-y-prensa.md` dice: *"Las notas del 15 y del 22 publican números
   que difieren en un dígito. **No citar el número**"*, pero `app/src/app/mi-casa/page.tsx` (línea 93)
   muestra `33 2804 8171`. Opciones: confirmar el número en el sitio oficial del municipio y subir P017
   a `fuente_primaria`, o quitar el número y dejar solo "TlaqueChat, el WhatsApp del ayuntamiento".
   Que TlaqueChat **existe** sí está respaldado: la nota del 15-oct, leída completa, lo menciona.
3. **Cloro:** contrastar la dosis del CDC con una guía de la Secretaría de Salud (lo dice la nota de S001).


---

# Segunda ronda (noche del 14-nov), 

| # | Corrección | Qué se hizo |
|---|---|---|
| a | Anexo B decía que la equivalencia del Dataset 01 "se consultó con el comité de SOLACYT". No hay constancia (`auditoria/auditoria-kit.md`: "Falta preguntar a SOLACYT") | Ya no menciona al comité. La salvedad explica, en términos técnicos, que se usó el producto "Principales resultados por AGEB y manzana urbana" del mismo Censo 2020, con las mismas variables de vivienda y más resolución. La nota 1 del anexo también se corrigió: decía que el respaldo era el "Dataset 02 (Marco Geoestadístico)", pero el #02 del catálogo es el CNGMD 2023 y aún no está en el repo. Ahora dice que se usan el #01 y el #17, y que el #02 se revisó pero no se incorporó |
| b | Sección 1.1 decía "dos a cuatro días continuos sin agua en la llave" | Reescrita: con el calendario vigente las zonas de Tlaquepaque (3 a 6) tienen **tres a cuatro** días seguidos de racionamiento; el SIAPA lo llama baja de presión, no corte total; "sin agua" es el **peor caso del modelo** y la sensibilidad deja llegar hasta la mitad (`f` de 0 a 0.5). Se quitó "fallas en la Planta Miravalle", que ninguna fuente del repo respalda |
| c | Anexo C hablaba de "dinámica del cloro residual", de "integrar" la NOM-127 y de recomendaciones de la OMS en *Mi Casa* | Ahora dice que el modelo **no simula cloro**: U = 48 h es un parámetro (sensibilidad 24 a 72 h) y la NOM-127 es el marco de referencia. *Mi Casa* cita al **CDC** (S001), no a la OMS. También se precisó Rubino: "la mitad de los tinacos de azotea muestreados excedió coliformes totales", piloto de 51 casas |
| d | Anexo C presentaba "1.4× y 5.6×" como general | Ahora: es del **escenario base** (`optimizador/resultados/resumen.md`); en las esquinas adversas baja a **1.2×** (cota mínima) y **1.1×** (cota máxima), igual que `optimizador/docs/viabilidad-presupuestal.md` |
| e | "Planta Miravalle" sin renglón de evidencia | Nuevo renglón **P018** (El Informador, 5-nov-2026, nota completa leída): 627 colonias, siete zonas, Planta Potabilizadora No. 1 de Miravalle, ~42% de la cobertura del SIAPA. Se cita en la sección 1.1 y en el Anexo C |
| f | La sección 1 decía ~420 palabras y medía 446 | Recontada después de los cambios: **496 palabras**; el encabezado lo dice así |

`datos/evidencia.csv` pasa de 101 a **102 renglones** (fixture: 47), regenerado con `scripts/genera_evidencia.py`.
Pruebas: **59, OK**. No se tocó ningún contrato.
