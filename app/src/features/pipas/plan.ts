// Lectura del plan.json precalculado por el priorizador (contrato plan v2). La app no recalcula el plan.
export type Cota = "min" | "max";
export type Viaje = {
  orden_eleccion: number; colonia: string; lon: number; lat: number;
  manzanas_cubiertas: { cvegeo: string; viviendas: number }[]; viviendas_objetivo: number; personas_beneficiadas: number;
};
export type ResumenDia = { necesidad_total: number; viviendas_atendidas: number; personas_atendidas: number; viajes_usados: number; cobertura_pct: number };
export type Parada = { n: number; colonia: string; viajes: number; viv: number; pers: number; lon: number; lat: number };

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Plan = any;

export const corrida = (plan: Plan, regla: "priorizado" | "baseline", cota: Cota) =>
  plan.corridas.find((c: Plan) => c.regla === regla && c.cota_para_ordenar === cota);

export const diaDe = (plan: Plan, regla: "priorizado" | "baseline", cota: Cota, fecha: string) =>
  corrida(plan, regla, cota)?.fechas.find((x: Plan) => x.fecha === fecha) as { fecha: string; viajes: Viaje[]; resumen: ResumenDia } | undefined;

export const semanaDe = (plan: Plan, cota: Cota) => plan.comparacion.find((x: Plan) => x.cota_para_ordenar === cota).semana;

/** Viajes agrupados por colonia, en el orden en que el priorizador las eligió (no es una ruta). */
export function paradas(viajes: Viaje[]): Parada[] {
  const m = new Map<string, Parada & { primero: number }>();
  for (const v of viajes) {
    const k = v.colonia || "sin colonia";
    const x = m.get(k) ?? { n: 0, colonia: k, viajes: 0, viv: 0, pers: 0, primero: v.orden_eleccion, lon: v.lon, lat: v.lat };
    x.viajes++; x.viv += v.viviendas_objetivo; x.pers += v.personas_beneficiadas;
    if (v.orden_eleccion < x.primero) { x.primero = v.orden_eleccion; x.lon = v.lon; x.lat = v.lat; }
    m.set(k, x);
  }
  return [...m.values()].sort((a, b) => a.primero - b.primero).map((x, i) => ({ n: i + 1, colonia: x.colonia, viajes: x.viajes, viv: x.viv, pers: x.pers, lon: x.lon, lat: x.lat }));
}
