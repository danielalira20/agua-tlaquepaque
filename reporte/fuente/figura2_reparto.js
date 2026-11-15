// Figura 2 del reporte: viviendas-dia atendidas en la semana con los mismos 441 viajes.
// Lee optimizador/resultados/costo_por_vivienda.csv (precio 1,200; baselines con las 47 cisternas) y escribe reporte/figuras/figura2_reparto.png.
// Uso: node reporte/fuente/figura2_reparto.js   (necesita playwright)
const fs = require("fs"); const path = require("path");
const { chromium } = require("playwright");
const RAIZ = path.resolve(__dirname, "..", "..");
const filas = fs.readFileSync(path.join(RAIZ, "optimizador/resultados/costo_por_vivienda.csv"), "utf8").trim().split("\n").map((l) => l.split(","));
const cab = filas.shift(); const col = (f, k) => f[cab.indexOf(k)];
const d = {};
for (const f of filas) {
  if (col(f, "costo_viaje_mxn") !== "1200") continue;
  const clave = col(f, "regla") === "priorizado" ? "pri" : col(f, "baseline_cisternas") === "todas" ? col(f, "baseline_turnos") : null;
  if (clave) (d[clave] ??= {})[col(f, "cota")] = +col(f, "viv_dia");
}
const fmt = (n) => n.toLocaleString("en-US");
const MAX = d.pri.max; const ANCHO = 300; const x = (v) => Math.round((v / MAX) * ANCHO);
const AZUL = "#2a78d6", GRIS = "#6f6e69", GRIS_CLARO = "#c3c2b7", TINTA = "#0b0b0b", TINTA2 = "#52514e";
const series = [
  { nombre: "Reparto priorizado (Aguanta)", min: d.pri.min, max: d.pri.max, color: AZUL, claro: AZUL, fuerte: true },
  { nombre: "Por turnos, solo cisternas con necesidad", min: d.con_necesidad.min, max: d.con_necesidad.max, color: GRIS, claro: GRIS_CLARO },
  { nombre: "Por turnos entre todas las cisternas", min: d.todas.min, max: d.todas.max, color: GRIS, claro: GRIS_CLARO },
];
const ALTO_FILA = 78, Y0 = 16, X0 = 8, BARRA = 22;
let svg = "";
series.forEach((s, i) => {
  const y = Y0 + i * ALTO_FILA;
  const etiqueta = s.min === s.max ? fmt(s.min) : `${fmt(s.min)} a ${fmt(s.max)}`;
  svg += `<text x="${X0}" y="${y + 16}" font-size="19" font-weight="${s.fuerte ? 700 : 400}" fill="${TINTA}">${s.nombre}</text>`;
  if (s.max > s.min) svg += `<rect x="${X0}" y="${y + 26}" width="${x(s.max)}" height="${BARRA}" rx="4" fill="${s.claro}"/>`;
  svg += `<rect x="${X0}" y="${y + 26}" width="${x(s.min)}" height="${BARRA}" rx="4" fill="${s.color}"/>`;
  if (s.max > s.min) svg += `<rect x="${X0 + x(s.min) - 1}" y="${y + 26}" width="2" height="${BARRA}" fill="#ffffff"/>`;
  svg += `<text x="${X0 + x(s.max) + 10}" y="${y + 44}" font-size="20" font-weight="700" fill="${TINTA}">${etiqueta}</text>`;
});
const yL = Y0 + series.length * ALTO_FILA + 6;
svg += `<line x1="${X0}" y1="${yL - 12}" x2="472" y2="${yL - 12}" stroke="#e1e0d9" stroke-width="1"/>`;
svg += `<rect x="${X0}" y="${yL}" width="20" height="14" rx="3" fill="${GRIS}"/><text x="${X0 + 27}" y="${yL + 13}" font-size="17" fill="${TINTA2}">cota mínima</text>`;
svg += `<rect x="${X0 + 150}" y="${yL}" width="20" height="14" rx="3" fill="${GRIS_CLARO}"/><text x="${X0 + 177}" y="${yL + 13}" font-size="17" fill="${TINTA2}">hasta la cota máxima</text>`;
const ALTO = yL + 26;
const html = `<body style="margin:0;background:#fff"><svg id="g" xmlns="http://www.w3.org/2000/svg" width="480" height="${ALTO}" viewBox="0 0 480 ${ALTO}" font-family="Arial, 'Liberation Sans', sans-serif"><rect width="480" height="${ALTO}" fill="#ffffff"/>${svg}</svg></body>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 480, height: ALTO }, deviceScaleFactor: 4 });
  await p.setContent(html); const el = await p.$("#g");
  const salida = path.join(RAIZ, "reporte/figuras/figura2_reparto.png");
  await el.screenshot({ path: salida }); await b.close();
  console.log(salida, JSON.stringify(d));
})();
