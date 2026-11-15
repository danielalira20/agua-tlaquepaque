import type { Metadata } from "next";
import { Atkinson_Hyperlegible_Next, Bricolage_Grotesque } from "next/font/google";
import "./globals.css";
import { Navegacion } from "@/ui/Navegacion";

const titulo = Bricolage_Grotesque({ subsets: ["latin"], variable: "--font-titulo", display: "swap" });
const texto = Atkinson_Hyperlegible_Next({ subsets: ["latin"], variable: "--font-texto", display: "swap" });

export const metadata: Metadata = {
  title: "Aguanta · ¿Cuánto aguanta tu casa?",
  description: "Tandeo en Tlaquepaque: cuántas viviendas se quedan sin agua cada día del calendario del SIAPA y a dónde mandar las pipas.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${titulo.variable} ${texto.variable}`}>
      <body className="min-h-screen bg-crema pb-16 text-tinta antialiased md:pb-0">
        <Navegacion />
        {children}
      </body>
    </html>
  );
}
