import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { StepIndicator } from "./StepIndicator";
import { cn } from "@/lib/utils";
import type { Step } from "@/types";

interface NavbarProps {
  /** Which step to highlight. Omit on homepage (no step indicator shown). */
  currentStep?: Step;
  /** Show step labels below pips */
  showStepLabels?: boolean;
  /** Back link — shown on review + preview pages */
  backHref?: string;
  backLabel?: string;
  className?: string;
}

export function Navbar({
  currentStep,
  showStepLabels = false,
  backHref,
  backLabel = "Back",
  className,
}: NavbarProps) {
  return (
    <header
      className={cn(
        "flex h-[52px] items-center justify-between border-b border-border bg-background px-6",
        className
      )}
    >
      {/* Logo */}
      <Link
        href="/"
        className="text-sm font-semibold tracking-tight text-foreground hover:opacity-80 transition-opacity"
      >
        ListingLogicAI
      </Link>

      {/* Center — step indicator (review + preview pages only) */}
      {currentStep ? (
        <StepIndicator
          currentStep={currentStep}
          showLabels={showStepLabels}
        />
      ) : (
        // Homepage — nav links
        <nav className="hidden sm:flex items-center gap-6">
          <a
            href="#how-it-works"
            className="text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            How it works
          </a>
          <a
            href="#pricing"
            className="text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            Pricing
          </a>
        </nav>
      )}

      {/* Right — back link or spacer */}
      <div className="w-[100px] flex justify-end">
        {backHref ? (
          <Link
            href={backHref}
            className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <ChevronLeft className="h-3 w-3" />
            {backLabel}
          </Link>
        ) : (
          // Spacer to keep logo centered on homepage
          <div />
        )}
      </div>
    </header>
  );
}
