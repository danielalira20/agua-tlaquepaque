"use client";
import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { H3HexagonLayer } from "@deck.gl/geo-layers";
import { ScatterplotLayer } from "@deck.gl/layers";
import type { Estado, Cisterna } from "@/lib/modelo";

const ESTILO = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json";

/** Azul lleno = con agua; pálido = seco. El panal se vacía conforme avanza el calendario. */
export function colorPct(p: number): [number, number, number] {
  const a: [number, number, number] = [29, 78, 216];   // blue-700
  const b: [number, number, number] = [226, 232, 240]; // slate-200
  return [0, 1, 2].map((i) => Math.round(a[i] + (b[i] - a[i]) * p)) as [number, number, number];
}

type Props = {
  estados: Estado[]; cisternas?: Cisterna[]; tresD: boolean;
  seleccion?: string | null; onSeleccion?: (id: string | null) => void;
  resaltar?: Set<string>;
};

export default function HexMap({ estados, cisternas = [], tresD, seleccion, onSeleccion, resaltar }: Props) {
  const div = useRef<HTMLDivElement>(null);
  const mapa = useRef<maplibregl.Map | null>(null);
  const overlay = useRef<MapboxOverlay | null>(null);

  useEffect(() => {
    if (!div.current || mapa.current) return;
    const m = new maplibregl.Map({ container: div.current, style: ESTILO, center: [-103.3, 20.6], zoom: 11.6, pitch: 50, bearing: -15, attributionControl: false });
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
    const maxP = Math.max(1, ...estados.map((e) => e.personas_sin_agua));
    overlay.current.setProps({
      layers: [
        new H3HexagonLayer<Estado>({
          id: "colonias", data: estados, pickable: true, extruded: tresD, coverage: 0.9, elevationScale: 1,
          getHexagon: (e) => e.colonia.h3,
          getFillColor: (e) => {
            const c = colorPct(e.pct_sin_agua);
            const dim = resaltar && !resaltar.has(e.colonia.id);
            return [...c, dim ? 70 : 230] as [number, number, number, number];
          },
          getElevation: (e) => 150 + (e.personas_sin_agua / maxP) * 1200,
          getLineColor: (e) => (e.colonia.id === seleccion ? [15, 23, 42, 255] : [255, 255, 255, 120]),
          getLineWidth: (e) => (e.colonia.id === seleccion ? 6 : 1), lineWidthUnits: "pixels", stroked: true,
          onClick: (p) => onSeleccion?.(p.object ? p.object.colonia.id : null),
          updateTriggers: { getFillColor: [estados, resaltar], getElevation: [estados], getLineColor: [seleccion], getLineWidth: [seleccion] },
          transitions: { getFillColor: 400, getElevation: 400 },
        }),
        new ScatterplotLayer<Cisterna>({
          id: "cisternas", data: cisternas, getPosition: (c) => [c.lng, c.lat], getRadius: 55, radiusMinPixels: 3,
          getFillColor: [249, 115, 22, 230], getLineColor: [255, 255, 255], lineWidthMinPixels: 1, stroked: true, pickable: true,
        }),
      ],
      getTooltip: ({ object }: { object?: Estado | Cisterna }) => {
        if (!object) return null;
        if ("colonia" in object) return { text: `${object.colonia.nombre} · zona ${object.colonia.zona}\n${(object.pct_sin_agua * 100).toFixed(0)} % de viviendas sin agua · ${object.personas_sin_agua.toLocaleString("es-MX")} personas` };
        return { text: "Cisterna comunitaria (ubicación simulada)" };
      },
    });
  }, [estados, cisternas, tresD, seleccion, onSeleccion, resaltar]);

  return <div ref={div} className="h-full w-full" />;
}
