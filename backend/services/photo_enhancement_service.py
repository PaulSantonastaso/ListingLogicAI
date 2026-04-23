"""
photo_enhancement_service.py

Handles Autoenhance.ai API integration for real estate photo editing.

Flow:
  1. trigger_photo_enhancement() — called from Stripe webhook
     Uploads images to Autoenhance, creates an order, stores order_id on session
  2. download_enhanced_photos() — called from Autoenhance webhook
     Downloads all enhanced images from a completed order

Enhancement settings per image:
  - Exterior with sky_visible: sky replacement + vertical correction
  - Exterior without sky:      vertical correction only
  - Interior:                  window pull + vertical correction

All other enhancements (color correction, exposure, white balance)
are handled automatically by Autoenhance's AI.

Environment variables required:
  AUTOENHANCE_API_KEY — from Autoenhance dashboard
"""

import logging
import os
from io import BytesIO

import httpx

logger = logging.getLogger(__name__)

AUTOENHANCE_BASE_URL = "https://api.autoenhance.ai/v3"
AUTOENHANCE_API_KEY = os.getenv("AUTOENHANCE_API_KEY", "")


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {AUTOENHANCE_API_KEY}",
        "Content-Type": "application/json",
        "x-api-version": "2025-05-05",
    }


def _enhancement_settings(room_type: str, sky_visible: bool) -> dict:
    """
    Returns per-image enhancement settings based on room type and sky visibility.
    Autoenhance handles all other corrections automatically.
    """
    is_exterior = room_type.upper() in ("FRONT_EXTERIOR", "BACK_EXTERIOR", "EXTERIOR")

    if is_exterior and sky_visible:
        return {
            "sky_replacement": True,
            "vertical_correction": True,
            "window_pull_type": "NONE",
        }
    elif is_exterior:
        return {
            "sky_replacement": False,
            "vertical_correction": True,
            "window_pull_type": "NONE",
        }
    else:
        return {
            "sky_replacement": False,
            "vertical_correction": True,
            "window_pull_type": "ONLY_WINDOWS",
        }


async def trigger_photo_enhancement(session_id: str, session: dict) -> None:
    """
    Uploads all session images to Autoenhance and creates an order.
    Stores the order_id on the session for webhook lookup.
    Called as a fire-and-forget task from the Stripe webhook.
    """
    if not AUTOENHANCE_API_KEY:
        logger.warning("[AUTOENHANCE] No API key set — skipping photo enhancement")
        return

    enhanced_images = session.get("enhanced_images") or []
    analyzed_images = session.get("analyzed_images") or []

    # Fall back to R2 if images not in memory (upsell after session expiry)
    if not enhanced_images:
        from services.r2_service import load_original_images
        enhanced_images = load_original_images(session_id)

    if not enhanced_images:
        logger.warning(f"[AUTOENHANCE] No images found on session {session_id}")
        return

    # Build renamed filename lookup for SEO-preserving filenames
    results = session.get("results") or {}
    listing_details = results.get("listing_details")
    rename_lookup: dict[str, str] = {}
    if listing_details and hasattr(listing_details, "all_images"):
        for img in listing_details.all_images:
            rename_lookup[img.image_id] = img.renamed_filename

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            # Step 1 — Create order
            order_resp = await client.post(
                f"{AUTOENHANCE_BASE_URL}/orders",
                headers=_headers(),
                json={"name": session_id},
            )
            order_resp.raise_for_status()
            order_id = order_resp.json()["id"]
            session["autoenhance_order_id"] = order_id
            logger.info(f"[AUTOENHANCE] Created order {order_id} for session {session_id}")

            # Step 2 — Upload each image with per-image settings
            for i, (image_bytes, filename) in enumerate(enhanced_images):
                # Derive our internal image ID — matches analyze_single_image_async
                our_image_id = f"img_{i+1:03}"

                # Match analyzed image for room_type and sky_visible
                analyzed = analyzed_images[i] if i < len(analyzed_images) else None
                room_type = analyzed.metadata.room_type if analyzed else "INTERIOR"
                sky_visible = analyzed.metadata.sky_visible if analyzed else False

                settings = _enhancement_settings(room_type, sky_visible)

                # Use renamed filename for SEO value — fall back to original filename
                renamed = rename_lookup.get(our_image_id, filename)

                # Create image record on Autoenhance
                create_resp = await client.post(
                    f"{AUTOENHANCE_BASE_URL}/images",
                    headers=_headers(),
                    json={
                        "order_id": order_id,
                        "filename": renamed,
                        **settings,
                    },
                )
                create_resp.raise_for_status()
                image_data = create_resp.json()
                s3_url = image_data["s3PutObjectUrl"]
                ae_image_id = image_data["id"]

                # Upload raw bytes to S3 presigned URL
                upload_resp = await client.put(
                    s3_url,
                    content=image_bytes,
                    headers={"Content-Type": "application/octet-stream"},
                )
                upload_resp.raise_for_status()
                logger.info(f"[AUTOENHANCE] Uploaded {ae_image_id} as {renamed}")

            # Step 3 — Process order
            process_resp = await client.post(
                f"{AUTOENHANCE_BASE_URL}/orders/{order_id}/process",
                headers=_headers(),
            )
            process_resp.raise_for_status()
            logger.info(f"[AUTOENHANCE] Order {order_id} submitted for processing")

    except Exception as e:
        logger.error(f"[AUTOENHANCE] trigger_photo_enhancement failed for session {session_id}: {e}")
        session["enhancement_status"] = "error"


async def download_enhanced_photos(order_id: str) -> list[tuple[bytes, str]]:
    """
    Downloads all enhanced images from a completed Autoenhance order.
    Returns a list of (image_bytes, filename) tuples.
    """
    results = []

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            # Get all images in the order
            images_resp = await client.get(
                f"{AUTOENHANCE_BASE_URL}/images",
                headers=_headers(),
                params={"order_id": order_id},
            )
            images_resp.raise_for_status()
            images = images_resp.json().get("images", [])

            for image in images:
                image_id = image["id"]
                filename = image.get("filename", f"{image_id}.jpg")

                # Get enhanced download URL
                download_resp = await client.get(
                    f"{AUTOENHANCE_BASE_URL}/images/{image_id}/enhanced",
                    headers=_headers(),
                )
                download_resp.raise_for_status()
                download_url = download_resp.json().get("url")

                if not download_url:
                    logger.warning(f"[AUTOENHANCE] No download URL for image {image_id}")
                    continue

                # Download the enhanced image bytes
                img_resp = await client.get(download_url)
                img_resp.raise_for_status()
                results.append((img_resp.content, filename))
                logger.info(f"[AUTOENHANCE] Downloaded enhanced image {filename}")

    except Exception as e:
        logger.error(f"[AUTOENHANCE] download_enhanced_photos failed for order {order_id}: {e}")

    return results