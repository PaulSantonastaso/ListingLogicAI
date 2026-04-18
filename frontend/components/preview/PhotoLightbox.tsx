"use client";

import { useEffect, useCallback, useState } from "react";
import { X, ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { getImageUrl } from "@/lib/api";
import type { ListingImage } from "@/types";

interface PhotoLightboxProps {
  sessionId: string;
  images: ListingImage[];
  initialIndex?: number;
  onClose: () => void;
}

export function PhotoLightbox({
  sessionId,
  images,
  initialIndex = 0,
  onClose,
}: PhotoLightboxProps) {
  const sorted = [...images].sort((a, b) => a.rank - b.rank);
  const [currentIndex, setCurrentIndex] = useState(initialIndex);
  const current = sorted[currentIndex];

  const prev = useCallback(() => {
    setCurrentIndex((i) => (i > 0 ? i - 1 : sorted.length - 1));
  }, [sorted.length]);

  const next = useCallback(() => {
    setCurrentIndex((i) => (i < sorted.length - 1 ? i + 1 : 0));
  }, [sorted.length]);

  // Keyboard navigation + scroll lock
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowLeft") prev();
      if (e.key === "ArrowRight") next();
    };
    document.addEventListener("keydown", handleKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", handleKey);
      document.body.style.overflow = "";
    };
  }, [onClose, prev, next]);

  const formatRoomType = (roomType: string) =>
    roomType.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div
      className="fixed inset-0 z-50 flex flex-col bg-black/95"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 text-white/80">
        <span className="text-xs font-medium">
          {currentIndex + 1} / {sorted.length} · Your curated photos
        </span>
        <button
          onClick={onClose}
          className="flex h-8 w-8 items-center justify-center rounded-full hover:bg-white/10 transition-colors"
          aria-label="Close"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Main image area */}
      <div className="relative flex flex-1 items-center justify-center overflow-hidden px-12">
        {/* Prev arrow */}
        <button
          onClick={prev}
          className="absolute left-2 flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors lg:left-4"
          aria-label="Previous photo"
        >
          <ChevronLeft className="h-5 w-5" />
        </button>

        {/* Photo */}
        <div className="flex h-full max-h-[60vh] w-full items-center justify-center">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            key={current.id}
            src={getImageUrl(sessionId, current.id)}
            alt={formatRoomType(current.roomType)}
            className="max-h-full max-w-full rounded-lg object-contain"
          />
        </div>

        {/* Next arrow */}
        <button
          onClick={next}
          className="absolute right-2 flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors lg:right-4"
          aria-label="Next photo"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      {/* Caption panel */}
      <div className="shrink-0 px-6 py-4 text-center">
        <div className="mx-auto max-w-xl">
          {/* Rank + room type */}
          <p className="mb-1.5 text-[11px] font-semibold uppercase tracking-widest text-white/50">
            #{current.rank} · {formatRoomType(current.roomType)}
          </p>

          {/* AI caption — select-none to prevent easy copy */}
          {current.caption && (
            <p
              className="mb-2 text-sm leading-relaxed text-white/90 select-none"
              aria-hidden="false"
            >
              {current.caption}
            </p>
          )}

          {/* Renamed filename */}
          <p className="text-[10px] text-white/30 select-none">
            {current.renamedFilename || current.filename}
          </p>
        </div>
      </div>

      {/* Thumbnail strip */}
      <div className="shrink-0 overflow-x-auto px-4 pb-4">
        <div className="flex gap-1.5 justify-center">
          {sorted.map((img, i) => (
            <button
              key={img.id}
              onClick={() => setCurrentIndex(i)}
              className={cn(
                "relative h-14 w-[56px] shrink-0 overflow-hidden rounded border-2 transition-all",
                i === currentIndex
                  ? "border-white"
                  : "border-transparent opacity-50 hover:opacity-80"
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
      </div>
    </div>
  );
}