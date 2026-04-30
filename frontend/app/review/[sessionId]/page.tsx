"use client";

import { useState, use, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Star } from "lucide-react";
import { Navbar } from "@/components/layout/Navbar";
import { PropertyDetailsCard } from "@/components/shared/PropertyDetailsCard";
import { MobileStickyBar } from "@/components/shared/MobileStickyBar";
import { DetectedFeaturesGrid } from "@/components/review/DetectedFeaturesGrid";
import { generateListing, getSession, getImageUrl, ApiError } from "@/lib/api";
import type { PropertyDetails, DetectedFeature, Session, ListingImage } from "@/types";
import posthog from "posthog-js";

// ─────────────────────────────────────────────────────────────────
// Page — server params, client logic
// ─────────────────────────────────────────────────────────────────

export default function ReviewPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = use(params);
  return <ReviewPageContent sessionId={sessionId} />;
}

// ─────────────────────────────────────────────────────────────────
// AI Intelligence Sidebar Panel
// ─────────────────────────────────────────────────────────────────

function AiIntelligencePanel({
  sessionId,
  images,
}: {
  sessionId: string;
  images: ListingImage[];
}) {
  const heroImage = images.find((img) => img.rank === 1);
  const socialImages = images.filter((img) => img.selectedForSocial).slice(0, 5);

  if (!heroImage) return null;

  return (
    <div style={{
      borderRadius: "10px",
      border: "1px solid hsl(var(--border))",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{
        display: "flex", alignItems: "center", gap: "8px",
        padding: "10px 14px",
        borderBottom: "1px solid hsl(var(--border))",
        background: "hsl(var(--muted))",
      }}>
        <div style={{
          width: "16px", height: "16px", borderRadius: "50%",
          background: "var(--metes-forest)",
          display: "flex", alignItems: "center", justifyContent: "center",
          flexShrink: 0,
        }}>
          <Star style={{ width: "9px", height: "9px", fill: "var(--metes-cream)", color: "var(--metes-cream)" }} />
        </div>
        <span style={{
          fontSize: "10px", fontWeight: 600, letterSpacing: "0.1em",
          textTransform: "uppercase", color: "var(--metes-ink-soft)",
        }}>
          AI selected your shots
        </span>
      </div>

      <div style={{ padding: "14px" }}>
        {/* Hero */}
        <div style={{
          display: "flex", alignItems: "center", gap: "12px",
          paddingBottom: "14px", marginBottom: "14px",
          borderBottom: "1px solid hsl(var(--border))",
        }}>
          <div style={{ position: "relative", flexShrink: 0 }}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={getImageUrl(sessionId, heroImage.id)}
              alt="Hero"
              style={{ width: "64px", height: "52px", objectFit: "cover", borderRadius: "6px" }}
            />
            <div style={{
              position: "absolute", top: "-6px", right: "-6px",
              width: "16px", height: "16px", borderRadius: "50%",
              background: "var(--metes-forest)",
              border: "2px solid white",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <Star style={{ width: "8px", height: "8px", fill: "var(--metes-cream)", color: "var(--metes-cream)" }} />
            </div>
          </div>
          <div>
            <p style={{ fontSize: "12px", fontWeight: 600, color: "hsl(var(--foreground))", marginBottom: "2px" }}>
              Hero selected
            </p>
            <p style={{ fontSize: "11px", color: "hsl(var(--muted-foreground))" }}>
              {heroImage.roomType.replace(/_/g, " ")} · Quality {Math.round(heroImage.qualityScore * 100)}%
            </p>
            <p style={{ fontSize: "10px", color: "var(--metes-ink-soft)", marginTop: "3px" }}>
              This image anchors your email + social copy
            </p>
          </div>
        </div>

        {/* Social picks */}
        {socialImages.length > 0 && (
          <div>
            <p style={{ fontSize: "10px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", color: "hsl(var(--muted-foreground))", marginBottom: "8px" }}>
              Selected for social posts
            </p>
            <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
              {socialImages.map((img) => (
                <div key={img.id} style={{ position: "relative", flexShrink: 0 }}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={getImageUrl(sessionId, img.id)}
                    alt={img.roomType}
                    style={{ width: "52px", height: "40px", objectFit: "cover", borderRadius: "5px", border: "1.5px solid var(--metes-forest)" }}
                  />
                  <div style={{
                    position: "absolute", bottom: "2px", left: 0, right: 0,
                    textAlign: "center",
                  }}>
                    <span style={{
                      background: "rgba(255,255,255,0.85)",
                      padding: "0 3px", borderRadius: "2px",
                      fontSize: "8px", fontWeight: 500,
                      color: "var(--metes-forest-deep)",
                    }}>
                      {img.roomType.replace(/_/g, " ")}
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <p style={{ fontSize: "10px", color: "var(--metes-ink-soft)", marginTop: "8px" }}>
              Each post is written around the room it&apos;s paired with
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// Content — loads session, manages editable state
// ─────────────────────────────────────────────────────────────────

function ReviewPageContent({ sessionId }: { sessionId: string }) {
  const router = useRouter();

  const [session, setSession] = useState<Session | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [isLoadingSession, setIsLoadingSession] = useState(true);

  const [property, setProperty] = useState<PropertyDetails | null>(null);
  const [features, setFeatures] = useState<DetectedFeature[]>([]);

  const [isGenerating, setIsGenerating] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const poll = async () => {
      try {
        const data = await getSession(sessionId);
        if (cancelled) return;

        if (data.status === "error") {
          setLoadError("Extraction failed. Try going back and uploading again.");
          setIsLoadingSession(false);
          return;
        }

        if (data.status === "extracting") {
          setTimeout(poll, 2000);
          return;
        }

        setSession(data);
        setProperty(data.property);
        setFeatures(data.detectedFeatures);
        setIsLoadingSession(false);
      } catch (err) {
        if (cancelled) return;
        setLoadError(
          err instanceof ApiError && err.status === 404
            ? "Session not found. It may have expired."
            : "Could not load your listing data. Try going back and uploading again."
        );
        setIsLoadingSession(false);
      }
    };

    poll();
    return () => { cancelled = true; };
  }, [sessionId]);

  const handleGenerate = async () => {
    if (!property) return;
    setGenerateError(null);
    setIsGenerating(true);

    posthog.capture("listing_generation_started", {
      session_id: sessionId,
      feature_count: features.length,
      image_count: session?.images.length ?? 0,
    });

    try {
      await generateListing(sessionId, { property, detectedFeatures: features });
      router.push(`/preview/${sessionId}`);
    } catch (err) {
      posthog.capture("listing_generation_error", {
        session_id: sessionId,
        error_message: err instanceof ApiError ? err.message : "unknown",
      });
      if (err instanceof Error) {
        posthog.captureException(err);
      }
      setGenerateError(
        err instanceof ApiError
          ? err.message
          : "Generation failed. Please try again."
      );
      setIsGenerating(false);
    }
  };

  // ── Loading ──
  if (isLoadingSession) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar backHref="/" backLabel="Start over" />
        <div className="flex flex-1 items-center justify-center">
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        </div>
      </div>
    );
  }

  // ── Error ──
  if (loadError || !session || !property) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar backHref="/" backLabel="Start over" />
        <div className="flex flex-1 items-center justify-center px-6">
          <div className="max-w-sm text-center">
            <p className="mb-2 text-sm font-medium text-foreground">Something went wrong</p>
            <p className="text-xs text-muted-foreground">{loadError}</p>
          </div>
        </div>
      </div>
    );
  }

  // ── Generate CTA button ──
  const GenerateButton = (
    <button
      onClick={handleGenerate}
      disabled={isGenerating}
      style={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        padding: "14px",
        borderRadius: "9px",
        background: isGenerating ? "var(--metes-ink-soft)" : "var(--metes-forest)",
        color: "var(--metes-cream)",
        border: "none",
        fontSize: "13px",
        fontWeight: 500,
        cursor: isGenerating ? "not-allowed" : "pointer",
        opacity: isGenerating ? 0.7 : 1,
        transition: "opacity 0.2s",
        letterSpacing: "0.01em",
      }}
    >
      {isGenerating ? (
        <>
          <Loader2 style={{ width: "14px", height: "14px" }} className="animate-spin" />
          Generating…
        </>
      ) : (
        "Generate My Campaign →"
      )}
    </button>
  );

  // ── Page ──
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar backHref="/" backLabel="Start over" />

      {/* Page header */}
      <div className="border-b border-border py-6">
        <div className="mx-auto max-w-[1280px] px-6 lg:px-12">
          <h1 className="mb-1 text-base font-semibold text-foreground">
            Here&apos;s what we found.
          </h1>
          <p className="text-xs text-muted-foreground">
            Tap any field to correct it. Everything here feeds your campaign — get it right before we write.
          </p>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="mx-auto w-full max-w-[1280px] px-6 lg:px-12">
        <div className="flex flex-1 flex-col md:grid md:grid-cols-[1fr_360px]">

          {/* ── Left: editable data ── */}
          <div className="py-6 pr-0 md:border-r md:border-border md:pr-8">
            <div className="flex flex-col gap-5">
              <PropertyDetailsCard
                property={property}
                mode="edit"
                onChange={setProperty}
              />

              {features.length > 0 && (
                <DetectedFeaturesGrid
                  features={features}
                  onChange={setFeatures}
                />
              )}
            </div>
          </div>

          {/* ── Right: AI intelligence + CTA (desktop only) ── */}
          <div className="hidden flex-col gap-4 py-6 pl-8 md:flex">
            <div>
              <p className="mb-1 text-sm font-semibold text-foreground">
                Ready to generate?
              </p>
              <p className="text-[11px] leading-relaxed text-muted-foreground">
                Every field feeds the copy. Address, price, and key features matter most.
              </p>
            </div>

            {/* AI Intelligence Panel */}
            {session.images.length > 0 && (
              <AiIntelligencePanel
                sessionId={sessionId}
                images={session.images}
              />
            )}

            {/* Generate CTA */}
            {GenerateButton}

            <p className="text-center text-[11px] text-muted-foreground">
              Generates in ~30 seconds
            </p>

            {generateError && (
              <p className="text-center text-[11px] text-destructive">{generateError}</p>
            )}

            <p className="text-center text-[11px] italic text-muted-foreground/60">
              Something&apos;s off? Edit any field above.
            </p>
          </div>
        </div>
      </div>

      {/* Mobile sticky bar */}
      <MobileStickyBar
        variant="generate"
        isLoading={isGenerating}
        onGenerate={handleGenerate}
      />

      {/* Bottom padding for mobile sticky bar */}
      <div className="h-20 md:hidden" />
    </div>
  );
}