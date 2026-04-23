"use client";

import { useRef, useEffect } from "react";
import { Mic, MicOff, ArrowRight, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useVoiceInput } from "@/hooks/useVoiceInput";

interface NotesBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading?: boolean;
  className?: string;
}

const PLACEHOLDER =
  "Paste your agent notes — address, price, beds/baths, recent upgrades, anything you'd tell a buyer...";

const MIN_HEIGHT = 100;
const MAX_HEIGHT = 280;

export function NotesBar({
  value,
  onChange,
  onSubmit,
  isLoading = false,
  className,
}: NotesBarProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea to content
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(Math.max(el.scrollHeight, MIN_HEIGHT), MAX_HEIGHT)}px`;
  }, [value]);

  const { isListening, isSupported, interimTranscript, error, toggleListening } =
    useVoiceInput({
      onTranscript: (text) => {
        // Append voice transcript to existing notes with a space
        onChange(value ? `${value} ${text}` : text);
      },
    });

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Cmd/Ctrl + Enter submits
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      onSubmit();
    }
  };

  const canSubmit = value.trim().length > 0 && !isLoading;

  return (
    <div className={cn("flex flex-col", className)}>
      {/* Textarea */}
      <div className="px-5 pb-2 pt-4">
        <textarea
          ref={textareaRef}
          value={value + (interimTranscript ? ` ${interimTranscript}` : "")}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={PLACEHOLDER}
          disabled={isLoading}
          rows={1}
          style={{ minHeight: MIN_HEIGHT }}
          className={cn(
            "w-full resize-none bg-transparent text-xs leading-relaxed text-foreground placeholder:text-muted-foreground/70 focus:outline-none disabled:opacity-50",
          )}
        />
      </div>

      {/* Voice error */}
      {error && (
        <p className="px-5 pb-1 text-[11px] text-destructive">{error}</p>
      )}

      {/* Footer bar */}
      <div className="flex items-center justify-between border-t border-border bg-muted/30 px-5 py-2.5">
        {/* Mic button + label */}
        <div className="flex items-center gap-2">
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
              "flex h-9 w-9 items-center justify-center rounded-full border transition-colors",
              isListening
                ? "border-foreground bg-foreground text-background"
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
          <span className="text-[11px] text-muted-foreground">
            {isListening ? "Listening…" : "Tap to speak your notes"}
          </span>
        </div>

        {/* Generate button */}
        <button
          type="button"
          onClick={onSubmit}
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
  );
}
