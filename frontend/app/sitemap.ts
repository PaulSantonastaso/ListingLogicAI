import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://www.metes.app",
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1,
    },
    {
      url: "https://www.metes.app/compliance-audit",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/photo-curation",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/neighborhood-intelligence",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: 'https://www.metes.app/tools/listing-description-checker',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/fair-housing-language-mls-listings",
      lastModified: new Date("2026-06-10"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/neighborhood-description-examples",
      lastModified: new Date("2026-06-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/ai-listing-description-tells",
      lastModified: new Date("2026-07-01"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/writing-for-zillow-2026",
      lastModified: new Date("2026-07-04"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/fair-housing-words-to-avoid",
      lastModified: new Date("2026-07-15"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/solo-agent-listing-marketing-economics",
      lastModified: new Date("2026-07-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/how-buyers-research-with-ai",
      lastModified: new Date("2026-07-29"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/neighborhood-content-that-ai-cites",
      lastModified: new Date("2026-08-19"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/learn/neighborhood-pages-agent-website",
      lastModified: new Date("2026-08-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/compare/metes-vs-chatgpt",
      lastModified: new Date("2026-06-17"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: "https://www.metes.app/tools/fha-compliance-checker",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: "https://www.metes.app/tools/neighborhood-guide-generator",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: 'https://www.metes.app/compare/metes-vs-listingai',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.7,
    },
  ];
}