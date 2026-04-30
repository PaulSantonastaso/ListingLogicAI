"use client";

import { useRef, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ImageIcon, Mic, MicOff, ArrowRight, Loader2, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { usePhotoUpload } from "@/hooks/usePhotoUpload";
import { useVoiceInput } from "@/hooks/useVoiceInput";
import { extractListing, ApiError } from "@/lib/api";
import posthog from "posthog-js";

// ─────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────

const PLACEHOLDER =
  "Add your notes — address, price, beds/baths, recent upgrades, anything you'd tell a buyer...";

const MIN_HEIGHT = 80;
const MAX_HEIGHT = 200;
const STRIP_MAX_VISIBLE = 8;

// Metes palette — scoped to composer only
const C = {
  creamWarm:    "#F4F0E8",
  forest:       "#1F3D2E",
  forestDeep:   "#14271E",
  gold:         "#B89968",
  goldDeep:     "#9A7E50",
  ink:          "#14271E",
  inkSoft:      "#4A6B53",
  border:       "rgba(20,39,30,0.10)",
  borderStrong: "rgba(20,39,30,0.18)",
  muted:        "rgba(20,39,30,0.04)",
  mutedText:    "rgba(20,39,30,0.55)",
};

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

  const { photos, addPhotos, removePhoto } = usePhotoUpload();

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

  // ── Drag and drop ──────────────────────────────────────────────

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

  // ── Submit ─────────────────────────────────────────────────────

  const handleSubmit = async () => {
    if (!notes.trim() || isLoading) return;
    setError(null);
    setIsLoading(true);

    posthog.capture("listing_submitted", {
      photo_count: photos.length,
      notes_length: notes.trim().length,
    });

    try {
      const files = photos.map((p) => p.file);
      const result = await extractListing(files, notes);
      router.push(`/review/${result.sessionId}`);
    } catch (err) {
      if (err instanceof ApiError) {
        posthog.capture("listing_submission_error", {
          error_status: err.status,
          photo_count: photos.length,
        });
        setError(
          err.status === 422
            ? "Please add more detail — address, price, and beds/baths are helpful."
            : err.status >= 500
            ? "Something went wrong on our end. Try again in a moment."
            : err.message
        );
      } else {
        posthog.capture("listing_submission_error", {
          error_status: 0,
          photo_count: photos.length,
        });
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
  const visiblePhotos = photos.slice(0, STRIP_MAX_VISIBLE);
  const extraCount = Math.max(0, photos.length - STRIP_MAX_VISIBLE);

  // ── Render ─────────────────────────────────────────────────────

  return (
    <div className={cn("mb-0", className)}>
      <div
        style={{
          background: C.creamWarm,
          borderRadius: "12px",
          overflow: "hidden",
          boxShadow: "0 24px 48px -12px rgba(0,0,0,0.4), 0 0 0 1px rgba(184,153,104,0.18)",
          opacity: isLoading ? 0.8 : 1,
          transition: "opacity 0.2s",
          border: isDragging ? `1px solid ${C.gold}` : "1px solid transparent",
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* ── Photo strip — only when photos exist ── */}
        {photos.length > 0 && (
          <div style={{
            display: "flex", alignItems: "center", gap: "6px",
            padding: "10px 12px", borderBottom: `1px solid ${C.border}`,
            overflowX: "auto", scrollbarWidth: "none",
          }}>
            {visiblePhotos.map((photo) => (
              <div
                key={photo.id}
                className="group"
                style={{ position: "relative", width: "48px", height: "48px", flexShrink: 0 }}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={photo.previewUrl}
                  alt={photo.file.name}
                  style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: "6px", border: `1px solid ${C.border}` }}
                />
                <button
                  type="button"
                  onClick={() => removePhoto(photo.id)}
                  aria-label={`Remove ${photo.file.name}`}
                  className="opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{
                    position: "absolute", top: "2px", right: "2px",
                    width: "16px", height: "16px", borderRadius: "50%",
                    background: `${C.forestDeep}CC`, color: C.creamWarm,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    border: "none", cursor: "pointer",
                  }}
                >
                  <X style={{ width: "10px", height: "10px" }} />
                </button>
              </div>
            ))}

            {extraCount > 0 && (
              <div style={{
                width: "48px", height: "48px", flexShrink: 0,
                borderRadius: "6px", border: `1px solid ${C.border}`,
                background: C.muted, display: "flex", alignItems: "center",
                justifyContent: "center", fontSize: "11px",
                fontFamily: "var(--font-jetbrains, monospace)", color: C.inkSoft,
              }}>
                +{extraCount}
              </div>
            )}
          </div>
        )}

        {/* ── Textarea ── */}
        <div style={{ padding: "14px 16px 6px" }}>
          <textarea
            ref={textareaRef}
            value={notes + (interimTranscript ? ` ${interimTranscript}` : "")}
            onChange={(e) => setNotes(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={PLACEHOLDER}
            disabled={isLoading}
            rows={1}
            style={{
              minHeight: MIN_HEIGHT,
              width: "100%",
              resize: "none",
              background: "transparent",
              border: "none",
              outline: "none",
              fontFamily: "var(--font-onest, var(--font-inter), sans-serif)",
              fontSize: "13px",
              lineHeight: 1.55,
              color: C.ink,
            }}
          />
        </div>

        {/* ── Footer ── */}
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "10px 12px", borderTop: `1px solid ${C.border}`,
          background: "rgba(20,39,30,0.03)",
        }}>
          {/* Left — add images + mic */}
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              style={{
                display: "inline-flex", alignItems: "center", gap: "6px",
                padding: "7px 11px", background: C.creamWarm,
                border: `1px solid ${C.border}`, borderRadius: "7px",
                fontSize: "11.5px", fontWeight: 500, color: C.inkSoft,
                cursor: isLoading ? "not-allowed" : "pointer",
                opacity: isLoading ? 0.4 : 1,
                fontFamily: "var(--font-onest, var(--font-inter), sans-serif)",
              }}
            >
              <ImageIcon style={{ width: "14px", height: "14px" }} />
              Add images
            </button>

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

            {/* Mic — hidden for now */}
            <button
              type="button"
              onClick={toggleListening}
              style={{ display: "none" }}
              disabled={!isSupported || isLoading}
            >
              {isListening ? <MicOff style={{ width: "14px", height: "14px" }} /> : <Mic style={{ width: "14px", height: "14px" }} />}
            </button>
          </div>

          {/* Right — submit */}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={!canSubmit}
            style={{
              display: "inline-flex", alignItems: "center", gap: "8px",
              padding: "9px 16px", background: canSubmit ? C.forest : C.inkSoft,
              color: C.creamWarm, border: "none", borderRadius: "8px",
              fontSize: "12.5px", fontWeight: 600,
              cursor: canSubmit ? "pointer" : "not-allowed",
              opacity: canSubmit ? 1 : 0.4,
              transition: "opacity 0.2s",
              fontFamily: "var(--font-manrope, var(--font-inter), sans-serif)",
            }}
          >
            {isLoading ? (
              <>
                <Loader2 style={{ width: "14px", height: "14px" }} className="animate-spin" />
                Extracting…
              </>
            ) : (
              <>
                Build My Listing
                <ArrowRight style={{ width: "14px", height: "14px" }} />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error — outside the box */}
      {(error || voiceError) && (
        <p style={{ marginTop: "8px", fontSize: "11px", color: "#C97B5C", paddingLeft: "4px" }}>
          {error ?? voiceError}
        </p>
      )}
    </div>
  );
}