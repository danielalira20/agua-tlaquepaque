import Link from "next/link";
import { Antetitulo, IconoCisterna, IconoGota, IconoTelefono, Info } from "@/ui";

function Accion({ Icono, tono, titulo, children }: { Icono: typeof IconoGota; tono: string; titulo: string; children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-3 rounded-2xl bg-white p-4 shadow-suave">
      <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-full ${tono}`}><Icono className="h-6 w-6" /></span>
      <div className="min-w-0">
        <div className="font-display font-bold">{titulo}</div>
        <div className="text-sm leading-relaxed text-tinta-suave">{children}</div>
      </div>
    </li>
  );
}

/** Tres cosas que sí puedes hacer si te quedas sin agua. */
export function Acciones({ colonia, cisternas }: { colonia: string; cisternas: number }) {
  return (
    <section>
      <Antetitulo className="mb-2">Si te quedas sin agua</Antetitulo>
      <ul className="space-y-2">
        <Accion Icono={IconoCisterna} tono="bg-agua-100 text-agua-700" titulo={cisternas > 0 ? `${cisternas} ${cisternas === 1 ? "cisterna" : "cisternas"} en ${colonia}` : `Sin cisterna comunitaria en ${colonia}`}>
          {cisternas > 0 ? "Cisternas comunitarias de tu colonia." : <>Busca cisternas de colonias vecinas en el <Link href="/panal" className="font-semibold text-agua-700 underline underline-offset-2">Mapa de hoy</Link>.</>}
        </Accion>
        <Accion Icono={IconoTelefono} tono="bg-barro-100 text-barro-700" titulo="Pide una pipa por TlaqueChat">
          WhatsApp del ayuntamiento: <b className="text-tinta">33 2804 8171</b>, de 7:00 a 22:00.
        </Accion>
        <Accion Icono={IconoGota} tono="bg-agua-50 text-agua-700" titulo="Cloro al agua guardada">
          <span>Si lleva más de 2 días guardada: <b className="text-tinta">2 gotas de cloro sin aroma por litro</b> (8 por galón) y reposar 30 min.{" "}
            <Info etiqueta="De dónde sale la dosis" className="ml-1">Fuente: CDC. Con cloro de 8.25 % usa menos: lee la etiqueta de tu botella.</Info>
          </span>
        </Accion>
      </ul>
    </section>
  );
}
