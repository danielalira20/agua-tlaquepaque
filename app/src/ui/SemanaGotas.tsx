"use client";
import { useId } from "react";

/** Una gota con nivel: 1 = llena (hay agua), 0 = barro (seca). */
export function Gota({ nivel, className = "h-8 w-8" }: { nivel: number; className?: string }) {
  const id = useId();
  const n = Math.max(0, Math.min(1, nivel));
  const y = 3 + (1 - n) * 19; // la gota ocupa de y=3 a y=22
  return (
    <svg viewBox="0 0 24 24" className={className} aria-hidden>
      <defs><clipPath id={id}><path d="M12 2.6c-3.3 4.5-6.4 7.7-6.4 11.3a6.4 6.4 0 0 0 12.8 0c0-3.6-3.1-6.8-6.4-11.3z" /></clipPath></defs>
      <g clipPath={`url(#${id})`}>
        <rect x="0" y="0" width="24" height="24" className="fill-barro-100" />
        <rect x="0" y={y} width="24" height="24" className="fill-agua-500 transition-all duration-500 ease-agua" />
      </g>
      <path d="M12 2.6c-3.3 4.5-6.4 7.7-6.4 11.3a6.4 6.4 0 0 0 12.8 0c0-3.6-3.1-6.8-6.4-11.3z" fill="none"
        className={n < 0.15 ? "stroke-barro-500" : "stroke-agua-700"} strokeWidth="1.4" />
    </svg>
  );
}

export type DiaGota = { fecha: string; dia: string; nivel: number; nota?: string };

/** La semana en 7 gotas. Sirve como selector (con onCambio) o como lectura (sin él). */
export function SemanaGotas({ dias, valor, onCambio, className = "" }: {
  dias: DiaGota[]; valor?: string; onCambio?: (fecha: string) => void; className?: string;
}) {
  return (
    <div className={`grid grid-cols-7 gap-1 ${className}`} role={onCambio ? "radiogroup" : "list"} aria-label="Días de la semana">
      {dias.map((d) => {
        const sel = d.fecha === valor;
        const contenido = (
          <>
            <span className="text-[11px] font-semibold capitalize">{d.dia.slice(0, 3)}</span>
            <Gota nivel={d.nivel} className="h-7 w-7" />
            <span className="text-[10px] tabular-nums opacity-70">{Number(d.fecha.slice(8))}</span>
          </>
        );
        const base = `flex flex-col items-center gap-0.5 rounded-2xl px-0.5 py-1.5 transition-all duration-200`;
        return onCambio ? (
          <button key={d.fecha} type="button" role="radio" aria-checked={sel} title={d.nota} onClick={() => onCambio(d.fecha)}
            className={`${base} ${sel ? "bg-white text-agua-800 shadow-suave ring-2 ring-agua-500" : "text-tinta-suave hover:bg-white/70"}`}>{contenido}</button>
        ) : (
          <div key={d.fecha} role="listitem" title={d.nota} className={`${base} ${sel ? "bg-white text-agua-800 ring-2 ring-agua-500" : "text-tinta-suave"}`}>{contenido}</div>
        );
      })}
    </div>
  );
}
