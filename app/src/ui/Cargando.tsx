import { Gota } from "./SemanaGotas";
/** Estado de carga amable: una gota y una frase. */
export function Cargando({ texto = "Cargando datos reales…" }: { texto?: string }) {
  return (
    <div className="grid min-h-[50vh] place-items-center p-10">
      <div className="flex flex-col items-center gap-3 text-tinta-suave">
        <div className="animate-bounce"><Gota nivel={0.6} className="h-12 w-12" /></div>
        <p className="text-sm font-semibold">{texto}</p>
      </div>
    </div>
  );
}
