"use client";
import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { H3HexagonLayer } from "@deck.gl/geo-layers";
import { ScatterplotLayer, TextLayer } from "@deck.gl/layers";
import type { Celda, Cisterna } from "@/lib/real";

const ESTILO = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json";
type RGB = [number, number, number];

/** Agua llena = azul; seco = barro. Se satura en 50 % (umbral de quiebre mayoritario). */
export const SATURA = 0.5;
// paradas de la escala: agua-600 → agua-200 → barro-200 → barro-500
const PARADAS: [number, RGB][] = [[0, [31, 95, 174]], [0.4, [169, 212, 236]], [0.7, [232, 195, 162]], [1, [196, 98, 58]]];
export function colorPct(p: number): RGB {
  const t = Math.sqrt(Math.min(1, Math.max(0, p) / SATURA));
  for (let i = 1; i < PARADAS.length; i++) {
    const [t1, b] = PARADAS[i];
    if (t <= t1) {
      const [t0, a] = PARADAS[i - 1];
      const k = (t - t0) / (t1 - t0);
      return [0, 1, 2].map((j) => Math.round(a[j] + (b[j] - a[j]) * k)) as RGB;
    }
  }
  return PARADAS[PARADAS.length - 1][1];
}
/** La misma escala como degradado CSS, para la leyenda. */
export const GRADIENTE_AGUA = `linear-gradient(90deg, ${PARADAS.map(([t, c]) => `rgb(${c.join(",")}) ${t * 100}%`).join(", ")})`;
export const COLOR_MARG: Record<string, RGB> = {
  "Muy alto": [127, 29, 29], Alto: [220, 38, 38], Medio: [251, 146, 60], Bajo: [254, 215, 170], "Muy bajo": [255, 247, 237], "sin dato": [203, 213, 225],
};
const FUERA: RGB = [214, 214, 208]; // fuera del programa: gris neutro, no se confunde con barro

export type Punto = { id: string; lon: number; lat: number; tipo: "cisterna" | "aproximada" | "propuesta" | "pipa"; texto: string };
const COLOR_PUNTO: Record<Punto["tipo"], [number, number, number, number]> = {
  cisterna: [249, 115, 22, 240], aproximada: [253, 186, 116, 220], propuesta: [168, 85, 247, 230], pipa: [26, 76, 142, 235],
};

export function puntosCisternas(cs: Cisterna[], verPropuestas: boolean): Punto[] {
  return cs.filter((c) => c.lon != null && c.lat != null && (verPropuestas || c.tipo !== "propuesta_municipio")).map((c) => ({
    id: c.id, lon: c.lon!, lat: c.lat!,
    tipo: c.tipo === "propuesta_municipio" ? "propuesta" : c.ubicacion === "centro_de_colonia" ? "aproximada" : "cisterna",
    texto: c.tipo === "propuesta_municipio" ? `Propuesta del municipio · ${c.colonia}` : `Cisterna${c.ubicacion === "centro_de_colonia" ? " (ubicación aproximada)" : ""} · ${c.colonia}`,
  }));
}

/** Número sobre el mapa (paradas de pipa). */
export type Rotulo = { id: string; lon: number; lat: number; texto: string };

type Props = {
  celdas: Celda[]; puntos?: Punto[]; rotulos?: Rotulo[]; tresD: boolean; modo?: "agua" | "marginacion";
  seleccion?: string | null; onSeleccion?: (h3: string | null) => void; resaltar?: Set<string>;
  /** En escritorio, píxeles que tapa una tarjeta a la izquierda: el mapa se centra en lo que queda libre. */
  margenIzq?: number;
  /** Puntos que deben quedar a la vista (por ejemplo, las paradas del día). */
  encuadre?: [number, number][];
};

export default function HexMap({ celdas, puntos = [], rotulos = [], tresD, modo = "agua", seleccion, onSeleccion, resaltar, margenIzq = 0, encuadre }: Props) {
  const div = useRef<HTMLDivElement>(null);
  const mapa = useRef<maplibregl.Map | null>(null);
  const overlay = useRef<MapboxOverlay | null>(null);

  useEffect(() => {
    if (!div.current || mapa.current) return;
    const m = new maplibregl.Map({ container: div.current, style: ESTILO, center: [-103.31, 20.6], zoom: 11.4, pitch: 50, bearing: -15, attributionControl: false });
    m.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
    m.addControl(new maplibregl.AttributionControl({ compact: true }));
    if (margenIzq && window.innerWidth >= 768) m.setPadding({ left: margenIzq, top: 0, right: 0, bottom: 0 });
    const o = new MapboxOverlay({ interleaved: false, layers: [] });
    m.addControl(o);
    mapa.current = m; overlay.current = o;
    return () => { m.remove(); mapa.current = null; };
  }, []);

  useEffect(() => { mapa.current?.easeTo({ pitch: tresD ? 50 : 0, bearing: tresD ? -15 : 0, duration: 600 }); }, [tresD]);

  // encuadra el mapa en los puntos pedidos cuando cambian (clave: sus coordenadas)
  const claveEncuadre = encuadre?.map((p) => p.join(",")).join(";") ?? "";
  useEffect(() => {
    const m = mapa.current;
    if (!m || !encuadre || encuadre.length === 0) return;
    let w = Infinity, so = Infinity, e = -Infinity, n = -Infinity;
    for (const [lon, lat] of encuadre) { w = Math.min(w, lon); e = Math.max(e, lon); so = Math.min(so, lat); n = Math.max(n, lat); }
    m.fitBounds([[w, so], [e, n]], { padding: 60, maxZoom: 13.5, duration: 700 });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [claveEncuadre]);

  useEffect(() => {
    if (!overlay.current) return;
    const maxP = Math.max(1, ...celdas.map((c) => c.pers_max));
    overlay.current.setProps({
      layers: [
        new H3HexagonLayer<Celda>({
          id: "panal", data: celdas, pickable: true, extruded: tresD, coverage: 0.92,
          getHexagon: (c) => c.h3,
          getFillColor: (c) => {
            const col = modo === "marginacion" ? COLOR_MARG[c.marg] ?? COLOR_MARG["sin dato"] : c.en_programa ? colorPct(c.pct_min) : FUERA;
            return [...col, resaltar && !resaltar.has(c.h3) ? 60 : 235] as [number, number, number, number];
          },
          getElevation: (c) => (modo === "agua" ? 40 + (c.pers_min / maxP) * 1400 : 40),
          getLineColor: (c) => (c.h3 === seleccion ? [15, 23, 42, 255] : [255, 255, 255, 140]),
          getLineWidth: (c) => (c.h3 === seleccion ? 5 : 1), lineWidthUnits: "pixels", stroked: true,
          onClick: (p) => onSeleccion?.(p.object ? p.object.h3 : null),
          updateTriggers: { getFillColor: [celdas, modo, resaltar], getElevation: [celdas, modo], getLineColor: [seleccion], getLineWidth: [seleccion] },
          transitions: { getFillColor: 350, getElevation: 350 },
        }),
        new ScatterplotLayer<Punto>({
          id: "puntos", data: puntos, getPosition: (p) => [p.lon, p.lat], getRadius: 70, radiusMinPixels: 3.5, pickable: true,
          getFillColor: (p) => COLOR_PUNTO[p.tipo], getLineColor: [255, 255, 255], lineWidthMinPixels: 1, stroked: true,
        }),
        new TextLayer<Rotulo>({
          id: "rotulos", data: rotulos, getPosition: (r) => [r.lon, r.lat], getText: (r) => r.texto,
          getSize: 13, sizeUnits: "pixels", getColor: [255, 255, 255, 255], fontWeight: 700, fontFamily: "system-ui, sans-serif",
          characterSet: "0123456789", getPixelOffset: [0, -16], background: true, getBackgroundColor: [26, 76, 142, 245],
          backgroundPadding: [6, 3], backgroundBorderRadius: 9,
        }),
      ],
      getTooltip: ({ object }: { object?: Celda | Punto }) => {
        if (!object) return null;
        if ("h3" in object) {
          const col = object.colonias.slice(0, 3).join(", ") + (object.colonias.length > 3 ? ` y ${object.colonias.length - 3} más` : "");
          return { text: `${col}\nZona ${object.zonas.join(", ") || "fuera del programa"} · ${object.manzanas.length} manzanas\nSin agua: ${Math.round(object.pct_min * 100)}–${Math.round(object.pct_max * 100)} % de viviendas` };
        }
        return { text: object.texto };
      },
    });
  }, [celdas, puntos, rotulos, tresD, modo, seleccion, onSeleccion, resaltar]);

  return <div ref={div} className="h-full w-full" />;
}
