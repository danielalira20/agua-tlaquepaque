// Todas las advertencias de una pantalla en un solo lugar, siempre igual.
export function LetraChica({ lista, children, className = "" }: { lista?: string[]; children?: React.ReactNode; className?: string }) {
  return (
    <details className={`group rounded-2xl border border-barro-200 bg-barro-50 px-4 py-3 text-sm text-barro-700 ${className}`}>
      <summary className="flex cursor-pointer list-none items-center justify-between gap-3 font-semibold">
        <span>Letra chica{lista ? ` · ${lista.length} cosas que hay que saber` : ""}</span>
        <span className="text-lg leading-none transition-transform group-open:rotate-45">+</span>
      </summary>
      <div className="mt-2 space-y-2 leading-relaxed">
        {lista && <ul className="list-disc space-y-1 pl-5">{lista.map((a) => <li key={a}>{a}</li>)}</ul>}
        {children}
      </div>
    </details>
  );
}
