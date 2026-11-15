# 1. Introducción y Caracterización del Problema
*(Texto para las Secciones 1.1 y 1.2 del Formato Oficial de Reporte Científico de SOLACYT)*
*Extensión: 496 palabras (contadas el 14-nov, sin este encabezado).*

---

### 1.1 Justificación: La Trampa del Tubo
Desde el 15 de octubre de 2026, el Sistema Intermunicipal de los Servicios de Agua Potable y Alcantarillado (SIAPA) aplica en el Área Metropolitana de Guadalajara (ZMG) un programa de rotación del servicio en 627 colonias, agrupadas en siete zonas que abastecen los acueductos de la Planta Potabilizadora No. 1 de Miravalle (alrededor del 42% de su cobertura; El Informador, 5-nov-2026). Con el calendario vigente desde el 4 de noviembre, las zonas de Tlaquepaque tienen de tres a cuatro días seguidos de racionamiento por semana. El SIAPA lo describe como baja de presión, no como corte total, y advierte que las colonias más alejadas o más altas tardan más en recuperar el servicio. Cuánta agua llega en esos días no está medido: el modelo supone, como peor caso, que no llega nada, y en la sensibilidad deja llegar hasta la mitad.

No obstante, las políticas públicas y los índices oficiales evalúan el acceso al agua mediante una métrica de infraestructura estática: la conexión física a la red pública entubada. En San Pedro Tlaquepaque, el Consejo Nacional de Población (CONAPO, 2020) clasifica al municipio con marginación "Muy Baja" y reporta que solo el 0.57% de los ocupantes carece de agua entubada (indicador OVSAE). Esta premisa asume que contar con tubería garantiza la disponibilidad del recurso. Sin embargo, bajo un régimen de suministro intermitente, la tubería no abastece en los periodos de corte; la disponibilidad efectiva del agua depende exclusivamente de la capacidad de almacenamiento doméstico (tinacos y cisternas).

### 1.2 Planteamiento del Problema y Delimitación Territorial
Al procesar los microdatos del Censo de Población y Vivienda 2020 (INEGI) a escala de manzana urbana, se evidencia una brecha desatendida: entre 21,775 y 41,879 viviendas habitadas en Tlaquepaque (13.8% a 26.5% de las 158,135 viviendas urbanas con datos) carecen de tinaco y cisterna. Tlaquepaque encabeza la proporción de viviendas sin almacenamiento de los cuatro municipios del SIAPA en ambas cotas: Guadalajara registra entre 3.1% y 9.3%, mientras que con Tonalá los intervalos se traslapan (8.5% a 20.3%; `datos/comparacion_municipios.md`). Para estas familias —entre 77,618 y 157,259 personas— la baja de presión representa desabasto inmediato y crítico (cero litros de reserva propia).

El presente estudio delimita su alcance a las colonias de San Pedro Tlaquepaque integradas en el programa oficial de rotación del SIAPA (Zonas 3, 4, 5 y 6). Este polígono abarca a 462,194 habitantes (78.6% del municipio con ubicación, con un rango de respaldo documental entre 63% y 79%; `datos/zonas_siapa/LEEME.md`). Las colonias del programa concentran entre el 80% y 82% del desabasto municipal; a su vez, dentro del programa, las Zonas 5 y 6 agrupan entre el 63.0% (cota máxima) y el 72.6% (cota mínima) de las viviendas sin almacenamiento.

Debido a que el Censo de INEGI no cruza la posesión simultánea de tinaco y cisterna en un mismo predio, todos los resultados se expresan bajo la regla de dos cotas: cota mínima (asumiendo nulo traslape entre depósitos) y cota máxima (asumiendo traslape total).
