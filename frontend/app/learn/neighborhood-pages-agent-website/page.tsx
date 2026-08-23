import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, LayoutGrid, MapPin, School, ShoppingBag, Coffee, Building2, Users, Home, Bike, Utensils, Landmark, Route } from "lucide-react";
import Footer from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "The 12 Neighborhood Pages Every Real Estate Agent Website Needs | Metes",
  description:
    "The neighborhood page inventory that drives SEO for agent websites. What to build, what each page needs, how to prioritize, and why AI systems cite them.",
  keywords: [
    "neighborhood pages real estate website",
    "neighborhood directory template",
    "topics for neighborhood guide pages",
    "real estate agent seo",
    "hyperlocal content real estate",
    "agent website neighborhood content",
    "neighborhood landing pages",
    "real estate content marketing",
  ],
  alternates: {
    canonical: "https://www.metes.app/learn/neighborhood-pages-agent-website",
  },
  openGraph: {
    title: "The 12 Neighborhood Pages Every Real Estate Agent Website Needs",
    description:
      "The neighborhood page inventory that drives SEO and AI citations for agent websites.",
    url: "https://www.metes.app/learn/neighborhood-pages-agent-website",
    siteName: "Metes",
    type: "article",
    images: [
      {
        url: "https://www.metes.app/og/neighborhood-pages-agent-website.png",
        width: 1200,
        height: 630,
        alt: "12 neighborhood pages every real estate agent website needs",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "The 12 Neighborhood Pages Every Real Estate Agent Website Needs",
    description: "The neighborhood page inventory that drives SEO for agent websites.",
    images: ["https://www.metes.app/og/neighborhood-pages-agent-website.png"],
  },
  robots: { index: true, follow: true },
};

const SCHEMA_JSON_LD = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://www.metes.app/learn/neighborhood-pages-agent-website#article",
      "headline": "The 12 Neighborhood Pages Every Real Estate Agent Website Needs",
      "description":
        "The neighborhood page inventory that drives SEO and AI citations for agent websites.",
      "image": "https://www.metes.app/og/neighborhood-pages-agent-website.png",
      "datePublished": "2026-08-22",
      "dateModified": "2026-08-22",
      "author": { "@type": "Organization", "name": "Metes Editorial", "url": "https://www.metes.app" },
      "publisher": {
        "@type": "Organization",
        "name": "Metes",
        "url": "https://www.metes.app",
        "logo": { "@type": "ImageObject", "url": "https://www.metes.app/logo.png" },
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://www.metes.app/learn/neighborhood-pages-agent-website",
      },
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.metes.app/learn/neighborhood-pages-agent-website#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How many neighborhood pages does an agent website really need?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The 12 page types in this piece are a comprehensive inventory. Most agents don't need all 12 for every neighborhood — start with 3-5 core page types (neighborhood overview, schools, dining, outdoor, and market update) per neighborhood and expand based on which pages actually rank and drive leads.",
          },
        },
        {
          "@type": "Question",
          "name": "Which neighborhood page type ranks fastest in Google?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Neighborhood overview pages typically rank fastest because they match the highest-volume query pattern ('best neighborhoods in [city]', 'living in [neighborhood]'). School district pages and market update pages follow because those queries have consistent monthly search demand.",
          },
        },
        {
          "@type": "Question",
          "name": "How long should each neighborhood page be?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "800-1,500 words is the sweet spot for most page types. Overview pages can go longer (1,500-2,500 words). Category-specific pages (dining, schools, outdoor) work at 800-1,200 words. Shorter than 600 words gets deprioritized in Google's helpful content assessment. Longer than 2,500 words adds diminishing returns unless the topic genuinely requires it.",
          },
        },
        {
          "@type": "Question",
          "name": "Do neighborhood pages get cited by ChatGPT and Claude?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, when structured properly. AI systems consistently cite neighborhood content with named specifics, verifiable data, structured markup, and dated updates. Generic neighborhood pages that describe locations in vague terms get skipped in AI citations regardless of Google ranking.",
          },
        },
        {
          "@type": "Question",
          "name": "Should agent websites duplicate MLS neighborhood content?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. LLMs and Google both deduplicate content that appears in multiple places. Agent website neighborhood pages should include distinct content — expanded local knowledge, agent voice, hyperlocal specifics MLS descriptions can't cover. Verbatim duplication of MLS content produces pages that never rank because they're not distinct.",
          },
        },
        {
          "@type": "Question",
          "name": "How often should neighborhood pages be updated?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Market update pages need monthly refreshes to stay current. Overview and category pages need quarterly review to catch business closures and neighborhood changes. School and infrastructure pages need annual updates. Visible 'last updated' dates on every page signal freshness to both Google and AI systems.",
          },
        },
        {
          "@type": "Question",
          "name": "Is it worth building 12 neighborhood pages if I only work in one neighborhood?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "For agents focused on a single neighborhood, yes — you're building a topical authority hub that dominates every long-tail query for that area. Better to own 12 pages ranking for 'Winter Garden' than 3 pages competing weakly across 4 neighborhoods.",
          },
        },
        {
          "@type": "Question",
          "name": "What's the biggest mistake agents make with neighborhood website content?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Building thin content across too many neighborhoods rather than deep content across a few. An agent website with 20 neighborhood pages of 300 words each will rank worse than the same agent with 5 neighborhoods x 4 page types at 1,000 words each. Depth compounds; breadth without depth dilutes.",
          },
        },
      ],
    },
  ],
};

const C = {
  cream: "#EFEAE0",
  creamWarm: "#F4F0E8",
  bgCard: "#FAF7F0",
  forest: "#1F3D2E",
  forestDeep: "#14271E",
  moss: "#4A6B53",
  gold: "#B89968",
  goldDeep: "#9A7E50",
  goldSoft: "#D9C49C",
  ink: "#14271E",
  inkSoft: "#4A6B53",
  muted: "rgba(20,39,30,0.55)",
  border: "rgba(20,39,30,0.10)",
  warn: "#C97B5C",
  pass: "#5C8A6E",
};

function SectionLabel({ children, light = false }: { children: React.ReactNode; light?: boolean }) {
  return (
    <div className={`mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] ${light ? "text-[#D9C49C]" : "text-[#9A7E50]"}`}>
      <span className={`inline-block h-px w-[18px] ${light ? "bg-[#D9C49C]" : "bg-[#9A7E50]"}`} />
      {children}
    </div>
  );
}

function BulletList({ items, light = false }: { items: React.ReactNode[]; light?: boolean }) {
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: "0 0 16px 0", display: "flex", flexDirection: "column", gap: "10px" }}>
      {items.map((item, i) => (
        <li key={i} style={{
          paddingLeft: "20px",
          position: "relative",
          fontFamily: "var(--font-manrope, sans-serif)",
          fontSize: "16px",
          lineHeight: 1.7,
          color: light ? "rgba(244,240,232,0.85)" : C.ink,
        }}>
          <span style={{ position: "absolute", left: "4px", color: C.gold, fontWeight: 600 }}>•</span>
          {item}
        </li>
      ))}
    </ul>
  );
}

interface PageTypeCardProps {
  num: string;
  Icon: React.ElementType;
  title: string;
  queryIntent: string;
  wordCount: string;
  priority: "Core" | "Supporting" | "Advanced";
  children: React.ReactNode;
}

function PageTypeCard({ num, Icon, title, queryIntent, wordCount, priority, children }: PageTypeCardProps) {
  const priorityColor = priority === "Core" ? C.pass : priority === "Supporting" ? C.gold : C.moss;
  const priorityBg = priority === "Core" ? "rgba(92,138,110,0.1)" : priority === "Supporting" ? "rgba(184,153,104,0.1)" : "rgba(74,107,83,0.1)";

  return (
    <div style={{
      marginBottom: "24px",
      background: C.bgCard,
      border: `1px solid ${C.border}`,
      borderRadius: "12px",
      padding: "24px 28px",
    }}>
      <div style={{ display: "flex", alignItems: "flex-start", gap: "16px", marginBottom: "14px" }}>
        <div style={{
          flexShrink: 0,
          width: "40px",
          height: "40px",
          borderRadius: "8px",
          background: "rgba(184,153,104,0.12)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: C.goldDeep,
        }}>
          <Icon className="h-5 w-5" strokeWidth={1.75} />
        </div>
        <div style={{ flex: 1 }}>
          <div style={{
            fontFamily: "var(--font-jetbrains, monospace)",
            fontSize: "10px",
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: C.goldDeep,
            marginBottom: "4px",
          }}>Page type {num}</div>
          <h3 style={{
            fontFamily: "var(--font-manrope, sans-serif)",
            fontSize: "20px",
            fontWeight: 600,
            color: C.ink,
            margin: 0,
            letterSpacing: "-0.005em",
          }}>{title}</h3>
        </div>
        <span style={{
          fontFamily: "var(--font-mono, monospace)",
          fontSize: "10px",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          color: priorityColor,
          background: priorityBg,
          padding: "4px 10px",
          borderRadius: "6px",
          height: "fit-content",
        }}>{priority}</span>
      </div>

      <div style={{
        fontFamily: "var(--font-manrope, sans-serif)",
        fontSize: "15px",
        lineHeight: 1.7,
        color: C.ink,
        marginBottom: "16px",
      }}>
        {children}
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "12px",
        marginTop: "16px",
        paddingTop: "14px",
        borderTop: `1px solid ${C.border}`,
      }}>
        <div>
          <div style={{ fontFamily: "var(--font-mono, monospace)", fontSize: "10px", textTransform: "uppercase", letterSpacing: "0.1em", color: C.muted, marginBottom: "3px" }}>Query intent</div>
          <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontSize: "13.5px", color: C.forest, fontStyle: "italic" }}>&ldquo;{queryIntent}&rdquo;</div>
        </div>
        <div>
          <div style={{ fontFamily: "var(--font-mono, monospace)", fontSize: "10px", textTransform: "uppercase", letterSpacing: "0.1em", color: C.muted, marginBottom: "3px" }}>Target length</div>
          <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontSize: "13.5px", color: C.forest, fontWeight: 500 }}>{wordCount}</div>
        </div>
      </div>
    </div>
  );
}

const h2Style = {
  fontFamily: "var(--font-manrope, sans-serif)",
  fontSize: "clamp(24px, 3.5vw, 36px)",
  fontWeight: 500 as const,
  lineHeight: 1.1,
  letterSpacing: "0.005em",
  color: C.ink,
  marginTop: 0,
  marginBottom: "24px",
};

const h3Style = {
  fontFamily: "var(--font-manrope, sans-serif)",
  fontSize: "clamp(18px, 2vw, 22px)",
  fontWeight: 600 as const,
  lineHeight: 1.25,
  letterSpacing: "-0.005em",
  color: C.ink,
  marginTop: "32px",
  marginBottom: "14px",
};

const proseStyle = {
  fontFamily: "var(--font-manrope, sans-serif)",
  fontSize: "16px",
  lineHeight: 1.7,
  color: C.ink,
  marginBottom: "16px",
};

const CONTENT = "mx-auto w-full max-w-[960px] px-6 lg:px-8";
const READING = "mx-auto max-w-[760px]";
const inlineLink = { color: C.forest, textDecoration: "underline", textDecorationColor: C.gold, textUnderlineOffset: "3px" };

export default function NeighborhoodPagesAgentWebsitePage() {
  return (
    <div className="min-h-screen bg-[#EFEAE0]">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(SCHEMA_JSON_LD) }} />
      <Header />

      {/* HERO */}
      <section className="border-b border-[rgba(20,39,30,0.10)] bg-[#F4F0E8]">
        <div className="mx-auto w-full max-w-[960px] px-6 py-16 sm:py-20 lg:px-8">
          <div className="mx-auto max-w-[760px]">
            <SectionLabel>Reference · Agent website content inventory</SectionLabel>
            <h1 className="mb-4 font-manrope text-[clamp(28px,4.5vw,48px)] font-medium leading-[1.08] tracking-[0.005em] text-[#14271E]">
              The 12 neighborhood pages <em className="not-italic text-[#9A7E50]">every real estate agent website needs</em>.
            </h1>
            <p className="mb-6 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              Most agent websites have one neighborhood page per market — a generic overview that ranks nowhere and gets ignored by AI systems. The agents winning search and citations are building topical clusters: 8-12 pages per neighborhood, each targeting a specific query pattern, all cross-linked, all citing named specifics.
            </p>
            <p className="mb-8 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              This piece is the inventory. What to build, what each page needs, how to prioritize, and why LLMs pull specific page types over generic content.
            </p>
            <p className="text-[13px] font-mono uppercase tracking-[0.08em] text-[rgba(20,39,30,0.55)]">
              Last updated: August 22, 2026 · ~15 minute read
            </p>
          </div>
        </div>
      </section>

      {/* TLDR + PRIORITIZATION */}
      <section className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div style={{
              background: C.bgCard,
              border: `1px solid ${C.border}`,
              borderRadius: "12px",
              padding: "28px",
              marginBottom: "32px",
            }}>
              <div className="mb-3 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">TLDR</div>
              <p style={proseStyle}>
                Agent websites that rank for neighborhood queries build topical clusters, not one-off pages. 12 page types cover the full search intent range for a neighborhood — from &ldquo;living in [neighborhood]&rdquo; overview queries to &ldquo;schools in [neighborhood]&rdquo; long-tail queries to &ldquo;[neighborhood] market update&rdquo; recurring queries.
              </p>
              <p style={proseStyle}>
                <strong>Core pages (build first):</strong> Neighborhood overview, schools, market update, dining and nightlife, outdoor and recreation.
              </p>
              <p style={proseStyle}>
                <strong>Supporting pages (build second):</strong> Community character and lifestyle, transportation and commute, family services, everyday amenities.
              </p>
              <p style={{ ...proseStyle, marginBottom: 0 }}>
                <strong>Advanced pages (build third):</strong> New construction and development, luxury and estate homes, first-time buyer guide.
              </p>
            </div>

            <div className="mb-3 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">Jump to</div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "8px" }}>
              {[
                { id: "core", label: "Core pages (build first)" },
                { id: "supporting", label: "Supporting pages (build second)" },
                { id: "advanced", label: "Advanced pages (build third)" },
                { id: "prioritization", label: "How to prioritize across neighborhoods" },
                { id: "faq", label: "Common questions" },
              ].map(({ id, label }) => (
                <li key={id}>
                  <a href={`#${id}`} style={{
                    fontFamily: "var(--font-manrope, sans-serif)",
                    fontSize: "14px",
                    color: C.forest,
                    textDecoration: "underline",
                    textDecorationColor: C.gold,
                    textUnderlineOffset: "3px",
                  }}>{label}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* CORE PAGES */}
      <section id="core" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#5C8A6E]">
              <LayoutGrid className="h-3 w-3" strokeWidth={2} />
              Build these first
            </div>
            <h2 style={h2Style}>Core pages</h2>

            <p style={proseStyle}>
              Five page types that cover the highest-volume neighborhood queries. Build these before anything else. Together they anchor the topical cluster.
            </p>

            <PageTypeCard num="1" Icon={MapPin} title="Neighborhood overview" queryIntent="living in Winter Garden" wordCount="1,500-2,500 words" priority="Core">
              <p style={{ margin: "0 0 12px 0" }}>The anchor page. What the neighborhood is, who lives there, what defines the character. Should cover the full range at high level — a brief on dining, outdoor, schools, transportation, community feel, and price range.</p>
              <p style={{ margin: 0 }}>Links out to every other page in the neighborhood cluster. Named specifics throughout — real streets, real landmarks, real businesses. Schema: Place, Article, FAQPage.</p>
            </PageTypeCard>

            <PageTypeCard num="2" Icon={School} title="Schools and school districts" queryIntent="schools in Winter Garden Florida" wordCount="1,000-1,500 words" priority="Core">
              <p style={{ margin: "0 0 12px 0" }}>Every elementary, middle, and high school serving the neighborhood. Named school districts. Zoning boundaries. GreatSchools ratings. Recent bond measures and school board news.</p>
              <p style={{ margin: 0 }}>High-intent query — buyers with kids evaluate neighborhoods primarily on schools. Ranks for both &ldquo;schools in [neighborhood]&rdquo; and &ldquo;best schools in [city]&rdquo; queries.</p>
            </PageTypeCard>

            <PageTypeCard num="3" Icon={Home} title="Market update (monthly refresh)" queryIntent="Winter Garden real estate market 2026" wordCount="800-1,200 words" priority="Core">
              <p style={{ margin: "0 0 12px 0" }}>Recurring content — median sale price, days on market, inventory count, price trends over 3, 6, and 12 months. Comparison to the broader metro market.</p>
              <p style={{ margin: 0 }}>Monthly refresh keeps content fresh and drives repeat traffic. Buyers and sellers researching market timing return to check the numbers. Freshness signal for both Google and AI systems.</p>
            </PageTypeCard>

            <PageTypeCard num="4" Icon={Utensils} title="Dining and nightlife" queryIntent="best restaurants in Winter Garden" wordCount="800-1,200 words" priority="Core">
              <p style={{ margin: "0 0 12px 0" }}>Named restaurants organized by category — casual, upscale, coffee, breakfast, family-friendly (careful with Fair Housing language here — describe atmosphere, not intended customers). Include the small local places, not just chains.</p>
              <p style={{ margin: 0 }}>Buyers evaluating neighborhoods use dining as a proxy for lifestyle. This page also ranks for buyer research queries about &ldquo;what&apos;s [neighborhood] like&rdquo; that don&apos;t obviously map to a category.</p>
            </PageTypeCard>

            <PageTypeCard num="5" Icon={Bike} title="Outdoor and recreation" queryIntent="parks and trails in Winter Garden" wordCount="800-1,200 words" priority="Core">
              <p style={{ margin: "0 0 12px 0" }}>Named parks, trails, bike paths, playgrounds, sports facilities, boat ramps, dog parks. Distance to major recreation areas (state parks, beaches, hiking).</p>
              <p style={{ margin: 0 }}>Active-lifestyle buyers filter neighborhoods heavily on outdoor access. This page captures those queries and also feeds &ldquo;things to do in [neighborhood]&rdquo; buyer research.</p>
            </PageTypeCard>
          </div>
        </div>
      </section>

      {/* SUPPORTING PAGES */}
      <section id="supporting" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <LayoutGrid className="h-3 w-3" strokeWidth={2} />
              Build these second
            </div>
            <h2 style={h2Style}>Supporting pages</h2>

            <p style={proseStyle}>
              Four page types that deepen the cluster once the core is in place. Lower search volume individually but strengthen topical authority and capture long-tail queries.
            </p>

            <PageTypeCard num="6" Icon={Users} title="Community character and lifestyle" queryIntent="what is Winter Garden like" wordCount="800-1,200 words" priority="Supporting">
              <p style={{ margin: "0 0 12px 0" }}>The subjective &ldquo;vibe&rdquo; page. Historical context, demographic notes (careful with Fair Housing — describe the neighborhood, not the residents), architectural styles, community events, farmers markets, seasonal traditions.</p>
              <p style={{ margin: 0 }}>Captures searches from buyers doing lifestyle-first research. Also strong content for AI citation because it&apos;s exactly the &ldquo;what&apos;s it like living in&rdquo; query pattern LLMs synthesize answers for.</p>
            </PageTypeCard>

            <PageTypeCard num="7" Icon={Route} title="Transportation and commute" queryIntent="commute from Winter Garden to downtown Orlando" wordCount="800-1,000 words" priority="Supporting">
              <p style={{ margin: "0 0 12px 0" }}>Named routes, real drive times, public transit options, airport distance, walkability score, bike-friendliness. Specific commute paths to major employment centers.</p>
              <p style={{ margin: 0 }}>Commute is the #1 practical concern for most buyers. This page ranks well because commute queries have consistent volume and specific answers.</p>
            </PageTypeCard>

            <PageTypeCard num="8" Icon={ShoppingBag} title="Everyday amenities and services" queryIntent="grocery stores in Winter Garden" wordCount="800-1,000 words" priority="Supporting">
              <p style={{ margin: "0 0 12px 0" }}>Named grocery stores, pharmacies, hardware stores, banks, urgent care, veterinarians, gyms. The practical &ldquo;can I live my life here&rdquo; inventory.</p>
              <p style={{ margin: 0 }}>Lower search volume than dining or schools but consistent. Also feeds AI-answered queries about neighborhood convenience.</p>
            </PageTypeCard>

            <PageTypeCard num="9" Icon={Coffee} title="Family services and childcare" queryIntent="daycares in Winter Garden Florida" wordCount="800-1,000 words" priority="Supporting">
              <p style={{ margin: "0 0 12px 0" }}>Named daycares, preschools, after-school programs, pediatricians, family-focused activities. Note carefully — Fair Housing rules restrict describing neighborhoods as &ldquo;family-friendly,&rdquo; but describing the specific services (which exist regardless of who uses them) is fine.</p>
              <p style={{ margin: 0 }}>Highly specific search intent. Buyers with young children evaluate this actively. Also captures relocating buyers who need to find services before moving.</p>
            </PageTypeCard>
          </div>
        </div>
      </section>

      {/* ADVANCED PAGES */}
      <section id="advanced" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <LayoutGrid className="h-3 w-3" strokeWidth={2} />
              Build these third
            </div>
            <h2 style={h2Style}>Advanced pages</h2>

            <p style={proseStyle}>
              Three page types that address specialized buyer segments. Lower priority for most agents but high-value for the right specialization.
            </p>

            <PageTypeCard num="10" Icon={Building2} title="New construction and development" queryIntent="new construction homes in Winter Garden" wordCount="1,000-1,500 words" priority="Advanced">
              <p style={{ margin: "0 0 12px 0" }}>Named builders, active developments, planned communities, expected completion timelines, price ranges by phase. Updates required as inventory shifts.</p>
              <p style={{ margin: 0 }}>Specific buyer intent — new construction shoppers know they want new construction. Higher-intent traffic, though lower volume than overview pages.</p>
            </PageTypeCard>

            <PageTypeCard num="11" Icon={Landmark} title="Luxury and estate homes" queryIntent="luxury homes in Winter Garden" wordCount="1,000-1,500 words" priority="Advanced">
              <p style={{ margin: "0 0 12px 0" }}>Named luxury enclaves, gated communities, estate neighborhoods. Price thresholds that define &ldquo;luxury&rdquo; in this market. Specific streets or communities that anchor the luxury segment.</p>
              <p style={{ margin: 0 }}>Only worth building if you actually work luxury or want to. Otherwise it&apos;s a page that ranks for queries you can&apos;t serve well.</p>
            </PageTypeCard>

            <PageTypeCard num="12" Icon={Home} title="First-time buyer guide" queryIntent="first time home buyer in Winter Garden" wordCount="1,200-1,800 words" priority="Advanced">
              <p style={{ margin: "0 0 12px 0" }}>Down payment norms, closing cost expectations, first-time buyer programs, entry-level neighborhoods within the market, typical timeline expectations. Named lenders and programs available.</p>
              <p style={{ margin: 0 }}>High-intent long-tail queries. Captures buyers early in their journey when they&apos;re researching what&apos;s possible before contacting an agent.</p>
            </PageTypeCard>
          </div>
        </div>
      </section>

      {/* PRIORITIZATION — FOREST DARK */}
      <section id="prioritization" className="relative overflow-hidden bg-[#14271E] py-20 sm:py-24">
        <div className="pointer-events-none absolute inset-0" style={{
          backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }} />
        <div className={`relative ${CONTENT}`}>
          <div className={READING}>
            <SectionLabel light>The strategic question</SectionLabel>
            <h2 style={{ ...h2Style, color: C.creamWarm }}>How to prioritize across neighborhoods</h2>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              12 page types × N neighborhoods = a lot of content. Real math on prioritization.
            </p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>Depth beats breadth</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              An agent website with 5 neighborhoods × 8 page types (40 pages, all substantive) will rank meaningfully better than the same agent with 20 neighborhoods × 2 page types (40 pages, but shallow). Topical clusters signal authority to Google and to AI systems. Thin coverage across many neighborhoods signals nothing.
            </p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>Start narrow, expand deliberately</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              For most agents, the right sequence:
            </p>
            <BulletList light items={[
              <><strong style={{ color: C.gold }}>Phase 1 (months 1-2):</strong> One primary neighborhood, all 5 core page types</>,
              <><strong style={{ color: C.gold }}>Phase 2 (months 3-4):</strong> Same neighborhood, add 4 supporting page types</>,
              <><strong style={{ color: C.gold }}>Phase 3 (months 5-6):</strong> Second neighborhood, all 5 core page types</>,
              <><strong style={{ color: C.gold }}>Phase 4 (months 7-12):</strong> Fill in advanced pages for primary neighborhood, add supporting pages for second</>,
              <><strong style={{ color: C.gold }}>Phase 5 (year 2+):</strong> Expand to third and fourth neighborhoods with same pattern</>,
            ]} />

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The market update trap</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              Market update pages promise fresh monthly content and often get abandoned after two updates. Only commit to market update pages you&apos;ll actually maintain. A stale market update page hurts more than no market update page — Google and buyers both notice the last-updated date reads &ldquo;March 2025.&rdquo;
            </p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>What to skip</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              Not every page type serves every agent. Skip:
            </p>
            <BulletList light items={[
              <>Luxury pages if you don&apos;t work luxury</>,
              <>New construction pages if there&apos;s no active new construction in the market</>,
              <>Family services pages if you can&apos;t maintain accurate daycare / school info</>,
              <>Market update pages if you won&apos;t commit to monthly refresh</>,
            ]} />

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)", marginBottom: 0 }}>
              For the framework on writing individual pages so AI systems consistently cite them, see <Link href="/learn/neighborhood-content-that-ai-cites" style={{ color: C.gold, textDecoration: "underline", textDecorationColor: C.gold, textUnderlineOffset: "3px" }}>how to write neighborhood content that AI actually cites</Link>.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="bg-[#EFEAE0] py-20 sm:py-24">
        <div className={CONTENT}>
          <div className={READING}>
            <SectionLabel>Common questions</SectionLabel>
            <h2 style={h2Style}>Common questions</h2>

            <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "24px" }}>
              {[
                { q: "How many neighborhood pages does an agent website really need?", a: "The 12 page types in this piece are a comprehensive inventory. Most agents don't need all 12 for every neighborhood — start with 3-5 core page types (neighborhood overview, schools, dining, outdoor, and market update) per neighborhood and expand based on which pages actually rank and drive leads." },
                { q: "Which neighborhood page type ranks fastest in Google?", a: "Neighborhood overview pages typically rank fastest because they match the highest-volume query pattern ('best neighborhoods in [city]', 'living in [neighborhood]'). School district pages and market update pages follow because those queries have consistent monthly search demand." },
                { q: "How long should each neighborhood page be?", a: "800-1,500 words is the sweet spot for most page types. Overview pages can go longer (1,500-2,500 words). Category-specific pages (dining, schools, outdoor) work at 800-1,200 words." },
                { q: "Do neighborhood pages get cited by ChatGPT and Claude?", a: "Yes, when structured properly. AI systems consistently cite neighborhood content with named specifics, verifiable data, structured markup, and dated updates. Generic neighborhood pages that describe locations in vague terms get skipped in AI citations regardless of Google ranking." },
                { q: "Should agent websites duplicate MLS neighborhood content?", a: "No. LLMs and Google both deduplicate content that appears in multiple places. Agent website neighborhood pages should include distinct content — expanded local knowledge, agent voice, hyperlocal specifics MLS descriptions can't cover." },
                { q: "How often should neighborhood pages be updated?", a: "Market update pages need monthly refreshes to stay current. Overview and category pages need quarterly review to catch business closures and neighborhood changes. School and infrastructure pages need annual updates." },
                { q: "Is it worth building 12 neighborhood pages if I only work in one neighborhood?", a: "For agents focused on a single neighborhood, yes — you're building a topical authority hub that dominates every long-tail query for that area. Better to own 12 pages ranking for 'Winter Garden' than 3 pages competing weakly across 4 neighborhoods." },
                { q: "What's the biggest mistake agents make with neighborhood website content?", a: "Building thin content across too many neighborhoods rather than deep content across a few. An agent website with 20 neighborhood pages of 300 words each will rank worse than the same agent with 5 neighborhoods x 4 page types at 1,000 words each. Depth compounds; breadth without depth dilutes." },
              ].map(({ q, a }, i) => (
                <details key={i} style={{
                  borderRadius: "12px",
                  border: `1px solid ${C.border}`,
                  background: C.bgCard,
                  padding: "20px 24px",
                }}>
                  <summary style={{
                    fontFamily: "var(--font-manrope, sans-serif)",
                    fontSize: "16px",
                    fontWeight: 500,
                    color: C.ink,
                    cursor: "pointer",
                    listStyle: "none",
                    letterSpacing: "-0.005em",
                  }}>{q}</summary>
                  <div style={{ marginTop: "14px", fontSize: "14.5px", lineHeight: 1.7, color: C.inkSoft }}>{a}</div>
                </details>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* SOURCES */}
      <section className="bg-[#EFEAE0] py-10">
        <div className={CONTENT}>
          <div className={READING}>
            <p style={{
              fontFamily: "var(--font-jetbrains, monospace)",
              fontSize: "12px",
              lineHeight: 1.6,
              color: C.muted,
              textAlign: "center",
              fontStyle: "italic",
            }}>
              Sources: Google Search Central documentation on topical authority; Schema.org Place and LocalBusiness vocabulary; observations from Metes GSC data and LangSmith production traces; internal Metes references to Weeks 3, 6, and 8. Not a guarantee of Google rankings or AI citation outcomes — SEO and GEO signals are directional guidance based on observed patterns.
            </p>
          </div>
        </div>
      </section>

      {/* FINAL CTA — FOREST DARK */}
      <section className="relative overflow-hidden bg-[#14271E] py-20 sm:py-24">
        <div className="pointer-events-none absolute inset-0" style={{
          backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }} />
        <div className={`relative ${CONTENT}`}>
          <div style={{ maxWidth: "760px" }}>
            <SectionLabel light>The through-line</SectionLabel>
            <h2 className="mb-5 font-manrope text-[clamp(28px,4vw,42px)] font-medium leading-[1.1] tracking-[0.005em] text-[#F4F0E8]">
              Depth beats breadth. <em className="not-italic text-[#B89968]">Own a neighborhood completely before adding the next one.</em>
            </h2>
            <p className="mb-8 max-w-[620px] text-[clamp(15px,1.3vw,17px)] leading-[1.6] text-[rgba(244,240,232,0.78)]">
              12 page types build a topical authority cluster that Google and AI systems both reward. Start with the 5 core types, expand deliberately, refresh consistently. Same discipline that makes any single page cited applies to the whole cluster: named specifics, verifiable data, structured markup, dated updates.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/tools/neighborhood-guide-generator" className="inline-flex items-center gap-2 rounded-[9px] bg-[#B89968] px-7 py-3.5 font-manrope text-[14px] font-medium text-[#14271E] no-underline transition-colors hover:bg-[#9A7E50] hover:text-[#F4F0E8]">
                Generate a neighborhood guide free
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
              <Link href="/" className="inline-flex items-center gap-2 rounded-[9px] border border-[rgba(244,240,232,0.3)] bg-transparent px-7 py-3.5 font-manrope text-[14px] font-medium text-[#F4F0E8] no-underline hover:border-[rgba(244,240,232,0.6)]">
                See the full Metes kit — $35
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}