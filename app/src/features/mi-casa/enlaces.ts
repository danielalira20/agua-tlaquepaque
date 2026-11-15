import type { ResultadoCasa } from "./calculos";

/**
 * WhatsApp de TlaqueChat, el canal del ayuntamiento de Tlaquepaque para pedir pipas.
 * El número y el horario salen de la prensa (Crónica, 14 y 15 de octubre de 2026); falta confirmarlos en el sitio oficial.
 * `telefono` va con lada de país y sin espacios, que es lo que pide wa.me.
 */
export const TLAQUECHAT = { telefono: "523328048171", visible: "33 2804 8171", horario: "de 7:00 a 22:00" } as const;

/** Enlace que abre WhatsApp con el texto ya escrito. Sin teléfono, la persona elige a quién mandarlo. */
export const enlaceWhatsApp = (texto: string, telefono?: string) => `https://wa.me/${telefono ?? ""}?text=${encodeURIComponent(texto)}`;

const diaSemana = (fecha: string) => new Date(fecha + "T12:00:00").toLocaleDateString("es-MX", { weekday: "long" });

const lista = (a: string[]) => (a.length <= 1 ? a.join("") : `${a.slice(0, -1).join(", ")} y ${a[a.length - 1]}`);

/** Días de la semana (sin fecha) en que la reserva no alcanza. El calendario se repite cada semana, así que no dependen de la fecha de hoy. */
export function diasSinAgua(r: ResultadoCasa): string[] {
  return [...new Set(r.semana.filter((x) => x.seca).map((x) => diaSemana(x.fecha)))];
}

/** Mensaje para TlaqueChat. TlaqueChat pide colonia y municipio; la calle y el número los escribe la persona. */
export function mensajePipa(r: ResultadoCasa, personas: number) {
  const dias = diasSinAgua(r);
  return [
    "Hola, necesito una pipa de agua.",
    `Colonia: ${r.col.nombre}, San Pedro Tlaquepaque.`,
    "Calle y número: ",
    `Personas en la casa: ${personas}.`,
    ...(dias.length ? [`Según el calendario del SIAPA, nos quedamos sin agua los días: ${lista(dias)}.`] : []),
  ].join("\n");
}

/** Mensaje para mandar a los vecinos. Solo dice lo que la app calculó; no promete nada. */
export function mensajeCompartir(r: ResultadoCasa, url: string) {
  const dias = diasSinAgua(r);
  return [
    dias.length
      ? `En ${r.col.nombre} el calendario del SIAPA nos deja sin agua los días: ${lista(dias)}, si no se tiene reserva suficiente.`
      : `Revisé cuánto aguanta una casa en ${r.col.nombre} cuando el SIAPA corta el agua.`,
    `Calcula cuánto aguanta la tuya: ${url}`,
  ].join("\n");
}

const dos = (n: number) => String(n).padStart(2, "0");
const marca = (f: Date) => `${f.getFullYear()}${dos(f.getMonth() + 1)}${dos(f.getDate())}T${dos(f.getHours())}${dos(f.getMinutes())}00`;
const marcaUTC = (f: Date) => `${f.getUTCFullYear()}${dos(f.getUTCMonth() + 1)}${dos(f.getUTCDate())}T${dos(f.getUTCHours())}${dos(f.getUTCMinutes())}${dos(f.getUTCSeconds())}Z`;
const texto = (s: string) => s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n");

/** Pliega las líneas a 75 caracteres, como pide el formato iCalendar. */
function plegar(linea: string) {
  const partes: string[] = [];
  let resto = linea;
  while (resto.length > 75) { partes.push(resto.slice(0, 75)); resto = " " + resto.slice(75); }
  partes.push(resto);
  return partes.join("\r\n");
}

/**
 * Recordatorio de calendario (.ics) para llenar tinaco y cubetas la noche anterior a cada día sin agua.
 * Se repite 4 semanas porque el calendario del SIAPA se repite cada semana, pero puede cambiar: el texto lo dice.
 * Las horas son locales (sin zona), así que suenan a las 19:00 de quien lo importe. Devuelve null si la reserva alcanza toda la semana.
 */
export function recordatorioICS(r: ResultadoCasa, consultado: string, ahora: Date = new Date()): string | null {
  const dias = r.semana.filter((x) => x.seca);
  if (!dias.length) return null;
  const vistos = new Set<number>();
  const eventos: string[] = [];
  for (const x of dias) {
    const dow = new Date(x.fecha + "T12:00:00").getDay();
    if (vistos.has(dow)) continue;
    vistos.add(dow);
    // primer aviso que todavía no pasó: las 19:00 del día anterior al próximo día sin agua
    let aviso: Date | null = null;
    for (let k = 0; k <= 8 && !aviso; k++) {
      const dia = new Date(ahora.getFullYear(), ahora.getMonth(), ahora.getDate() + k);
      if (dia.getDay() !== dow) continue;
      const cand = new Date(dia.getFullYear(), dia.getMonth(), dia.getDate() - 1, 19, 0);
      if (cand.getTime() > ahora.getTime()) aviso = cand;
    }
    if (!aviso) continue;
    const fin = new Date(aviso.getTime() + 30 * 60000);
    const nombre = diaSemana(x.fecha);
    const cuando = new Date(consultado + "T12:00:00").toLocaleDateString("es-MX", { day: "numeric", month: "long" });
    const resumen = `Llena tu tinaco: mañana (${nombre}) te quedas sin agua`;
    const nota = `Llena tinaco, cubetas y botellas esta noche. Según el calendario del SIAPA consultado el ${cuando}; puede cambiar, así que revísalo en Aguanta. Recuerda clorar el agua guardada.`;
    eventos.push([
      "BEGIN:VEVENT",
      `UID:aguanta-${dow}-${marcaUTC(ahora)}@aguanta`,
      `DTSTAMP:${marcaUTC(ahora)}`,
      `DTSTART:${marca(aviso)}`,
      `DTEND:${marca(fin)}`,
      "RRULE:FREQ=WEEKLY;COUNT=4",
      plegar(`SUMMARY:${texto(resumen)}`),
      plegar(`DESCRIPTION:${texto(nota)}`),
      "BEGIN:VALARM",
      "TRIGGER:PT0S",
      "ACTION:DISPLAY",
      plegar(`DESCRIPTION:${texto(resumen)}`),
      "END:VALARM",
      "END:VEVENT",
    ].join("\r\n"));
  }
  if (!eventos.length) return null;
  return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Aguanta//Tlaquepaque//ES", "CALSCALE:GREGORIAN", ...eventos, "END:VCALENDAR", ""].join("\r\n");
}
