"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Hex, IconoCasa, IconoInicio, IconoLibro, IconoMapa, IconoPipa } from "./Iconos";

// Las URL no cambian (manual, video y reporte las usan); solo cambian los nombres.
const RUTAS = [
  { href: "/", largo: "Inicio", corto: "Inicio", Icono: IconoInicio },
  { href: "/mi-casa", largo: "Mi casa", corto: "Mi casa", Icono: IconoCasa },
  { href: "/panal", largo: "Mapa de hoy", corto: "Mapa", Icono: IconoMapa },
  { href: "/pipas", largo: "Plan de pipas", corto: "Pipas", Icono: IconoPipa },
  { href: "/datos", largo: "Cómo funciona", corto: "Método", Icono: IconoLibro },
] as const;

export function Navegacion() {
  const p = usePathname();
  const activa = (href: string) => (href === "/" ? p === "/" : p.startsWith(href));
  return (
    <>
      <header className="sticky top-0 z-30 flex h-14 items-center gap-6 border-b border-tinta/10 bg-crema/90 px-4 backdrop-blur md:px-6">
        <Link href="/" aria-label="Aguanta, inicio" className="flex shrink-0 items-center gap-2">
          <Hex className="h-7 w-7 text-agua-600" />
          <span className="font-display text-xl font-bold tracking-tight">Aguanta</span>
        </Link>
        <nav className="hidden gap-1 md:flex" aria-label="Secciones">
          {RUTAS.map(({ href, largo, Icono }) => (
            <Link key={href} href={href} aria-current={activa(href) ? "page" : undefined}
              className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-colors ${activa(href) ? "bg-agua-600 text-white shadow-suave" : "text-tinta-suave hover:bg-agua-50 hover:text-agua-700"}`}>
              <Icono className="h-4 w-4" />{largo}
            </Link>
          ))}
        </nav>
        <span className="ml-auto hidden text-sm text-tinta-suave lg:block">Tandeo en Tlaquepaque</span>
      </header>

      {/* celular: barra inferior con 5 íconos */}
      <nav aria-label="Secciones" className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-5 border-t border-tinta/10 bg-crema/95 pb-[env(safe-area-inset-bottom)] backdrop-blur md:hidden">
        {RUTAS.map(({ href, corto, Icono }) => (
          <Link key={href} href={href} aria-current={activa(href) ? "page" : undefined}
            className={`flex min-h-14 flex-col items-center justify-center gap-0.5 text-[11px] font-semibold ${activa(href) ? "text-agua-700" : "text-tinta-suave"}`}>
            <span className={`grid h-7 w-12 place-items-center rounded-full transition-colors ${activa(href) ? "bg-agua-100" : ""}`}><Icono className="h-5 w-5" /></span>
            {corto}
          </Link>
        ))}
      </nav>
    </>
  );
}
