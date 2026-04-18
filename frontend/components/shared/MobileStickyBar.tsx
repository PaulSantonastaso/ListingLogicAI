"use client";

import { Lock, Download, Loader2 } from "lucide-react";
import { cn, formatPrice } from "@/lib/utils";
import { PRICING, type PurchaseOption } from "@/types";

type MobileStickyBarVariant = "checkout" | "download" | "generate";

interface MobileStickyBarBaseProps {
  className?: string;
}

interface CheckoutVariantProps extends MobileStickyBarBaseProps {
  variant: "checkout";
  selectedOption: PurchaseOption;
  isLoading?: boolean;
  onCheckout: () => void;
}

interface DownloadVariantProps extends MobileStickyBarBaseProps {
  variant: "download";
  onDownload: () => void;
}

interface GenerateVariantProps extends MobileStickyBarBaseProps {
  variant: "generate";
  isLoading?: boolean;
  onGenerate: () => void;
}

type MobileStickyBarProps =
  | CheckoutVariantProps
  | DownloadVariantProps
  | GenerateVariantProps;

export function MobileStickyBar(props: MobileStickyBarProps) {
  return (
    <div
      className={cn(
        // Only visible below lg breakpoint — desktop uses right column cards
        "fixed bottom-0 left-0 right-0 z-40 border-t border-border bg-background px-4 py-3 lg:hidden",
        props.className
      )}
    >
      {props.variant === "checkout" && <CheckoutBar {...props} />}
      {props.variant === "download" && <DownloadBar {...props} />}
      {props.variant === "generate" && <GenerateBar {...props} />}
    </div>
  );
}

// ── Checkout bar ──────────────────────────────────────────────────

function CheckoutBar({
  selectedOption,
  isLoading = false,
  onCheckout,
}: CheckoutVariantProps) {
  const total = selectedOption === "listing" ? PRICING.listing : PRICING.both;

  return (
    <div className="flex items-center justify-between gap-3">
      <div>
        <p className="text-xs text-muted-foreground">
          {selectedOption === "listing" ? "Listing Copy" : "Listing + Photos"}
        </p>
        <p className="text-sm font-semibold text-foreground">
          {formatPrice(total)}
        </p>
      </div>
      <button
        onClick={onCheckout}
        disabled={isLoading}
        className={cn(
          "flex shrink-0 items-center gap-2 rounded-md bg-foreground px-5 py-2.5 text-xs font-semibold text-background transition-opacity",
          isLoading ? "cursor-not-allowed opacity-60" : "hover:opacity-90"
        )}
      >
        {isLoading ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
        ) : (
          <Lock className="h-3 w-3" />
        )}
        Checkout
      </button>
    </div>
  );
}

// ── Download bar ──────────────────────────────────────────────────

function DownloadBar({ onDownload }: DownloadVariantProps) {
  return (
    <div className="flex items-center justify-between gap-3">
      <p className="text-xs text-muted-foreground">
        Your package is ready
      </p>
      <button
        onClick={onDownload}
        className="flex shrink-0 items-center gap-2 rounded-md bg-foreground px-5 py-2.5 text-xs font-semibold text-background hover:opacity-90 transition-opacity"
      >
        <Download className="h-3.5 w-3.5" />
        Download
      </button>
    </div>
  );
}

// ── Generate bar (review page) ────────────────────────────────────

function GenerateBar({ isLoading = false, onGenerate }: GenerateVariantProps) {
  return (
    <button
      onClick={onGenerate}
      disabled={isLoading}
      className={cn(
        "flex w-full items-center justify-center gap-2 rounded-md bg-foreground py-3 text-xs font-semibold text-background transition-opacity",
        isLoading ? "cursor-not-allowed opacity-60" : "hover:opacity-90"
      )}
    >
      {isLoading ? (
        <>
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
          Generating…
        </>
      ) : (
        "Generate My Campaign →"
      )}
    </button>
  );
}
