"use client";
import { useMemo, useState } from "react";
import { IconoCheck, IconoLupa } from "@/ui";
import { normaliza, type Colonia } from "../calculos";

/** Paso 1: buscador de colonia con lista que se filtra al escribir (no un menú de 200 opciones). */
export function PasoColonia({ colonias, valor, onElegir }: { colonias: Colonia[]; valor: string; onElegir: (nombre: string) => void }) {
  const [q, setQ] = useState("");
  const lista = useMemo(() => {
    const n = normaliza(q);
    return n ? colonias.filter((c) => normaliza(c.nombre).includes(n)) : colonias;
  }, [colonias, q]);
  return (
    <div>
      <label className="relative block">
        <span className="sr-only">Buscar tu colonia</span>
        <IconoLupa className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-tinta-suave" />
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Escribe tu colonia" autoComplete="off" enterKeyHint="search"
          onKeyDown={(e) => { if (e.key === "Enter" && lista[0]) onElegir(lista[0].nombre); }}
          className="min-h-12 w-full rounded-full bg-white pl-12 pr-4 text-base shadow-suave outline-none ring-1 ring-tinta/10 placeholder:text-tinta-suave focus:ring-2 focus:ring-agua-500" />
      </label>
      <div className="mt-3 max-h-[min(22rem,48vh)] overflow-y-auto rounded-2xl bg-white p-1.5 shadow-suave" role="listbox" aria-label="Colonias">
        {lista.length === 0 && <p className="p-4 text-sm text-tinta-suave">No encontramos «{q}». Prueba con otra parte del nombre.</p>}
        {lista.map((c) => {
          const sel = c.nombre === valor;
          return (
            <button key={c.nombre} type="button" role="option" aria-selected={sel} onClick={() => onElegir(c.nombre)}
              className={`flex min-h-12 w-full items-center justify-between gap-3 rounded-xl px-3 text-left transition-colors ${sel ? "bg-agua-50 text-agua-800" : "hover:bg-crema"}`}>
              <span className="font-semibold">{c.nombre}</span>
              <span className="flex shrink-0 items-center gap-2 text-xs text-tinta-suave">
                {c.zonas.length ? `Zona ${c.zonas.join(", ")}` : "Sin racionamiento"}
                {sel && <IconoCheck className="h-5 w-5 text-agua-600" />}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
