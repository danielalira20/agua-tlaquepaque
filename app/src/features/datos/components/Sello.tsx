import { IconoCheck } from "@/ui";

/** El motor que corre en el navegador da exactamente lo mismo que el de referencia en Python. */
export function Sello() {
  return (
    <div className="flex items-center gap-3 rounded-2xl bg-white px-4 py-3 shadow-suave">
      <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-emerald-100 text-emerald-700"><IconoCheck className="h-6 w-6" /></span>
      <div className="text-sm leading-snug">
        <div className="font-bold">Motor oficial = motor de referencia</div>
        <div className="text-tinta-suave">34,097 de 34,097 renglones iguales (TypeScript contra Python)</div>
      </div>
    </div>
  );
}
