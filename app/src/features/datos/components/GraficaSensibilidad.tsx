"use client";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fmt } from "@/lib/real";
import type { DatosCalculados } from "../calculos";
import { COLOR, PanelGrafica, miles } from "./PanelGrafica";

/** Cuánto cambia el resultado si cambian el consumo y el agua que sí llega (f). */
export function GraficaSensibilidad({ g }: { g: DatosCalculados }) {
  return (
    <PanelGrafica
      hallazgo="Lo que más mueve el resultado es cuánta agua se gasta, no cuánta llega"
      nota="Personas-día sin agua en la semana (cota mínima). A 50 L por persona, f casi no cambia nada: quien no tiene dónde guardar se seca igual.">
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={g.sens} margin={{ left: -10, right: 8 }}><CartesianGrid stroke={COLOR.rejilla} vertical={false} /><XAxis dataKey="consumo" fontSize={11} stroke={COLOR.texto} /><YAxis fontSize={11} tickFormatter={miles} stroke={COLOR.texto} /><Tooltip formatter={(v: number) => fmt(v)} /><Legend />
          <Line dataKey="f0" name="f = 0 (corte total)" stroke={COLOR.barro} strokeWidth={2.5} dot={false} />
          <Line dataKey="f0.25" name="f = 25 %" stroke={COLOR.aguaMedio} strokeWidth={2.5} strokeDasharray="6 3" dot={false} />
          <Line dataKey="f0.5" name="f = 50 %" stroke={COLOR.agua} strokeWidth={2.5} strokeDasharray="2 3" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </PanelGrafica>
  );
}
