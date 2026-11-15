import { fmt } from "@/lib/real";
import { BarraRango, Etiqueta, Tarjeta, textoRango } from "@/ui";
import type { DatosCalculados } from "../calculos";

/** Marginación: una capa aparte. Cada grado con su barra de viviendas sin almacenamiento. */
export function Equidad({ g }: { g: DatosCalculados }) {
  const total = Math.max(...g.eq.map((x) => x.smax));
  return (
    <Tarjeta as="section">
      <h2 className="text-xl font-bold leading-snug">La marginación se muestra aparte: no entra en el cálculo ni en la prioridad de las pipas</h2>
      <p className="mt-1 text-sm leading-relaxed text-tinta-suave">Grado de marginación urbana por AGEB (CONAPO 2020, dataset 17), con las casas sin tinaco ni cisterna de cada grado.</p>
      <ul className="mt-4 space-y-4">
        {g.eq.map((x) => (
          <li key={x.gr}>
            <div className="flex items-baseline justify-between gap-3"><span className="font-bold">{x.gr}</span><span className="text-xs text-tinta-suave">{fmt(x.pob)} personas</span></div>
            <BarraRango tam="md" tono="barro" min={x.smin} max={x.smax} total={total} className="mt-1"
              etiqueta={<>viviendas sin tinaco ni cisterna · {textoRango(x.pmin, x.pmax)} personas-día sin agua en la semana</>} />
          </li>
        ))}
      </ul>
      <Etiqueta tipo="real" className="mt-4" />
    </Tarjeta>
  );
}
