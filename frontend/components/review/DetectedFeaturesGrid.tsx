"use client";

import { cn, formatConfidence } from "@/lib/utils";
import type { DetectedFeature } from "@/types";

interface DetectedFeaturesGridProps {
  features: DetectedFeature[];
  onChange: (updated: DetectedFeature[]) => void;
  className?: string;
}

export function DetectedFeaturesGrid({
  features,
  onChange,
  className,
}: DetectedFeaturesGridProps) {
  // Group features by category for the 4-column layout
  const categories = Array.from(new Set(features.map((f) => f.category)));

  const handleToggle = (featureName: string) => {
    onChange(
      features.map((f) =>
        f.name === featureName ? { ...f, checked: !f.checked } : f
      )
    );
  };

  if (categories.length === 0) return null;

  return (
    <div className={cn("overflow-hidden rounded-lg border border-border", className)}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
        <span className="section-label">Image-Detected Features</span>
        <span className="text-[10px] text-muted-foreground">
          Auto-checked above 90% confidence
        </span>
      </div>

      {/* Grid — up to 4 columns, one per category */}
      <div
        className="grid divide-x divide-muted"
        style={{ gridTemplateColumns: `repeat(${Math.min(categories.length, 4)}, 1fr)` }}
      >
        {categories.slice(0, 4).map((category) => {
          const categoryFeatures = features.filter((f) => f.category === category);

          return (
            <div key={category} className="p-3.5">
              <p className="mb-2.5 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
                {category}
              </p>
              <ul className="flex flex-col gap-1.5">
                {categoryFeatures.map((feature) => (
                  <li key={feature.name} className="flex items-center gap-1.5">
                    {/* Checkbox */}
                    <button
                      type="button"
                      role="checkbox"
                      aria-checked={feature.checked}
                      onClick={() => handleToggle(feature.name)}
                      className={cn(
                        "flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-[3px] border transition-colors",
                        feature.checked
                          ? "border-foreground bg-foreground"
                          : "border-border bg-background"
                      )}
                    >
                      {feature.checked && (
                        <svg width="8" height="6" viewBox="0 0 8 6" fill="none">
                          <path
                            d="M1 3l2 2 4-4"
                            stroke="white"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                      )}
                    </button>

                    {/* Feature name */}
                    <span className="flex-1 truncate text-[11px] text-foreground">
                      {feature.name}
                    </span>

                    {/* Confidence */}
                    <span
                      className={cn(
                        "shrink-0 text-[10px] tabular-nums",
                        feature.confidence >= 0.9
                          ? "text-foreground"
                          : "text-muted-foreground"
                      )}
                    >
                      {formatConfidence(feature.confidence)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}
