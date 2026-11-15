import Image from "next/image";
import { IconoCerrar } from "./Iconos";

/** La mascota de cuerpo completo en tamaño chico, para avatares, la barra y la carga. Se dimensiona por altura. Es decorativa: el texto de al lado dice lo importante. */
export function MascotaChica({ className = "h-14" }: { className?: string }) {
  return <Image src="/mascota/tlacuache.webp" alt="" width={379} height={409} className={`w-auto shrink-0 ${className}`} />;
}

/** La mascota de cuerpo completo: un tlacuache con un mapa y una manguera. */
export function Mascota({ className = "w-36" }: { className?: string }) {
  return <Image src="/mascota/tlacuache.webp" alt="Un tlacuache con un mapa y una manguera, la mascota de Aguanta" width={379} height={409} className={`h-auto ${className}`} />;
}

/** Un consejo corto de la mascota. Solo guía: no da cifras ni afirma nada sobre el agua. */
export function Consejo({ children, className = "", cara = "h-16", onCerrar }: {
  children: React.ReactNode; className?: string; cara?: string; onCerrar?: () => void;
}) {
  return (
    <div role="note" className={`flex items-start gap-2.5 ${className}`}>
      <MascotaChica className={cara} />
      <div className="relative min-w-0 flex-1 rounded-2xl rounded-tl-sm bg-white px-4 py-2.5 text-sm leading-relaxed text-tinta shadow-suave">
        <div className={onCerrar ? "pr-6" : ""}>{children}</div>
        {onCerrar && (
          <button type="button" onClick={onCerrar} aria-label="Cerrar consejo"
            className="absolute right-1.5 top-1.5 grid h-7 w-7 place-items-center rounded-full text-tinta-suave hover:bg-agua-50"><IconoCerrar className="h-4 w-4" /></button>
        )}
      </div>
    </div>
  );
}
