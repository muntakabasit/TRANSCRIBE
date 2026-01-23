import type { Metadata } from "next";
import "./globals.css";
import PWAInstall from "@/components/PWAInstall";

export const metadata: Metadata = {
  title: "DAWT-Transcribe | Free Audio Transcription",
  description: "Free audio transcription for everyone. Supports YouTube, TikTok, Instagram, and 12+ languages including Pidgin, Twi, Igbo, Yoruba.",
  keywords: "transcribe, transcription, speech to text, audio, youtube, tiktok, instagram, pidgin, twi, igbo, yoruba",
  manifest: "/manifest.json",
  themeColor: "#E8B44C",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "DAWT-Transcribe",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/x-icon" href="/favicon.ico" />
        <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png" />
        <link rel="icon" type="image/png" sizes="512x512" href="/icon-512.png" />
        <link rel="apple-touch-icon" href="/icon-192.png" />
        <meta name="theme-color" content="#E8B44C" />
      </head>
      <body className="antialiased">
        <PWAInstall />
        {children}
      </body>
    </html>
  );
}
