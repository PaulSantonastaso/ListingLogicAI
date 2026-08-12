import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Sparkles, Search, FileCheck, Globe, XCircle, TrendingDown } from "lucide-react";
import Footer from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "How Buyers Research Neighborhoods With AI in 2026 | Metes",
  description:
    "Zillow, Redfin, and Realtor.com all have ChatGPT apps now. Google's March 2026 Core Update rewards hyper-local content. Here's what your listings need to say to get cited by AI.",
  keywords: [
    "how buyers use chatgpt real estate",
    "ai citations real estate listings",
    "geo real estate 2026",
    "realtor.com chatgpt integration",
    "zillow chatgpt app",
    "generative engine optimization real estate",
    "ai listing description ranking",
    "buyer research ai 2026",
  ],
  alternates: {
    canonical: "https://www.metes.app/learn/how-buyers-research-with-ai",
  },
  openGraph: {
    title: "How Buyers Research Neighborhoods With AI in 2026",
    description:
      "What changed in the buyer research funnel, what LLMs actually cite, and what listing content needs to say for AI to include it.",
    url: "https://www.metes.app/learn/how-buyers-research-with-ai",
    siteName: "Metes",
    type: "article",
    images: [
      {
        url: "https://www.metes.app/og/how-buyers-research-with-ai.png",
        width: 1200,
        height: 630,
        alt: "How buyers research neighborhoods with AI in 2026",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "How Buyers Research Neighborhoods With AI in 2026",
    description: "The buyer research funnel changed. Here's what your content needs to say.",
    images: ["https://www.metes.app/og/how-buyers-research-with-ai.png"],
  },
  robots: { index: true, follow: true },
};

const SCHEMA_JSON_LD = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://www.metes.app/learn/how-buyers-research-with-ai#article",
      "headline": "How Buyers Actually Research Neighborhoods With AI in 2026 (and What Your Listing Needs to Say)",
      "description":
        "What changed in the buyer research funnel this year, what LLMs actually cite, and what listing content needs to be for AI to include it.",
      "image": "https://www.metes.app/og/how-buyers-research-with-ai.png",
      "datePublished": "2026-07-29",
      "dateModified": "2026-07-29",
      "author": {
        "@type": "Organization",
        "name": "Metes Editorial",
        "url": "https://www.metes.app",
      },
      "publisher": {
        "@type": "Organization",
        "name": "Metes",
        "url": "https://www.metes.app",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.metes.app/logo.png",
        },
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://www.metes.app/learn/how-buyers-research-with-ai",
      },
      "keywords":
        "GEO, generative engine optimization, ChatGPT, Realtor.com, Zillow, Redfin, AI citations, real estate, listing content",
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.metes.app/learn/how-buyers-research-with-ai#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is GEO for real estate?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "GEO (Generative Engine Optimization) is the practice of structuring content so that AI systems like ChatGPT, Claude, Perplexity, and Google AI Overview cite it when synthesizing answers. It's related to SEO but focused on being included in AI-generated responses rather than ranking in traditional search results.",
          },
        },
        {
          "@type": "Question",
          "name": "Does Fair Housing-compliant content help with AI citations?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. LLMs are trained to avoid problematic language, which includes Fair Housing violations. Content that contains phrases like 'family-friendly neighborhood' gets deprioritized in AI recommendations, not just flagged for Fair Housing risk.",
          },
        },
        {
          "@type": "Question",
          "name": "How do buyers actually use ChatGPT for home research in 2026?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Documented patterns include: narrowing down neighborhoods based on lifestyle criteria, comparing markets, estimating costs, researching school districts and commute times, and identifying agents worth contacting.",
          },
        },
        {
          "@type": "Question",
          "name": "Which real estate portals have AI integrations?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Three major portals launched ChatGPT apps: Zillow (October 2025, first to launch), Redfin (February 2026), and Realtor.com (March 30, 2026). Homes.com chose to build an in-platform AI experience rather than a ChatGPT app.",
          },
        },
        {
          "@type": "Question",
          "name": "Should I optimize my listing for ChatGPT specifically or all AI systems?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "All AI systems. The discipline is largely the same across ChatGPT, Claude, Perplexity, and Google AI Overview — named specifics, verifiable data, structured markup, dated content, authoritative attribution, and Fair Housing compliance.",
          },
        },
        {
          "@type": "Question",
          "name": "Do buyers still click through to listings after AI research?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sometimes. Zero-click searches now account for the majority of Google searches. But when buyers are ready to schedule a tour or contact an agent, they do click through. The buyer's opinion often forms before the click.",
          },
        },
        {
          "@type": "Question",
          "name": "What's the highest-impact GEO change I can make to my listings?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Name specific businesses, parks, streets, and neighborhoods in your MLS descriptions with real distances. Every specific becomes a verification anchor that LLMs cite.",
          },
        },
        {
          "@type": "Question",
          "name": "Does structured data (Schema.org) matter for AI citations?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Schema markup (LocalBusiness, Place, FAQPage, Article, RealEstateAgent) makes content programmatically legible to AI systems. Content with proper markup has better citation surface than the same content in unmarked prose.",
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
        <li
          key={i}
          style={{
            paddingLeft: "20px",
            position: "relative",
            fontFamily: "var(--font-manrope, sans-serif)",
            fontSize: "16px",
            lineHeight: 1.7,
            color: light ? "rgba(244,240,232,0.85)" : C.ink,
          }}
        >
          <span style={{ position: "absolute", left: "4px", color: C.gold, fontWeight: 600 }}>•</span>
          {item}
        </li>
      ))}
    </ul>
  );
}

interface TimelineCardProps { date: string; title: string; children: React.ReactNode; light?: boolean; }

function TimelineCard({ date, title, children, light = false }: TimelineCardProps) {
  return (
    <div style={{
      marginBottom: "18px",
      background: light ? "rgba(184,153,104,0.06)" : C.bgCard,
      border: `1px solid ${light ? "rgba(184,153,104,0.25)" : C.border}`,
      borderRadius: "12px",
      padding: "20px 24px",
    }}>
      <div style={{
        fontFamily: "var(--font-jetbrains, monospace)",
        fontSize: "11px",
        letterSpacing: "0.14em",
        textTransform: "uppercase",
        color: light ? C.goldSoft : C.goldDeep,
        marginBottom: "6px",
      }}>{date}</div>
      <h4 style={{
        fontFamily: "var(--font-manrope, sans-serif)",
        fontSize: "18px",
        fontWeight: 600,
        color: light ? C.creamWarm : C.ink,
        margin: "0 0 10px 0",
        letterSpacing: "-0.005em",
      }}>{title}</h4>
      <div style={{
        fontFamily: "var(--font-manrope, sans-serif)",
        fontSize: "15px",
        lineHeight: 1.65,
        color: light ? "rgba(244,240,232,0.78)" : C.inkSoft,
      }}>{children}</div>
    </div>
  );
}

interface CitationCardProps { title: string; children: React.ReactNode; }

function CitationCard({ title, children }: CitationCardProps) {
  return (
    <div style={{
      marginBottom: "18px",
      background: C.bgCard,
      border: `1px solid ${C.border}`,
      borderRadius: "10px",
      padding: "20px 24px",
    }}>
      <h4 style={{
        fontFamily: "var(--font-manrope, sans-serif)",
        fontSize: "17px",
        fontWeight: 600,
        color: C.ink,
        margin: "0 0 10px 0",
        letterSpacing: "-0.005em",
      }}>{title}</h4>
      <div style={{
        fontFamily: "var(--font-manrope, sans-serif)",
        fontSize: "15px",
        lineHeight: 1.7,
        color: C.ink,
      }}>{children}</div>
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

export default function BuyerAIResearchPage() {
  return (
    <div className="min-h-screen bg-[#EFEAE0]">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(SCHEMA_JSON_LD) }} />
      <Header />

      <section className="border-b border-[rgba(20,39,30,0.10)] bg-[#F4F0E8]">
        <div className="mx-auto w-full max-w-[960px] px-6 py-16 sm:py-20 lg:px-8">
          <div className="mx-auto max-w-[760px]">
            <SectionLabel>Guide · GEO for real estate</SectionLabel>
            <h1 className="mb-4 font-manrope text-[clamp(28px,4.5vw,48px)] font-medium leading-[1.08] tracking-[0.005em] text-[#14271E]">
              How buyers actually research neighborhoods with AI in 2026 <em className="not-italic text-[#9A7E50]">(and what your listing needs to say)</em>.
            </h1>
            <p className="mb-6 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              Realtor.com launched its ChatGPT integration on March 30, 2026. It joined Redfin (February 2026) and Zillow (October 2025). All three major real estate portals now have apps inside ChatGPT. That&apos;s not a future trend. That&apos;s the current infrastructure.
            </p>
            <p className="mb-8 max-w-[640px] text-[clamp(14px,1.2vw,17px)] leading-[1.6] text-[#4A6B53]">
              The buyer research funnel changed in early 2026, and most listing agents haven&apos;t updated their content strategy to match. This piece is about what actually happens when buyers use AI to research neighborhoods and properties — and what listing content needs to be for AI to cite it.
            </p>
            <p className="text-[13px] font-mono uppercase tracking-[0.08em] text-[rgba(20,39,30,0.55)]">
              Last updated: July 29, 2026 · ~20 minute read
            </p>
          </div>
        </div>
      </section>

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
              <p style={proseStyle}>Three real things happened in the buyer research funnel in early 2026. Zillow launched its ChatGPT app in October 2025. Redfin followed in February 2026. Realtor.com joined in March 2026. Simultaneously, Google&apos;s March 2026 Core Update started rewarding hyper-local content. Zero-click searches now account for the majority of all Google searches.</p>
              <p style={proseStyle}>The result: buyers get AI-generated answers before they visit a listing portal. Whether your content shows up in those answers is now a distribution question. Generic listings get skipped. Specific, verifiable, named content gets cited.</p>
              <p style={{ ...proseStyle, marginBottom: 0 }}>The discipline required is the same discipline Fair Housing compliance and neighborhood specificity already required. Content that describes the property in named specifics, avoids AI-generated language patterns, includes structured data, and passes Fair Housing review is exactly the content LLMs cite.</p>
            </div>

            <div className="mb-3 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">Jump to</div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "8px" }}>
              {[
                { id: "what-changed", label: "What actually changed in 2026" },
                { id: "llm-citation", label: "How LLMs decide what to cite" },
                { id: "listings-citable", label: "What makes a listing citable in 2026" },
                { id: "agent-websites", label: "What agent websites need for GEO" },
                { id: "dont-do", label: "What NOT to do" },
                { id: "zero-click", label: "The zero-click reality" },
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

      <section id="what-changed" className="relative overflow-hidden bg-[#14271E] py-20 sm:py-24">
        <div className="pointer-events-none absolute inset-0" style={{
          backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }} />
        <div className={`relative ${CONTENT}`}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#D9C49C]">
              <Sparkles className="h-3 w-3" strokeWidth={2} />
              The infrastructure shift
            </div>
            <h2 style={{ ...h2Style, color: C.creamWarm }}>What actually changed in 2026</h2>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Real dated developments. Not speculation.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The portal integrations</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Three major real estate portals launched ChatGPT integrations in the past nine months.</p>

            <TimelineCard light date="October 2025" title="Zillow — first to launch">
              First real estate firm to launch a ChatGPT app. Conversational search inside ChatGPT that routes high-intent buyers back to Zillow.
            </TimelineCard>

            <TimelineCard light date="February 2026" title="Redfin — second portal">
              Similar model — pre-search conversation in ChatGPT, transition to Redfin for listings.
            </TimelineCard>

            <TimelineCard light date="March 30, 2026" title="Realtor.com — most recent">
              Focused on the &ldquo;pre-search phase&rdquo; — affordability calculations, neighborhood exploration, budget guidance. Available to all ChatGPT users. Realtor.com specifically negotiated with MLSs to prohibit MLS data from being used to train ChatGPT&apos;s underlying model.
            </TimelineCard>

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Homes.com, CoStar Group&apos;s portal, chose a different path — launching an in-platform, voice-enabled AI experience in February 2026 rather than a ChatGPT app.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The Google Core Update</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Google&apos;s March 2026 Core Update specifically rewarded hyper-local, experience-driven content and reduced the visibility of generic material. Same signal LLMs use for citation — specificity beats generality. Same discipline required.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The zero-click reality</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Zero-click searches — where Google&apos;s AI Overview or featured snippet answers the query without the user visiting a website — now account for the majority of all Google searches. The buyer gets the answer. Never clicks. Never sees the source.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The ads announcement</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>January 16, 2026: OpenAI announced testing ads inside ChatGPT. Real estate as an advertising surface became targetable. That opens a whole separate strategy question but it&apos;s worth naming as part of the 2026 shift.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The honest wrinkle worth naming</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Bloomberg&apos;s late-March 2026 investigation found that despite more than 300 third-party ChatGPT apps available, the apps are difficult to discover inside ChatGPT, generate limited traffic back to partners, and have been deliberately restricted in functionality by companies unwilling to hand OpenAI control over customer relationships. An OpenAI spokesperson acknowledged the developer experience needs improvement.</p>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>That&apos;s an uncomfortable fact for the &ldquo;ChatGPT apps are transforming real estate&rdquo; narrative. The apps exist. Their measured traffic impact so far is limited. What matters more than the specific portal apps is the broader behavior shift: buyers using ChatGPT, Claude, Perplexity, and Google AI Overview directly to research neighborhoods and properties, whether through portal apps or general LLM queries.</p>

            <h3 style={{ ...h3Style, color: C.creamWarm }}>The query patterns buyers are actually using</h3>
            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)" }}>Not hypothetical. Documented from real estate industry reporting:</p>

            <BulletList light items={[
              <>&ldquo;Best neighborhoods in Naples, Florida for retirees&rdquo;</>,
              <>&ldquo;What&apos;s the best neighborhood in Austin for families with a budget under $500,000&rdquo;</>,
              <>&ldquo;Compare Weslyn Park to Nona Preserve for young families&rdquo;</>,
              <>&ldquo;What&apos;s it like living in [neighborhood]&rdquo;</>,
              <>&ldquo;Family-friendly areas in Orlando with good schools and short commutes&rdquo;</>,
              <>&ldquo;How do I find a good buyer&apos;s agent in Central Florida&rdquo;</>,
            ]} />

            <p style={{ ...proseStyle, color: "rgba(244,240,232,0.85)", marginBottom: 0 }}>Each of these is a query where an LLM synthesizes an answer from multiple sources. Whether your listing content, agent website, or neighborhood guide shows up in that answer determines whether the buyer forms an opinion about your listings before they ever visit a portal.</p>
          </div>
        </div>
      </section>

      <section id="llm-citation" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <Search className="h-3 w-3" strokeWidth={2} />
              The mechanics
            </div>
            <h2 style={h2Style}>How LLMs decide what to cite</h2>
            <p style={proseStyle}>Meta-technical section. What patterns LLMs consistently favor when synthesizing answers.</p>

            <div style={{
              background: "rgba(184,153,104,0.06)",
              border: `1px solid rgba(184,153,104,0.25)`,
              borderRadius: "10px",
              padding: "16px 20px",
              marginBottom: "24px",
            }}>
              <p style={{ ...proseStyle, margin: 0, fontSize: "14.5px", fontStyle: "italic" }}>Language matters here. LLM citation behavior is observable, not documented. Everything in this section is inference from consistent patterns, not confirmed mechanisms. Use it as directional guidance, not gospel.</p>
            </div>

            <CitationCard title="Named specifics over categories">
              <p style={{ margin: "0 0 12px 0" }}>The single most consistent pattern. &ldquo;Coffee shop nearby&rdquo; is a category. &ldquo;Old Fox Books &amp; Coffeehouse two blocks away&rdquo; is a named specific.</p>
              <p style={{ margin: "0 0 12px 0" }}>LLMs cite the second version. Named specifics can be verified against Google Places, business directories, and third-party sources. Categories cannot.</p>
              <p style={{ margin: 0 }}>Named streets beat &ldquo;a quiet street.&rdquo; Named parks beat &ldquo;green space nearby.&rdquo; Named schools beat &ldquo;good schools.&rdquo; The general form: whatever a buyer could Google to verify is what LLMs cite.</p>
            </CitationCard>

            <CitationCard title="Verifiable data over descriptive claims">
              <p style={{ margin: "0 0 12px 0" }}>Distances that can be checked. Addresses that resolve. Hours that match the business. When LLMs synthesize answers, they cross-reference claims against verifiable sources.</p>
              <p style={{ margin: 0 }}>Fabricated specifics get caught. Repeated fabrication destroys content credibility for the whole site.</p>
            </CitationCard>

            <CitationCard title="Recent, dated content">
              <p style={{ margin: "0 0 12px 0" }}>Content with visible dates ranks higher than undated content in LLM retrieval. &ldquo;Last updated July 2026&rdquo; is a citation signal. Undated pages carry ambiguity.</p>
              <p style={{ margin: 0 }}>This is why every /learn/ piece in this series has a visible &ldquo;last updated&rdquo; date near the top. Not decoration. Signal.</p>
            </CitationCard>

            <CitationCard title="Structured markup">
              <p style={{ margin: 0 }}>Schema.org markup — LocalBusiness, Place, FAQPage, Article, RealEstateAgent — makes content programmatically legible. Content with proper schema markup has better citation surface than the same content in unmarked prose. This isn&apos;t optional in 2026.</p>
            </CitationCard>

            <CitationCard title="FAQ format">
              <p style={{ margin: 0 }}>Question-answer pairs match the format LLMs return. Content structured as FAQ gets pulled more often than the same information written as prose.</p>
            </CitationCard>

            <CitationCard title="Authoritative source signals">
              <p style={{ margin: "0 0 12px 0" }}>Named authors. Verified organizations. Cited references. LinkedIn presence. Original data or research. LLMs weight sources they can attribute over anonymous content.</p>
              <p style={{ margin: 0 }}>Cross-references: <Link href="/learn/ai-listing-description-tells" style={inlineLink}>the six categories of AI tells</Link> covers the traits that make AI-generated content spot-able. Those same traits make it non-citable.</p>
            </CitationCard>
          </div>
        </div>
      </section>

      <section id="listings-citable" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#5C8A6E]">
              <FileCheck className="h-3 w-3" strokeWidth={2} />
              Actionable
            </div>
            <h2 style={h2Style}>What makes a listing citable in 2026</h2>
            <p style={proseStyle}>Actionable section. Specific patterns for listing content that AI systems consistently cite.</p>

            <h3 style={h3Style}>Named neighborhood specifics</h3>
            <p style={proseStyle}>Not &ldquo;close to shops&rdquo; but &ldquo;two blocks from Quiet Waters Park, five minutes to the Annapolis City Dock, walking distance to Old Fox Books &amp; Coffeehouse.&rdquo;</p>
            <p style={proseStyle}>Named businesses, named parks, named streets, real distances. The <Link href="/learn/neighborhood-description-examples" style={inlineLink}>neighborhood description examples reference</Link> shows what this looks like across 12 markets.</p>

            <h3 style={h3Style}>Verifiable landmarks</h3>
            <p style={proseStyle}>If your listing mentions a park, name it. If it mentions restaurants, name them. If it mentions distances, get them right. The through-line: whatever a buyer could Google to verify is what LLMs cite.</p>

            <h3 style={h3Style}>Neighborhood name specificity</h3>
            <p style={proseStyle}>Not &ldquo;downtown&rdquo; but &ldquo;Riverbend neighborhood.&rdquo; Buyers search neighborhood names, not general descriptors. LLMs match against neighborhood names.</p>

            <h3 style={h3Style}>Time-bound recency</h3>
            <p style={proseStyle}>&ldquo;2024 kitchen renovation with quartz counters and gas range&rdquo; beats &ldquo;recently renovated kitchen.&rdquo; Dates verify. Vagueness doesn&apos;t.</p>

            <h3 style={h3Style}>Structured features</h3>
            <p style={proseStyle}>Bed count, bath count, square footage, lot size, year built — the structured facts LLMs pull first when synthesizing an answer.</p>

            <h3 style={h3Style}>Zero AI tells</h3>
            <p style={proseStyle}>Content that reads AI-generated gets deprioritized by LLM training. <Link href="/learn/ai-listing-description-tells" style={inlineLink}>The six categories of AI tells</Link> covers the specific patterns.</p>

            <h3 style={h3Style}>Fair Housing compliance</h3>
            <p style={proseStyle}>LLMs are trained to avoid problematic language. Fair Housing violations flag content out of LLM recommendations, not just out of Zillow syndication. <Link href="/learn/fair-housing-words-to-avoid" style={inlineLink}>The Fair Housing word list</Link> documents the specific phrases that trigger both.</p>
          </div>
        </div>
      </section>

      <section id="agent-websites" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <Globe className="h-3 w-3" strokeWidth={2} />
              The second surface
            </div>
            <h2 style={h2Style}>What agent websites need for GEO</h2>
            <p style={proseStyle}>Different surface, same discipline.</p>

            <h3 style={h3Style}>Named service areas</h3>
            <p style={proseStyle}>&ldquo;Serving Central Florida&rdquo; is generic. &ldquo;Serving Weslyn Park, Sunbridge, Nona Preserve, East Orlando, Orange County&rdquo; is citable.</p>

            <h3 style={h3Style}>Specific credentials</h3>
            <p style={proseStyle}>Years licensed. MLS memberships. Specialties. Verified transaction count. Real, verifiable credentials rather than &ldquo;experienced professional&rdquo; generalities.</p>

            <h3 style={h3Style}>FAQ pages</h3>
            <p style={proseStyle}>Every common client question with a specific answer. LLMs pull FAQ format naturally. An FAQ page with 15-25 well-answered questions is one of the highest-citation-surface elements a real estate agent website can have.</p>

            <h3 style={h3Style}>Neighborhood guides</h3>
            <p style={proseStyle}>Long-form content on specific neighborhoods. What it&apos;s like to live in each named neighborhood. Which schools serve it, which restaurants define it, which parks anchor it. This is the exact content LLMs pull when synthesizing &ldquo;tell me about [neighborhood]&rdquo; answers.</p>

            <h3 style={h3Style}>Structured data</h3>
            <p style={proseStyle}>LocalBusiness schema on the agent bio page. RealEstateAgent schema on service pages. FAQPage schema on the FAQ page. In 2026 this isn&apos;t optional.</p>

            <h3 style={h3Style}>Author attribution</h3>
            <p style={proseStyle}>Agent name on every content piece. Real bio with verifiable credentials. Consistent LinkedIn presence. LLMs cite content with authoritative attribution more readily than anonymous content.</p>
          </div>
        </div>
      </section>

      <section id="dont-do" className="bg-[#EFEAE0] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#C97B5C]">
              <XCircle className="h-3 w-3" strokeWidth={2} />
              The traps
            </div>
            <h2 style={h2Style}>What NOT to do</h2>

            <h3 style={h3Style}>Keyword stuffing</h3>
            <p style={proseStyle}>Same problem for GEO as for SEO. AI systems downrank keyword-stuffed content just like Google does.</p>

            <h3 style={h3Style}>Fabricated specifics</h3>
            <p style={proseStyle}>The failure mode that destroys credibility permanently. Named businesses that don&apos;t exist. Distances that are wrong. LLMs cross-reference against Google Places and other verifiable sources. Fabricated specifics get caught. Once caught, the whole site&apos;s citation weight drops.</p>

            <h3 style={h3Style}>Generic AI-generated prose</h3>
            <p style={proseStyle}>Content that reads AI-generated gets deprioritized. <Link href="/learn/ai-listing-description-tells" style={inlineLink}>The six categories of AI tells</Link> documents the patterns. The fix isn&apos;t &ldquo;don&apos;t use AI.&rdquo; It&apos;s &ldquo;use AI intentionally, edit for the tells, verify the specifics, add named grounding data.&rdquo;</p>

            <h3 style={h3Style}>Missing structured data</h3>
            <p style={proseStyle}>Content that&apos;s citable in prose but lacks Schema.org markup gets pulled less than content with the same information plus proper markup.</p>

            <h3 style={h3Style}>Duplicate content across MLSs</h3>
            <p style={proseStyle}>LLMs deduplicate. If your description is identical across the MLS feed, Zillow, Realtor.com, Redfin, and your own site, only one version gets cited. Your own site needs distinct content — expanded description, neighborhood context, agent voice — that doesn&apos;t exist verbatim on the portals.</p>

            <h3 style={h3Style}>Undated content</h3>
            <p style={proseStyle}>&ldquo;Last updated 2022&rdquo; is a signal to LLMs that the content may be stale. Every piece of content on your site should have a visible last-updated date.</p>
          </div>
        </div>
      </section>

      <section id="zero-click" className="border-t border-[rgba(20,39,30,0.10)] bg-[#F4F0E8] py-16 sm:py-20">
        <div className={CONTENT}>
          <div className={READING}>
            <div className="mb-4 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#9A7E50]">
              <TrendingDown className="h-3 w-3" strokeWidth={2} />
              Strategic implication
            </div>
            <h2 style={h2Style}>The zero-click reality</h2>
            <p style={proseStyle}>The uncomfortable strategic implication.</p>
            <p style={proseStyle}>Zero-click searches are now the majority of all searches. When a buyer asks ChatGPT &ldquo;best neighborhoods in Orlando for families,&rdquo; they get a synthesized answer. Named neighborhoods. Named schools. Named amenities. Sometimes named agents. They may never click through to any of the source websites.</p>

            <h3 style={h3Style}>What this changes about content strategy</h3>
            <p style={proseStyle}>Old model: content drives traffic drives conversion. The metric was &ldquo;visitors to my site.&rdquo;</p>
            <p style={proseStyle}>New model: content drives citation drives brand recognition drives eventual direct contact. The metric is &ldquo;am I in the answer AI systems give buyers?&rdquo;</p>

            <h3 style={h3Style}>The compounding effect</h3>
            <p style={proseStyle}>Every citation surface is small individually. But if a buyer asks five questions about Central Florida real estate over two weeks, and Metes shows up in three of the answers, brand recognition builds. When they eventually search for an agent, &ldquo;Metes&rdquo; is a name they&apos;ve seen before.</p>

            <h3 style={h3Style}>The measurement problem</h3>
            <p style={proseStyle}>You can&apos;t measure this well yet. GSC shows impressions and clicks for traditional search results. It doesn&apos;t show whether ChatGPT cited your content. The current approximation is manual testing — ask each major LLM your priority queries every few weeks.</p>
          </div>
        </div>
      </section>

      <section id="faq" className="bg-[#EFEAE0] py-20 sm:py-24">
        <div className={CONTENT}>
          <div className={READING}>
            <SectionLabel>Common questions</SectionLabel>
            <h2 style={h2Style}>Common questions</h2>

            <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "24px" }}>
              {[
                { q: "What is GEO for real estate?", a: "GEO (Generative Engine Optimization) is the practice of structuring content so that AI systems like ChatGPT, Claude, Perplexity, and Google AI Overview cite it when synthesizing answers. It's related to SEO but focused on being included in AI-generated responses rather than ranking in traditional search results." },
                { q: "Does Fair Housing-compliant content help with AI citations?", a: "Yes. LLMs are trained to avoid problematic language, which includes Fair Housing violations. Content that contains phrases like 'family-friendly neighborhood' gets deprioritized in AI recommendations, not just flagged for Fair Housing risk. The same discipline that keeps you compliant makes your content more citable." },
                { q: "How do buyers actually use ChatGPT for home research in 2026?", a: "Documented patterns include: narrowing down neighborhoods based on lifestyle criteria, comparing markets, estimating costs, researching school districts and commute times, and identifying agents worth contacting." },
                { q: "Which real estate portals have AI integrations?", a: "Three major portals launched ChatGPT apps: Zillow (October 2025, first to launch), Redfin (February 2026), and Realtor.com (March 30, 2026). Homes.com chose to build an in-platform AI experience rather than a ChatGPT app." },
                { q: "Should I optimize my listing for ChatGPT specifically or all AI systems?", a: "All AI systems. The discipline is largely the same across ChatGPT, Claude, Perplexity, and Google AI Overview — named specifics, verifiable data, structured markup, dated content, authoritative attribution, and Fair Housing compliance." },
                { q: "Do buyers still click through to listings after AI research?", a: "Sometimes. Zero-click searches now account for the majority of Google searches. But when buyers are ready to schedule a tour or contact an agent, they do click through. The buyer's opinion often forms before the click, based on what AI cited during research." },
                { q: "What's the highest-impact GEO change I can make to my listings?", a: "Name specific businesses, parks, streets, and neighborhoods in your MLS descriptions with real distances. Every specific becomes a verification anchor that LLMs cite." },
                { q: "Does structured data (Schema.org) matter for AI citations?", a: "Yes. Schema markup makes content programmatically legible to AI systems. Content with proper markup has better citation surface than the same content in unmarked prose. This isn't optional in 2026." },
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
              Sources: Realtor.com press release (March 30, 2026, PRNewswire); Inman coverage of Realtor.com ChatGPT integration; HousingWire coverage of portal AI integrations; Bloomberg late-March 2026 reporting on ChatGPT app ecosystem traffic; Google March 2026 Core Update announcement; OpenAI ads announcement (January 16, 2026); internal Metes references to Weeks 1, 3, 4, 5, and 6. Not marketing advice or guaranteed outcomes — LLM citation behavior is observable, not documented.
            </p>
          </div>
        </div>
      </section>

      <section className="relative overflow-hidden bg-[#14271E] py-20 sm:py-24">
        <div className="pointer-events-none absolute inset-0" style={{
          backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }} />
        <div className={`relative ${CONTENT}`}>
          <div style={{ maxWidth: "760px" }}>
            <SectionLabel light>The through-line</SectionLabel>
            <h2 className="mb-5 font-manrope text-[clamp(28px,4vw,42px)] font-medium leading-[1.1] tracking-[0.005em] text-[#F4F0E8]">
              Describe the property in named specifics. Include structured data. <em className="not-italic text-[#B89968]">Pass Fair Housing review.</em>
            </h2>
            <p className="mb-8 max-w-[620px] text-[clamp(15px,1.3vw,17px)] leading-[1.6] text-[rgba(244,240,232,0.78)]">
              The same discipline that keeps you compliant makes your content citable. The same discipline that makes your listings feel human makes them stand out to LLMs. GEO isn&apos;t a separate practice — it&apos;s the discipline this whole series has been about, applied to a new distribution surface.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/tools/listing-description-checker" className="inline-flex items-center gap-2 rounded-[9px] bg-[#B89968] px-7 py-3.5 font-manrope text-[14px] font-medium text-[#14271E] no-underline transition-colors hover:bg-[#9A7E50] hover:text-[#F4F0E8]">
                Audit a listing free
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