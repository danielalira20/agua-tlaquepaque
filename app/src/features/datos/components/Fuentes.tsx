import { fmt, type Datos } from "@/lib/real";
import { Antetitulo, Etiqueta } from "@/ui";

/** De dónde sale cada dato y para qué se usa. */
export function Fuentes({ d }: { d: Datos }) {
  const c = d.meta.conteos;
  const filas = [
    { n: "01", fuente: "INEGI · Censo 2020 por manzana", para: "Viviendas, ocupantes, tinaco y cisterna: alimentan el motor." },
    { n: "17", fuente: "CONAPO · marginación urbana por AGEB 2020", para: "Capa de equidad en el mapa y el desglose por grado." },
    { n: "—", fuente: `SIAPA · portal de rotación y lista oficial (${d.calendarios.vigente.consultado})`, para: "Zona de cada manzana y calendario por fecha (complemento)." },
    { n: "—", fuente: "Gobierno de Tlaquepaque · mapa de cisternas", para: `${fmt(c.cisternas)} cisternas y ${fmt(c.propuestas)} propuestas (complemento).` },
  ];
  return (
    <section>
      <Antetitulo className="mb-3">De dónde salen los datos</Antetitulo>
      <ul className="grid gap-3 md:grid-cols-2">
        {filas.map((f) => (
          <li key={f.fuente} className="flex items-start gap-3 rounded-2xl bg-white p-4 shadow-suave">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-agua-50 text-sm font-bold text-agua-700">{f.n}</span>
            <div className="min-w-0">
              <div className="font-bold leading-snug">{f.fuente}</div>
              <div className="text-sm leading-relaxed text-tinta-suave">{f.para}</div>
              <Etiqueta tipo="real" className="mt-2" />
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
