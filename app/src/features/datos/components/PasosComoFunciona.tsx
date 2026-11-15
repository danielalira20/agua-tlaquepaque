import { Antetitulo, IconoFlecha, IconoGota, IconoMapa, IconoPipa, IconoTinaco } from "@/ui";

const PASOS = [
  { Icono: IconoMapa, titulo: "El agua llega por turnos", texto: "El SIAPA reparte el agua por zona y por día. Cada manzana sabe en qué zona cae.", tono: "bg-agua-100 text-agua-700" },
  { Icono: IconoTinaco, titulo: "Cada casa guarda lo que puede", texto: "Con tinaco, con cisterna, con los dos o con nada. El Censo no los cruza, así que cada cifra sale como rango.", tono: "bg-agua-100 text-agua-700" },
  { Icono: IconoGota, titulo: "La reserva se gasta", texto: "Si dura menos que las horas sin servicio, la casa se queda sin agua ese día.", tono: "bg-barro-100 text-barro-700" },
  { Icono: IconoPipa, titulo: "Las pipas van a donde más se seca", texto: "El priorizador elige primero las colonias con más casas secas ese día.", tono: "bg-barro-100 text-barro-700" },
] as const;

/** De la red a tu llave en cuatro pasos: se lee de un vistazo, de izquierda a derecha (arriba a abajo en el celular). */
export function PasosComoFunciona() {
  return (
    <section aria-label="Cómo funciona, en cuatro pasos">
      <Antetitulo className="mb-3">De la red a tu llave, en cuatro pasos</Antetitulo>
      <ol className="grid gap-3 md:grid-cols-4">
        {PASOS.map(({ Icono, titulo, texto, tono }, i) => (
          <li key={titulo} style={{ animationDelay: `${i * 90}ms` }} className="aparecer relative rounded-tarjeta bg-white p-4 shadow-suave">
            <div className="flex items-center gap-3">
              <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-full ${tono}`}><Icono className="h-6 w-6" /></span>
              <span className="font-display text-3xl font-bold text-tinta/20" aria-hidden>{i + 1}</span>
            </div>
            <h3 className="mt-3 text-lg font-bold leading-snug">{titulo}</h3>
            <p className="mt-1 text-sm leading-relaxed text-tinta-suave">{texto}</p>
            {i < PASOS.length - 1 && <IconoFlecha className="absolute -right-3.5 top-1/2 z-10 hidden h-6 w-6 -translate-y-1/2 rounded-full bg-crema p-0.5 text-agua-500 md:block" />}
          </li>
        ))}
      </ol>
    </section>
  );
}
