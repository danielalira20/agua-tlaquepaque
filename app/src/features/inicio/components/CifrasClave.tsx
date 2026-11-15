"use client";
import { useMemo } from "react";
import { useReal } from "@/lib/real";
import { BarraRango, Etiqueta, Tarjeta } from "@/ui";

/** Tres cifras, calculadas de los datos (no escritas a mano), salvo El Sauz, que viene del hallazgo documentado. */
export function CifrasClave() {
  const d = useReal();
  const t = useMemo(() => {
    if (!d) return null;
    let min = 0, max = 0, viv = 0;
    for (const m of d.manzanas) if (m.en_programa) { min += m.sin_almacen_min; max += m.sin_almacen_max; viv += m.viviendas; }
    return { min, max, viv };
  }, [d]);
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Tarjeta>
        {t ? <BarraRango tam="lg" min={t.min} max={t.max} total={t.viv} etiqueta="casas sin tinaco ni cisterna en las zonas con tandeo (3 a 6)" />
          : <div className="h-20 animate-pulse rounded-2xl bg-crema-2" />}
        <Etiqueta tipo="real" className="mt-3" />
      </Tarjeta>
      <Tarjeta>
        <div className="font-display text-3xl font-bold leading-none">El Sauz</div>
        <div className="mt-2 text-sm leading-snug text-tinta-suave">la colonia de mayor riesgo: 11,889 personas, casi todas sin dónde guardar agua y sin cisterna comunitaria</div>
        <Etiqueta tipo="real" className="mt-3" />
      </Tarjeta>
      <Tarjeta>
        <div className="font-display text-3xl font-bold leading-none">{d ? `${d.plan.parametros.pipas} pipas · ${d.meta.conteos.cisternas} cisternas` : "…"}</div>
        <div className="mt-2 text-sm leading-snug text-tinta-suave">lo que el municipio ya opera, hoy sin una herramienta que diga a dónde mandarlas</div>
        <Etiqueta tipo="real" className="mt-3" />
      </Tarjeta>
    </div>
  );
}
