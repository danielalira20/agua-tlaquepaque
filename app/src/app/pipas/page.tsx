"use client";
// Plan de pipas: ¿a dónde mando las pipas hoy? Paradas del día, una comparación en una imagen y los límites del plan en un desplegable.
import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";
import { latLngToCell } from "h3-js";
import { useReal, calcular, fechaInicial, fechaLarga } from "@/lib/real";
import { puntosCisternas, type Punto, type Rotulo } from "@/components/HexMap";
import { Antetitulo, Cargando, ETAPAS_MAPA, Etiqueta, Info, SemanaGotas, Segmentado, textoRango } from "@/ui";
import { diaDe, paradas, semanaDe, type Cota } from "@/features/pipas/plan";
import { Comparacion } from "@/features/pipas/components/Comparacion";
import { ListaParadas } from "@/features/pipas/components/ListaParadas";
import { Limites } from "@/features/pipas/components/Limites";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false, loading: () => <Cargando etapas={ETAPAS_MAPA} etapa={2} sinMascota /> });

export default function PlanDePipas() {
  const d = useReal();
  const [fechaElegida, setFecha] = useState<string | null>(null);
  const fecha = fechaElegida ?? (d ? fechaInicial(d) : "");
  const [cota, setCota] = useState<Cota>("min");
  const [sel, setSel] = useState<string | null>(null);
  const [selN, setSelN] = useState<number | null>(null);

  // Se deja pintar la etapa «Calculando» antes del cálculo, que bloquea la pantalla un momento.
  const [listo, setListo] = useState(!!d);
  useEffect(() => { if (!d) return; const t = setTimeout(() => setListo(true), 60); return () => clearTimeout(t); }, [d]);

  const cal = d?.calendarios.vigente;
  const res = useMemo(() => (d && listo && cal ? calcular(d, cal, fecha, d.meta.supuestos) : null), [d, listo, cal, fecha]);
  const hoy = d ? diaDe(d.plan, "priorizado", cota, fecha) : undefined;
  const viajes = useMemo(() => hoy?.viajes ?? [], [hoy]);
  const lista = useMemo(() => paradas(viajes), [viajes]);
  const resaltar = useMemo(() => new Set(viajes.map((v) => latLngToCell(v.lat, v.lon, 8))), [viajes]);
  const puntos: Punto[] = useMemo(() => [
    ...(d ? puntosCisternas(d.cisternas, false) : []),
    ...viajes.map((v) => ({ id: `v${v.orden_eleccion}`, lon: v.lon, lat: v.lat, tipo: "pipa" as const, texto: `Pipa · ${v.colonia} · ${v.viviendas_objetivo} casas` })),
  ], [d, viajes]);
  const encuadre = useMemo(() => lista.map((p) => [p.lon, p.lat] as [number, number]), [lista]);
  const rotulos: Rotulo[] = useMemo(() => lista.map((p) => ({ id: `p${p.n}`, lon: p.lon, lat: p.lat, texto: String(p.n) })), [lista]);
  // gota de cada día: qué parte de las casas sin agua alcanzan las pipas (plan priorizado, cota elegida)
  const gotas = useMemo(() => (d && cal ? cal.dias.map((x) => {
    const r = diaDe(d.plan, "priorizado", cota, x.fecha)?.resumen;
    return { fecha: x.fecha, dia: x.dia, nivel: (r?.cobertura_pct ?? 0) / 100, nota: r ? `Las pipas llegan al ${r.cobertura_pct.toFixed(0)} % de las casas sin agua` : undefined };
  }) : []), [d, cal, cota]);

  if (!d || !cal || !res || !hoy) return <Cargando etapas={ETAPAS_MAPA} etapa={d ? 1 : 0} />;
  const at = (regla: "priorizado" | "baseline", c: Cota) => diaDe(d.plan, regla, c, fecha)!.resumen;
  const sMin = semanaDe(d.plan, "min"), sMax = semanaDe(d.plan, "max");

  return (
    <div className="md:grid md:h-[calc(100vh-3.5rem)] md:grid-cols-[1fr_28rem]">
      <div className="relative z-0 h-[50vh] md:h-auto">
        <HexMap encuadre={encuadre} celdas={res.celdas} puntos={puntos} rotulos={rotulos} tresD={false} resaltar={resaltar} seleccion={sel} onSeleccion={(h) => { setSel(h); setSelN(null); }} />
        <div className="absolute left-3 right-14 top-3 z-10 flex flex-wrap items-center gap-x-3 gap-y-1 rounded-2xl md:right-auto bg-white/95 px-3 py-2 text-[11px] text-tinta-suave shadow-suave backdrop-blur">
          <span className="flex items-center gap-1.5"><span className="grid h-4 w-5 place-items-center rounded-md bg-agua-700 text-[9px] font-bold text-white">1</span>parada</span>
          <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-orange-500" />cisterna</span>
          <span>hexágono resaltado = recibe pipa</span>
        </div>
      </div>

      <aside className="space-y-4 bg-crema p-4 md:overflow-y-auto md:overflow-x-hidden md:border-l md:border-tinta/10 md:p-5">
        <section className="aparecer">
          <div className="flex items-center justify-between"><Antetitulo>Plan de pipas</Antetitulo><Etiqueta tipo="estimado" /></div>
          <h1 className="mt-1 text-2xl font-bold first-letter:uppercase">{fechaLarga(fecha)}</h1>
          <p className="text-sm text-tinta-suave">{hoy.resumen.viajes_usados} viajes · {lista.length} colonias · casas sin agua en el programa: {textoRango(at("priorizado", "min").necesidad_total, at("priorizado", "max").necesidad_total)}</p>
          <SemanaGotas className="mt-3" dias={gotas} valor={fecha} onCambio={(f) => { setFecha(f); setSel(null); setSelN(null); }} />
          <div className="mt-3 flex items-center gap-2">
            <Segmentado className="flex-1" valor={cota} onCambio={(c) => { setCota(c); setSel(null); setSelN(null); }}
              opciones={[{ valor: "min", texto: "Seguro secas" }, { valor: "max", texto: "Posiblemente secas" }]} />
            <Info etiqueta="Qué cambia este botón">El plan se puede ordenar por las casas que <b>seguro</b> están sin agua (cota mínima) o por las que <b>podrían</b> estarlo (cota máxima). Cambia a dónde van las pipas; la comparación de abajo muestra siempre las dos.</Info>
          </div>
        </section>

        <Comparacion viajes={hoy.resumen.viajes_usados}
          pri={[at("priorizado", "min").viviendas_atendidas, at("priorizado", "max").viviendas_atendidas]}
          base={[at("baseline", "min").viviendas_atendidas, at("baseline", "max").viviendas_atendidas]}
          semPri={[sMin.viviendas_atendidas.priorizado, sMax.viviendas_atendidas.priorizado]}
          semBase={[sMin.viviendas_atendidas.baseline, sMax.viviendas_atendidas.baseline]} />

        <section>
          <h2 className="mb-2 text-base font-bold">Paradas de hoy ({lista.length})</h2>
          <ListaParadas paradas={lista} seleccion={selN} onElegir={(p) => { setSel(latLngToCell(p.lat, p.lon, 8)); setSelN(p.n); }} />
        </section>

        <Limites p={d.plan.parametros} />
      </aside>
    </div>
  );
}
