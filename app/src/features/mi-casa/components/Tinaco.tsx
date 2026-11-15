"use client";
import { useEffect, useId, useState } from "react";

/**
 * El tinaco que se vacía: azul = las horas que cubre tu reserva, barro = lo que le falta
 * al corte más largo de la semana. Al abrirse baja desde lleno hasta su nivel.
 */
export function Tinaco({ nivel, className = "h-44 w-36" }: { nivel: number; className?: string }) {
  const id = useId();
  const [n, setN] = useState(1);
  useEffect(() => { const t = setTimeout(() => setN(Math.max(0, Math.min(1, nivel))), 400); return () => clearTimeout(t); }, [nivel]);
  const TOP = 24, ALTO = 112;
  const y = TOP + (1 - n) * ALTO;
  const cuerpo = "M14 54c0-17 13-30 46-30s46 13 46 30v62c0 12-13 20-46 20s-46-8-46-20z";
  return (
    <svg viewBox="0 0 120 150" className={className} role="img" aria-label={`Tinaco lleno al ${Math.round(nivel * 100)} %`}>
      <defs><clipPath id={id}><path d={cuerpo} /></clipPath></defs>
      <rect x="50" y="10" width="20" height="9" rx="4" className="fill-agua-200 stroke-agua-700" strokeWidth="2" />
      <path d={cuerpo} className="fill-barro-100" />
      <g clipPath={`url(#${id})`}>
        <g style={{ transform: `translateY(${y}px)`, transition: "transform 1.8s var(--ease-agua)" }}>
          <path d="M0 0q15-7 30 0t30 0 30 0 30 0V200H0z" className="fill-agua-500" />
          <path d="M0 6q15-7 30 0t30 0 30 0 30 0V200H0z" className="fill-agua-400" opacity="0.5" />
        </g>
        <rect x="24" y="44" width="7" height="58" rx="3.5" fill="white" opacity="0.35" />
      </g>
      <path d={cuerpo} fill="none" className="stroke-agua-700" strokeWidth="3" />
      {[0.25, 0.5, 0.75].map((m) => <path key={m} d={`M96 ${TOP + (1 - m) * ALTO}h10`} className="stroke-agua-700" strokeWidth="2" strokeLinecap="round" opacity="0.5" />)}
      <path d="M32 138v8M88 138v8" className="stroke-agua-700" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}
