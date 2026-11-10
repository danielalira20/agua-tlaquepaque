"use client";
import { useEffect, useState } from "react";
import type { Calendario, Cisterna, Colonia } from "./modelo";

export type Datos = { colonias: Colonia[]; cisternas: Cisterna[]; calendarios: Record<string, Calendario> };

let cache: Datos | null = null;

export function useDatos() {
  const [datos, setDatos] = useState<Datos | null>(cache);
  useEffect(() => {
    if (cache) return;
    Promise.all([fetch("/datos/colonias.json").then((r) => r.json()), fetch("/datos/calendario.json").then((r) => r.json())]).then(
      ([c, cal]) => { cache = { colonias: c.colonias, cisternas: c.cisternas, calendarios: cal }; setDatos(cache); }
    );
  }, []);
  return datos;
}
