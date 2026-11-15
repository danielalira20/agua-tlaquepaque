// Genera reporte/REPORTE_CIENTIFICO.docx a partir de contenido.js.
// Formato oficial: Arial 12, interlineado 1.5, dos columnas despues del resumen, tamaño carta.
// Uso: node reporte/fuente/genera_reporte.js   (necesita el paquete `docx`)
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, SectionType, Footer, PageNumber, BorderStyle, ShadingType,
} = require("docx");
const c = require("./contenido.js");

const DIR = path.resolve(__dirname, "..");
const FUENTE = "Arial";
const AMARILLO = { type: ShadingType.CLEAR, fill: "FFFF00" }; // marca lo que falta completar
const T = 24; // 12 pt
const LINEA = 360; // interlineado 1.5
const MARGEN = 1440; // 1 pulgada
const ANCHO_TEXTO_PX = 624; // 6.5 pulgadas a 96 ppp
const SEPARACION_COLUMNAS = 432; // 0.3 pulgadas
const ANCHO_COLUMNA_PX = Math.floor(((12240 - 2 * MARGEN - SEPARACION_COLUMNAS) / 2 / 1440) * 96);

/** Convierte **negrita**, *cursiva* y [por completar] en corridas de texto. */
function corridas(texto, extra = {}) {
  const out = [];
  const partes = texto.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\])/).filter((x) => x !== "");
  for (const p of partes) {
    if (p.startsWith("**")) out.push(new TextRun({ text: p.slice(2, -2), bold: true, font: FUENTE, size: T, ...extra }));
    else if (p.startsWith("*")) out.push(new TextRun({ text: p.slice(1, -1), italics: true, font: FUENTE, size: T, ...extra }));
    else if (p.startsWith("[") && /completar|nombre completo/i.test(p)) out.push(new TextRun({ text: p, shading: AMARILLO, font: FUENTE, size: T, ...extra }));
    else out.push(new TextRun({ text: p, font: FUENTE, size: T, ...extra }));
  }
  return out;
}

const parrafo = (texto, opciones = {}) =>
  new Paragraph({
    children: corridas(texto, opciones.run),
    alignment: opciones.alineacion ?? AlignmentType.JUSTIFIED,
    spacing: { line: LINEA, before: 0, after: opciones.despues ?? 160 },
    indent: opciones.sangria,
    keepNext: opciones.keepNext,
    keepLines: opciones.keepLines,
  });

const titulo = (texto, nivel) =>
  new Paragraph({
    children: [new TextRun({ text: texto, bold: true, italics: nivel === 2, font: FUENTE, size: T })],
    alignment: AlignmentType.LEFT,
    spacing: { line: LINEA, before: nivel === 1 ? 200 : 80, after: 80 },
    keepNext: true,
    outlineLevel: nivel - 1,
  });

function tamanoPng(ruta) {
  const b = fs.readFileSync(ruta);
  return { ancho: b.readUInt32BE(16), alto: b.readUInt32BE(20), datos: b };
}

function figura(f, anchoPx) {
  const { ancho, alto, datos } = tamanoPng(path.join(DIR, f.archivo));
  return [
    new Paragraph({
      children: [new ImageRun({ type: "png", data: datos, transformation: { width: anchoPx, height: Math.round((anchoPx * alto) / ancho) },
        altText: { title: f.pie.replace(/\*/g, ""), description: f.pie.replace(/\*/g, ""), name: path.basename(f.archivo) } })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      keepNext: true,
    }),
    new Paragraph({ children: corridas(f.pie, { size: 20 }), alignment: AlignmentType.CENTER, spacing: { line: 276, before: 0, after: 200 } }),
  ];
}

// ---------- Portada ----------
const p = c.portada;
const centro = (texto, run = {}, espacio = {}) =>
  new Paragraph({ children: corridas(texto, run), alignment: AlignmentType.CENTER, spacing: { line: LINEA, before: 0, after: 120, ...espacio } });
const portada = [
  new Paragraph({
    children: [new TextRun({ text: "[Logotipo del concurso]", shading: AMARILLO, font: FUENTE, size: T })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 600, after: 600 },
  }),
  centro(p.concurso, { bold: true, size: 32 }),
  centro(p.reto, { size: 28 }, { after: 900 }),
  new Paragraph({
    children: [new TextRun({ text: p.titulo, bold: true, font: FUENTE, size: 44 })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 300 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: "2A78D6", space: 14 } },
  }),
  new Paragraph({ children: [], spacing: { after: 500 } }),
  ...p.campos.map(([k, v]) => centro(`**${k}:** ${v}`, {}, { after: 140 })),
];

// ---------- Resumen ----------
const resumen = [
  new Paragraph({ children: [new TextRun({ text: "Resumen", bold: true, font: FUENTE, size: T })], alignment: AlignmentType.CENTER, spacing: { line: LINEA, after: 160 }, pageBreakBefore: false }),
  ...c.resumen.map((t) => parrafo(t)),
  ...figura(c.figura1, ANCHO_TEXTO_PX),
];

// ---------- Cuerpo a dos columnas ----------
const cuerpo = [];
for (const s of c.secciones) {
  if (s.titulo) cuerpo.push(titulo(s.titulo, s.nivel));
  for (const t of s.parrafos || []) cuerpo.push(parrafo(t, { alineacion: AlignmentType.LEFT }));
  if (s.figura) cuerpo.push(...figura(s.figura, ANCHO_COLUMNA_PX));
}

// ---------- Bibliografía (una columna, sangría francesa) ----------
const bibliografia = [
  titulo("7. Bibliografía", 1),
  ...c.bibliografia.map((t) => parrafo(t, { alineacion: AlignmentType.LEFT, sangria: { left: 720, hanging: 720 }, despues: 120, keepLines: true })),
];

const pagina = { size: { width: 12240, height: 15840 }, margin: { top: MARGEN, right: MARGEN, bottom: MARGEN, left: MARGEN } };
const pie = new Footer({
  children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FUENTE, size: 20 })] })],
});

const doc = new Document({
  creator: "Equipo Aguanta",
  title: p.titulo,
  description: "Reporte científico. Hackathon Jalisco Internacional 2026, Reto 01 Ciudades Inteligentes.",
  styles: { default: { document: { run: { font: FUENTE, size: T, language: { value: "es-MX" } } } } },
  sections: [
    { properties: { page: pagina, titlePage: true }, footers: { default: pie, first: new Footer({ children: [] }) }, children: portada },
    { properties: { page: pagina, type: SectionType.NEXT_PAGE }, footers: { default: pie }, children: resumen },
    { properties: { page: pagina, type: SectionType.CONTINUOUS, column: { count: 2, space: SEPARACION_COLUMNAS, equalWidth: true } }, footers: { default: pie }, children: cuerpo },
    { properties: { page: pagina, type: SectionType.CONTINUOUS }, footers: { default: pie }, children: bibliografia },
  ],
});

// ---------- Copia en texto (para revisar en GitHub sin abrir Word) ----------
const md = [
  "<!-- Generado por reporte/fuente/genera_reporte.js a partir de reporte/fuente/contenido.js. No editar a mano. -->",
  `# ${p.titulo}`, `*${p.concurso} · ${p.reto}*`, ...p.campos.map(([k, v]) => `- **${k}:** ${v}`),
  "## Resumen", ...c.resumen, `![Figura 1](${c.figura1.archivo})`, c.figura1.pie,
  ...c.secciones.flatMap((s) => [
    ...(s.titulo ? [`${s.nivel === 1 ? "##" : "###"} ${s.titulo}`] : []), ...(s.parrafos || []),
    ...(s.figura ? [`![Figura 2](${s.figura.archivo})`, s.figura.pie] : []),
  ]),
  "## 7. Bibliografía", ...c.bibliografia,
].join("\n\n") + "\n";
fs.writeFileSync(path.join(DIR, "REPORTE_CIENTIFICO.md"), md);

const salida = path.join(DIR, "REPORTE_CIENTIFICO.docx");
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(salida, buf);
  console.log(`${path.relative(process.cwd(), salida)}  ${(buf.length / 1024).toFixed(0)} KB`);
});
