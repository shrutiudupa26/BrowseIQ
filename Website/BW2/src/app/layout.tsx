import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BrowseIQ - AI-Powered Browsing Analytics",
  description: "Transform your browsing history into actionable insights. BrowseIQ is a privacy-first Dex Chrome Extension feature that provides AI-powered, personalized browsing analytics.",
  keywords: "browsing analytics, AI insights, productivity tracking, browser extension, Dex",
  authors: [{ name: "BrowseIQ Team" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body 
        className="antialiased"
        suppressHydrationWarning={true}
      >
        {children}
      </body>
    </html>
  );
}
