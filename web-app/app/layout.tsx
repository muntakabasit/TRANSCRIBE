import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DAWT-Transcribe | Free Audio Transcription",
  description: "Convert speech to text with high accuracy. Support for YouTube, recordings, and 12+ languages.",
  keywords: "transcribe, transcription, speech to text, audio, youtube, subtitle",
  manifest: "/manifest.json",
  themeColor: "#4A90E2",
  viewport: {
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "DAWT-Transcribe",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/icon-192.png" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
