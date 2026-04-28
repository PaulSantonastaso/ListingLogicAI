"use client";

import { use, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/layout/Navbar";
import { PropertyDetailsCard } from "@/components/shared/PropertyDetailsCard";
import { PurchaseCard } from "@/components/shared/PurchaseCard";
import { MobileStickyBar } from "@/components/shared/MobileStickyBar";
import { PhotoGrid } from "@/components/preview/PhotoGrid";
import {
  ListingHeader,
  SkeletonSection,
} from "@/components/preview/PreviewBlocks";
import {
  MlsDescription,
  SocialLaunchPack,
  EmailCampaign,
  CompliancePanel,
  SuccessBanner,
} from "@/components/preview/ContentComponents";
import { useGenerationPolling } from "@/hooks/useGenerationPolling";
import { createCheckout, getDownloadUrl, ApiError } from "@/lib/api";
import type { PurchaseOption, Session } from "@/types";
import { Download } from "lucide-react";

// ─────────────────────────────────────────────────────────────────
// Page entry — unwrap async params
// ─────────────────────────────────────────────────────────────────

export default function PreviewPage({
  params,
  searchParams,
}: {
  params: Promise<{ sessionId: string }>;
  searchParams: Promise<{ paid?: string }>;
}) {
  const { sessionId } = use(params);
  const { paid } = use(searchParams);
  return <PreviewPageContent sessionId={sessionId} paidParam={paid} />;
}

// ─────────────────────────────────────────────────────────────────
// Content
// ─────────────────────────────────────────────────────────────────

function PreviewPageContent({
  sessionId,
  paidParam,
}: {
  sessionId: string;
  paidParam?: string;
}) {
  const router = useRouter();
  const [activeImageId, setActiveImageId] = useState<string | undefined>();
  const [checkoutError, setCheckoutError] = useState<string | null>(null);
  const [selectedOption, setSelectedOption] = useState<PurchaseOption>("listing");

  const { session, error: pollError } = useGenerationPolling({
    sessionId,
    onComplete: (s) => {
      const hero = s.images.find((img) => img.rank === 1);
      if (hero) setActiveImageId(hero.id);
    },
  });

  const isGenerating = !session || session.status === "generating";
  const isComplete = session?.status === "complete";
  const content = session?.generatedContent;

  const paidStatus: "none" | "listing" | "both" =
    paidParam === "listing" || paidParam === "both"
      ? paidParam
      : session?.paid ?? "none";

  const isPurchased = paidStatus !== "none";

  // ── Handlers ──────────────────────────────────────────────────

  const handleCheckout = useCallback(
    async (option: PurchaseOption, agentEmail: string) => {
      setCheckoutError(null);
      try {
        const origin = window.location.origin;
        const { checkoutUrl } = await createCheckout(sessionId, {
          option,
          agentEmail,
          successUrl: `${origin}/preview/${sessionId}?paid=${option}`,
          cancelUrl: `${origin}/preview/${sessionId}`,
        });
        window.location.href = checkoutUrl;
      } catch (err) {
        setCheckoutError(
          err instanceof ApiError ? err.message : "Checkout failed. Please try again."
        );
        throw err;
      }
    },
    [sessionId]
  );

  const handleDownload = useCallback(() => {
    if (!session?.downloadToken) return;
    window.open(getDownloadUrl(sessionId, session.downloadToken), "_blank");
  }, [session, sessionId]);

  const handlePhotoUpsell = useCallback(async () => {
    try {
      const origin = window.location.origin;
      const { checkoutUrl } = await createCheckout(sessionId, {
        option: "photos",
        agentEmail: session?.agentEmail ?? "",
        successUrl: `${origin}/preview/${sessionId}?paid=both`,
        cancelUrl: `${origin}/preview/${sessionId}?paid=listing`,
      });
      window.location.href = checkoutUrl;
    } catch (err) {
      console.error("Photo upsell checkout failed:", err);
    }
  }, [sessionId, session]);

  const property = session?.property;

  // ── Render ────────────────────────────────────────────────────

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar
        backHref={`/review/${sessionId}`}
        backLabel="Back to review"
      />

      {/* Success banner — post-purchase */}
      {isPurchased && session?.agentEmail && (
        <SuccessBanner
          agentEmail={session.agentEmail}
          onDownload={handleDownload}
        />
      )}

      {/* ── Photo section ── */}
      <div className="mx-auto w-full max-w-[1280px] px-6 pt-6 lg:px-12">
        {property && session.images.length > 0 ? (
          <PhotoGrid
            sessionId={sessionId}
            images={session.images}
            activeImageId={activeImageId}
            onSelect={setActiveImageId}
          />
        ) : (
          <div className="mb-3">
            <div className="flex gap-1 overflow-hidden rounded-xl" style={{ height: 320 }}>
              <div className="shimmer w-1/2 shrink-0" />
              <div className="grid w-1/2 grid-cols-2 grid-rows-2 gap-1">
                <div className="shimmer" />
                <div className="shimmer" />
                <div className="shimmer" />
                <div className="shimmer" />
              </div>
            </div>
            <div className="mt-1.5 flex gap-1.5">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="shimmer h-16 w-[80px] shrink-0 rounded-md" />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ── Two-column layout ── */}
      <div className="mx-auto w-full max-w-[1280px] px-6 lg:px-12">
        <div className="flex flex-1 flex-col lg:grid lg:grid-cols-[1fr_360px]">

          {/* ── Left: listing content ── */}
          <div className="py-6 pr-0 lg:pr-8">

            {property ? (
              <ListingHeader
                property={property}
                headline={content?.listingHeadline}
                isPurchased={isPurchased}
              />
            ) : (
              <div className="mb-5 flex flex-col gap-1.5">
                <div className="shimmer h-5 w-3/4 rounded" />
                <div className="shimmer h-3 w-1/2 rounded" />
              </div>
            )}

            {isComplete && content ? (
              <>
                <MlsDescription content={content} isPurchased={isPurchased} />
                <PropertyDetailsCard
                  property={property!}
                  mode="readonly"
                  className="mb-4"
                />
                <SocialLaunchPack
                  content={content}
                  sessionId={sessionId}
                  images={session.images}
                  isPurchased={isPurchased}
                />
                <EmailCampaign content={content} isPurchased={isPurchased} />
                <CompliancePanel content={content} isPurchased={isPurchased} />
              </>
            ) : (
              <>
                <SkeletonSection title="MLS Description" lineCount={5} generatingLabel="Writing…" />
                {property ? (
                  <PropertyDetailsCard
                    property={property}
                    mode="readonly"
                    className="mb-4"
                  />
                ) : (
                  <SkeletonSection title="Property Details" lineCount={4} />
                )}
                <SkeletonSection title="Social Launch Pack" lineCount={3} generatingLabel="Creating…" />
                <SkeletonSection title="Email Campaign" lineCount={4} generatingLabel="Drafting…" />
                <SkeletonSection title="Fair Housing Compliance" lineCount={2} generatingLabel="Reviewing…" />
              </>
            )}

            {pollError && (
              <p className="mt-2 text-center text-xs text-destructive">
                Generation error: {pollError.message}. Try refreshing.
              </p>
            )}
          </div>

          {/* ── Right: purchase card (desktop, sticky) ── */}
          <div className="hidden lg:flex flex-col gap-4 py-6 pl-8">
            <div style={{ position: "sticky", top: "76px" }}>
              {isPurchased ? (
                <PostPurchasePanel
                  session={session}
                  paidStatus={paidStatus as "listing" | "both"}
                  onDownload={handleDownload}
                  onNewListing={() => router.push("/")}
                  onPhotoUpsell={handlePhotoUpsell}
                />
              ) : (
                <>
                  <PurchaseCard
                    sessionId={sessionId}
                    isGenerating={isGenerating}
                    onCheckout={handleCheckout}
                  />
                  {checkoutError && (
                    <p className="mt-2 text-center text-[11px] text-destructive">{checkoutError}</p>
                  )}
                </>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* ── Mobile sticky bar ── */}
      {isPurchased ? (
        <MobileStickyBar variant="download" onDownload={handleDownload} />
      ) : (
        <MobileStickyBar
          variant="checkout"
          selectedOption={selectedOption}
          onCheckout={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        />
      )}

      <div className="h-20 lg:hidden" />
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// PostPurchasePanel
// ─────────────────────────────────────────────────────────────────

function PostPurchasePanel({
  session,
  paidStatus,
  onDownload,
  onNewListing,
  onPhotoUpsell,
}: {
  session: Session | null;
  paidStatus: "listing" | "both";
  onDownload: () => void;
  onNewListing: () => void;
  onPhotoUpsell: () => void;
}) {
  return (
    <div className="flex flex-col gap-3">
      {/* Download card */}
      <div className="rounded-lg border border-border p-4">
        <p className="mb-1 text-xs font-semibold text-foreground">
          Your campaign is ready
        </p>
        <p className="mb-4 text-[11px] leading-relaxed text-muted-foreground">
          Sent to{" "}
          <span className="font-medium text-foreground">
            {session?.agentEmail ?? "your email"}
          </span>
          . Download link valid for 7 days.
        </p>
        <button
          onClick={onDownload}
          style={{ background: "var(--metes-forest)", color: "var(--metes-cream)" }}
          className="flex w-full items-center justify-center gap-2 rounded-md py-2.5 text-xs font-semibold transition-opacity hover:opacity-90"
        >
          <Download className="h-3.5 w-3.5" />
          Download Package
        </button>
        <div className="mt-3 rounded-md border border-border bg-muted/30 p-2.5">
          <p className="text-[10px] text-muted-foreground">Delivered to</p>
          <p className="text-xs font-medium text-foreground">
            {session?.agentEmail ?? "—"}
          </p>
        </div>
      </div>

      {/* Photo upsell */}
      {paidStatus === "listing" && (
        <div
          className="rounded-lg p-4"
          style={{ border: `1px dashed var(--metes-gold)` }}
        >
          <p
            className="mb-1 text-[10px] font-semibold uppercase tracking-widest"
            style={{ color: "var(--metes-gold-deep)" }}
          >
            Add-on available
          </p>
          <p className="mb-1 text-xs font-semibold text-foreground">
            Professionally edited photos
          </p>
          <p className="mb-3 text-[11px] leading-relaxed text-muted-foreground">
            Sky replacement, color correction, and perspective fix on all photos. Delivered to your email.
          </p>
          <button
            onClick={onPhotoUpsell}
            style={{ borderColor: "var(--metes-forest)", color: "var(--metes-forest)" }}
            className="flex w-full items-center justify-center gap-2 rounded-md border py-2 text-xs font-semibold transition-colors hover:bg-muted"
          >
            Add Photo Editing — $45
          </button>
        </div>
      )}

      {/* New listing */}
      <div className="pt-1 text-center">
        <p className="mb-2 text-[11px] text-muted-foreground">Have another listing?</p>
        <button
          onClick={onNewListing}
          style={{ borderColor: "var(--metes-border)" }}
          className="rounded-md border px-5 py-2 text-xs font-semibold text-foreground transition-colors hover:bg-muted"
        >
          Start a new listing
        </button>
      </div>
    </div>
  );
}