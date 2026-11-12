"use client";
import type { Calendario } from "@/lib/real";
import { fechaLarga } from "@/lib/real";
import type { SupuestosMotor } from "@/lib/motor";

export function SelectorFecha({ cal, fecha, onFecha }: { cal: Calendario; fecha: string; onFecha: (f: string) => void }) {
  return (
    <div className="grid grid-cols-7 gap-1">
      {cal.dias.map((d) => (
        <button key={d.fecha} onClick={() => onFecha(d.fecha)} title={`${fechaLarga(d.fecha)} · zonas sin servicio: ${d.zonas_sin_servicio.join(", ") || "ninguna"}`}
          className={`rounded-lg px-1 py-1.5 text-center text-xs font-medium ${d.fecha === fecha ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"}`}>
          <div className="capitalize">{d.dia.slice(0, 3)}</div>
          <div className="text-[10px] opacity-70">{d.fecha.slice(8)}</div>
        </button>
      ))}
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

/** Lo interactivo del motor: consumo, f y horas efectivas. El resto viene de motor/supuestos.json. */
export function Supuestos({ s, onChange }: { s: SupuestosMotor; onChange: (s: SupuestosMotor) => void }) {
  return (
    <div className="space-y-2">
      <Deslizador label="Tamaño del tinaco" value={s.tinaco_l} min={600} max={1100} step={100} unidad=" L" onChange={(v) => onChange({ ...s, tinaco_l: v })} />
      <Deslizador label="Consumo por persona" value={s.consumo_l_persona_dia} min={50} max={150} step={25} unidad=" L/día" onChange={(v) => onChange({ ...s, consumo_l_persona_dia: v })} />
      <Deslizador label="Agua que sí llega en racionamiento (f)" value={s.fraccion_suministro_en_racionamiento * 100} min={0} max={50} step={25} unidad=" %" onChange={(v) => onChange({ ...s, fraccion_suministro_en_racionamiento: v / 100 })} />
      <Deslizador label="Horas efectivas del primer día" value={s.horas_efectivas_corte} min={24} max={48} step={12} unidad=" h" onChange={(v) => onChange({ ...s, horas_efectivas_corte: v })} />
    </div>
  );
}

/** Cuántos días aguanta un tinaco con los supuestos actuales (lo que más mueve el orden de las manzanas). */
export function diasTinaco(s: SupuestosMotor, ocupantes = 3.8) {
  return s.tinaco_l / (ocupantes * s.consumo_l_persona_dia * (1 - s.fraccion_suministro_en_racionamiento));
}

export function Advertencias({ lista, className = "" }: { lista: string[]; className?: string }) {
  return (
    <details className={`rounded-xl border border-amber-200 bg-amber-50 p-3 text-xs text-amber-900 ${className}`}>
      <summary className="cursor-pointer font-semibold">Lo que hay que saber de estos números ({lista.length})</summary>
      <ul className="mt-2 list-disc space-y-1 pl-4">{lista.map((a) => <li key={a}>{a}</li>)}</ul>
    </details>
  );
}
