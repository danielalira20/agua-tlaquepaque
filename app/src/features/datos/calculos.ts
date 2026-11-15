// Cómo funciona: las mismas cuentas de siempre (motor oficial en el navegador), fuera de la pantalla.
import type { Calendario, Datos } from "@/lib/real";
import { evaluarManzana, parsearZonas, type SupuestosMotor } from "@/lib/motor";

export const GRADOS = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo", "sin dato"];
export type Rango = [number, number];

/** Cede el hilo al navegador para que pinte y responda entre un cálculo pesado y otro. */
const pausa = () => new Promise<void>((r) => setTimeout(r, 0));

/** Personas-día sin agua en la semana (cotas), igual que `personasDia` de lib/real pero solo sobre manzanas con zona. */
function personasDiaZona(manzanas: Datos["manzanas"], cal: Calendario, ss: SupuestosMotor) {
  let min = 0, max = 0;
  for (const x of cal.dias) for (const m of manzanas) {
    const o = evaluarManzana(m, cal.esquema, x.fecha, ss);
    min += o.viv_sin_agua_min * m.ocupantes_prom; max += o.viv_sin_agua_max * m.ocupantes_prom;
  }
  return { min, max };
}
const conZona = (d: Datos) => d.manzanas.filter((m) => m.viviendas > 0 && parsearZonas(m.zona).length > 0);

/**
 * Esta pantalla corre el motor unas 20 veces sobre todas las manzanas. Para que la app no se congele:
 * (1) se calcula por partes, cediendo el hilo entre una y otra, y (2) solo se recorren las manzanas con
 * zona de racionamiento: sin zona no hay corte, así que no pueden sumar personas sin agua.
 */
export async function calcularDatos(d: Datos) {
  const s = d.meta.supuestos, cv = d.calendarios.vigente, co = d.calendarios.original;
  const mz = d.manzanas.filter((m) => m.viviendas > 0);
  const mzZona = mz.filter((m) => parsearZonas(m.zona).length > 0);

  // 1. personas sin agua por día, vigente vs original, con cotas
  const porDia: Record<string, any>[] = [];
  for (const x of cv.dias) {
    const fila: Record<string, any> = { dia: `${x.dia.slice(0, 3)} ${x.fecha.slice(8)}` };
    for (const [nom, cal] of [["vigente", cv], ["original", co]] as const) {
      let a = 0, b = 0;
      for (const m of mzZona) { const o = evaluarManzana(m, cal.esquema, x.fecha, s); a += o.viv_sin_agua_min * m.ocupantes_prom; b += o.viv_sin_agua_max * m.ocupantes_prom; }
      fila[nom] = [Math.round(a), Math.round(b)];
    }
    porDia.push(fila);
    await pausa();
  }
  const sem = { vig: personasDiaZona(mzZona, cv, s), ori: personasDiaZona(mzZona, co, s) };
  await pausa();

  // 3. dónde está el riesgo: viviendas sin almacenamiento por zona (solo dentro del programa)
  const zonas: Record<string, { min: number; max: number }> = {};
  for (const m of mz) { if (!m.en_programa) continue; const z = parsearZonas(m.zona).join(" y ") || "?"; zonas[z] ??= { min: 0, max: 0 }; zonas[z].min += m.sin_almacen_min; zonas[z].max += m.sin_almacen_max; }
  const porZona = Object.entries(zonas).sort((a, b) => b[1].min - a[1].min).map(([z, v]) => ({ zona: `Zona ${z}`, minimo: v.min, rango: v.max - v.min }));

  // 4. equidad: por grado de marginación (capa aparte)
  const eq: { gr: string; viv: number; pob: number; smin: number; smax: number; pmin: number; pmax: number }[] = [];
  for (const gr of GRADOS) {
    const ms = mz.filter((m) => m.grado_marginacion === gr);
    let pmin = 0, pmax = 0;
    for (const x of cv.dias) for (const m of ms) {
      if (!parsearZonas(m.zona).length) continue;
      const o = evaluarManzana(m, cv.esquema, x.fecha, s); pmin += o.viv_sin_agua_min * m.ocupantes_prom; pmax += o.viv_sin_agua_max * m.ocupantes_prom;
    }
    eq.push({ gr, viv: ms.reduce((n, m) => n + m.viviendas, 0), pob: ms.reduce((n, m) => n + m.pob, 0), smin: ms.reduce((n, m) => n + m.sin_almacen_min, 0), smax: ms.reduce((n, m) => n + m.sin_almacen_max, 0), pmin, pmax });
    await pausa();
  }

  // 5. colonias con más viviendas sin almacenamiento
  const col: Record<string, { viv: number; pob: number; min: number; max: number; zonas: Set<string> }> = {};
  for (const m of mz) { if (!m.colonia) continue; const c = (col[m.colonia] ??= { viv: 0, pob: 0, min: 0, max: 0, zonas: new Set() }); c.viv += m.viviendas; c.pob += m.pob; c.min += m.sin_almacen_min; c.max += m.sin_almacen_max; parsearZonas(m.zona).forEach((z) => c.zonas.add(z)); }
  const top = Object.entries(col).sort((a, b) => b[1].min - a[1].min).slice(0, 12);

  const tot = mz.reduce((a, m) => ({ viv: a.viv + m.viviendas, min: a.min + m.sin_almacen_min, max: a.max + m.sin_almacen_max, tin: a.tin + m.viv_tinaco, cis: a.cis + m.viv_cisterna }), { viv: 0, min: 0, max: 0, tin: 0, cis: 0 });
  // solo dentro del programa (la cota se compara con ese total)
  const enPrograma = porZona.reduce((a, z) => ({ min: a.min + z.minimo, max: a.max + z.minimo + z.rango }), { min: 0, max: 0 });
  const z56 = porZona.filter((z) => ["Zona 5", "Zona 6", "Zona 5 y 6"].includes(z.zona)).reduce((a, z) => ({ min: a.min + z.minimo, max: a.max + z.minimo + z.rango }), { min: 0, max: 0 });
  const peso56 = { min: (100 * z56.min) / enPrograma.min, max: (100 * z56.max) / enPrograma.max };
  return { porDia, sem, porZona, eq, top, tot, enPrograma, peso56 };
}
/** Sensibilidad: consumo × f (personas-día de la semana, cotas). Es lo más pesado, por eso se pide solo cuando la gráfica se ve. */
export async function calcularSensibilidad(d: Datos) {
  const s = d.meta.supuestos, cv = d.calendarios.vigente, mzZona = conZona(d);
  const sens: Record<string, any>[] = [];
  for (const c of [50, 75, 100, 125, 150]) {
    const fila: Record<string, any> = { consumo: `${c} L` };
    for (const f of [0, 0.25, 0.5]) { const r = personasDiaZona(mzZona, cv, { ...s, consumo_l_persona_dia: c, fraccion_suministro_en_racionamiento: f }); fila[`f${f}`] = Math.round(r.min); fila[`f${f}max`] = Math.round(r.max); await pausa(); }
    sens.push(fila);
  }
  return sens;
}
export type Sensibilidad = Awaited<ReturnType<typeof calcularSensibilidad>>;
const sensHecha = new WeakMap<Datos, Promise<Sensibilidad>>();
export const sensibilidadCalculada = (d: Datos) => { let p = sensHecha.get(d); if (!p) { p = calcularSensibilidad(d); sensHecha.set(d, p); } return p; };

export type DatosCalculados = Awaited<ReturnType<typeof calcularDatos>>;

// Se calcula una sola vez por carga de datos: al volver a esta pantalla es instantáneo.
const hechos = new WeakMap<Datos, DatosCalculados>();
const enCurso = new WeakMap<Datos, Promise<DatosCalculados>>();
export const datosCalculadosYa = (d: Datos) => hechos.get(d) ?? null;
export function datosCalculados(d: Datos): Promise<DatosCalculados> {
  let p = enCurso.get(d);
  if (!p) { p = calcularDatos(d).then((r) => { hechos.set(d, r); return r; }); enCurso.set(d, p); }
  return p;
}
