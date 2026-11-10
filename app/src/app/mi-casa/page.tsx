"use client";
import { useMemo, useState } from "react";
import { useDatos } from "@/lib/datos";
import { autonomiaHoras, horasSinServicio, SUPUESTOS, fechaLarga, fmt } from "@/lib/modelo";
import { Badge, Tarjeta } from "@/components/ui";

type Alm = "ninguno" | "tinaco" | "cisterna" | "ambos";

export default function MiCasa() {
  const datos = useDatos();
  const [coloniaId, setColoniaId] = useState("c001");
  const [alm, setAlm] = useState<Alm>("ninguno");
  const [personas, setPersonas] = useState(4);
  const [consumo, setConsumo] = useState(50);
  const hoy = "2026-11-11";

  const r = useMemo(() => {
    if (!datos) return null;
    const c = datos.colonias.find((x) => x.id === coloniaId)!;
    const cal = datos.calendarios.noviembre;
    const litros = { ninguno: 0, tinaco: SUPUESTOS.tinaco, cisterna: SUPUESTOS.cisterna, ambos: SUPUESTOS.tinaco + SUPUESTOS.cisterna }[alm];
    const aut = litros ? autonomiaHoras(litros, personas, consumo) : 0;
    const i = cal.dias.findIndex((d) => d.fecha === hoy);
    const prox = cal.dias.slice(i).find((d) => d.zonas_sin_servicio.includes(c.zona));
    // primer día en que las horas acumuladas sin servicio superan la autonomía
    const seca = cal.dias.slice(i).find((d) => horasSinServicio(cal, c.zona, d.fecha, SUPUESTOS.horasEfectivas) > aut);
    const cis = datos.cisternas.filter((x) => x.colonia_id === c.id).length;
    const semana = cal.dias.slice(i, i + 7);
    return { c, aut, prox, seca, cis, semana, cal };
  }, [datos, coloniaId, alm, personas, consumo]);

  if (!datos || !r) return <div className="p-10 text-slate-500">Cargando…</div>;

  return (
    <main className="mx-auto grid max-w-5xl gap-6 p-6 md:grid-cols-[1fr_1.2fr]">
      <Tarjeta>
        <h1 className="text-2xl font-bold">¿Cuánto aguanta tu casa?</h1>
        <p className="mt-1 text-sm text-slate-600">Dinos cómo guardas agua y te decimos cuándo te vas a quedar sin ella según el calendario del SIAPA.</p>
        <label className="mt-5 block text-sm font-medium">Tu colonia
          <select value={coloniaId} onChange={(e) => setColoniaId(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-300 p-2">
            {datos.colonias.map((c) => <option key={c.id} value={c.id}>{c.nombre} · zona {c.zona}</option>)}
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
      </Tarjeta>

      <div className="space-y-4">
        <div className="rounded-2xl bg-blue-700 p-5 text-white shadow">
          <div className="text-sm opacity-80">Tu casa en {r.c.nombre} (zona {r.c.zona})</div>
          <div className="mt-1 text-3xl font-bold">
            {r.aut === 0 ? "Sin reserva: te quedas sin agua en cuanto hay corte" : `Aguanta ${r.aut < 48 ? `${r.aut.toFixed(0)} horas` : `${(r.aut / 24).toFixed(1)} días`}`}
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
            <div><div className="opacity-70">Próximo corte</div><div className="font-semibold capitalize">{r.prox ? fechaLarga(r.prox.fecha) : "—"}</div></div>
            <div><div className="opacity-70">Te quedas sin agua</div><div className="font-semibold capitalize">{r.seca ? fechaLarga(r.seca.fecha) : "no en estas 2 semanas"}</div></div>
          </div>
          <div className="mt-3"><Badge tipo="simulado" /> <span className="text-xs opacity-80">calendario y colonias por confirmar</span></div>
        </div>

        <Tarjeta>
          <div className="text-sm font-semibold">Tu semana</div>
          <div className="mt-2 grid grid-cols-7 gap-1 text-center text-xs">
            {r.semana.map((d) => {
              const corte = d.zonas_sin_servicio.includes(r.c.zona);
              const sec = horasSinServicio(r.cal, r.c.zona, d.fecha, SUPUESTOS.horasEfectivas) > r.aut;
              return <div key={d.fecha} className={`rounded-lg p-2 ${sec ? "bg-slate-200 text-slate-500" : corte ? "bg-sky-100 text-sky-900" : "bg-blue-600 text-white"}`}><div className="capitalize">{d.dia.slice(0, 3)}</div><div className="text-[10px]">{sec ? "sin agua" : corte ? "corte" : "llega"}</div></div>;
            })}
          </div>
        </Tarjeta>

        <Tarjeta>
          <div className="text-sm font-semibold">Si te quedas sin agua</div>
          <ul className="mt-2 space-y-1 text-sm text-slate-700">
            <li>🚰 Cisternas comunitarias en tu colonia: <b>{r.cis}</b> <Badge tipo="simulado" /></li>
            <li>📱 Pide pipa por TlaqueChat (WhatsApp del ayuntamiento)</li>
            <li>🧴 Agua guardada más de 2 días: <b>2 gotas de cloro por litro y reposar 30 min</b> antes de usarla para cocinar o beber.</li>
          </ul>
        </Tarjeta>

        <Tarjeta className="bg-[#e7f6e9]">
          <div className="text-xs text-slate-500">Aviso que recibiría la familia (maqueta)</div>
          <div className="mt-2 rounded-xl rounded-tl-none bg-white p-3 text-sm shadow-sm">
            Hola 👋 En <b>{r.c.nombre}</b> {r.prox ? <>el corte es el <b className="capitalize">{fechaLarga(r.prox.fecha)}</b></> : "no hay cortes próximos"}. {r.aut === 0 ? "Llena todo lo que puedas la noche anterior." : `Tu reserva alcanza ${(r.aut / 24).toFixed(1)} días.`} Cisterna más cercana: {r.cis ? "en tu colonia" : "colonia vecina"}. Recuerda clorar el agua guardada.
          </div>
        </Tarjeta>
      </div>
    </main>
  );
}
