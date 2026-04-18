import type {
  Session,
  ExtractResponse,
  GenerateRequest,
  GenerateResponse,
  CheckoutRequest,
  CheckoutResponse,
  MockPaymentResponse,
} from "@/types";

// ─────────────────────────────────────────────────────────────────
// Base config
// ─────────────────────────────────────────────────────────────────

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ─────────────────────────────────────────────────────────────────
// Internal fetch wrapper
// ─────────────────────────────────────────────────────────────────

class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  init?: RequestInit
): Promise<T> {
  const url = `${BASE_URL}${path}`;

  const res = await fetch(url, {
    ...init,
    headers: {
      // Don't set Content-Type for FormData — browser sets it with boundary
      ...(init?.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
      ...init?.headers,
    },
  });

  if (!res.ok) {
    let message = `API error ${res.status}`;
    try {
      const body = await res.json();
      message = body.detail ?? body.message ?? message;
    } catch {
      // response body not JSON — keep generic message
    }
    throw new ApiError(res.status, message);
  }

  return res.json() as Promise<T>;
}

// ─────────────────────────────────────────────────────────────────
// API methods
// ─────────────────────────────────────────────────────────────────

/**
 * POST /api/extract
 * Sends photos + notes. Returns session with extracted property data.
 */
export async function extractListing(
  photos: File[],
  notes: string
): Promise<ExtractResponse> {
  const formData = new FormData();
  formData.append("notes", notes);
  photos.forEach((file) => formData.append("images", file));

  return request<ExtractResponse>("/api/extract", {
    method: "POST",
    body: formData,
  });
}

/**
 * POST /api/generate/:sessionId
 * Kicks off background generation. Returns immediately with status: "generating".
 */
export async function generateListing(
  sessionId: string,
  payload: GenerateRequest
): Promise<GenerateResponse> {
  return request<GenerateResponse>(`/api/generate/${sessionId}`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * GET /api/session/:sessionId
 * Poll this every 2s on the preview page.
 */
export async function getSession(sessionId: string): Promise<Session> {
  return request<Session>(`/api/session/${sessionId}`);
}

/**
 * GET /api/images/:sessionId/:imageId
 * Returns the image URL — used directly in <img> src, not fetched via JS.
 */
export function getImageUrl(sessionId: string, imageId: string): string {
  return `${BASE_URL}/api/images/${sessionId}/${imageId}`;
}

/**
 * GET /api/download/:sessionId/:token
 * Returns the download URL — navigate browser here to trigger download.
 */
export function getDownloadUrl(sessionId: string, token: string): string {
  return `${BASE_URL}/api/download/${sessionId}/${token}`;
}

/**
 * POST /api/checkout/:sessionId
 * Creates a Stripe Checkout session. Redirect browser to checkoutUrl.
 */
export async function createCheckout(
  sessionId: string,
  payload: CheckoutRequest
): Promise<CheckoutResponse> {
  return request<CheckoutResponse>(`/api/checkout/${sessionId}`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * POST /api/mock-payment/:sessionId
 * Dev/staging only — simulates a successful payment without Stripe.
 */
export async function mockPayment(
  sessionId: string,
  option: "listing" | "both"
): Promise<MockPaymentResponse> {
  return request<MockPaymentResponse>(`/api/mock-payment/${sessionId}`, {
    method: "POST",
    body: JSON.stringify({ option }),
  });
}

/**
 * GET /health
 * Lightweight ping to confirm the backend is reachable.
 */
export async function healthCheck(): Promise<{ status: string }> {
  return request<{ status: string }>("/health");
}

// Re-export error class so callers can instanceof check
export { ApiError };
