import { Gota, IconoCisterna, IconoTinaco } from "@/ui";
import { fmt } from "@/lib/real";
import type { Almacen } from "../calculos";

const OPCIONES: { valor: Almacen; titulo: string; Icono: () => React.ReactNode }[] = [
  { valor: "ninguno", titulo: "Nada", Icono: () => <Gota nivel={0} className="h-10 w-10" /> },
  { valor: "tinaco", titulo: "Tinaco", Icono: () => <IconoTinaco className="h-10 w-10" /> },
  { valor: "cisterna", titulo: "Cisterna", Icono: () => <IconoCisterna className="h-10 w-10" /> },
  { valor: "ambos", titulo: "Los dos", Icono: () => <span className="flex items-center"><IconoTinaco className="h-8 w-8" /><IconoCisterna className="-ml-1 h-8 w-8" /></span> },
];

/** Paso 2: cuatro tarjetas grandes con ícono; se entiende sin leer. */
export function PasoAlmacen({ valor, onElegir, tinacoL, cisternaL }: { valor: Almacen | null; onElegir: (a: Almacen) => void; tinacoL: number; cisternaL: number }) {
  const ayuda: Record<Almacen, string> = {
    ninguno: "Sin tinaco ni cisterna", tinaco: `Calculamos ${fmt(tinacoL)} L`, cisterna: `Calculamos ${fmt(cisternaL)} L`, ambos: `Calculamos ${fmt(tinacoL + cisternaL)} L`,
  };
  return (
    <div className="grid grid-cols-2 gap-3" role="radiogroup" aria-label="Cómo guardas agua">
      {OPCIONES.map(({ valor: v, titulo, Icono }) => {
        const sel = valor === v;
        return (
          <button key={v} type="button" role="radio" aria-checked={sel} onClick={() => onElegir(v)}
            className={`flex min-h-36 flex-col items-center justify-center gap-2 rounded-tarjeta p-4 text-center transition-all duration-200 ${sel ? "bg-agua-600 text-white shadow-flota" : "bg-white text-agua-700 shadow-suave hover:-translate-y-0.5 hover:shadow-flota"}`}>
            <Icono />
            <span className={`font-display text-lg font-bold ${sel ? "text-white" : "text-tinta"}`}>{titulo}</span>
            <span className={`text-xs ${sel ? "text-agua-100" : "text-tinta-suave"}`}>{ayuda[v]}</span>
          </button>
        );
      })}
    </div>
  );
}
