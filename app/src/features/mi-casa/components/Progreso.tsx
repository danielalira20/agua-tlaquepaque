/** Tres barras: dónde vas y a dónde puedes volver. */
export function Progreso({ paso, titulos, onIr }: { paso: number; titulos: string[]; onIr: (p: number) => void }) {
  return (
    <div>
      <div className="flex gap-2" role="list" aria-label="Pasos">
        {titulos.map((t, i) => {
          const hecho = i < paso, actual = i === paso;
          const barra = `h-2 w-full rounded-full transition-colors duration-300 ${hecho || actual ? "bg-agua-600" : "bg-crema-2"} ${actual ? "ring-4 ring-agua-100" : ""}`;
          return hecho ? (
            <button key={t} type="button" role="listitem" onClick={() => onIr(i)} aria-label={`Volver al paso ${i + 1}: ${t}`} className="group flex-1 py-2"><span className={`block ${barra} group-hover:bg-agua-500`} /></button>
          ) : (
            <div key={t} role="listitem" aria-current={actual ? "step" : undefined} className="flex-1 py-2"><div className={barra} /></div>
          );
        })}
      </div>
      <div className="mt-1 text-xs font-bold uppercase tracking-[0.14em] text-agua-600">Paso {paso + 1} de {titulos.length}</div>
    </div>
  );
}
