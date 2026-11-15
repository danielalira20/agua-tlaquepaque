import { Deslizador } from "@/components/Controles";
import { Aclaraciones, Hoja } from "@/ui";
import { fmt } from "@/lib/real";

/** Ajustar: el consumo por persona y lo que supone el cálculo. Cerrado por defecto. */
export function HojaConsumo({ abierta, onCerrar, consumo, onConsumo, tinacoL, cisternaL }: {
  abierta: boolean; onCerrar: () => void; consumo: number; onConsumo: (c: number) => void; tinacoL: number; cisternaL: number;
}) {
  const supuestos = [
    `Un tinaco de ${fmt(tinacoL)} L y una cisterna de ${fmt(cisternaL)} L, llenos al empezar el racionamiento.`,
    "Un día de racionamiento cuenta como cero agua: es la peor cota (el SIAPA dice que es baja de presión).",
    "Si tu colonia abarca varias zonas, se toma el peor caso de cada día.",
  ];
  return (
    <Hoja abierta={abierta} onCerrar={onCerrar} titulo="Ajustar el cálculo">
      <div className="rounded-2xl bg-white p-4 shadow-suave">
        <Deslizador label="Consumo por persona" value={consumo} min={50} max={150} step={25} unidad=" L/día" onChange={onConsumo} />
        <p className="mt-2 text-xs text-tinta-suave">50 L al día es el mínimo que recomienda la OMS. Si en tu casa se gasta más, mueve el control y tu resultado cambia al instante.</p>
      </div>
      <Aclaraciones className="mt-4" titulo="Qué supone este cálculo" resumen={`${supuestos.length} puntos`} lista={supuestos} />
    </Hoja>
  );
}
