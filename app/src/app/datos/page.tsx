"use client";
// Cómo funciona: cuatro pasos, seis hallazgos y de dónde sale cada dato. Las cuentas viven en features/datos/calculos.ts.
import { useMemo } from "react";
import { fmt, useReal } from "@/lib/real";
import { Aclaraciones, Antetitulo, Cargando } from "@/ui";
import { calcularDatos } from "@/features/datos/calculos";
import { CifrasDatos } from "@/features/datos/components/CifrasDatos";
import { Colonias } from "@/features/datos/components/Colonias";
import { Equidad } from "@/features/datos/components/Equidad";
import { Fuentes } from "@/features/datos/components/Fuentes";
import { GraficaCalendarios } from "@/features/datos/components/GraficaCalendarios";
import { GraficaSensibilidad } from "@/features/datos/components/GraficaSensibilidad";
import { GraficaZonas } from "@/features/datos/components/GraficaZonas";
import { PasosComoFunciona } from "@/features/datos/components/PasosComoFunciona";
import { Sello } from "@/features/datos/components/Sello";

export default function Datos() {
  const d = useReal();
  const g = useMemo(() => (d ? calcularDatos(d) : null), [d]);
  if (!d || !g) return <Cargando texto="Calculando con el motor oficial…" />;
  const s = d.meta.supuestos;
  const cuenta = [
    "Cada manzana se parte en estratos: con tinaco y cisterna, solo tinaco, solo cisterna, nada. El Censo no los cruza, así que el número de viviendas con ambos va en un intervalo, y todo resultado sale como cota mínima y máxima.",
    "Autonomía de un estrato = litros ÷ (ocupantes × consumo × (1 − f)) × 24 h. Sin almacenamiento = 0 h.",
    `Horas sin servicio: el primer día de racionamiento cuenta ${s.horas_efectivas_corte} h y cada día seguido suma 24. Con varias zonas, el intervalo se ensancha.`,
    "Un estrato se queda sin agua si su autonomía es menor que esas horas.",
    `Si aguanta pero el agua lleva más de ${s.u_horas_agua_guardada} h guardada, hay que desinfectarla.`,
  ];

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-4 md:p-6">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div className="max-w-2xl">
          <Antetitulo>Cómo funciona</Antetitulo>
          <h1 className="mt-1 text-3xl font-bold leading-tight md:text-4xl">Cómo calculamos cuánta agua te queda</h1>
          <p className="mt-2 text-tinta-suave">Todo se calcula en tu navegador, a partir de {fmt(d.meta.conteos.manzanas)} manzanas reales. Cada cifra sale como un rango (mínimo y máximo) porque el Censo no lo dice todo.</p>
        </div>
        <Sello />
      </header>

      <PasosComoFunciona />
      <Aclaraciones titulo="La cuenta paso a paso" resumen={`${cuenta.length} puntos`} lista={cuenta}>
        <p>Detalle completo en <code className="rounded bg-white px-1.5 py-0.5 text-[0.85em]">motor/ESPECIFICACION.md</code>.</p>
      </Aclaraciones>

      <CifrasDatos d={d} g={g} />

      <div className="grid gap-6 md:grid-cols-2">
        <GraficaCalendarios g={g} />
        <GraficaSensibilidad g={g} />
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <GraficaZonas g={g} />
        <Equidad g={g} />
      </div>
      <Colonias g={g} />

      <Fuentes d={d} />
      <Aclaraciones titulo="Qué tener en cuenta al leer estos números" resumen={`${d.meta.advertencias.length} avisos`} lista={d.meta.advertencias} />
    </main>
  );
}
