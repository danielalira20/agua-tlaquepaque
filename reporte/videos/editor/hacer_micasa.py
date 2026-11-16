"""Video 2 · Mi casa ("¿Cuánto aguanta tu casa?").

Correr desde reporte/videos/editor/:  python voz.py guion_micasa.json voz_micasa  &&  python hacer_micasa.py
La grabación va en reporte/videos/MiCasa.mov (Drive, carpeta de grabaciones).

Lo que se ve en la grabación (verificado a resolución completa, manda sobre la guía):
- Paso 2 elige «Los dos» (el resultado dice «Tinaco y cisterna», calculamos 6,100 L), no «Tinaco».
- Paso 1 no escribe: baja por la lista hasta Artesanos (cada colonia trae su zona).
- Artesanos no tiene cisterna comunitaria: la app manda a buscar en colonias vecinas.
- El número de TlaqueChat no está confirmado (rama fix/tlaquechat-sin-numero): se difumina en todos los cuadros.
"""
import sys, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI); sys.path.insert(0, AQUI)
from motor2 import *
from motor2 import _gota, contorno_gota

SRC = os.path.join(AQUI, "..", "MiCasa.mov")
G = json.load(open("guion_micasa.json", encoding="utf-8"))
VERDE = (110, 220, 150)
MASC = Image.open(os.path.join(AQUI, "..", "..", "..", "app", "public", "mascota", "tlacuache.webp")).convert("RGBA")
LAYOUTS["paso"] = (300, 150, 1320, 792)   # tarjeta un poco más chica para que quepa el indicador de pasos arriba
PASOS = ["Colonia", "Agua guardada", "Personas"]

# Tramos limpios de la grabación (s). Fuera quedan: transición de 23.5 a 33.5 (negro, blanco, WhatsApp),
# 36.5 a 39.5 (WhatsApp otra vez), el tooltip localhost de 21 a 23 y la barra de grabación desde 57.
TRAMOS = {"paso1_quieto": (0.0, 0.1), "paso1": (2.6, 6.2), "paso2": (6.4, 10.8), "paso3": (11.3, 14.2),
          "resultado": (14.6, 20.8), "vecinos": (33.6, 36.0), "ajustar": (42.6, 47.4)}
fu = {k: Fuente(SRC, a, b, f"cuadros_micasa/{k}") for k, (a, b) in TRAMOS.items()}

# El número de TlaqueChat (33 2804 8171) sale en la tarjeta «Pide una pipa». Se difumina en el disco una sola vez.
NUMERO = (2088, 612, 2312, 682)
def tapar_numero(carpeta):
    marca = os.path.join(carpeta, ".numero_tapado")
    if os.path.exists(marca): return
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".jpg"): continue
        p = os.path.join(carpeta, f); im = Image.open(p).convert("RGB")
        trozo = im.crop(NUMERO).filter(ImageFilter.GaussianBlur(12)).filter(ImageFilter.GaussianBlur(12))
        im.paste(trozo, NUMERO[:2]); im.save(p, quality=95)
    open(marca, "w").close()
for k in ("resultado", "vecinos"):
    tapar_numero(f"cuadros_micasa/{k}"); fu[k].__init__(SRC, *TRAMOS[k], f"cuadros_micasa/{k}")

LLENO = (0, 0, SRC_W, SRC_H)
COLUMNA = (580, 150, 1760, 1056)   # columna central de los pasos 1 a 3

def T(k, m, d=0.0): return m.get(k, 0) + d
def F(k, m, d=0.0): return m.get(k + "_fin", 0) + d

# ---------- beats ----------
def gota_que_se_vacia(img, cx, cy, R, nivel, t, k):
    """Gota grande con agua adentro; `nivel` de 0 (vacía) a 1 (llena), con una ola en la superficie."""
    if k <= 0: return
    caja = (int(cx - R * 1.3), int(cy - R * 2.0), int(cx + R * 1.3), int(cy + R * 1.3)); w, h = caja[2] - caja[0], caja[3] - caja[1]
    cxl, cyl = w / 2, h - R * 1.3 + R * 0.1
    pts = contorno_gota(cxl, cyl, R)
    mk = Image.new("L", (w, h), 0); ImageDraw.Draw(mk).polygon(pts, fill=255)
    arriba, abajo = min(p[1] for p in pts), max(p[1] for p in pts)
    ysup = abajo - nivel * (abajo - arriba)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa)
    dr.polygon([(x, ysup + 9 * math.sin(x / 38 + t * 4.5)) for x in range(0, w + 8, 8)] + [(w, h), (0, h)], fill=CELESTE + (int(200 * k),))
    agua = Image.new("RGBA", (w, h), (0, 0, 0, 0)); agua.paste(capa, (0, 0), mk)
    borde = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(borde).line(pts + [pts[0], pts[1]], fill=CELESTE + (int(255 * k),), width=8, joint="curve")
    base = Image.alpha_composite(Image.alpha_composite(img.crop(caja).convert("RGBA"), agua), borde)
    img.paste(base.convert("RGB"), (caja[0], caja[1] + int(30 * (1 - k))))

def b_apertura(t, d, m):
    img = fondo(); gotas_flotantes(img, t)
    texto_animado(img, [[("MI CASA · PARA LAS FAMILIAS", CELESTE)]], fuente(TXT, 34), t, 0.05, x=260, y=330, alinear="izq")
    texto_animado(img, [[("¿Cuánto aguanta", BLANCO)]], fuente(TIT, 124), t, 0.15, x=260, y=385, alinear="izq", stagger=0.08)
    texto_animado(img, [[("tu casa?", NARANJA)]], fuente(TIT, 124), t, 0.45, x=260, y=530, alinear="izq", stagger=0.08)
    gota_que_se_vacia(img, 1560, 610, 160, 0.92 - 0.55 * ease(t / max(d, 0.1)), t, ease_out((t - 0.3) / 0.5))
    return respirar(img, t, d)

def b_intro(t, d, m):
    img = fondo(); cam = camara([(0, (100, 60, 2730, 1638)), (0.55, COLUMNA), (1, (640, 170, 1640, 984))], t / d)
    encabezado(img, [[("Mi casa: ", BLANCO), ("tres preguntas, una respuesta.", NARANJA)]], t, t_in=0.5)
    inc = 16 * (1 - ease_out(t / 1.0))
    pantalla(img, fu["paso1_quieto"].cuadro(t, d), cam, "head", inclinacion=inc)
    return img

BUSCADOR, ARTESANOS = (880, 630, 2040, 735), (892, 900, 2028, 990)
def b_colonia(t, d, m):
    img = fondo(); u = t / d
    cam = camara([(0, COLUMNA), (0.35, (760, 520, 1400, 840)), (1, (760, 560, 1400, 840))], u)
    pasos_progreso(img, 1, t, PASOS)
    pantalla(img, fu["paso1"].cuadro(t, d), cam, "paso")
    t_art = d - 1.5
    if t < t_art: recuadro(img, a_pantalla(BUSCADOR, cam, "paso"), t, 0.5, CELESTE)
    else: recuadro(img, a_pantalla(ARTESANOS, cam, "paso"), t, t_art, CELESTE)
    return img

LOS_DOS = (1474, 974, 2040, 1288)
def b_almacen(t, d, m):
    img = fondo(); cam = camara([(0, COLUMNA), (0.4, (840, 590, 1220, 732)), (1, (840, 590, 1220, 732))], t / d)
    pasos_progreso(img, 2, t, PASOS)
    pantalla(img, fu["paso2"].cuadro(t, d), cam, "left")
    t_dos = F("M3", m, -1.0)
    recuadro(img, a_pantalla(LOS_DOS, cam, "left"), t, t_dos, CELESTE)
    texto_animado(img, [[("Tinaco y cisterna", BLANCO)]], fuente(TIT, 64), t, t_dos + 0.1, x=1330, y=330, alinear="izq")
    texto_animado(img, [[("6,100 L", NARANJA)]], fuente(TIT, 150), t, t_dos + 0.2, x=1330, y=420, alinear="izq", stagger=0)
    texto_animado(img, [[("1,100 del tinaco", BLANCO)], [("+ 5,000 de la cisterna", BLANCO)]], fuente(TXT, 36), t, t_dos + 0.4, x=1330, y=610, alinear="izq")
    chip(img, "Lo que calcula la app", 1330, 730, t, t_dos + 0.6, color=GRIS)
    return img

CONTADOR = (880, 632, 2040, 1016)
def b_personas(t, d, m):
    img = fondo(); cam = camara([(0, (700, 270, 1520, 912)), (1, (730, 300, 1460, 876))], t / d)
    pasos_progreso(img, 3, t, PASOS)
    pantalla(img, fu["paso3"].cuadro(t, d), cam, "paso")
    recuadro(img, a_pantalla(CONTADOR, cam, "paso"), t, 0.4, CELESTE)
    return img

TU_COLONIA = (388, 300, 1512, 672)
def b_resultado(t, d, m):
    img = fondo(); cam = camara([(0, (60, 40, 2700, 1620)), (0.4, (300, 140, 1400, 840)), (1, (330, 160, 1350, 810))], t / d)
    pantalla(img, fu["resultado"].cuadro(t, d), cam, "full")
    recuadro(img, a_pantalla(TU_COLONIA, cam), t, 1.4, CELESTE)
    leyenda_grande(img, [("ARTESANOS: ", BLANCO), ("SIN RACIONAMIENTO", CELESTE)], t, 1.8)
    return img

CISTERNA, PIPA, CLORO = (1552, 346, 2532, 516), (1552, 536, 2532, 880), (1552, 900, 2532, 1124)
def b_quehacer(t, d, m):
    img = fondo()
    t_cis = T("M6a", m) + 3.0; t_pipa = T("M6b", m) - 0.1; t_clo = T("M6c", m) - 0.1
    cam = camara([(0, (1400, 220, 1520, 912)), (t_cis / d, (1470, 270, 1440, 864)), (1, (1480, 280, 1420, 852))], t / d)
    encabezado(img, [[("Si te quedas sin agua: ", BLANCO), ("qué hacer.", NARANJA)]], t)
    pantalla(img, fu["resultado"].cuadro(t, d), cam, "head")
    if t < t_pipa: recuadro(img, a_pantalla(CISTERNA, cam, "head"), t, t_cis, CELESTE)
    elif t < t_clo: recuadro(img, a_pantalla(PIPA, cam, "head"), t, t_pipa, CELESTE)
    else: recuadro(img, a_pantalla(CLORO, cam, "head"), t, t_clo, CELESTE)
    return img

AVISALE = (1552, 1216, 2532, 1556)
def b_vecinos(t, d, m):
    img = fondo(); cam = camara([(0, (1300, 760, 1500, 900)), (1, (1440, 880, 1200, 720))], t / d)
    pantalla(img, fu["vecinos"].cuadro(t, d), cam, "full")
    recuadro(img, a_pantalla(AVISALE, cam), t, 0.5, CELESTE)
    return img

DESLIZADOR = (2032, 190, 2860, 436)
def b_ajustar(t, d, m):
    img = fondo(); cam = camara([(0, (1700, 0, 1230, 738)), (1, (1820, 40, 1100, 660))], t / d)
    encabezado(img, [[("Tu casa, ", BLANCO), ("tus litros.", NARANJA)]], t, x=110, y=70)
    pantalla(img, fu["ajustar"].cuadro(t, d), cam, "left")
    recuadro(img, a_pantalla(DESLIZADOR, cam, "left"), t, 0.6, CELESTE)
    texto_animado(img, [[("CONSUMO POR PERSONA", CELESTE)]], fuente(TXT, 36), t, 0.3, x=1330, y=300, alinear="izq")
    n = 50 + contador(25, t, 0.9, 1.4)
    texto_animado(img, [[(str(n), NARANJA), (" L", BLANCO)]], fuente(TIT, 190), t, 0.4, x=1330, y=345, alinear="izq", stagger=0)
    texto_animado(img, [[("litros por persona", BLANCO)], [("al día", BLANCO)]], fuente(TXT, 40), t, 0.7, x=1330, y=585, alinear="izq")
    chip(img, "50 L: el mínimo de la OMS", 1330, 720, t, 1.6, color=GRIS)
    return img

def b_sauz_titulo(t, d, m):
    img = fondo(); gotas_flotantes(img, t)
    texto_animado(img, [[("LA COLONIA DE MAYOR RIESGO", CELESTE)]], fuente(TXT, 36), t, 0.05, y=300)
    texto_animado(img, [[("Pero en El Sauz,", BLANCO)], [("la historia es otra.", NARANJA)]], fuente(TIT, 116), t, 0.1, y=370, stagger=0.08)
    return respirar(img, t, d)

def b_sauz_dato(t, d, m):
    img = fondo(); gotas_flotantes(img, t + 5)
    brillo(img, 960, 330, 560, NARANJA, 0.10, t, 0.2)
    texto_animado(img, [[("EL SAUZ · ZONA 6", CELESTE)]], fuente(TXT, 36), t, 0.1, y=150)
    texto_animado(img, [[(miles(contador(11889, t, 0.25, 1.5)), NARANJA)]], fuente(TIT, 300), t, 0.2, y=190, stagger=0)
    texto_animado(img, [[("personas, casi todas ", BLANCO), ("sin dónde guardar agua", NARANJA)]], fuente(TIT, 68), t, 0.8, y=540)
    texto_animado(img, [[("Al menos 2,950 de sus 3,546 viviendas no tienen tinaco ni cisterna", GRIS)]], fuente(TXTR, 32), t, 1.3, y=650)
    chip(img, "Dato real · INEGI, Censo 2020", None, 740, t, 1.6, color=VERDE)
    return respirar(img, t, d, 0.025)

def casa(dr, cx, cy, s, color, tinaco, k):
    """Misma casita que en hacer_inicio.py (b_uno_de_cuatro)."""
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

def _centrado(img, txt, fnt, cx):
    return cx - ImageDraw.Draw(img).textlength(txt, font=fnt) / 2

def reserva(img, cx, y, nivel, color, k):
    """Barra de reserva de agua debajo de una casita."""
    if k <= 0: return
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa); a = int(255 * k); ancho = 300
    dr.rounded_rectangle([cx - ancho / 2, y, cx + ancho / 2, y + 22], 11, outline=color + (a,), width=3)
    if nivel > 0.02: dr.rounded_rectangle([cx - ancho / 2 + 5, y + 5, cx - ancho / 2 + 5 + (ancho - 10) * nivel, y + 17], 6, fill=color + (a,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"))

def b_contraste(t, d, m):
    img = fondo(); gotas_flotantes(img, t + 9); IZQ, DER = 620, 1300
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa)
    casa(dr, IZQ, 330, 200, CELESTE, True, ease_out((t - 0.2) / 0.45))
    casa(dr, DER, 330, 200, NARANJA, False, ease_out((t - 0.7) / 0.45))
    img.paste(Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB"))
    f1, f2 = fuente(TXT, 36), fuente(TIT, 68)
    for cx, l1, l2, c2, t0 in [(IZQ, "Con tinaco", "aguanta días", BLANCO, 0.5), (DER, "Sin tinaco ni cisterna", "Día 1 = sin agua", NARANJA, 1.0)]:
        texto_animado(img, [[(l1, GRIS)]], f1, t, t0, x=_centrado(img, l1, f1, cx), y=500, alinear="izq")
        texto_animado(img, [[(l2, c2)]], f2, t, t0 + 0.15, x=_centrado(img, l2, f2, cx), y=550, alinear="izq")
    reserva(img, IZQ, 665, 1.0 - 0.3 * ease((t - 0.8) / (d - 0.8)), CELESTE, ease_out((t - 0.6) / 0.4))
    reserva(img, DER, 665, 1.0 - ease((t - 1.4) / 0.9), NARANJA, ease_out((t - 1.1) / 0.4))
    texto_animado(img, [[("RESERVA", GRIS)]], fuente(TXT, 22), t, 0.7, x=_centrado(img, "RESERVA", fuente(TXT, 22), IZQ), y=700, alinear="izq")
    texto_animado(img, [[("RESERVA", GRIS)]], fuente(TXT, 22), t, 1.2, x=_centrado(img, "RESERVA", fuente(TXT, 22), DER), y=700, alinear="izq")
    t2 = m.get("M11", 0) + 3.3
    texto_animado(img, [[("Aguanta les dice ", BLANCO), ("qué días prepararse.", NARANJA)]], fuente(TIT, 72), t, t2, y=790)
    return respirar(img, t, d, 0.025)

def b_final(t, d, m):
    """Tarjeta final: el tlacuache se despide."""
    img = fondo(); gotas_flotantes(img, t + 13, alpha=50)
    brillo(img, 960, 330, 420, NARANJA, 0.16, t, 0.1)
    pegar_rebote(img, MASC, 960, 300, t, 0.1, 300)
    texto_animado(img, [[("Aguanta", BLANCO)]], fuente(TIT, 120), t, 0.45, y=470)
    texto_animado(img, [[("Saber cuánto aguantas, ", BLANCO), ("antes de que se acabe.", NARANJA)]], fuente(TIT, 56), t, 0.8, y=625)
    chip(img, "Siguiente: El mapa de hoy", None, 740, t, 1.5, color=CELESTE)
    texto_animado(img, [[("Equipo #15 · Hackathon Jalisco Internacional 2026 · Reto 01", GRIS)]], fuente(TXTR, 26), t, 1.9, y=905)
    texto_animado(img, [[("Voz generada con inteligencia artificial", GRIS)]], fuente(TXTR, 24), t, 2.1, y=945)
    return img

beats = [
    {"nombre": "apertura", "render": b_apertura, "voz": ["M0"]},
    {"nombre": "intro", "render": b_intro, "voz": ["M1"]},
    {"nombre": "colonia", "render": b_colonia, "voz": ["M2"]},
    {"nombre": "almacen", "render": b_almacen, "voz": ["M3"]},
    {"nombre": "personas", "render": b_personas, "voz": ["M4"]},
    {"nombre": "resultado", "render": b_resultado, "voz": ["M5"]},
    {"nombre": "que hacer", "render": b_quehacer, "voz": ["M6a", "M6b", "M6c"]},
    {"nombre": "vecinos", "render": b_vecinos, "voz": ["M7"]},
    {"nombre": "ajustar", "render": b_ajustar, "voz": ["M8"]},
    {"nombre": "sauz", "render": b_sauz_titulo, "voz": ["M9"]},
    {"nombre": "sauz dato", "render": b_sauz_dato, "voz": ["M10"]},
    {"nombre": "contraste", "render": b_contraste, "voz": ["M11"]},
    {"nombre": "final", "render": b_final, "voz": ["M12"]},
]
COLA = 2.2   # la tarjeta final se queda en pantalla un poco después de la voz
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rev":
        momentos = [(i, f) for i in range(len(beats)) for f in (0.15, 0.55, 0.95)]
        plan, total = previsualizar_continuo(beats, "voz_micasa", G, momentos, sys.argv[2] if len(sys.argv) > 2 else "rev_micasa.jpg")
        print(round(total, 1)); print(plan)
    else:
        total, plan = montar_continuo(beats, "voz_micasa", G, os.path.join("..", "editados", "MiCasa_editado.mp4"), tail=COLA, fundido=0.9)
        print(round(total, 1)); print(plan)
