import "@/styles/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "MemoryOS",
  description: "A personal memory operating system for structured learning.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

