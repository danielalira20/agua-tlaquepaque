import { fmt } from "@/lib/real";
import { BarraRango, Etiqueta, Tarjeta } from "@/ui";
import type { DatosCalculados } from "../calculos";

type Fila = DatosCalculados["top"][number];

function Colonia({ nombre, x, total }: { nombre: string; x: Fila[1]; total: number }) {
  const zonas = [...x.zonas].sort().join(", ");
  return (
    <li>
      <div className="flex items-baseline justify-between gap-3">
        <span className="font-bold">{nombre}</span>
        <span className="shrink-0 text-xs text-tinta-suave">{zonas ? `Zona ${zonas}` : <span className="text-barro-600">fuera del programa</span>}</span>
      </div>
      <BarraRango tam="md" tono="barro" min={x.min} max={x.max} total={total} className="mt-1"
        etiqueta={<>viviendas sin tinaco ni cisterna · {Math.round((100 * x.min) / x.viv)}–{Math.round((100 * x.max) / x.viv)} % de sus viviendas · {fmt(x.pob)} personas</>} />
    </li>
  );
}

/** Las colonias con más viviendas sin dónde guardar agua. Seis a la vista, el resto se abre. */
export function Colonias({ g }: { g: DatosCalculados }) {
  const total = Math.max(...g.top.map(([, x]) => x.max));
  const primeras = g.top.slice(0, 6), resto = g.top.slice(6);
  return (
    <Tarjeta as="section">
      <h2 className="text-xl font-bold leading-snug">{g.top[0]?.[0]} encabeza la lista de colonias con más casas sin tinaco ni cisterna</h2>
      <p className="mt-1 text-sm leading-relaxed text-tinta-suave">Las {g.top.length} colonias con más viviendas sin almacenamiento. La barra oscura es la cota mínima; la clara, hasta la máxima.</p>
      <ul className="mt-4 space-y-4">{primeras.map(([n, x]) => <Colonia key={n} nombre={n} x={x} total={total} />)}</ul>
      {resto.length > 0 && (
        <details className="group mt-4">
          <summary className="flex min-h-10 cursor-pointer list-none items-center justify-center rounded-full bg-crema-2 px-4 text-sm font-semibold text-agua-800 hover:bg-agua-50">
            <span className="group-open:hidden">Ver las otras {resto.length}</span><span className="hidden group-open:inline">Ocultar</span>
          </summary>
          <ul className="mt-4 space-y-4">{resto.map(([n, x]) => <Colonia key={n} nombre={n} x={x} total={total} />)}</ul>
        </details>
      )}
      <Etiqueta tipo="real" className="mt-4" />
    </Tarjeta>
  );
}
