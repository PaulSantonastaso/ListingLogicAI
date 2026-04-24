"use client";

import { useRef, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ImageIcon, Mic, MicOff, ArrowRight, Loader2, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { usePhotoUpload } from "@/hooks/usePhotoUpload";
import { useVoiceInput } from "@/hooks/useVoiceInput";
import { extractListing, ApiError } from "@/lib/api";

// ─────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────

const PLACEHOLDER =
  "Add your notes — address, price, beds/baths, recent upgrades, anything you'd tell a buyer...";

const MIN_HEIGHT = 100;
const MAX_HEIGHT = 200;
const STRIP_MAX_VISIBLE = 8;

// ─────────────────────────────────────────────────────────────────
// Composer
// ─────────────────────────────────────────────────────────────────

interface ComposerProps {
  className?: string;
}

export function Composer({ className }: ComposerProps) {
  const router = useRouter();
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Photo upload state
  const {
    photos,
    addPhotos,
    removePhoto,
  } = usePhotoUpload();

  // Voice input
  const { isListening, isSupported, interimTranscript, error: voiceError, toggleListening } =
    useVoiceInput({
      onTranscript: (text) => {
        setNotes((prev) => (prev ? `${prev} ${text}` : text));
      },
    });

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(Math.max(el.scrollHeight, MIN_HEIGHT), MAX_HEIGHT)}px`;
  }, [notes]);

  // ── Drag and drop ─────────────────────────────────────────────

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files?.length) {
      addPhotos(e.dataTransfer.files);
    }
  };

  // ── Submit ────────────────────────────────────────────────────

  const handleSubmit = async () => {
    if (!notes.trim() || isLoading) return;
    setError(null);
    setIsLoading(true);

    try {
      const files = photos.map((p) => p.file);
      const result = await extractListing(files, notes);
      router.push(`/review/${result.sessionId}`);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(
          err.status === 422
            ? "Please add more detail — address, price, and beds/baths are helpful."
            : err.status >= 500
            ? "Something went wrong on our end. Try again in a moment."
            : err.message
        );
      } else {
        setError("Could not reach the server. Check your connection and try again.");
      }
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };

  const canSubmit = notes.trim().length > 0 && !isLoading;

  // ── Photo strip helpers ───────────────────────────────────────

  const visiblePhotos = photos.slice(0, STRIP_MAX_VISIBLE);
  const extraCount = Math.max(0, photos.length - STRIP_MAX_VISIBLE);

  // ── Render ────────────────────────────────────────────────────

  return (
    <div className={cn("mx-6 mb-12", className)}>
      <div
        className={cn(
          "overflow-hidden rounded-xl border transition-colors",
          isDragging ? "border-foreground bg-muted/20" : "border-border",
          isLoading && "opacity-80"
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* ── Photo strip — only when photos exist ── */}
        {photos.length > 0 && (
          <div className="flex items-center gap-1.5 overflow-x-auto border-b border-border px-4 py-2.5 scrollbar-thin">
            {visiblePhotos.map((photo) => (
              <div
                key={photo.id}
                className="group relative h-14 w-14 shrink-0 overflow-hidden rounded-md border border-border"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={photo.previewUrl}
                  alt={photo.file.name}
                  className="h-full w-full object-cover"
                />
                <button
                  type="button"
                  onClick={() => removePhoto(photo.id)}
                  className="absolute right-0.5 top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-foreground/80 text-background opacity-0 transition-opacity group-hover:opacity-100"
                  aria-label={`Remove ${photo.file.name}`}
                >
                  <X className="h-2.5 w-2.5" />
                </button>
              </div>
            ))}

            {/* +N more badge */}
            {extraCount > 0 && (
              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-md border border-border bg-muted text-[11px] font-medium text-muted-foreground">
                +{extraCount}
              </div>
            )}
          </div>
        )}

        {/* ── Textarea ── */}
        <div className="px-4 pb-2 pt-3">
          <textarea
            ref={textareaRef}
            value={notes + (interimTranscript ? ` ${interimTranscript}` : "")}
            onChange={(e) => setNotes(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={PLACEHOLDER}
            disabled={isLoading}
            rows={1}
            style={{ minHeight: MIN_HEIGHT }}
            className="w-full resize-none bg-transparent text-xs leading-relaxed text-foreground placeholder:text-muted-foreground/70 focus:outline-none disabled:opacity-50"
          />
        </div>

        {/* ── Footer ── */}
        <div className="flex items-center justify-between border-t border-border bg-muted/30 px-4 py-2.5">
          {/* Left — add images + mic */}
          <div className="flex items-center gap-2">
            {/* Add images button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className={cn(
                "flex items-center gap-1.5 rounded-md border border-border bg-background px-3 py-1.5 text-[11px] font-medium text-muted-foreground transition-colors hover:border-foreground/40 hover:text-foreground",
                isLoading && "cursor-not-allowed opacity-40"
              )}
            >
              <ImageIcon className="h-3.5 w-3.5" />
              Add images
            </button>

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp,image/heic"
              multiple
              className="hidden"
              onChange={(e) => {
                if (e.target.files) addPhotos(e.target.files);
                e.target.value = "";
              }}
            />

            {/* Mic button */}
            <button
              type="button"
              onClick={toggleListening}
              style={{ display: "none" }}
              disabled={!isSupported || isLoading}
              title={
                !isSupported
                  ? "Voice input not supported in this browser"
                  : isListening
                  ? "Stop listening"
                  : "Tap to speak your notes"
              }
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full border transition-colors",
                isListening
                  ? "border-foreground bg-foreground text-background animate-pulse"
                  : "border-border bg-background text-muted-foreground hover:border-foreground/40",
                (!isSupported || isLoading) && "cursor-not-allowed opacity-40"
              )}
            >
              {isListening ? (
                <MicOff className="h-3.5 w-3.5" />
              ) : (
                <Mic className="h-3.5 w-3.5" />
              )}
            </button>
          </div>

          {/* Right — submit */}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={!canSubmit}
            className={cn(
              "flex items-center gap-2 rounded-md bg-foreground px-4 py-2 text-xs font-semibold text-background transition-opacity",
              canSubmit ? "hover:opacity-90" : "cursor-not-allowed opacity-40"
            )}
          >
            {isLoading ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Extracting…
              </>
            ) : (
              <>
                Build My Listing
                <ArrowRight className="h-3.5 w-3.5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error + voice error — outside the border box */}
      {(error || voiceError) && (
        <p className="mt-2 px-1 text-[11px] text-destructive">
          {error ?? voiceError}
        </p>
      )}
    </div>
  );
}