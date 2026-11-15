"use client";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fmt } from "@/lib/real";
import type { DatosCalculados } from "../calculos";
import { COLOR, PanelGrafica, miles } from "./PanelGrafica";

/** Dónde están las casas sin tinaco ni cisterna: por zona de racionamiento. */
export function GraficaZonas({ g }: { g: DatosCalculados }) {
  const p = (n: number) => n.toLocaleString("es-MX", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  return (
    <PanelGrafica
      hallazgo={<>Las zonas 5 y 6 concentran entre <span className="text-barro-600">{p(g.peso56.max)} % y {p(g.peso56.min)} %</span> de las casas sin tinaco ni cisterna</>}
      nota="Solo manzanas dentro del programa. Barra oscura: cota mínima; clara: hasta la máxima. Entre las dos cotas siempre es más de la mitad."
      tipo="real">
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={g.porZona} layout="vertical" margin={{ left: 0, right: 8 }}><CartesianGrid stroke={COLOR.rejilla} horizontal={false} /><XAxis type="number" fontSize={11} tickFormatter={miles} stroke={COLOR.texto} /><YAxis type="category" dataKey="zona" fontSize={11} width={78} stroke={COLOR.texto} /><Tooltip formatter={(v: number) => fmt(v)} />
          <Bar dataKey="minimo" name="cota mínima" stackId="a" fill={COLOR.barro} /><Bar dataKey="rango" name="hasta la máxima" stackId="a" fill={COLOR.barroClaro} />
        </BarChart>
      </ResponsiveContainer>
    </PanelGrafica>
  );
}
