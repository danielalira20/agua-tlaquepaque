"use client";
import { useMemo } from "react";
import { Badge } from "./ui";

/** Panal animado para el inicio: cada celda se vacía y se vuelve a llenar como el agua, a su propio ritmo. */
export default function PanalHero({ radio = 5, tam = 22 }: { radio?: number; tam?: number }) {
  const celdas = useMemo(() => {
    const out: { x: number; y: number; d: number; dur: number; k: number }[] = [];
    let s = 11;
    const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let q = -radio; q <= radio; q++) for (let r = Math.max(-radio, -q - radio); r <= Math.min(radio, -q + radio); r++) {
      const x = tam * Math.sqrt(3) * (q + r / 2), y = tam * 1.5 * r;
      const dist = Math.hypot(x, y) / (tam * radio * 1.5);
      out.push({ x, y, d: -(rnd() * 9), dur: 6 + rnd() * 6, k: dist });
    }
    return out;
  }, [radio, tam]);
  const w = tam * Math.sqrt(3) * (2 * radio + 1) + 8, h = tam * 1.5 * (2 * radio) + tam * 2 + 8;
  const pts = Array.from({ length: 6 }, (_, i) => { const a = (Math.PI / 180) * (60 * i - 30); return `${(tam * 0.94 * Math.cos(a)).toFixed(2)},${(tam * 0.94 * Math.sin(a)).toFixed(2)}`; }).join(" ");

  return (
    <div>
      <style>{`
        @keyframes vaciar { 0%,15% { fill:#1d4ed8 } 45% { fill:#93c5fd } 60%,70% { fill:#e2e8f0 } 85%,100% { fill:#1d4ed8 } }
        @keyframes flotar { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
        .celda { animation: vaciar var(--dur) ease-in-out infinite; animation-delay: var(--d); }
        .panal { animation: flotar 7s ease-in-out infinite; }
      `}</style>
      <svg viewBox={`${-w / 2} ${-h / 2} ${w} ${h}`} className="panal w-full max-w-md drop-shadow-[0_20px_40px_rgba(29,78,216,0.25)]" aria-hidden>
        <defs><radialGradient id="brillo"><stop offset="0" stopColor="#60a5fa" stopOpacity="0.5" /><stop offset="1" stopColor="#60a5fa" stopOpacity="0" /></radialGradient></defs>
        <circle r={w / 2.2} fill="url(#brillo)" />
        {celdas.map((c, i) => (
          <polygon key={i} points={pts} transform={`translate(${c.x} ${c.y})`} className="celda" fill="#1d4ed8"
            style={{ ["--d" as string]: `${c.d - c.k * 3}s`, ["--dur" as string]: `${c.dur}s`, opacity: 0.95 - c.k * 0.35 }} />
        ))}
      </svg>
      <div className="mx-auto -mt-2 flex w-fit items-center gap-2 whitespace-nowrap rounded-full bg-white/90 px-3 py-1 text-xs shadow backdrop-blur">
        <span className="h-2 w-2 rounded-full bg-emerald-500" /> Demo con datos simulados <Badge tipo="simulado" />
      </div>
    </div>
  );
}
