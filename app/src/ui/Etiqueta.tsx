// Real / Estimado / Simulado: un punto y una palabra. La explicación vive en el desplegable de cada pantalla.
export type TipoDato = "real" | "estimado" | "simulado";
const ESTILO: Record<TipoDato, { punto: string; texto: string; titulo: string }> = {
  real: { punto: "bg-emerald-500", texto: "Dato real", titulo: "Sale de una fuente oficial (Censo, SIAPA, CONAPO, municipio)" },
  estimado: { punto: "bg-agua-500", texto: "Estimado", titulo: "Lo calcula el modelo a partir de datos reales" },
  simulado: { punto: "border border-dashed border-tinta-suave bg-transparent", texto: "Simulado", titulo: "Maqueta: no es un dato" },
};
export function Etiqueta({ tipo, className = "" }: { tipo: TipoDato; className?: string }) {
  const e = ESTILO[tipo];
  return (
    <span title={e.titulo} className={`inline-flex items-center gap-1.5 text-xs font-semibold text-tinta-suave ${className}`}>
      <span className={`h-2 w-2 rounded-full ${e.punto}`} />{e.texto}
    </span>
  );
}
