// Íconos de trazo propio (24×24). Heredan el color del texto.
type P = { className?: string };
const base = { viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };

export const IconoInicio = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M3.5 10.5 12 4l8.5 6.5V20a1 1 0 0 1-1 1H15v-6H9v6H4.5a1 1 0 0 1-1-1z" /></svg>
);
export const IconoGota = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M12 3.2c-3.2 4.4-6.2 7.5-6.2 11a6.2 6.2 0 0 0 12.4 0c0-3.5-3-6.6-6.2-11z" /></svg>
);
export const IconoCasa = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M3.5 10.5 12 4l8.5 6.5V20a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1z" /><path d="M12 11.2c-1.3 1.8-2.5 3-2.5 4.4a2.5 2.5 0 0 0 5 0c0-1.4-1.2-2.6-2.5-4.4z" /></svg>
);
export const IconoMapa = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M12 2.8 20 7.4v9.2l-8 4.6-8-4.6V7.4z" /><path d="M12 12v9.2M12 12l8-4.6M12 12 4 7.4" /></svg>
);
export const IconoPipa = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M2.5 6.5h10.5v10H2.5zM13 9.5h4.2l3.3 3.6v3.4H13" /><circle cx="6.5" cy="17.5" r="1.9" /><circle cx="16.5" cy="17.5" r="1.9" /></svg>
);
export const IconoLibro = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M4.5 5.5A2.5 2.5 0 0 1 7 3h12.5v15H7a2.5 2.5 0 0 0-2.5 2.5zM4.5 5.5v15M8.5 7.5h7M8.5 11h5" /></svg>
);
export const IconoCapas = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="m12 3.5 8.5 4.5-8.5 4.5L3.5 8z" /><path d="m3.5 12 8.5 4.5 8.5-4.5M3.5 16l8.5 4.5 8.5-4.5" /></svg>
);
export const IconoAjustes = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M4 7h10M18 7h2M4 17h4M12 17h8" /><circle cx="16" cy="7" r="2" /><circle cx="10" cy="17" r="2" /></svg>
);
export const IconoCerrar = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M6 6l12 12M18 6 6 18" /></svg>
);
export const IconoFlecha = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M5 12h14M13 6l6 6-6 6" /></svg>
);
export const IconoCisterna = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><ellipse cx="12" cy="6" rx="7" ry="2.5" /><path d="M5 6v11c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V6" /><path d="M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5" /></svg>
);
export const IconoTelefono = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><rect x="6.5" y="2.5" width="11" height="19" rx="2.5" /><path d="M10.5 18h3" /></svg>
);

export const IconoTinaco = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M6 9.5c0-2.2 2.7-4 6-4s6 1.8 6 4V18c0 1.1-2.7 2-6 2s-6-.9-6-2z" /><path d="M6 9.5c0 1.1 2.7 2 6 2s6-.9 6-2" /><path d="M12 3v2.5" /><path d="M8.5 20v1.5M15.5 20v1.5" /></svg>
);
export const IconoLupa = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><circle cx="10.5" cy="10.5" r="6" /><path d="m15 15 5 5" /></svg>
);
export const IconoMas = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M12 5v14M5 12h14" /></svg>
);
export const IconoMenos = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M5 12h14" /></svg>
);
export const IconoAtras = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="M19 12H5M11 6l-6 6 6 6" /></svg>
);
export const IconoPersona = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><circle cx="12" cy="7.5" r="3.3" /><path d="M5.5 20c.4-3.6 3-5.8 6.5-5.8s6.1 2.2 6.5 5.8" /></svg>
);
export const IconoCheck = ({ className = "h-5 w-5" }: P) => (
  <svg {...base} className={className}><path d="m5 12.5 4.5 4.5L19 7.5" /></svg>
);

/** El hexágono de la marca. */
export const Hex = ({ className = "h-6 w-6", style }: P & { style?: React.CSSProperties }) => (
  <svg viewBox="0 0 24 24" className={className} style={style} fill="currentColor" aria-hidden><path d="M12 2l8.66 5v10L12 22l-8.66-5V7z" /></svg>
);
