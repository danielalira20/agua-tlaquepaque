"use client";
import { useMemo } from "react";
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useDatos } from "@/lib/datos";
import { estadoColonia, resumenDia, SUPUESTOS, fmt } from "@/lib/modelo";
import { Badge, Tarjeta } from "@/components/ui";

const AZUL = "#1d4ed8", CLARO = "#93c5fd", GRIS = "#94a3b8";

export default function Datos() {
  const datos = useDatos();
  const g = useMemo(() => {
    if (!datos) return null;
    const dias = datos.calendarios.noviembre.dias.filter((d) => d.fecha >= "2026-11-09" && d.fecha <= "2026-11-22");
    const porDia = dias.map((d) => {
      const fila: Record<string, number | string> = { dia: d.fecha.slice(5) };
      for (const v of ["octubre", "noviembre"] as const) fila[v] = resumenDia(datos.colonias.map((c) => estadoColonia(c, datos.calendarios[v], d.fecha, SUPUESTOS))).personas_sin_agua;
      return fila;
    });
    const sens = [50, 75, 100, 125, 150].map((consumo) => {
      const est = datos.colonias.map((c) => estadoColonia(c, datos.calendarios.noviembre, "2026-11-12", { ...SUPUESTOS, consumo }));
      const porEstrato = (n: string) => est.reduce((s, e) => s + (e.estratos.find((x) => x.nombre === n)?.seca ? e.estratos.find((x) => x.nombre === n)!.viviendas : 0), 0);
      return { consumo: `${consumo} L`, "Sin almacenamiento": porEstrato("Sin almacenamiento"), "Con tinaco": porEstrato("Con tinaco"), "Con cisterna": porEstrato("Con cisterna") };
    });
    const tot = datos.colonias.reduce((a, c) => ({ viv: a.viv + c.viviendas, sin: a.sin + c.viv_sin_almacen, tin: a.tin + c.viv_tinaco, cis: a.cis + c.viv_cisterna, pob: a.pob + c.pob }), { viv: 0, sin: 0, tin: 0, cis: 0, pob: 0 });
    const top = [...datos.colonias].sort((a, b) => b.viv_sin_almacen / b.viviendas - a.viv_sin_almacen / a.viviendas).slice(0, 10);
    return { porDia, sens, tot, top };
  }, [datos]);
  if (!g) return <div className="p-10 text-slate-500">Cargando…</div>;

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold">Datos y modelo</h1>
        <p className="text-sm text-slate-600">Todo lo que ves en el Panal sale de aquí. Las cifras de colonias son <Badge tipo="simulado" /> hasta que entren las reales; la estructura y el método son los definitivos.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Tarjeta><div className="text-2xl font-bold">{fmt(g.tot.pob)}</div><div className="text-sm text-slate-600">personas en {datos!.colonias.length} colonias</div></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">{((g.tot.sin / g.tot.viv) * 100).toFixed(0)} %</div><div className="text-sm text-slate-600">viviendas sin tinaco ni cisterna</div></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">{((g.tot.tin / g.tot.viv) * 100).toFixed(0)} %</div><div className="text-sm text-slate-600">solo tinaco (1,100 L)</div></Tarjeta>
        <Tarjeta><div className="text-2xl font-bold">{((g.tot.cis / g.tot.viv) * 100).toFixed(0)} %</div><div className="text-sm text-slate-600">con cisterna (5,000 L)</div></Tarjeta>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Tarjeta>
          <h2 className="font-semibold">Personas sin agua por día: calendario de octubre vs. noviembre</h2>
          <p className="mb-2 text-xs text-slate-500">Cuando el SIAPA pasó de 2 a 3 días de suspensión, esto es lo que cambió.</p>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={g.porDia}><CartesianGrid stroke="#e2e8f0" /><XAxis dataKey="dia" fontSize={11} /><YAxis fontSize={11} tickFormatter={(v) => `${v / 1000}k`} /><Tooltip formatter={(v: number) => fmt(v)} /><Legend />
              <Line type="monotone" dataKey="octubre" stroke={CLARO} strokeWidth={2} dot={false} /><Line type="monotone" dataKey="noviembre" stroke={AZUL} strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </Tarjeta>
        <Tarjeta>
          <h2 className="font-semibold">Sensibilidad al consumo: quién se seca el jueves 12</h2>
          <p className="mb-2 text-xs text-slate-500">A 50 L/persona/día solo se seca quien no tiene dónde guardar. A 100–150 L también las casas con tinaco. El supuesto decide quién sale en el mapa.</p>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={g.sens}><CartesianGrid stroke="#e2e8f0" /><XAxis dataKey="consumo" fontSize={11} /><YAxis fontSize={11} tickFormatter={(v) => `${v / 1000}k`} /><Tooltip formatter={(v: number) => fmt(v)} /><Legend />
              <Bar dataKey="Sin almacenamiento" stackId="a" fill={GRIS} /><Bar dataKey="Con tinaco" stackId="a" fill={CLARO} /><Bar dataKey="Con cisterna" stackId="a" fill={AZUL} />
            </BarChart>
          </ResponsiveContainer>
        </Tarjeta>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Tarjeta>
          <h2 className="font-semibold">Colonias con más viviendas sin almacenamiento</h2>
          <table className="mt-2 w-full text-sm"><thead className="text-left text-xs text-slate-500"><tr><th>Colonia</th><th>Zona</th><th className="text-right">% sin almacén</th><th className="text-right">Personas</th></tr></thead>
            <tbody>{g.top.map((c) => <tr key={c.id} className="border-t"><td>{c.nombre}</td><td>{c.zona}</td><td className="text-right tabular-nums">{((c.viv_sin_almacen / c.viviendas) * 100).toFixed(0)} %</td><td className="text-right tabular-nums">{fmt(c.pob)}</td></tr>)}</tbody></table>
        </Tarjeta>
        <Tarjeta>
          <h2 className="font-semibold">Cómo se calcula</h2>
          <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-slate-700">
            <li>Cada colonia se divide en <b>estratos</b>: sin almacenamiento, con tinaco, con cisterna (Censo 2020, dataset 01). Nunca se promedia la colonia: una casa sin tinaco no usa el del vecino.</li>
            <li>Autonomía por estrato = litros ÷ (ocupantes × consumo). Sin almacenamiento = 0 h.</li>
            <li>El calendario del SIAPA (por fecha y zona) da las horas acumuladas sin servicio. Un estrato está <b>seco</b> si las horas superan su autonomía.</li>
            <li>El color del hexágono es el % de viviendas secas; la altura, las personas.</li>
            <li>Las pipas se reparten por severidad = % secas × (0.5 + 0.5 × marginación), con marginación del dataset 17 (CONAPO, nivel AGEB).</li>
          </ol>
        </Tarjeta>
      </div>

      <Tarjeta>
        <h2 className="font-semibold">Datasets del catálogo y cómo se usan</h2>
        <table className="mt-2 w-full text-sm"><thead className="text-left text-xs text-slate-500"><tr><th>#</th><th>Dataset</th><th>Institución · año</th><th>Qué tomamos</th><th>Para qué</th></tr></thead><tbody>
          <tr className="border-t"><td>01</td><td>Principales resultados por AGEB y manzana urbana</td><td>INEGI · Censo 2020</td><td>POBTOT, TVIVHAB, VPH_TINACO, VPH_CISTER, VPH_AGUADV</td><td>Describir el problema y alimentar el modelo (estratos por manzana)</td></tr>
          <tr className="border-t"><td>17</td><td>Índices de marginación</td><td>CONAPO · 2020</td><td>Índice por AGEB</td><td>Caracterizar quién vive sin almacenamiento y ponderar el priorizador</td></tr>
          <tr className="border-t"><td>—</td><td>Rotación del servicio de agua</td><td>SIAPA · 2026 (consultado 10-nov)</td><td>Zonas y días sin servicio</td><td>Calendario por fecha (complemento, no cuenta como dataset del catálogo)</td></tr>
        </tbody></table>
      </Tarjeta>

      <Tarjeta>
        <h2 className="font-semibold">Supuestos declarados</h2>
        <ul className="mt-2 grid gap-1 text-sm text-slate-700 md:grid-cols-2">
          <li>Tinaco 1,100 L · cisterna 5,000 L (el Censo no dice litros)</li>
          <li>Consumo 50 L/persona/día (mínimo OMS); se reporta a 100 y 150</li>
          <li>Un día de corte = 24 h efectivas sin agua en la llave (se prueba 24–48)</li>
          <li>Agua guardada más de 48 h se marca para desinfectar</li>
          <li>Censo 2020: 6 años de antigüedad</li>
          <li>Un hexágono representa una colonia, no su forma real</li>
          <li>Colonias, calendario de noviembre y ubicación de cisternas: simulados hasta confirmar en el portal del SIAPA y el mapa municipal</li>
        </ul>
      </Tarjeta>
    </main>
  );
}
