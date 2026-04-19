// ─────────────────────────────────────────────────────────────────
// ListingLogicAI — shared types
// These mirror the FastAPI response shapes. Keep in sync with
// backend/models.py (or equivalent Pydantic schemas) as the API
// evolves.
// ─────────────────────────────────────────────────────────────────

// ── Session status ────────────────────────────────────────────────

export type SessionStatus =
  | "extracting"   // POST /api/extract in progress
  | "extracted"    // extraction complete, waiting for agent review
  | "generating"   // POST /api/generate/:sessionId in progress
  | "complete"     // generation done, all content available
  | "error";       // terminal error

// ── Image data ────────────────────────────────────────────────────

export interface ListingImage {
  id: string;
  /** URL served by GET /api/images/:sessionId/:imageId */
  url: string;
  /** AI-assigned rank (1 = hero) */
  rank: number;
  /** Room type detected by vision model */
  roomType: string;
  /** 0–1 confidence score for the room type */
  qualityScore: number;
  /** Whether this image is eligible for twilight sky replacement */
  skyVisible: boolean;
  /** Whether the AI selected this image for social posts */
  selectedForSocial: boolean;
  /** AI-generated marketing caption from image_caption_chain */
  caption: string;
   /** Original filename */
  filename: string;
  /** Renamed filename from image_rename_service */
  renamedFilename: string;
  /** Whether this image is in the curated set (top 25) */
  isCurated: boolean;
}

// ── Detected features ─────────────────────────────────────────────

export interface DetectedFeature {
  name: string;
  /** 0–1 confidence score */
  confidence: number;
  /** Auto-checked when confidence >= 0.90 */
  checked: boolean;
  /** Room/category grouping for the 4-column grid */
  category: string;
}

// ── Property details ──────────────────────────────────────────────

export interface PropertyDetails {
  address: string;
  city: string;
  state: string;
  zip: string;
  listPrice: number;
  beds: number;
  baths: number;
  sqft: number;
  yearBuilt?: number;
  lotSize?: string;
  garage?: string;
  propertyType?: string;
  mlsNumber?: string;
  /** Agent-editable key features shown as chips */
  keyFeatures: string[];
}

// ── Generated content ─────────────────────────────────────────────

export interface SocialPost {
  platform: "facebook" | "instagram_1" | "instagram_2";
  /** Image ID selected for this post */
  imageId: string;
  caption: string;
  hashtags: string[];
}

export interface EmailVariant {
  type: "just_listed" | "open_house" | "why_this_home" | "just_sold";
  subject: string;
  previewText: string;
  body: string;
}

export interface ComplianceResult {
  totalAssets: number;
  passed: number;
  revised: number;
  flagged: number;
}

export interface GeneratedContent {
  listingHeadline: string;
  mlsDescription: string;
  /** Character count of MLS description */
  mlsCharCount: number;
  socialPosts: SocialPost[];
  emails: EmailVariant[];
  compliance: ComplianceResult;
}

// ── Full session ──────────────────────────────────────────────────

/** Response shape for GET /api/session/:sessionId */
export interface Session {
  sessionId: string;
  status: SessionStatus;
  property: PropertyDetails;
  images: ListingImage[];
  detectedFeatures: DetectedFeature[];
  /** Only present when status === 'complete' */
  generatedContent?: GeneratedContent;
  /** Stripe payment state */
  paid: "none" | "listing" | "both";
  /** Agent email captured at checkout, for post-purchase confirmation */
  agentEmail?: string;
  /** Download token — present after payment */
  downloadToken?: string;
  createdAt: string;
  updatedAt: string;
}

// ── API request / response shapes ────────────────────────────────

export interface ExtractRequest {
  notes: string;
  // photos sent as FormData, not typed here
}

export interface ExtractResponse {
  sessionId: string;
  status: "extracted";
  property: PropertyDetails;
  images: ListingImage[];
  detectedFeatures: DetectedFeature[];
}

export interface GenerateRequest {
  /** Optionally pass updated property details from agent edits */
  property?: Partial<PropertyDetails>;
  /** Optionally pass updated feature selections */
  detectedFeatures?: DetectedFeature[];
}

export interface GenerateResponse {
  sessionId: string;
  status: "generating";
}

export interface CheckoutRequest {
  option: "listing" | "both" | "photos";
  /** Agent email for delivery confirmation */
  agentEmail: string;
  successUrl: string;
  cancelUrl: string;
}

export interface CheckoutResponse {
  /** Stripe Checkout Session URL — redirect the browser here */
  checkoutUrl: string;
}

export interface MockPaymentResponse {
  sessionId: string;
  paid: "listing" | "both";
  downloadToken: string;
}

// ── UI-specific types ─────────────────────────────────────────────

/** Which purchase option the agent has selected in PurchaseCard */
export type PurchaseOption = "listing" | "both" | "photos";

/** Step indicator state */
export type Step = "upload" | "review" | "preview";

export const STEP_ORDER: Step[] = ["upload", "review", "preview"];

export const STEP_LABELS: Record<Step, string> = {
  upload:  "Upload",
  review:  "Review",
  preview: "Preview",
};

/** Pricing constants — single source of truth for the UI */
export const PRICING = {
  listing: 35.00,
  photos:  45.00,
  both:    80.00,
} as const;
