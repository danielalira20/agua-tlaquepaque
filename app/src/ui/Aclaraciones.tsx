// Desplegable cerrado con lo que hay que saber para leer bien una pantalla.
// Cada uno lleva un título que dice de qué trata (nunca un rótulo genérico), para que
// la persona sepa qué va a encontrar antes de abrirlo.
export function Aclaraciones({ titulo, resumen, lista, children, className = "" }: {
  titulo: string; resumen?: string; lista?: string[]; children?: React.ReactNode; className?: string;
}) {
  return (
    <details className={`group rounded-2xl border border-barro-200 bg-barro-50 px-4 py-3 text-sm text-barro-700 ${className}`}>
      <summary className="flex cursor-pointer list-none items-center justify-between gap-3 font-semibold">
        <span>{titulo}{resumen ? <span className="font-normal text-barro-600"> · {resumen}</span> : null}</span>
        <span className="text-lg leading-none transition-transform group-open:rotate-45" aria-hidden="true">+</span>
      </summary>
      <div className="mt-2 space-y-2 leading-relaxed">
        {lista && <ul className="list-disc space-y-1 pl-5">{lista.map((a) => <li key={a}>{a}</li>)}</ul>}
        {children}
      </div>
    </details>
  );
}
