"use client";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { precargarDatos } from "@/lib/real";
import { IconoCasa, IconoInicio, IconoLibro, IconoMapa, IconoPipa } from "./Iconos";

// Las URL no cambian (manual, video y reporte las usan); solo cambian los nombres.
const RUTAS = [
  { href: "/", largo: "Inicio", corto: "Inicio", Icono: IconoInicio },
  { href: "/mi-casa", largo: "Mi casa", corto: "Mi casa", Icono: IconoCasa },
  { href: "/panal", largo: "Mapa de hoy", corto: "Mapa", Icono: IconoMapa },
  { href: "/pipas", largo: "Plan de pipas", corto: "Pipas", Icono: IconoPipa },
  { href: "/datos", largo: "Cómo funciona", corto: "Método", Icono: IconoLibro },
] as const;

// Las pantallas del mapa pesan más (deck.gl y los datos): se empiezan a bajar al acercarse a su botón.
const PESADAS = ["/panal", "/pipas"];
const precargar = (href: string) => {
  if (!PESADAS.includes(href)) return;
  precargarDatos();
  void import("@/components/HexMap");
};

export function Navegacion() {
  const p = usePathname();
  // A dónde se tocó y aún no llega: marca el botón al instante y muestra una barra de avance, para que el clic nunca parezca muerto.
  const [destino, setDestino] = useState<string | null>(null);
  useEffect(() => { setDestino(null); }, [p]);
  useEffect(() => {
    if (!destino) return;
    const t = setTimeout(() => setDestino(null), 20000);
    return () => clearTimeout(t);
  }, [destino]);
  const activa = (href: string) => (href === "/" ? p === "/" : p.startsWith(href));
  const marcada = (href: string) => (destino ? href === destino : activa(href));
  const ir = (href: string) => () => { if (!activa(href)) setDestino(href); };
  const nombre = RUTAS.find((r) => r.href === destino)?.largo;
  return (
    <>
      <div aria-hidden className={`pointer-events-none fixed inset-x-0 top-0 z-50 h-1 overflow-hidden transition-opacity duration-150 ${destino ? "opacity-100" : "opacity-0"}`}>
        <div className="progreso-nav h-full w-1/3 rounded-full bg-agua-600" />
      </div>
      <p role="status" className="sr-only">{nombre ? `Abriendo ${nombre}…` : ""}</p>
      <header className="sticky top-0 z-30 flex h-14 items-center gap-6 border-b border-tinta/10 bg-crema/90 px-4 backdrop-blur md:px-6">
        <Link href="/" aria-label="Aguanta, inicio" className="flex shrink-0 items-center gap-2">
          <Image src="/mascota/tlacuache.webp" alt="" width={379} height={409} className="h-11 w-auto" priority />
          <span className="font-display text-xl font-bold tracking-tight">Aguanta</span>
        </Link>
        <nav className="hidden gap-1 md:flex" aria-label="Secciones">
          {RUTAS.map(({ href, largo, Icono }) => (
            <Link key={href} href={href} aria-current={activa(href) ? "page" : undefined} onClick={ir(href)} onPointerEnter={() => precargar(href)} onFocus={() => precargar(href)}
              className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-colors ${marcada(href) ? "bg-agua-600 text-white shadow-suave" : "text-tinta-suave hover:bg-agua-50 hover:text-agua-700"} ${destino === href ? "motion-safe:animate-pulse" : ""}`}>
              <Icono className="h-4 w-4" />{largo}
            </Link>
          ))}
        </nav>
        <span className="ml-auto hidden text-sm text-tinta-suave lg:block">Tandeo en Tlaquepaque</span>
      </header>

      {/* celular: barra inferior con 5 íconos */}
      <nav aria-label="Secciones" className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-5 border-t border-tinta/10 bg-crema/95 pb-[env(safe-area-inset-bottom)] backdrop-blur md:hidden">
        {RUTAS.map(({ href, corto, Icono }) => (
          <Link key={href} href={href} aria-current={activa(href) ? "page" : undefined} onClick={ir(href)} onTouchStart={() => precargar(href)} onFocus={() => precargar(href)}
            className={`flex min-h-14 flex-col items-center justify-center gap-0.5 text-[11px] font-semibold ${marcada(href) ? "text-agua-700" : "text-tinta-suave"}`}>
            <span className={`grid h-7 w-12 place-items-center rounded-full transition-colors ${marcada(href) ? "bg-agua-100" : ""} ${destino === href ? "motion-safe:animate-pulse" : ""}`}><Icono className="h-5 w-5" /></span>
            {corto}
          </Link>
        ))}
      </nav>
    </>
  );
}
