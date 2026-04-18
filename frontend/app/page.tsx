import { Navbar } from "@/components/layout/Navbar";
import { Composer } from "@/components/home/Composer";
import { FileText, Share2, Mail, ShieldCheck } from "lucide-react";

// ─────────────────────────────────────────────────────────────────
// Static content
// ─────────────────────────────────────────────────────────────────

const VALUE_PROPS = [
  {
    emoji: "📸",
    headline: "We read your listing",
    body: "Drop in your photos and notes. Our AI extracts every feature, finish, and upgrade — bedrooms, pool type, countertops, recent renovations — automatically.",
  },
  {
    emoji: "🏠",
    headline: "We curate your best shots",
    body: "Your top 25 photos selected by marketing impact, ranked, and renamed for MLS upload. Pool before garage. Primary suite before storage room.",
  },
  {
    emoji: "✍️",
    headline: "We write everything",
    body: "MLS description, three social posts, a four-email campaign, and a full Fair Housing compliance audit — delivered in under 60 seconds.",
  },
];

const HOW_IT_WORKS = [
  {
    num: "1",
    title: "Upload your photos + notes",
    body: "Drop in your listing photos and paste your agent notes. Address, price, beds/baths, upgrades — anything you'd tell a buyer.",
  },
  {
    num: "2",
    title: "Review AI-extracted details",
    body: "Our AI reads your photos and notes to extract property details. Tap any field to correct it before we generate.",
  },
  {
    num: "3",
    title: "Download your campaign",
    body: "MLS description, social posts, email sequence, and compliance audit — ready in under 60 seconds.",
  },
];

const DELIVERABLES = [
  {
    icon: FileText,
    title: "MLS Description",
    sub: "Optimized for character limits + Fair Housing",
  },
  {
    icon: Share2,
    title: "Social Launch Pack",
    sub: "Facebook + 2× Instagram captions with curated images",
  },
  {
    icon: Mail,
    title: "Email Campaign",
    sub: "4 sequences: Just Listed, Open House, Why This Home, Just Sold",
  },
  {
    icon: ShieldCheck,
    title: "Compliance Audit",
    sub: "Fair Housing review on every asset before you publish",
  },
];

// ─────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────

export default function HomePage() {
  return (
    <div id="top" className="min-h-screen bg-background">
      <Navbar />

      {/* ── Consistent container — everything lives inside this ── */}
      <div className="mx-auto max-w-5xl px-6">

        {/* ── Hero ── */}
        <section className="pb-8 pt-16 text-center">
          <p className="mb-4 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
            AI-powered listing marketing
          </p>
          <h1 className="mx-auto mb-4 max-w-2xl text-4xl font-bold leading-[1.1] tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Your listing.{" "}
            <br className="hidden sm:block" />
            Market-ready.{" "}
            <br className="hidden sm:block" />
            In 60 seconds.
          </h1>
          <p className="mx-auto mb-10 max-w-md text-sm text-muted-foreground">
            Upload your photos and notes. Get MLS copy, social posts, and email campaigns — done.
          </p>
        </section>

        {/* ── Composer — same container width ── */}
        <Composer className="mb-16" />

        {/* ── Value props — 3-pack, Antimetal style ── */}
        <section className="mb-20">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {VALUE_PROPS.map(({ emoji, headline, body }) => (
              <div
                key={headline}
                className="rounded-2xl bg-muted/60 p-8"
              >
                <div className="mb-4 text-3xl">{emoji}</div>
                <h3 className="mb-3 text-lg font-semibold leading-snug text-foreground">
                  {headline}
                </h3>
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {body}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* ── How it works ── */}
        <section id="how-it-works" className="mb-20">
          <p className="section-label mb-8">How it works</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {HOW_IT_WORKS.map(({ num, title, body }) => (
              <div key={num} className="rounded-xl border border-border p-6">
                <div className="mb-4 flex h-8 w-8 items-center justify-center rounded-full bg-muted text-xs font-semibold text-foreground">
                  {num}
                </div>
                <p className="mb-2 text-sm font-semibold text-foreground">{title}</p>
                <p className="text-xs leading-relaxed text-muted-foreground">{body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Deliverables ── */}
        <section className="mb-20">
          <p className="section-label mb-8">What you get for $24.99</p>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {DELIVERABLES.map(({ icon: Icon, title, sub }) => (
              <div
                key={title}
                className="flex items-start gap-4 rounded-xl border border-border p-5"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted">
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="mb-0.5 text-sm font-semibold text-foreground">{title}</p>
                  <p className="text-xs text-muted-foreground">{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing" className="mb-24">
          <p className="section-label mb-8">Pricing</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">

            {/* Listing only */}
            <div className="rounded-2xl border border-border p-8">
              <p className="mb-1 text-3xl font-bold text-foreground">$24.99</p>
              <p className="mb-6 text-sm text-muted-foreground">Listing Copy Package</p>
              <ul className="mb-8 flex flex-col gap-2.5">
                {[
                  "MLS-ready listing description",
                  "Social launch pack (Facebook + 2× Instagram)",
                  "4-email campaign sequence",
                  "Fair Housing compliance audit",
                  "Curated + renamed photo set",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2 text-xs text-muted-foreground">
                    <span className="mt-0.5 text-foreground">—</span>
                    {f}
                  </li>
                ))}
              </ul>
              <a
                href="#top"
                className="block w-full rounded-lg border border-border py-3 text-center text-xs font-semibold text-foreground transition-colors hover:bg-muted"
              >
                Try it now
              </a>
            </div>

            {/* Listing + Photos */}
            <div className="rounded-2xl border border-foreground bg-muted/30 p-8">
              <p className="mb-1 text-3xl font-bold text-foreground">$73.99</p>
              <p className="mb-6 text-sm text-muted-foreground">Listing Copy + Photo Editing</p>
              <ul className="mb-8 flex flex-col gap-2.5">
                {[
                  "Everything in Listing Copy",
                  "Color correction + perspective fix",
                  "Twilight sky replacement on eligible exteriors",
                  "Enhanced photos delivered to your email",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2 text-xs text-muted-foreground">
                    <span className="mt-0.5 text-foreground">—</span>
                    {f}
                  </li>
                ))}
              </ul>
              <a
                href="#top"
                className="block w-full rounded-lg bg-foreground py-3 text-center text-xs font-semibold text-background transition-opacity hover:opacity-90"
              >
                Try it now
              </a>
            </div>
          </div>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            Subscription available after your first listing — agents who try it, keep it.
          </p>
        </section>

      </div>
    </div>
  );
}