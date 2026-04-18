"""
main.py

FastAPI entry point for ListingLogicAI.
Wraps the existing LangChain pipeline services behind a REST API.

All response shapes match the TypeScript types in frontend/types/index.ts.

Session storage is in-memory for beta — moves to Redis post-launch.
Sessions expire after 24 hours.

Endpoints:
    GET  /health
    POST /api/extract
    POST /api/generate/{session_id}
    GET  /api/session/{session_id}
    GET  /api/images/{session_id}/{image_id}
    GET  /api/download/{session_id}/{token}
    POST /api/checkout/{session_id}
    POST /api/webhook/stripe
    POST /api/mock-payment/{session_id}
"""

import asyncio
import hashlib
import hmac
import os
import time
import uuid
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ListingLogicAI API",
    description="AI-powered listing marketing engine for high-performing agents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory session store
# ---------------------------------------------------------------------------

SESSION_TTL = 86400          # 24 hours
DOWNLOAD_TOKEN_TTL = 604800  # 7 days
_sessions: dict[str, dict] = {}


def _create_session() -> dict:
    session_id = str(uuid.uuid4())
    now = time.time()
    session = {
        "session_id": session_id,
        "created_at": now,
        "updated_at": now,
        "api_key": API_KEY,
        "extracted_details": None,
        "image_intelligence": None,
        "original_images": None,
        "enhanced_images": None,
        "analyzed_images": None,
        "generation_status": "extracting",
        "generation_error": None,
        "results": None,
        "paid": "none",           # "none" | "listing" | "both"
        "agent_email": None,
        "download_token": None,
        "download_token_created_at": None,
    }
    _sessions[session_id] = session
    return session


def _get_session(session_id: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired.")
    if time.time() - session["created_at"] > SESSION_TTL:
        del _sessions[session_id]
        raise HTTPException(status_code=404, detail="Session expired.")
    return session


def _generate_download_token(session_id: str) -> str:
    secret = os.getenv("DOWNLOAD_TOKEN_SECRET", "dev-secret-change-in-production")
    payload = f"{session_id}:{time.time()}"
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _validate_download_token(session_id: str, token: str) -> bool:
    session = _sessions.get(session_id)
    if not session:
        return False
    if not session.get("download_token"):
        return False
    if session["download_token"] != token:
        return False
    created_at = session.get("download_token_created_at", 0)
    if time.time() - created_at > DOWNLOAD_TOKEN_TTL:
        return False
    return True


# ---------------------------------------------------------------------------
# Serialization helpers — all output matches frontend/types/index.ts exactly
# ---------------------------------------------------------------------------

def _serialize_property(details) -> Optional[dict]:
    """
    Maps Pydantic PropertyDetails → frontend PropertyDetails type.
    Field name mapping:
      postal_code  → zip
      key_features → keyFeatures
      bedrooms     → beds
      bathrooms    → baths
      list_price   → listPrice
    """
    if not details:
        return None
    return {
        "address": details.address or "",
        "city": details.city or "",
        "state": details.state or "",
        "zip": details.postal_code or "",
        "listPrice": details.list_price or 0,
        "beds": details.bedrooms or 0,
        "baths": details.bathrooms or 0,
        "sqft": getattr(details, "square_footage", 0) or 0,
        "yearBuilt": getattr(details, "year_built", None),
        "lotSize": getattr(details, "lot_size_square_feet", None),
        "garage": str(getattr(details, "garage_spaces", "")) if getattr(details, "garage_spaces", None) else None,
        "propertyType": getattr(details, "property_type", None),
        "communityName": getattr(details, "community_name", None),
        "subdivisionName": getattr(details, "subdivision_name", None),
        "keyFeatures": details.key_features or [],
    }


def _serialize_images(intelligence, session_id: str, rename_result=None) -> list[dict]:
    """
    Maps ImageIntelligence -> frontend ListingImage[] type.
    rename_result: optional RenameResult — populated after generation.
    """
    if not intelligence or not intelligence.ranked_images:
        return []

    base_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")

    # Build lookup: image_id -> renamed_filename
    rename_lookup: dict[str, str] = {}
    is_curated_set: set[str] = set()
    if rename_result:
        for renamed_img in rename_result.all_images:
            rename_lookup[renamed_img.image_id] = renamed_img.renamed_filename
        for renamed_img in rename_result.curated:
            is_curated_set.add(renamed_img.image_id)

    return [
        {
            "id": img.image_id,
            "url": f"{base_url}/api/images/{session_id}/{img.image_id}",
            "rank": idx + 1,
            "roomType": img.room_type or "other",
            "qualityScore": img.quality_score or 0.5,
            "skyVisible": getattr(img, "sky_visible", False) or False,
            "selectedForSocial": img.image_id in (intelligence.highlight_images or []),
            "caption": img.reason or "",
            "filename": img.filename,
            "renamedFilename": rename_lookup.get(img.image_id, img.filename),
            "isCurated": img.image_id in is_curated_set if is_curated_set else idx < 25,
        }
        for idx, img in enumerate(intelligence.ranked_images)
    ]


def _serialize_detected_features(analyzed_images) -> list[dict]:
    """
    Maps List[PropertyImage].feature_candidates → frontend DetectedFeature[].
    Groups by room type for the 4-column grid.
    """
    if not analyzed_images:
        return []

    seen = set()
    features = []

    for img in analyzed_images:
        for feature in img.visible_features:
            key = f"{feature.name}:{img.metadata.room_type}"
            if key in seen:
                continue
            seen.add(key)
            features.append({
                "name": feature.name,
                "confidence": feature.confidence,
                "checked": feature.confidence >= 0.90,
                "category": img.metadata.room_type or "other",
            })

    # Sort by confidence desc
    features.sort(key=lambda f: f["confidence"], reverse=True)
    return features


def _serialize_generated_content(results: dict) -> Optional[dict]:
    """
    Maps pipeline results dict → frontend GeneratedContent type.
    Field name mapping:
      headline     → listingHeadline
      mls_summary  → mlsDescription + mlsCharCount
      social_posts → socialPosts (reshaped)
      email_campaign → emails (array, not object)
      compliance_results → compliance (summary counts)
    """
    if not results:
        return None

    campaign = results.get("email_campaign")
    social_posts = results.get("social_posts", [])
    compliance_list = results.get("compliance_results", [])
    mls = results.get("mls_summary", "")
    headline = results.get("headline", "")

    # Compliance summary counts
    passed = sum(1 for r in compliance_list if r.status == "pass")
    revised = sum(1 for r in compliance_list if r.status == "revised")
    flagged = sum(1 for r in compliance_list if r.status == "flagged")

    # Social posts → frontend shape
    serialized_social = []
    for post in social_posts:
        platform = (post.platform or "facebook").lower().replace(" ", "_")
        if "instagram" in platform:
            slot = post.slot_name or ""
            platform = "instagram_1" if "1" in slot or slot.endswith("1") else "instagram_2"
        else:
            platform = "facebook"

        serialized_social.append({
            "platform": platform,
            "imageId": post.image_id or "",
            "caption": post.social_media_post or "",
            "hashtags": [],
            "cropGuidance": post.crop_guidance or "",
            "recommendedAspectRatio": post.recommended_aspect_ratio or "",
            "roomType": post.room_type or "",
        })

    # Email campaign → array
    emails = []
    if campaign:
        email_map = [
            ("just_listed", campaign.just_listed),
            ("open_house", campaign.open_house),
            ("why_this_home", campaign.why_this_home),
            ("just_sold", campaign.just_sold),
        ]
        for email_type, email in email_map:
            emails.append({
                "type": email_type,
                "subject": email.subject,
                "previewText": email.preview_text,
                "body": email.body,
            })

    return {
        "listingHeadline": headline,
        "mlsDescription": mls,
        "mlsCharCount": len(mls),
        "socialPosts": serialized_social,
        "emails": emails,
        "compliance": {
            "totalAssets": len(compliance_list),
            "passed": passed,
            "revised": revised,
            "flagged": flagged,
        },
    }


def _serialize_session(session: dict) -> dict:
    """
    Full session serialization matching frontend Session type exactly.

    Frontend Session shape:
    {
      sessionId, status, property, images, detectedFeatures,
      generatedContent?, paid, agentEmail?, downloadToken?,
      createdAt, updatedAt
    }
    """
    # Map internal generation_status → frontend SessionStatus
    status_map = {
        "extracting": "extracting",
        "extracted":  "extracted",
        "generating": "generating",
        "complete":   "complete",
        "error":      "error",
        "pending":    "extracting",
    }
    status = status_map.get(session.get("generation_status", "extracting"), "extracting")

    results = session.get("results")
    generated_content = _serialize_generated_content(results) if results else None
    rename_result = results.get("rename_result") if results else None

    return {
        "sessionId": session["session_id"],
        "status": status,
        "property": _serialize_property(session.get("extracted_details")),
        "images": _serialize_images(
            session.get("image_intelligence"),
            session["session_id"],
            rename_result=rename_result,
        ),
        "detectedFeatures": _serialize_detected_features(
            session.get("analyzed_images")
        ),
        "generatedContent": generated_content,
        "paid": session.get("paid", "none"),
        "agentEmail": session.get("agent_email"),
        "downloadToken": session.get("download_token"),
        "createdAt": str(session["created_at"]),
        "updatedAt": str(session.get("updated_at", session["created_at"])),
    }


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# POST /api/extract
# ---------------------------------------------------------------------------

@app.post("/api/extract")
async def extract(
    notes: str = Form(...),
    images: list[UploadFile] = File(default=[]),
):
    """
    Step 1 — Extract property details from agent notes and analyze images.
    Creates a new session. Returns sessionId + extracted data.

    Frontend ExtractResponse shape:
    { sessionId, status, property, images, detectedFeatures }
    """
    from services.listing_pipeline_service import extract_property_data_service
    from services.image_analysis_service import analyze_and_caption_property_images
    from services.fusion_service import merge_image_features_into_property
    from services.image_enhancement_service import enhance_listing_photos
    from services.property_normalization_service import normalize_property_details
    from services.image_intelligence_service import build_image_intelligence

    if not notes.strip():
        raise HTTPException(status_code=422, detail="Agent notes are required.")

    session = _create_session()
    session_id = session["session_id"]

    try:
        details = await extract_property_data_service(notes, API_KEY)

        if images:
            image_data = []
            for upload in images:
                image_bytes = await upload.read()
                image_data.append((image_bytes, upload.filename or "image.jpg"))

            session["original_images"] = image_data

            enhanced = enhance_listing_photos(image_data)
            session["enhanced_images"] = enhanced

            analyzed = await analyze_and_caption_property_images(enhanced, API_KEY)
            session["analyzed_images"] = analyzed

            intelligence = build_image_intelligence(analyzed)
            session["image_intelligence"] = intelligence

            details = merge_image_features_into_property(details, analyzed)

        details = normalize_property_details(details)
        session["extracted_details"] = details
        session["generation_status"] = "extracted"
        session["updated_at"] = time.time()

    except Exception as e:
        del _sessions[session_id]
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    return {
        "sessionId": session_id,
        "status": "extracted",
        "property": _serialize_property(details),
        "images": _serialize_images(
            session.get("image_intelligence"), session_id
        ),
        "detectedFeatures": _serialize_detected_features(
            session.get("analyzed_images")
        ),
    }


# ---------------------------------------------------------------------------
# POST /api/generate/{session_id}
# ---------------------------------------------------------------------------

@app.post("/api/generate/{session_id}")
async def generate(session_id: str, request: Request):
    """
    Step 2 — Generate the full marketing campaign.
    Accepts agent edits (property + detectedFeatures) in request body.
    Fires background task — client polls /api/session/:sessionId.

    Frontend GenerateRequest shape:
    { property?: Partial<PropertyDetails>, detectedFeatures?: DetectedFeature[] }
    """
    session = _get_session(session_id)

    if session["generation_status"] == "generating":
        raise HTTPException(status_code=409, detail="Generation already in progress.")

    body = await request.json()
    email_tone = body.get("emailTone", "Professional")

    # Apply agent edits from HITL review
    edits = body.get("property")
    if edits and session["extracted_details"]:
        details = session["extracted_details"]
        # Map frontend camelCase → backend snake_case
        if edits.get("address") is not None:
            details.address = edits["address"] or None
        if edits.get("city") is not None:
            details.city = edits["city"] or None
        if edits.get("state") is not None:
            details.state = edits["state"] or None
        if edits.get("zip") is not None:
            details.postal_code = edits["zip"] or None
        if edits.get("listPrice") is not None:
            details.list_price = int(edits["listPrice"] or 0)
        if edits.get("beds") is not None:
            details.bedrooms = int(edits["beds"] or 0)
        if edits.get("baths") is not None:
            details.bathrooms = float(edits["baths"] or 0)
        if edits.get("communityName") is not None:
            details.community_name = edits["communityName"] or None
        if edits.get("subdivisionName") is not None:
            details.subdivision_name = edits["subdivisionName"] or None
        if edits.get("keyFeatures") is not None:
            details.key_features = edits["keyFeatures"]
        session["extracted_details"] = details

    # Apply feature selections from HITL detected features grid
    feature_edits = body.get("detectedFeatures")
    if feature_edits:
        selected_names = [f["name"] for f in feature_edits if f.get("checked")]
        if session["extracted_details"]:
            existing = session["extracted_details"].key_features or []
            merged = list(dict.fromkeys(existing + selected_names))
            session["extracted_details"].key_features = merged

    session["generation_status"] = "generating"
    session["updated_at"] = time.time()

    asyncio.create_task(_run_generation(session_id, email_tone))

    return {"sessionId": session_id, "status": "generating"}


async def _run_generation(session_id: str, email_tone: str):
    """Background task — runs the full pipeline and updates session state."""
    from services.listing_pipeline_service import generate_marketing_assets_service
    from services.image_rename_service import build_renamed_image_set

    session = _sessions.get(session_id)
    if not session:
        return

    try:
        results = await generate_marketing_assets_service(
            session["extracted_details"],
            API_KEY,
            email_tone,
            image_intelligence=session.get("image_intelligence"),
            photos_count=len(session.get("original_images") or []),
        )

        if session.get("image_intelligence") and session.get("original_images"):
            rename_result = build_renamed_image_set(
                image_intelligence=session["image_intelligence"],
                original_images=session["original_images"],
            )
            results["rename_result"] = rename_result

        session["results"] = results
        session["generation_status"] = "complete"
        session["updated_at"] = time.time()

    except Exception as e:
        session["generation_status"] = "error"
        session["generation_error"] = str(e)
        session["updated_at"] = time.time()


# ---------------------------------------------------------------------------
# GET /api/session/{session_id}
# ---------------------------------------------------------------------------

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """
    Returns full session state matching frontend Session type.
    Polled every 2 seconds by useGenerationPolling hook.
    """
    session = _get_session(session_id)
    return _serialize_session(session)


# ---------------------------------------------------------------------------
# GET /api/images/{session_id}/{image_id}
# ---------------------------------------------------------------------------

@app.get("/api/images/{session_id}/{image_id}")
async def get_image(session_id: str, image_id: str):
    """
    Serves individual image bytes.
    React <img src={getImageUrl(sessionId, imageId)}> points here.
    image_id can be a ranked image_id or 'hero'.
    """
    session = _get_session(session_id)
    analyzed = session.get("analyzed_images")
    original = session.get("original_images")

    if not analyzed or not original:
        raise HTTPException(status_code=404, detail="No images in this session.")

    original_lookup = {filename: img_bytes for img_bytes, filename in original}
    intelligence = session.get("image_intelligence")

    # Resolve image_id
    if image_id == "hero" and intelligence and intelligence.hero_image_id:
        target = next(
            (img for img in analyzed if img.image_id == intelligence.hero_image_id),
            None
        )
    else:
        target = next(
            (img for img in analyzed if img.image_id == image_id),
            None
        )

    if not target:
        raise HTTPException(status_code=404, detail="Image not found.")

    image_bytes = original_lookup.get(target.filename)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image bytes not found.")

    filename = target.filename.lower()
    if filename.endswith(".png"):
        media_type = "image/png"
    elif filename.endswith(".webp"):
        media_type = "image/webp"
    else:
        media_type = "image/jpeg"

    return Response(content=image_bytes, media_type=media_type)


# ---------------------------------------------------------------------------
# GET /api/download/{session_id}/{token}
# ---------------------------------------------------------------------------

@app.get("/api/download/{session_id}/{token}")
async def download(session_id: str, token: str):
    """
    Serves marketing package ZIP.
    Token: 7-day TTL, multi-use, no auth required.
    """
    from services.package_builder_service import build_marketing_package_zip

    if not _validate_download_token(session_id, token):
        raise HTTPException(status_code=403, detail="Invalid or expired download link.")

    session = _get_session(session_id)

    if not session.get("results"):
        raise HTTPException(status_code=404, detail="No results available.")

    details = session.get("extracted_details")
    address = details.address if details else None
    rename_result = session["results"].get("rename_result")

    zip_bytes = build_marketing_package_zip(
        session["results"],
        address=address,
        email_tone="Professional",
        rename_result=rename_result,
    )

    filename = (
        f"{address.replace(' ', '_')[:40]}_listing_package.zip"
        if address else "listing_package.zip"
    )

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ---------------------------------------------------------------------------
# POST /api/checkout/{session_id}
# ---------------------------------------------------------------------------

@app.post("/api/checkout/{session_id}")
async def create_checkout(session_id: str, request: Request):
    """
    Creates a Stripe Checkout session.

    Frontend CheckoutRequest shape:
    { option, agentEmail, successUrl, cancelUrl }
    """
    session = _get_session(session_id)

    if session["generation_status"] != "complete":
        raise HTTPException(status_code=400, detail="Generation must complete before checkout.")

    body = await request.json()
    purchase_type = body.get("option", "listing")   # frontend sends "option"
    agent_email = body.get("agentEmail", "")
    success_url = body.get("successUrl", f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}")
    cancel_url = body.get("cancelUrl", f"{FRONTEND_URL}/preview/{session_id}")

    # Store email now — available immediately on redirect
    session["agent_email"] = agent_email
    session["updated_at"] = time.time()

    if not STRIPE_SECRET_KEY:
        # Dev mode — simulate checkout without Stripe
        token = _generate_download_token(session_id)
        session["paid"] = purchase_type
        session["download_token"] = token
        session["download_token_created_at"] = time.time()
        return {
            "checkoutUrl": f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}",
        }

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY

        details = session.get("extracted_details")
        address = details.address if details else "Your listing"

        line_items: list[Any] = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"ListingLogicAI — {address}",
                        "description": "MLS description, social posts, email campaign, compliance audit, curated photos.",
                    },
                    "unit_amount": 2499,
                },
                "quantity": 1,
            }
        ]

        if purchase_type == "both":
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Professional Photo Editing",
                        "description": "Color correction, perspective fix, and twilight sky replacement.",
                    },
                    "unit_amount": 4900,
                },
                "quantity": 1,
            })

        checkout_kwargs: dict[str, Any] = {
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": {
                "session_id": session_id,
                "purchase_type": purchase_type,
            },
        }

        if agent_email:
            checkout_kwargs["customer_email"] = agent_email

        checkout_session = stripe.checkout.Session.create(**checkout_kwargs)

        return {"checkoutUrl": checkout_session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checkout creation failed: {str(e)}")


# ---------------------------------------------------------------------------
# POST /api/webhook/stripe
# ---------------------------------------------------------------------------

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Handles Stripe payment confirmation.
    Marks session as paid, generates download token.
    TODO (Item 7.5): Send delivery email via Resend.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if STRIPE_WEBHOOK_SECRET:
        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid webhook signature.")
    else:
        import json
        event = json.loads(payload)

    if event["type"] == "checkout.session.completed":
        stripe_session = event["data"]["object"]
        metadata = stripe_session.get("metadata", {})
        session_id = metadata.get("session_id")
        purchase_type = metadata.get("purchase_type", "listing")
        agent_email = stripe_session.get("customer_details", {}).get("email")

        if session_id and session_id in _sessions:
            s = _sessions[session_id]
            s["paid"] = purchase_type           # "listing" | "both"
            s["agent_email"] = agent_email
            s["updated_at"] = time.time()

            token = _generate_download_token(session_id)
            s["download_token"] = token
            s["download_token_created_at"] = time.time()

            # TODO (Item 7.5): Send delivery email via Resend
            # await send_listing_delivery_email(
            #     to=agent_email,
            #     session=s,
            #     download_token=token,
            # )

    return {"received": True}


# ---------------------------------------------------------------------------
# POST /api/mock-payment/{session_id}  — DEV ONLY
# ---------------------------------------------------------------------------

@app.post("/api/mock-payment/{session_id}")
async def mock_payment(session_id: str, request: Request):
    """
    DEV ONLY — simulates a completed payment without Stripe.

    Frontend MockPaymentResponse shape:
    { sessionId, paid, downloadToken }
    """
    if ENVIRONMENT != "development":
        raise HTTPException(status_code=404, detail="Not found.")

    session = _get_session(session_id)
    body = await request.json()
    purchase_type = body.get("option", "listing")   # frontend sends "option"
    agent_email = body.get("agentEmail", "test@example.com")

    session["paid"] = purchase_type
    session["agent_email"] = agent_email
    session["updated_at"] = time.time()

    token = _generate_download_token(session_id)
    session["download_token"] = token
    session["download_token_created_at"] = time.time()

    return {
        "sessionId": session_id,
        "paid": purchase_type,
        "downloadToken": token,
    }