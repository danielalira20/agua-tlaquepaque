"use client";
// Datos reales (app/public/datos/real/, exportados por scripts/exporta_app.py) + motor oficial en el navegador.
// Python exporta los datos; aquí solo se recalcula lo interactivo (consumo, f, horas de corte, calendario).
import { useEffect, useState } from "react";
import { latLngToCell } from "h3-js";
import { evaluarManzana, type Esquema, type SupuestosMotor } from "./motor";

export type Manzana = {
  cvegeo: string; colonia: string; geocol: string; zona: string; zona_confianza: string; en_programa: boolean;
  lon: number | null; lat: number | null; viviendas: number; pob: number; ocupantes_prom: number;
  viv_tinaco: number; viv_cisterna: number; sin_almacen_min: number; sin_almacen_max: number; grado_marginacion: string; nucleo_robusto?: boolean;
};
export type DiaCal = { fecha: string; dia: string; zonas_sin_servicio: (string | number)[] };
export type Calendario = { version: string; vigente_desde: string; vigente_hasta: string | null; consultado: string; esquema: Esquema; dias: DiaCal[]; nota_vigencia?: string };
export type Cisterna = { id: string; tipo: string; colonia: string; ubicacion: string; lon: number | null; lat: number | null; cuenta_como_cobertura: boolean };
export type Meta = { ventana: { desde: string; hasta: string }; calendario_usado: string; supuestos: SupuestosMotor; conteos: Record<string, number>; fuentes: string[]; advertencias: string[] };
export type Datos = { manzanas: Manzana[]; calendarios: Record<string, Calendario>; cisternas: Cisterna[]; meta: Meta; plan: any };

let cache: Datos | null = null;
let promesa: Promise<Datos> | null = null;
const cargar = () =>
  (promesa ??= Promise.all(["manzanas", "calendarios", "cisternas", "meta", "plan"].map((f) => fetch(`/datos/real/${f}.json`).then((r) => r.json()))).then(
    ([manzanas, calendarios, cisternas, meta, plan]) => (cache = { manzanas, calendarios, cisternas, meta, plan })
  ));

export function useReal() {
  const [d, setD] = useState<Datos | null>(cache);
  useEffect(() => { if (!cache) cargar().then(setD); }, []);
  return d;
}

/** Rango "a – b"; si son iguales, igual se marca como cota. */
export const rango = (a: number, b: number, dec = 0) => {
  const f = (x: number) => x.toLocaleString("es-MX", { maximumFractionDigits: dec, minimumFractionDigits: dec });
  return a === b ? `${f(a)} (mín = máx)` : `${f(a)} – ${f(b)}`;
};
export const fmt = (n: number) => Math.round(n).toLocaleString("es-MX");
export const fechaLarga = (f: string) => new Date(f + "T12:00:00").toLocaleDateString("es-MX", { weekday: "long", day: "numeric", month: "short" });

export type Celda = {
  h3: string; manzanas: number[]; viviendas: number; pob: number;
  sin_min: number; sin_max: number; pers_min: number; pers_max: number; guard_max: number;
  pct_min: number; pct_max: number; colonias: string[]; zonas: string[]; marg: string; en_programa: boolean; nucleo: number;
};

export type Resumen = { viv: number; pob: number; sin_min: number; sin_max: number; pers_min: number; pers_max: number; guard_min: number; guard_max: number; mzas_quiebre: number };

/** Corre el motor para una fecha sobre todas las manzanas y agrupa en hexágonos H3. */
export function calcular(d: Datos, cal: Calendario, fecha: string, s: SupuestosMotor, resH3 = 8) {
  const celdas = new Map<string, Celda>();
  const r: Resumen = { viv: 0, pob: 0, sin_min: 0, sin_max: 0, pers_min: 0, pers_max: 0, guard_min: 0, guard_max: 0, mzas_quiebre: 0 };
  const porManzana = d.manzanas.map((m, i) => {
    if (!(m.viviendas > 0)) return null;
    const o = evaluarManzana(m, cal.esquema, fecha, s);
    r.viv += m.viviendas; r.pob += m.pob;
    r.sin_min += o.viv_sin_agua_min; r.sin_max += o.viv_sin_agua_max;
    r.pers_min += o.viv_sin_agua_min * m.ocupantes_prom; r.pers_max += o.viv_sin_agua_max * m.ocupantes_prom;
    r.guard_min += o.viv_agua_guardada_min; r.guard_max += o.viv_agua_guardada_max;
    if (o.estado !== "con_agua") r.mzas_quiebre++;
    if (m.lat != null && m.lon != null) {
      const h = latLngToCell(m.lat, m.lon, resH3);
      let c = celdas.get(h);
      if (!c) celdas.set(h, (c = { h3: h, manzanas: [], viviendas: 0, pob: 0, sin_min: 0, sin_max: 0, pers_min: 0, pers_max: 0, guard_max: 0, pct_min: 0, pct_max: 0, colonias: [], zonas: [], marg: "", en_programa: false, nucleo: 0 }));
      c.manzanas.push(i); c.viviendas += m.viviendas; c.pob += m.pob;
      c.sin_min += o.viv_sin_agua_min; c.sin_max += o.viv_sin_agua_max;
      c.pers_min += o.viv_sin_agua_min * m.ocupantes_prom; c.pers_max += o.viv_sin_agua_max * m.ocupantes_prom;
      c.guard_max += o.viv_agua_guardada_max;
      if (m.colonia && !c.colonias.includes(m.colonia)) c.colonias.push(m.colonia);
      for (const z of m.zona.split(",").filter(Boolean)) if (!c.zonas.includes(z)) c.zonas.push(z);
      c.en_programa ||= m.en_programa;
      if (m.nucleo_robusto) c.nucleo++;
    }
    return o;
  });
  const grados = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo"];
  for (const c of celdas.values()) {
    c.pct_min = c.viviendas ? c.sin_min / c.viviendas : 0;
    c.pct_max = c.viviendas ? c.sin_max / c.viviendas : 0;
    c.zonas.sort();
    // grado de marginación dominante por viviendas (capa aparte, no entra en la severidad)
    const cuenta: Record<string, number> = {};
    for (const i of c.manzanas) { const g = d.manzanas[i].grado_marginacion; cuenta[g] = (cuenta[g] ?? 0) + d.manzanas[i].viviendas; }
    c.marg = grados.concat("sin dato").sort((a, b) => (cuenta[b] ?? 0) - (cuenta[a] ?? 0))[0];
  }
  return { celdas: [...celdas.values()], resumen: r, porManzana };
}

/** Personas-día sin agua en una ventana de fechas (cotas). */
export function personasDia(d: Datos, cal: Calendario, s: SupuestosMotor, fechas = cal.dias.map((x) => x.fecha)) {
  let min = 0, max = 0;
  for (const f of fechas) for (const m of d.manzanas) {
    if (!(m.viviendas > 0)) continue;
    const o = evaluarManzana(m, cal.esquema, f, s);
    min += o.viv_sin_agua_min * m.ocupantes_prom; max += o.viv_sin_agua_max * m.ocupantes_prom;
  }
  return { min, max };
}
