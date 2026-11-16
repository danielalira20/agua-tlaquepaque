"""Video 1 · Inicio (versión aprobada como referencia de estilo).

Correr desde reporte/videos/editor/:  python voz.py guion_inicio.json voz_inicio  &&  python hacer_inicio.py
"""
import sys, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI); sys.path.insert(0, AQUI)
from motor2 import *

SRC = os.path.join(AQUI, "..", "Inicio.mov")
G = json.load(open("guion_inicio.json", encoding="utf-8"))
MASC = Image.open(os.path.join(AQUI, "..", "..", "..", "app", "public", "mascota", "tlacuache.webp")).convert("RGBA")
fu = {k: Fuente(SRC, a, b, f"cuadros_inicio/{k}") for k, (a, b) in {
    "hero": (0.0, 1.5), "puertas": (2.0, 4.6), "micasa": (5.0, 7.9), "mapa": (11.8, 13.95),
    "como": (17.0, 17.12), "cifras": (20.0, 27.6), "firmes": (29.0, 29.12)}.items()}
LLENO = (0, 0, SRC_W, SRC_H)

def T(k, m, d=0.0): return m.get(k, 0) + d  # momento en que empieza una frase dentro del beat

# ---------- beats ----------
def b_627(t, d, m):
    img = fondo()
    texto_animado(img, [[("DESDE EL 15 DE OCTUBRE", CELESTE)]], fuente(TXT, 36), t, 0.1, y=190)
    n = contador(627, t, 0.25, 1.4)
    texto_animado(img, [[(str(n), NARANJA)]], fuente(TIT, 300), t, 0.2, y=230, stagger=0)
    texto_animado(img, [[("colonias con ", BLANCO), ("tandeo", NARANJA)]], fuente(TIT, 80), t, 0.7, y=590)
    texto_animado(img, [[("Área metropolitana de Guadalajara · SIAPA", GRIS)]], fuente(TXTR, 32), t, 1.2, y=720)
    return img

def b_apertura(t, d, m):
    """Portada del video: la tesis del proyecto en grande, con la mascota."""
    img = fondo()
    texto_animado(img, [[("TANDEO EN SAN PEDRO TLAQUEPAQUE", CELESTE)]], fuente(TXT, 34), t, 0.05, x=260, y=235, alinear="izq")
    for i, (txt, c) in enumerate([("El mismo corte de agua", BLANCO), ("no le pega igual", NARANJA), ("a todas las casas.", BLANCO)]):
        texto_animado(img, [[(txt, c)]], fuente(TIT, 104), t, 0.25 + i * 0.3, x=260, y=300 + i * 130, alinear="izq", stagger=0.05)
    pegar(img, MASC, 1600, 600, t, 0.9, 330)
    return img

def casa(dr, cx, cy, s, color, tinaco, k):
    if k <= 0: return
    a = int(255 * k); off = 30 * (1 - k); cy += off
    cuerpo = [cx - s * 0.5, cy - s * 0.15, cx + s * 0.5, cy + s * 0.6]
    techo = [(cx - s * 0.62, cy - s * 0.1), (cx, cy - s * 0.6), (cx + s * 0.62, cy - s * 0.1)]
    if tinaco:
        dr.rectangle(cuerpo, fill=color + (a,)); dr.polygon(techo, fill=color + (a,))
        dr.rounded_rectangle([cx + s * 0.12, cy - s * 0.78, cx + s * 0.42, cy - s * 0.38], 10, fill=BLANCO + (a,))
        dr.rectangle([cx - s * 0.12, cy + s * 0.25, cx + s * 0.12, cy + s * 0.6], fill=NAVY1 + (a,))
    else:
        dr.rectangle(cuerpo, outline=color + (a,), width=9); dr.line(techo, fill=color + (a,), width=9, joint="curve")
        dr.rectangle([cx - s * 0.12, cy + s * 0.25, cx + s * 0.12, cy + s * 0.6], outline=color + (a,), width=7)

def b_uno_de_cuatro(t, d, m):
    img = fondo()
    texto_animado(img, [[("SAN PEDRO TLAQUEPAQUE", CELESTE)]], fuente(TXT, 36), t, 0.05, y=120)
    texto_animado(img, [[("Hasta ", BLANCO), ("1 de cada 4", NARANJA), (" casas", BLANCO)]], fuente(TIT, 104), t, 0.15, y=175)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa)
    for i in range(4):
        casa(dr, 600 + i * 240, 520, 150, CELESTE if i < 3 else NARANJA, i < 3, ease_out((t - 0.6 - i * 0.18) / 0.45))
    img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"))
    texto_animado(img, [[("sin ", NARANJA), ("tinaco ni cisterna", NARANJA)]], fuente(TXT, 34), t, 1.5, x=1220, y=680, alinear="izq")
    t3 = T("N3", m)
    texto_animado(img, [[("Día 1 de corte = ", BLANCO), ("un día sin agua.", NARANJA)]], fuente(TIT, 72), t, t3 + 0.1, y=790)
    return img

def b_pregunta(t, d, m):
    img = fondo()
    texto_animado(img, [[("¿Quién se queda", BLANCO)], [("sin agua hoy?", NARANJA)]], fuente(TIT, 124), t, 0.05, y=330, stagger=0.09)
    return img

def b_hero(t, d, m):
    img = fondo(); u = t / d
    cam = camara([(0, LLENO), (0.5, (120, 0, 2600, 1560)), (0.8, (1640, 280, 1000, 600)), (1, (1640, 280, 1000, 600))], u)
    inc = 16 * (1 - ease_out(t / 1.0))
    pantalla(img, fu["hero"].cuadro(t, d), cam, "full", inclinacion=inc)
    if u < 0.62: leyenda_grande(img, [("CENSO 2020 + ", BLANCO), ("CALENDARIO DEL SIAPA", CELESTE)], t, 0.6)
    else: leyenda_grande(img, [("MANZANA ", BLANCO), ("POR MANZANA", NARANJA)], t, 0.62 * d + 0.1)
    return img

PUERTAS = [(246, 860, 1030, 1320), (1070, 870, 1850, 1330), (1890, 870, 2674, 1330)]
def b_puertas(t, d, m):
    img = fondo(); cam = camara([(0, (200, 150, 2550, 1530)), (1, (260, 300, 2400, 1440))], t / d)
    encabezado(img, [[("Una puerta ", BLANCO), ("para cada quien.", NARANJA)]], t)
    pantalla(img, fu["puertas"].cuadro(t, d), cam, "head")
    for i, (r, c) in enumerate(zip(PUERTAS, [CELESTE, NARANJA, BLANCO])):
        recuadro(img, a_pantalla(r, cam, "head"), t, 0.35 + i * 0.3, c)
    return img

def b_familias(t, d, m):
    img = fondo(); cam = camara([(0, LLENO), (0.45, (800, 250, 1400, 840)), (1, (820, 330, 1300, 780))], t / d)
    encabezado(img, [[("Para la familia: ", BLANCO), ("qué días te quedas sin agua.", NARANJA)]], t)
    pantalla(img, fu["micasa"].cuadro(t, d), cam, "head")
    recuadro(img, a_pantalla((880, 630, 2040, 735), cam, "head"), t, 1.2, CELESTE)
    return img

def b_municipio(t, d, m):
    img = fondo(); cam = camara([(0, (0, 0, 2800, 1680)), (0.5, (820, 520, 1750, 1050)), (1, (1000, 780, 1000, 600))], t / d)
    encabezado(img, [[("Para el municipio: ", BLANCO), ("dónde se secan las casas hoy.", NARANJA)]], t)
    pantalla(img, fu["mapa"].cuadro(t, d), cam, "head")
    recuadro(img, a_pantalla((1225, 990, 1525, 1175), cam, "head"), t, 1.6, NARANJA)
    return img

def b_jurado(t, d, m):
    img = fondo(); cam = camara([(0, (100, 60, 2600, 1560)), (0.45, (20, 240, 1400, 840)), (1, (60, 300, 1300, 780))], t / d)
    encabezado(img, [[("Para el jurado: ", BLANCO), ("cada número, explicado.", NARANJA)]], t)
    pantalla(img, fu["como"].cuadro(t, d), cam, "head")
    recuadro(img, a_pantalla((240, 566, 1294, 712), cam, "head"), t, 1.3, CELESTE)
    leyenda_grande(img, [("34,097 DE 34,097 ", BLANCO), ("IGUALES", NARANJA)], t, 1.6, layout="head", tam=58)
    return img

def b_casas(t, d, m):
    img = fondo()
    texto_animado(img, [[("EN LAS ZONAS CON TANDEO", CELESTE)]], fuente(TXT, 36), t, 0.1, y=180)
    a, b = contador(17420, t, 0.25, 1.5), contador(34429, t, 0.25, 1.8)
    texto_animado(img, [[(miles(a), BLANCO), (" – ", GRIS), (miles(b), NARANJA)]], fuente(TIT, 190), t, 0.2, y=250, stagger=0)
    texto_animado(img, [[("casas sin ", BLANCO), ("tinaco ni cisterna", NARANJA)]], fuente(TIT, 76), t, 0.8, y=520)
    chip(img, "Dato real · INEGI, Censo 2020", None, 680, t, 1.4, color=(110, 220, 150))
    return img

SAUZ = (1070, 810, 1850, 1200)
def b_sauz(t, d, m):
    img = fondo(); cam = camara([(0, (215, 180, 2500, 1500)), (0.45, (885, 660, 1150, 690)), (1, (905, 690, 1100, 660))], t / d)
    encabezado(img, [[("La colonia de ", BLANCO), ("mayor riesgo.", NARANJA)]], t, x=110, y=70)
    pantalla(img, fu["cifras"].cuadro(t, d), cam, "left")
    recuadro(img, a_pantalla(SAUZ, cam, "left"), t, 0.9, NARANJA)
    texto_animado(img, [[("El Sauz", BLANCO)]], fuente(TIT, 92), t, 0.5, x=1330, y=330, alinear="izq")
    texto_animado(img, [[(miles(contador(11889, t, 0.7, 1.3)), NARANJA)]], fuente(TIT, 120), t, 0.6, x=1330, y=450, alinear="izq", stagger=0)
    texto_animado(img, [[("personas, casi todas", BLANCO)], [("sin dónde guardar agua", BLANCO)]], fuente(TXT, 36), t, 1.0, x=1330, y=610, alinear="izq")
    return img

PASOS = [("1", "Medimos", "quién tiene tinaco,", "cisterna o nada", CELESTE, "N11a"),
         ("2", "Anticipamos", "qué día se seca", "cada casa", BLANCO, "N11b"),
         ("3", "Actuamos", "a dónde mandar", "primero las pipas", NARANJA, "N11c")]
def b_pasos(t, d, m):
    img = fondo()
    texto_animado(img, [[("CÓMO LO HACE, ", CELESTE), ("EN TRES PASOS", NARANJA)]], fuente(TXT, 38), t, 0.05, y=200)
    for i, (n, tit, l1, l2, c, k) in enumerate(PASOS):
        t0 = T(k, m) - 0.1; cx = 400 + i * 560; kk = ease_out((t - t0) / 0.45)
        if kk > 0:
            capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa); r = 74; cy = 430 + 30 * (1 - kk)
            pts = [(cx + r * math.cos(math.radians(60 * j - 30)), cy + r * math.sin(math.radians(60 * j - 30))) for j in range(6)]
            dr.polygon(pts, fill=TARJETA_OSCURA + (int(255 * kk),), outline=c + (int(255 * kk),), width=5)
            fnt = fuente(TIT, 76); tw = dr.textlength(n, font=fnt); dr.text((cx - tw / 2, cy - 50), n, font=fnt, fill=c + (int(255 * kk),))
            img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"))
        texto_animado(img, [[(tit, c)]], fuente(TIT, 66), t, t0 + 0.15, x=cx - ImageDraw.Draw(img).textlength(tit, font=fuente(TIT, 66)) / 2, y=555, alinear="izq")
        for j, l in enumerate((l1, l2)):
            texto_animado(img, [[(l, BLANCO)]], fuente(TXT, 36), t, t0 + 0.3, x=cx - ImageDraw.Draw(img).textlength(l, font=fuente(TXT, 36)) / 2, y=665 + j * 46, alinear="izq")
    return img

def b_firmes(t, d, m):
    img = fondo(); cam = camara([(0, (220, 210, 2450, 1470)), (0.5, (1140, 978, 1300, 780)), (1, (1140, 978, 1300, 780))], t / d)
    pantalla(img, fu["firmes"].cuadro(t, d), cam, "full")
    recuadro(img, a_pantalla((1296, 1520, 2286, 1572), cam, "full"), t, 1.2, NARANJA)
    leyenda_grande(img, [("CADA CIFRA, ", BLANCO), ("CON SU ETIQUETA", NARANJA)], t, 0.3, tam=64)
    return img

beats = [
    {"nombre": "apertura", "render": b_apertura, "voz": ["N0"]},
    {"nombre": "627", "render": b_627, "voz": ["N1"]},
    {"nombre": "1 de 4", "render": b_uno_de_cuatro, "voz": ["N2", "N3"]},
    {"nombre": "pregunta", "render": b_pregunta, "voz": ["NQ"]},
    {"nombre": "hero", "render": b_hero, "voz": ["N4"]},
    {"nombre": "puertas", "render": b_puertas, "voz": ["N5"]},
    {"nombre": "familias", "render": b_familias, "voz": ["N6"]},
    {"nombre": "municipio", "render": b_municipio, "voz": ["N7"]},
    {"nombre": "jurado", "render": b_jurado, "voz": ["N8"]},
    {"nombre": "casas", "render": b_casas, "voz": ["N9"]},
    {"nombre": "sauz", "render": b_sauz, "voz": ["N10"]},
    {"nombre": "pasos", "render": b_pasos, "voz": ["N11a", "N11b", "N11c"]},
    {"nombre": "firmes", "render": b_firmes, "voz": ["N12"]},
]
if __name__ == "__main__":
    total, plan = montar_continuo(beats, "voz_inicio", G, os.path.join("..", "editados", "Inicio_editado_v3.mp4"))
    print(round(total, 1)); print(plan)
