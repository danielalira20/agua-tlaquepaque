# Dataset 17 — Marginación (CONAPO): lo que se obtuvo y lo que falta

## Estado: parcial. Falta un archivo que hay que bajar a mano.

| Nivel | Formato | ¿Se obtuvo? |
|---|---|---|
| Entidad federativa 2020 | `.xlsx` | Sí |
| **Municipio 2020** | `.xlsx` | **Sí** |
| **AGEB urbana 2020** | `.zip` | **No** |
| Colonia 2020 | `.zip` | No |

CONAPO publica los niveles AGEB y colonia **únicamente** como `.zip`, y su servidor
responde con una página de error a las peticiones de `.zip` desde esta sesión. Los
`.xlsx` del mismo servidor descargan sin problema, así que no es un archivo caído:
es el filtro del sitio. **Desde un navegador normal la descarga funciona.**

### Lo que hay que hacer, y toma un minuto

1. Abrir https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372
2. Bajar **"Base de datos a nivel AGEB 2020"** (`IMU_2020.zip`)
3. Dejarlo en `datos/raw/IMU_2020.zip`

Con eso se procesa el cruce por AGEB, que es determinista: el AGEB sale de los
primeros 13 caracteres del `cvegeo` de cada manzana, sin empatar nombres.

---

## El hallazgo del nivel municipal, que vale por sí solo

El archivo municipal sí se obtuvo, y dice algo que conviene al reporte.

| Municipio | Población | Grado de marginación | Lugar estatal | Lugar nacional |
|---|---:|---|---:|---:|
| Guadalajara | 1,385,629 | Muy bajo | 125 de 125 | 2,456 de 2,469 |
| Zapopan | 1,476,491 | Muy bajo | 124 | 2,454 |
| **San Pedro Tlaquepaque** | **687,127** | **Muy bajo** | **123** | **2,424** |
| Tonalá | 569,913 | Muy bajo | 119 | 2,378 |

*(Número alto significa menos marginado.)*

**Oficialmente, Tlaquepaque es uno de los municipios menos marginados de México.**
Lugar 2,424 de 2,469. Y el indicador de agua del propio índice lo confirma:

> **OVSAE, ocupantes en viviendas sin agua entubada: 0.57%**

Es decir, para el índice oficial de vulnerabilidad, en Tlaquepaque prácticamente
nadie tiene problema de agua.

### Y aquí está el contraste

| Fuente | Qué mide | Resultado |
|---|---|---|
| CONAPO, OVSAE | Viviendas **sin tubo** | 0.57% |
| Nuestro análisis | Viviendas **sin dónde guardar** | **13.8% a 26.5%** |

Entre 21,775 y 41,879 de las 158,135 viviendas de Tlaquepaque no tienen tinaco ni
cisterna. El índice oficial no las ve, porque **mide el tubo, no el almacenamiento.**

Es la tesis del proyecto confirmada por el propio instrumento oficial: cuando el
agua llega por turnos, tener tubo deja de significar tener agua, y ningún índice
de marginación vigente capta esa diferencia.

### Un segundo argumento: el nivel municipal no discrimina

Los cuatro municipios del calendario del SIAPA son "Muy bajo" y están pegados entre
sí (lugares 119 a 125 de 125). **El índice municipal no sirve para priorizar dentro
de la zona de estudio.** Por eso hace falta el archivo a nivel AGEB: es el único que
permite distinguir entre colonias de un mismo municipio.

---

## Cómo queda el requisito obligatorio del kit

El dataset 17 es uno de los dos obligatorios. En el peor caso, con solo el archivo
municipal, **el requisito igual se cumple**, porque se usa en la caracterización del
problema: es el que demuestra que el índice oficial no ve el problema que estamos
midiendo. Esa era justamente la mitigación propuesta en `decisiones/propuesta-dani.md`
para que el dataset no dependiera únicamente del optimizador.

Con el archivo de AGEB se gana además el peso de vulnerabilidad para la función
objetivo del priorizador. Sin él, hay que usar un proxy construido con variables del
Censo que ya tenemos, y declararlo.

## Archivos

- `marginacion_municipal.csv` — los cuatro municipios del calendario del SIAPA con
  sus indicadores, índice, grado y lugar
