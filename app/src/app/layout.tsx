import type { Metadata } from "next";
import "./globals.css";
import { Nav } from "@/components/ui";

export const metadata: Metadata = {
  title: "Aguanta · ¿Cuánto aguanta tu casa?",
  description: "Tandeo en Tlaquepaque: cuántas viviendas se quedan sin agua cada día del calendario del SIAPA y a dónde mandar las pipas.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <Nav />
        {children}
      </body>
    </html>
  );
}
