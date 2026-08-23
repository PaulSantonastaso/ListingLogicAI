import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, MapPin, Search, FileCheck, XCircle, Compass } from "lucide-react";
import Footer from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "How to Write Neighborhood Content That AI Actually Cites | Metes",
  description:
    "ChatGPT, Claude, and Google AI Overview cite named specifics, not generic descriptors. Here's the framework for neighborhood content that gets pulled into buyer research answers.",
  keywords: [
    "neighborhood content real estate",
    "neighborhood guide generator",
    "ai citations neighborhood",
    "google places grounding",
    "geo neighborhood pages",
    "how to write neighborhood description",
    "real estate neighborhood seo",
    "chatgpt neighborhood research",
  ],
  alternates: {
    canonical: "https://www.metes.app/learn/neighborhood-content-that-ai-cites",
  },
  openGraph: {
    title: "How to Write Neighborhood Content That AI Actually Cites",
    description:
      "The framework for neighborhood content that gets pulled by ChatGPT, Claude, and Google AI Overview when buyers research neighborhoods.",
    url: "https://www.metes.app/learn/neighborhood-content-that-ai-cites",
    siteName: "Metes",
    type: "article",
    images: [
      {
        url: "https://www.metes.app/og/neighborhood-content-that-ai-cites.png",
        width: 1200,
        height: 630,
        alt: "How to write neighborhood content that AI cites",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "How to Write Neighborhood Content That AI Actually Cites",
    description: "Framework for neighborhood content that gets pulled by ChatGPT and Google AI Overview.",
    images: ["https://www.metes.app/og/neighborhood-content-that-ai-cites.png"],
  },
  robots: { index: true, follow: true },
};

const SCHEMA_JSON_LD = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://www.metes.app/learn/neighborhood-content-that-ai-cites#article",
      "headline": "How to Write Neighborhood Content That AI Actually Cites",
      "description":
        "The framework for neighborhood content that gets pulled by AI systems when buyers research neighborhoods.",
      "image": "https://www.metes.app/og/neighborhood-content-that-ai-cites.png",
      "datePublished": "2026-08-19",
      "dateModified": "2026-08-19",
      "author": { "@type": "Organization", "name": "Metes Editorial", "url": "https://www.metes.app" },
      "publisher": {
        "@type": "Organization",
        "name": "Metes",
        "url": "https://www.metes.app",
        "logo": { "@type": "ImageObject", "url": "https://www.metes.app/logo.png" },
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://www.metes.app/learn/neighborhood-content-that-ai-cites",
      },
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.metes.app/learn/neighborhood-content-that-ai-cites#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Why do LLMs cite named specifics over generic descriptors?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "LLMs cross-reference claims against verifiable sources like Google Places, business directories, and third-party databases. Named specifics (like 'Old Fox Books & Coffeehouse two blocks away') can be verified. Generic descriptors (like 'coffee shop nearby') cannot. Content that includes verifiable specifics carries higher citation weight than content that describes properties in generalities.",
          },
        },
        {
          "@type": "Question",
          "name": "What is Google Places grounding?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Google Places grounding is the practice of generating neighborhood content from live Google Places API data rather than model imagination. Every named business, park, and landmark in the output comes from real Places data, meaning distances, ratings, and business names are verifiable rather than hallucinated. This is the technical difference between neighborhood content AI cites versus content it skips.",
          },
        },
        {
          "@type": "Question",
          "name": "Should real estate agents write neighborhood content manually or use a tool?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Depends on volume and quality control. Manual writing takes 30-60 minutes per neighborhood if done well with actual research. Tools that ground output in Google Places data produce comparable quality in seconds. If you write one or two neighborhood pieces per year, manual is fine. If you're doing 10+ listings per year, a tool with proper grounding pays for itself in time savings alone.",
          },
        },
        {
          "@type": "Question",
          "name": "What structured data should neighborhood pages include?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "At minimum, Place schema for the neighborhood itself, LocalBusiness schema for named businesses referenced, and Article schema for the content wrapper. FAQPage schema if you include a Q&A section. Structured data makes content programmatically legible to AI systems and improves citation surface.",
          },
        },
        {
          "@type": "Question",
          "name": "How long should neighborhood content be?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Long enough to include real specifics, short enough that every sentence adds value. For MLS description use, 100-200 words focused on named specifics. For agent website neighborhood pages, 800-1,500 words covering dining, outdoor, everyday services, and community character with named examples in each category. Bloating for length hurts more than helps.",
          },
        },
        {
          "@type": "Question",
          "name": "Does Fair Housing compliance affect neighborhood content citation?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. LLMs are trained to avoid problematic language, which includes Fair Housing violations. 'Family-friendly neighborhood' is both a Fair Housing violation and a phrase LLMs deprioritize. The same discipline that keeps content compliant makes it more citable.",
          },
        },
        {
          "@type": "Question",
          "name": "How often should neighborhood content be updated?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Refresh dates every 6-12 months. Business closures, new restaurants, and neighborhood changes mean specifics get stale. Visibly dated content ('Last updated August 2026') carries more citation weight than undated content. When a referenced business closes, update the reference within a month or the citation weight drops.",
          },
        },
        {
          "@type": "Question",
          "name": "What's the biggest mistake agents make writing neighborhood content?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Generic language. Writing 'quiet neighborhood with good schools and easy access to shopping' provides no verification anchors for AI systems. Writing 'Winter Garden Elementary is three blocks north; Central Ford Cafe on Plant Street serves breakfast until 2pm' provides five verifiable claims in one sentence. Generic descriptions get skipped; named specifics get cited.",
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

function ExampleCompare({ generic, specific }: { generic: string; specific: string }) {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "12px",
      marginBottom: "18px",
    }}>
      <div style={{
        background: "rgba(201,123,92,0.06)",
        border: `1px solid rgba(201,123,92,0.25)`,
        borderRadius: "10px",
        padding: "18px 20px",
      }}>
        <div style={{
          fontFamily: "var(--font-jetbrains, monospace)",
          fontSize: "10px",
          letterSpacing: "0.14em",
          textTransform: "uppercase",
          color: C.warn,
          marginBottom: "8px",
        }}>Generic — skipped</div>
        <p style={{
          fontFamily: "var(--font-manrope, sans-serif)",
          fontSize: "14.5px",
          lineHeight: 1.6,
          color: C.ink,
          margin: 0,
        }}>{generic}</p>
      </div>
      <div style={{
        background: "rgba(92,138,110,0.06)",
        border: `1px solid rgba(92,138,110,0.25)`,
        borderRadius: "10px",
        padding: "18px 20px",
      }}>
        <div style={{
          fontFamily: "var(--font-jetbrains, monospace)",
          fontSize: "10px",
          letterSpacing: "0.14em",
          textTransform: "uppercase",
          color: C.pass,
          marginBottom: "8px",
        }}>Specific — cited</div>
        <p style={{
          fontFamily: "var(--font-manrope, sans-serif)",
          fontSize: "14.5px",
          lineHeight: 1.6,
          color: C.ink,
          margin: 0,
        }}>{specific}</p>
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

export default function NeighborhoodContentAICitesPage() {
  return (
    <div className="min-h-screen bg-[#EFEAE0]">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(SCHEMA_JSON_LD) }} />
      <Header />

      {/* HERO */}
      <section className="border-b border-[rgba(20,39,30,0.10)] bg-[#F4F0E8]">
        <div className="mx-auto w-full max-w-[960px] px-6 py-16 sm:py-20 lg:px-8">
          <div className="mx-auto max-w-[760px]">
            <SectionLabel>Guide · Neighborhood content for GEO</SectionLabel>
            <h1 className="mb-4 font-manrope text-[clamp(28px,4.5vw,48px)] font-medium leading-[1.08] tracking-[0.005em] text-[#14271E]">
              How to write neighborhood content <em className="not-italic text-[#9A7E50]">that AI actually cites</em>.
            </h1>
            <p className="mb-6 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              When a buyer asks ChatGPT &ldquo;what&apos;s it like living in Winter Garden&rdquo; or asks Perplexity to compare two neighborhoods, the AI synthesizes an answer from multiple sources. Some content gets cited. Most gets skipped.
            </p>
            <p className="mb-8 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              This piece is the framework for writing neighborhood content that ends up in the answers, not on the cutting room floor. Named specifics, verifiable data, structured markup, and the discipline that separates content AI cites from content AI ignores.
            </p>
            <p className="text-[13px] font-mono uppercase tracking-[0.08em] text-[rgba(20,39,30,0.55)]">
              Last updated: August 19, 2026 · ~14 minute read
            </p>
          </div>
        </div>
      </section>

      {/* TLDR */}
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
                LLMs cite neighborhood content that includes named specifics — real businesses, real streets, real distances — because those claims can be verified against Google Places and third-party sources. Content that describes properties in generalities (&ldquo;quiet neighborhood, close to shops&rdquo;) gets skipped.
              </p>
              <p style={proseStyle}>
                The same discipline that makes content Fair Housing compliant and that avoids AI tells also makes content citable. Named streets beat &ldquo;a quiet street.&rdquo; Named restaurants beat &ldquo;dining options.&rdquo; Verified schools beat &ldquo;good schools.&rdquo;
              </p>
              <p style={{ ...proseStyle, marginBottom: 0 }}>
                This piece breaks down the framework — grounding sources, structural requirements, common failure modes, and when a tool matters versus when to write manually.
              </p>
            </div>

            <div className="mb-3 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">Jump to</div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "8px" }}>
              {[
                { id: "why-specifics", label: "Why named specifics get cited" },
                { id: "grounding", label: "What Google Places grounding actually does" },
                { id: "framework", label: "The framework: research, verify, structure, publish" },
                { id: "structure", label: "Structural requirements for citation" },
                { id: "failures", label: "Common failure modes" },
                { id: "tool-vs-manual", label: "When to use a tool vs write manually" },
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

      {/* WHY SPECIFICS — FOREST DARK */}
      <section id="why-specifics" className="relative overflow-hidden bg-[#14271E] py-20 sm:py-24">
        <div className="pointer-events-none absolute inset-0" style={{
          backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }} />
        <div className={`relative ${CONTENT}`}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#D9C49C]">
              <Search className="h-3 w-3" strokeWidth={2} />
              The core principle
            </div>
            <h2 style={{ ...h2Style, color: C.creamWarm }}>Why named specifics get cited</h2>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              When ChatGPT, Claude, Perplexity, or Google AI Overview synthesizes an answer to a neighborhood question, it looks for content it can verify. Named specifics can be cross-referenced against Google Places, business directories, mapping data, and third-party sources. Generic descriptors cannot.
            </p>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              This isn&apos;t speculation. It&apos;s observable pattern behavior across multiple LLM systems. AI-generated answers to neighborhood queries consistently pull named businesses, named streets, named schools, and verified distances. Generic content — the kind most listing descriptions and agent-website neighborhood pages contain — doesn&apos;t show up in the answers.
            </p>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>
              A short caveat before continuing: LLM citation behavior is observable, not documented. Everything in this piece is inference from consistent patterns, not confirmed mechanisms from OpenAI or Anthropic. Treat it as directional guidance grounded in real observation.
            </p>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)", marginBottom: 0 }}>
              For more on how buyers actually use AI to research neighborhoods in 2026 and what the broader shift means for listing marketing, see <Link href="/learn/how-buyers-research-with-ai" style={{ color: C.gold, textDecoration: "underline", textDecorationColor: C.gold, textUnderlineOffset: "3px" }}>how buyers research neighborhoods with AI</Link>.
            </p>
          </div>
        </div>
      </section>

      {/* GROUNDING */}
      <section id="grounding" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <MapPin className="h-3 w-3" strokeWidth={2} />
              The technical differentiation
            </div>
            <h2 style={h2Style}>What Google Places grounding actually does</h2>

            <p style={proseStyle}>
              Google Places is the world&apos;s largest verified database of local businesses. Names, addresses, hours, ratings, categories, distances, phone numbers. When neighborhood content is generated from Places data rather than model imagination, every named specific has a verification anchor.
            </p>

            <p style={proseStyle}>
              The mechanics are simple: query Places API for businesses within a defined radius of an address, filter by relevance and rating, then generate content that references only businesses that exist in the returned data. No hallucination possible because the model is constrained to the verified list.
            </p>

            <p style={proseStyle}>
              The output looks different from ungrounded generation:
            </p>

            <ExampleCompare
              generic="This neighborhood offers excellent dining options, beautiful parks, and convenient access to shopping."
              specific="Cinzzetti's serves Italian family-style two blocks north; Northwest Open Space anchors weekend runs with trails through 200 acres; Whole Foods Market on 120th Ave handles grocery runs in under 10 minutes."
            />

            <p style={proseStyle}>
              The generic version can be written about any neighborhood in America. The specific version can only describe one place — the one where those businesses actually exist. That specificity is what LLMs cite.
            </p>

            <p style={proseStyle}>
              Grounding is also what prevents the credibility-destroying failure mode: fabricated businesses. When an ungrounded model generates neighborhood content, it might invent a plausible-sounding restaurant that doesn&apos;t exist. Buyers who Google it and find nothing lose trust. LLMs that cross-reference and find nothing deprioritize the content permanently.
            </p>
          </div>
        </div>
      </section>

      {/* FRAMEWORK */}
      <section id="framework" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <Compass className="h-3 w-3" strokeWidth={2} />
              The framework
            </div>
            <h2 style={h2Style}>Research, verify, structure, publish</h2>

            <p style={proseStyle}>
              The four-step framework for neighborhood content that AI systems consistently cite.
            </p>

            <h3 style={h3Style}>1. Research — pull real data from real sources</h3>
            <p style={proseStyle}>
              Start with Google Places or a similar verified source. Pull businesses within a 1-2 mile radius of the property. Note category, rating, review count, and distance for each.
            </p>
            <p style={proseStyle}>
              For a listing agent writing one property at a time, this can be manual research: 15-20 minutes on Google Maps identifying key destinations. For volume workflows, this is where a tool with Places API access pays off — same data, seconds instead of minutes.
            </p>

            <h3 style={h3Style}>2. Verify — cross-check every specific</h3>
            <p style={proseStyle}>
              Every named business, distance, and detail should be verifiable. Confirm business names against Google Maps. Check distances via a real routing tool. Verify school district assignments through the district website, not general knowledge.
            </p>
            <p style={proseStyle}>
              Fabricated specifics are the failure mode that destroys credibility permanently. A single wrong distance or invented restaurant caught by a buyer damages trust for every future listing. LLMs that verify and find fabrication deprioritize the source.
            </p>

            <h3 style={h3Style}>3. Structure — organize for both readers and LLMs</h3>
            <p style={proseStyle}>
              Group content by category — dining, outdoor, everyday services, community character. Each category should have 2-4 named examples with brief context. Include a lifestyle paragraph that weaves specifics into narrative form.
            </p>
            <p style={proseStyle}>
              Structural pattern that works for both humans and LLMs: named specifics in list format (easy to scan, easy for LLMs to extract), lifestyle paragraph in prose (context for humans, narrative synthesis for LLMs).
            </p>

            <h3 style={h3Style}>4. Publish — with proper markup and dates</h3>
            <p style={proseStyle}>
              Every neighborhood page needs Schema.org markup — Place schema for the neighborhood itself, LocalBusiness schema for named businesses referenced, Article schema for the content wrapper. Add a visible &ldquo;last updated&rdquo; date. Include structured data for coordinates when possible.
            </p>
            <p style={proseStyle}>
              Undated content signals stale content to LLMs. Content without Schema.org markup gets pulled less than the same content with proper markup. Both are cheap to add.
            </p>
          </div>
        </div>
      </section>

      {/* STRUCTURE */}
      <section id="structure" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#5C8A6E]">
              <FileCheck className="h-3 w-3" strokeWidth={2.5} />
              Actionable
            </div>
            <h2 style={h2Style}>Structural requirements for citation</h2>

            <p style={proseStyle}>
              The specific structural elements that separate cited content from skipped content.
            </p>

            <h3 style={h3Style}>Named entities in every claim</h3>
            <p style={proseStyle}>
              Every claim about the neighborhood should be anchored to a named entity. Never &ldquo;close to shopping&rdquo; — always &ldquo;5 minutes to Winter Garden Village.&rdquo; Never &ldquo;good schools&rdquo; — always &ldquo;zoned for Winter Garden Elementary (rated 8/10 on GreatSchools).&rdquo;
            </p>
            <ExampleCompare
              generic="The neighborhood has great restaurants and beautiful parks."
              specific="Three named restaurants within walking distance (Central Ford Cafe, Locust & Vine, The Yellow Dog); Central Park Winter Garden with the West Orange Trail bike path anchors weekend recreation."
            />

            <h3 style={h3Style}>Verified distances and coordinates</h3>
            <p style={proseStyle}>
              Distances should be verifiable via mapping tools. &ldquo;Two blocks north,&rdquo; &ldquo;5-minute drive,&rdquo; &ldquo;quarter mile east.&rdquo; When possible, include coordinates in structured data so LLMs can map the property to its geographic context.
            </p>

            <h3 style={h3Style}>Schema.org markup</h3>
            <p style={proseStyle}>
              Minimum viable markup for a neighborhood page:
            </p>
            <BulletList items={[
              <><strong>Place schema</strong> for the neighborhood itself with name, description, geo coordinates</>,
              <><strong>LocalBusiness schema</strong> for each named business referenced</>,
              <><strong>Article schema</strong> for the content wrapper with author, datePublished, dateModified</>,
              <><strong>FAQPage schema</strong> if the page includes Q&amp;A content</>,
              <><strong>BreadcrumbList schema</strong> for navigation context</>,
            ]} />

            <h3 style={h3Style}>Visible dates</h3>
            <p style={proseStyle}>
              &ldquo;Last updated August 2026&rdquo; near the top of the page. Not buried in a footer. Not in a meta tag alone. Visible to both readers and LLMs. Dates signal freshness, and freshness weights citation.
            </p>

            <h3 style={h3Style}>Category structure</h3>
            <p style={proseStyle}>
              Content organized into scannable categories works better than long unstructured prose. Dining, outdoor, everyday services, community character, transportation. Each with named examples. LLMs extract structured content more reliably than unstructured narrative.
            </p>

            <h3 style={h3Style}>FAQ format for common questions</h3>
            <p style={proseStyle}>
              Question-answer pairs at the bottom of the page match the format LLMs return when synthesizing answers. Questions like &ldquo;What are the schools in Winter Garden?&rdquo; or &ldquo;What&apos;s the commute to downtown Orlando?&rdquo; give LLMs directly extractable content.
            </p>

            <h3 style={h3Style}>Fair Housing compliance</h3>
            <p style={proseStyle}>
              LLMs are trained to avoid problematic language. &ldquo;Family-friendly neighborhood&rdquo; is both a Fair Housing violation and a phrase LLMs deprioritize. The same discipline that keeps content compliant makes it more citable. See <Link href="/learn/fair-housing-words-to-avoid" style={inlineLink}>the Fair Housing word list</Link> for the specific phrases to avoid.
            </p>
          </div>
        </div>
      </section>

      {/* FAILURES */}
      <section id="failures" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#C97B5C]">
              <XCircle className="h-3 w-3" strokeWidth={2} />
              The traps
            </div>
            <h2 style={h2Style}>Common failure modes</h2>

            <h3 style={h3Style}>Generic descriptors</h3>
            <p style={proseStyle}>
              The single most common failure. Writing about &ldquo;quiet streets,&rdquo; &ldquo;good schools,&rdquo; &ldquo;convenient shopping&rdquo; provides zero verification anchors. Content reads AI-generated to both humans and LLMs. Skipped in citation.
            </p>

            <h3 style={h3Style}>Fabricated specifics</h3>
            <p style={proseStyle}>
              Made-up business names, wrong distances, incorrect school district assignments. Once caught by verification, the whole site&apos;s citation weight drops. Not just the specific page. LLMs treat fabrication as a source-level problem.
            </p>

            <h3 style={h3Style}>Copy-paste across neighborhoods</h3>
            <p style={proseStyle}>
              Writing one neighborhood description and lightly modifying it for each listing. LLMs deduplicate near-identical content. Only one version gets cited, usually the one on the highest-authority source (a portal, not the agent site). Distinct content per neighborhood is required.
            </p>

            <h3 style={h3Style}>AI tells without editing</h3>
            <p style={proseStyle}>
              Content that reads AI-generated gets deprioritized by LLM training. The <Link href="/learn/ai-listing-description-tells" style={inlineLink}>six categories of AI tells</Link> — em-dash pairs, superlative escalation, cliché generation, symmetric sentence structure — all apply to neighborhood content. Content that hits three or more categories gets skipped.
            </p>

            <h3 style={h3Style}>Missing structured data</h3>
            <p style={proseStyle}>
              Content that&apos;s citable in prose but lacks Schema.org markup gets pulled less. Structured markup is the difference between programmatically legible content and content the LLM has to guess about.
            </p>

            <h3 style={h3Style}>Stale references</h3>
            <p style={proseStyle}>
              Named businesses close. New restaurants open. Named schools consolidate. Content that references businesses that no longer exist fails verification when LLMs check. Regular refresh cycles matter — every 6-12 months at minimum.
            </p>
          </div>
        </div>
      </section>

      {/* TOOL VS MANUAL */}
      <section id="tool-vs-manual" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <SectionLabel>The practical question</SectionLabel>
            <h2 style={h2Style}>When to use a tool vs write manually</h2>

            <p style={proseStyle}>
              The honest math on neighborhood content workflow.
            </p>

            <h3 style={h3Style}>Manual writing works when</h3>
            <BulletList items={[
              <>Volume is low (1-3 neighborhoods per year)</>,
              <>You know the specific area deeply and can pull specifics from memory</>,
              <>The property is in a specialized market where verified data is thin</>,
              <>You want complete voice control over every sentence</>,
            ]} />
            <p style={proseStyle}>
              Time cost: 30-60 minutes per neighborhood done properly with research and verification. Faster than that and you&apos;re probably skipping the verification step, which produces content that fails LLM citation.
            </p>

            <h3 style={h3Style}>Tools with Places grounding win when</h3>
            <BulletList items={[
              <>Volume is meaningful (10+ neighborhoods per year)</>,
              <>You&apos;re working in markets where you don&apos;t have deep personal knowledge</>,
              <>You need consistent format across many properties</>,
              <>You want to verify every specific automatically rather than manually</>,
            ]} />
            <p style={proseStyle}>
              Tools that ground output in Google Places data produce comparable quality in seconds. The tradeoff is voice control — grounded output is more constrained than freely-written content. For most listing agents, the constraint is a feature (prevents hallucination and drift) rather than a bug.
            </p>

            <h3 style={h3Style}>The hybrid approach</h3>
            <p style={proseStyle}>
              Some agents use tools for the research and structural draft, then edit for voice and add personal knowledge that Places data can&apos;t capture. Best of both — verified specifics as the foundation, agent expertise as the polish.
            </p>

            <p style={proseStyle}>
              Metes takes the tool-first approach: Google Places grounding provides the verified data, the LLM chain generates lifestyle content constrained to that data, and the output is delivered as MLS-ready copy plus the full neighborhood guide. See <Link href="/learn/neighborhood-description-examples" style={inlineLink}>real neighborhood description examples</Link> across 12 markets for what grounded output looks like in practice.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-20 sm:py-24">
        <div className={CONTENT}>
          <div className={READING}>
            <SectionLabel>Common questions</SectionLabel>
            <h2 style={h2Style}>Common questions</h2>

            <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "24px" }}>
              {[
                { q: "Why do LLMs cite named specifics over generic descriptors?", a: "LLMs cross-reference claims against verifiable sources like Google Places, business directories, and third-party databases. Named specifics (like 'Old Fox Books & Coffeehouse two blocks away') can be verified. Generic descriptors (like 'coffee shop nearby') cannot. Content that includes verifiable specifics carries higher citation weight than content that describes properties in generalities." },
                { q: "What is Google Places grounding?", a: "Google Places grounding is the practice of generating neighborhood content from live Google Places API data rather than model imagination. Every named business, park, and landmark in the output comes from real Places data, meaning distances, ratings, and business names are verifiable rather than hallucinated." },
                { q: "Should real estate agents write neighborhood content manually or use a tool?", a: "Depends on volume and quality control. Manual writing takes 30-60 minutes per neighborhood if done well with actual research. Tools that ground output in Google Places data produce comparable quality in seconds. If you write one or two neighborhood pieces per year, manual is fine. If you're doing 10+ listings per year, a tool with proper grounding pays for itself in time savings alone." },
                { q: "What structured data should neighborhood pages include?", a: "At minimum, Place schema for the neighborhood itself, LocalBusiness schema for named businesses referenced, and Article schema for the content wrapper. FAQPage schema if you include a Q&A section. Structured data makes content programmatically legible to AI systems and improves citation surface." },
                { q: "How long should neighborhood content be?", a: "Long enough to include real specifics, short enough that every sentence adds value. For MLS description use, 100-200 words focused on named specifics. For agent website neighborhood pages, 800-1,500 words covering dining, outdoor, everyday services, and community character with named examples in each category." },
                { q: "Does Fair Housing compliance affect neighborhood content citation?", a: "Yes. LLMs are trained to avoid problematic language, which includes Fair Housing violations. 'Family-friendly neighborhood' is both a Fair Housing violation and a phrase LLMs deprioritize. The same discipline that keeps content compliant makes it more citable." },
                { q: "How often should neighborhood content be updated?", a: "Refresh dates every 6-12 months. Business closures, new restaurants, and neighborhood changes mean specifics get stale. Visibly dated content ('Last updated August 2026') carries more citation weight than undated content." },
                { q: "What's the biggest mistake agents make writing neighborhood content?", a: "Generic language. Writing 'quiet neighborhood with good schools and easy access to shopping' provides no verification anchors for AI systems. Writing 'Winter Garden Elementary is three blocks north; Central Ford Cafe on Plant Street serves breakfast until 2pm' provides five verifiable claims in one sentence." },
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
              Sources: Google Places API documentation; Schema.org neighborhood and Place vocabulary; observations from LangSmith production traces of Metes neighborhood chain; internal Metes references to Weeks 3, 4, 6, and 8. LLM citation behavior is observable, not documented — inference from consistent patterns, not confirmed mechanisms.
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
              Named specifics get cited. <em className="not-italic text-[#B89968]">Generic descriptors get skipped.</em>
            </h2>
            <p className="mb-8 max-w-[620px] text-[clamp(15px,1.3vw,17px)] leading-[1.6] text-[rgba(244,240,232,0.78)]">
              Write neighborhood content the same way Metes generates it — Google Places grounded, verified specifics, structured markup, Fair Housing safe. The same discipline that makes content trustworthy to buyers makes it citable to AI systems.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/tools/neighborhood-guide-generator" className="inline-flex items-center gap-2 rounded-[9px] bg-[#B89968] px-7 py-3.5 font-manrope text-[14px] font-medium text-[#14271E] no-underline transition-colors hover:bg-[#9A7E50] hover:text-[#F4F0E8]">
                Try the free Neighborhood Guide Generator
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