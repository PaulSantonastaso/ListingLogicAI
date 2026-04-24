import { Star } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ListingImage } from "@/types";

// Re-export getImageUrl from api for convenience in components
// (avoids importing from two places)
import { getImageUrl as apiGetImageUrl } from "@/lib/api";

interface ImageIntelligencePanelProps {
  sessionId: string;
  images: ListingImage[];
  className?: string;
}

export function ImageIntelligencePanel({
  sessionId,
  images,
  className,
}: ImageIntelligencePanelProps) {
  const heroImage = images.find((img) => img.rank === 1);
  const socialImages = images.filter((img) => img.selectedForSocial).slice(0, 5);

  return (
    <div className={cn("overflow-hidden rounded-lg border border-border", className)}>
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-border bg-muted/50 px-4 py-3">
        <div className="flex h-4 w-4 items-center justify-center rounded-full bg-foreground">
          <Star className="h-2.5 w-2.5 fill-background text-background" />
        </div>
        <span className="section-label">AI Image Intelligence</span>
      </div>

      <div className="p-4">
        {/* Hero image */}
        {heroImage && (
          <div className="mb-4 flex items-center gap-3 border-b border-muted pb-4">
            <div className="relative shrink-0">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={apiGetImageUrl(sessionId, heroImage.id)}
                alt="Hero listing photo"
                className="h-14 w-[72px] rounded-md object-cover"
              />
              <div className="absolute -right-1.5 -top-1.5 flex h-4 w-4 items-center justify-center rounded-full border-2 border-background bg-foreground">
                <Star className="h-2 w-2 fill-background text-background" />
              </div>
            </div>
            <div>
              <p className="text-xs font-semibold text-foreground">Hero image selected</p>
              <p className="text-[11px] text-muted-foreground">
                {heroImage.roomType} · Quality {Math.round(heroImage.qualityScore * 100)}%
              </p>
            </div>
          </div>
        )}

        {/* Social post thumbnails */}
        {socialImages.length > 0 && (
          <div>
            <p className="mb-2 text-[11px] text-muted-foreground">
              Selected for social posts
            </p>
            <div className="flex gap-2 overflow-x-auto scrollbar-thin pb-1">
              {socialImages.map((img) => (
                <div
                  key={img.id}
                  className="relative shrink-0"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={apiGetImageUrl(sessionId, img.id)}
                    alt={img.roomType}
                    className="h-10 w-[52px] rounded-md border-2 border-foreground object-cover"
                  />
                  <div className="absolute bottom-0.5 left-0 right-0 text-center">
                    <span className="rounded-sm bg-white/80 px-1 text-[8px] font-medium text-foreground">
                      {img.roomType}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
