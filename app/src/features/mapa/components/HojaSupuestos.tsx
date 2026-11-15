import type { SupuestosMotor } from "@/lib/motor";
import { Supuestos, diasTinaco } from "@/components/Controles";
import { Hoja, Aclaraciones } from "@/ui";

/** Los supuestos que mueven el mapa, y los avisos para leer el mapa. */
export function HojaSupuestos({ abierta, onCerrar, s, onCambio, cambiado, onRestablecer, advertencias }: {
  abierta: boolean; onCerrar: () => void; s: SupuestosMotor; onCambio: (s: SupuestosMotor) => void;
  cambiado: boolean; onRestablecer: () => void; advertencias: string[];
}) {
  return (
    <Hoja abierta={abierta} onCerrar={onCerrar} titulo="Ajustar supuestos">
      <div className="rounded-2xl bg-white p-4 shadow-suave">
        <div className="text-sm text-tinta-suave">Con estos supuestos, un tinaco aguanta</div>
        <div className="font-display text-4xl font-bold text-agua-700">{diasTinaco(s).toFixed(1)} días</div>
        <div className="text-xs text-tinta-suave">en una casa de 3.8 personas</div>
      </div>
      <div className="mt-4 rounded-2xl bg-white p-4 shadow-suave"><Supuestos s={s} onChange={onCambio} /></div>
      <p className="mt-3 text-xs leading-relaxed text-tinta-suave">Con 6 días o más, el orden de las manzanas es casi el del caso base; con menos de 4 cambia bastante. El caso base (50 L por persona, tinaco de 1,100 L) es el más cómodo.</p>
      {cambiado && <button type="button" onClick={onRestablecer} className="mt-3 min-h-10 rounded-full bg-agua-600 px-4 text-sm font-semibold text-white">Volver al caso base</button>}
      <Aclaraciones className="mt-5" titulo="Qué tener en cuenta al leer el mapa" resumen={`${advertencias.length} avisos`} lista={advertencias}>
        <p>Cada hexágono agrupa las manzanas reales que caen en él (H3, resolución 8).</p>
      </Aclaraciones>
    </Hoja>
  );
}
