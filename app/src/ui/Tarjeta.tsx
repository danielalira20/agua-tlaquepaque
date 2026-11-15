// Contenedores base. Sin datos: solo forma.
export function Tarjeta({ children, className = "", as: Tag = "div" }: { children: React.ReactNode; className?: string; as?: "div" | "section" | "article" | "aside" }) {
  return <Tag className={`rounded-tarjeta border border-tinta/5 bg-white p-5 shadow-suave ${className}`}>{children}</Tag>;
}

/** Título corto de sección, en mayúsculas pequeñas. */
export function Antetitulo({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`text-xs font-bold uppercase tracking-[0.14em] text-agua-600 ${className}`}>{children}</div>;
}

/** Botón píldora. `tono` cambia el énfasis, nunca la forma. */
export function BotonPildora({ children, activo = false, onClick, className = "", titulo, deshabilitado = false }: {
  children: React.ReactNode; activo?: boolean; onClick?: () => void; className?: string; titulo?: string; deshabilitado?: boolean;
}) {
  return (
    <button type="button" onClick={onClick} title={titulo} disabled={deshabilitado} aria-pressed={activo}
      className={`inline-flex min-h-10 items-center justify-center gap-2 rounded-full px-4 text-sm font-semibold transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-45 ${activo ? "bg-agua-600 text-white shadow-suave" : "bg-white text-tinta shadow-suave hover:bg-agua-50"} ${className}`}>
      {children}
    </button>
  );
}
