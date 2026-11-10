// Genera datos SIMULADOS con la forma de los contratos: una colonia por hexágono H3.
// Cuando Magui y Nat entreguen la lista real de colonias y la geometría, este archivo se reemplaza.
import { gridDisk, cellToLatLng } from "h3-js";
import { latLngToCell } from "h3-js";
import { writeFileSync } from "node:fs";

const CENTRO = [20.6, -103.3]; // San Pedro Tlaquepaque
const centro = latLngToCell(CENTRO[0], CENTRO[1], 8);
const celdas = gridDisk(centro, 6).slice(0, 111);

const reales3 = ["El Álamo", "Las Juntas", "El Tapatío", "Barrio de Santiago", "Colonial Tlaquepaque", "Las Vegas", "Villas El Tapatío"];
const reales4 = ["La Arena", "San Pedrito", "Tateposco"];
let s = 7;
const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };

const usados = { 3: 0, 4: 0 };
const colonias = celdas.map((h3, i) => {
  const [lat, lng] = cellToLatLng(h3);
  const este = lng > CENTRO[1];
  const zona = este ? 4 : 3;
  const reales = zona === 3 ? reales3 : reales4;
  const nombre = reales[usados[zona]++] ?? `Colonia ejemplo ${i + 1}`;
  // gradiente: más al sur y al este, menos almacenamiento y más marginación
  const g = Math.min(1, Math.max(0, (CENTRO[0] - lat) * 25 + (lng - CENTRO[1]) * 10 + 0.5));
  const viviendas = Math.round(200 + rnd() * 700);
  const pSin = Math.min(0.7, 0.03 + g * 0.45 + rnd() * 0.15);
  const pCis = Math.max(0.02, 0.45 - g * 0.35 + rnd() * 0.1);
  const viv_sin_almacen = Math.round(viviendas * pSin);
  const viv_cisterna = Math.round(viviendas * pCis);
  const viv_tinaco = viviendas - viv_sin_almacen - viv_cisterna;
  const ocupantes_prom = +(3.4 + rnd() * 0.9).toFixed(2);
  return {
    id: `c${String(i + 1).padStart(3, "0")}`, nombre, zona, h3, lat: +lat.toFixed(5), lng: +lng.toFixed(5),
    manzanas: Math.round(viviendas / 37), viviendas, pob: Math.round(viviendas * ocupantes_prom), ocupantes_prom,
    viv_sin_almacen, viv_tinaco, viv_cisterna,
    marginacion: +(0.2 + g * 0.7 + rnd() * 0.1).toFixed(2), // dataset 17 (nivel AGEB), 0..1
    simulado: !(reales3.includes(nombre) || reales4.includes(nombre)) ? "nombre y cifras" : "cifras",
  };
});

// 60 cisternas comunitarias ya colocadas (ubicación SIMULADA; la real sale del mapa del municipio)
const cisternas = Array.from({ length: 60 }, (_, i) => {
  const c = colonias[Math.floor(rnd() * colonias.length)];
  return { id: `cis${i + 1}`, colonia_id: c.id, lat: +(c.lat + (rnd() - 0.5) * 0.006).toFixed(5), lng: +(c.lng + (rnd() - 0.5) * 0.006).toFixed(5) };
});

// Calendario por FECHA. Dos versiones: esquema original (15-oct) y esquema del 4-nov.
const DIAS = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];
const esquemas = {
  octubre: { 3: ["miercoles", "sabado"], 4: ["lunes", "jueves"] },
  noviembre: { 3: ["miercoles", "jueves", "sabado"], 4: ["lunes", "jueves", "domingo"] }, // SIMULADO: confirmar en el portal del SIAPA
};
function calendario(version) {
  const dias = [];
  for (let d = new Date("2026-11-02T12:00:00"); d <= new Date("2026-11-29T12:00:00"); d.setDate(d.getDate() + 1)) {
    const fecha = d.toISOString().slice(0, 10);
    const dia = DIAS[d.getDay()];
    const zonas = [3, 4].filter((z) => esquemas[version][z].includes(dia));
    dias.push({ fecha, dia, zonas_sin_servicio: zonas });
  }
  return { fuente: "rotaciondeserviciosiapa.jalisco.gob.mx", consultado: "2026-11-10", version, esquema: esquemas[version], dias };
}

writeFileSync("public/datos/colonias.json", JSON.stringify({ generado: new Date().toISOString(), nota: "SIMULADO. Un hexágono = una colonia (representación, no su forma real).", colonias, cisternas }));
writeFileSync("public/datos/calendario.json", JSON.stringify({ octubre: calendario("octubre"), noviembre: calendario("noviembre") }));
console.log(colonias.length, "colonias,", cisternas.length, "cisternas");
