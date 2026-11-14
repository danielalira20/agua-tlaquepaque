// Cruce del motor oficial (TypeScript) contra el de referencia (Python).
// Uso, desde app/:  node scripts/verifica-vectores.ts
// Conteos de viviendas y horas deben coincidir EXACTAMENTE (motor/ESPECIFICACION.md, sección 11).
import { readFileSync } from "node:fs";
import { evaluarManzana, type SupuestosMotor } from "../src/lib/motor.ts";

const raiz = new URL("../../", import.meta.url);
const v = JSON.parse(readFileSync(new URL("motor/vectores/vectores.json", raiz), "utf8"));
const cal = JSON.parse(readFileSync(new URL(`motor/calendarios/${v.calendario}.json`, raiz), "utf8"));
const entradas = new Map<string, any>(v.entradas.map((e: any) => [e.cvegeo, e]));
const campos = ["horas_sin_servicio_min", "horas_sin_servicio_max", "viv_sin_agua_min", "viv_sin_agua_max", "viv_agua_guardada_min", "viv_agua_guardada_max", "estado"] as const;

let total = 0, malas = 0;
for (const [nombre, conj] of Object.entries<any>(v.conjuntos)) {
  const s = conj.supuestos as SupuestosMotor;
  let malasConj = 0;
  for (const esperado of conj.salida) {
    const e = entradas.get(esperado.cvegeo);
    const r = evaluarManzana(e, cal.esquema, esperado.fecha, s) as any;
    total++;
    const dif = campos.filter((k) => r[k] !== esperado[k]);
    if (dif.length) {
      malas++; malasConj++;
      if (malasConj <= 5) console.log(`  ✗ ${nombre} ${esperado.cvegeo} ${esperado.fecha}: ` + dif.map((k) => `${k} oficial=${r[k]} referencia=${esperado[k]}`).join(", "));
    }
  }
  console.log(`${malasConj === 0 ? "✓" : "✗"} ${nombre}: ${conj.salida.length - malasConj}/${conj.salida.length} renglones iguales`);
}
console.log(`\nVectores: ${total - malas}/${total} iguales`);

// Cruce completo contra la exportación de la app (todas las manzanas, todas las fechas, supuestos base).
const real = new URL("app/public/datos/real/", raiz);
const mz = JSON.parse(readFileSync(new URL("manzanas.json", real), "utf8"));
const est = JSON.parse(readFileSync(new URL("estado.json", real), "utf8"));
const meta = JSON.parse(readFileSync(new URL("meta.json", real), "utf8"));
const cv = JSON.parse(readFileSync(new URL("calendarios.json", real), "utf8"))[meta.calendario_usado];
const cod: Record<string, number> = { con_agua: 0, quiebre_parcial: 1, quiebre_mayoritario: 2 };
let n = 0, m = 0;
for (const d of est.fechas) {
  mz.forEach((x: any, i: number) => {
    if (!(x.viviendas > 0)) return;
    const r = evaluarManzana(x, cv.esquema, d.fecha, meta.supuestos);
    n++;
    if (r.viv_sin_agua_min !== d.viv_sin_agua_min[i] || r.viv_sin_agua_max !== d.viv_sin_agua_max[i] ||
        r.viv_agua_guardada_min !== d.viv_agua_guardada_min[i] || r.viv_agua_guardada_max !== d.viv_agua_guardada_max[i] ||
        r.horas_sin_servicio_min !== d.horas_sin_servicio_min[i] || r.horas_sin_servicio_max !== d.horas_sin_servicio_max[i] ||
        cod[r.estado] !== d.estado[i]) { m++; if (m <= 5) console.log(`  ✗ estado.json ${x.cvegeo} ${d.fecha}`); }
  });
}
console.log(`estado.json: ${n - m}/${n} iguales`);
process.exit(malas || m ? 1 : 0);
