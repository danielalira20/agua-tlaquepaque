"use client";
import { useEffect } from "react";
import { IconoCerrar } from "./Iconos";

/** Hoja que se abre desde la derecha (escritorio) o desde abajo (celular). Esc o fondo para cerrar. */
export function Hoja({ abierta, onCerrar, titulo, children }: { abierta: boolean; onCerrar: () => void; titulo: string; children: React.ReactNode }) {
  useEffect(() => {
    if (!abierta) return;
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onCerrar(); };
    document.addEventListener("keydown", esc);
    return () => document.removeEventListener("keydown", esc);
  }, [abierta, onCerrar]);
  if (!abierta) return null;
  return (
    <div className="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label={titulo}>
      <button type="button" aria-label="Cerrar" onClick={onCerrar} className="absolute inset-0 bg-tinta/30 backdrop-blur-[2px]" />
      <div className="aparecer absolute inset-x-0 bottom-0 max-h-[85vh] overflow-y-auto rounded-t-[2rem] bg-crema p-5 shadow-flota md:inset-y-3 md:left-auto md:right-3 md:max-h-none md:w-[26rem] md:rounded-tarjeta">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="text-xl font-bold">{titulo}</h2>
          <button type="button" onClick={onCerrar} aria-label="Cerrar" className="grid h-10 w-10 place-items-center rounded-full bg-white shadow-suave hover:bg-agua-50"><IconoCerrar /></button>
        </div>
        {children}
      </div>
    </div>
  );
}
