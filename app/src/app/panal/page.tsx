"use client";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";
import { useReal, calcular, rango, fmt, fechaLarga } from "@/lib/real";
import type { SupuestosMotor } from "@/lib/motor";
import { Badge } from "@/components/ui";
import { Advertencias, SelectorFecha, Supuestos, diasTinaco } from "@/components/Controles";
import { COLOR_MARG, colorPct, puntosCisternas } from "@/components/HexMap";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false, loading: () => <div className="grid h-full place-items-center text-slate-400">Cargando mapa…</div> });

const CONF: Record<string, string> = { alta: "alta", media: "media", baja: "baja", conflicto: "fuentes en conflicto", ambiguo: "ambigua", ninguna: "fuera del programa", sin_poligono: "sin polígono", sin_geometria: "sin ubicación" };

export default function Panal() {
  const d = useReal();
  const [version, setVersion] = useState<"vigente" | "original">("vigente");
  const [fecha, setFecha] = useState("2026-11-12");
  const [tresD, setTresD] = useState(true);
  const [modo, setModo] = useState<"agua" | "marginacion">("agua");
  const [sel, setSel] = useState<string | null>(null);
  const [s, setS] = useState<SupuestosMotor | null>(null);
  const [verCis, setVerCis] = useState(true);
  const [verProp, setVerProp] = useState(false);
  const [verNucleo, setVerNucleo] = useState(false);

  const sup = s ?? d?.meta.supuestos ?? null;
  const cal = d?.calendarios[version];
  const res = useMemo(() => (d && cal && sup ? calcular(d, cal, fecha, sup) : null), [d, cal, fecha, sup]);
  const hayNucleo = !!d?.manzanas.some((m) => m.nucleo_robusto);
  const nNucleo = useMemo(() => d?.manzanas.filter((m) => m.nucleo_robusto).length ?? 0, [d]);
  const resaltar = useMemo(() => (verNucleo && res ? new Set(res.celdas.filter((c) => c.nucleo > 0).map((c) => c.h3)) : undefined), [verNucleo, res]);
  // parte del riesgo de almacenamiento en zonas 5 y 6 (dentro del programa), con las dos cotas
  const z56 = useMemo(() => {
    if (!d) return null;
    let t0 = 0, t1 = 0, a = 0, b = 0;
    for (const m of d.manzanas) {
      if (!m.en_programa || !(m.viviendas > 0)) continue;
      const z = m.zona.split(",").filter(Boolean);
      t0 += m.sin_almacen_min; t1 += m.sin_almacen_max;
      if (z.every((x) => x === "5" || x === "6")) { a += m.sin_almacen_min; b += m.sin_almacen_max; }
    }
    return { min: (100 * a) / t0, max: (100 * b) / t1 };
  }, [d]);
  const puntos = useMemo(() => (d && verCis ? puntosCisternas(d.cisternas, verProp) : []), [d, verCis, verProp]);
  if (!d || !cal || !sup || !res) return <div className="p-10 text-slate-500">Cargando datos reales…</div>;

  const r = res.resumen;
  const c = res.celdas.find((x) => x.h3 === sel);
  const dia = cal.dias.find((x) => x.fecha === fecha);

  // detalle de la celda: composición por estrato (cotas) y confianza de la zona
  const det = c && (() => {
    let tin = 0, cis = 0, nada_min = 0, nada_max = 0;
    const conf: Record<string, number> = {};
    for (const i of c.manzanas) {
      const m = d.manzanas[i];
      tin += m.viv_tinaco; cis += m.viv_cisterna; nada_min += m.sin_almacen_min; nada_max += m.sin_almacen_max;
      conf[m.zona_confianza] = (conf[m.zona_confianza] ?? 0) + m.pob;
    }
    return { tin, cis, nada_min, nada_max, conf };
  })();

  return (
    <div className="relative h-[calc(100vh-3.5rem)]">
      <HexMap celdas={res.celdas} puntos={puntos} tresD={tresD} modo={modo} seleccion={sel} onSeleccion={setSel} resaltar={resaltar} />

      <div className="absolute left-4 top-4 flex flex-wrap gap-2">
        <div className="flex rounded-full bg-white p-1 shadow">
          {(["vigente", "original"] as const).map((v) => (
            <button key={v} onClick={() => setVersion(v)} className={`rounded-full px-3 py-1 text-sm font-medium ${version === v ? "bg-slate-900 text-white" : "text-slate-700"}`}>
              {v === "vigente" ? "Calendario vigente (4-nov)" : "Original (15-oct)"}
            </button>
          ))}
        </div>
        <div className="flex rounded-full bg-white p-1 shadow">
          {(["agua", "marginacion"] as const).map((v) => (
            <button key={v} onClick={() => setModo(v)} className={`rounded-full px-3 py-1 text-sm font-medium ${modo === v ? "bg-blue-700 text-white" : "text-slate-700"}`}>{v === "agua" ? "Sin agua" : "Marginación"}</button>
          ))}
        </div>
        <button onClick={() => setTresD(!tresD)} className="rounded-full bg-white px-3 py-1 text-sm font-medium shadow">{tresD ? "Ver 2D" : "Ver 3D"}</button>
        <button onClick={() => setVerCis(!verCis)} className={`rounded-full px-3 py-1 text-sm font-medium shadow ${verCis ? "bg-orange-500 text-white" : "bg-white"}`}>Cisternas</button>
        <button disabled={!hayNucleo} onClick={() => setVerNucleo(!verNucleo)} title={hayNucleo ? "Manzanas que quedan entre las 250 más críticas en al menos el 90 % de las simulaciones" : "Pendiente: falta el campo nucleo_robusto en manzanas.json"}
          className={`rounded-full px-3 py-1 text-sm font-medium shadow disabled:opacity-50 ${verNucleo ? "bg-amber-500 text-white" : "bg-white"}`}>Núcleo robusto{hayNucleo ? ` (${nNucleo})` : ""}</button>
        <button onClick={() => setVerProp(!verProp)} className={`rounded-full px-3 py-1 text-sm font-medium shadow ${verProp ? "bg-purple-600 text-white" : "bg-white"}`}>10 propuestas</button>
      </div>

      <aside className="absolute bottom-4 right-4 top-4 w-[23rem] overflow-y-auto rounded-2xl bg-white/95 p-5 shadow-xl backdrop-blur">
        <div className="flex items-center justify-between">
          <div className="text-xs font-semibold uppercase tracking-wider text-blue-700">Panal · Tlaquepaque</div>
          <Badge tipo="real" />
        </div>
        <div className="text-lg font-bold capitalize">{fechaLarga(fecha)}</div>
        <div className="text-xs text-slate-500">Zonas con racionamiento hoy: {dia?.zonas_sin_servicio.join(", ") || "ninguna"}</div>

        {c && det ? (
          <div className="mt-4">
            <button onClick={() => setSel(null)} className="text-xs text-blue-700">← Volver al resumen</button>
            <div className="mt-1 text-lg font-bold leading-snug">{c.colonias.slice(0, 4).join(", ")}{c.colonias.length > 4 ? ` y ${c.colonias.length - 4} más` : ""}</div>
            <div className="text-sm text-slate-600">Zona {c.zonas.join(", ") || "fuera del programa"} · {c.manzanas.length} manzanas · {fmt(c.pob)} personas</div>
            <div className="mt-3 text-3xl font-bold tabular-nums" style={{ color: `rgb(${colorPct(c.pct_min).join(",")})` }}>{Math.round(c.pct_min * 100)}–{Math.round(c.pct_max * 100)} %</div>
            <div className="text-sm text-slate-600">de las viviendas sin agua · {rango(c.pers_min, c.pers_max)} personas</div>
            <div className="mt-4 text-sm font-semibold">Cómo guardan agua sus {fmt(c.viviendas)} viviendas</div>
            <ul className="mt-1 space-y-1 text-sm">
              <li className="flex justify-between"><span>Sin tinaco ni cisterna</span><b className="tabular-nums">{rango(det.nada_min, det.nada_max)}</b></li>
              <li className="flex justify-between"><span>Con tinaco</span><b className="tabular-nums">{fmt(det.tin)}</b></li>
              <li className="flex justify-between"><span>Con cisterna</span><b className="tabular-nums">{fmt(det.cis)}</b></li>
            </ul>
            <p className="mt-1 text-[11px] text-slate-500">El Censo no cruza tinaco con cisterna: por eso las viviendas sin nada van como rango.</p>
            <div className="mt-3 text-sm font-semibold">Confianza de la zona</div>
            <ul className="mt-1 text-xs text-slate-600">{Object.entries(det.conf).map(([k, v]) => <li key={k}>{CONF[k] ?? k}: {fmt(v)} personas</li>)}</ul>
            <div className="mt-2 text-xs text-slate-600">Marginación dominante: <b>{c.marg}</b> <span className="text-slate-400">(capa aparte, no entra en el cálculo)</span></div>
          </div>
        ) : (
          <div className="mt-4 space-y-4">
            <div>
              <div className="text-3xl font-bold tabular-nums">{rango(r.sin_min, r.sin_max)}</div>
              <div className="text-sm text-slate-600">viviendas sin agua hoy (cota mínima – máxima)</div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div><div className="text-xl font-bold tabular-nums">{rango(r.pers_min, r.pers_max)}</div><div className="text-xs text-slate-600">personas sin agua</div></div>
              <div><div className="text-xl font-bold tabular-nums">{fmt(r.mzas_quiebre)}</div><div className="text-xs text-slate-600">manzanas con 10 % o más de viviendas secas</div></div>
            </div>
            {z56 && <div><div className="text-xl font-bold tabular-nums">{z56.max.toFixed(1)} % – {z56.min.toFixed(1)} %</div><div className="text-xs text-slate-600">del riesgo de almacenamiento está en las zonas 5 y 6 ({z56.min.toFixed(1)} % con la cota mín., {z56.max.toFixed(1)} % con la máx.)</div></div>}
            <div><div className="text-xl font-bold tabular-nums">{rango(r.guard_min, r.guard_max)}</div><div className="text-xs text-slate-600">viviendas con agua guardada más de {sup.u_horas_agua_guardada} h: desinfectar</div></div>
          </div>
        )}

        <div className="mt-5 border-t pt-4"><SelectorFecha cal={cal} fecha={fecha} onFecha={setFecha} /></div>

        <div className="mt-4 border-t pt-4 text-sm">
          {modo === "agua" ? (
            <>
              <div className="font-semibold">Color: % de viviendas sin agua (cota mín.) · altura: personas</div>
              <div className="mt-1 h-2 rounded" style={{ background: "linear-gradient(90deg, rgb(29,78,216), rgb(226,232,240))" }} />
              <div className="flex justify-between text-xs text-slate-500"><span>todas con agua</span><span>50 % o más secas</span></div>
              <div className="mt-1 text-xs text-slate-500">Gris muy claro: fuera del programa de racionamiento.</div>
            </>
          ) : (
            <>
              <div className="font-semibold">Grado de marginación (CONAPO 2020, por AGEB)</div>
              <div className="mt-1 flex flex-wrap gap-2 text-xs">{Object.entries(COLOR_MARG).map(([k, v]) => <span key={k} className="flex items-center gap-1"><span className="h-3 w-3 rounded-sm" style={{ background: `rgb(${v.join(",")})` }} />{k}</span>)}</div>
            </>
          )}
          <div className="mt-2 flex flex-wrap gap-3 text-xs text-slate-600">
            <span><span className="text-orange-500">●</span> cisterna</span><span><span className="text-orange-300">●</span> ubicación aproximada</span><span><span className="text-purple-600">●</span> propuesta</span>
          </div>
        </div>

        <details className="mt-4 border-t pt-4">
          <summary className="cursor-pointer text-sm font-semibold">Supuestos (mueven el mapa)</summary>
          <div className="mt-2"><Supuestos s={sup} onChange={setS} /></div>
          <p className="mt-2 text-xs text-slate-600">Con estos supuestos un tinaco aguanta ~<b>{diasTinaco(sup).toFixed(1)} días</b> (casa de 3.8 personas). Con 6 o más días el orden de las manzanas es casi el del caso base; con menos de 4 cambia bastante. El caso base (50 L, 1,100 L) es el extremo más cómodo.</p>
          {s && <button onClick={() => setS(null)} className="mt-2 text-xs text-blue-700">Volver a los supuestos base</button>}
        </details>

        <Advertencias lista={d.meta.advertencias} className="mt-4" />
        <p className="mt-3 text-[11px] text-slate-400">Cada hexágono agrupa las manzanas reales que caen en él (H3, resolución 8). Toca uno para ver sus colonias y su composición.</p>
      </aside>
    </div>
  );
}
