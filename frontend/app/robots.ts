import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/review/", "/preview/", "/api/"],
      },
    ],
    sitemap: "https://www.metes.app/sitemap.xml",
  };
}