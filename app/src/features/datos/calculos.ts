// Cómo funciona: las mismas cuentas de siempre (motor oficial en el navegador), fuera de la pantalla.
import { personasDia, type Datos } from "@/lib/real";
import { evaluarManzana, parsearZonas } from "@/lib/motor";

export const GRADOS = ["Muy alto", "Alto", "Medio", "Bajo", "Muy bajo", "sin dato"];
export type Rango = [number, number];

export function calcularDatos(d: Datos) {
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
  // solo dentro del programa (la cota se compara con ese total)
  const enPrograma = porZona.reduce((a, z) => ({ min: a.min + z.minimo, max: a.max + z.minimo + z.rango }), { min: 0, max: 0 });
  const z56 = porZona.filter((z) => ["Zona 5", "Zona 6", "Zona 5 y 6"].includes(z.zona)).reduce((a, z) => ({ min: a.min + z.minimo, max: a.max + z.minimo + z.rango }), { min: 0, max: 0 });
  const peso56 = { min: (100 * z56.min) / enPrograma.min, max: (100 * z56.max) / enPrograma.max };
  return { porDia, sem, sens, porZona, eq, top, tot, enPrograma, peso56 };
}
export type DatosCalculados = ReturnType<typeof calcularDatos>;
