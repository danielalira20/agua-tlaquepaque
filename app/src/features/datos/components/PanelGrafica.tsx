import { Etiqueta, Tarjeta, type TipoDato } from "@/ui";

/** Una gráfica = un hallazgo. El título dice la conclusión; la nota, cómo leerla. */
export function PanelGrafica({ hallazgo, nota, tipo = "estimado", children, className = "" }: {
  hallazgo: React.ReactNode; nota?: React.ReactNode; tipo?: TipoDato; children: React.ReactNode; className?: string;
}) {
  return (
    <Tarjeta as="section" className={className}>
      <h2 className="text-xl font-bold leading-snug">{hallazgo}</h2>
      {nota && <p className="mt-1 text-sm leading-relaxed text-tinta-suave">{nota}</p>}
      <div className="mt-4">{children}</div>
      <Etiqueta tipo={tipo} className="mt-3" />
    </Tarjeta>
  );
}

export const COLOR = { agua: "#1f5fae", aguaMedio: "#4b98cc", aguaClaro: "#a9d4ec", barro: "#c4623a", barroClaro: "#e8c3a2", rejilla: "#f3eadc", texto: "#5b6675" };
export const miles = (v: number) => `${Math.round(v / 1000)}k`;
