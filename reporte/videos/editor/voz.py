"""Genera la narración con Kokoro (voz ef_dora, español latino).

Uso: python voz.py guion_<video>.json voz_<video>/

El guion puede traer "_pasajes": cada pasaje se sintetiza de corrido (una sola llamada, para que la entonación fluya
como una lectura real) y después se localiza dónde empieza y termina cada frase dentro del pasaje.
Salida en la carpeta: <id>.wav (pasaje, sin silencios en los bordes) y marcas.json con los tiempos de cada frase.
Necesita en editor/modelos/: kokoro-v1.0.onnx y voices-v1.0.bin (ver GUIA_EDICION_VIDEOS.md).
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

AQUI = os.path.dirname(os.path.abspath(__file__))
SR = 24000

def recortar(a, umbral=0.012, pad=0.03, fade=0.012):
    """Quita silencio al inicio y al final, y suaviza los bordes para que no truene."""
    idx = np.where(np.abs(a) > umbral)[0]
    if len(idx) == 0: return a
    a = a[max(0, idx[0] - int(pad * SR)): idx[-1] + int(pad * SR)].copy()
    n = int(fade * SR); a[:n] *= np.linspace(0, 1, n); a[-n:] *= np.linspace(1, 0, n)
    return a

def silencios(a, min_dur=0.07, rel=0.035):
    """Tramos de silencio (inicio, fin) en segundos dentro de un audio."""
    hop, win = int(0.010 * SR), int(0.025 * SR)
    env = np.array([np.sqrt(np.mean(a[i:i + win] ** 2)) for i in range(0, len(a) - win, hop)])
    lim = rel * env.max(); mudo = env < lim; tr = []; i = 0
    while i < len(mudo):
        if mudo[i]:
            j = i
            while j < len(mudo) and mudo[j]: j += 1
            if (j - i) * 0.010 >= min_dur: tr.append((i * 0.010 + 0.005, j * 0.010 + 0.005))
            i = j
        else: i += 1
    return tr

def localizar(pasaje, durs):
    """Reparte las frases del pasaje usando los silencios reales; durs = duración de cada frase sintetizada sola."""
    L = len(pasaje) / SR; tot = sum(durs); esp = np.cumsum(durs)[:-1] * L / tot
    tr = silencios(pasaje); usados = []; cortes = []
    for e in esp:
        cand = [(abs((s + f) / 2 - e) - 0.5 * (f - s), s, f) for s, f in tr if abs((s + f) / 2 - e) < 0.9 and (not usados or s > usados[-1][1])]
        if cand:
            _, s, f = min(cand); usados.append((s, f)); cortes.append((s, f))
        else: cortes.append((e, e))
    marcas = []; ini = 0.0
    for j in range(len(durs)):
        fin = cortes[j][0] if j < len(cortes) else L
        marcas.append((round(ini, 3), round(fin, 3)))
        if j < len(cortes): ini = cortes[j][1]
    return marcas

def main():
    k = Kokoro(os.path.join(AQUI, "modelos", "kokoro-v1.0.onnx"), os.path.join(AQUI, "modelos", "voices-v1.0.bin"))
    g = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    def decir(t):
        s, _ = k.create(t, voice="ef_dora", speed=1.0, lang="es-419"); return recortar(s.astype(np.float32))
    marcas = {}
    for p in g["_pasajes"]:
        texto = p.get("texto") or " ".join(g[c]["voz"] for c in p["claves"])
        aud = decir(texto); sf.write(os.path.join(out, p["id"] + ".wav"), aud, SR)
        durs = [len(decir(g[c]["voz"])) / SR for c in p["claves"]] if len(p["claves"]) > 1 else [len(aud) / SR]
        ms = localizar(aud, durs)
        marcas[p["id"]] = {"dur": round(len(aud) / SR, 3), "frases": {c: m for c, m in zip(p["claves"], ms)}}
        print(p["id"], marcas[p["id"]])
    json.dump(marcas, open(os.path.join(out, "marcas.json"), "w"), indent=1)

if __name__ == "__main__": main()
