// Una cifra con dos cotas se dibuja: tramo seguro (mínimo) + tramo posible (hasta el máximo).
// Así no hace falta escribir "cota mínima – máxima" junto a cada número.
const f = (n: number, dec = 0) => n.toLocaleString("es-MX", { maximumFractionDigits: dec, minimumFractionDigits: dec });

export function textoRango(min: number, max: number, dec = 0) {
  return min === max ? f(min, dec) : `${f(min, dec)} – ${f(max, dec)}`;
}

export function BarraRango({ min, max, total, etiqueta, dec = 0, tam = "lg", tono = "barro", sufijo = "", className = "" }: {
  min: number; max: number; total?: number; etiqueta?: React.ReactNode; dec?: number; tam?: "xl" | "lg" | "md";
  tono?: "barro" | "agua" | "neutro"; sufijo?: string; className?: string;
}) {
  const txt = { xl: "text-5xl md:text-6xl", lg: "text-3xl", md: "text-xl" }[tam];
  const solido = { barro: "bg-barro-500", agua: "bg-agua-600", neutro: "bg-tinta-suave" }[tono];
  const claro = { barro: "bg-barro-200", agua: "bg-agua-200", neutro: "bg-tinta/20" }[tono];
  const a = total ? Math.min(100, (100 * min) / total) : 0;
  const b = total ? Math.min(100, (100 * max) / total) : 0;
  return (
    <div className={className}>
      <div className={`font-display font-bold leading-none tracking-tight tabular-nums ${txt}`}>
        {textoRango(min, max, dec)}{sufijo && <span className="ml-1 text-[0.5em] font-semibold text-tinta-suave">{sufijo}</span>}
      </div>
      {total ? (
        <div className="mt-3 h-2.5 w-full overflow-hidden rounded-full bg-crema-2" role="img"
          aria-label={`Entre ${f(min, dec)} y ${f(max, dec)} de ${f(total)}`}>
          <div className="relative h-full">
            <div className={`absolute inset-y-0 left-0 rounded-full ${solido} transition-[width] duration-500 ease-agua`} style={{ width: `${a}%` }} />
            <div className={`absolute inset-y-0 rounded-r-full ${claro} transition-all duration-500 ease-agua`} style={{ left: `${a}%`, width: `${Math.max(0, b - a)}%` }} />
          </div>
        </div>
      ) : null}
      {etiqueta && <div className="mt-2 text-sm leading-snug text-tinta-suave">{etiqueta}</div>}
    </div>
  );
}
