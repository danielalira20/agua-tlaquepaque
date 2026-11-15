import { fmt } from "@/lib/real";
import type { Parada } from "../plan";

/** Las paradas del día. El número es el orden en que el priorizador eligió la colonia, no una ruta. */
export function ListaParadas({ paradas, seleccion, onElegir }: { paradas: Parada[]; seleccion: number | null; onElegir: (p: Parada) => void }) {
  return (
    <ol className="space-y-2">
      {paradas.map((p) => (
        <li key={p.colonia}>
          <button type="button" onClick={() => onElegir(p)} aria-pressed={seleccion === p.n}
            className={`flex w-full items-center gap-3 rounded-2xl bg-white p-3 text-left shadow-suave transition-all hover:-translate-y-0.5 ${seleccion === p.n ? "ring-2 ring-agua-500" : ""}`}>
            <span className="relative grid h-10 w-9 shrink-0 place-items-center">
              <svg viewBox="0 0 24 24" className="absolute inset-0 h-full w-full text-agua-700" aria-hidden><path fill="currentColor" d="M12 2.2c-3.5 4.8-6.8 8.2-6.8 12a6.8 6.8 0 0 0 13.6 0c0-3.8-3.3-7.2-6.8-12z" /></svg>
              <span className="relative mt-2 text-xs font-bold text-white">{p.n}</span>
            </span>
            <span className="min-w-0 flex-1">
              <span className="block truncate font-semibold">{p.colonia}</span>
              <span className="block text-xs text-tinta-suave">{p.viajes} {p.viajes === 1 ? "viaje" : "viajes"} · {fmt(p.viv)} casas · {fmt(p.pers)} personas</span>
            </span>
          </button>
        </li>
      ))}
    </ol>
  );
}
