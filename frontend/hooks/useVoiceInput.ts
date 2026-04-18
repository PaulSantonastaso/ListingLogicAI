"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface UseVoiceInputOptions {
  /** Called with the final transcript when speech ends */
  onTranscript: (text: string) => void;
  /** Language for recognition — defaults to browser language */
  lang?: string;
}

interface UseVoiceInputResult {
  isListening: boolean;
  isSupported: boolean;
  interimTranscript: string;
  error: string | null;
  startListening: () => void;
  stopListening: () => void;
  toggleListening: () => void;
}

// Web Speech API type declarations (not in all TS libs)
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}

export function useVoiceInput({
  onTranscript,
  lang,
}: UseVoiceInputOptions): UseVoiceInputResult {
  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  const isSupported =
    typeof window !== "undefined" &&
    ("SpeechRecognition" in window || "webkitSpeechRecognition" in window);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    recognitionRef.current = null;
    setIsListening(false);
    setInterimTranscript("");
  }, []);

  const startListening = useCallback(() => {
    if (!isSupported) {
      setError("Voice input is not supported in this browser.");
      return;
    }
    if (isListening) return;

    setError(null);

    const SpeechRecognitionAPI =
      window.SpeechRecognition ?? window.webkitSpeechRecognition;

    const recognition = new SpeechRecognitionAPI();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = lang ?? navigator.language ?? "en-US";

    recognition.onstart = () => setIsListening(true);

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let interim = "";
      let final = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          final += transcript;
        } else {
          interim += transcript;
        }
      }

      setInterimTranscript(interim);

      if (final) {
        onTranscript(final.trim());
        setInterimTranscript("");
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      const msg =
        event.error === "not-allowed"
          ? "Microphone access denied. Check your browser permissions."
          : event.error === "no-speech"
          ? "No speech detected. Try again."
          : `Voice input error: ${event.error}`;
      setError(msg);
      stopListening();
    };

    recognition.onend = () => {
      setIsListening(false);
      setInterimTranscript("");
    };

    recognitionRef.current = recognition;
    recognition.start();
  }, [isSupported, isListening, lang, onTranscript, stopListening]);

  const toggleListening = useCallback(() => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  }, [isListening, startListening, stopListening]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      recognitionRef.current?.stop();
    };
  }, []);

  return {
    isListening,
    isSupported,
    interimTranscript,
    error,
    startListening,
    stopListening,
    toggleListening,
  };
}
