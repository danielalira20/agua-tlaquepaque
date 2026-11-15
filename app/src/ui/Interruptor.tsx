/** Renglón con interruptor: nombre, una línea de ayuda y el switch. */
export function Interruptor({ etiqueta, ayuda, activo, onCambio, deshabilitado = false, muestra }: {
  etiqueta: string; ayuda?: string; activo: boolean; onCambio: (v: boolean) => void; deshabilitado?: boolean; muestra?: React.ReactNode;
}) {
  return (
    <label className={`flex items-center gap-3 rounded-2xl bg-white px-4 py-3 shadow-suave ${deshabilitado ? "opacity-50" : "cursor-pointer"}`}>
      {muestra && <span className="shrink-0">{muestra}</span>}
      <span className="min-w-0 flex-1">
        <span className="block text-sm font-semibold">{etiqueta}</span>
        {ayuda && <span className="block text-xs text-tinta-suave">{ayuda}</span>}
      </span>
      <input type="checkbox" className="peer sr-only" checked={activo} disabled={deshabilitado} onChange={(e) => onCambio(e.target.checked)} />
      <span aria-hidden className="relative h-6 w-11 shrink-0 rounded-full bg-crema-2 transition-colors peer-checked:bg-agua-600 peer-focus-visible:ring-2 peer-focus-visible:ring-agua-300 after:absolute after:left-0.5 after:top-0.5 after:h-5 after:w-5 after:rounded-full after:bg-white after:shadow after:transition-transform peer-checked:after:translate-x-5" />
    </label>
  );
}

/** Dos o tres opciones excluyentes en una píldora. */
export function Segmentado<T extends string>({ opciones, valor, onCambio, className = "" }: {
  opciones: { valor: T; texto: string }[]; valor: T; onCambio: (v: T) => void; className?: string;
}) {
  return (
    <div role="radiogroup" className={`flex rounded-full bg-crema-2 p-1 ${className}`}>
      {opciones.map((o) => (
        <button key={o.valor} type="button" role="radio" aria-checked={valor === o.valor} onClick={() => onCambio(o.valor)}
          className={`min-h-9 flex-1 rounded-full px-3 text-sm font-semibold transition-all ${valor === o.valor ? "bg-white text-agua-800 shadow-suave" : "text-tinta-suave hover:text-tinta"}`}>{o.texto}</button>
      ))}
    </div>
  );
}
