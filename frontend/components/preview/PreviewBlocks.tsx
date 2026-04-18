import { cn } from "@/lib/utils";
import { getImageUrl } from "@/lib/api";
import { formatListPrice } from "@/lib/utils";
import type { ListingImage, PropertyDetails } from "@/types";
 
// ─────────────────────────────────────────────────────────────────
// PhotoStrip
// ─────────────────────────────────────────────────────────────────
 
interface PhotoStripProps {
  sessionId: string;
  images: ListingImage[];
  activeImageId?: string;
  onSelect?: (imageId: string) => void;
  className?: string;
}
 
export function PhotoStrip({
  sessionId,
  images,
  activeImageId,
  onSelect,
  className,
}: PhotoStripProps) {
  const sorted = [...images].sort((a, b) => a.rank - b.rank);
 
  return (
    <div
      className={cn(
        "mb-5 flex gap-1.5 overflow-x-auto scrollbar-thin pb-1",
        className
      )}
    >
      {sorted.map((img) => (
        <button
          key={img.id}
          type="button"
          onClick={() => onSelect?.(img.id)}
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
  );
}
 
// ─────────────────────────────────────────────────────────────────
// ListingHeader
// ─────────────────────────────────────────────────────────────────
 
interface ListingHeaderProps {
  property: PropertyDetails;
  headline?: string;
  isPurchased: boolean;
  className?: string;
}
 
export function ListingHeader({
  property,
  headline,
  isPurchased,
  className,
}: ListingHeaderProps) {
  return (
    <div className={cn("mb-5", className)}>
      <h2 className="mb-1 text-lg font-semibold text-foreground">
        {property.address}, {property.city} {property.state}
      </h2>
 
      {/* Meta row */}
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-foreground">
          {formatListPrice(property.listPrice)}
        </span>
        <MetaDot />
        <span className="text-xs text-muted-foreground">{property.beds} bd</span>
        <MetaDot />
        <span className="text-xs text-muted-foreground">{property.baths} ba</span>
        <MetaDot />
        <span className="text-xs text-muted-foreground">
          {property.sqft.toLocaleString()} sqft
        </span>
      </div>
 
      {/* Headline */}
      {headline ? (
        <div
          className={cn(
            "rounded-r-lg border-l-[3px] border-foreground bg-muted/40 px-4 py-2.5",
            !isPurchased && "copy-gated"
          )}
        >
          <p className="section-label mb-1">Listing headline</p>
          <p className="text-xs font-medium text-foreground">{headline}</p>
        </div>
      ) : (
        // Skeleton
        <div className="rounded-r-lg border-l-[3px] border-border bg-muted/40 px-4 py-2.5">
          <div className="mb-1.5 h-2.5 w-24 shimmer rounded" />
          <div className="h-3 w-56 shimmer rounded" />
        </div>
      )}
    </div>
  );
}
 
function MetaDot() {
  return <span className="h-1 w-1 rounded-full bg-muted-foreground/50" />;
}
 
// ─────────────────────────────────────────────────────────────────
// ContentSection — reusable wrapper used for all content panels
// ─────────────────────────────────────────────────────────────────
 
interface ContentSectionProps {
  title: string;
  badge?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}
 
export function ContentSection({
  title,
  badge,
  children,
  className,
}: ContentSectionProps) {
  return (
    <div
      className={cn("mb-4 overflow-hidden rounded-lg border border-border", className)}
    >
      <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
        <span className="section-label">{title}</span>
        {badge && <div>{badge}</div>}
      </div>
      <div className="p-4">{children}</div>
    </div>
  );
}
 
// ─────────────────────────────────────────────────────────────────
// SkeletonSection — shimmer placeholder in the shape of a section
// ─────────────────────────────────────────────────────────────────
 
interface SkeletonSectionProps {
  title: string;
  lineCount?: number;
  generatingLabel?: string;
  className?: string;
}
 
export function SkeletonSection({
  title,
  lineCount = 5,
  generatingLabel,
  className,
}: SkeletonSectionProps) {
  return (
    <div
      className={cn("mb-4 overflow-hidden rounded-lg border border-border", className)}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
        <span className="section-label">{title}</span>
        {generatingLabel && (
          <span className="flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-[10px] text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground animate-pulse" />
            {generatingLabel}
          </span>
        )}
      </div>
 
      {/* Shimmer lines */}
      <div className="flex flex-col gap-1.5 p-4">
        {Array.from({ length: lineCount }).map((_, i) => (
          <div
            key={i}
            className="shimmer h-2.5 rounded"
            style={{ width: `${[100, 88, 95, 72, 83, 78, 91][i % 7]}%` }}
          />
        ))}
      </div>
    </div>
  );
}