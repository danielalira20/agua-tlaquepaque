// Motor simplificado para la demo. Replica la lógica del carril de Dani:
// la autonomía se calcula POR ESTRATO de vivienda, nunca promediando la colonia.

export type Colonia = {
  id: string; nombre: string; zona: number; h3: string; lat: number; lng: number;
  manzanas: number; viviendas: number; pob: number; ocupantes_prom: number;
  viv_sin_almacen: number; viv_tinaco: number; viv_cisterna: number;
  marginacion: number; simulado: string;
};
export type Cisterna = { id: string; colonia_id: string; lat: number; lng: number };
export type DiaCal = { fecha: string; dia: string; zonas_sin_servicio: number[] };
export type Calendario = { version: string; consultado: string; esquema: Record<string, string[]>; dias: DiaCal[] };

export type Supuestos = {
  consumo: number;        // L por persona al día (50 OMS básico / 100 / 150)
  tinaco: number;         // L
  cisterna: number;       // L
  horasEfectivas: number; // horas que dura un día de corte en la llave (24..48)
  U: number;              // horas a partir de las cuales el agua guardada se marca
};
export const SUPUESTOS: Supuestos = { consumo: 50, tinaco: 1100, cisterna: 5000, horasEfectivas: 24, U: 48 };

export type Estrato = { nombre: string; viviendas: number; autonomia_h: number; seca: boolean; guardada: boolean };
export type Estado = {
  colonia: Colonia; fecha: string; horas_sin_servicio: number;
  estratos: Estrato[]; viv_sin_agua: number; pct_sin_agua: number; personas_sin_agua: number;
  viv_agua_guardada: number; severidad: number;
};

/** Horas acumuladas sin servicio en una zona hasta el final de `fecha`. */
export function horasSinServicio(cal: Calendario, zona: number, fecha: string, horasEfectivas: number) {
  const i = cal.dias.findIndex((d) => d.fecha === fecha);
  if (i < 0) return 0;
  let dias = 0;
  for (let j = i; j >= 0 && cal.dias[j].zonas_sin_servicio.includes(zona); j--) dias++;
  return dias === 0 ? 0 : horasEfectivas + (dias - 1) * 24;
}

export function autonomiaHoras(litros: number, ocupantes: number, consumo: number) {
  return (litros / (ocupantes * consumo)) * 24;
}

export function estadoColonia(c: Colonia, cal: Calendario, fecha: string, s: Supuestos = SUPUESTOS): Estado {
  const h = horasSinServicio(cal, c.zona, fecha, s.horasEfectivas);
  const mk = (nombre: string, viviendas: number, litros: number): Estrato => {
    const a = litros === 0 ? 0 : autonomiaHoras(litros, c.ocupantes_prom, s.consumo);
    return { nombre, viviendas, autonomia_h: a, seca: h > a, guardada: h > 0 && h <= a && h > s.U };
  };
  const estratos = [
    mk("Sin almacenamiento", c.viv_sin_almacen, 0),
    mk("Con tinaco", c.viv_tinaco, s.tinaco),
    mk("Con cisterna", c.viv_cisterna, s.cisterna),
  ];
  const viv_sin_agua = estratos.filter((e) => e.seca).reduce((n, e) => n + e.viviendas, 0);
  const viv_agua_guardada = estratos.filter((e) => e.guardada).reduce((n, e) => n + e.viviendas, 0);
  const pct = c.viviendas ? viv_sin_agua / c.viviendas : 0;
  return {
    colonia: c, fecha, horas_sin_servicio: h, estratos, viv_sin_agua, pct_sin_agua: pct,
    personas_sin_agua: Math.round(pct * c.pob), viv_agua_guardada,
    severidad: pct * (0.5 + 0.5 * c.marginacion),
  };
}

/** Priorizador glotón: reparte los viajes del día a las colonias con más personas sin agua, ponderado por marginación. */
export function priorizar(estados: Estado[], viajesDia = 63, litrosViaje = 10000, litrosHogar = 200) {
  const hogaresViaje = Math.floor(litrosViaje / litrosHogar);
  const orden = [...estados].filter((e) => e.viv_sin_agua > 0).sort((a, b) => b.severidad * b.colonia.pob - a.severidad * a.colonia.pob);
  const plan: { estado: Estado; viajes: number; viviendas_objetivo: number; litros: number; score: number }[] = [];
  let restan = viajesDia;
  for (const e of orden) {
    if (restan <= 0) break;
    const viajes = Math.min(restan, Math.ceil(e.viv_sin_agua / hogaresViaje));
    restan -= viajes;
    plan.push({ estado: e, viajes, viviendas_objetivo: Math.min(e.viv_sin_agua, viajes * hogaresViaje), litros: viajes * litrosViaje, score: e.severidad * e.colonia.pob });
  }
  const personasAtendidas = plan.reduce((n, p) => n + Math.round(p.viviendas_objetivo * p.estado.colonia.ocupantes_prom), 0);
  return { plan, viajesUsados: viajesDia - restan, personasAtendidas };
}

export function resumenDia(estados: Estado[]) {
  const viv = estados.reduce((n, e) => n + e.colonia.viviendas, 0);
  const sin = estados.reduce((n, e) => n + e.viv_sin_agua, 0);
  return {
    pct_viv_sin_agua: viv ? sin / viv : 0,
    personas_sin_agua: estados.reduce((n, e) => n + e.personas_sin_agua, 0),
    colonias_afectadas: estados.filter((e) => e.viv_sin_agua > 0).length,
    viv_agua_guardada: estados.reduce((n, e) => n + e.viv_agua_guardada, 0),
  };
}

export const fmt = (n: number) => n.toLocaleString("es-MX");
export const pct = (x: number) => `${(x * 100).toFixed(1)} %`;
export const fechaLarga = (f: string) => new Date(f + "T12:00:00").toLocaleDateString("es-MX", { weekday: "long", day: "numeric", month: "short" });
