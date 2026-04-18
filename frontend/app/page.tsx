import { Navbar } from "@/components/layout/Navbar";
import { Composer } from "@/components/home/Composer";
import {
  FileText, Share2, Mail, ShieldCheck,
  Upload, Sparkles, Download,
} from "lucide-react";

// ─────────────────────────────────────────────────────────────────
// Static content
// ─────────────────────────────────────────────────────────────────

const HOW_IT_WORKS = [
  {
    num: "1",
    icon: Upload,
    title: "Upload your photos + notes",
    body: "Drop in your listing photos and paste your agent notes. Address, price, beds/baths, upgrades — anything you'd tell a buyer.",
  },
  {
    num: "2",
    icon: Sparkles,
    title: "Review AI-extracted details",
    body: "Our AI reads your photos and notes to extract property details. Tap any field to correct it before we generate.",
  },
  {
    num: "3",
    icon: Download,
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
    sub: "Facebook + 2× Instagram captions",
  },
  {
    icon: Mail,
    title: "Email Campaign",
    sub: "4 sequences: Just Listed, Open House, Why This Home, Just Sold",
  },
  {
    icon: ShieldCheck,
    title: "Compliance Audit",
    sub: "Fair Housing review on every asset",
  },
];

// ─────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────

export default function HomePage() {
  return (
    <div id="top" className="min-h-screen bg-background">
      <Navbar />

      {/* ── Hero ── */}
      <section className="px-6 pb-0 pt-12 text-center">
        <p className="mb-3 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
          AI-powered listing marketing
        </p>
        <h1 className="mx-auto mb-3 max-w-lg text-2xl font-semibold leading-tight tracking-tight text-foreground sm:text-3xl">
          Your listing, market-ready
          <br />
          in under a minute.
        </h1>
        <p className="mx-auto mb-10 max-w-sm text-xs text-muted-foreground">
          Upload photos and paste your notes. Get MLS copy, social posts, and email campaigns — done.
        </p>
      </section>

      {/* ── Upload form (above fold, IS the hero) ── */}
      <Composer />

      {/* ── Below fold divider ── */}
      <div className="flex items-center gap-4 px-6 pb-10">
        <div className="h-px flex-1 bg-border" />
        <span className="text-[11px] text-muted-foreground">↓ below the fold</span>
        <div className="h-px flex-1 bg-border" />
      </div>

      <div className="mx-auto max-w-2xl px-6 pb-20">

        {/* ── How it works ── */}
        <section id="how-it-works" className="mb-14">
          <p className="section-label mb-4">How it works</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {HOW_IT_WORKS.map(({ num, icon: Icon, title, body }) => (
              <div
                key={num}
                className="rounded-lg border border-border p-5"
              >
                <div className="mb-3 flex h-7 w-7 items-center justify-center rounded-full bg-muted text-xs font-semibold text-foreground">
                  {num}
                </div>
                <p className="mb-1.5 text-xs font-semibold text-foreground">{title}</p>
                <p className="text-[11px] leading-relaxed text-muted-foreground">{body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Deliverables ── */}
        <section className="mb-14">
          <p className="section-label mb-4">What you get for $24.99</p>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {DELIVERABLES.map(({ icon: Icon, title, sub }) => (
              <div
                key={title}
                className="flex items-center gap-3 rounded-lg border border-border p-4"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted">
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-foreground">{title}</p>
                  <p className="text-[11px] text-muted-foreground">{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing">
          <p className="section-label mb-4">Pricing</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {/* Listing only */}
            <div className="rounded-xl border border-border p-6">
              <p className="mb-1 text-xl font-semibold text-foreground">$24.99</p>
              <p className="mb-5 text-xs text-muted-foreground">Listing Copy Package</p>
              <ul className="mb-6 flex flex-col gap-2">
                {["MLS description", "Social launch pack", "Email campaign (4 sequences)", "Compliance audit"].map((f) => (
                  <li key={f} className="text-[11px] text-muted-foreground">— {f}</li>
                ))}
              </ul>
              <a
                href="#top"
                className="block w-full rounded-md border border-border py-2.5 text-center text-xs font-semibold text-foreground transition-colors hover:bg-muted"
              >
                Try it now
              </a>
            </div>

            {/* Listing + Photos */}
            <div className="rounded-xl border border-foreground bg-muted/30 p-6">
              <p className="mb-1 text-xl font-semibold text-foreground">$73.99</p>
              <p className="mb-5 text-xs text-muted-foreground">Listing Copy + Photo Editing</p>
              <ul className="mb-6 flex flex-col gap-2">
                {[
                  "Everything in Listing Copy",
                  "Color correction + perspective fix",
                  "Twilight sky replacement",
                  "Photos delivered to email",
                ].map((f) => (
                  <li key={f} className="text-[11px] text-muted-foreground">— {f}</li>
                ))}
              </ul>
              <a
                href="#top"
                className="block w-full rounded-md bg-foreground py-2.5 text-center text-xs font-semibold text-background transition-opacity hover:opacity-90"
              >
                Try it now
              </a>
            </div>
          </div>
          <p className="mt-4 text-center text-[11px] text-muted-foreground">
            Subscription available after your first listing — agents who try it, keep it.
          </p>
        </section>
      </div>
    </div>
  );
}
