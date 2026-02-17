import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: "#1b56f5",
};

export const metadata: Metadata = {
  title: "Prepp.ai — Kvalitetssikrede lærermanualer med AI",
  description:
    "Generer kildebelagte undervisningsbriefer koblet til LK20 på sekunder. Lærerens trygge havn i en travel hverdag.",
  openGraph: {
    title: "Prepp.ai — Kvalitetssikrede lærermanualer med AI",
    description:
      "Generer kildebelagte undervisningsbriefer koblet til LK20 på sekunder.",
    locale: "nb_NO",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="no" className={inter.variable}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
