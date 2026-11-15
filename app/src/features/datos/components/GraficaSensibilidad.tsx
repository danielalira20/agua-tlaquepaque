"use client";
import { useEffect, useRef, useState } from "react";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fmt, type Datos } from "@/lib/real";
import { sensibilidadCalculada, type Sensibilidad } from "../calculos";
import { COLOR, PanelGrafica, miles } from "./PanelGrafica";

/** Cuánto cambia el resultado si cambian el consumo y el agua que sí llega (f). Se calcula al acercarse a la pantalla. */
export function GraficaSensibilidad({ d }: { d: Datos }) {
  const caja = useRef<HTMLDivElement>(null);
  const [datos, setDatos] = useState<Sensibilidad | null>(null);
  useEffect(() => {
    const el = caja.current; if (!el) return;
    let vivo = true;
    const pedir = () => { sensibilidadCalculada(d).then((r) => { if (vivo) setDatos(r); }); };
    if (typeof IntersectionObserver === "undefined") { pedir(); return () => { vivo = false; }; }
    const o = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { o.disconnect(); pedir(); } }, { rootMargin: "400px" });
    o.observe(el);
    return () => { vivo = false; o.disconnect(); };
  }, [d]);
  return (
    <PanelGrafica
      hallazgo="Lo que más mueve el resultado es cuánta agua se gasta, no cuánta llega"
      nota="Personas-día sin agua en la semana (cota mínima). A 50 L por persona, f casi no cambia nada: quien no tiene dónde guardar se seca igual.">
      <div ref={caja} className="h-[250px]">
        {datos ? (
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={datos} margin={{ left: -10, right: 8 }}><CartesianGrid stroke={COLOR.rejilla} vertical={false} /><XAxis dataKey="consumo" fontSize={11} stroke={COLOR.texto} /><YAxis fontSize={11} tickFormatter={miles} stroke={COLOR.texto} /><Tooltip formatter={(v: number) => fmt(v)} /><Legend />
              <Line dataKey="f0" name="f = 0 (corte total)" stroke={COLOR.barro} strokeWidth={2.5} dot={false} />
              <Line dataKey="f0.25" name="f = 25 %" stroke={COLOR.aguaMedio} strokeWidth={2.5} strokeDasharray="6 3" dot={false} />
              <Line dataKey="f0.5" name="f = 50 %" stroke={COLOR.agua} strokeWidth={2.5} strokeDasharray="2 3" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="grid h-full animate-pulse place-items-center rounded-2xl bg-crema-2 text-sm font-semibold text-tinta-suave">Calculando con el motor…</div>
        )}
      </div>
    </PanelGrafica>
  );
}
