"use client";

import { useState, use, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { Navbar } from "@/components/layout/Navbar";
import { PropertyDetailsCard } from "@/components/shared/PropertyDetailsCard";
import { MobileStickyBar } from "@/components/shared/MobileStickyBar";
import { ImageIntelligencePanel } from "@/components/review/ImageIntelligencePanel";
import { DetectedFeaturesGrid } from "@/components/review/DetectedFeaturesGrid";
import { generateListing, getSession, ApiError } from "@/lib/api";
import type { PropertyDetails, DetectedFeature, Session } from "@/types";

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
// Content — loads session, manages editable state
// ─────────────────────────────────────────────────────────────────

function ReviewPageContent({ sessionId }: { sessionId: string }) {
  const router = useRouter();

  // Session loading
  const [session, setSession] = useState<Session | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [isLoadingSession, setIsLoadingSession] = useState(true);

  // Editable copies of session data
  const [property, setProperty] = useState<PropertyDetails | null>(null);
  const [features, setFeatures] = useState<DetectedFeature[]>([]);

  // Generate state
  const [isGenerating, setIsGenerating] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);

  // Load session on mount
  useEffect(() => {
    (async () => {
      try {
        const data = await getSession(sessionId);
        setSession(data);
        setProperty(data.property);
        setFeatures(data.detectedFeatures);
      } catch (err) {
        console.log("Session load error:", err);
        setLoadError(
          err instanceof ApiError && err.status === 404
            ? "Session not found. It may have expired."
            : "Could not load your listing data. Try going back and uploading again."
        );
      } finally {
        setIsLoadingSession(false);
      }
    })();
  }, [sessionId]);

  const handleGenerate = async () => {
    if (!property) return;
    setGenerateError(null);
    setIsGenerating(true);

    try {
      await generateListing(sessionId, { property, detectedFeatures: features });
      // Redirect immediately — preview page handles the polling
      router.push(`/preview/${sessionId}`);
    } catch (err) {
      setGenerateError(
        err instanceof ApiError
          ? err.message
          : "Generation failed. Please try again."
      );
      setIsGenerating(false);
    }
  };

  // ── Loading state ──
  if (isLoadingSession) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar currentStep="review" showStepLabels backHref="/" backLabel="Start over" />
        <div className="flex flex-1 items-center justify-center">
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        </div>
      </div>
    );
  }

  // ── Error state ──
  if (loadError || !session || !property) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar currentStep="review" showStepLabels backHref="/" backLabel="Start over" />
        <div className="flex flex-1 items-center justify-center px-6">
          <div className="max-w-sm text-center">
            <p className="mb-2 text-sm font-medium text-foreground">Something went wrong</p>
            <p className="text-xs text-muted-foreground">{loadError}</p>
          </div>
        </div>
      </div>
    );
  }

  // ── Summary for right column ──
  const summaryItems = [
    { label: "Address", value: property.address },
    { label: "Price", value: `$${property.listPrice.toLocaleString()}` },
    { label: "Photos", value: `${session.images.length} uploaded` },
    { label: "Beds / Baths", value: `${property.beds} bd · ${property.baths} ba` },
    {
      label: "Features",
      value: `${features.filter((f) => f.checked).length} detected`,
    },
  ];

  // ── Page ──
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar currentStep="review" showStepLabels backHref="/" backLabel="Start over" />

      {/* Page header */}
      <div className="border-b border-border px-8 py-6">
        <p className="section-label mb-1">Step 2 of 3</p>
        <h1 className="mb-1 text-base font-semibold text-foreground">
          Does this look right?
        </h1>
        <p className="text-xs text-muted-foreground">
          Fix anything below — tap any field to edit inline. When you&apos;re ready, generate your campaign.
        </p>
      </div>

      {/* Two-column layout */}
      <div className="flex flex-1 flex-col md:grid md:grid-cols-[1fr_280px]">

        {/* ── Left: editable data ── */}
        <div className="border-r border-border px-8 py-6">
          <div className="flex flex-col gap-5">
            <PropertyDetailsCard
              property={property}
              mode="edit"
              onChange={setProperty}
            />

            {session.images.length > 0 && (
              <ImageIntelligencePanel
                sessionId={sessionId}
                images={session.images}
              />
            )}

            {features.length > 0 && (
              <DetectedFeaturesGrid
                features={features}
                onChange={setFeatures}
              />
            )}
          </div>
        </div>

        {/* ── Right: summary + CTA (desktop) ── */}
        <div className="hidden flex-col gap-4 p-6 md:flex">
          <div>
            <p className="mb-1 text-xs font-medium text-foreground">Looks right?</p>
            <p className="text-[11px] leading-relaxed text-muted-foreground">
              Fix anything above — tap any field to edit inline. When you&apos;re ready, generate your campaign.
            </p>
          </div>

          {/* Summary */}
          <div className="rounded-lg border border-border p-3.5">
            {summaryItems.map(({ label, value }, i) => (
              <div key={label}>
                {i > 0 && <div className="my-2 h-px bg-muted" />}
                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-muted-foreground">{label}</span>
                  <span className="text-[11px] font-medium text-foreground">{value}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Generate CTA */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-foreground py-3.5 text-xs font-semibold text-background transition-opacity disabled:cursor-not-allowed disabled:opacity-60 hover:opacity-90"
          >
            {isGenerating ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Generating…
              </>
            ) : (
              "Generate My Campaign →"
            )}
          </button>

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
