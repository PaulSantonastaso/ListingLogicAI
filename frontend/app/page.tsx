import { Composer } from "@/components/home/Composer";

// ─────────────────────────────────────────────────────────────────
// Metes brand palette — scoped to landing page
// ─────────────────────────────────────────────────────────────────

const C = {
  cream:        "#EFEAE0",
  creamWarm:    "#F4F0E8",
  bgCard:       "#FAF7F0",
  forest:       "#1F3D2E",
  forestDeep:   "#14271E",
  moss:         "#4A6B53",
  gold:         "#B89968",
  goldDeep:     "#9A7E50",
  goldSoft:     "#D9C49C",
  ink:          "#14271E",
  inkSoft:      "#4A6B53",
  muted:        "rgba(20,39,30,0.55)",
  border:       "rgba(20,39,30,0.10)",
  borderDark:   "rgba(244,240,232,0.12)",
  creamText:    "rgba(244,240,232,0.78)",
  creamMuted:   "rgba(244,240,232,0.55)",
  creamDim:     "rgba(244,240,232,0.70)",
};

const CONTENT = "mx-auto w-full max-w-[1280px] px-6 lg:px-12";

// ─────────────────────────────────────────────────────────────────
// Sub-components
// ─────────────────────────────────────────────────────────────────

function SectionLabel({ children, light }: { children: React.ReactNode; light?: boolean }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: "8px",
      fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px",
      color: light ? "#D9C49C" : "#9A7E50",
      letterSpacing: "0.14em", textTransform: "uppercase" as const, marginBottom: "16px",
    }}>
      <span style={{ width: "18px", height: "1px", background: light ? "#D9C49C" : "#9A7E50", display: "inline-block" }} />
      {children}
    </div>
  );
}

const sectionHeadline: React.CSSProperties = {
  fontFamily: "var(--font-manrope, sans-serif)",
  fontWeight: 500,
  fontSize: "clamp(28px, 4vw, 48px)",
  lineHeight: 1.06,
  letterSpacing: "-0.015em",
  color: "#14271E",
};

const sectionSub: React.CSSProperties = {
  fontSize: "clamp(14px, 1.2vw, 16px)",
  lineHeight: 1.6,
  color: "#4A6B53",
  maxWidth: "560px",
};

const proofHeadline: React.CSSProperties = {
  fontFamily: "var(--font-manrope, sans-serif)",
  fontWeight: 500, fontSize: "16px", lineHeight: 1.3,
  letterSpacing: "-0.015em", color: "#14271E",
};

const proofBody: React.CSSProperties = {
  fontSize: "12.5px", lineHeight: 1.55, color: "#4A6B53",
};

const moatBody: React.CSSProperties = {
  fontSize: "14px", lineHeight: 1.6, color: "#4A6B53", margin: 0,
};

const baLabel: React.CSSProperties = {
  position: "absolute", top: "12px", left: "12px",
  background: "rgba(20,39,30,0.65)", color: "#F4F0E8",
  fontFamily: "var(--font-jetbrains, monospace)", fontSize: "10px",
  letterSpacing: "0.08em", textTransform: "uppercase" as const,
  padding: "4px 9px", borderRadius: "4px",
};

function ProofCard({ tag, tagColor, tagBg, children }: {
  tag: string; tagColor: string; tagBg: string; children: React.ReactNode;
}) {
  return (
    <div className="proof-card" style={{ background: "#FAF7F0", borderRadius: "12px", border: "1px solid rgba(20,39,30,0.10)", padding: "18px 18px 16px", display: "flex", flexDirection: "column", gap: "12px" }}>
      <span style={{ display: "inline-flex", alignItems: "center", alignSelf: "flex-start", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "10px", letterSpacing: "0.08em", textTransform: "uppercase" as const, color: tagColor, padding: "4px 8px", background: tagBg, borderRadius: "4px" }}>{tag}</span>
      {children}
    </div>
  );
}

function SocialPost({ platform, children }: { platform: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "rgba(20,39,30,0.03)", borderRadius: "8px", padding: "12px", fontSize: "12px", lineHeight: 1.5, color: "#14271E" }}>
      <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "9px", letterSpacing: "0.08em", textTransform: "uppercase" as const, color: "rgba(20,39,30,0.55)", marginBottom: "6px" }}>{platform}</div>
      {children}
    </div>
  );
}

function MoatCard({ num, title, children }: { num: string; title: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "#EFEAE0", borderRadius: "14px", padding: "28px", border: "1px solid rgba(20,39,30,0.10)", display: "flex", flexDirection: "column", gap: "16px" }}>
      <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "#1F3D2E", color: "#B89968", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "12px", fontWeight: 500 }}>{num}</div>
      <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 700, fontSize: "18px", lineHeight: 1.25, letterSpacing: "-0.015em", color: "#14271E" }}>{title}</div>
      {children}
    </div>
  );
}

function Highlight({ children }: { children: React.ReactNode }) {
  return (
    <span style={{ background: "rgba(184,153,104,0.25)", color: "#14271E", padding: "1px 5px", borderRadius: "3px", fontWeight: 500 }}>{children}</span>
  );
}

function CompareRow({ label, color, children }: { label: string; color: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "rgba(20,39,30,0.04)", borderRadius: "8px", padding: "10px 12px", fontSize: "12px", lineHeight: 1.5 }}>
      <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "9px", letterSpacing: "0.08em", textTransform: "uppercase" as const, color, marginBottom: "4px" }}>{label}</div>
      <div style={{ color: "#14271E", fontStyle: "italic" }}>{children}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────

export default function HomePage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "metes",
            "url": "https://www.metes.app",
            "description": "AI-powered listing marketing for high-performing solo real estate agents. Generate MLS descriptions, social posts, email campaigns, and Fair Housing audits from listing photos and agent notes.",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "offers": {
              "@type": "Offer",
              "price": "35.00",
              "priceCurrency": "USD",
              "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "price": "35.00",
                "priceCurrency": "USD",
                "unitText": "per listing"
              }
            },
            "audience": {
              "@type": "Audience",
              "audienceType": "Real estate agents"
            },
            "featureList": [
              "MLS listing description",
              "Social media launch pack",
              "4-email campaign sequence",
              "Fair Housing compliance audit",
              "Photo ranking and renaming",
              "Professional photo editing"
            ]
          })
        }}
      />
      <style>{`
        html, body { background: #EFEAE0; }

        @keyframes metespulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.45; transform: scale(0.8); }
        }
        .metes-pulse { animation: metespulse 1.6s ease-in-out infinite; }

        .proof-scroll {
          display: flex;
          gap: 12px;
          overflow-x: auto;
          scroll-snap-type: x mandatory;
          scrollbar-width: none;
        }
        .proof-scroll::-webkit-scrollbar { display: none; }

        @media (min-width: 1024px) {
          .proof-scroll {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            overflow-x: visible;
          }
        }

        .proof-card {
          flex-shrink: 0;
          width: 80vw;
          max-width: 340px;
          scroll-snap-align: start;
        }

        @media (min-width: 1024px) {
          .proof-card { width: auto; max-width: none; }
        }

        .ba-card-before {
          background: linear-gradient(180deg, #8C9499 0%, #A0A8AC 35%, #6F5A4A 60%, #5C4A3D 100%);
        }
        .ba-card-after {
          background: linear-gradient(180deg, #6BA3D6 0%, #98C4E5 35%, #B89968 60%, #8A6F44 100%);
        }

        .grid-bg { position: relative; }
        .grid-bg::before {
          content: '';
          position: absolute;
          inset: 0;
          background-image:
            linear-gradient(rgba(184,153,104,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(184,153,104,0.06) 1px, transparent 1px);
          background-size: 32px 32px;
          pointer-events: none;
        }
      `}</style>

      <div style={{ background: C.cream, minHeight: "100vh" }}>

        {/* ── NAV ── */}
        <nav style={{ borderBottom: `1px solid ${C.border}`, background: C.cream, position: "sticky", top: 0, zIndex: 50 }}>
          <div className={CONTENT} style={{ height: "60px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 700, fontSize: "17px", color: C.forest }}>
              <div style={{ width: "24px", height: "24px", background: C.forest, borderRadius: "6px", position: "relative", flexShrink: 0 }}>
                <div style={{ position: "absolute", inset: "6px", border: `1.5px solid ${C.gold}`, borderRadius: "2px" }} />
              </div>
              metes
            </div>
            <div style={{ display: "flex", gap: "24px", alignItems: "center" }}>
              <a href="#how-it-works" style={{ fontSize: "13px", fontWeight: 500, color: C.inkSoft, textDecoration: "none" }}>How it works</a>
              <a href="#pricing" style={{ fontSize: "13px", fontWeight: 500, color: C.inkSoft, textDecoration: "none" }}>Pricing</a>
            </div>
          </div>
        </nav>

        {/* ── HERO ── */}
        <section className="grid-bg" style={{ background: C.forest, padding: "80px 0 56px" }}>
          <div className={CONTENT} style={{ position: "relative", zIndex: 1 }}>
            <div style={{ maxWidth: "760px", margin: "0 auto", textAlign: "center" }}>
              <div style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "5px 14px", border: `1px solid ${C.borderDark}`, borderRadius: "100px", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", letterSpacing: "0.06em", color: C.creamMuted, marginBottom: "24px" }}>
                <span className="metes-pulse" style={{ width: "6px", height: "6px", background: C.gold, borderRadius: "50%", display: "block" }} />
                AI-powered listing marketing
              </div>
              <h1 style={{ fontFamily: "var(--font-manrope, sans-serif)", fontSize: "clamp(40px, 6vw, 76px)", lineHeight: 1.02, marginBottom: "20px", color: C.creamWarm, fontWeight: 500 }}>
                The marketing kit your listing{" "}
                <em style={{ fontStyle: "normal", color: C.gold }}>deserved</em>.
              </h1>
              <p style={{ fontSize: "clamp(15px, 1.5vw, 17px)", lineHeight: 1.55, color: C.creamText, maxWidth: "480px", margin: "0 auto 36px" }}>
                Upload your photos and notes. Get the full marketing kit — done.
              </p>
            </div>
            <div style={{ maxWidth: "760px", margin: "0 auto" }}>
              <Composer className="mb-0 mx-0" />
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "16px", marginTop: "24px", flexWrap: "wrap", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", color: C.creamMuted, letterSpacing: "0.04em" }}>
                <span><strong style={{ color: C.goldSoft, fontWeight: 500 }}>$35</strong> per listing</span>
                <span style={{ width: "3px", height: "3px", background: "rgba(244,240,232,0.3)", borderRadius: "50%", display: "inline-block" }} />
                <span>No subscription</span>
                <span style={{ width: "3px", height: "3px", background: "rgba(244,240,232,0.3)", borderRadius: "50%", display: "inline-block" }} />
                <span><strong style={{ color: C.goldSoft, fontWeight: 500 }}>See everything</strong> before you pay</span>
              </div>
            </div>
          </div>
        </section>

        {/* ── FREE PREVIEW PROOF ── */}
        <section style={{ padding: "80px 0", background: C.cream }}>
          <div className={CONTENT}>
            <div style={{ marginBottom: "40px" }}>
              <SectionLabel>Free preview</SectionLabel>
              <h2 style={{ ...sectionHeadline, marginBottom: "12px" }}>
                See the whole thing before you pay <em style={{ fontStyle: "normal", color: C.goldDeep }}>$35</em>.
              </h2>
              <p style={sectionSub}>
                No signup, no email, no trial. Upload, generate, scroll through everything we made — then decide if it&apos;s worth the download.
              </p>
            </div>
            <div className="proof-scroll">
              <ProofCard tag="MLS Description" tagColor={C.moss} tagBg="rgba(74,107,83,0.08)">
                <div style={proofHeadline}>A Spanish revival tucked into the Catalina foothills.</div>
                <div style={proofBody}>Saltillo floors run from the entryway to a sun-soaked primary suite that opens onto its own private patio. The newly renovated kitchen anchors the home, while a year-round heated pool below frames the view.</div>
                <div style={{ marginTop: "auto", paddingTop: "12px", borderTop: `1px solid ${C.border}`, display: "flex", justifyContent: "space-between", fontSize: "11px", color: C.muted }}>
                  <span><strong style={{ color: C.forest, fontWeight: 500 }}>1,247</strong> chars · MLS-ready</span>
                  <span>Lifestyle tone</span>
                </div>
              </ProofCard>

              <ProofCard tag="Social Launch Pack" tagColor={C.goldDeep} tagBg="rgba(184,153,104,0.12)">
                <div style={proofHeadline}>Ready-to-post for every channel.</div>
                <SocialPost platform="Instagram · Caption 1">Sun, saltillo, and a pool that&apos;s heated year-round — 412 Oak Ridge just hit the market. 4 bed / 3 bath in the Catalinas. DM for a private tour. 🌵</SocialPost>
                <SocialPost platform="Facebook · Just Listed">New listing alert: $1.275M Spanish revival on a quiet ridge with Catalina views. Open House Saturday 1–3.</SocialPost>
              </ProofCard>

              <ProofCard tag="Email Campaign" tagColor={C.forest} tagBg="rgba(31,61,46,0.08)">
                <div style={proofHeadline}>Four emails. Sequenced for the listing&apos;s full lifecycle.</div>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {[["01", "Just Listed: Catalina foothills, $1.275M"], ["02", "Open House Saturday — 412 Oak Ridge"], ["03", "Why this Spanish revival is special"], ["04", "Just Sold: 412 Oak Ridge, in 11 days"]].map(([num, subject]) => (
                    <div key={num} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "8px 10px", background: "rgba(20,39,30,0.03)", borderRadius: "6px", fontSize: "12px" }}>
                      <span style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "10px", color: C.goldDeep, flexShrink: 0 }}>{num}</span>
                      <span style={{ color: C.ink, fontWeight: 500 }}>{subject}</span>
                    </div>
                  ))}
                </div>
              </ProofCard>

              <ProofCard tag="Compliance Audit" tagColor="#5C8A6E" tagBg="rgba(92,138,110,0.12)">
                <div style={proofHeadline}>Fair Housing reviewed before you publish.</div>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {["No protected-class language detected", "\"Walkable\" flagged & approved with context", "All 4 emails + 3 social posts cleared"].map((text) => (
                    <div key={text} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "8px 10px", background: "rgba(20,39,30,0.03)", borderRadius: "6px", fontSize: "12px" }}>
                      <div style={{ width: "16px", height: "16px", borderRadius: "50%", background: "#5C8A6E", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "9px", flexShrink: 0 }}>✓</div>
                      <span style={{ color: C.ink, fontWeight: 500 }}>{text}</span>
                    </div>
                  ))}
                </div>
              </ProofCard>

              <ProofCard tag="Photo Curation" tagColor={C.moss} tagBg="rgba(74,107,83,0.08)">
                <div style={proofHeadline}>Your top 25 photos, ranked and renamed.</div>
                <div style={{ background: "rgba(20,39,30,0.06)", borderRadius: "8px", padding: "14px", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", lineHeight: 1.7 }}>
                  {[["01", "front_exterior", "_hero"], ["02", "primary_suite", "_natural_light"], ["03", "pool", "_screened"], ["04", "kitchen", "_island"]].map(([n, r, f]) => (
                    <div key={n}><span style={{ color: C.goldDeep }}>{n}</span> <span style={{ color: C.forest }}>{r}</span><span style={{ color: C.muted }}>{f}</span></div>
                  ))}
                </div>
                <div style={proofBody}>Pool before garage. Hero shot first. Drag, drop, publish.</div>
              </ProofCard>
            </div>
          </div>
        </section>

        {/* ── FOUR MOATS ── */}
        <section style={{ padding: "80px 0", background: C.creamWarm }} id="why-metes">
          <div className={CONTENT}>
            <SectionLabel>Why Metes</SectionLabel>
            <h2 style={{ ...sectionHeadline, marginBottom: "48px" }}>
              Four things <em style={{ fontStyle: "normal", color: C.goldDeep }}>no one else does</em>.
            </h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <MoatCard num="01" title="We read your photos, not just your notes.">
                <p style={moatBody}>Our image intelligence finds features you forgot to mention. Saltillo floors, screen enclosures, kitchen islands — all detected automatically and woven into the copy.</p>
                <div style={{ background: "rgba(20,39,30,0.04)", borderRadius: "10px", padding: "14px" }}>
                  <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "9px", letterSpacing: "0.08em", textTransform: "uppercase" as const, color: C.muted, marginBottom: "4px" }}>From your notes</div>
                  <div style={{ color: C.ink, marginBottom: "8px", fontSize: "12px" }}>&ldquo;4 bed, 3 bath, recently renovated&rdquo;</div>
                  <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "9px", letterSpacing: "0.08em", textTransform: "uppercase" as const, color: C.muted, marginBottom: "4px" }}>From your photos</div>
                  <div style={{ fontSize: "12px" }}>+ <Highlight>saltillo floors</Highlight> · <Highlight>screen-enclosed pool</Highlight> · <Highlight>vaulted ceilings</Highlight></div>
                </div>
              </MoatCard>

              <MoatCard num="02" title="Lifestyle-forward, never utility-forward.">
                <p style={moatBody}>Other AI leads with garages and granite. Metes leads with what people actually fall in love with — the light, the suite, the moment of arriving home.</p>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  <CompareRow label="Typical AI" color="#C97B5C">&ldquo;4-bedroom home with 2-car garage and granite countertops.&rdquo;</CompareRow>
                  <CompareRow label="Metes" color="#5C8A6E">&ldquo;Saltillo floors run to a sun-soaked primary suite with its own private patio.&rdquo;</CompareRow>
                </div>
              </MoatCard>

              <MoatCard num="03" title="Fair Housing audit on every asset.">
                <p style={moatBody}>A liability shield, not a checklist. Metes reviews every line of the MLS, every social post, every email — flagging protected-class language before you publish. One mistake costs more than every Metes listing you&apos;ll ever buy.</p>
              </MoatCard>

              <MoatCard num="04" title="Top photos ranked & renamed for upload.">
                <p style={moatBody}>Your best 25 photos, scored by marketing impact and renamed to MLS-friendly filenames. Pool before garage. Hero shot first.</p>
                <div style={{ background: C.forestDeep, borderRadius: "8px", padding: "12px 14px", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", lineHeight: 1.7 }}>
                  {[["01", "front_exterior", "_hero.jpg"], ["02", "primary_suite", "_natural_light.jpg"], ["03", "pool", "_screened.jpg"]].map(([n, r, e]) => (
                    <div key={n}><span style={{ color: C.gold }}>{n}</span> <span style={{ color: C.creamWarm }}>{r}</span><span style={{ color: "rgba(244,240,232,0.6)" }}>{e}</span></div>
                  ))}
                </div>
              </MoatCard>
            </div>
          </div>
        </section>

        {/* ── HOW IT WORKS ── */}
        <section style={{ padding: "80px 0", background: C.cream }} id="how-it-works">
          <div className={CONTENT}>
            <SectionLabel>How it works</SectionLabel>
            <h2 style={{ ...sectionHeadline, marginBottom: "40px" }}>
              Three steps. <em style={{ fontStyle: "normal", color: C.goldDeep }}>One coffee.</em>
            </h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {[
                ["STEP 01", "Upload photos & notes", "Drop in up to 50 photos and paste whatever you'd tell a buyer — formal or scattered, both work."],
                ["STEP 02", "Review what we extracted", "Tap any field to fix what the AI got wrong. You stay in control before a single asset is generated."],
                ["STEP 03", "Preview, then download", "See the full marketing kit. If it works, $35 unlocks the ZIP. If not, walk away — no card on file."],
              ].map(([step, title, body]) => (
                <div key={step} style={{ border: `1px solid ${C.border}`, borderRadius: "12px", padding: "24px", background: C.creamWarm }}>
                  <div style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", color: C.goldDeep, letterSpacing: "0.08em", marginBottom: "14px" }}>{step}</div>
                  <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 700, fontSize: "15px", color: C.forestDeep, marginBottom: "8px" }}>{title}</div>
                  <div style={{ fontSize: "13px", lineHeight: 1.6, color: C.inkSoft }}>{body}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── PHOTO EDITING — DARK ── */}
        <section className="grid-bg" style={{ background: C.forestDeep, padding: "80px 0" }}>
          <div className={CONTENT} style={{ position: "relative", zIndex: 1 }}>
            <SectionLabel light>Photo editing add-on</SectionLabel>
            <h2 style={{ ...sectionHeadline, color: C.creamWarm, marginBottom: "12px" }}>
              Skies that always look <em style={{ fontStyle: "normal", color: C.gold }}>like the day you wished it was</em>.
            </h2>
            <p style={{ ...sectionSub, color: C.creamDim, marginBottom: "40px", maxWidth: "600px" }}>
              Most exterior shots get gray, blown-out, or overcast skies. Our photo editing add-on swaps them for clean blue skies, fixes color and perspective on the rest, and delivers them straight to your email.
            </p>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2" style={{ marginBottom: "24px" }}>
              <div style={{ borderRadius: "12px", overflow: "hidden", aspectRatio: "4/3", position: "relative" }} className="ba-card-before">
                <span style={baLabel}>Before</span>
              </div>
              <div style={{ borderRadius: "12px", overflow: "hidden", aspectRatio: "4/3", position: "relative" }} className="ba-card-after">
                <span style={{ ...baLabel, background: "rgba(184,153,104,0.95)", color: C.forestDeep }}>After</span>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              {["Blue sky replacement", "Color correction", "Perspective fix"].map((cap) => (
                <div key={cap} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "12px 16px", background: "rgba(244,240,232,0.05)", border: `1px solid ${C.borderDark}`, borderRadius: "10px", fontSize: "13px", color: C.creamWarm }}>
                  <span style={{ width: "6px", height: "6px", background: C.gold, borderRadius: "50%", flexShrink: 0, display: "inline-block" }} />
                  {cap}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── PRICING ── */}
        <section style={{ padding: "80px 0", background: C.cream }} id="pricing">
          <div className={CONTENT}>
            <SectionLabel>Pricing</SectionLabel>
            <h2 style={{ ...sectionHeadline, marginBottom: "48px" }}>
              Pay per listing.<br /><em style={{ fontStyle: "normal", color: C.goldDeep }}>No subscription.</em>
            </h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:max-w-3xl">
              <div style={{ background: C.creamWarm, borderRadius: "14px", padding: "32px 28px", border: `1px solid ${C.border}` }}>
                <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 900, fontSize: "48px", letterSpacing: "-0.04em", color: C.forestDeep, lineHeight: 1, marginBottom: "6px" }}>$35</div>
                <div style={{ fontSize: "14px", fontWeight: 500, color: C.inkSoft, marginBottom: "28px" }}>Listing Copy Package</div>
                <ul style={{ listStyle: "none", padding: 0, marginBottom: "28px", display: "flex", flexDirection: "column", gap: "8px" }}>
                  {["MLS-ready listing description", "Social launch pack (Facebook + 2× Instagram)", "4-email campaign sequence", "Fair Housing compliance audit", "Top 25 photos ranked & renamed"].map((f) => (
                    <li key={f} style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "13px", lineHeight: 1.5, color: C.inkSoft }}>
                      <span style={{ width: "5px", height: "5px", borderRadius: "50%", background: C.goldDeep, marginTop: "7px", flexShrink: 0, display: "inline-block" }} />
                      {f}
                    </li>
                  ))}
                </ul>
                <a href="#top" style={{ display: "block", width: "100%", textAlign: "center", padding: "14px", borderRadius: "9px", fontSize: "14px", fontWeight: 500, textDecoration: "none", background: C.forest, color: C.creamWarm, fontFamily: "var(--font-onest, sans-serif)" }}>
                  Start a listing
                </a>
              </div>

              <div style={{ background: C.creamWarm, borderRadius: "14px", padding: "32px 28px", border: `1px dashed ${C.goldDeep}`, position: "relative" }}>
                <div style={{ position: "absolute", top: "-11px", left: "24px", background: C.gold, color: C.forestDeep, fontFamily: "var(--font-jetbrains, monospace)", fontSize: "10px", fontWeight: 500, letterSpacing: "0.06em", textTransform: "uppercase" as const, padding: "3px 10px", borderRadius: "100px" }}>+ Add-on</div>
                <div style={{ fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 900, fontSize: "48px", letterSpacing: "-0.04em", color: C.forestDeep, lineHeight: 1, marginBottom: "6px" }}>+ $45</div>
                <div style={{ fontSize: "14px", fontWeight: 500, color: C.inkSoft, marginBottom: "28px" }}>Add Photo Editing</div>
                <ul style={{ listStyle: "none", padding: 0, marginBottom: "28px", display: "flex", flexDirection: "column", gap: "8px" }}>
                  {["Blue sky replacement on eligible exteriors", "Color correction across all photos", "Perspective & level correction", "Enhanced photos delivered to your email"].map((f) => (
                    <li key={f} style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "13px", lineHeight: 1.5, color: C.inkSoft }}>
                      <span style={{ width: "5px", height: "5px", borderRadius: "50%", background: C.goldDeep, marginTop: "7px", flexShrink: 0, display: "inline-block" }} />
                      {f}
                    </li>
                  ))}
                </ul>
                <a href="#top" style={{ display: "block", width: "100%", textAlign: "center", padding: "14px", borderRadius: "9px", fontSize: "14px", fontWeight: 500, textDecoration: "none", background: "transparent", color: C.forest, border: `1px solid ${C.forest}`, fontFamily: "var(--font-onest, sans-serif)" }}>
                  Add at checkout
                </a>
              </div>
            </div>
            <p style={{ marginTop: "24px", fontSize: "13px", color: C.muted }}>
              No card on file. <strong style={{ color: C.forest, fontWeight: 500 }}>Generate first, decide if it&apos;s worth $35.</strong>
            </p>
          </div>
        </section>

        {/* ── FOOTER ── */}
        <footer style={{ background: C.forestDeep, padding: "64px 0 32px" }}>
          <div className={CONTENT}>
            <div className="grid grid-cols-2 gap-8 sm:grid-cols-[2fr_1fr_1fr_1fr]" style={{ marginBottom: "48px" }}>
              <div className="col-span-2 sm:col-span-1">
                <div style={{ display: "flex", alignItems: "center", gap: "8px", fontFamily: "var(--font-manrope, sans-serif)", fontWeight: 700, fontSize: "17px", color: C.creamWarm, marginBottom: "16px" }}>
                  <div style={{ width: "24px", height: "24px", background: C.forest, borderRadius: "6px", position: "relative", flexShrink: 0 }}>
                    <div style={{ position: "absolute", inset: "6px", border: `1.5px solid ${C.gold}`, borderRadius: "2px" }} />
                  </div>
                  metes
                </div>
                <p style={{ fontSize: "13px", lineHeight: 1.6, color: "rgba(244,240,232,0.65)", maxWidth: "280px" }}>
                  The marketing kit for the modern listing. Built for solo agents who&apos;d rather be showing homes than writing about them.
                </p>
              </div>
              {([["Product", ["How it works", "See an example", "Pricing"]], ["Company", ["About", "Contact"]], ["Legal", ["Terms", "Privacy", "MLS compliance"]]] as [string, string[]][]).map(([heading, links]) => (
                <div key={heading}>
                  <h4 style={{ fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", letterSpacing: "0.14em", textTransform: "uppercase" as const, color: C.goldSoft, marginBottom: "16px" }}>{heading}</h4>
                  {links.map((link) => (
                    <a key={link} href="#" style={{ display: "block", color: "rgba(244,240,232,0.78)", textDecoration: "none", fontSize: "13px", marginBottom: "10px" }}>{link}</a>
                  ))}
                </div>
              ))}
            </div>
            <div style={{ borderTop: `1px solid ${C.borderDark}`, paddingTop: "24px", display: "flex", justifyContent: "space-between", fontFamily: "var(--font-jetbrains, monospace)", fontSize: "11px", color: "rgba(244,240,232,0.5)", letterSpacing: "0.04em" }}>
              <span>© 2026 metes</span>
              <span>metes.app</span>
            </div>
          </div>
        </footer>

      </div>
    </>
  );
}