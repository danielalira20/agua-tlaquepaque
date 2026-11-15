import { BarraRango, Info, textoRango } from "@/ui";

/** Las mismas pipas, dos formas de repartirlas: una sola imagen y una frase. */
export function Comparacion({ pri, base, viajes, semPri, semBase }: {
  pri: [number, number]; base: [number, number]; viajes: number; semPri: [number, number]; semBase: [number, number];
}) {
  const escala = Math.max(pri[1], base[1]) * 1.05;
  const razones = [pri[0] / Math.max(1, base[0]), pri[1] / Math.max(1, base[1])].sort((a, b) => a - b);
  const r = (x: number) => x.toLocaleString("es-MX", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  return (
    <section className="rounded-2xl bg-white p-4 shadow-suave">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-base font-bold">Las mismas {viajes} pipas, dos repartos</h2>
        <Info etiqueta="Cómo se compara">
          <p className="font-semibold">Los dos repartos usan los mismos viajes.</p>
          <ul className="mt-2 space-y-2">
            <li><b>Primero donde más casas están secas:</b> el plan del priorizador.</li>
            <li><b>Por turnos:</b> un baseline estilizado. Los viajes rotan entre las cisternas instaladas; no es lo que hace hoy el municipio.</li>
          </ul>
          <p className="mt-3 border-t border-white/20 pt-3 font-semibold">En la semana, priorizar atiende:</p>
          <ul className="mt-1 list-disc space-y-1 pl-5">
            <li>de <b>1.9 a 4.9 veces</b> lo del reparto por turnos;</li>
            <li>de <b>1.1 a 3.1 veces</b> lo de un reparto que solo visita las cisternas con necesidad ese día.</li>
          </ul>
          <p className="mt-2 text-xs text-white/70">Es el rango de cuatro escenarios (el caso base y tres esquinas de supuestos) con las dos cotas. En el caso base, contra el reparto por turnos: 4.9 veces con la cota mínima y 2.2 con la máxima. Gana menos cuando casi todo el municipio se queda sin agua.</p>
        </Info>
      </div>
      <div className="mt-4 space-y-4">
        <div>
          <div className="mb-1 text-sm font-semibold text-agua-700">Primero donde más casas están secas</div>
          <BarraRango tam="md" tono="agua" min={pri[0]} max={pri[1]} total={escala} />
        </div>
        <div>
          <div className="mb-1 text-sm font-semibold text-tinta-suave">Por turnos entre cisternas</div>
          <BarraRango tam="md" tono="neutro" min={base[0]} max={base[1]} total={escala} />
        </div>
      </div>
      <p className="mt-3 text-xs text-tinta-suave">casas sin agua que reciben pipa hoy</p>
      <div className="mt-3 rounded-xl bg-agua-50 p-3 text-agua-900">
        <div className="text-xs font-semibold uppercase tracking-wide text-agua-700">Hoy, priorizar llega a</div>
        <div className="font-display text-2xl font-bold">{r(razones[0])} – {r(razones[1])} veces <span className="text-base font-semibold">las casas del reparto por turnos</span></div>
        <dl className="mt-2 space-y-1 border-t border-agua-100 pt-2 text-sm">
          <div className="flex flex-wrap justify-between gap-x-3"><dt className="text-agua-700">En la semana, priorizar</dt><dd className="font-bold">{textoRango(semPri[0], semPri[1])} casas</dd></div>
          <div className="flex flex-wrap justify-between gap-x-3"><dt className="text-tinta-suave">En la semana, por turnos</dt><dd className="font-bold text-tinta-suave">{textoRango(semBase[0], semBase[1])} casas</dd></div>
        </dl>
        <p className="mt-1 text-xs text-tinta-suave">Cada casa cuenta una vez por día.</p>
      </div>
    </section>
  );
}
