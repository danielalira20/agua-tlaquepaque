"use client";
import { useMemo, useState } from "react";
import { useReal, fechaLarga, fmt } from "@/lib/real";
import { autonomiaH, horasDeZonas, parsearZonas } from "@/lib/motor";
import { Badge, Tarjeta } from "@/components/ui";

type Alm = "ninguno" | "tinaco" | "cisterna" | "ambos";

export default function MiCasa() {
  const d = useReal();
  const [colonia, setColonia] = useState("El Sauz");
  const [alm, setAlm] = useState<Alm>("ninguno");
  const [personas, setPersonas] = useState(4);
  const [consumo, setConsumo] = useState(50);

  const colonias = useMemo(() => {
    if (!d) return [];
    const m = new Map<string, Set<string>>();
    for (const x of d.manzanas) if (x.colonia) { if (!m.has(x.colonia)) m.set(x.colonia, new Set()); parsearZonas(x.zona).forEach((z) => m.get(x.colonia)!.add(z)); }
    return [...m.entries()].map(([nombre, z]) => ({ nombre, zonas: [...z].sort() })).sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
  }, [d]);

  const r = useMemo(() => {
    if (!d) return null;
    const col = colonias.find((c) => c.nombre === colonia);
    if (!col) return null;
    const s = d.meta.supuestos, cal = d.calendarios.vigente;
    const litros = { ninguno: 0, tinaco: s.tinaco_l, cisterna: s.cisterna_l, ambos: s.tinaco_l + s.cisterna_l }[alm];
    const aut = autonomiaH(litros, personas, consumo, 0);
    // si la colonia abarca varias zonas, se toma el peor caso por día (cota alta)
    const semana = cal.dias.map((x) => {
      const H = Math.max(...horasDeZonas(col.zonas, cal.esquema, x.fecha, s.horas_efectivas_corte));
      return { ...x, H, corte: H > 0, seca: aut < H };
    });
    const cis = d.cisternas.filter((c) => c.colonia === colonia && c.tipo !== "propuesta_municipio" && c.cuenta_como_cobertura).length;
    return { col, aut, semana, cis, primera: semana.find((x) => x.seca) };
  }, [d, colonias, colonia, alm, personas, consumo]);

  if (!d || !r) return <div className="p-10 text-slate-500">Cargando…</div>;
  const fuera = r.col.zonas.length === 0;

  return (
    <main className="mx-auto grid max-w-5xl gap-6 p-6 md:grid-cols-[1fr_1.2fr]">
      <Tarjeta>
        <h1 className="text-2xl font-bold">¿Cuánto aguanta tu casa?</h1>
        <p className="mt-1 text-sm text-slate-600">Dinos cómo guardas agua y te decimos qué días de esta semana te quedas sin ella, según el calendario vigente del SIAPA.</p>
        <label className="mt-5 block text-sm font-medium">Tu colonia
          <select value={colonia} onChange={(e) => setColonia(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-2">
            {colonias.map((c) => <option key={c.nombre} value={c.nombre}>{c.nombre} · {c.zonas.length ? `zona ${c.zonas.join(", ")}` : "sin racionamiento"}</option>)}
          </select>
        </label>
        <div className="mt-4 text-sm font-medium">¿Cómo guardas agua?</div>
        <div className="mt-1 flex flex-wrap gap-2">
          {([["ninguno", "Nada"], ["tinaco", "Tinaco"], ["cisterna", "Cisterna"], ["ambos", "Ambos"]] as [Alm, string][]).map(([v, t]) => (
            <button key={v} onClick={() => setAlm(v)} className={`rounded-full px-4 py-1.5 text-sm font-medium ${alm === v ? "bg-blue-600 text-white" : "bg-slate-100"}`}>{t}</button>
          ))}
        </div>
        <label className="mt-4 block text-sm font-medium">¿Cuántas personas viven en tu casa? <b>{personas}</b>
          <input type="range" min={1} max={10} value={personas} onChange={(e) => setPersonas(+e.target.value)} className="w-full" />
        </label>
        <label className="mt-2 block text-sm font-medium">Consumo por persona: <b>{consumo} L/día</b> <span className="font-normal text-slate-500">(50 = mínimo OMS)</span>
          <input type="range" min={50} max={150} step={25} value={consumo} onChange={(e) => setConsumo(+e.target.value)} className="w-full" />
        </label>
        <p className="mt-4 text-xs text-slate-500">Supuestos: tinaco de {fmt(d.meta.supuestos.tinaco_l)} L y cisterna de {fmt(d.meta.supuestos.cisterna_l)} L llenos al empezar el racionamiento; un día de racionamiento = cero agua (la peor cota: el SIAPA dice que es baja de presión).</p>
      </Tarjeta>

      <div className="space-y-4">
        <div className="rounded-2xl bg-blue-700 p-5 text-white shadow">
          <div className="text-sm opacity-80">Tu casa en {r.col.nombre} ({fuera ? "sin racionamiento" : `zona ${r.col.zonas.join(", ")}`})</div>
          <div className="mt-1 text-3xl font-bold leading-tight">
            {fuera ? "Tu colonia no está en el programa de racionamiento" : r.aut === 0 ? "Sin reserva: te quedas sin agua cada día de racionamiento" : `Tu reserva aguanta ${r.aut < 48 ? `${r.aut.toFixed(0)} horas` : `${(r.aut / 24).toFixed(1)} días`}`}
          </div>
          {!fuera && <div className="mt-3 text-sm">{r.primera ? <>Esta semana te quedas sin agua desde el <b className="capitalize">{fechaLarga(r.primera.fecha)}</b>.</> : "Esta semana no te quedas sin agua."}</div>}
          {r.col.zonas.length > 1 && <div className="mt-2 text-xs opacity-80">Tu colonia abarca varias zonas: mostramos el peor caso.</div>}
        </div>

        <Tarjeta>
          <div className="text-sm font-semibold">Tu semana</div>
          <div className="mt-2 grid grid-cols-7 gap-1 text-center text-xs">
            {r.semana.map((x) => (
              <div key={x.fecha} className={`rounded-lg p-2 ${x.seca ? "bg-slate-200 text-slate-500" : x.corte ? "bg-sky-100 text-sky-900" : "bg-blue-600 text-white"}`}>
                <div className="capitalize">{x.dia.slice(0, 3)} {x.fecha.slice(8)}</div><div className="text-[10px]">{x.seca ? "sin agua" : x.corte ? `aguantas (${x.H} h)` : "llega"}</div>
              </div>
            ))}
          </div>
          <div className="mt-2"><Badge tipo="real" /> <span className="text-xs text-slate-500">calendario del portal del SIAPA, consultado el {d.calendarios.vigente.consultado}; puede cambiar</span></div>
        </Tarjeta>

        <Tarjeta>
          <div className="text-sm font-semibold">Si te quedas sin agua</div>
          <ul className="mt-2 space-y-1 text-sm text-slate-700">
            <li>🚰 Cisternas comunitarias en {r.col.nombre}: <b>{r.cis}</b> {r.cis === 0 && <span className="text-slate-500">(revisa la colonia vecina en el Panal)</span>}</li>
            <li>📱 Pide pipa por TlaqueChat, el WhatsApp del ayuntamiento (33 2804 8171, de 7:00 a 22:00)</li>
            <li>🧴 Agua guardada más de 2 días: <b>2 gotas de cloro sin aroma por litro (8 por galón) y reposar 30 min</b> antes de beberla o cocinar. <span className="text-xs text-slate-500">Fuente: CDC; con cloro de 8.25 % usa menos, lee la etiqueta.</span></li>
          </ul>
        </Tarjeta>

        <Tarjeta className="bg-[#e7f6e9]">
          <div className="text-xs text-slate-500">Aviso que recibiría la familia (maqueta) <Badge tipo="simulado" /></div>
          <div className="mt-2 rounded-xl rounded-tl-none bg-white p-3 text-sm shadow-sm">
            Hola 👋 En <b>{r.col.nombre}</b> {r.primera ? <>te quedarías sin agua el <b className="capitalize">{fechaLarga(r.primera.fecha)}</b>. Llena todo lo que puedas la noche anterior.</> : "esta semana tu reserva alcanza."} {r.cis ? "Hay cisterna comunitaria en tu colonia." : "La cisterna más cercana está en una colonia vecina."} Recuerda clorar el agua guardada.
          </div>
        </Tarjeta>
      </div>
    </main>
  );
}
