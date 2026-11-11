#!/usr/bin/env python3
"""
Extrae la lista de colonias por zona del PDF oficial del SIAPA.

    https://rotaciondeserviciosiapa.jalisco.gob.mx/pdf/colonias_siapa.pdf

    python3 scripts/extrae_lista_pdf.py PDF SALIDA.csv

Cada página trae un encabezado "Zona N - Municipio", la línea de días de baja
presión y de una a tres columnas de nombres. Una barra lateral decorativa mete
"Zona 1" ... "Zona 7" entre los nombres: se descarta. Un asterisco al final del
nombre significa "colonia abastecida por varios acueductos, distribuida en varias
zonas" y se guarda en la columna `multizona`.

Salida: zona, municipio, colonia, multizona, dias_baja_presion, pagina, nombre_dudoso

Los nombres de Tlaquepaque se verificaron contra el archivo del equipo (scripts/verifica_lista_pdf.py).
Los de otros municipios pueden salir corruptos: quedan marcados con nombre_dudoso=1 y no se usan.
"""
import csv
import re
import sys

import pdfplumber

# La barra lateral decorativa ("Zona 1".."Zona 7") se superpone a algunos nombres y mezcla las letras, y
# unos pocos van con letras espaciadas. Se corrigen a mano, solo los de Tlaquepaque, que es lo que usa
# el proyecto. Cada corrección se verificó contra el texto de `pdftotext -layout` y contra la lista del equipo.
CORRECCIONES = {
    "ZFoRnAaC 3CIONAMIENTO RESIDENCIAL ARRAYANES": "FRACCIONAMIENTO RESIDENCIAL ARRAYANES",
    "ZFoRnAaN 4CISCO SILVA ROMERO": "FRANCISCO SILVA ROMERO",
    "ZoGnaU 4ADALUPE EJIDAL": "GUADALUPE EJIDAL",
    "ZoInNaD 2IGENA DE SAN SEBASTIANITO": "INDIGENA DE SAN SEBASTIANITO",
    "ZoJnAaR 3DINES TOLUQUILLA": "JARDINES TOLUQUILLA",
    "C I U D A D D E L S O L": "CIUDAD DEL SOL",
    "M I R A D O R D E L T E S O R O": "MIRADOR DEL TESORO",
    "R INCONADA DE LOS ENCINOS": "RINCONADA DE LOS ENCINOS",
    "T L A QUEPAQUE PUEBLITO CONDOMINIO": "TLAQUEPAQUE PUEBLITO CONDOMINIO",
}

ENC = re.compile(r"Zona\s+(\d)\s*-\s*(.+)")


def lineas(palabras, tol=6):
    """Agrupa palabras en renglones por cercanía vertical."""
    filas = []
    for w in sorted(palabras, key=lambda w: (w["top"], w["x0"])):
        if filas and abs(filas[-1][0] - w["top"]) <= tol:
            filas[-1][1].append(w)
        else:
            filas.append([w["top"], [w]])
    return [(t, sorted(ws, key=lambda w: w["x0"])) for t, ws in filas]


def sin_barra_lateral(palabras):
    """Quita 'Zona' y el dígito que le sigue en el mismo renglón."""
    fuera = set()
    for i, w in enumerate(palabras):
        if w["text"] == "Zona":
            for j, v in enumerate(palabras):
                if j != i and v["text"].isdigit() and len(v["text"]) == 1 \
                        and abs(v["top"] - w["top"]) <= 3 and 0 <= v["x0"] - w["x1"] <= 40:
                    fuera.add(j)
            fuera.add(i)
    return [w for i, w in enumerate(palabras) if i not in fuera]


def pagina(p):
    ws = [w for w in p.extract_words() if w["x0"] >= 0 and w["x1"] <= p.width]  # hay texto fuera de la página
    texto = " ".join(w["text"] for w in ws[:40])
    m = ENC.search(texto)
    if not m:
        return None
    zona, muni = m.group(1), m.group(2).split("Días")[0].strip()
    dias = None
    top_dias = None
    for t, fila in lineas(ws):
        s = " ".join(w["text"] for w in fila)
        if s.startswith("Días de baja presión"):
            dias = s.split(":", 1)[1].strip()
            top_dias = t
            break
    cuerpo = [w for w in ws if w["top"] > top_dias + 10 and w["text"] != "*Tu"]
    # el pie de página empieza en "*Tu colonia se abastece"
    pie = [w["top"] for w in ws if w["text"].startswith("*Tu")]
    if pie:
        cuerpo = [w for w in cuerpo if w["top"] < min(pie) - 5]
    cuerpo = sin_barra_lateral(cuerpo)
    # Dos columnas. La de la derecha empieza donde se agrupan más inicios de renglón entre x=450 y x=700
    inicios = {}
    for _, fila in lineas(cuerpo):
        for a, b in zip(fila, fila[1:]):
            if 450 <= b["x0"] <= 700 and b["x0"] - a["x1"] > 25:
                k = round(b["x0"] / 10) * 10
                inicios[k] = inicios.get(k, 0) + 1
    derecha = min(w["x0"] for w in cuerpo) if not inicios else None
    if inicios:
        k = max(inicios, key=inicios.get)
        derecha = min(w["x0"] for w in cuerpo if abs(w["x0"] - k) <= 30 and w["x0"] >= 450) - 5
    nombres = []
    for lado in (0, 1):
        for _, fila in lineas(cuerpo):
            palabras = [w for w in fila if (w["x0"] >= derecha) == bool(lado)]
            if palabras and (lado == 0 or inicios):
                nombres.append(" ".join(w["text"] for w in palabras))
    return zona, muni, dias, nombres


def main(pdf, salida):
    filas = []
    with pdfplumber.open(pdf) as doc:
        for n, p in enumerate(doc.pages, 1):
            r = pagina(p)
            if not r:
                continue
            zona, muni, dias, nombres = r
            for nom in nombres:
                multi = nom.rstrip().endswith("*")
                limpio = nom.strip().rstrip("*").strip()
                limpio = CORRECCIONES.get(limpio, limpio)
                filas.append({"zona": zona, "municipio": muni, "colonia": limpio,
                              "multizona": "1" if multi else "0", "dias_baja_presion": dias, "pagina": n})
    raros = []
    for f in filas:
        f["nombre_dudoso"] = "1" if re.search(r"[a-z]| .( .)+ ", f["colonia"]) else "0"
        if f["nombre_dudoso"] == "1":
            raros.append(f)
    for f in raros:
        print(f"AVISO nombre dudoso (pagina {f['pagina']}, {f['municipio']}): {f['colonia']!r}", file=sys.stderr)
    with open(salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["zona", "municipio", "colonia", "multizona", "dias_baja_presion", "pagina", "nombre_dudoso"])
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} colonias, {len({(f['zona'], f['municipio']) for f in filas})} secciones", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
