import { fechaLarga } from "@/lib/real";
import type { Datos } from "@/lib/real";
import { Antetitulo, Etiqueta, Gota, IconoAjustes, IconoCheck, SemanaGotas, Tarjeta, type DiaGota } from "@/ui";
import { ETIQUETA_ALMACEN, textoReserva, type Almacen, type ResultadoCasa } from "../calculos";
import { Acciones } from "./Acciones";
import { AvisoWhatsApp } from "./AvisoWhatsApp";
import { Tinaco } from "./Tinaco";

function Resumen({ colonia, alm, personas, onEditar }: { colonia: string; alm: Almacen; personas: number; onEditar: (paso: number) => void }) {
  const chip = "inline-flex min-h-10 items-center rounded-full bg-white px-4 text-sm font-semibold text-agua-800 shadow-suave transition-colors hover:bg-agua-50";
  return (
    <div className="flex flex-wrap gap-2" aria-label="Tus respuestas">
      <button type="button" className={chip} onClick={() => onEditar(0)} aria-label={`Cambiar colonia: ${colonia}`}>{colonia}</button>
      <button type="button" className={chip} onClick={() => onEditar(1)} aria-label={`Cambiar cómo guardas agua: ${ETIQUETA_ALMACEN[alm]}`}>{ETIQUETA_ALMACEN[alm]}</button>
      <button type="button" className={chip} onClick={() => onEditar(2)} aria-label={`Cambiar personas: ${personas}`}>{personas} {personas === 1 ? "persona" : "personas"}</button>
    </div>
  );
}

function Leyenda() {
  const it = (nivel: number, t: string) => <span className="inline-flex items-center gap-1"><Gota nivel={nivel} className="h-4 w-4" />{t}</span>;
  return <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-tinta-suave">{it(1, "llega el agua")}{it(0.55, "aguantas con tu reserva")}{it(0.05, "te quedas sin agua")}</div>;
}

/** Lo que ve la familia al terminar: el tinaco, la semana en gotas y qué hacer. */
export function Resultado({ d, r, alm, personas, consumo, onEditar, onAjustar, onReiniciar }: {
  d: Datos; r: ResultadoCasa; alm: Almacen; personas: number; consumo: number;
  onEditar: (paso: number) => void; onAjustar: () => void; onReiniciar: () => void;
}) {
  const dias: DiaGota[] = r.semana.map((x) => ({
    fecha: x.fecha, dia: x.dia, nivel: x.seca ? 0.05 : x.corte ? 0.55 : 1,
    nota: `${fechaLarga(x.fecha)}: ${x.seca ? "te quedas sin agua" : x.corte ? `aguantas (${x.H} h de corte)` : "llega el agua"}`,
  }));
  const titular = r.fuera ? "Tu colonia no está en el programa de racionamiento"
    : r.aut === 0 ? "Sin reserva: te quedas sin agua cada día de racionamiento"
    : `Tu reserva aguanta ${textoReserva(r.aut)}`;
  const cubre = r.fuera ? null : r.peor === 0 ? "Esta semana no hay corte en tu zona."
    : r.aut >= r.peor ? `Cubres las ${r.peor} h del corte más largo de la semana.`
    : `Cubres ${Math.round(r.aut)} de las ${r.peor} h del corte más largo de la semana.`;

  return (
    <div className="space-y-4">
      <Resumen colonia={r.col.nombre} alm={alm} personas={personas} onEditar={onEditar} />
      <div className="grid gap-4 md:grid-cols-[1.15fr_1fr]">
        <div className="space-y-4">
          <Tarjeta as="section" className="aparecer">
            <div className="flex items-center gap-4">
              {r.fuera ? <span className="grid h-24 w-24 shrink-0 place-items-center rounded-full bg-agua-50 text-agua-600"><IconoCheck className="h-12 w-12" /></span> : <Tinaco nivel={r.nivel} className="h-40 w-32 shrink-0" />}
              <div className="min-w-0">
                <Antetitulo>Tu casa en {r.col.nombre}</Antetitulo>
                <h1 className="mt-1 text-2xl font-bold leading-tight md:text-3xl">{titular}</h1>
                {!r.fuera && (
                  <span className={`mt-3 inline-flex rounded-full px-3 py-1 text-xs font-bold ${r.primera ? "bg-barro-100 text-barro-700" : "bg-agua-100 text-agua-800"}`}>
                    {r.primera ? <>Te quedas sin agua desde el&nbsp;{fechaLarga(r.primera.fecha)}</> : "Esta semana no te quedas sin agua"}
                  </span>
                )}
              </div>
            </div>
            {cubre && <p className="mt-3 text-sm text-tinta-suave">{cubre}{r.col.zonas.length > 1 && " Tu colonia abarca varias zonas: mostramos el peor caso."}</p>}
          </Tarjeta>

          <Tarjeta as="section">
            <Antetitulo className="mb-2">Tu semana</Antetitulo>
            <SemanaGotas dias={dias} />
            <Leyenda />
            <p className="mt-3 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-tinta-suave">
              <Etiqueta tipo="real" /> Calendario del portal del SIAPA, consultado el {d.calendarios.vigente.consultado}; puede cambiar.
            </p>
          </Tarjeta>
        </div>

        <div className="space-y-4">
          <Acciones colonia={r.col.nombre} cisternas={r.cis} />
          <AvisoWhatsApp r={r} />
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <button type="button" onClick={onAjustar} className="inline-flex min-h-10 items-center gap-2 rounded-full bg-white px-4 text-sm font-semibold text-agua-800 shadow-suave hover:bg-agua-50">
          <IconoAjustes /> Ajustar · {consumo} L por persona
        </button>
        <button type="button" onClick={onReiniciar} className="min-h-10 px-2 text-sm font-semibold text-tinta-suave underline underline-offset-4 hover:text-tinta">Empezar de nuevo</button>
      </div>
    </div>
  );
}
