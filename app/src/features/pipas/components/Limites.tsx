import { Aclaraciones } from "@/ui";

/** Lo que sí y lo que no aguanta el plan, en viñetas cortas. */
export function Limites({ p }: { p: { pipas: number; viajes_por_dia: number; litros_por_viaje: number; litros_por_hogar: number; radio_cobertura_m: number } }) {
  return (
    <Aclaraciones titulo="Límites de este plan de pipas" resumen="7 puntos">
      <ul className="list-disc space-y-1 pl-5">
        <li>La ventaja de priorizar se mantiene en todos los escenarios que probamos, aunque es pequeña en los peores.</li>
        <li><b>Dónde se para cada pipa sí cambia:</b> solo el 37 % de las manzanas atendidas coincide con el caso base. Si cambia un supuesto, el plan se recalcula.</li>
        <li>Los puntos fijos (cisternas permanentes) deben salir del núcleo robusto.</li>
        <li>La marginación no pesa en la prioridad: con la cota máxima, las AGEB de marginación «Muy alto» pueden quedarse sin viajes (el reporte lo detalla).</li>
        <li>El número de cada parada es el orden en que el priorizador eligió la colonia, <b>no una ruta</b>.</li>
        <li>Parámetros declarados: {p.pipas} pipas, {p.viajes_por_dia} viajes al día, {p.litros_por_viaje.toLocaleString("es-MX")} L por viaje, {p.litros_por_hogar} L por hogar, radio de cobertura de {p.radio_cobertura_m} m.</li>
        <li><b>El baseline es estilizado:</b> los mismos viajes repartidos por turnos entre las cisternas instaladas; no es lo que hace hoy el municipio.</li>
      </ul>
    </Aclaraciones>
  );
}
