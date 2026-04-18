"use client";

import { useState } from "react";
import { ImageIcon, ChevronDown, ChevronUp, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { usePhotoUpload } from "@/hooks/usePhotoUpload";

interface PhotoZoneProps {
  /** Expose the current files to the parent UploadForm */
  onPhotosChange: (files: File[]) => void;
  className?: string;
}

export function PhotoZone({ onPhotosChange, className }: PhotoZoneProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const {
    photos,
    isDragging,
    error,
    addPhotos,
    removePhoto,
    fileInputRef,
    openFilePicker,
    dragHandlers,
  } = usePhotoUpload();

  // Notify parent whenever photos change
  const handleAdd = (files: FileList | File[]) => {
    addPhotos(files);
    // Collect all current files + new ones
    const newFiles = Array.from(files);
    const existing = photos.map((p) => p.file);
    onPhotosChange([...existing, ...newFiles]);
  };

  const handleRemove = (id: string) => {
    removePhoto(id);
    // Rebuild list without the removed item
    const remaining = photos.filter((p) => p.id !== id).map((p) => p.file);
    onPhotosChange(remaining);
  };

  return (
    <div className={cn("border-b border-border", className)}>
      {/* ── Collapsed row ── */}
      <button
        type="button"
        onClick={() => setIsExpanded((v) => !v)}
        className="flex w-full items-center gap-3 bg-muted/30 px-5 py-3.5 text-left transition-colors hover:bg-muted/50"
      >
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-border bg-background">
          <ImageIcon className="h-4 w-4 text-muted-foreground" />
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium text-foreground">
            {photos.length > 0
              ? `${photos.length} photo${photos.length > 1 ? "s" : ""} added`
              : "Add listing photos"}
          </p>
          <p className="text-[11px] text-muted-foreground">
            {photos.length > 0
              ? "Tap to add more or review"
              : "Tap to upload up to 50 photos · more photos = better output"}
          </p>
        </div>

        {isExpanded ? (
          <ChevronUp className="h-4 w-4 shrink-0 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-4 w-4 shrink-0 text-muted-foreground" />
        )}
      </button>

      {/* ── Expanded dropzone ── */}
      {isExpanded && (
        <div className="border-t border-border bg-background px-5 pb-4 pt-4">
          {/* Drop target */}
          <div
            {...dragHandlers}
            onClick={openFilePicker}
            className={cn(
              "flex min-h-[100px] cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed transition-colors",
              isDragging
                ? "border-foreground bg-muted/50"
                : "border-border hover:border-foreground/40 hover:bg-muted/20"
            )}
          >
            <ImageIcon className="mb-2 h-6 w-6 text-muted-foreground" />
            <p className="text-xs font-medium text-foreground">
              {isDragging ? "Drop photos here" : "Click or drag photos here"}
            </p>
            <p className="mt-0.5 text-[11px] text-muted-foreground">
              JPEG, PNG, WebP, HEIC · up to 50 photos
            </p>
          </div>

          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp,image/heic"
            multiple
            className="hidden"
            onChange={(e) => {
              if (e.target.files) handleAdd(e.target.files);
              // Reset input so same files can be re-added if removed
              e.target.value = "";
            }}
          />

          {/* Error message */}
          {error && (
            <p className="mt-2 text-[11px] text-destructive">{error}</p>
          )}

          {/* Thumbnail grid */}
          {photos.length > 0 && (
            <div className="mt-3 grid grid-cols-4 gap-2 sm:grid-cols-6">
              {photos.map((photo) => (
                <div
                  key={photo.id}
                  className="group relative aspect-square overflow-hidden rounded-md border border-border"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={photo.previewUrl}
                    alt={photo.file.name}
                    className="h-full w-full object-cover"
                  />
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRemove(photo.id);
                    }}
                    className="absolute right-0.5 top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-foreground/80 text-background opacity-0 transition-opacity group-hover:opacity-100"
                    aria-label={`Remove ${photo.file.name}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
