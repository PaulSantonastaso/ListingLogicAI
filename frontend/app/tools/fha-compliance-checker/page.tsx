"use client";

import { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/layout/Navbar";
import { Loader2, AlertTriangle, CheckCircle2 } from "lucide-react";
import posthog from "posthog-js";

type ScanStatus = "idle" | "loading" | "passed" | "flagged" | "email_gate" | "error";

interface ComplianceResult {
  status: "pass" | "revised" | "flagged";
  issues_found: string[];
  compliant_text: string;
  reviewer_notes: string | null;
}

const C = {
  cream:        "#EFEAE0",
  creamWarm:    "#F4F0E8",
  bgCard:       "#FAF7F0",
  forest:       "#1F3D2E",
  forestDeep:   "#14271E",
  gold:         "#B89968",
  goldDeep:     "#9A7E50",
  ink:          "#14271E",
  inkSoft:      "#4A6B53",
  muted:        "rgba(20,39,30,0.55)",
  border:       "rgba(20,39,30,0.10)",
  borderStrong: "rgba(20,39,30,0.18)",
  warn:         "#C97B5C",
  warnBg:       "rgba(201,123,92,0.08)",
  success:      "#5C8A6E",
  successBg:    "rgba(92,138,110,0.08)",
};

const CONTENT = "mx-auto w-full max-w-[1280px] px-6 lg:px-12";

const FHA_CATEGORIES = [
  {
    title: "Familial Status & Age Discrimination",
    intro: "HUD aggressively prosecutes ads that imply a property is suited only for certain types of families or age groups.",
    items: [
      { num: 1, phrase: '"Family-Friendly" or "Great for Families"', risk: "Excludes single buyers, couples without children, or retirees.", safe: '"Spacious layout with multiple living areas" or "Multi-level home with a large fenced yard."' },
      { num: 2, phrase: '"Empty Nesters" or "Perfect for Retirees"', risk: "Discriminates against younger buyers or families with children. Exceptions exist only for legally registered 55+ communities.", safe: '"Low-maintenance, single-story living."' },
      { num: 3, phrase: '"Bachelor Pad"', risk: "Discriminates based on sex and familial status.", safe: '"Modern, open-concept condo."' },
      { num: 4, phrase: '"Mother-in-Law Suite"', risk: "Some strict MLS boards flag this as implying a specific familial arrangement.", safe: '"Accessory Dwelling Unit (ADU)," "Guest suite," or "Separate living quarters."' },
    ],
  },
  {
    title: "Disability & Mobility Discrimination",
    intro: "You must describe the property, not the physical capabilities of the buyer.",
    items: [
      { num: 5, phrase: '"Walking Distance to..."', risk: "Discriminates against individuals with mobility impairments who cannot walk. One of the most common accidental violations.", safe: '"Two blocks from..." or "A short distance to..."' },
      { num: 6, phrase: '"Perfect for an Active Lifestyle"', risk: "Implies the neighborhood is exclusionary to those with physical handicaps.", safe: '"Located near trailheads and tennis courts."' },
    ],
  },
  {
    title: "Race, National Origin, and Religion",
    intro: "Never use language that implies a neighborhood has a specific demographic makeup.",
    items: [
      { num: 7, phrase: '"Exclusive Neighborhood"', risk: "Historically used as a proxy for racial or economic steering.", safe: '"Private, gated community" or "Secluded cul-de-sac."' },
      { num: 8, phrase: '"Safe Streets" or "Low Crime Area"', risk: "Can be interpreted as coded language for steering buyers toward or away from certain demographic areas.", safe: '"Dead-end street," "Neighborhood watch program," or "Fenced perimeter."' },
      { num: 9, phrase: '"Near the Catholic Church" or "Walking distance to the Synagogue"', risk: "Shows a preference for a specific religion.", safe: "Do not mention religious institutions as amenities." },
      { num: 10, phrase: '"Traditional Community"', risk: "Often flagged as implying a preference for a specific race or national origin.", safe: 'Describe the architecture: "Classic Colonial-style homes."' },
    ],
  },
  {
    title: "Sex and Gender Bias",
    intro: "Language that assumes the gender or relationship status of the buyer.",
    items: [
      { num: 11, phrase: '"His and Hers Closets"', risk: "Assumes a heterosexual couple will purchase the home.", safe: '"Dual walk-in closets" or "Primary suite with two large closets."' },
      { num: 12, phrase: '"Handyman\'s Dream"', risk: "Gender-biased language implying only men do renovations.", safe: '"Fixer-upper," "Great investment potential," or "Ready for your personal touch."' },
    ],
  },
];

export default function ComplianceCheckPage() {
  const [text, setText] = useState("");
  const [email, setEmail] = useState("");
  const [scanStatus, setScanStatus] = useState<ScanStatus>("idle");
  const [result, setResult] = useState<ComplianceResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [runsUsed, setRunsUsed] = useState(0);

  const handleScan = async (overrideEmail?: string) => {
    if (!text.trim() || scanStatus === "loading") return;
    setScanStatus("loading");
    setResult(null);
    setErrorMsg(null);

    posthog.capture("fha_scan_submitted", {
      text_length: text.trim().length,
      has_email: !!(overrideEmail || email),
    });

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/tools/compliance-check`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, email: overrideEmail || email || null }),
        }
      );

      if (res.status === 402) {
        const data = await res.json();
        const runs = data.detail?.runs_used ?? 3;
        setRunsUsed(runs);
        setScanStatus("email_gate");
        posthog.capture("fha_scan_email_gated", { runs_used: runs });
        return;
      }

      if (!res.ok) {
        const data = await res.json();
        setErrorMsg(
          data.detail === "not_real_estate_content"
            ? "This doesn't look like a real estate listing description. Please paste an MLS description or property draft."
            : "Something went wrong. Please try again."
        );
        setScanStatus("error");
        return;
      }

      const data: ComplianceResult = await res.json();
      setResult(data);
      setScanStatus(data.status === "pass" ? "passed" : "flagged");
    } catch {
      setErrorMsg("Could not reach the server. Check your connection and try again.");
      setScanStatus("error");
    }
  };

  const sectionLabel = (text: string, light?: boolean) => (
    <div style={{ display: "flex", alignItems: "center", gap: "8px", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", color: light ? "#D9C49C" : C.goldDeep, letterSpacing: "0.14em", textTransform: "uppercase" as const, marginBottom: "16px" }}>
      <span style={{ width: "18px", height: "1px", background: light ? "#D9C49C" : C.goldDeep, display: "inline-block" }} />
      {text}
    </div>
  );

  return (
    <div style={{ background: C.cream, minHeight: "100vh" }}>
      <Navbar />

      {/* ── HERO ── */}
      <section style={{ background: C.creamWarm, borderBottom: `1px solid ${C.border}`, padding: "64px 0 56px" }}>
        <div className={CONTENT}>
          <div style={{ maxWidth: "760px" }}>
            {sectionLabel("Free tool · Fair Housing compliance")}
            <h1 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "clamp(28px, 4vw, 48px)", lineHeight: 1.08, letterSpacing: "0.02em", color: C.forestDeep, marginBottom: "16px" }}>
              Is Your MLS Description Breaking the Law?
            </h1>
            <p style={{ fontSize: "clamp(14px, 1.2vw, 17px)", lineHeight: 1.6, color: C.inkSoft, maxWidth: "600px", marginBottom: "32px" }}>
              The Fair Housing Act is stricter than most agents realize. Paste your property draft below for an instant AI-powered compliance audit. Keep your license safe — 100% free.
            </p>

            {/* Scan box */}
            <div style={{ background: C.bgCard, borderRadius: "14px", border: `1px solid ${C.borderStrong}`, overflow: "hidden", boxShadow: "0 4px 24px rgba(20,39,30,0.06)" }}>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your rough MLS description here..."
                disabled={scanStatus === "loading"}
                style={{ width: "100%", minHeight: "160px", padding: "20px 24px", background: "transparent", border: "none", outline: "none", resize: "none" as const, fontFamily: "var(--font-manrope, sans-serif)", fontSize: "14px", lineHeight: 1.6, color: C.ink, boxSizing: "border-box" as const }}
              />
              <div style={{ borderTop: `1px solid ${C.border}`, padding: "12px 16px", display: "flex", alignItems: "center", justifyContent: "space-between", background: "rgba(20,39,30,0.02)" }}>
                <span style={{ fontSize: "11px", color: C.muted, fontFamily: "var(--font-jetbrains, monospace)" }}>
                  {text.length} / 2000 characters
                </span>
                <button
                  onClick={() => handleScan()}
                  disabled={!text.trim() || text.length > 2000 || scanStatus === "loading"}
                  style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "10px 20px", borderRadius: "8px", background: (!text.trim() || scanStatus === "loading") ? C.inkSoft : C.forest, color: C.creamWarm, border: "none", fontSize: "13px", fontWeight: 500, cursor: (!text.trim() || scanStatus === "loading") ? "not-allowed" : "pointer", opacity: (!text.trim() || text.length > 2000) ? 0.5 : 1, transition: "opacity 0.2s", fontFamily: "var(--font-manrope, sans-serif)" }}
                >
                  {scanStatus === "loading" ? (
                    <><Loader2 style={{ width: "14px", height: "14px" }} className="animate-spin" /> Scanning…</>
                  ) : "Scan for FHA Risks →"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── RESULT ── */}
      {scanStatus !== "idle" && scanStatus !== "loading" && (
        <section style={{ padding: "48px 0", background: C.cream, borderBottom: `1px solid ${C.border}` }}>
          <div className={CONTENT}>
            <div style={{ maxWidth: "760px" }}>

              {scanStatus === "email_gate" && (
                <div style={{ background: C.bgCard, borderRadius: "14px", border: `1px solid ${C.borderStrong}`, padding: "32px" }}>
                  <p style={{ fontSize: "11px", fontWeight: 600, letterSpacing: "0.1em", textTransform: "uppercase" as const, color: C.goldDeep, marginBottom: "10px", fontFamily: "var(--font-jetbrains, monospace)" }}>Free scans used</p>
                  <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "22px", color: C.forestDeep, marginBottom: "10px" }}>
                    You&apos;ve used your {runsUsed} free scans.
                  </h2>
                  <p style={{ fontSize: "14px", color: C.inkSoft, lineHeight: 1.6, marginBottom: "24px" }}>
                    Enter your email to keep scanning — no subscription, no spam.
                  </p>
                  <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" as const }}>
                    <input
                      type="email"
                      placeholder="your@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleScan(email)}
                      style={{ flex: 1, minWidth: "200px", padding: "10px 14px", borderRadius: "8px", border: `1px solid ${C.borderStrong}`, background: C.creamWarm, fontSize: "13px", color: C.ink, outline: "none", fontFamily: "var(--font-manrope, sans-serif)" }}
                    />
                    <button
                      onClick={() => handleScan(email)}
                      disabled={!email.trim()}
                      style={{ padding: "10px 20px", borderRadius: "8px", background: C.forest, color: C.creamWarm, border: "none", fontSize: "13px", fontWeight: 500, cursor: !email.trim() ? "not-allowed" : "pointer", opacity: !email.trim() ? 0.5 : 1, fontFamily: "var(--font-manrope, sans-serif)" }}
                    >
                      Continue scanning →
                    </button>
                  </div>
                </div>
              )}

              {scanStatus === "error" && (
                <div style={{ background: C.warnBg, borderRadius: "14px", border: `1px solid ${C.warn}`, padding: "24px 28px" }}>
                  <p style={{ fontSize: "14px", color: C.warn, fontWeight: 500 }}>{errorMsg}</p>
                </div>
              )}

              {scanStatus === "flagged" && result && (
                <div style={{ background: C.warnBg, borderRadius: "14px", border: `1px solid ${C.warn}`, padding: "28px 32px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
                    <AlertTriangle style={{ width: "20px", height: "20px", color: C.warn, flexShrink: 0 }} />
                    <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "20px", color: C.forestDeep, margin: 0 }}>⚠️ High Risk Detected.</h2>
                  </div>
                  {result.issues_found.length > 0 && (
                    <div style={{ marginBottom: "20px" }}>
                      <p style={{ fontSize: "12px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" as const, color: C.warn, marginBottom: "10px", fontFamily: "var(--font-jetbrains, monospace)" }}>Issues found</p>
                      <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column" as const, gap: "6px" }}>
                        {result.issues_found.map((issue, i) => (
                          <li key={i} style={{ display: "flex", alignItems: "flex-start", gap: "8px", fontSize: "13px", color: C.ink, lineHeight: 1.5 }}>
                            <span style={{ color: C.warn, flexShrink: 0 }}>⚠</span>{issue}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {result.reviewer_notes && (
                    <p style={{ fontSize: "13px", color: C.inkSoft, lineHeight: 1.6, marginBottom: "20px", fontStyle: "italic" }}>{result.reviewer_notes}</p>
                  )}
                  <div style={{ borderTop: `1px solid rgba(201,123,92,0.2)`, paddingTop: "20px" }}>
                    <p style={{ fontSize: "14px", color: C.forestDeep, lineHeight: 1.6, marginBottom: "16px" }}>
                      Don&apos;t risk a rejected listing or a lawsuit. Let metes rewrite this description from scratch. For just $35, our AI generates a compelling, 100% compliant MLS description, builds a custom Neighborhood Guide, and sorts your 50 raw photos.
                    </p>
                    <Link href="/" style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "12px 24px", borderRadius: "9px", background: C.forest, color: C.creamWarm, textDecoration: "none", fontSize: "13px", fontWeight: 500, fontFamily: "var(--font-manrope, sans-serif)" }}>
                      Generate a Compliant Listing Kit — $35 →
                    </Link>
                  </div>
                </div>
              )}

              {scanStatus === "passed" && result && (
                <div style={{ background: C.successBg, borderRadius: "14px", border: `1px solid ${C.success}`, padding: "28px 32px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
                    <CheckCircle2 style={{ width: "20px", height: "20px", color: C.success, flexShrink: 0 }} />
                    <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "20px", color: C.forestDeep, margin: 0 }}>✅ Zero FHA Risks Detected. But is it ready to sell?</h2>
                  </div>
                  {result.reviewer_notes && (
                    <p style={{ fontSize: "13px", color: C.inkSoft, lineHeight: 1.6, marginBottom: "20px", fontStyle: "italic" }}>{result.reviewer_notes}</p>
                  )}
                  <div style={{ borderTop: `1px solid rgba(92,138,110,0.2)`, paddingTop: "20px" }}>
                    <p style={{ fontSize: "14px", color: C.forestDeep, lineHeight: 1.6, marginBottom: "16px" }}>
                      Your copy is legally safe, but is it optimized to stop the scroll? metes can instantly upgrade this draft — hyper-local Neighborhood Guide, sorted photos, and platform-specific social posts in under 60 seconds.
                    </p>
                    <Link href="/" style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "12px 24px", borderRadius: "9px", background: C.forest, color: C.creamWarm, textDecoration: "none", fontSize: "13px", fontWeight: 500, fontFamily: "var(--font-manrope, sans-serif)" }}>
                      Upgrade to the Complete Marketing Kit — $35 →
                    </Link>
                  </div>
                </div>
              )}

            </div>
          </div>
        </section>
      )}

      {/* ── $16,000 MISTAKE ── */}
      <section style={{ padding: "80px 0", background: C.cream }}>
        <div className={CONTENT}>
          <div style={{ maxWidth: "760px" }}>
            <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "clamp(22px, 3vw, 36px)", letterSpacing: "0.02em", color: C.forestDeep, marginBottom: "20px", lineHeight: 1.2 }}>
              The $16,000 Mistake You Didn&apos;t Know You Made.
            </h2>
            <p style={{ fontSize: "clamp(14px, 1.2vw, 16px)", lineHeight: 1.7, color: C.inkSoft, marginBottom: "16px" }}>
              Writing &ldquo;perfect for a young family&rdquo; or &ldquo;walking distance to the park&rdquo; might sound like great marketing, but to the Department of Housing and Urban Development (HUD), it&apos;s a violation of the Fair Housing Act.
            </p>
            <p style={{ fontSize: "clamp(14px, 1.2vw, 16px)", lineHeight: 1.7, color: C.inkSoft }}>
              A single flagged word can lead to a rejected MLS listing, a suspended social media ad account, or a devastating discrimination lawsuit resulting in fines upwards of <strong style={{ color: C.forestDeep }}>$16,000 for a first offense</strong>. You don&apos;t have time to memorize the rulebook. Let metes do it for you.
            </p>
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section style={{ padding: "80px 0", background: C.creamWarm, borderTop: `1px solid ${C.border}`, borderBottom: `1px solid ${C.border}` }}>
        <div className={CONTENT}>
          {sectionLabel("How it works")}
          <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "clamp(22px, 3vw, 36px)", letterSpacing: "0.02em", color: C.forestDeep, marginBottom: "40px" }}>
            AI-Powered Protection in 3 Seconds.
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {[
              ["STEP 01", "Paste Your Draft", "Drop your rough notes or current MLS description into the scanner above."],
              ["STEP 02", "Instant Risk Analysis", "Our specialized real estate AI cross-references your text against established FHA guidelines and known exclusionary terms."],
              ["STEP 03", "Clear Results", "We highlight the exact issues that put you at risk and explain why they are problematic so you can rewrite with confidence."],
            ].map(([step, title, body]) => (
              <div key={step} style={{ background: C.bgCard, borderRadius: "12px", padding: "24px", border: `1px solid ${C.border}` }}>
                <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", color: C.goldDeep, letterSpacing: "0.08em", marginBottom: "14px" }}>{step}</div>
                <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "15px", color: C.forestDeep, marginBottom: "8px" }}>{title}</div>
                <div style={{ fontSize: "13px", lineHeight: 1.6, color: C.inkSoft }}>{body}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FHA CHECKLIST ── */}
      <section style={{ padding: "80px 0", background: C.cream }}>
        <div className={CONTENT}>
          <div style={{ maxWidth: "860px" }}>
            {sectionLabel("Reference guide")}
            <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "clamp(22px, 3vw, 36px)", letterSpacing: "0.02em", color: C.forestDeep, marginBottom: "16px", lineHeight: 1.2 }}>
              The Ultimate FHA Compliance Checklist: Words to Avoid in Real Estate Ads
            </h2>
            <p style={{ fontSize: "clamp(14px, 1.2vw, 16px)", lineHeight: 1.7, color: C.inkSoft, marginBottom: "48px" }}>
              Even experienced agents unintentionally use language that violates the Fair Housing Act or local MLS rules. HUD strictly prohibits advertising that indicates any preference, limitation, or discrimination based on race, color, religion, sex, handicap, familial status, or national origin.
            </p>

            <div style={{ display: "flex", flexDirection: "column" as const, gap: "48px" }}>
              {FHA_CATEGORIES.map((category, ci) => (
                <div key={ci}>
                  <h3 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "20px", color: C.forestDeep, marginBottom: "10px", letterSpacing: "0.01em" }}>
                    {category.title}
                  </h3>
                  <p style={{ fontSize: "14px", lineHeight: 1.6, color: C.inkSoft, marginBottom: "24px" }}>{category.intro}</p>
                  <div style={{ display: "flex", flexDirection: "column" as const, gap: "12px" }}>
                    {category.items.map((item) => (
                      <div key={item.num} style={{ background: C.bgCard, borderRadius: "12px", padding: "20px 24px", border: `1px solid ${C.border}` }}>
                        <p style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "12px", fontWeight: 600, color: C.forestDeep, marginBottom: "12px" }}>
                          {item.num}. {item.phrase}
                        </p>
                        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                          <div style={{ background: C.warnBg, borderRadius: "8px", padding: "12px 14px" }}>
                            <p style={{ fontSize: "10px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" as const, color: C.warn, marginBottom: "4px", fontFamily: "var(--font-jetbrains, monospace)" }}>The Risk</p>
                            <p style={{ fontSize: "12px", lineHeight: 1.55, color: C.ink }}>{item.risk}</p>
                          </div>
                          <div style={{ background: C.successBg, borderRadius: "8px", padding: "12px 14px" }}>
                            <p style={{ fontSize: "10px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" as const, color: C.success, marginBottom: "4px", fontFamily: "var(--font-jetbrains, monospace)" }}>Safe Alternative</p>
                            <p style={{ fontSize: "12px", lineHeight: 1.55, color: C.ink }}>{item.safe}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── BOTTOM CTA ── */}
      <section style={{ padding: "80px 0", background: C.forest, position: "relative" as const, overflow: "hidden" }}>
        <div style={{ position: "absolute" as const, inset: 0, backgroundImage: "linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px)", backgroundSize: "32px 32px", pointerEvents: "none" as const }} />
        <div className={CONTENT} style={{ position: "relative" as const, zIndex: 1 }}>
          <div style={{ maxWidth: "640px" }}>
            {sectionLabel("Stop guessing", true)}
            <h2 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "clamp(22px, 3vw, 40px)", letterSpacing: "0.02em", color: "#F4F0E8", marginBottom: "16px", lineHeight: 1.15 }}>
              Start Scanning.
            </h2>
            <p style={{ fontSize: "clamp(14px, 1.2vw, 16px)", lineHeight: 1.7, color: "rgba(244,240,232,0.78)", marginBottom: "32px" }}>
              Memorizing every nuance of the Fair Housing Act is impossible while managing clients, contracts, and showings. Scroll up to paste your draft — or let metes handle the whole thing for $35.
            </p>
            <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" as const }}>
              <Link href="/" style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "14px 28px", borderRadius: "9px", background: C.gold, color: C.forestDeep, textDecoration: "none", fontSize: "14px", fontWeight: 500, fontFamily: "var(--font-manrope, sans-serif)" }}>
                Generate Your Compliant Listing Kit — $35 →
              </Link>
              <button
                onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
                style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "14px 28px", borderRadius: "9px", background: "transparent", color: "#F4F0E8", border: "1px solid rgba(244,240,232,0.3)", fontSize: "14px", fontWeight: 500, cursor: "pointer", fontFamily: "var(--font-manrope, sans-serif)" }}
              >
                Scan my description ↑
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{ background: C.forestDeep, padding: "32px 0" }}>
        <div className={CONTENT} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap" as const, gap: "16px" }}>
          <Link href="/" style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 500, fontSize: "15px", color: "#F4F0E8", textDecoration: "none" }}>metes</Link>
          <p style={{ fontSize: "12px", color: "rgba(244,240,232,0.5)", fontFamily: "var(--font-jetbrains, monospace)" }}>
            metes · AI-powered listing marketing · metes.app
          </p>
        </div>
      </footer>
    </div>
  );
}