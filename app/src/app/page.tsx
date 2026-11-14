import Link from "next/link";
import { Tarjeta, Badge } from "@/components/ui";
import PanalHero from "@/components/PanalHero";

export default function Inicio() {
  return (
    <main className="mx-auto max-w-5xl p-6">
      <section className="grid items-center gap-8 py-10 md:grid-cols-[1.2fr_1fr]">
        <div>
          <div className="text-sm font-semibold uppercase tracking-wider text-blue-700">Hackathon Jalisco 2026 · Reto 01 Ciudades</div>
          <h1 className="mt-2 text-4xl font-bold leading-tight">El mismo corte de agua: para una casa es una molestia, para la de enfrente es una emergencia.</h1>
          <p className="mt-4 text-lg text-slate-600">Cruzamos el Censo (quién tiene tinaco, cisterna o nada) con el calendario de tandeo del SIAPA para decir, manzana por manzana y día por día, <b>cuántas viviendas se quedan sin agua</b> en Tlaquepaque, y a dónde mandar las pipas primero.</p>
          <div className="mt-6 flex gap-3">
            <Link href="/panal" className="rounded-full bg-blue-700 px-5 py-2.5 font-medium text-white">Ver el panal</Link>
            <Link href="/mi-casa" className="rounded-full bg-slate-100 px-5 py-2.5 font-medium">¿Cuánto aguanta tu casa?</Link>
          </div>
        </div>
        <div className="justify-self-center"><PanalHero /></div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Tarjeta><div className="text-3xl font-bold">17,420 – 34,429</div><div className="text-sm text-slate-600">viviendas sin tinaco ni cisterna dentro del programa de racionamiento de Tlaquepaque (zonas 3 a 6)</div><div className="mt-2"><Badge tipo="real" /> <span className="text-xs text-slate-500">Censo 2020 + zonas del SIAPA, cota mín–máx</span></div></Tarjeta>
        <Tarjeta><div className="text-3xl font-bold">El Sauz</div><div className="text-sm text-slate-600">la colonia de mayor riesgo: 11,889 personas, la gran mayoría de sus viviendas sin dónde guardar agua y ninguna cisterna comunitaria. Zona 6.</div><div className="mt-2"><Badge tipo="real" /></div></Tarjeta>
        <Tarjeta><div className="text-3xl font-bold">32 pipas · 50 cisternas</div><div className="text-sm text-slate-600">lo que el municipio ya opera, hoy sin una herramienta que priorice dónde se secan las casas</div><div className="mt-2"><Badge tipo="real" /> <span className="text-xs text-slate-500">prensa y mapa municipal, 2026</span></div></Tarjeta>
      </section>

      <section className="mt-10 grid gap-4 md:grid-cols-3">
        {[
          ["1. Medimos", "Por cada colonia, cuántas viviendas no tienen dónde guardar agua, cuántas tienen tinaco y cuántas cisterna. Nunca promediamos: una casa sin tinaco no usa el del vecino."],
          ["2. Anticipamos", "Con el calendario del SIAPA sabemos qué día se corta el agua en cada zona y cuántas horas aguanta cada tipo de casa. El panal se va vaciando día a día."],
          ["3. Actuamos", "Las mismas 32 pipas, repartidas primero a donde más viviendas están secas y más marginación hay. Sin pedir más agua."],
        ].map(([t, d]) => <Tarjeta key={t}><div className="font-semibold">{t}</div><p className="mt-1 text-sm text-slate-600">{d}</p></Tarjeta>)}
      </section>

      <section className="mt-10 rounded-2xl border border-dashed border-slate-300 p-5 text-sm text-slate-600">
        <b>Qué hay que saber de estos números.</b> Un día de racionamiento se modela como cero agua: es la cota alta del daño (el SIAPA dice que es baja de presión). El 16 % de la población tiene zona solo por el polígono del portal. El Censo es de 2020 y no dice de cuántos litros son los tinacos. El calendario del SIAPA ya cambió una vez y puede volver a cambiar. Por eso todo número va como rango, y cada uno lleva su etiqueta: <Badge tipo="real" /> <Badge tipo="estimado" /> <Badge tipo="simulado" />.
      </section>
    </main>
  );
}
