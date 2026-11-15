"use client";
import { useEffect, useId, useRef, useState } from "react";

/** ⓘ: la explicación se abre solo si se pide. Clic para abrir, Esc o clic fuera para cerrar. */
export function Info({ children, etiqueta = "Más información", lado = "abajo", className = "" }: {
  children: React.ReactNode; etiqueta?: string; lado?: "abajo" | "arriba"; className?: string;
}) {
  const [abierto, setAbierto] = useState(false);
  const caja = useRef<HTMLSpanElement>(null);
  const id = useId();
  useEffect(() => {
    if (!abierto) return;
    const fuera = (e: MouseEvent) => { if (caja.current && !caja.current.contains(e.target as Node)) setAbierto(false); };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") setAbierto(false); };
    document.addEventListener("mousedown", fuera); document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("mousedown", fuera); document.removeEventListener("keydown", esc); };
  }, [abierto]);
  return (
    <span ref={caja} className={`relative inline-flex align-middle ${className}`}>
      <button type="button" aria-label={etiqueta} aria-expanded={abierto} aria-controls={id} onClick={() => setAbierto(!abierto)}
        className={`grid h-6 w-6 place-items-center rounded-full text-[13px] font-bold transition-colors ${abierto ? "bg-agua-600 text-white" : "bg-agua-50 text-agua-700 hover:bg-agua-100"}`}>i</button>
      {abierto && (
        <span id={id} role="dialog" className={`aparecer absolute left-1/2 z-50 w-72 max-w-[80vw] -translate-x-1/2 rounded-2xl bg-tinta p-4 text-left text-sm font-normal normal-case leading-relaxed tracking-normal text-white shadow-flota ${lado === "abajo" ? "top-8" : "bottom-8"}`}>
          {children}
        </span>
      )}
    </span>
  );
}
