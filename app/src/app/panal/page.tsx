"use client";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";
import { useDatos } from "@/lib/datos";
import { estadoColonia, resumenDia, SUPUESTOS, fmt, pct, fechaLarga, type Supuestos as TS } from "@/lib/modelo";
import { Badge, Kpi } from "@/components/ui";
import { SelectorFecha, Supuestos } from "@/components/Controles";
import { colorPct } from "@/components/HexMap";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false, loading: () => <div className="grid h-full place-items-center text-slate-400">Cargando mapa…</div> });

export default function Panal() {
  const datos = useDatos();
  const [version, setVersion] = useState<"octubre" | "noviembre">("noviembre");
  const [fecha, setFecha] = useState("2026-11-12");
  const [tresD, setTresD] = useState(true);
  const [sel, setSel] = useState<string | null>(null);
  const [s, setS] = useState<TS>(SUPUESTOS);
  const [verCis, setVerCis] = useState(false);

  const cal = datos?.calendarios[version];
  const estados = useMemo(() => (datos && cal ? datos.colonias.map((c) => estadoColonia(c, cal, fecha, s)) : []), [datos, cal, fecha, s]);
  const r = useMemo(() => resumenDia(estados), [estados]);
  const e = estados.find((x) => x.colonia.id === sel);

  if (!datos || !cal) return <div className="p-10 text-slate-500">Cargando datos…</div>;

  return (
    <div className="relative h-[calc(100vh-3.5rem)]">
      <HexMap estados={estados} cisternas={verCis ? datos.cisternas : []} tresD={tresD} seleccion={sel} onSeleccion={setSel} />

      {/* controles arriba a la izquierda */}
      <div className="absolute left-4 top-4 flex gap-2">
        <div className="flex rounded-full bg-white p-1 shadow">
          {(["octubre", "noviembre"] as const).map((v) => (
            <button key={v} onClick={() => setVersion(v)} className={`rounded-full px-3 py-1 text-sm font-medium capitalize ${version === v ? "bg-slate-900 text-white" : "text-slate-700"}`}>Calendario {v}</button>
          ))}
        </div>
        <button onClick={() => setTresD(!tresD)} className="rounded-full bg-white px-3 py-1 text-sm font-medium shadow">{tresD ? "Ver 2D" : "Ver 3D"}</button>
        <button onClick={() => setVerCis(!verCis)} className={`rounded-full px-3 py-1 text-sm font-medium shadow ${verCis ? "bg-orange-500 text-white" : "bg-white"}`}>60 cisternas</button>
      </div>

      {/* panel lateral */}
      <aside className="absolute right-4 top-4 bottom-4 w-[22rem] overflow-y-auto rounded-2xl bg-white/95 p-5 shadow-xl backdrop-blur">
        <div className="text-xs font-semibold uppercase tracking-wider text-blue-700">Panal · Tlaquepaque</div>
        <div className="text-lg font-bold capitalize">{fechaLarga(fecha)}</div>
        <div className="mt-1 text-xs text-slate-500">Zonas sin servicio hoy: {cal.dias.find((d) => d.fecha === fecha)?.zonas_sin_servicio.join(", ") || "ninguna"}</div>

        {e ? (
          <div className="mt-4">
            <button onClick={() => setSel(null)} className="text-xs text-blue-700">← Volver al resumen</button>
            <div className="mt-1 text-xl font-bold">{e.colonia.nombre}</div>
            <div className="text-sm text-slate-600">Zona {e.colonia.zona} · {e.colonia.manzanas} manzanas · {fmt(e.colonia.pob)} personas</div>
            <div className="mt-1"><Badge tipo="simulado" /> <span className="text-xs text-slate-500">{e.colonia.simulado}</span></div>
            <div className="mt-4 text-4xl font-bold tabular-nums" style={{ color: `rgb(${colorPct(e.pct_sin_agua).join(",")})` }}>{pct(e.pct_sin_agua)}</div>
            <div className="text-sm text-slate-600">de las viviendas sin agua · {fmt(e.personas_sin_agua)} personas</div>
            <div className="mt-1 text-xs text-slate-500">{e.horas_sin_servicio} h acumuladas sin servicio</div>
            <div className="mt-4 text-sm font-semibold">Composición de viviendas</div>
            {e.estratos.map((x) => (
              <div key={x.nombre} className="mt-2">
                <div className="flex justify-between text-sm"><span>{x.nombre}</span><span className="tabular-nums">{fmt(x.viviendas)} {x.seca ? "· seca" : x.guardada ? "· agua guardada" : "· con agua"}</span></div>
                <div className="h-2 rounded bg-slate-100"><div className={`h-2 rounded ${x.seca ? "bg-slate-300" : x.guardada ? "bg-sky-300" : "bg-blue-600"}`} style={{ width: `${(x.viviendas / e.colonia.viviendas) * 100}%` }} /></div>
                <div className="text-[11px] text-slate-500">{x.autonomia_h === 0 ? "Sin reserva: se queda sin agua en cuanto hay corte" : `Aguanta ${x.autonomia_h.toFixed(0)} h con ${s.consumo} L/persona/día`}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-4 space-y-4">
            <Kpi valor={pct(r.pct_viv_sin_agua)} etiqueta="de las viviendas sin agua hoy" badge="estimado" />
            <div className="grid grid-cols-2 gap-3">
              <Kpi valor={fmt(r.personas_sin_agua)} etiqueta="personas sin agua" badge="estimado" />
              <Kpi valor={String(r.colonias_afectadas)} etiqueta="colonias afectadas" badge="simulado" />
            </div>
            <Kpi valor={fmt(r.viv_agua_guardada)} etiqueta={`viviendas con agua guardada más de ${s.U} h (desinfectar)`} badge="estimado" />
          </div>
        )}

        <div className="mt-5 border-t pt-4">
          <SelectorFecha cal={cal} fecha={fecha} onFecha={setFecha} />
        </div>

        <div className="mt-4 border-t pt-4">
          <div className="text-sm font-semibold">Color: % de viviendas sin agua · altura: personas</div>
          <div className="mt-1 h-2 rounded" style={{ background: "linear-gradient(90deg, rgb(29,78,216), rgb(226,232,240))" }} />
          <div className="flex justify-between text-xs text-slate-500"><span>todas con agua</span><span>todas secas</span></div>
        </div>

        <details className="mt-4 border-t pt-4">
          <summary className="cursor-pointer text-sm font-semibold">Supuestos (mueven el mapa)</summary>
          <div className="mt-2"><Supuestos s={s} onChange={setS} /></div>
          <p className="mt-2 text-[11px] text-slate-500">Con 50 L/persona/día un tinaco de 1,100 L dura más que el ciclo: solo se seca quien no tiene dónde guardar. A 100–150 L también fallan las casas con tinaco.</p>
        </details>

        <p className="mt-4 text-[11px] text-slate-400">Cada hexágono representa una colonia (no su forma real). Toca uno para ver su composición y su fuente.</p>
      </aside>
    </div>
  );
}
