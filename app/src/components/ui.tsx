"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function Badge({ tipo }: { tipo: "simulado" | "estimado" | "real" }) {
  const s = {
    simulado: "border-dashed border-slate-400 text-slate-600 bg-white",
    estimado: "border-sky-300 text-sky-800 bg-sky-50",
    real: "border-emerald-300 text-emerald-800 bg-emerald-50",
  }[tipo];
  const t = { simulado: "Simulado", estimado: "Estimado", real: "Dato real" }[tipo];
  return <span className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium ${s}`}>{t}</span>;
}

const rutas = [
  ["/", "Inicio"], ["/panal", "Panal"], ["/mi-casa", "Mi casa"], ["/pipas", "Pipas"], ["/datos", "Datos"],
] as const;

export function Nav() {
  const p = usePathname();
  return (
    <header className="flex h-14 items-center gap-6 border-b border-slate-200 bg-white px-5">
      <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tight text-slate-900">
        <Hex className="h-6 w-6 text-blue-600" /> Aguanta
      </Link>
      <nav className="flex gap-1">
        {rutas.map(([href, t]) => (
          <Link key={href} href={href} className={`rounded-full px-4 py-1.5 text-sm font-medium ${p === href ? "bg-blue-600 text-white" : "text-slate-700 hover:bg-slate-100"}`}>{t}</Link>
        ))}
      </nav>
      <span className="ml-auto hidden text-sm text-slate-500 md:block">¿Cuánto aguanta tu casa?</span>
    </header>
  );
}

export function Hex({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="currentColor"><path d="M12 2l8.66 5v10L12 22l-8.66-5V7z" /></svg>
  );
}

export function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`rounded-2xl border border-slate-200 bg-white p-5 shadow-sm ${className}`}>{children}</div>;
}

export function Kpi({ valor, etiqueta, badge }: { valor: string; etiqueta: string; badge?: "simulado" | "estimado" | "real" }) {
  return (
    <div>
      <div className="text-3xl font-bold tabular-nums text-slate-900">{valor}</div>
      <div className="text-sm text-slate-600">{etiqueta}</div>
      {badge && <div className="mt-1"><Badge tipo={badge} /></div>}
    </div>
  );
}
