import { fechaLarga, fmt, type Resumen } from "@/lib/real";
import { Antetitulo, BarraRango, Etiqueta, Info, SemanaGotas, Tarjeta, textoRango, type DiaGota } from "@/ui";

/** La tarjeta del día: una cifra protagonista, dos chicas y el selector de la semana. */
export function TarjetaHoy({ fecha, dias, onFecha, r, zonasHoy, z56, uHoras, original, className = "" }: {
  fecha: string; dias: DiaGota[]; onFecha: (f: string) => void; r: Resumen; zonasHoy: string;
  z56: { min: number; max: number } | null; uHoras: number; original: boolean; className?: string;
}) {
  return (
    <Tarjeta as="section" className={`aparecer ${className}`}>
      <div className="flex items-center justify-between gap-2">
        <Antetitulo>Mapa de hoy</Antetitulo>
        <Etiqueta tipo="estimado" />
      </div>
      <h1 className="mt-1 text-2xl font-bold capitalize">{fechaLarga(fecha)}</h1>
      <p className="text-sm text-tinta-suave">
        Sin servicio: zonas {zonasHoy}{original && <b className="ml-1 rounded-full bg-barro-100 px-2 py-0.5 text-xs text-barro-700">calendario original</b>}
      </p>

      <SemanaGotas className="mt-3" dias={dias} valor={fecha} onCambio={onFecha} />

      <BarraRango className="mt-5" tam="lg" min={r.sin_min} max={r.sin_max} total={r.viv}
        etiqueta={<span className="inline-flex items-center gap-2">viviendas se quedan sin agua
          <Info etiqueta="¿Por qué dos números?">El Censo dice cuántas casas tienen tinaco y cuántas cisterna, pero no cuántas tienen las dos. El primer número cuenta las casas que <b>seguro</b> se quedan sin agua; el segundo, las que <b>podrían</b>. En la barra, lo oscuro es el mínimo y lo claro llega al máximo, sobre {fmt(r.viv)} viviendas.</Info>
        </span>} />

      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-2xl bg-crema p-3">
          <div className="font-display text-lg font-bold tabular-nums leading-tight">{textoRango(r.pers_min, r.pers_max)}</div>
          <div className="text-xs text-tinta-suave">personas sin agua</div>
        </div>
        <div className="rounded-2xl bg-crema p-3">
          <div className="font-display text-lg font-bold tabular-nums leading-tight">{fmt(r.mzas_quiebre)}</div>
          <div className="text-xs text-tinta-suave">manzanas con 10 % o más de casas secas</div>
        </div>
      </div>

      <details className="group mt-3 rounded-2xl bg-crema px-3 py-2 text-sm">
        <summary className="flex cursor-pointer list-none items-center justify-between font-semibold text-agua-700">Más del día<span className="transition-transform group-open:rotate-45">+</span></summary>
        <ul className="mt-2 space-y-2 text-tinta-suave">
          {z56 && <li><b className="text-tinta">{z56.max.toFixed(1)} % – {z56.min.toFixed(1)} %</b> del riesgo de almacenamiento está en las zonas 5 y 6.</li>}
          <li><b className="text-tinta">{textoRango(r.guard_min, r.guard_max)}</b> viviendas tienen agua guardada hace más de {uHoras} h: hay que desinfectarla.</li>
        </ul>
      </details>
      <p className="mt-3 text-xs text-tinta-suave">Toca un hexágono para ver sus colonias.</p>
    </Tarjeta>
  );
}
