"use client";
// Mi casa: tres preguntas cortas y un resultado. La cuenta vive en features/mi-casa/calculos.ts.
import { useMemo, useState } from "react";
import { useReal } from "@/lib/real";
import { Antetitulo, Cargando, IconoAtras, IconoFlecha } from "@/ui";
import { coloniasDe, resultadoCasa, type Almacen } from "@/features/mi-casa/calculos";
import { HojaConsumo } from "@/features/mi-casa/components/HojaConsumo";
import { PasoAlmacen } from "@/features/mi-casa/components/PasoAlmacen";
import { PasoColonia } from "@/features/mi-casa/components/PasoColonia";
import { PasoPersonas } from "@/features/mi-casa/components/PasoPersonas";
import { Progreso } from "@/features/mi-casa/components/Progreso";
import { Resultado } from "@/features/mi-casa/components/Resultado";

const PASOS = [
  { corto: "Colonia", pregunta: "¿En qué colonia vives?", ayuda: "Escríbela o elígela de la lista." },
  { corto: "Agua guardada", pregunta: "¿Cómo guardas agua en casa?", ayuda: "Elige lo que tienes." },
  { corto: "Personas", pregunta: "¿Cuántas personas viven en tu casa?", ayuda: "Cuenta a todas las que toman agua en casa." },
];

export default function MiCasa() {
  const d = useReal();
  const [paso, setPaso] = useState(0); // 0–2 preguntas, 3 resultado
  const [colonia, setColonia] = useState("");
  const [alm, setAlm] = useState<Almacen | null>(null);
  const [personas, setPersonas] = useState(4);
  const [consumo, setConsumo] = useState(50);
  const [ajustar, setAjustar] = useState(false);

  const colonias = useMemo(() => (d ? coloniasDe(d) : []), [d]);
  const col = colonias.find((c) => c.nombre === colonia);
  const r = useMemo(() => (d && col && alm ? resultadoCasa(d, col, alm, personas, consumo) : null), [d, col, alm, personas, consumo]);

  if (!d) return <Cargando />;

  if (paso === 3 && r && alm) {
    return (
      <main className="mx-auto max-w-5xl p-4 md:p-6">
        <Resultado d={d} r={r} alm={alm} personas={personas} consumo={consumo} onEditar={setPaso} onAjustar={() => setAjustar(true)}
          onReiniciar={() => { setPaso(0); setColonia(""); setAlm(null); setPersonas(4); setConsumo(50); }} />
        <HojaConsumo abierta={ajustar} onCerrar={() => setAjustar(false)} consumo={consumo} onConsumo={setConsumo} tinacoL={d.meta.supuestos.tinaco_l} cisternaL={d.meta.supuestos.cisterna_l} />
      </main>
    );
  }

  const listo = paso === 0 ? !!col : paso === 1 ? !!alm : true;
  const p = PASOS[Math.min(paso, 2)];
  return (
    <main className="mx-auto max-w-xl p-4 md:p-6">
      <Progreso paso={paso} titulos={PASOS.map((x) => x.corto)} onIr={setPaso} />
      <div key={paso} className="aparecer mt-4">
        <Antetitulo>¿Cuánto aguanta tu casa?</Antetitulo>
        <h1 className="mt-1 text-3xl font-bold leading-tight">{p.pregunta}</h1>
        <p className="mb-4 mt-1 text-tinta-suave">{p.ayuda}</p>
        {paso === 0 && <PasoColonia colonias={colonias} valor={colonia} onElegir={(n) => { setColonia(n); setPaso(1); }} />}
        {paso === 1 && <PasoAlmacen valor={alm} onElegir={(a) => { setAlm(a); setPaso(2); }} tinacoL={d.meta.supuestos.tinaco_l} cisternaL={d.meta.supuestos.cisterna_l} />}
        {paso === 2 && <PasoPersonas valor={personas} onCambio={setPersonas} />}
      </div>
      <div className="mt-6 flex items-center justify-between gap-3">
        {paso > 0 ? (
          <button type="button" onClick={() => setPaso(paso - 1)} className="inline-flex min-h-12 items-center gap-2 rounded-full bg-white px-5 font-semibold shadow-suave hover:bg-agua-50"><IconoAtras /> Atrás</button>
        ) : <span />}
        <button type="button" disabled={!listo} onClick={() => setPaso(paso + 1)}
          className="inline-flex min-h-12 items-center gap-2 rounded-full bg-agua-600 px-6 font-semibold text-white shadow-suave transition-all hover:bg-agua-700 disabled:cursor-not-allowed disabled:opacity-40">
          {paso === 2 ? "Ver mi resultado" : "Siguiente"} <IconoFlecha className="h-5 w-5" />
        </button>
      </div>
    </main>
  );
}
