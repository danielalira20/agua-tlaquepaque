import { fmt, type Celda, type Datos } from "@/lib/real";
import { colorPct } from "@/components/HexMap";
import { Hex, Hoja, Info, textoRango } from "@/ui";

const CONF: Record<string, string> = { alta: "alta", media: "media", baja: "baja", conflicto: "fuentes en conflicto", ambiguo: "ambigua", ninguna: "fuera del programa", sin_poligono: "sin polígono", sin_geometria: "sin ubicación" };

function Fila({ texto, min, max, total, color }: { texto: string; min: number; max: number; total: number; color: string }) {
  const a = total ? (100 * min) / total : 0, b = total ? (100 * max) / total : 0;
  return (
    <li>
      <div className="flex justify-between text-sm"><span>{texto}</span><b className="tabular-nums">{textoRango(min, max)}</b></div>
      <div className="mt-1 h-2 overflow-hidden rounded-full bg-crema-2">
        <div className="relative h-full">
          <div className={`absolute inset-y-0 left-0 rounded-full ${color}`} style={{ width: `${a}%` }} />
          {b > a && <div className={`absolute inset-y-0 rounded-r-full opacity-40 ${color}`} style={{ left: `${a}%`, width: `${b - a}%` }} />}
        </div>
      </div>
    </li>
  );
}

/** Detalle de un hexágono: qué colonias son, cuántas casas se secan y cómo guardan agua. */
export function HojaHexagono({ d, c, onCerrar }: { d: Datos; c: Celda | undefined; onCerrar: () => void }) {
  if (!c) return null;
  let tin = 0, cis = 0, nmin = 0, nmax = 0;
  const conf: Record<string, number> = {};
  for (const i of c.manzanas) {
    const m = d.manzanas[i];
    tin += m.viv_tinaco; cis += m.viv_cisterna; nmin += m.sin_almacen_min; nmax += m.sin_almacen_max;
    conf[m.zona_confianza] = (conf[m.zona_confianza] ?? 0) + m.pob;
  }
  const titulo = c.colonias.slice(0, 3).join(", ") + (c.colonias.length > 3 ? ` y ${c.colonias.length - 3} más` : "") || "Sin colonia";
  return (
    <Hoja abierta onCerrar={onCerrar} titulo={titulo} modal={false}>
      <p className="-mt-2 text-sm text-tinta-suave">Zona {c.zonas.join(", ") || "fuera del programa"} · {c.manzanas.length} manzanas · {fmt(c.pob)} personas</p>

      <div className="mt-4 rounded-2xl bg-white p-4 shadow-suave">
        <div className="flex items-center gap-3">
          <Hex className="h-10 w-10 shrink-0 drop-shadow" style={{ color: c.en_programa ? `rgb(${colorPct(c.pct_min).join(",")})` : "rgb(214,214,208)" }} />
          <div className="font-display text-5xl font-bold tabular-nums leading-none">{textoRango(Math.round(c.pct_min * 100), Math.round(c.pct_max * 100))} %</div>
        </div>
        <div className="mt-1 text-sm text-tinta-suave">de las casas sin agua este día · {textoRango(c.pers_min, c.pers_max)} personas</div>
      </div>

      <div className="mt-4 rounded-2xl bg-white p-4 shadow-suave">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold">Cómo guardan agua sus {fmt(c.viviendas)} casas</h3>
          <Info lado="abajo" etiqueta="Por qué un rango">El Censo no cruza tinaco con cisterna: una casa puede tener las dos. Por eso las casas sin nada van como rango y las barras no suman 100 %.</Info>
        </div>
        <ul className="mt-3 space-y-3">
          <Fila texto="Sin tinaco ni cisterna" min={nmin} max={nmax} total={c.viviendas} color="bg-barro-500" />
          <Fila texto="Con tinaco" min={tin} max={tin} total={c.viviendas} color="bg-agua-500" />
          <Fila texto="Con cisterna" min={cis} max={cis} total={c.viviendas} color="bg-agua-300" />
        </ul>
      </div>

      <details className="group mt-4 rounded-2xl bg-white px-4 py-3 text-sm shadow-suave">
        <summary className="flex cursor-pointer list-none items-center justify-between font-semibold">Detalles<span className="transition-transform group-open:rotate-45">+</span></summary>
        <div className="mt-2 space-y-2 text-tinta-suave">
          <div>Marginación dominante: <b className="text-tinta">{c.marg}</b> (capa aparte, no entra en el cálculo).</div>
          <div>Confianza de la zona:
            <ul className="mt-1 list-disc pl-5">{Object.entries(conf).map(([k, v]) => <li key={k}>{CONF[k] ?? k}: {fmt(v)} personas</li>)}</ul>
          </div>
        </div>
      </details>
    </Hoja>
  );
}
