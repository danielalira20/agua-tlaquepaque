"use client";
import type { SupuestosMotor } from "@/lib/motor";

export function Deslizador({ label, value, min, max, step = 1, unidad = "", onChange }: { label: string; value: number; min: number; max: number; step?: number; unidad?: string; onChange: (v: number) => void }) {
  return (
    <label className="block text-sm">
      <span className="flex justify-between text-tinta"><span>{label}</span><b className="tabular-nums">{value}{unidad}</b></span>
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
