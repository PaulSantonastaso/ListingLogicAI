"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { getImageUrl } from "@/lib/api";
import { PhotoLightbox } from "@/components/preview/PhotoLightbox";
import type { ListingImage } from "@/types";

interface PhotoGridProps {
  sessionId: string;
  images: ListingImage[];
  activeImageId?: string;
  onSelect?: (imageId: string) => void;
  className?: string;
}

export function PhotoGrid({
  sessionId,
  images,
  activeImageId,
  onSelect,
  className,
}: PhotoGridProps) {
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxIndex, setLightboxIndex] = useState(0);

  const sorted = [...images].sort((a, b) => a.rank - b.rank);
  const hero = sorted[0];
  const secondary = sorted.slice(1, 5); // ranks 2-5 fill the 2×2

  if (!hero) return null;

  const openLightbox = (index: number) => {
    setLightboxIndex(index);
    setLightboxOpen(true);
  };

  return (
    <div className={cn("mb-3", className)}>
      {/* Main grid — hero left, 2×2 right */}
      <div className="flex gap-1 overflow-hidden rounded-xl" style={{ height: 320 }}>

        {/* Hero — 50% width, full height */}
        <div
          className="relative w-1/2 shrink-0 cursor-pointer overflow-hidden"
          onClick={() => openLightbox(0)}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={getImageUrl(sessionId, hero.id)}
            alt="Hero listing photo"
            className="h-full w-full object-cover transition-transform hover:scale-[1.02]"
          />
          <div className="absolute bottom-2 left-2 rounded bg-background/80 px-2 py-0.5 text-[9px] font-semibold text-foreground backdrop-blur-sm">
            Hero — AI selected
          </div>
        </div>

        {/* Right side — 2×2 grid, 50% width, full height */}
        <div className="grid w-1/2 grid-cols-2 grid-rows-2 gap-1">
          {secondary.map((img, i) => (
            <div
              key={img.id}
              className="relative cursor-pointer overflow-hidden"
              onClick={() => openLightbox(i + 1)}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={getImageUrl(sessionId, img.id)}
                alt={img.roomType}
                className="h-full w-full object-cover transition-transform hover:scale-[1.02]"
              />
            </div>
          ))}

          {/* Fill empty slots */}
          {secondary.length < 4 &&
            Array.from({ length: 4 - secondary.length }).map((_, i) => (
              <div key={`placeholder-${i}`} className="h-full bg-muted" />
            ))}
        </div>
      </div>

      {/* See all photos button — Zillow style, bottom right */}
      <div className="relative">
        <button
          onClick={() => openLightbox(0)}
          className="absolute -top-12 right-2 flex items-center gap-1.5 rounded-md bg-background/90 px-3 py-1.5 text-xs font-semibold text-foreground shadow-sm backdrop-blur-sm transition-colors hover:bg-background border border-border/50"
        >
          <svg className="h-3.5 w-3.5" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="1" y="1" width="6" height="6" rx="1" />
            <rect x="9" y="1" width="6" height="6" rx="1" />
            <rect x="1" y="9" width="6" height="6" rx="1" />
            <rect x="9" y="9" width="6" height="6" rx="1" />
          </svg>
          See all {images.length} curated photos
        </button>
      </div>

      {/* Photo strip — directly below grid */}
      <div className="mt-1.5 flex gap-1.5 overflow-x-auto pb-1 scrollbar-thin">
        {sorted.map((img, i) => (
          <button
            key={img.id}
            type="button"
            onClick={() => {
              onSelect?.(img.id);
              openLightbox(i);
            }}
            className={cn(
              "relative h-16 w-[80px] shrink-0 overflow-hidden rounded-md border-2 transition-all",
              img.id === activeImageId
                ? "border-foreground"
                : "border-transparent hover:border-foreground/30"
            )}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={getImageUrl(sessionId, img.id)}
              alt={img.roomType}
              className="h-full w-full object-cover"
            />
          </button>
        ))}
      </div>

      {/* Lightbox */}
      {lightboxOpen && (
        <PhotoLightbox
          sessionId={sessionId}
          images={sorted}
          initialIndex={lightboxIndex}
          onClose={() => setLightboxOpen(false)}
        />
      )}
    </div>
  );
}