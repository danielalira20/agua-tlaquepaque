import { Hoja, Interruptor, Segmentado } from "@/ui";

export type Capas = { modo: "agua" | "marginacion"; cisternas: boolean; propuestas: boolean; nucleo: boolean; version: "vigente" | "original" };

const punto = (c: string) => <span className="block h-3 w-3 rounded-full ring-2 ring-white" style={{ background: c }} />;

/** Todo lo que se puede prender o apagar en el mapa, en un solo lugar. */
export function MenuCapas({ abierto, onCerrar, capas, onCapas, nCisternas, nNucleo }: {
  abierto: boolean; onCerrar: () => void; capas: Capas; onCapas: (c: Capas) => void; nCisternas: number; nNucleo: number;
}) {
  const set = (p: Partial<Capas>) => onCapas({ ...capas, ...p });
  return (
    <Hoja abierta={abierto} onCerrar={onCerrar} titulo="Capas del mapa">
      <section>
        <h3 className="mb-2 text-sm font-bold">Color de los hexágonos</h3>
        <Segmentado valor={capas.modo} onCambio={(v) => set({ modo: v })}
          opciones={[{ valor: "agua", texto: "Casas sin agua" }, { valor: "marginacion", texto: "Marginación" }]} />
        <p className="mt-2 text-xs text-tinta-suave">La marginación es una capa aparte: no entra en el cálculo.</p>
      </section>
      <section className="mt-5 space-y-2">
        <h3 className="text-sm font-bold">Mostrar</h3>
        <Interruptor etiqueta={`Cisternas comunitarias (${nCisternas})`} ayuda="Naranja claro: ubicación aproximada" activo={capas.cisternas} onCambio={(v) => set({ cisternas: v })} muestra={punto("rgb(249,115,22)")} />
        <Interruptor etiqueta="10 cisternas propuestas" ayuda="Las que el municipio planea instalar" activo={capas.propuestas} onCambio={(v) => set({ propuestas: v, cisternas: v || capas.cisternas })} muestra={punto("rgb(168,85,247)")} />
        <Interruptor etiqueta={nNucleo ? `Núcleo robusto (${nNucleo})` : "Núcleo robusto"} activo={capas.nucleo} onCambio={(v) => set({ nucleo: v })} deshabilitado={!nNucleo}
          ayuda={nNucleo ? "Manzanas entre las 250 más críticas en al menos el 90 % de 300 simulaciones con los rangos de supuestos de la decisión 1" : "Pendiente: los datos de la app aún no traen este campo"} muestra={punto("rgb(245,158,11)")} />
      </section>
      <section className="mt-5">
        <h3 className="mb-2 text-sm font-bold">Calendario del SIAPA</h3>
        <Segmentado valor={capas.version} onCambio={(v) => set({ version: v })}
          opciones={[{ valor: "vigente", texto: "Vigente (4-nov)" }, { valor: "original", texto: "Original (15-oct)" }]} />
        <p className="mt-2 text-xs text-tinta-suave">Compara qué cambió para las casas cuando el SIAPA movió los días de corte.</p>
      </section>
    </Hoja>
  );
}
