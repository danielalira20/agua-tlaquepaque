import { fechaLarga } from "@/lib/real";
import { Etiqueta } from "@/ui";
import type { ResultadoCasa } from "../calculos";

/** Maqueta del aviso que recibiría la familia. Siempre marcada como simulada. */
export function AvisoWhatsApp({ r }: { r: ResultadoCasa }) {
  return (
    <section className="rounded-tarjeta bg-[#e7f6e9] p-4 shadow-suave">
      <div className="flex items-center justify-between gap-2 text-xs font-semibold text-tinta-suave"><span>Así sería el aviso en tu WhatsApp</span><Etiqueta tipo="simulado" /></div>
      <div className="mt-2 rounded-2xl rounded-tl-none bg-white p-3 text-sm leading-relaxed shadow-sm">
        Hola, en <b>{r.col.nombre}</b>{" "}
        {r.primera ? <>te quedarías sin agua el <b>{fechaLarga(r.primera.fecha)}</b>. Llena todo lo que puedas la noche anterior.</> : "esta semana tu reserva alcanza."}{" "}
        {r.cis ? "Hay cisterna comunitaria en tu colonia." : "La cisterna más cercana está en una colonia vecina."} Recuerda clorar el agua guardada.
      </div>
    </section>
  );
}
