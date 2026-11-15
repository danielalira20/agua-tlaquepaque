"use client";
import { Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fmt } from "@/lib/real";
import { textoRango } from "@/ui";
import type { DatosCalculados } from "../calculos";
import { COLOR, PanelGrafica, miles } from "./PanelGrafica";

/** Personas sin agua por día con el calendario vigente contra el original. */
export function GraficaCalendarios({ g }: { g: DatosCalculados }) {
  const x = (a: number, b: number) => (a / b).toLocaleString("es-MX", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  const lo = x(g.sem.vig.min, g.sem.ori.min), hi = x(g.sem.vig.max, g.sem.ori.max);
  const veces = lo === hi ? `×${lo}` : `×${lo} – ×${hi}`;
  return (
    <PanelGrafica
      hallazgo={<>El calendario vigente deja sin agua a <span className="text-barro-600">{veces}</span> más personas que el original</>}
      nota={<>Personas-día sin agua en la semana: {textoRango(g.sem.vig.min, g.sem.vig.max)} con el vigente. La banda va de la cota mínima a la máxima.</>}>
      <ResponsiveContainer width="100%" height={250}>
        <AreaChart data={g.porDia} margin={{ left: -10, right: 8 }}><CartesianGrid stroke={COLOR.rejilla} vertical={false} /><XAxis dataKey="dia" fontSize={11} stroke={COLOR.texto} /><YAxis fontSize={11} tickFormatter={miles} stroke={COLOR.texto} />
          <Tooltip formatter={(v: any) => (Array.isArray(v) ? `${fmt(v[0])} – ${fmt(v[1])}` : v)} /><Legend />
          <Area dataKey="original" name="Original (15-oct)" stroke={COLOR.aguaMedio} fill={COLOR.aguaClaro} fillOpacity={0.55} />
          <Area dataKey="vigente" name="Vigente (4-nov)" stroke={COLOR.barro} fill={COLOR.barro} fillOpacity={0.3} />
        </AreaChart>
      </ResponsiveContainer>
    </PanelGrafica>
  );
}
