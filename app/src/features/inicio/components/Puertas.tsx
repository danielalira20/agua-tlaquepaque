import Link from "next/link";
import { IconoCasa, IconoFlecha, IconoLibro, IconoPipa } from "@/ui";

const PUERTAS = [
  { href: "/mi-casa", quien: "Para tu familia", titulo: "¿Cuánto aguanta mi casa?", linea: "Tu colonia y tu tinaco: qué días te quedas sin agua.", Icono: IconoCasa, fondo: "bg-agua-600 text-white", icono: "bg-white/20 text-white", quienC: "text-agua-100" },
  { href: "/panal", quien: "Para coordinar", titulo: "Planear las pipas de hoy", linea: "Quién se seca hoy y a dónde mandar las pipas.", Icono: IconoPipa, fondo: "bg-barro-100 text-tinta", icono: "bg-barro-500 text-white", quienC: "text-barro-700" },
  { href: "/datos", quien: "Para el jurado", titulo: "Cómo lo calculamos", linea: "Datos, modelo y fuentes, con sus límites.", Icono: IconoLibro, fondo: "bg-white text-tinta", icono: "bg-agua-50 text-agua-700", quienC: "text-tinta-suave" },
] as const;

/** Tres puertas: cada persona entra por la suya. */
export function Puertas() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {PUERTAS.map(({ href, quien, titulo, linea, Icono, fondo, icono, quienC }, i) => (
        <Link key={href} href={href} style={{ animationDelay: `${120 + i * 90}ms` }}
          className={`aparecer group flex flex-col rounded-tarjeta p-5 shadow-suave transition-all duration-300 hover:-translate-y-1 hover:shadow-flota ${fondo}`}>
          <span className={`grid h-12 w-12 place-items-center rounded-2xl ${icono}`}><Icono className="h-6 w-6" /></span>
          <span className={`mt-4 text-xs font-bold uppercase tracking-[0.14em] ${quienC}`}>{quien}</span>
          <span className="mt-1 font-display text-xl font-bold leading-tight">{titulo}</span>
          <span className="mt-1 text-sm opacity-80">{linea}</span>
          <span className="mt-4 inline-flex items-center gap-1 text-sm font-semibold">Entrar <IconoFlecha className="h-4 w-4 transition-transform group-hover:translate-x-1" /></span>
        </Link>
      ))}
    </div>
  );
}
