"use client";
import { useEffect, useState } from "react";
import { MascotaChica } from "./Mascota";

/** Etapas de las pantallas que calculan sobre los datos reales (mapa y plan de pipas). */
export const ETAPAS_MAPA = ["Descargando los datos reales", "Calculando con el motor oficial", "Dibujando el mapa"];

/**
 * Estado de carga amable: la mascota y una frase. Con `etapas` muestra en qué paso va (`etapa` empieza en 0),
 * para que una espera larga no parezca una pantalla trabada. Si pasan 8 s, avisa que está tardando.
 * `sinMascota` es para cuando ya hay otra mascota en pantalla (el consejo del mapa).
 */
export function Cargando({ texto = "Cargando datos reales…", etapas, etapa = 0, sinMascota = false }: { texto?: string; etapas?: string[]; etapa?: number; sinMascota?: boolean }) {
  const [lento, setLento] = useState(false);
  useEffect(() => { const t = setTimeout(() => setLento(true), 8000); return () => clearTimeout(t); }, []);
  return (
    <div className="grid min-h-[50vh] place-items-center p-8" role="status" aria-live="polite">
      <div className="flex w-full max-w-xs flex-col items-center gap-3 text-center text-tinta-suave">
        {!sinMascota && <div className="motion-safe:animate-bounce"><MascotaChica className="h-28" /></div>}
        {etapas ? (
          <>
            <p className="text-sm font-semibold text-tinta">{etapas[Math.min(etapa, etapas.length - 1)]}…</p>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-agua-50" aria-hidden>
              <div className="h-full rounded-full bg-agua-600 transition-all duration-500" style={{ width: `${((Math.min(etapa, etapas.length - 1) + 0.5) / etapas.length) * 100}%` }} />
            </div>
            <ol className="w-full space-y-1 text-left text-xs">
              {etapas.map((e, i) => (
                <li key={e} className={`flex items-center gap-2 ${i === etapa ? "font-semibold text-tinta" : i < etapa ? "text-agua-700" : "text-tinta-suave/70"}`}>
                  <span aria-hidden className={`grid h-4 w-4 shrink-0 place-items-center rounded-full text-[10px] ${i < etapa ? "bg-agua-600 text-white" : i === etapa ? "border-2 border-agua-600 motion-safe:animate-pulse" : "border border-tinta/20"}`}>{i < etapa ? "✓" : ""}</span>
                  {e}
                </li>
              ))}
            </ol>
          </>
        ) : (
          <p className="text-sm font-semibold">{texto}</p>
        )}
        <p className="text-xs">{lento ? "Está tardando más de lo normal. Si no avanza, revisa tu conexión y recarga la página." : "La primera vez puede tardar unos segundos."}</p>
      </div>
    </div>
  );
}
