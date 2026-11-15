"use client";
import { useState } from "react";
import { Antetitulo, IconoGota, Info } from "@/ui";
import type { ResultadoCasa } from "../calculos";
import { enlaceWhatsApp, mensajeCompartir, recordatorioICS } from "../enlaces";

const boton = "inline-flex min-h-11 items-center justify-center rounded-full px-4 text-sm font-bold transition-colors";

function descarga(nombre: string, contenido: string) {
  const url = URL.createObjectURL(new Blob([contenido], { type: "text/calendar;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url; a.download = nombre;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** Dos cosas que sí funcionan hoy sin servidor: un recordatorio en el calendario y avisarle a los vecinos por WhatsApp. */
export function Avisos({ r, consultado }: { r: ResultadoCasa; consultado: string }) {
  const [listo, setListo] = useState(false);
  const hayDiasSinAgua = r.semana.some((x) => x.seca);

  function recordar() {
    const ics = recordatorioICS(r, consultado);
    if (!ics) return;
    descarga("aguanta-recordatorio.ics", ics);
    setListo(true);
  }
  function compartir() {
    const url = window.location.href.split("#")[0];
    window.open(enlaceWhatsApp(mensajeCompartir(r, url)), "_blank", "noopener,noreferrer");
  }

  return (
    <section>
      <Antetitulo className="mb-2">Que no te agarre desprevenido</Antetitulo>
      <div className="space-y-3 rounded-2xl bg-white p-4 shadow-suave">
        {hayDiasSinAgua && (
          <div>
            <div className="flex items-start gap-3">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-agua-50 text-agua-700"><IconoGota className="h-6 w-6" /></span>
              <div className="min-w-0 text-sm leading-relaxed text-tinta-suave">
                <div className="font-display font-bold text-tinta">Recordatorio la noche anterior</div>
                Te avisa a las 7 de la noche, el día antes de cada día sin agua, para llenar tinaco y cubetas.{" "}
                <Info etiqueta="Cómo funciona el recordatorio" className="ml-1">
                  Descargas un archivo y lo abres con tu calendario. Se repite 4 semanas según el calendario del SIAPA, que puede cambiar: si cambia, vuelve a calcularlo aquí.
                </Info>
              </div>
            </div>
            <button type="button" onClick={recordar} className={`${boton} mt-3 w-full bg-agua-600 text-white hover:bg-agua-700`}>Agregar a mi calendario</button>
            {listo && <p role="status" className="mt-2 text-xs font-semibold text-agua-700">Listo: abre el archivo descargado para agregarlo a tu calendario.</p>}
          </div>
        )}
        <div className={hayDiasSinAgua ? "border-t border-tinta/10 pt-3" : ""}>
          <div className="font-display font-bold">Avísale a tus vecinos</div>
          <p className="text-sm leading-relaxed text-tinta-suave">Manda por WhatsApp el cálculo de tu colonia y el enlace de esta página.</p>
          <button type="button" onClick={compartir} className={`${boton} mt-3 w-full bg-agua-50 text-agua-800 hover:bg-agua-100`}>Compartir por WhatsApp</button>
        </div>
      </div>
    </section>
  );
}
