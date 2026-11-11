"use client";
import type { Calendario, Supuestos } from "@/lib/modelo";
import { fechaLarga } from "@/lib/modelo";

export function SelectorFecha({ cal, fecha, onFecha }: { cal: Calendario; fecha: string; onFecha: (f: string) => void }) {
  const i = cal.dias.findIndex((d) => d.fecha === fecha);
  const ventana = cal.dias.slice(Math.max(0, i - 3), Math.max(7, i + 4));
  return (
    <div>
      <div className="grid grid-cols-7 gap-1">
        {ventana.map((d) => {
          const corte = d.zonas_sin_servicio.length > 0;
          return (
            <button key={d.fecha} onClick={() => onFecha(d.fecha)} title={fechaLarga(d.fecha)}
              className={`rounded-lg px-1 py-1.5 text-center text-xs font-medium ${d.fecha === fecha ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"}`}>
              <div className="capitalize">{d.dia.slice(0, 3)}</div>
              <div className="text-[10px] opacity-70">{d.fecha.slice(8)}{corte ? " ·" : ""}</div>
            </button>
          );
        })}
      </div>
      <input type="range" min={0} max={cal.dias.length - 1} value={i} onChange={(e) => onFecha(cal.dias[+e.target.value].fecha)} className="mt-2 w-full" />
    </div>
  );
}

export function Deslizador({ label, value, min, max, step = 1, unidad = "", onChange }: { label: string; value: number; min: number; max: number; step?: number; unidad?: string; onChange: (v: number) => void }) {
  return (
    <label className="block text-sm">
      <span className="flex justify-between text-slate-700"><span>{label}</span><b className="tabular-nums">{value}{unidad}</b></span>
      <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(+e.target.value)} className="w-full" />
    </label>
  );
}

export function Supuestos({ s, onChange }: { s: Supuestos; onChange: (s: Supuestos) => void }) {
  return (
    <div className="space-y-2">
      <Deslizador label="Consumo por persona" value={s.consumo} min={50} max={150} step={25} unidad=" L/día" onChange={(v) => onChange({ ...s, consumo: v })} />
      <Deslizador label="Horas efectivas de corte" value={s.horasEfectivas} min={24} max={48} step={6} unidad=" h" onChange={(v) => onChange({ ...s, horasEfectivas: v })} />
      <Deslizador label="Tinaco" value={s.tinaco} min={600} max={2500} step={100} unidad=" L" onChange={(v) => onChange({ ...s, tinaco: v })} />
    </div>
  );
}
