"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { PhotoZone } from "./PhotoZone";
import { NotesBar } from "./NotesBar";
import { extractListing, ApiError } from "@/lib/api";
import { cn } from "@/lib/utils";

interface UploadFormProps {
  className?: string;
}

export function UploadForm({ className }: UploadFormProps) {
  const router = useRouter();
  const [photos, setPhotos] = useState<File[]>([]);
  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!notes.trim()) return;
    setError(null);
    setIsLoading(true);

    try {
      const result = await extractListing(photos, notes);
      router.push(`/review/${result.sessionId}`);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(
          err.status === 422
            ? "Please add more detail to your notes — address, price, and beds/baths are helpful."
            : err.status >= 500
            ? "Something went wrong on our end. Try again in a moment."
            : err.message
        );
      } else {
        setError("Could not reach the server. Check your connection and try again.");
      }
      setIsLoading(false);
    }
    // Don't set isLoading(false) on success — stay locked until navigation completes
  };

  return (
    <div
      className={cn(
        "mx-6 mb-12 overflow-hidden rounded-xl border border-dashed border-border",
        isLoading && "opacity-80",
        className
      )}
    >
      <PhotoZone onPhotosChange={setPhotos} />
      <NotesBar
        value={notes}
        onChange={setNotes}
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
      {error && (
        <div className="border-t border-border bg-muted/30 px-5 py-3">
          <p className="text-[11px] text-destructive">{error}</p>
        </div>
      )}
    </div>
  );
}
