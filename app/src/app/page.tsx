// Inicio: ¿qué quieres saber? Un héroe, tres puertas y tres cifras. Lo demás, en un desplegable al final.
import PanalHero from "@/components/PanalHero";
import { Puertas } from "@/features/inicio/components/Puertas";
import { CifrasClave } from "@/features/inicio/components/CifrasClave";
import { Antetitulo, IconoGota, IconoMapa, IconoPipa, Mascota, Aclaraciones } from "@/ui";

const PASOS = [
  { Icono: IconoGota, t: "Medimos", d: "Quién tiene tinaco, cisterna o nada, manzana por manzana." },
  { Icono: IconoMapa, t: "Anticipamos", d: "Qué día se seca cada casa con el calendario del SIAPA." },
  { Icono: IconoPipa, t: "Actuamos", d: "A dónde mandar primero las mismas pipas." },
];

export default function Inicio() {
  return (
    <main className="mx-auto max-w-6xl px-4 pb-12 md:px-6">
      <section className="grid items-center gap-6 py-8 md:grid-cols-[1.25fr_1fr] md:py-12">
        <div className="aparecer">
          <Antetitulo>Tandeo en San Pedro Tlaquepaque</Antetitulo>
          <h1 className="mt-3 text-4xl font-extrabold leading-[1.05] tracking-tight md:text-6xl">
            El mismo corte de agua no le pega igual a <span className="text-barro-500">todas las casas</span>.
          </h1>
          <p className="mt-4 max-w-xl text-lg text-tinta-suave">Aguanta te dice qué casas se quedan sin agua cada día y a dónde mandar las pipas primero.</p>
        </div>
        <div className="relative justify-self-center">
          <PanalHero />
          <Mascota className="pointer-events-none absolute -bottom-6 -left-14 hidden w-32 md:block lg:-left-20 lg:w-40" />
        </div>
      </section>

      <Puertas />

      <section className="mt-10">
        <CifrasClave />
      </section>

      <section className="mt-10 grid gap-3 md:grid-cols-3">
        {PASOS.map(({ Icono, t, d }, i) => (
          <div key={t} className="flex items-start gap-3 rounded-2xl p-2">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-agua-100 text-agua-700"><Icono /></span>
            <div><div className="font-display font-bold">{i + 1}. {t}</div><p className="text-sm text-tinta-suave">{d}</p></div>
          </div>
        ))}
      </section>

      <Aclaraciones className="mt-10" titulo="¿Qué tan firmes son estos números?" resumen="límites y etiquetas">
        <p>Un día de racionamiento se modela como cero agua: es la cota alta del daño (el SIAPA dice que es baja de presión). El 16 % de la población tiene zona solo por el polígono del portal. El Censo es de 2020 y no dice de cuántos litros son los tinacos. El calendario del SIAPA ya cambió una vez y puede volver a cambiar.</p>
        <p>Por eso todo número va como rango y cada uno lleva su etiqueta: <b>Dato real</b> (fuente oficial), <b>Estimado</b> (lo calcula el modelo) o <b>Simulado</b> (maqueta).</p>
        <p className="text-xs">Hackathon Jalisco Internacional 2026 · Reto 01 Ciudades inteligentes.</p>
      </Aclaraciones>
    </main>
  );
}
