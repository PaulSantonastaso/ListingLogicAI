"""
photo_enhancement_service.py

Handles Autoenhance.ai API integration for real estate photo editing.

Flow:
  1. trigger_photo_enhancement() — called from Stripe webhook
     Uploads images to Autoenhance, stores image_ids on session
  2. download_enhanced_photos() — called from Autoenhance webhook
     Downloads all enhanced images using stored image_ids

Enhancement settings per image:
  - Exterior (front/back): sky replacement + vertical correction
  - Interior: window pull + vertical correction

Environment variables required:
  AUTOENHANCE_API_KEY — from Autoenhance dashboard
"""

import logging
import os
from typing import TYPE_CHECKING

import httpx
import pickle

if TYPE_CHECKING:
    import redis as redis_module

logger = logging.getLogger(__name__)

AUTOENHANCE_BASE_URL = "https://api.autoenhance.ai/v3"
AUTOENHANCE_API_KEY = os.getenv("AUTOENHANCE_API_KEY", "")

AUTOENHANCE_KEY_TTL = 604800  # 7 days


def _headers() -> dict:
    return {
        "x-api-key": AUTOENHANCE_API_KEY,
        "Content-Type": "application/json",
        "x-api-version": "2025-05-05",
    }


def _enhancement_settings(room_type: str) -> dict:
    """
    Returns per-image enhancement settings based on room type.
    sky_visible is not available on ImageMetadata — routing based on room_type only.
    Autoenhance handles color correction, exposure, and white balance automatically.
    """
    is_exterior = room_type.upper() in (
        "FRONT_EXTERIOR", "BACK_EXTERIOR", "EXTERIOR"
    )

    if is_exterior:
        return {
            "sky_replacement": True,
            "vertical_correction": True,
            "window_pull_type": "NONE",
        }
    else:
        return {
            "sky_replacement": False,
            "vertical_correction": True,
            "window_pull_type": "ONLY_WINDOWS",
        }


async def trigger_photo_enhancement(
    session_id: str,
    session: dict,
    redis_client: "redis_module.Redis | None" = None,
    session_ttl: int = 86400,
) -> None:
    """
    Uploads all session images to Autoenhance.
    Stores list of image_ids on session for webhook download lookup.
    Called as fire-and-forget from Stripe webhook.

    redis_client: passed from main.py so the service stays Redis-unaware
    at import time. When provided, writes the autoenhance:{order_id} →
    session_id reverse-lookup key immediately after the order is created,
    enabling O(1) session lookup in the Autoenhance webhook handler.
    """
    if not AUTOENHANCE_API_KEY:
        logger.warning("[AUTOENHANCE] No API key set — skipping photo enhancement")
        return

    enhanced_images = session.get("original_images") or []
    analyzed_images = session.get("analyzed_images") or []

    # Fall back to R2 if images not in memory (upsell after session expiry)
    if not enhanced_images:
        from services.r2_service import load_original_images
        enhanced_images = load_original_images(session_id)

    if not enhanced_images:
        logger.warning(f"[AUTOENHANCE] No images found on session {session_id}")
        return

    # Build renamed filename lookup from rename_result (in-memory, pre-serialization)
    results = session.get("results") or {}
    rename_result = results.get("rename_result")
    rename_lookup: dict[str, str] = {}
    if rename_result and hasattr(rename_result, "all_images"):
        for img in rename_result.all_images:
            rename_lookup[img.image_id] = img.renamed_filename

    uploaded_image_ids: list[str] = []

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:

            # Step 1 — Create order to group all images
            order_resp = await client.post(
                f"{AUTOENHANCE_BASE_URL}/orders",
                headers=_headers(),
                json={"name": session_id},
            )
            order_resp.raise_for_status()
            order_id = order_resp.json()["order_id"]
            session["autoenhance_order_id"] = order_id
            logger.info(f"[AUTOENHANCE] Created order {order_id} for session {session_id}")

            # Write reverse-lookup key immediately — webhook needs this to find the session
            if redis_client and order_id:
                redis_client.setex(
                    f"autoenhance:{order_id}",
                    AUTOENHANCE_KEY_TTL,
                    session_id.encode(),
                )
                logger.info(f"[AUTOENHANCE] Reverse-lookup key written for order {order_id}")

            for i, (image_bytes, filename) in enumerate(enhanced_images):
                our_image_id = f"img_{i+1:03}"

                # Get room type from analyzed images
                analyzed = analyzed_images[i] if i < len(analyzed_images) else None
                room_type = analyzed.metadata.room_type if analyzed else "other"

                settings = _enhancement_settings(room_type)

                # Use renamed filename for SEO value
                renamed = rename_lookup.get(our_image_id, filename)

                # Step 2 — Register image with Autoenhance under the order
                create_resp = await client.post(
                    f"{AUTOENHANCE_BASE_URL}/images/",
                    headers=_headers(),
                    json={
                        "image_name": renamed,
                        "order_id": order_id,
                        **settings,
                    },
                )
                create_resp.raise_for_status()
                image_data = create_resp.json()

                ae_image_id = image_data["image_id"]
                # Support both old and new API versions
                upload_url = image_data.get("upload_url") or image_data.get("s3PutObjectUrl")

                if not upload_url:
                    logger.warning(f"[AUTOENHANCE] No upload URL for image {renamed}")
                    continue

                # Step 3 — Upload image bytes
                # Content-Type must match what Autoenhance signed the URL with
                import mimetypes
                mime_type, _ = mimetypes.guess_type(renamed)
                content_type = mime_type or "image/jpeg"
                upload_resp = await client.put(
                    upload_url,
                    content=image_bytes,
                    headers={"Content-Type": content_type},
                )
                upload_resp.raise_for_status()

                uploaded_image_ids.append(ae_image_id)
                session["autoenhance_image_ids"] = uploaded_image_ids[:]
                ae_rename_map = session.get("autoenhance_rename_map") or {}
                ae_rename_map[ae_image_id] = renamed
                session["autoenhance_rename_map"] = ae_rename_map
                if redis_client:
                    redis_client.setex(
                        f"session:{session_id}",
                        session_ttl,
                        pickle.dumps(session),
                    )
                logger.info(f"[AUTOENHANCE] Uploaded {renamed} as {ae_image_id}")

        # Final status update
        session["autoenhance_image_ids"] = uploaded_image_ids
        session["enhancement_status"] = "processing"
        logger.info(
            f"[AUTOENHANCE] {len(uploaded_image_ids)} images uploaded for session {session_id}"
        )

    except Exception as e:
        logger.error(
            f"[AUTOENHANCE] trigger_photo_enhancement failed for session {session_id}: {e}"
        )
        session["enhancement_status"] = "error"


async def download_enhanced_photos(session: dict) -> list[tuple[bytes, str]]:
    """
    Downloads all enhanced images using image_ids stored on the session.
    Returns a list of (image_bytes, image_name) tuples.
    Called from the Autoenhance webhook when order_is_processing=False.
    """
    image_ids: list[str] = session.get("autoenhance_image_ids") or []
    logger.info(f"[AUTOENHANCE] Session keys: {list(session.keys())}")
    logger.info(f"[AUTOENHANCE] image_ids on session: {image_ids}")
    logger.info(f"[AUTOENHANCE] enhancement_status: {session.get('enhancement_status')}")
    if not image_ids:
        logger.warning("[AUTOENHANCE] No image IDs on session — cannot download")
        return []

    results: list[tuple[bytes, str]] = []

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            for image_id in image_ids:
                ae_resp = await client.get(
                    f"{AUTOENHANCE_BASE_URL}/images/{image_id}/enhanced",
                    headers=_headers(),
                    params={"preview": False},
                    follow_redirects=False,
                )
                if ae_resp.status_code == 200:
                    image_bytes = ae_resp.content
                    content_disposition = ae_resp.headers.get("content-disposition", "")
                elif ae_resp.status_code in (301, 302, 303, 307, 308):
                    location = ae_resp.headers.get("location", "")
                    if location.startswith("/"):
                        location = f"https://api.autoenhance.ai{location}"
                    img_resp = await client.get(location, follow_redirects=True)
                    img_resp.raise_for_status()
                    image_bytes = img_resp.content
                    content_disposition = img_resp.headers.get("content-disposition", "")
                else:
                    logger.error(f"[AUTOENHANCE] Unexpected status {ae_resp.status_code} for {image_id}")
                    continue

                rename_map = session.get("autoenhance_rename_map") or {}
                filename = rename_map.get(image_id) or f"{image_id}.jpg"

                results.append((image_bytes, filename))
                logger.info(f"[AUTOENHANCE] Downloaded enhanced image {image_id}")

    except Exception as e:
        logger.error(f"[AUTOENHANCE] download_enhanced_photos failed: {e}")

    return results