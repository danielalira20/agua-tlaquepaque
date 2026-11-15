"use client";
import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { H3HexagonLayer } from "@deck.gl/geo-layers";
import { ScatterplotLayer } from "@deck.gl/layers";
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
  cisterna: [249, 115, 22, 240], aproximada: [253, 186, 116, 220], propuesta: [168, 85, 247, 230], pipa: [15, 23, 42, 230],
};

export function puntosCisternas(cs: Cisterna[], verPropuestas: boolean): Punto[] {
  return cs.filter((c) => c.lon != null && c.lat != null && (verPropuestas || c.tipo !== "propuesta_municipio")).map((c) => ({
    id: c.id, lon: c.lon!, lat: c.lat!,
    tipo: c.tipo === "propuesta_municipio" ? "propuesta" : c.ubicacion === "centro_de_colonia" ? "aproximada" : "cisterna",
    texto: c.tipo === "propuesta_municipio" ? `Propuesta del municipio · ${c.colonia}` : `Cisterna${c.ubicacion === "centro_de_colonia" ? " (ubicación aproximada)" : ""} · ${c.colonia}`,
  }));
}

type Props = {
  celdas: Celda[]; puntos?: Punto[]; tresD: boolean; modo?: "agua" | "marginacion";
  seleccion?: string | null; onSeleccion?: (h3: string | null) => void; resaltar?: Set<string>;
};

export default function HexMap({ celdas, puntos = [], tresD, modo = "agua", seleccion, onSeleccion, resaltar }: Props) {
  const div = useRef<HTMLDivElement>(null);
  const mapa = useRef<maplibregl.Map | null>(null);
  const overlay = useRef<MapboxOverlay | null>(null);

  useEffect(() => {
    if (!div.current || mapa.current) return;
    const m = new maplibregl.Map({ container: div.current, style: ESTILO, center: [-103.31, 20.6], zoom: 11.4, pitch: 50, bearing: -15, attributionControl: false });
    m.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
    m.addControl(new maplibregl.AttributionControl({ compact: true }));
    const o = new MapboxOverlay({ interleaved: false, layers: [] });
    m.addControl(o);
    mapa.current = m; overlay.current = o;
    return () => { m.remove(); mapa.current = null; };
  }, []);

  useEffect(() => { mapa.current?.easeTo({ pitch: tresD ? 50 : 0, bearing: tresD ? -15 : 0, duration: 600 }); }, [tresD]);

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
  }, [celdas, puntos, tresD, modo, seleccion, onSeleccion, resaltar]);

  return <div ref={div} className="h-full w-full" />;
}
