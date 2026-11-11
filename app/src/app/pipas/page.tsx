"use client";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";
import { useDatos } from "@/lib/datos";
import { estadoColonia, priorizar, resumenDia, SUPUESTOS, fmt, fechaLarga } from "@/lib/modelo";
import { Badge, Kpi, Tarjeta } from "@/components/ui";
import { SelectorFecha } from "@/components/Controles";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false });

export default function Pipas() {
  const datos = useDatos();
  const [fecha, setFecha] = useState("2026-11-12");
  const [sel, setSel] = useState<string | null>(null);
  const cal = datos?.calendarios.noviembre;
  const estados = useMemo(() => (datos && cal ? datos.colonias.map((c) => estadoColonia(c, cal, fecha, SUPUESTOS)) : []), [datos, cal, fecha]);
  const p = useMemo(() => priorizar(estados), [estados]);
  const r = resumenDia(estados);
  const ids = useMemo(() => new Set(p.plan.map((x) => x.estado.colonia.id)), [p]);
  if (!datos || !cal) return <div className="p-10 text-slate-500">Cargando…</div>;

  // cobertura actual: las 60 cisternas solo cubren a quien vive en su colonia (supuesto simple para la demo)
  const conCis = new Set(datos.cisternas.map((c) => c.colonia_id));
  const cubiertasHoy = estados.filter((e) => e.viv_sin_agua > 0 && conCis.has(e.colonia.id)).reduce((n, e) => n + e.personas_sin_agua, 0);

  return (
    <div className="grid h-[calc(100vh-3.5rem)] grid-cols-[1fr_26rem]">
      <div className="relative">
        <HexMap estados={estados} cisternas={datos.cisternas} tresD={false} seleccion={sel} onSeleccion={setSel} resaltar={ids} />
        <div className="absolute left-4 top-4 rounded-full bg-white px-3 py-1 text-xs shadow">Resaltadas: colonias con pipa asignada hoy · <span className="text-orange-600">●</span> cisternas actuales</div>
      </div>
      <aside className="overflow-y-auto border-l bg-white p-5">
        <div className="text-xs font-semibold uppercase tracking-wider text-blue-700">Operador de pipas</div>
        <div className="text-lg font-bold capitalize">{fechaLarga(fecha)}</div>
        <div className="mt-3"><SelectorFecha cal={cal} fecha={fecha} onFecha={setFecha} /></div>

        <div className="mt-4 grid grid-cols-2 gap-3">
          <Kpi valor={`${p.viajesUsados}/63`} etiqueta="viajes asignados (32 pipas)" badge="estimado" />
          <Kpi valor={fmt(p.personasAtendidas)} etiqueta="personas atendidas con las mismas pipas" badge="simulado" />
          <Kpi valor={fmt(cubiertasHoy)} etiqueta="personas sin agua con cisterna en su colonia (cobertura actual)" badge="simulado" />
          <Kpi valor={fmt(r.personas_sin_agua)} etiqueta="personas sin agua hoy en total" badge="estimado" />
        </div>
        <p className="mt-3 rounded-lg bg-blue-50 p-3 text-xs text-blue-900">No pedimos más agua ni más pipas: las mismas 32 pipas y 63 viajes, repartidos primero a donde más viviendas están secas y más marginación hay (dataset 17, CONAPO).</p>

        <div className="mt-4 text-sm font-semibold">Orden del día <Badge tipo="simulado" /></div>
        <ol className="mt-2 space-y-2">
          {p.plan.map((x, i) => (
            <li key={x.estado.colonia.id} onClick={() => setSel(x.estado.colonia.id)} className={`cursor-pointer rounded-xl border p-3 text-sm ${sel === x.estado.colonia.id ? "border-slate-900" : "border-slate-200"}`}>
              <div className="flex items-center gap-2"><span className="grid h-6 w-6 place-items-center rounded-full bg-blue-700 text-xs font-bold text-white">{i + 1}</span><b>{x.estado.colonia.nombre}</b><span className="ml-auto text-xs text-slate-500">zona {x.estado.colonia.zona}</span></div>
              <div className="mt-1 grid grid-cols-3 gap-1 text-xs text-slate-600">
                <span>{x.viajes} viaje{x.viajes > 1 ? "s" : ""} · {fmt(x.litros)} L</span>
                <span>{fmt(x.viviendas_objetivo)} viv. objetivo</span>
                <span>{fmt(x.estado.viv_sin_agua)} viv. secas</span>
              </div>
              <div className="mt-1 text-[11px] text-slate-500">Por qué: {(x.estado.pct_sin_agua * 100).toFixed(0)} % de viviendas sin agua · marginación {x.estado.colonia.marginacion.toFixed(2)} · {conCis.has(x.estado.colonia.id) ? "ya tiene cisterna" : "sin cisterna comunitaria"}</div>
            </li>
          ))}
          {p.plan.length === 0 && <li className="text-sm text-slate-500">Hoy ninguna colonia se queda sin agua. Las pipas quedan libres.</li>}
        </ol>
        <Tarjeta className="mt-4 text-xs text-slate-600">
          Supuestos: 10,000 L por viaje, 200 L por hogar (50 hogares por viaje), 63 viajes/día (prensa, oct-2026). La asignación es un algoritmo glotón; el plan real sale del optimizador de Jass (plan.json).
        </Tarjeta>
      </aside>
    </div>
  );
}
