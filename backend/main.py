"""
main.py

FastAPI entry point for ListingLogicAI.
Wraps the existing LangChain pipeline services behind a REST API.

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
"""

import asyncio
import hashlib
import hmac
import os
import time
import uuid
from typing import Optional, Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse

from backend.models import listing_details

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

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
# Structure per session:
# {
#   "session_id": str,
#   "created_at": float,
#   "api_key": str,
#   "extracted_details": PropertyDetails | None,
#   "image_intelligence": ImageIntelligence | None,
#   "original_images": list[(bytes, str)] | None,
#   "enhanced_images": list[(bytes, str)] | None,
#   "analyzed_images": list[PropertyImage] | None,
#   "generation_status": "pending" | "generating" | "complete" | "error",
#   "generation_error": str | None,
#   "results": dict | None,
#   "paid": bool,
#   "purchase_type": "listing" | "both" | None,
#   "download_token": str | None,
#   "download_token_created_at": float | None,
# }

SESSION_TTL = 86400        # 24 hours
DOWNLOAD_TOKEN_TTL = 604800  # 7 days
_sessions: dict[str, dict] = {}


def _create_session() -> dict:
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "created_at": time.time(),
        "api_key": API_KEY,
        "extracted_details": None,
        "image_intelligence": None,
        "original_images": None,
        "enhanced_images": None,
        "analyzed_images": None,
        "generation_status": "pending",
        "generation_error": None,
        "results": None,
        "paid": False,
        "purchase_type": None,
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


def _serialize_session_for_client(session: dict) -> dict:
    """
    Return a client-safe view of the session.
    Strips image bytes and internal fields.
    """
    extracted = session.get("extracted_details")
    intelligence = session.get("image_intelligence")
    results = session.get("results")

    return {
        "sessionId": session["session_id"],
        "generationStatus": session["generation_status"],
        "generationError": session.get("generation_error"),
        "paid": session["paid"],
        "purchaseType": session.get("purchase_type"),
        "extractedDetails": extracted.model_dump() if extracted else None,
        "imageIntelligence": _serialize_image_intelligence(intelligence),
        "imageCount": len(session.get("original_images") or []),
        "results": _serialize_results(results) if results else None,
    }


def _serialize_image_intelligence(intelligence) -> Optional[dict]:
    if not intelligence:
        return None
    return {
        "heroImageId": intelligence.hero_image_id,
        "highlightImages": intelligence.highlight_images,
        "rankedImages": [
            {
                "imageId": img.image_id,
                "filename": img.filename,
                "roomType": img.room_type,
                "score": img.score,
                "reason": img.reason,
                "isHero": img.image_id == intelligence.hero_image_id,
                "visibleFeatures": img.visible_features,
                "marketingWorthy": img.marketing_worthy,
            }
            for img in intelligence.ranked_images
        ],
        "weakImages": [
            {"imageId": img.image_id, "filename": img.filename, "reason": img.reason}
            for img in intelligence.weak_images
        ],
        "highlights": [
            {"feature": h.feature, "supportingImageIds": h.supporting_image_ids}
            for h in intelligence.highlights
        ],
    }


def _serialize_results(results: dict) -> dict:
    if not results:
        return {}

    campaign = results.get("email_campaign")
    social_posts = results.get("social_posts", [])
    compliance = results.get("compliance_results", [])

    listing_details = results.get("listing_details")

    return {
        "headline": results.get("headline"),
        "mlsSummary": results.get("mls_summary"),
        "socialPosts": [
            {
                "platform": p.platform,
                "slotName": p.slot_name,
                "imageId": p.image_id,
                "imageFilename": p.image_filename,
                "recommendedAspectRatio": p.recommended_aspect_ratio,
                "cropGuidance": p.crop_guidance,
                "roomType": p.room_type,
                "visibleFeatures": p.visible_features,
                "caption": p.social_media_post,
            }
            for p in social_posts
        ],
        "emailCampaign": {
            "justListed": {
                "subject": campaign.just_listed.subject,
                "previewText": campaign.just_listed.preview_text,
                "body": campaign.just_listed.body,
            },
            "openHouse": {
                "subject": campaign.open_house.subject,
                "previewText": campaign.open_house.preview_text,
                "body": campaign.open_house.body,
            },
            "whyThisHome": {
                "subject": campaign.why_this_home.subject,
                "previewText": campaign.why_this_home.preview_text,
                "body": campaign.why_this_home.body,
            },
            "justSold": {
                "subject": campaign.just_sold.subject,
                "previewText": campaign.just_sold.preview_text,
                "body": campaign.just_sold.body,
            },
        } if campaign else None,
        "complianceResults": [
            {
                "assetType": r.asset_type,
                "status": r.status,
                "issuesFound": r.issues_found,
                "reviewerNotes": r.reviewer_notes,
                "compliantText": r.compliant_text,
            }
            for r in compliance
        ],
        "listingDetails": listing_details.model_dump() if listing_details else None,    
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
    Creates a new session and returns the sessionId for subsequent calls.
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
        # Extract property details from notes
        details = await extract_property_data_service(notes, API_KEY)

        # Process images if provided
        if images:
            image_data = []
            for upload in images:
                image_bytes = await upload.read()
                image_data.append((image_bytes, upload.filename))

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

    except Exception as e:
        del _sessions[session_id]
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    return {
        "sessionId": session_id,
        "extractedDetails": details.model_dump(),
        "imageIntelligence": _serialize_image_intelligence(session.get("image_intelligence")),
        "imageCount": len(session.get("original_images") or []),
    }


# ---------------------------------------------------------------------------
# POST /api/generate/{session_id}
# ---------------------------------------------------------------------------

@app.post("/api/generate/{session_id}")
async def generate(
    session_id: str,
    request: Request,
):
    """
    Step 2 — Generate the full marketing campaign.
    Accepts optional HITL edits to extracted details in the request body.
    Generation runs async — poll /api/session/{session_id} for status.
    """
    from services.listing_pipeline_service import generate_marketing_assets_service

    session = _get_session(session_id)

    if session["generation_status"] == "generating":
        raise HTTPException(status_code=409, detail="Generation already in progress.")

    body = await request.json()
    email_tone = body.get("emailTone", "Professional")

    # Apply HITL edits if provided
    edits = body.get("edits")
    if edits and session["extracted_details"]:
        details = session["extracted_details"]
        if edits.get("address") is not None:
            details.address = edits["address"] or None
        if edits.get("city") is not None:
            details.city = edits["city"] or None
        if edits.get("state") is not None:
            details.state = edits["state"] or None
        if edits.get("postalCode") is not None:
            details.postal_code = edits["postalCode"] or None
        if edits.get("listPrice") is not None:
            details.list_price = int(edits["listPrice"] or 0)
        if edits.get("bedrooms") is not None:
            details.bedrooms = int(edits["bedrooms"] or 0)
        if edits.get("bathrooms") is not None:
            details.bathrooms = float(edits["bathrooms"] or 0)
        if edits.get("communityName") is not None:
            details.community_name = edits["communityName"] or None
        if edits.get("subdivisionName") is not None:
            details.subdivision_name = edits["subdivisionName"] or None
        if edits.get("keyFeatures") is not None:
            details.key_features = edits["keyFeatures"]
        session["extracted_details"] = details

    session["generation_status"] = "generating"

    # Fire and forget — client polls for status
    asyncio.create_task(_run_generation(session_id, email_tone))

    return {"sessionId": session_id, "status": "generating"}


async def _run_generation(session_id: str, email_tone: str):
    """Background task — runs the pipeline and updates session state."""
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

        # Build rename result if images available
        if session.get("image_intelligence") and session.get("original_images"):
            rename_result = build_renamed_image_set(
                image_intelligence=session["image_intelligence"],
                original_images=session["original_images"],
            )
            results["rename_result"] = rename_result

        session["results"] = results
        session["generation_status"] = "complete"

    except Exception as e:
        session["generation_status"] = "error"
        session["generation_error"] = str(e)


# ---------------------------------------------------------------------------
# GET /api/session/{session_id}
# ---------------------------------------------------------------------------

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """
    Returns current session state.
    Polled every 2 seconds by the frontend during generation.
    """
    session = _get_session(session_id)
    return _serialize_session_for_client(session)


# ---------------------------------------------------------------------------
# GET /api/images/{session_id}/{image_id}
# ---------------------------------------------------------------------------

@app.get("/api/images/{session_id}/{image_id}")
async def get_image(session_id: str, image_id: str):
    """
    Serves individual image bytes for the preview photo grid.
    React <img> tags point here for lazy loading.
    image_id can be a ranked image_id or 'hero'.
    """
    session = _get_session(session_id)
    analyzed = session.get("analyzed_images")
    original = session.get("original_images")

    if not analyzed or not original:
        raise HTTPException(status_code=404, detail="No images found for this session.")

    # Build lookup: image_id -> bytes
    original_lookup = {filename: img_bytes for img_bytes, filename in original}

    # Find the requested image
    target_image = None
    intelligence = session.get("image_intelligence")

    if image_id == "hero" and intelligence and intelligence.hero_image_id:
        target_image = next(
            (img for img in analyzed if img.image_id == intelligence.hero_image_id),
            None
        )
    else:
        target_image = next(
            (img for img in analyzed if img.image_id == image_id),
            None
        )

    if not target_image:
        raise HTTPException(status_code=404, detail="Image not found.")

    image_bytes = original_lookup.get(target_image.filename)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image bytes not found.")

    # Detect content type from filename
    filename = target_image.filename.lower()
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
    Serves the marketing package ZIP.
    Token is validated — 7-day TTL, multi-use.
    """
    from services.package_builder_service import build_marketing_package_zip

    if not _validate_download_token(session_id, token):
        raise HTTPException(status_code=403, detail="Invalid or expired download link.")

    session = _get_session(session_id)

    if not session.get("results"):
        raise HTTPException(status_code=404, detail="No results available for this session.")

    address = None
    if session.get("extracted_details"):
        address = session["extracted_details"].address

    email_tone = "Professional"
    rename_result = session["results"].get("rename_result")

    zip_bytes = build_marketing_package_zip(
        session["results"],
        address=address,
        email_tone=email_tone,
        rename_result=rename_result,
    )

    filename = f"{address.replace(' ', '_')[:40]}_listing_package.zip" if address else "listing_package.zip"

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
    purchase_type: "listing" | "both"
    Returns the Stripe checkout URL for frontend redirect.
    """
    session = _get_session(session_id)

    if session["generation_status"] != "complete":
        raise HTTPException(status_code=400, detail="Generation must complete before checkout.")

    body = await request.json()
    purchase_type = body.get("purchaseType", "listing")

    if not STRIPE_SECRET_KEY:
        # Dev mode — return mock checkout URL
        return {
            "checkoutUrl": f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}&mock=true",
            "sessionId": session_id,
        }

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY

        address = session["extracted_details"].address if session["extracted_details"] else "Your listing"

        line_items: list[Any] = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"ListingLogicAI — {address}",
                        "description": "Full marketing package: MLS description, social posts, email campaign, compliance audit, curated photos.",
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
                        "description": "Color correction, perspective fix, and twilight sky replacement on curated photos.",
                    },
                    "unit_amount": 4900,  # $49.00
                },
                "quantity": 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}",
            cancel_url=f"{FRONTEND_URL}/preview/{session_id}",
            metadata={
                "session_id": session_id,
                "purchase_type": purchase_type,
            },
        )

        return {"checkoutUrl": checkout_session.url, "sessionId": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checkout creation failed: {str(e)}")


# ---------------------------------------------------------------------------
# POST /api/webhook/stripe
# ---------------------------------------------------------------------------

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Handles Stripe payment confirmation.
    On successful payment:
    - Marks session as paid
    - Generates download token
    - Triggers email delivery via Resend (stubbed for now)
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
        # Dev mode — parse payload directly
        import json
        event = json.loads(payload)

    if event["type"] == "checkout.session.completed":
        stripe_session = event["data"]["object"]
        metadata = stripe_session.get("metadata", {})
        session_id = metadata.get("session_id")
        purchase_type = metadata.get("purchase_type", "listing")

        if session_id and session_id in _sessions:
            session = _sessions[session_id]
            session["paid"] = True
            session["purchase_type"] = purchase_type

            # Generate download token
            token = _generate_download_token(session_id)
            session["download_token"] = token
            session["download_token_created_at"] = time.time()

            # TODO (Item 7.5): Send delivery email via Resend
            # await send_listing_delivery_email(
            #     to=stripe_session.get("customer_details", {}).get("email"),
            #     session=session,
            #     download_token=token,
            # )

    return {"received": True}


# ---------------------------------------------------------------------------
# Dev mock endpoint — bypasses Stripe for local testing
# ---------------------------------------------------------------------------

@app.post("/api/mock-payment/{session_id}")
async def mock_payment(session_id: str, request: Request):
    """
    DEV ONLY — simulates a completed payment without Stripe.
    Remove or gate behind env check before production.
    """
    if os.getenv("ENVIRONMENT", "development") != "development":
        raise HTTPException(status_code=404, detail="Not found.")

    session = _get_session(session_id)
    body = await request.json()
    purchase_type = body.get("purchaseType", "listing")

    session["paid"] = True
    session["purchase_type"] = purchase_type
    token = _generate_download_token(session_id)
    session["download_token"] = token
    session["download_token_created_at"] = time.time()

    return {
        "sessionId": session_id,
        "purchaseType": purchase_type,
        "downloadToken": token,
        "redirectUrl": f"{FRONTEND_URL}/preview/{session_id}?paid={purchase_type}",
    }