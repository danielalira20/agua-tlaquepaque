# Zonas de racionamiento del SIAPA por manzana

Resuelve el cruce que faltaba para correr el motor: **en qué zona está cada manzana**.
Es lo único que une el Censo (por manzana) con el calendario del SIAPA (por colonia y
zona).

Se regenera con:

    pip install -r scripts/requirements.txt
    python3 scripts/asigna_zonas.py

## Archivos

| Archivo | Qué es |
|---|---|
| `manzana_zona.csv` | **El resultado.** Una fila por manzana, con su zona, de dónde salió y qué tan firme es. Es compatible con `motor/referencia.py --zonas` |
| `resumen_zonas.csv` | Manzanas, personas y viviendas por zona y nivel de confianza |
| `pendientes_revision.csv` | Lo que hay que mirar contra el PDF original (ver abajo) |
| `equivalencias_nombres.csv` | 17 emparejamientos de nombres revisados a mano, cada uno con su motivo |
| `colonias_siapa.pdf` | **El documento oficial** (`rotaciondeserviciosiapa.jalisco.gob.mx/pdf/colonias_siapa.pdf`, descargado el 11-nov-2026). Colonias por zona y municipio, con los días de baja presión. Metadatos del archivo: creado el 30-oct-2026 |
| `lista_oficial_pdf.csv` | Extracción propia del PDF (`scripts/extrae_lista_pdf.py`). Los nombres dudosos de otros municipios van marcados |
| `lista_oficial_colonias.csv`, `.json` | La misma lista, extraída por el equipo. **Verificada contra el PDF para Tlaquepaque: las 115 filas coinciden en nombre y zona** (`scripts/verifica_lista_pdf.py`). Es la que usa `asigna_zonas.py` |
| `portal_rotacion.topo.json` | Polígonos de colonias y zonas del portal oficial `rotaciondeserviciosiapa.jalisco.gob.mx`, leídos el 11-nov-2026 |
| `portal_ajustes_vigente.json`, `portal_ajustes_original.json` | Días de racionamiento por zona, vigente (3-nov) y original (15-oct) |

## Por qué hacen falta dos fuentes

| | Da | No da |
|---|---|---|
| **Lista oficial** | El nombre de la colonia y su zona, según el documento del SIAPA | Geometría |
| **Polígonos del portal** | Geometría, y una zona por colonia | La zona es "el cruce original del mapa" (un cálculo geométrico), no la lista |

Ninguna alcanza sola. La lista no se puede ubicar en el mapa y el portal puede incluir
colonias que la lista no tiene.

## La regla

Por cada polígono del portal que contiene manzanas de Tlaquepaque:

1. **Contraparte en la lista:** nombre exacto (sin acentos ni puntuación) y municipio de
   la lista dentro de la etiqueta del polígono. El portal etiqueta `San Pedro Tlaquepaque
   y Tonalá` a las colonias que cruzan el límite. Si no, la tabla de equivalencias.
2. **No se aceptan parecidos automáticos.** Hay colonias distintas con el mismo nombre
   (El Mirador de Tlaquepaque y El Mirador de Guadalajara) y otras casi iguales que no lo
   son (`Santa Anita` no es `Santa María`; `Parques del Bosque` no es `Jardines del Bosque`).
3. Con contraparte: si el portal no da zona, se usa la de la lista; si coinciden o se
   traslapan, la intersección; si no tienen **ninguna zona en común, se usan las dos como
   rango** y se marca `conflicto`.
4. Sin contraparte: la zona del portal tal cual.
5. Sin zona en ninguna fuente: fuera del programa.

## Niveles de confianza

Todo Tlaquepaque, 587,874 personas en 4,863 manzanas con ubicación:

| Confianza | Qué significa | Personas | % |
|---|---|---:|---:|
| **alta** | El portal y la lista coinciden | 342,310 | 58.2% |
| **media** | Solo la lista da zona (el portal no) | 17,569 | 3.0% |
| **conflicto** | Se contradicen. Se usan las dos zonas | 8,232 | 1.4% |
| **baja** | Solo el polígono del portal; la colonia no está en la lista | 93,901 | 16.0% |
| ambiguo | La manzana toca 2 o más polígonos | 182 | 0.0% |
| ninguna | Fuera del programa según las dos fuentes | 123,777 | 21.1% |
| sin_poligono | No se pudo ubicar la manzana | 1,903 | 0.3% |

**Dentro del programa: 462,194 personas (78.6%).** De ellas, 368,111 (62.6% de Tlaquepaque)
tienen respaldo de la lista oficial y 94,083 (16.0%) dependen solo del portal. Por eso la
cobertura del programa se debe presentar **como rango: entre 63% y 79%**.

## Lo que hay que saber

1. **Las dos fuentes no coinciden para una parte grande de la población.** El 16% de
   las personas de Tlaquepaque (confianza `baja`) vive en polígonos que tienen zona en el
   portal pero ningún nombre en la lista, ni siquiera tras la tabla de equivalencias.
   Incluye `Centro` (8,630 personas), `Camichines` (8,484) y `Parques del Bosque` (7,799).
   De las 15 colonias con más viviendas sin almacenamiento dentro del programa, 11 tienen
   respaldo de la lista (10 con confianza alta y El Vergel con media) y 4 dependen solo
   del portal (Parques del Bosque, Geo Villas Los Olivos III, Miraflores y Miravalle).
2. **Los conflictos son tres colonias:** El Tapatío (portal: zona 4; lista: zona 3), San
   Juan (portal 3; lista 4) y un pedazo de El Sauz (portal 4; lista 6). El Tapatío es una
   colonia grande y bien puede estar partida entre dos zonas.
3. **Hay polígonos que el PDF no nombra.** Seis polígonos de Tlaquepaque sin zona en el portal
   comparten nombre con colonias del PDF de otro municipio (`La Duraznera` está en Guadalajara,
   `La Guadalupana` en Tonalá, `Miraflores` en Zapopan...). Podrían ser la misma colonia o no.
   8,906 personas. No se aceptaron sin corroboración.
4. **El conteo no cuadra con la prensa.** La lista trae 661 filas y 612 nombres únicos;
   la prensa reportó 627 colonias.
5. **La lista ya está verificada contra el PDF oficial, y eso deja claro qué es el 16%.**
   Las colonias de confianza `baja` **no aparecen en el PDF en ningún municipio** (se buscaron
   `Centro` de Tlaquepaque, `Parques del Bosque`, `Geo Villas`, `Parques de La Victoria`, `Parques del Palmar`, `Paseos
   del Prado`, `Artesanos` y `Felipe Ángeles`). Su zona del portal sale solo del cálculo
   geométrico del mapa. No sabemos si el SIAPA las raciona; sabemos que su propio documento
   de colonias no las nombra.
6. **El calendario puede volver a cambiar.** El SIAPA lo modificó el 4 de noviembre y el
   portal dice que se "podrá ajustar". Los calendarios están versionados en `motor/calendarios/`.

## Qué sale de aquí

`../HALLAZGOS_zonas.md` (riesgo por zona, contraste con cisternas, motor una semana) y
`riesgo_por_zona.csv`, `motor_semana.csv`, generados por `scripts/recalcular_hallazgos.py`.

## Lo que queda por hacer

- Preguntar al SIAPA (o a quien publicó el portal) si las colonias que el PDF no nombra pero el
  mapa sí ubica en una zona reciben racionamiento. Es lo que decide si el 16% cuenta.
- Revisar `pendientes_revision.csv`, en particular las 12 filas `portal_sin_lista_con_homonimo`
  y las 6 `sin_zona_con_homonimo`.
- Decidir qué hacer con las 8 manzanas del Censo que no tienen polígono en el Marco
  Geoestadístico: el motor las trata como fuera del programa.
