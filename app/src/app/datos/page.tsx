"use client";
import { useMemo } from "react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useReal, rango, fmt, personasDia } from "@/lib/real";
import { evaluarManzana, parsearZonas } from "@/lib/motor";
import { Badge, Tarjeta } from "@/components/ui";
import { Advertencias } from "@/components/Controles";

const AZUL = "#1d4ed8", CLARO = "#93c5fd", GRIS = "#94a3b8";
const k = (v: number) => `${Math.round(v / 1000)}k`;
const GRADOS = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo", "sin dato"];

export default function Datos() {
  const d = useReal();
  const g = useMemo(() => {
    if (!d) return null;
    const s = d.meta.supuestos, cv = d.calendarios.vigente, co = d.calendarios.original;
    const mz = d.manzanas.filter((m) => m.viviendas > 0);

    // 1. personas sin agua por día, vigente vs original, con cotas
    const porDia = cv.dias.map((x) => {
      const fila: Record<string, any> = { dia: `${x.dia.slice(0, 3)} ${x.fecha.slice(8)}` };
      for (const [nom, cal] of [["vigente", cv], ["original", co]] as const) {
        let a = 0, b = 0;
        for (const m of mz) { const o = evaluarManzana(m, cal.esquema, x.fecha, s); a += o.viv_sin_agua_min * m.ocupantes_prom; b += o.viv_sin_agua_max * m.ocupantes_prom; }
        fila[nom] = [Math.round(a), Math.round(b)];
      }
      return fila;
    });
    const sem = { vig: personasDia(d, cv, s), ori: personasDia(d, co, s) };

    // 2. sensibilidad: consumo × f (personas-día de la semana, cota mínima y máxima)
    const sens = [50, 75, 100, 125, 150].map((c) => {
      const fila: Record<string, any> = { consumo: `${c} L` };
      for (const f of [0, 0.25, 0.5]) { const r = personasDia(d, cv, { ...s, consumo_l_persona_dia: c, fraccion_suministro_en_racionamiento: f }); fila[`f${f}`] = Math.round(r.min); fila[`f${f}max`] = Math.round(r.max); }
      return fila;
    });

    // 3. dónde está el riesgo: viviendas sin almacenamiento por zona (solo dentro del programa)
    const zonas: Record<string, { min: number; max: number }> = {};
    for (const m of mz) { if (!m.en_programa) continue; const z = parsearZonas(m.zona).join(" y ") || "?"; zonas[z] ??= { min: 0, max: 0 }; zonas[z].min += m.sin_almacen_min; zonas[z].max += m.sin_almacen_max; }
    const porZona = Object.entries(zonas).sort((a, b) => b[1].min - a[1].min).map(([z, v]) => ({ zona: `Zona ${z}`, minimo: v.min, rango: v.max - v.min }));

    // 4. equidad: por grado de marginación (capa aparte)
    const eq = GRADOS.map((gr) => {
      const ms = mz.filter((m) => m.grado_marginacion === gr);
      let pmin = 0, pmax = 0;
      for (const x of cv.dias) for (const m of ms) { const o = evaluarManzana(m, cv.esquema, x.fecha, s); pmin += o.viv_sin_agua_min * m.ocupantes_prom; pmax += o.viv_sin_agua_max * m.ocupantes_prom; }
      return { gr, viv: ms.reduce((n, m) => n + m.viviendas, 0), pob: ms.reduce((n, m) => n + m.pob, 0), smin: ms.reduce((n, m) => n + m.sin_almacen_min, 0), smax: ms.reduce((n, m) => n + m.sin_almacen_max, 0), pmin, pmax };
    });

    // 5. colonias con más viviendas sin almacenamiento
    const col: Record<string, { viv: number; pob: number; min: number; max: number; zonas: Set<string> }> = {};
    for (const m of mz) { if (!m.colonia) continue; const c = (col[m.colonia] ??= { viv: 0, pob: 0, min: 0, max: 0, zonas: new Set() }); c.viv += m.viviendas; c.pob += m.pob; c.min += m.sin_almacen_min; c.max += m.sin_almacen_max; parsearZonas(m.zona).forEach((z) => c.zonas.add(z)); }
    const top = Object.entries(col).sort((a, b) => b[1].min - a[1].min).slice(0, 12);

    const tot = mz.reduce((a, m) => ({ viv: a.viv + m.viviendas, min: a.min + m.sin_almacen_min, max: a.max + m.sin_almacen_max, tin: a.tin + m.viv_tinaco, cis: a.cis + m.viv_cisterna }), { viv: 0, min: 0, max: 0, tin: 0, cis: 0 });
    return { porDia, sem, sens, porZona, eq, top, tot };
  }, [d]);

  if (!d || !g) return <div className="p-10 text-slate-500">Calculando con el motor…</div>;
  const c = d.meta.conteos;

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Datos y modelo</h1>
          <p className="text-sm text-slate-600">Todo se calcula en tu navegador con el motor oficial, a partir de las {fmt(c.manzanas)} manzanas reales. Siempre mostramos cota mínima y máxima.</p>
        </div>
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs text-emerald-900">✓ Motor oficial (TypeScript) = motor de referencia (Python): 34,097 de 34,097 renglones iguales</div>
      </div>
      <Advertencias lista={d.meta.advertencias} />

      <div className="grid gap-4 md:grid-cols-4">
        <Tarjeta><div className="text-2xl font-bold">{fmt(c.personas)}</div><div className="text-sm text-slate-600">personas en Tlaquepaque · {fmt(c.personas_en_programa)} dentro del programa</div><Badge tipo="real" /></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">{rango(g.tot.min, g.tot.max)}</div><div className="text-sm text-slate-600">viviendas sin tinaco ni cisterna</div><Badge tipo="real" /></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">{rango(g.sem.vig.min, g.sem.vig.max)}</div><div className="text-sm text-slate-600">personas-día sin agua, semana 9–15 nov (calendario vigente)</div><Badge tipo="estimado" /></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">×{(g.sem.vig.min / g.sem.ori.min).toFixed(1)}</div><div className="text-sm text-slate-600">personas-día con el calendario vigente contra el original (cota mínima)</div><Badge tipo="estimado" /></Tarjeta>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Tarjeta>
          <h2 className="font-semibold">Personas sin agua por día: calendario vigente vs. original</h2>
          <p className="mb-2 text-xs text-slate-500">La banda va de la cota mínima a la máxima.</p>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={g.porDia}><CartesianGrid stroke="#e2e8f0" /><XAxis dataKey="dia" fontSize={11} /><YAxis fontSize={11} tickFormatter={k} />
              <Tooltip formatter={(v: any) => (Array.isArray(v) ? `${fmt(v[0])} – ${fmt(v[1])}` : v)} /><Legend />
              <Area dataKey="original" name="Original (15-oct)" stroke={CLARO} fill={CLARO} fillOpacity={0.35} />
              <Area dataKey="vigente" name="Vigente (4-nov)" stroke={AZUL} fill={AZUL} fillOpacity={0.35} />
            </AreaChart>
          </ResponsiveContainer>
        </Tarjeta>
        <Tarjeta>
          <h2 className="font-semibold">Sensibilidad: consumo y agua que sí llega (f)</h2>
          <p className="mb-2 text-xs text-slate-500">Personas-día sin agua en la semana (cota mínima). El consumo es lo que más mueve el resultado; f casi no mueve a 50 L porque quien no tiene dónde guardar se seca igual.</p>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={g.sens}><CartesianGrid stroke="#e2e8f0" /><XAxis dataKey="consumo" fontSize={11} /><YAxis fontSize={11} tickFormatter={k} /><Tooltip formatter={(v: number) => fmt(v)} /><Legend />
              <Line dataKey="f0" name="f = 0 (corte total)" stroke={AZUL} strokeWidth={2} /><Line dataKey="f0.25" name="f = 25 %" stroke="#3b82f6" strokeWidth={2} strokeDasharray="5 3" /><Line dataKey="f0.5" name="f = 50 %" stroke={CLARO} strokeWidth={2} strokeDasharray="2 2" />
            </LineChart>
          </ResponsiveContainer>
        </Tarjeta>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Tarjeta>
          <h2 className="font-semibold">Dónde está el riesgo: viviendas sin almacenamiento por zona</h2>
          <p className="mb-2 text-xs text-slate-500">Solo manzanas dentro del programa. Barra oscura: cota mínima; clara: hasta la máxima.</p>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={g.porZona} layout="vertical" margin={{ left: 20 }}><CartesianGrid stroke="#e2e8f0" /><XAxis type="number" fontSize={11} tickFormatter={k} /><YAxis type="category" dataKey="zona" fontSize={11} width={70} /><Tooltip formatter={(v: number) => fmt(v)} />
              <Bar dataKey="minimo" name="cota mínima" stackId="a" fill={AZUL} /><Bar dataKey="rango" name="hasta la máxima" stackId="a" fill={CLARO} />
            </BarChart>
          </ResponsiveContainer>
        </Tarjeta>
        <Tarjeta>
          <h2 className="font-semibold">Equidad: por grado de marginación</h2>
          <p className="mb-2 text-xs text-slate-500">CONAPO 2020 por AGEB (dataset 17). Es una capa aparte: no entra en el cálculo ni en la prioridad de las pipas.</p>
          <table className="w-full text-sm"><thead className="text-left text-xs text-slate-500"><tr><th>Grado</th><th className="text-right">Personas</th><th className="text-right">Viv. sin almacén</th><th className="text-right">Personas-día sin agua</th></tr></thead>
            <tbody>{g.eq.map((x) => <tr key={x.gr} className="border-t"><td>{x.gr}</td><td className="text-right tabular-nums">{fmt(x.pob)}</td><td className="text-right tabular-nums">{rango(x.smin, x.smax)}</td><td className="text-right tabular-nums">{rango(x.pmin, x.pmax)}</td></tr>)}</tbody></table>
        </Tarjeta>
      </div>

      <Tarjeta>
        <h2 className="font-semibold">Colonias con más viviendas sin tinaco ni cisterna</h2>
        <table className="mt-2 w-full text-sm"><thead className="text-left text-xs text-slate-500"><tr><th>Colonia</th><th>Zona</th><th className="text-right">Personas</th><th className="text-right">Viviendas sin almacén</th><th className="text-right">% de sus viviendas</th></tr></thead>
          <tbody>{g.top.map(([n, x]) => <tr key={n} className="border-t"><td>{n}</td><td>{[...x.zonas].sort().join(", ") || <span className="text-amber-700">fuera del programa</span>}</td><td className="text-right tabular-nums">{fmt(x.pob)}</td><td className="text-right tabular-nums">{rango(x.min, x.max)}</td><td className="text-right tabular-nums">{Math.round((100 * x.min) / x.viv)}–{Math.round((100 * x.max) / x.viv)} %</td></tr>)}</tbody></table>
      </Tarjeta>

      <div className="grid gap-6 md:grid-cols-2">
        <Tarjeta>
          <h2 className="font-semibold">Cómo se calcula</h2>
          <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-slate-700">
            <li>Cada manzana se parte en estratos: con tinaco y cisterna, solo tinaco, solo cisterna, nada. El Censo no los cruza, así que el número de viviendas con ambos va en un intervalo, y todo resultado sale como cota mínima y máxima.</li>
            <li>Autonomía de un estrato = litros ÷ (ocupantes × consumo × (1 − f)) × 24 h. Sin almacenamiento = 0 h.</li>
            <li>Horas sin servicio: el primer día de racionamiento cuenta {d.meta.supuestos.horas_efectivas_corte} h y cada día seguido suma 24. Con varias zonas, el intervalo se ensancha.</li>
            <li>Un estrato se queda sin agua si su autonomía es menor que esas horas. Si aguanta pero el agua lleva más de {d.meta.supuestos.u_horas_agua_guardada} h guardada, hay que desinfectarla.</li>
            <li>Detalle completo en <code>motor/ESPECIFICACION.md</code>.</li>
          </ol>
        </Tarjeta>
        <Tarjeta>
          <h2 className="font-semibold">Datasets y fuentes</h2>
          <table className="mt-2 w-full text-sm"><thead className="text-left text-xs text-slate-500"><tr><th>#</th><th>Fuente</th><th>Para qué</th></tr></thead><tbody>
            <tr className="border-t"><td>01</td><td>INEGI · Censo 2020 por manzana</td><td>Viviendas, ocupantes, tinaco y cisterna: alimentan el motor</td></tr>
            <tr className="border-t"><td>17</td><td>CONAPO · marginación urbana por AGEB 2020</td><td>Capa de equidad en el mapa y tabla por grado</td></tr>
            <tr className="border-t"><td>—</td><td>SIAPA · portal de rotación y lista oficial ({d.calendarios.vigente.consultado})</td><td>Zona de cada manzana y calendario por fecha (complemento)</td></tr>
            <tr className="border-t"><td>—</td><td>Gobierno de Tlaquepaque · mapa de cisternas</td><td>{fmt(c.cisternas)} cisternas y {fmt(c.propuestas)} propuestas (complemento)</td></tr>
          </tbody></table>
        </Tarjeta>
      </div>
    </main>
  );
}
