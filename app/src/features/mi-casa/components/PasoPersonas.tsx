import { IconoMas, IconoMenos, IconoPersona } from "@/ui";

const MIN = 1, MAX = 10;

/** Paso 3: un contador grande con − y +, y las personas dibujadas. */
export function PasoPersonas({ valor, onCambio }: { valor: number; onCambio: (n: number) => void }) {
  const boton = "grid h-14 w-14 place-items-center rounded-full bg-white text-agua-700 shadow-suave transition-all hover:bg-agua-50 active:scale-95 disabled:opacity-40";
  return (
    <div className="rounded-tarjeta bg-white p-6 shadow-suave">
      <div className="flex items-center justify-center gap-6">
        <button type="button" className={boton} onClick={() => onCambio(Math.max(MIN, valor - 1))} disabled={valor <= MIN} aria-label="Una persona menos"><IconoMenos className="h-6 w-6" /></button>
        <div className="min-w-24 text-center" aria-live="polite">
          <div className="font-display text-6xl font-bold tabular-nums text-agua-700">{valor}</div>
          <div className="text-sm text-tinta-suave">{valor === 1 ? "persona" : "personas"}</div>
        </div>
        <button type="button" className={boton} onClick={() => onCambio(Math.min(MAX, valor + 1))} disabled={valor >= MAX} aria-label="Una persona más"><IconoMas className="h-6 w-6" /></button>
      </div>
      <div className="mt-5 flex flex-wrap justify-center gap-1" aria-hidden>
        {Array.from({ length: MAX }, (_, i) => <IconoPersona key={i} className={`h-7 w-7 transition-colors duration-200 ${i < valor ? "text-agua-500" : "text-crema-2"}`} />)}
      </div>
    </div>
  );
}
