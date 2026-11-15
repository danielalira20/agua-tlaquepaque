// Cuenta las palabras del reporte por seccion, como el contador de Word (cadenas separadas por espacios).
// Uso: node reporte/fuente/cuenta_palabras.js
const c = require("./contenido.js");
const limpio = (s) => s.replace(/\*\*/g, "").replace(/\*/g, "");
const n = (s) => limpio(s).split(/\s+/).filter(Boolean).length;
const filas = [];
const p = c.portada;
filas.push(["Portada", n(p.concurso) + n(p.reto) + n(p.titulo) + p.campos.reduce((a, [k, v]) => a + n(k) + n(v), 0)]);
filas.push(["Resumen (300 a 450)", n("Resumen") + c.resumen.reduce((a, x) => a + n(x), 0)]);
filas.push(["Pie de la figura 1", n(c.figura1.pie)]);
let actual = null;
for (const s of c.secciones) {
  if (s.titulo && s.nivel === 1) { actual = [s.titulo, 0]; filas.push(actual); }
  if (s.titulo) actual[1] += n(s.titulo);
  for (const x of s.parrafos || []) actual[1] += n(x);
  if (s.figura) actual[1] += n(s.figura.pie);
}
filas.push(["7. Bibliografía", n("7. Bibliografía") + c.bibliografia.reduce((a, x) => a + n(x), 0)]);
const total = filas.reduce((a, f) => a + f[1], 0);
for (const [k, v] of filas) console.log(String(v).padStart(5), " ", k);
console.log(String(total).padStart(5), "  TOTAL (limite: 1,500 a 2,000)");
const res = c.resumen.reduce((a, x) => a + n(x), 0);
console.log(`Resumen sin el titulo: ${res}`);
if (total > 2000 || total < 1500 || res < 300 || res > 450) { console.error("FUERA DE LIMITE"); process.exit(1); }
