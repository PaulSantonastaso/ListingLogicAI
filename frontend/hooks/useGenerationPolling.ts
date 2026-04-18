"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { getSession } from "@/lib/api";
import type { Session, SessionStatus } from "@/types";

const POLL_INTERVAL_MS = 2000;

/** Statuses that mean polling should stop */
const TERMINAL_STATUSES: SessionStatus[] = ["complete", "error"];

interface UseGenerationPollingOptions {
  /** Session ID to poll */
  sessionId: string;
  /** Initial session data if already available (e.g. passed via server component) */
  initialSession?: Session | null;
  /** Called when status reaches "complete" */
  onComplete?: (session: Session) => void;
  /** Called on terminal error */
  onError?: (error: Error) => void;
}

interface UseGenerationPollingResult {
  session: Session | null;
  isPolling: boolean;
  error: Error | null;
  /** Manually trigger a single refetch (e.g. after user action) */
  refetch: () => Promise<void>;
}

export function useGenerationPolling({
  sessionId,
  initialSession = null,
  onComplete,
  onError,
}: UseGenerationPollingOptions): UseGenerationPollingResult {
  const [session, setSession] = useState<Session | null>(initialSession);
  const [isPolling, setIsPolling] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Use a ref to avoid stale closures in the interval callback
  const sessionRef = useRef(session);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    sessionRef.current = session;
  }, [session]);

  const stopPolling = useCallback(() => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (isMountedRef.current) {
      setIsPolling(false);
    }
  }, []);

  const fetchSession = useCallback(async () => {
    try {
      const data = await getSession(sessionId);
      if (!isMountedRef.current) return;

      setSession(data);
      setError(null);

      if (TERMINAL_STATUSES.includes(data.status)) {
        stopPolling();
        if (data.status === "complete") {
          onComplete?.(data);
        }
      }
    } catch (err) {
      if (!isMountedRef.current) return;
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);
      stopPolling();
      onError?.(error);
    }
  }, [sessionId, stopPolling, onComplete, onError]);

  // Start polling when the component mounts, unless already in a terminal state
  useEffect(() => {
    isMountedRef.current = true;

    const currentStatus = sessionRef.current?.status;
    if (currentStatus && TERMINAL_STATUSES.includes(currentStatus)) {
      // Already done — no polling needed
      return;
    }

    setIsPolling(true);

    // Fetch immediately, then start interval
    fetchSession();
    intervalRef.current = setInterval(fetchSession, POLL_INTERVAL_MS);

    return () => {
      isMountedRef.current = false;
      stopPolling();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId]); // Only restart if sessionId changes

  const refetch = useCallback(async () => {
    await fetchSession();
  }, [fetchSession]);

  return { session, isPolling, error, refetch };
}
