// Motor oficial de autonomía. Implementa motor/ESPECIFICACION.md (v0.3).
// No importa nada para poder probarse con Node directamente (scripts/verifica-vectores.ts).

export type SupuestosMotor = {
  consumo_l_persona_dia: number;
  tinaco_l: number;
  cisterna_l: number;
  horas_efectivas_corte: number;
  fraccion_suministro_en_racionamiento: number;
  u_horas_agua_guardada: number;
  umbral_estado_parcial_pct: number;
  umbral_estado_mayoritario_pct: number;
};

export const SUPUESTOS_BASE: SupuestosMotor = {
  consumo_l_persona_dia: 50, tinaco_l: 1100, cisterna_l: 5000, horas_efectivas_corte: 24,
  fraccion_suministro_en_racionamiento: 0, u_horas_agua_guardada: 48,
  umbral_estado_parcial_pct: 10, umbral_estado_mayoritario_pct: 50,
};

export type Esquema = Record<string, string[]>; // zona -> días de la semana con racionamiento
export type EntradaManzana = { viviendas: number; viv_tinaco: number; viv_cisterna: number; ocupantes_prom: number; zona: string };
export type Estado = "con_agua" | "quiebre_parcial" | "quiebre_mayoritario";
export type Salida = {
  horas_sin_servicio_min: number; horas_sin_servicio_max: number;
  viv_sin_agua_min: number; viv_sin_agua_max: number;
  viv_agua_guardada_min: number; viv_agua_guardada_max: number;
  requiere_desinfeccion: boolean; estado: Estado; pct_min: number; pct_max: number;
};

export const DIAS = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

/** Día de la semana de una fecha ISO (AAAA-MM-DD), sin depender de la zona horaria. */
export function diaSemana(fecha: string): string {
  const [y, m, d] = fecha.split("-").map(Number);
  return DIAS[new Date(Date.UTC(y, m - 1, d)).getUTCDay()];
}

function restarDia(fecha: string): string {
  const [y, m, d] = fecha.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d - 1)).toISOString().slice(0, 10);
}

/** Sección 4. */
export function horasSinServicio(diasZona: string[], fecha: string, he: number): number {
  let n = 0;
  let f = fecha;
  while (diasZona.includes(diaSemana(f))) {
    n++;
    f = restarDia(f);
    if (n > 7) throw new Error("zona con racionamiento los 7 dias: no soportada");
  }
  return n === 0 ? 0 : he + (n - 1) * 24;
}

/** Sección 5. Misma expresión que la referencia para obtener el mismo redondeo de punto flotante. */
export function autonomiaH(litros: number, ocupantes: number, consumo: number, f = 0): number {
  if (!(f >= 0 && f < 1)) throw new Error("fraccion_suministro_en_racionamiento debe estar en [0, 1)");
  if (litros <= 0) return 0;
  return (litros / (ocupantes * consumo * (1 - f))) * 24;
}

export function parsearZonas(z: string): string[] {
  return String(z ?? "").split(",").map((s) => s.trim()).filter(Boolean);
}

export function horasDeZonas(zonas: string[], esquema: Esquema, fecha: string, he: number): number[] {
  if (!zonas.length) return [0];
  return zonas.map((z) => {
    if (!(z in esquema)) throw new Error(`zona ${z} no esta en el calendario`);
    return horasSinServicio(esquema[z], fecha, he);
  });
}

/** Secciones 3, 5 y 6 para una manzana y una lista de H (una por zona). */
export function calcularManzana(m: EntradaManzana, horas: number[], s: SupuestosMotor): Salida {
  const V = Math.round(m.viviendas);
  const T = Math.min(Math.round(m.viv_tinaco || 0), V);
  const C = Math.min(Math.round(m.viv_cisterna || 0), V);
  const o = m.ocupantes_prom, c = s.consumo_l_persona_dia, f = s.fraccion_suministro_en_racionamiento, U = s.u_horas_agua_guardada;
  const aut = {
    ambos: autonomiaH(s.tinaco_l + s.cisterna_l, o, c, f),
    solo_t: autonomiaH(s.tinaco_l, o, c, f),
    solo_c: autonomiaH(s.cisterna_l, o, c, f),
    ninguno: 0,
  };
  const aMin = Math.max(0, T + C - V), aMax = Math.min(T, C);
  const sin: number[] = [], guard: number[] = [];
  for (const H of horas) {
    for (const a of [aMin, aMax]) {
      const e = { ambos: a, solo_t: T - a, solo_c: C - a, ninguno: V - T - C + a };
      let si = 0, gu = 0;
      for (const k of ["ambos", "solo_t", "solo_c", "ninguno"] as const) {
        if (aut[k] < H) si += e[k];
        else if (k !== "ninguno" && H > U) gu += e[k];
      }
      sin.push(si); guard.push(gu);
    }
  }
  const smin = Math.min(...sin), smax = Math.max(...sin);
  const pmin = V > 0 ? (100 * smin) / V : 0;
  const estado: Estado = pmin < s.umbral_estado_parcial_pct ? "con_agua" : pmin <= s.umbral_estado_mayoritario_pct ? "quiebre_parcial" : "quiebre_mayoritario";
  return {
    horas_sin_servicio_min: Math.min(...horas), horas_sin_servicio_max: Math.max(...horas),
    viv_sin_agua_min: smin, viv_sin_agua_max: smax,
    viv_agua_guardada_min: Math.min(...guard), viv_agua_guardada_max: Math.max(...guard),
    requiere_desinfeccion: Math.max(...guard) > 0, estado, pct_min: pmin, pct_max: V > 0 ? (100 * smax) / V : 0,
  };
}

/** Atajo: una manzana en una fecha. */
export function evaluarManzana(m: EntradaManzana, esquema: Esquema, fecha: string, s: SupuestosMotor): Salida {
  return calcularManzana(m, horasDeZonas(parsearZonas(m.zona), esquema, fecha, s.horas_efectivas_corte), s);
}
