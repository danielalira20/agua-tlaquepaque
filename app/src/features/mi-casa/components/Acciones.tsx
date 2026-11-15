"use client";
import { useState } from "react";
import Link from "next/link";
import { Antetitulo, IconoCisterna, IconoGota, IconoTelefono, Info } from "@/ui";
import type { ResultadoCasa } from "../calculos";
import { TLAQUECHAT, mensajePipa } from "../enlaces";

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
export function Acciones({ r, personas }: { r: ResultadoCasa; personas: number }) {
  const colonia = r.col.nombre, cisternas = r.cis;
  const [copiado, setCopiado] = useState(false);

  async function copiarMensaje() {
    try {
      await navigator.clipboard.writeText(mensajePipa(r, personas));
      setCopiado(true);
      setTimeout(() => setCopiado(false), 4000);
    } catch { /* portapapeles no disponible (navegador o permisos): el botón simplemente no confirma */ }
  }

  return (
    <section>
      <Antetitulo className="mb-2">Si te quedas sin agua</Antetitulo>
      <ul className="space-y-2">
        <Accion Icono={IconoCisterna} tono="bg-agua-100 text-agua-700" titulo={cisternas > 0 ? `${cisternas} ${cisternas === 1 ? "cisterna" : "cisternas"} en ${colonia}` : `Sin cisterna comunitaria en ${colonia}`}>
          {cisternas > 0 ? "Cisternas comunitarias de tu colonia." : <>Busca cisternas de colonias vecinas en el <Link href="/panal" className="font-semibold text-agua-700 underline underline-offset-2">Mapa de hoy</Link>.</>}
        </Accion>
        <Accion Icono={IconoTelefono} tono="bg-barro-100 text-barro-700" titulo="Pide una pipa por TlaqueChat">
          <span>
            {TLAQUECHAT.nombre} es el WhatsApp del ayuntamiento para pedir pipas.{" "}
            <Info etiqueta="Por qué no hay número aquí" className="ml-1">
              Confirmamos que TlaqueChat existe (nota de prensa leída completa), pero no su número: dos notas oficiales
              publican cifras que difieren en un dígito, así que no lo citamos hasta confirmarlo con el municipio.
            </Info>
          </span>
          <button type="button" onClick={copiarMensaje}
            className="mt-3 flex min-h-11 w-full items-center justify-center rounded-full bg-agua-600 px-4 text-sm font-bold text-white transition-colors hover:bg-agua-700">
            {copiado ? "Copiado: pégalo en TlaqueChat" : "Copiar mensaje para pedir pipa"}
          </button>
        </Accion>
        <Accion Icono={IconoGota} tono="bg-agua-50 text-agua-700" titulo="Cloro al agua guardada">
          <span>Si lleva más de 2 días guardada: <b className="text-tinta">2 gotas de cloro sin aroma por litro</b> (8 por galón) y reposar 30 min.{" "}
            <Info etiqueta="De dónde sale la dosis" className="ml-1">Fuente: CDC, para cloro sin aroma de 5 a 9 %.</Info>
          </span>
        </Accion>
      </ul>
    </section>
  );
}
