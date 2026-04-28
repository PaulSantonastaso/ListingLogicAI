import type { Metadata } from "next";
import { Inter, JetBrains_Mono, Onest } from "next/font/google";
import Script from "next/script";
import "./globals.css";

const META_PIXEL_ID = process.env.NEXT_PUBLIC_META_PIXEL_ID;

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  weight: ["400", "500", "600"],
  display: "swap",
});

const onest = Onest({
  subsets: ["latin"],
  variable: "--font-onest",
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  weight: ["400", "500"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "metes — AI-Powered Real Estate Listing Marketing",
  description:
    "Upload your listing photos and agent notes. Get MLS copy, social posts, email campaigns, and a Fair Housing audit — in under 60 seconds. $35 per listing, no subscription.",
  metadataBase: new URL("https://www.metes.app"),
  manifest: "/manifest.json",
  keywords: [
    "real estate listing marketing",
    "AI listing description",
    "MLS description generator",
    "real estate social media posts",
    "Fair Housing compliance",
    "listing marketing for agents",
    "real estate email campaign",
    "AI real estate marketing",
  ],
  authors: [{ name: "metes", url: "https://www.metes.app" }],
  creator: "metes",
  openGraph: {
    title: "metes — AI-Powered Real Estate Listing Marketing",
    description:
      "MLS copy, social posts, email campaigns, and Fair Housing audit — generated from your photos and notes. $35 per listing.",
    url: "https://www.metes.app",
    siteName: "metes",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "metes — AI-Powered Real Estate Listing Marketing",
    description:
      "MLS copy, social posts, email campaigns, and Fair Housing audit — generated from your photos and notes. $35 per listing.",
    creator: "@metesapp",
  },
  alternates: {
    canonical: "https://www.metes.app",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${onest.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
        {META_PIXEL_ID && (
          <>
            <Script id="meta-pixel" strategy="afterInteractive">
              {`
                !function(f,b,e,v,n,t,s)
                {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
                n.callMethod.apply(n,arguments):n.queue.push(arguments)};
                if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
                n.queue=[];t=b.createElement(e);t.async=!0;
                t.src=v;s=b.getElementsByTagName(e)[0];
                s.parentNode.insertBefore(t,s)}(window, document,'script',
                'https://connect.facebook.net/en_US/fbevents.js');
                fbq('init', '${META_PIXEL_ID}');
                fbq('track', 'PageView');
              `}
            </Script>
            <noscript>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                height="1"
                width="1"
                style={{ display: "none" }}
                src={`https://www.facebook.com/tr?id=${META_PIXEL_ID}&ev=PageView&noscript=1`}
                alt=""
              />
            </noscript>
          </>
        )}
      </body>
    </html>
  );
}
