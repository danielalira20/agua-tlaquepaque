"""Motor de edición estilo Agro para los videos de Aguanta.

Cada "beat" es una función render(t, dur) -> imagen RGB. Hay piezas para:
pantalla de la app en tarjeta (con cámara, inclinación 3D y recuadros), títulos con palabras que entran,
contadores, tarjetas de datos, encabezados y subtítulos. La voz manda la duración de cada beat.
"""
import json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
NAVY1, NAVY2 = (9, 20, 42), (20, 50, 92)
BLANCO, NARANJA, CELESTE, GRIS = (246, 242, 234), (240, 138, 93), (142, 197, 255), (160, 176, 204)
TARJETA_OSCURA = (14, 34, 66)
XFADE = 0.3
SRC_W, SRC_H = 2930, 1758

_fuentes = {}
def fuente(nombre, tam):
    k = (nombre, tam)
    if k not in _fuentes: _fuentes[k] = ImageFont.truetype(F + nombre, tam)
    return _fuentes[k]
TIT, TXT, TXTR = "Bricolage-Bold.ttf", "Atkinson-Bold.ttf", "Atkinson-Regular.ttf"

def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ease_out(u): u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 3

# ---------- fondo ----------
_FONDO = None
def fondo():
    global _FONDO
    if _FONDO is None:
        y, x = np.mgrid[0:H, 0:W]
        t = (x / W * 0.45 + y / H * 0.55)[..., None]
        img = np.array(NAVY1) * (1 - t) + np.array(NAVY2) * t
        d = np.sqrt((x - W * 0.82) ** 2 + (y - H * 0.12) ** 2)[..., None]
        img = img + np.clip(1 - d / 900, 0, 1) * 26
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa); r = 46; dx = r * math.sqrt(3)
        for fila in range(-1, int(H / (1.5 * r)) + 2):
            for col in range(-1, int(W / dx) + 2):
                cx = col * dx + (dx / 2 if fila % 2 else 0); cy = fila * 1.5 * r
                dr.polygon([(cx + r * math.cos(math.radians(60 * k - 30)), cy + r * math.sin(math.radians(60 * k - 30))) for k in range(6)], outline=(255, 255, 255, 9))
        _FONDO = Image.alpha_composite(im, capa).convert("RGB")
    return _FONDO.copy()

# ---------- fuente de video ----------
class Fuente:
    """Cuadros de un tramo de la grabación (JPG a resolución completa)."""
    def __init__(self, src, ini, fin, carpeta):
        os.makedirs(carpeta, exist_ok=True)
        if not os.listdir(carpeta):
            subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ini), "-to", str(fin), "-i", src, "-vf", f"fps={FPS}", "-q:v", "2", f"{carpeta}/%05d.jpg"], check=True)
        self.carpeta = carpeta; self.n = len([f for f in os.listdir(carpeta) if f.endswith(".jpg")]); self._c = (None, None)
    def cuadro(self, t, dur, rate_min=0.45):
        r = max(rate_min, min(1.0, (self.n / FPS) / dur)) if dur > 0 else 1
        i = min(self.n - 1, int(t * FPS * r))
        if self._c[0] != i:
            im = Image.open(f"{self.carpeta}/{i + 1:05d}.jpg").convert("RGB")
            im.paste(im.crop((0, 1490, 140, 1615)), (0, 1615))  # tapa el botón N de Next.js
            self._c = (i, im)
        return self._c[1]

def camara(kfs, u):
    if u <= kfs[0][0]: return kfs[0][1]
    for (u0, r0), (u1, r1) in zip(kfs, kfs[1:]):
        if u <= u1:
            k = ease((u - u0) / (u1 - u0) if u1 > u0 else 1)
            return tuple(a + (b - a) * k for a, b in zip(r0, r1))
    return kfs[-1][1]

# ---------- pantalla en tarjeta ----------
LAYOUTS = {"full": (240, 80, 1440, 864), "head": (340, 215, 1240, 744), "left": (110, 200, 1150, 690)}
_mascaras, _sombras = {}, {}
def _mascara(w, h):
    if (w, h) not in _mascaras:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=255); _mascaras[(w, h)] = m
    return _mascaras[(w, h)]
def _sombra(rect):
    if rect not in _sombras:
        x, y, w, h = rect; s = Image.new("L", (W, H), 0)
        ImageDraw.Draw(s).rounded_rectangle([x + 6, y + 18, x + w + 6, y + h + 18], 28, fill=160); _sombras[rect] = s.filter(ImageFilter.GaussianBlur(26))
    return _sombras[rect]

def _coeficientes(dst, src):
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def pantalla(img, cuadro_src, cam, layout="full", inclinacion=0.0, escala=1.0):
    """Pega el recorte `cam` del cuadro en la tarjeta del layout. inclinacion en grados (giro sobre el eje vertical)."""
    x, y, w, h = LAYOUTS[layout]
    if escala != 1.0:
        cx, cy = x + w / 2, y + h / 2; w2, h2 = int(w * escala), int(h * escala); x, y, w, h = int(cx - w2 / 2), int(cy - h2 / 2), w2, h2
    cx_, cy_, cw, ch = cam
    rec = cuadro_src.crop((int(cx_), int(cy_), int(cx_ + cw), int(cy_ + ch))).resize((w, h), Image.LANCZOS)
    if abs(inclinacion) < 0.3:
        img.paste((3, 8, 20), (0, 0), _sombra((x, y, w, h))); img.paste(rec, (x, y), _mascara(w, h)); return
    a = math.radians(inclinacion); d = 2200.0
    def proy(px, pz):  # px relativo al centro, pz profundidad
        s = d / (d + pz); return px * s, s
    hw, hh = w / 2, h / 2
    zl, zr = -hw * math.sin(a), hw * math.sin(a); xl, xr = -hw * math.cos(a), hw * math.cos(a)
    (pxl, sl), (pxr, sr) = proy(xl, zl), proy(xr, zr)
    cxw, cyw = x + hw, y + hh
    quad = [(cxw + pxl, cyw - hh * sl), (cxw + pxr, cyw - hh * sr), (cxw + pxr, cyw + hh * sr), (cxw + pxl, cyw + hh * sl)]
    rgba = rec.convert("RGBA"); rgba.putalpha(_mascara(w, h))
    coef = _coeficientes(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    capa = rgba.transform((W, H), Image.PERSPECTIVE, coef, Image.BICUBIC)
    sombra = Image.new("L", (W, H), 0); ImageDraw.Draw(sombra).polygon([(px + 6, py + 18) for px, py in quad], fill=150)
    img.paste((3, 8, 20), (0, 0), sombra.filter(ImageFilter.GaussianBlur(24)))
    img.paste(capa, (0, 0), capa)

def a_pantalla(src_rect, cam, layout="full"):
    """Convierte un rectángulo en pixeles de la grabación a coordenadas del video final."""
    x, y, w, h = LAYOUTS[layout]; cx, cy, cw, ch = cam; sx, sy = w / cw, h / ch
    a, b, c, d = src_rect
    return (x + (a - cx) * sx, y + (b - cy) * sy, x + (c - cx) * sx, y + (d - cy) * sy)

def recuadro(img, caja, t, t_in, color=NARANJA):
    """Marco brillante que aparece sobre un elemento."""
    k = ease_out((t - t_in) / 0.4)
    if k <= 0: return
    x0, y0, x1, y1 = caja; m = 10 * (1 - k)
    x0, y0, x1, y1 = x0 - 8 - m, y0 - 8 - m, x1 + 8 + m, y1 + 8 + m
    pad = 40; bx0, by0 = int(max(0, x0 - pad)), int(max(0, y0 - pad)); bx1, by1 = int(min(W, x1 + pad)), int(min(H, y1 + pad))
    if bx1 <= bx0 or by1 <= by0: return
    caja_l = [x0 - bx0, y0 - by0, x1 - bx0, y1 - by0]; tam = (bx1 - bx0, by1 - by0)
    halo = Image.new("RGBA", tam, (0, 0, 0, 0)); ImageDraw.Draw(halo).rounded_rectangle(caja_l, 16, outline=color + (int(170 * k),), width=14)
    halo = halo.filter(ImageFilter.GaussianBlur(10))
    ImageDraw.Draw(halo).rounded_rectangle(caja_l, 16, outline=color + (int(255 * k),), width=5)
    trozo = img.crop((bx0, by0, bx1, by1)).convert("RGBA"); img.paste(Image.alpha_composite(trozo, halo).convert("RGB"), (bx0, by0))

# ---------- texto animado ----------
def palabras(partes):
    out = []
    for txt, color in partes:
        for w_ in txt.split(" "):
            if w_: out.append((w_, color))
    return out

def texto_animado(img, lineas, fnt, t, t_in, x=None, y=0, interlineado=1.15, alinear="centro", stagger=0.06, dur=0.4, sombra=False):
    """lineas: lista de listas de (texto, color). Cada palabra sube y aparece."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa)
    esp = dr.textlength(" ", font=fnt); alto = fnt.size * interlineado; i = 0
    for n, linea in enumerate(lineas):
        ps = palabras(linea); ancho = sum(dr.textlength(p, font=fnt) for p, _ in ps) + esp * (len(ps) - 1)
        xx = (W - ancho) / 2 if alinear == "centro" else x
        yy = y + n * alto
        for p, c in ps:
            k = ease_out((t - t_in - i * stagger) / dur); i += 1
            if k > 0:
                off = 28 * (1 - k)
                if sombra: dr.text((xx + 3, yy + off + 4), p, font=fnt, fill=(0, 0, 0, int(140 * k)))
                dr.text((xx, yy + off), p, font=fnt, fill=c + (int(255 * k),))
            xx += dr.textlength(p, font=fnt) + esp
    base = img.convert("RGBA"); img.paste(Image.alpha_composite(base, capa).convert("RGB"))

def contador(valor, t, t_in, dur=1.3):
    return int(round(valor * ease_out((t - t_in) / dur)))
def miles(n): return f"{n:,}"

def subtitulo(img, texto):
    dr = ImageDraw.Draw(img); fnt = fuente(TXT, 32)
    palabras_ = texto.split(); lineas = []; act = ""
    for p in palabras_:
        prueba = (act + " " + p).strip()
        if dr.textlength(prueba, font=fnt) <= 1560: act = prueba
        else: lineas.append(act); act = p
    if act: lineas.append(act)
    lineas = lineas[:2]; y0 = 972 if len(lineas) == 2 else 992
    for i, l in enumerate(lineas):
        tw = dr.textlength(l, font=fnt)
        dr.text(((W - tw) / 2, y0 + i * 42), l, font=fnt, fill=BLANCO, stroke_width=3, stroke_fill=(6, 14, 30))

def encabezado(img, partes_lineas, t, t_in=0.1, x=340, y=60, tam=56):
    texto_animado(img, partes_lineas, fuente(TIT, tam), t, t_in, x=x, y=y, alinear="izq", interlineado=1.1)

def leyenda_grande(img, partes, t, t_in, layout="full", tam=70):
    """Letras de impacto sobre la pantalla, abajo a la izquierda (estilo «SATÉLITE Y RELIEVE»)."""
    x, y, w, h = LAYOUTS[layout]
    k = ease_out((t - t_in) / 0.4)
    if k > 0:
        grad = Image.new("L", (w, int(h * 0.42)), 0)
        g = np.linspace(0, 200 * k, grad.size[1]).astype(np.uint8)[:, None].repeat(w, 1); grad = Image.fromarray(g)
        img.paste((6, 14, 30), (x, y + h - grad.size[1]), grad)
    texto_animado(img, [partes], fuente(TIT, tam), t, t_in, x=x + 50, y=y + h - tam * 1.55, alinear="izq", stagger=0.08, sombra=True)

def chip(img, texto, x, y, t, t_in, color=CELESTE):
    k = ease_out((t - t_in) / 0.35)
    if k <= 0: return
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(capa); fnt = fuente(TXT, 28)
    tw = dr.textlength(texto, font=fnt); xx = x if x is not None else (W - tw - 52) / 2
    dr.rounded_rectangle([xx, y, xx + tw + 52, y + 56], 28, fill=TARJETA_OSCURA + (int(255 * k),))
    dr.text((xx + 26, y + 11), texto, font=fnt, fill=color + (int(255 * k),))
    base = img.convert("RGBA"); img.paste(Image.alpha_composite(base, capa).convert("RGB"))

def pegar(img, imagen_rgba, cx, cy, t, t_in, ancho):
    k = ease_out((t - t_in) / 0.45)
    if k <= 0: return
    esc = 0.85 + 0.15 * k; w = int(ancho * esc); h = int(imagen_rgba.height * w / imagen_rgba.width)
    im = imagen_rgba.resize((w, h), Image.LANCZOS); a = im.split()[3].point(lambda v: int(v * k)); im.putalpha(a)
    img.paste(im, (int(cx - w / 2), int(cy - h / 2)), im)

# ---------- montaje ----------
def montar(beats, voz_dir, guion, salida, lead=0.3, gap=0.22, tail=0.45, min_dur=1.2):
    """beats: dicts con render (fn t,dur -> img), voz (claves) o dur (silencio). Devuelve plan."""
    dv = json.load(open(f"{voz_dir}/duraciones.json"))
    plan = []; t = 0.0; subs = []; clips = []
    for b in beats:
        if b.get("voz"):
            d = lead; marcas = {}
            for k in b["voz"]: marcas[k] = d; d += dv[k] + gap
            d = d - gap + tail + b.get("extra", 0)
        else:
            d = b["dur"]; marcas = {}
        d = max(min_dur, d); b["marcas"] = marcas; b["duracion"] = d
        plan.append((t, d, b))
        for k, off in marcas.items():
            clips.append((t + off, k)); subs.append((t + off, t + off + dv[k] + 0.12, guion[k]["sub"]))
        t += d - XFADE
    total = t + XFADE
    import soundfile as sf
    sr = 24000; audio = np.zeros(int((total + 0.5) * sr), dtype=np.float32)
    for ini, k in clips:
        a, _ = sf.read(f"{voz_dir}/{k}.wav", dtype="float32"); i = int(ini * sr); audio[i:i + len(a)] += a
    sf.write(salida + ".wav", audio, sr)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", salida + ".wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    for f in range(int(total * FPS)):
        tt = f / FPS; act = [(a, d, b) for a, d, b in plan if a <= tt < a + d] or [plan[-1]]
        a, d, b = act[0]; img = b["render"](tt - a, d, b["marcas"])
        if len(act) > 1:
            a2, d2, b2 = act[1]; img = Image.blend(img, b2["render"](tt - a2, d2, b2["marcas"]), ease((tt - a2) / XFADE))
        for s0, s1, txt in subs:
            if s0 <= tt < s1: subtitulo(img, txt); break
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait()
    return total, [(round(a, 2), round(d, 2), b.get("nombre", "")) for a, d, b in plan]


def previsualizar(beats, voz_dir, momentos, salida, lead=0.3, gap=0.22, tail=0.45, min_dur=1.2):
    """Renderiza cuadros sueltos (beat_idx, fraccion) a una hoja de contacto, sin codificar el video."""
    dv = json.load(open(f"{voz_dir}/duraciones.json")); ims = []
    for b in beats:
        if b.get("voz"):
            d = lead; marcas = {}
            for k in b["voz"]: marcas[k] = d; d += dv[k] + gap
            d = d - gap + tail + b.get("extra", 0)
        else: d = b["dur"]; marcas = {}
        b["marcas"] = marcas; b["duracion"] = max(min_dur, d)
    for i, fr in momentos:
        b = beats[i]; ims.append(b["render"](fr * b["duracion"], b["duracion"], b["marcas"]).resize((640, 360)))
    cols = 3; filas = (len(ims) + cols - 1) // cols; hoja = Image.new("RGB", (cols * 646, filas * 366), "white")
    for k, im in enumerate(ims): hoja.paste(im, ((k % cols) * 646, (k // cols) * 366))
    hoja.save(salida)


# ---------- montaje continuo (narración de corrido) ----------
def planear_continuo(beats, voz_dir, guion, lead=0.6, gap_pasajes=0.4, tail=1.1):
    """La narración manda: cada pasaje se coloca tal cual (sin cortarlo) y cada beat dura lo que dura su voz.
    Las transiciones caen en las pausas naturales entre frases. Devuelve (plan, total, subs, pasajes_abs)."""
    marcas = json.load(open(f"{voz_dir}/marcas.json")); abs_fr = {}; pas = []; t = lead
    for p in guion["_pasajes"]:
        m = marcas[p["id"]]; pas.append((t, p["id"]))
        for c, (s, e) in m["frases"].items(): abs_fr[c] = (t + s, t + e)
        t += m["dur"] + gap_pasajes
    fin_voz = max(e for s, e in abs_fr.values()); total = fin_voz + tail
    ini = [0.0]
    for i in range(1, len(beats)):
        e_prev = max(abs_fr[c][1] for c in beats[i - 1]["voz"]); s_next = min(abs_fr[c][0] for c in beats[i]["voz"])
        ini.append((e_prev + s_next) / 2)
    plan = []; subs = []
    for i, b in enumerate(beats):
        fin = ini[i + 1] + XFADE if i + 1 < len(beats) else total
        b["marcas"] = {}
        for c in b["voz"]:
            b["marcas"][c] = abs_fr[c][0] - ini[i]; b["marcas"][c + "_fin"] = abs_fr[c][1] - ini[i]
            if guion[c]["sub"]: subs.append((abs_fr[c][0] - 0.05, abs_fr[c][1] + 0.15, guion[c]["sub"]))
        b["duracion"] = fin - ini[i]; plan.append((ini[i], b["duracion"], b))
    return plan, total, subs, pas

def normalizar(entrada, salida):
    """Volumen parejo (−16 LUFS) en dos pasadas y modo lineal: no hay bombeo ni saltos de volumen."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", entrada, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rfind("{"):])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", entrada, "-af", af, "-ar", "24000", salida], check=True)

def montar_continuo(beats, voz_dir, guion, salida, lead=0.6, gap_pasajes=0.4, tail=1.1, fundido=0.8):
    import soundfile as sf
    plan, total, subs, pas = planear_continuo(beats, voz_dir, guion, lead, gap_pasajes, tail)
    sr = 24000; audio = np.zeros(int((total + 0.3) * sr), dtype=np.float32)
    for t0, pid in pas:
        a, _ = sf.read(f"{voz_dir}/{pid}.wav", dtype="float32"); i = int(t0 * sr); audio[i:i + len(a)] += a
    n = int(fundido * sr); fin = int(total * sr); audio[fin - n:fin] *= np.linspace(1, 0, n); audio[fin:] = 0
    sf.write(salida + ".crudo.wav", audio, sr); normalizar(salida + ".crudo.wav", salida + ".wav")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", salida + ".wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    negro = fondo()
    for f in range(int(total * FPS)):
        tt = f / FPS; act = [(a, d, b) for a, d, b in plan if a <= tt < a + d] or [plan[-1]]
        a, d, b = act[0]; img = b["render"](tt - a, d, b["marcas"])
        if len(act) > 1:
            a2, d2, b2 = act[1]; img = Image.blend(img, b2["render"](tt - a2, d2, b2["marcas"]), ease((tt - a2) / XFADE))
        for s0, s1, txt in subs:
            if s0 <= tt < s1: subtitulo(img, txt); break
        if tt > total - fundido: img = Image.blend(img, negro, ease((tt - (total - fundido)) / fundido))
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait()
    return total, [(round(a, 2), round(d, 2), b.get("nombre", "")) for a, d, b in plan]

def previsualizar_continuo(beats, voz_dir, guion, momentos, salida):
    plan, total, subs, pas = planear_continuo(beats, voz_dir, guion); ims = []
    for i, fr in momentos:
        b = beats[i]; im = b["render"](fr * b["duracion"], b["duracion"], b["marcas"]); tt = plan[i][0] + fr * b["duracion"]
        for s0, s1, txt in subs:
            if s0 <= tt < s1: subtitulo(im, txt); break
        ims.append(im.resize((640, 360)))
    cols = 3; filas = (len(ims) + cols - 1) // cols; hoja = Image.new("RGB", (cols * 646, filas * 366), "white")
    for k, im in enumerate(ims): hoja.paste(im, ((k % cols) * 646, (k // cols) * 366))
    hoja.save(salida); return [(round(a, 2), round(d, 2), b.get("nombre", "")) for a, d, b in plan], total
