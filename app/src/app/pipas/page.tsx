"use client";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";
import { latLngToCell } from "h3-js";
import { useReal, calcular, rango, fmt, fechaLarga } from "@/lib/real";
import { Badge, Tarjeta } from "@/components/ui";
import { SelectorFecha } from "@/components/Controles";
import { puntosCisternas, type Punto } from "@/components/HexMap";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false });

type Viaje = { orden_eleccion: number; colonia: string; lon: number; lat: number; manzanas_cubiertas: { cvegeo: string; viviendas: number }[]; viviendas_objetivo: number; personas_beneficiadas: number; prioridad_score: number };

export default function Pipas() {
  const d = useReal();
  const [fecha, setFecha] = useState("2026-11-12");
  const [cota, setCota] = useState<"min" | "max">("min");
  const [sel, setSel] = useState<string | null>(null);

  const cal = d?.calendarios.vigente;
  const res = useMemo(() => (d && cal ? calcular(d, cal, fecha, d.meta.supuestos) : null), [d, cal, fecha]);
  const corrida = (regla: string) => d?.plan.corridas.find((c: any) => c.regla === regla && c.cota_para_ordenar === cota);
  const pri = corrida("priorizado"), base = corrida("baseline");
  const dPri = pri?.fechas.find((x: any) => x.fecha === fecha), dBase = base?.fechas.find((x: any) => x.fecha === fecha);
  const viajes: Viaje[] = dPri?.viajes ?? [];

  // agrupar viajes por colonia para la lista
  const porColonia = useMemo(() => {
    const m = new Map<string, { colonia: string; viajes: number; viv: number; pers: number; primero: number; lon: number; lat: number }>();
    for (const v of viajes) {
      const k = v.colonia || "sin colonia";
      const x = m.get(k) ?? { colonia: k, viajes: 0, viv: 0, pers: 0, primero: v.orden_eleccion, lon: v.lon, lat: v.lat };
      x.viajes++; x.viv += v.viviendas_objetivo; x.pers += v.personas_beneficiadas; x.primero = Math.min(x.primero, v.orden_eleccion);
      m.set(k, x);
    }
    return [...m.values()].sort((a, b) => a.primero - b.primero);
  }, [viajes]);

  const resaltar = useMemo(() => new Set(viajes.map((v) => latLngToCell(v.lat, v.lon, 8))), [viajes]);
  const puntos: Punto[] = useMemo(() => [
    ...(d ? puntosCisternas(d.cisternas, false) : []),
    ...viajes.map((v) => ({ id: `v${v.orden_eleccion}`, lon: v.lon, lat: v.lat, tipo: "pipa" as const, texto: `Pipa · ${v.colonia} · ${v.viviendas_objetivo} viviendas` })),
  ], [d, viajes]);

  if (!d || !cal || !res || !dPri) return <div className="p-10 text-slate-500">Cargando…</div>;
  const rp = dPri.resumen, rb = dBase.resumen;
  const semC = (c: string) => d.plan.comparacion.find((x: any) => x.cota_para_ordenar === c).semana;
  const sMin = semC("min"), sMax = semC("max");
  const dia = (regla: string, c: string) => d.plan.corridas.find((x: any) => x.regla === regla && x.cota_para_ordenar === c).fechas.find((x: any) => x.fecha === fecha).resumen;

  return (
    <div className="grid h-[calc(100vh-3.5rem)] grid-cols-[1fr_27rem]">
      <div className="relative">
        <HexMap celdas={res.celdas} puntos={puntos} tresD={false} resaltar={resaltar} seleccion={sel} onSeleccion={setSel} />
        <div className="absolute left-4 top-4 rounded-full bg-white px-3 py-1 text-xs shadow">Resaltados: hexágonos con pipa hoy · <span className="text-slate-900">●</span> punto de pipa · <span className="text-orange-500">●</span> cisterna</div>
      </div>
      <aside className="overflow-y-auto border-l bg-white p-5">
        <div className="flex items-center justify-between"><div className="text-xs font-semibold uppercase tracking-wider text-blue-700">Operador de pipas</div><Badge tipo="estimado" /></div>
        <div className="text-lg font-bold capitalize">{fechaLarga(fecha)}</div>
        <div className="mt-3"><SelectorFecha cal={cal} fecha={fecha} onFecha={setFecha} /></div>
        <div className="mt-3 flex rounded-full bg-slate-100 p-1 text-xs">
          {(["min", "max"] as const).map((c) => <button key={c} onClick={() => setCota(c)} className={`flex-1 rounded-full py-1 font-medium ${cota === c ? "bg-white shadow" : ""}`}>Ordenar por cota {c === "min" ? "mínima" : "máxima"}</button>)}
        </div>

        <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-xl bg-blue-50 p-3"><div className="text-xs text-blue-900">Priorizado</div><div className="text-xl font-bold tabular-nums">{rango(dia("priorizado", "min").viviendas_atendidas, dia("priorizado", "max").viviendas_atendidas)}</div><div className="text-xs text-slate-600">viviendas secas atendidas hoy (ordenando por cota mín. – máx.)</div></div>
          <div className="rounded-xl bg-slate-50 p-3"><div className="text-xs text-slate-600">Baseline estilizado</div><div className="text-xl font-bold tabular-nums">{rango(dia("baseline", "min").viviendas_atendidas, dia("baseline", "max").viviendas_atendidas)}</div><div className="text-xs text-slate-600">con los mismos {rb.viajes_usados} viajes, por turnos entre cisternas</div></div>
        </div>
        <p className="mt-3 rounded-lg bg-blue-50 p-3 text-xs text-blue-900">En la semana, con los mismos 441 viajes: <b>{rango(sMin.viviendas_atendidas.priorizado, sMax.viviendas_atendidas.priorizado)}</b> viviendas atendidas priorizando contra <b>{rango(sMin.viviendas_atendidas.baseline, sMax.viviendas_atendidas.baseline)}</b> en el baseline. En 120 simulaciones con otros supuestos, el priorizador atiende entre <b>2.6 y 4.9 veces</b> lo que el reparto por turnos; contra un reparto que solo visita las cisternas con necesidad ese día, la ventaja va de <b>1.1 a 3.1 veces</b> según la cota y el escenario. No pedimos más agua ni más pipas.</p>
        <p className="mt-2 rounded-lg border border-amber-200 bg-amber-50 p-3 text-xs text-amber-900"><b>Lo que sí y lo que no aguanta.</b> La ventaja del priorizador se mantiene en todos los escenarios que probamos, aunque es pequeña en los peores; <b>dónde se para cada pipa, no</b>: solo el 37 % de las manzanas atendidas coincide con el caso base. Estos puntos son el plan con los supuestos base; si cambia un supuesto, el plan se recalcula. Los puntos fijos (cisternas permanentes) deben salir del núcleo robusto. La marginación no pesa en la prioridad: con la cota máxima, las AGEB de marginación «Muy alto» pueden quedarse sin viajes (el reporte lo detalla).</p>
        <p className="mt-2 text-[11px] text-slate-500">Necesidad hoy: {rango(dia("priorizado", "min").necesidad_total, dia("priorizado", "max").necesidad_total)} viviendas sin agua en el programa. Hoy en todo el municipio: {rango(res.resumen.sin_min, res.resumen.sin_max)}.</p>

        <div className="mt-4 text-sm font-semibold">Colonias con pipa hoy ({porColonia.length})</div>
        <ol className="mt-2 space-y-2">
          {porColonia.map((x, i) => (
            <li key={x.colonia} onClick={() => setSel(latLngToCell(x.lat, x.lon, 8))} className="cursor-pointer rounded-xl border border-slate-200 p-3 text-sm hover:border-slate-400">
              <div className="flex items-center gap-2"><span className="grid h-6 w-6 place-items-center rounded-full bg-blue-700 text-xs font-bold text-white">{i + 1}</span><b>{x.colonia}</b></div>
              <div className="mt-1 text-xs text-slate-600">{x.viajes} viaje{x.viajes > 1 ? "s" : ""} · {fmt(x.viv)} viviendas objetivo · {fmt(x.pers)} personas</div>
            </li>
          ))}
        </ol>
        <Tarjeta className="mt-4 text-xs text-slate-600">
          32 pipas, 63 viajes al día, 10,000 L por viaje, 200 L por hogar, radio de cobertura de {d.plan.parametros.radio_cobertura_m} m (parámetro declarado). <b>El baseline es estilizado</b>: los mismos viajes repartidos por turnos entre las cisternas instaladas; no es lo que hace hoy el municipio. El orden de la lista es el orden en que el priorizador eligió los puntos, <b>no una ruta</b>.
        </Tarjeta>
      </aside>
    </div>
  );
}
