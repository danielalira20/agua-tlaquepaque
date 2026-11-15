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
          Los dos repartos usan los mismos viajes. El <b>reparto por turnos</b> es un <b>baseline estilizado</b>: los viajes rotan entre las cisternas instaladas; no es lo que hace hoy el municipio. En 120 simulaciones con otros supuestos, priorizar atiende entre 2.6 y 4.9 veces lo del reparto por turnos; contra un reparto que solo visita las cisternas con necesidad ese día, la ventaja va de 1.1 a 3.1 veces, según la cota y el escenario.
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
      <p className="mt-3 rounded-xl bg-agua-50 p-3 text-sm text-agua-900">
        Hoy, priorizar llega a <b>{r(razones[0])} – {r(razones[1])} veces</b> más casas que el reparto por turnos. En la semana suma <b>{textoRango(semPri[0], semPri[1])}</b> casas atendidas contra {textoRango(semBase[0], semBase[1])} (cada casa cuenta una vez por día). Sin pedir más agua ni más pipas.
      </p>
    </section>
  );
}
