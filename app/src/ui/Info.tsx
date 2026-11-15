"use client";
import { useCallback, useEffect, useId, useRef, useState } from "react";

type Posicion = { left: number; ancho: number; alto: number; top?: number; bottom?: number };

const MARGEN = 12;
const ANCHO_MAX = 336;
const ALTO_MAX = 416;

/**
 * ⓘ: la explicación se abre solo si se pide. Clic para abrir, Esc o clic fuera para cerrar.
 * El recuadro va con posición fija y se acomoda dentro de la pantalla, así que
 * nunca se sale por un lado ni obliga a deslizar. Se cierra al hacer scroll o cambiar de tamaño.
 */
export function Info({ children, etiqueta = "Más información", lado = "abajo", className = "" }: {
  children: React.ReactNode; etiqueta?: string; lado?: "abajo" | "arriba"; className?: string;
}) {
  const [pos, setPos] = useState<Posicion | null>(null);
  const boton = useRef<HTMLButtonElement>(null);
  const caja = useRef<HTMLSpanElement>(null);
  const globo = useRef<HTMLSpanElement>(null);
  const id = useId();
  const abierto = pos !== null;

  const abrir = useCallback(() => {
    const el = boton.current; if (!el) return;
    const r = el.getBoundingClientRect();
    const ancho = Math.min(ANCHO_MAX, window.innerWidth - MARGEN * 2);
    const left = Math.min(Math.max(MARGEN, r.left + r.width / 2 - ancho / 2), window.innerWidth - ancho - MARGEN);
    const espacioAbajo = window.innerHeight - r.bottom;
    const arriba = lado === "arriba" ? r.top > 160 : espacioAbajo < 320 && r.top > espacioAbajo;
    const alto = Math.max(120, Math.min(ALTO_MAX, (arriba ? r.top : espacioAbajo) - 8 - MARGEN));
    setPos(arriba ? { left, ancho, alto, bottom: window.innerHeight - r.top + 8 } : { left, ancho, alto, top: r.bottom + 8 });
  }, [lado]);

  useEffect(() => {
    if (!abierto) return;
    const cerrar = () => setPos(null);
    const fuera = (e: MouseEvent) => {
      const t = e.target as Node;
      if (caja.current?.contains(t) || globo.current?.contains(t)) return;
      cerrar();
    };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") cerrar(); };
    const scroll = (e: Event) => { if (!globo.current?.contains(e.target as Node)) cerrar(); };
    document.addEventListener("mousedown", fuera); document.addEventListener("keydown", esc);
    window.addEventListener("scroll", scroll, true); window.addEventListener("resize", cerrar);
    return () => {
      document.removeEventListener("mousedown", fuera); document.removeEventListener("keydown", esc);
      window.removeEventListener("scroll", scroll, true); window.removeEventListener("resize", cerrar);
    };
  }, [abierto]);

  return (
    <span ref={caja} className={`inline-flex align-middle ${className}`}>
      <button ref={boton} type="button" aria-label={etiqueta} aria-expanded={abierto} aria-controls={id} onClick={() => (abierto ? setPos(null) : abrir())}
        className={`grid h-6 w-6 place-items-center rounded-full text-[13px] font-bold transition-colors ${abierto ? "bg-agua-600 text-white" : "bg-agua-50 text-agua-700 hover:bg-agua-100"}`}>i</button>
      {pos && (
        <span ref={globo} id={id} role="dialog" aria-label={etiqueta}
          style={{ position: "fixed", left: pos.left, width: pos.ancho, maxHeight: pos.alto, top: pos.top, bottom: pos.bottom }}
          className="aparecer z-[100] block overflow-y-auto rounded-2xl bg-tinta p-4 text-left text-sm font-normal normal-case leading-relaxed tracking-normal text-white shadow-flota">
          {children}
        </span>
      )}
    </span>
  );
}
