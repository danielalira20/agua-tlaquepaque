import { COLOR_MARG, GRADIENTE_AGUA } from "@/components/HexMap";

/** Leyenda compacta sobre el mapa. */
export function Leyenda({ modo, className = "" }: { modo: "agua" | "marginacion"; className?: string }) {
  return (
    <div className={`rounded-2xl bg-white/95 px-3 py-2 text-[11px] text-tinta-suave shadow-suave backdrop-blur ${className}`}>
      {modo === "agua" ? (
        <>
          <div className="mb-1 font-semibold text-tinta">% de casas sin agua · altura = personas</div>
          <div className="h-2 w-48 rounded-full" style={{ background: GRADIENTE_AGUA }} />
          <div className="mt-0.5 flex w-48 justify-between"><span>con agua</span><span>50 % o más secas</span></div>
          <div className="mt-1 flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-sm bg-[rgb(214,214,208)]" />fuera del programa</div>
        </>
      ) : (
        <>
          <div className="mb-1 font-semibold text-tinta">Marginación (CONAPO 2020)</div>
          <div className="flex max-w-56 flex-wrap gap-x-2 gap-y-1">
            {Object.entries(COLOR_MARG).map(([k, v]) => <span key={k} className="flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-sm" style={{ background: `rgb(${v.join(",")})` }} />{k}</span>)}
          </div>
        </>
      )}
    </div>
  );
}
