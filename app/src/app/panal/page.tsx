"use client";
// Mapa de hoy: ¿quién se queda sin agua hoy? Un héroe (la tarjeta del día), el mapa y el detalle detrás de un toque.
import dynamic from "next/dynamic";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useReal, calcular } from "@/lib/real";
import type { SupuestosMotor } from "@/lib/motor";
import { puntosCisternas } from "@/components/HexMap";
import { BotonPildora, Cargando, ETAPAS_MAPA, Consejo, IconoAjustes, IconoCapas } from "@/ui";
import { nivelesSemana, riesgoZonas56 } from "@/features/mapa/calculos";
import { TarjetaHoy } from "@/features/mapa/components/TarjetaHoy";
import { Leyenda } from "@/features/mapa/components/Leyenda";
import { MenuCapas, type Capas } from "@/features/mapa/components/MenuCapas";
import { HojaSupuestos } from "@/features/mapa/components/HojaSupuestos";
import { HojaHexagono } from "@/features/mapa/components/HojaHexagono";

const HexMap = dynamic(() => import("@/components/HexMap"), { ssr: false, loading: () => <Cargando etapas={ETAPAS_MAPA} etapa={2} sinMascota /> });

export default function MapaDeHoy() {
  const d = useReal();
  const [fecha, setFecha] = useState("2026-11-12");
  const [tresD, setTresD] = useState(true);
  const [capas, setCapas] = useState<Capas>({ modo: "agua", cisternas: true, propuestas: false, nucleo: false, version: "vigente" });
  const [sel, setSel] = useState<string | null>(null);
  const [s, setS] = useState<SupuestosMotor | null>(null);
  const [verCapas, setVerCapas] = useState(false);
  const [verAjustes, setVerAjustes] = useState(false);
  const [consejo, setConsejo] = useState(true); // el consejo de la mascota se va al cerrarlo o al tocar un hexágono

  // Se deja pintar la etapa «Calculando» antes del cálculo, que bloquea la pantalla un momento.
  const [listo, setListo] = useState(!!d);
  useEffect(() => { if (!d) return; const t = setTimeout(() => setListo(true), 60); return () => clearTimeout(t); }, [d]);

  const sup = s ?? d?.meta.supuestos ?? null;
  const cal = d?.calendarios[capas.version];
  const res = useMemo(() => (d && listo && cal && sup ? calcular(d, cal, fecha, sup) : null), [d, listo, cal, fecha, sup]);
  const dias = useMemo(() => (d && listo && cal && sup ? nivelesSemana(d, cal, sup) : []), [d, listo, cal, sup]);
  const z56 = useMemo(() => (d && listo ? riesgoZonas56(d) : null), [d, listo]);
  const nNucleo = useMemo(() => d?.manzanas.filter((m) => m.nucleo_robusto).length ?? 0, [d]);
  const resaltar = useMemo(() => (capas.nucleo && res ? new Set(res.celdas.filter((c) => c.nucleo > 0).map((c) => c.h3)) : undefined), [capas.nucleo, res]);
  const puntos = useMemo(() => (d && capas.cisternas ? puntosCisternas(d.cisternas, capas.propuestas) : []), [d, capas.cisternas, capas.propuestas]);
  const cerrarHex = useCallback(() => setSel(null), []);
  const cerrarCapas = useCallback(() => setVerCapas(false), []);
  const cerrarAjustes = useCallback(() => setVerAjustes(false), []);

  if (!d || !cal || !sup || !res) return <Cargando etapas={ETAPAS_MAPA} etapa={d ? 1 : 0} />;
  const dia = cal.dias.find((x) => x.fecha === fecha);
  const nCisternas = d.cisternas.filter((c) => c.tipo !== "propuesta_municipio").length;

  return (
    <div className="md:relative md:h-[calc(100vh-3.5rem)]">
      <div className="relative z-0 h-[60vh] md:absolute md:inset-0 md:h-auto">
        <HexMap margenIzq={380} celdas={res.celdas} puntos={puntos} tresD={tresD} modo={capas.modo} seleccion={sel} onSeleccion={setSel} resaltar={resaltar} />
        <div className="absolute left-3 top-3 z-10 flex gap-2 md:left-auto md:right-14 md:top-4">
          <BotonPildora onClick={() => setVerCapas(true)}><IconoCapas className="h-4 w-4" />Capas</BotonPildora>
          <BotonPildora onClick={() => setTresD(!tresD)} titulo={tresD ? "Ver el mapa plano" : "Ver el mapa en 3D"}>{tresD ? "2D" : "3D"}</BotonPildora>
          <BotonPildora onClick={() => setVerAjustes(true)}><IconoAjustes className="h-4 w-4" />Ajustar</BotonPildora>
        </div>
        {consejo && !sel && (
          <div className="absolute left-3 right-16 top-14 z-10 md:bottom-4 md:left-auto md:right-4 md:top-auto md:w-64">
            <Consejo cara="h-14" onCerrar={() => setConsejo(false)}>Toca un hexágono para ver el detalle de esa zona.</Consejo>
          </div>
        )}
        <Leyenda modo={capas.modo} className="absolute bottom-9 left-3 z-10 md:bottom-4 md:left-[24.5rem]" />
      </div>

      <TarjetaHoy className="relative z-10 mx-3 -mt-6 mb-4 md:absolute md:left-4 md:top-4 md:m-0 md:max-h-[calc(100%-2rem)] md:w-[22.5rem] md:overflow-y-auto"
        fecha={fecha} dias={dias} onFecha={setFecha} r={res.resumen} zonasHoy={dia?.zonas_sin_servicio.join(", ") || "ninguna"}
        z56={z56} uHoras={sup.u_horas_agua_guardada} original={capas.version === "original"} />

      <HojaHexagono d={d} c={res.celdas.find((x) => x.h3 === sel)} onCerrar={cerrarHex} />
      <MenuCapas abierto={verCapas} onCerrar={cerrarCapas} capas={capas} onCapas={setCapas} nCisternas={nCisternas} nNucleo={nNucleo} />
      <HojaSupuestos abierta={verAjustes} onCerrar={cerrarAjustes} s={sup} onCambio={setS} cambiado={!!s} onRestablecer={() => setS(null)} advertencias={d.meta.advertencias} />
    </div>
  );
}
