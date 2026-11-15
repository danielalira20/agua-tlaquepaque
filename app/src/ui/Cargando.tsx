import { MascotaChica } from "./Mascota";
/** Estado de carga amable: la mascota y una frase. */
export function Cargando({ texto = "Cargando datos reales…" }: { texto?: string }) {
  return (
    <div className="grid min-h-[50vh] place-items-center p-10">
      <div className="flex flex-col items-center gap-3 text-tinta-suave">
        <div className="motion-safe:animate-bounce"><MascotaChica className="h-28" /></div>
        <p className="text-sm font-semibold">{texto}</p>
      </div>
    </div>
  );
}
