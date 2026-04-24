"""
main.py

FastAPI entry point for ListingLogicAI.
Wraps the existing LangChain pipeline services behind a REST API.

All response shapes match the TypeScript types in frontend/types/index.ts.

Session storage uses Redis (pickle serialization, 24h TTL).
Sessions are keyed as session:{session_id}.
Autoenhance order→session reverse lookup keyed as autoenhance:{order_id}.

Endpoints:
    GET  /health
    POST /api/extract
    POST /api/generate/{session_id}
    GET  /api/session/{session_id}
    GET  /api/images/{session_id}/{image_id}
    GET  /api/download/{session_id}/{token}
    POST /api/checkout/{session_id}
    POST /api/webhook/stripe
    POST /api/webhook/autoenhance
    POST /api/mock-payment/{session_id}
"""

import asyncio
import hashlib
import hmac
import os
import pickle
import time
import uuid
from typing import Any, Optional

import redis
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
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

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
# Redis session store
# ---------------------------------------------------------------------------

SESSION_TTL = 86400          # 24 hours
DOWNLOAD_TOKEN_TTL = 604800  # 7 days
AUTOENHANCE_KEY_TTL = 604800 # 7 days — matches download token window

_redis_client: redis.Redis = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=False,
)


def _session_key(session_id: str) -> str:
    return f"session:{session_id}"


def _autoenhance_key(order_id: str) -> str:
    return f"autoenhance:{order_id}"


def _read_session(session_id: str) -> Optional[dict]:
    raw: bytes | None = _redis_client.get(_session_key(session_id))  # type: ignore[assignment]
    if not raw:
        return None
    return pickle.loads(raw)


def _write_session(session: dict, ttl: int = SESSION_TTL) -> None:
    _redis_client.setex(
        _session_key(session["session_id"]),
        ttl,
        pickle.dumps(session),
    )


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
        "enhancement_status": "none",
        "photo_download_url": None,
        "autoenhance_order_id": None,
        "autoenhance_image_ids": [],
    }
    _write_session(session)
    return session


def _get_session(session_id: str) -> dict:
    session = _read_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired.")
    return session


def _generate_download_token(session_id: str) -> str:
    secret = os.getenv("DOWNLOAD_TOKEN_SECRET", "dev-secret-change-in-production")
    payload = f"{session_id}:{time.time()}"
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def _validate_download_token(session_id: str, token: str) -> bool:
    session = _read_session(session_id)
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
        "lotSize": getattr(details, "lot_size_sqft", None),
        "garage": getattr(details, "garage_spaces", None),
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
    print(f"[EXTRACT] Request received - {len(images)} images, notes length: {len(notes)}")
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
            print(f"[EXTRACT] Images read - {len(image_data)} files")

            enhanced = enhance_listing_photos(image_data)
            session["enhanced_images"] = enhanced
            print(f"[EXTRACT] Enhancement complete - {len(enhanced)} files")

            try:
                analyzed = await analyze_and_caption_property_images(enhanced, API_KEY)
                session["analyzed_images"] = analyzed
                print(f"[EXTRACT] Analysis complete - {len(analyzed)} images")
            except Exception as e:
                print(f"[EXTRACT] Analysis failed: {e}")
                raise

            intelligence = build_image_intelligence(analyzed)
            session["image_intelligence"] = intelligence
            print(f"[EXTRACT] Intelligence built")

            details = merge_image_features_into_property(details, analyzed)
            print(f"[EXTRACT] Features merged")

        details = normalize_property_details(details)
        session["extracted_details"] = details
        session["generation_status"] = "extracted"
        session["updated_at"] = time.time()
        _write_session(session)

    except Exception as e:
        _redis_client.delete(_session_key(session_id))
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
    _write_session(session)

    asyncio.create_task(_run_generation(session_id, email_tone))

    return {"sessionId": session_id, "status": "generating"}


async def _run_generation(session_id: str, email_tone: str):
    """Background task — runs the full pipeline and updates session state."""
    from services.listing_pipeline_service import generate_marketing_assets_service
    from services.image_rename_service import build_renamed_image_set

    session = _read_session(session_id)
    if not session:
        return

    try:
        results = await generate_marketing_assets_service(
            session["extracted_details"],
            API_KEY,
            email_tone,
            image_intelligence=session.get("image_intelligence"),
            photos_count=len(session.get("original_images") or []),
            google_places_api_key=GOOGLE_PLACES_API_KEY,
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
        _write_session(session)

    except Exception as e:
        session["generation_status"] = "error"
        session["generation_error"] = str(e)
        session["updated_at"] = time.time()
        _write_session(session)


# ---------------------------------------------------------------------------
# GET /api/session/{session_id}
# ---------------------------------------------------------------------------

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """
    Returns full session state matching frontend Session type.
    Polled every 2 seconds by useGenerationPolling hook.
    Falls back to R2 rehydration for paid sessions after Redis expiry.
    """
    session = _read_session(session_id)

    # Fall back to R2 for paid sessions (e.g. 7-day preview link after TTL)
    if not session:
        from services.r2_service import load_session_json
        session = load_session_json(session_id)
        if session:
            # Rehydrate into Redis with full download token TTL
            _write_session(session, ttl=DOWNLOAD_TOKEN_TTL)
        else:
            raise HTTPException(status_code=404, detail="Session not found or expired.")

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
# GET /api/images/enhanced/{session_id}/{filename}
# ---------------------------------------------------------------------------

@app.get("/api/images/enhanced/{session_id}/{filename}")
async def get_enhanced_image(session_id: str, filename: str):
    """
    Serves enhanced images from R2 for the preview grid.
    Only available after Autoenhance processing completes.
    """
    from services.r2_service import get_enhanced_image as r2_get_enhanced_image
    image_bytes = r2_get_enhanced_image(session_id, filename)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Enhanced image not found.")

    import mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    return Response(content=image_bytes, media_type=mime_type or "image/jpeg")


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
    _write_session(session)

    if not STRIPE_SECRET_KEY:
        # Dev mode — simulate checkout without Stripe
        token = _generate_download_token(session_id)
        session["paid"] = purchase_type
        session["download_token"] = token
        session["download_token_created_at"] = time.time()
        _write_session(session)

        # Send delivery email — same as real payment flow
        if agent_email:
            print(f"[EMAIL] Dev checkout — attempting to send to {agent_email}")
            from services.email_service import send_listing_delivery_email
            result = await send_listing_delivery_email(
                to=agent_email,
                session=session,
                download_token=token,
            )
            print(f"[EMAIL] Send result: {result}")

        return {
            "checkoutUrl": f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}",
        }

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY

        details = session.get("extracted_details")
        address = details.address if details else "Your listing"

        line_items: list[Any] = []

        if purchase_type in ("listing", "both"):
            line_items.append({
                "price": os.getenv("STRIPE_LISTING_PRICE_ID"),
                "quantity": 1,
            })

        if purchase_type in ("photos", "both"):
            line_items.append({
                "price": os.getenv("STRIPE_PHOTOS_PRICE_ID"),
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
    Marks session as paid, generates download token, sends delivery email.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    import json
    try:
        if STRIPE_WEBHOOK_SECRET and sig_header:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        else:
            event = json.loads(payload)
    except Exception as e:
        print(f"[WEBHOOK] Signature verification failed: {e}")
        print(f"[WEBHOOK] Falling back to unsigned parsing")
        event = json.loads(payload)

    if event["type"] == "checkout.session.completed":
        stripe_session = event["data"]["object"]
        metadata = stripe_session["metadata"] if "metadata" in stripe_session else {}
        session_id = metadata["session_id"] if "session_id" in metadata else None
        purchase_type = metadata["purchase_type"] if "purchase_type" in metadata else "listing"
        customer_details = stripe_session["customer_details"] if "customer_details" in stripe_session else {}
        agent_email = customer_details["email"] if "email" in customer_details else None

        if session_id:
            s = _read_session(session_id)
            if s:
                s["paid"] = purchase_type
                s["agent_email"] = agent_email
                s["updated_at"] = time.time()

                token = _generate_download_token(session_id)
                s["download_token"] = token
                s["download_token_created_at"] = time.time()
                _write_session(s)

                # Send listing delivery email — fire and forget
                if agent_email:
                    from services.email_service import send_listing_delivery_email
                    asyncio.create_task(
                        send_listing_delivery_email(
                            to=agent_email,
                            session=s,
                            download_token=token,
                        )
                    )

                # Persist session JSON and original images to R2
                from services.r2_service import save_session_json, save_original_images
                asyncio.create_task(asyncio.to_thread(save_session_json, session_id, s))
                original_images = s.get("original_images") or []
                if original_images:
                    asyncio.create_task(
                        asyncio.to_thread(save_original_images, session_id, original_images)
                    )

                # Trigger photo enhancement if photos were purchased
                if purchase_type in ("photos", "both"):
                    from services.photo_enhancement_service import trigger_photo_enhancement
                    asyncio.create_task(
                        trigger_photo_enhancement(session_id=session_id, session=s, redis_client=_redis_client)
                    )

    return {"received": True}


# ---------------------------------------------------------------------------
# POST /api/webhook/autoenhance
# ---------------------------------------------------------------------------

@app.post("/api/webhook/autoenhance")
async def autoenhance_webhook(request: Request):
    """
    Receives per-image processing callbacks from Autoenhance.ai.
    When the full order is complete (order_is_processing=False),
    downloads enhanced images, uploads ZIP to R2, sends delivery email.

    Session lookup uses the autoenhance:{order_id} reverse-lookup key in Redis
    (written by trigger_photo_enhancement), avoiding a full keyspace scan.
    """
    payload = await request.json()

    event = payload.get("event")
    order_id = payload.get("order_id")
    order_is_processing = payload.get("order_is_processing", True)
    has_error = payload.get("error", False)

    print(f"[AUTOENHANCE] Webhook received — order={order_id} processing={order_is_processing} error={has_error}")

    # Only act when the full order is complete
    if order_is_processing:
        return {"received": True}

    # O(1) session lookup via reverse-lookup key
    session_id_bytes: bytes | None = _redis_client.get(_autoenhance_key(order_id))  # type: ignore[assignment]
    if not session_id_bytes:
        print(f"[AUTOENHANCE] No session found for order_id={order_id}")
        return {"received": True}

    session_id = session_id_bytes.decode()
    session = _read_session(session_id)

    if not session:
        print(f"[AUTOENHANCE] Session {session_id} expired or missing for order={order_id}")
        return {"received": True}

    agent_email = session.get("agent_email")
    if not agent_email:
        print(f"[AUTOENHANCE] No agent email on session {session_id} — skipping delivery")
        return {"received": True}

    try:
        from services.photo_enhancement_service import download_enhanced_photos
        from services.r2_service import upload_photos_zip
        from services.email_service import send_photos_delivery_email

        # Download all enhanced images from Autoenhance
        enhanced_images = await download_enhanced_photos(session=session)
        if not enhanced_images:
            print(f"[AUTOENHANCE] No enhanced images returned for order={order_id}")
            return {"received": True}

        # Build ZIP and upload to R2
        photo_download_url = await upload_photos_zip(
            session_id=session_id,
            images=enhanced_images,
        )

        # Send delivery email
        asyncio.create_task(
            send_photos_delivery_email(
                to=agent_email,
                session=session,
                photo_download_url=photo_download_url,
                photo_count=len(enhanced_images),
            )
        )

        session["enhancement_status"] = "complete"
        session["photo_download_url"] = photo_download_url
        session["updated_at"] = time.time()
        _write_session(session)

        # Save enhanced images to R2 for preview grid display
        from services.r2_service import save_enhanced_images, save_session_json
        asyncio.create_task(
            asyncio.to_thread(save_enhanced_images, session_id, enhanced_images)
        )
        # Re-save session JSON with updated enhancement status and photo URL
        asyncio.create_task(asyncio.to_thread(save_session_json, session_id, session))

        print(f"[AUTOENHANCE] Order {order_id} complete — {len(enhanced_images)} photos delivered to {agent_email}")

    except Exception as e:
        print(f"[AUTOENHANCE] Error processing completed order {order_id}: {e}")
        session["enhancement_status"] = "error"
        _write_session(session)

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
    _write_session(session)

    # Send delivery email — same as real payment flow
    if agent_email:
        from services.email_service import send_listing_delivery_email
        result = await send_listing_delivery_email(
            to=agent_email,
            session=session,
            download_token=token,
        )

    return {
        "sessionId": session_id,
        "paid": purchase_type,
        "downloadToken": token,
    }