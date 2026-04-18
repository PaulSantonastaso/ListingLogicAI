import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  // Only load the weights we use (400, 500, 600)
  weight: ["400", "500", "600"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "ListingLogicAI — AI-Powered Real Estate Marketing",
  description:
    "Upload your listing photos and agent notes. Get a complete marketing campaign — MLS description, social posts, and email sequences — in under a minute.",
  metadataBase: new URL("https://listinglogicai.com"),
  openGraph: {
    title: "ListingLogicAI",
    description: "AI-powered listing marketing for high-performing agents.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
