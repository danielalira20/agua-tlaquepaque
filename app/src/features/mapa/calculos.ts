// Agregados que solo necesita la pantalla del mapa. El cálculo por manzana es el del motor oficial.
import type { Calendario, Datos } from "@/lib/real";
import { evaluarManzana, type SupuestosMotor } from "@/lib/motor";
import type { DiaGota } from "@/ui";

/** Nivel de cada gota de la semana, relativo a la propia semana: la gota más llena es el mejor día y la más
 *  vacía el peor (viviendas sin agua, cota mínima). El número exacto va en el título de cada gota. */
export function nivelesSemana(d: Datos, cal: Calendario, s: SupuestosMotor): DiaGota[] {
  const sin = cal.dias.map((x) => {
    let n = 0;
    for (const m of d.manzanas) if (m.viviendas > 0) n += evaluarManzana(m, cal.esquema, x.fecha, s).viv_sin_agua_min;
    return n;
  });
  const lo = Math.min(...sin), hi = Math.max(...sin);
  return cal.dias.map((x, i) => ({
    fecha: x.fecha, dia: x.dia, nivel: hi > lo ? 0.85 - 0.55 * ((sin[i] - lo) / (hi - lo)) : 0.85,
    nota: `${Math.round(sin[i]).toLocaleString("es-MX")} viviendas sin agua como mínimo · racionamiento en zonas ${x.zonas_sin_servicio.join(", ") || "ninguna"}`,
  }));
}

/** Parte del riesgo de almacenamiento que está en las zonas 5 y 6 (dentro del programa), con las dos cotas. */
export function riesgoZonas56(d: Datos) {
  let t0 = 0, t1 = 0, a = 0, b = 0;
  for (const m of d.manzanas) {
    if (!m.en_programa || !(m.viviendas > 0)) continue;
    const z = m.zona.split(",").filter(Boolean);
    t0 += m.sin_almacen_min; t1 += m.sin_almacen_max;
    if (z.every((x) => x === "5" || x === "6")) { a += m.sin_almacen_min; b += m.sin_almacen_max; }
  }
  return { min: (100 * a) / t0, max: (100 * b) / t1 };
}
