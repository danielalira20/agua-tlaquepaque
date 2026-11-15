// Mi casa: la misma cuenta de siempre (motor oficial), ahora fuera de la pantalla.
import { autonomiaH, horasDeZonas, parsearZonas } from "@/lib/motor";
import type { Datos } from "@/lib/real";

export type Almacen = "ninguno" | "tinaco" | "cisterna" | "ambos";
export type Colonia = { nombre: string; zonas: string[] };
export type DiaCasa = { fecha: string; dia: string; H: number; corte: boolean; seca: boolean };
export type ResultadoCasa = {
  col: Colonia; fuera: boolean;
  /** horas que aguanta la reserva */
  aut: number;
  semana: DiaCasa[];
  /** cisternas comunitarias de la colonia que cuentan como cobertura */
  cis: number;
  primera?: DiaCasa;
  /** horas del corte más largo de la semana */
  peor: number;
  /** 0–1: qué parte del corte más largo cubre la reserva */
  nivel: number;
};

export const ETIQUETA_ALMACEN: Record<Almacen, string> = {
  ninguno: "Sin tinaco ni cisterna", tinaco: "Tinaco", cisterna: "Cisterna", ambos: "Tinaco y cisterna",
};

export const normaliza = (s: string) => s.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase().trim();

/** Colonias con sus zonas de racionamiento (vacío = fuera del programa), en orden alfabético. */
export function coloniasDe(d: Datos): Colonia[] {
  const m = new Map<string, Set<string>>();
  for (const x of d.manzanas) {
    if (!x.colonia) continue;
    if (!m.has(x.colonia)) m.set(x.colonia, new Set());
    parsearZonas(x.zona).forEach((z) => m.get(x.colonia)!.add(z));
  }
  return [...m.entries()].map(([nombre, z]) => ({ nombre, zonas: [...z].sort() })).sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
}

export function litrosDe(d: Datos, alm: Almacen) {
  const s = d.meta.supuestos;
  return { ninguno: 0, tinaco: s.tinaco_l, cisterna: s.cisterna_l, ambos: s.tinaco_l + s.cisterna_l }[alm];
}

export function resultadoCasa(d: Datos, col: Colonia, alm: Almacen, personas: number, consumo: number): ResultadoCasa {
  const s = d.meta.supuestos, cal = d.calendarios.vigente;
  const aut = autonomiaH(litrosDe(d, alm), personas, consumo, 0);
  // si la colonia abarca varias zonas, se toma el peor caso por día (cota alta)
  const semana = cal.dias.map((x) => {
    const H = Math.max(...horasDeZonas(col.zonas, cal.esquema, x.fecha, s.horas_efectivas_corte));
    return { ...x, H, corte: H > 0, seca: aut < H };
  });
  const cis = d.cisternas.filter((c) => c.colonia === col.nombre && c.tipo !== "propuesta_municipio" && c.cuenta_como_cobertura).length;
  const peor = Math.max(0, ...semana.map((x) => x.H));
  return { col, fuera: col.zonas.length === 0, aut, semana, cis, primera: semana.find((x) => x.seca), peor, nivel: peor <= 0 ? 1 : Math.min(1, aut / peor) };
}

/** "132 horas" o "5.5 días", como siempre. */
export const textoReserva = (aut: number) => (aut < 48 ? `${aut.toFixed(0)} horas` : `${(aut / 24).toFixed(1)} días`);
