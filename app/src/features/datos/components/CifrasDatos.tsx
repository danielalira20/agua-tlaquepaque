import { fmt, textoVentana, type Datos } from "@/lib/real";
import { BarraRango, Etiqueta, Tarjeta, textoRango } from "@/ui";
import type { DatosCalculados } from "../calculos";

/** Tres cifras de partida: a cuántas personas, a cuántas casas y a cuántos días sin agua se refiere todo. */
export function CifrasDatos({ d, g }: { d: Datos; g: DatosCalculados }) {
  const c = d.meta.conteos;
  return (
    <section className="grid gap-4 md:grid-cols-3" aria-label="Cifras de partida">
      <Tarjeta>
        <div className="font-display text-3xl font-bold leading-none tabular-nums">{fmt(c.personas)}</div>
        <div className="mt-2 text-sm leading-snug text-tinta-suave">personas en Tlaquepaque; {fmt(c.personas_en_programa)} viven dentro del programa de racionamiento</div>
        <Etiqueta tipo="real" className="mt-3" />
      </Tarjeta>
      <Tarjeta>
        <BarraRango tam="lg" min={g.tot.min} max={g.tot.max} total={g.tot.viv} etiqueta={<>viviendas sin tinaco ni cisterna en todo el municipio; dentro de las zonas con tandeo, {textoRango(g.enPrograma.min, g.enPrograma.max)}</>} />
        <Etiqueta tipo="real" className="mt-3" />
      </Tarjeta>
      <Tarjeta>
        <div className="font-display text-3xl font-bold leading-none tabular-nums">{textoRango(g.sem.vig.min, g.sem.vig.max)}</div>
        <div className="mt-2 text-sm leading-snug text-tinta-suave">personas-día sin agua en la semana {textoVentana(d.meta)}, con el calendario vigente</div>
        <Etiqueta tipo="estimado" className="mt-3" />
      </Tarjeta>
    </section>
  );
}
