"""
r2_service.py

Cloudflare R2 storage for ListingLogicAI.
S3-compatible API — uses boto3 with R2 endpoint.

Handles:
  1. Enhanced photo ZIPs — download link in photos delivery email
  2. Original images — persisted at payment for upsell fulfillment
  3. Enhanced images — served in preview page grid post-enhancement
  4. Session JSON — durable session state for 7-day preview link

Environment variables required:
  R2_ACCOUNT_ID
  R2_ACCESS_KEY_ID
  R2_SECRET_ACCESS_KEY
  R2_BUCKET_NAME
  R2_PUBLIC_URL
"""

import json
import logging
import os
import zipfile
from io import BytesIO
from typing import Any

logger = logging.getLogger(__name__)

SESSION_TTL = 604800  # 7 days in seconds


def _get_s3_client():
    """
    Build and return a boto3 S3 client configured for Cloudflare R2.
    Returns None if credentials are not set (stub mode).
    """
    account_id = os.getenv("R2_ACCOUNT_ID")
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")

    if not all([account_id, access_key, secret_key]):
        return None

    import boto3
    from botocore.config import Config

    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def _bucket() -> str:
    return os.getenv("R2_BUCKET_NAME", "llai-photos")


# ---------------------------------------------------------------------------
# Session JSON — durable preview page state
# ---------------------------------------------------------------------------

def save_session_json(session_id: str, session: dict) -> bool:
    """
    Serializes and saves session state to R2 as JSON.
    Called at payment time and again when enhancement completes.
    Returns True on success, False on failure (never raises).

    R2 key: sessions/{session_id}/session.json
    """
    s3 = _get_s3_client()
    if not s3:
        logger.warning("[R2] Stub mode — skipping session JSON save")
        return False

    r2_key = f"sessions/{session_id}/session.json"

    try:
        # Build a serializable snapshot — exclude raw image bytes
        snapshot = {
            "session_id": session_id,
            "paid": session.get("paid", "none"),
            "agent_email": session.get("agent_email"),
            "download_token": session.get("download_token"),
            "download_token_created_at": session.get("download_token_created_at"),
            "enhancement_status": session.get("enhancement_status", "none"),
            "photo_download_url": session.get("photo_download_url"),
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at"),
            "generation_status": session.get("generation_status"),
            "extracted_details": _serialize_details(session.get("extracted_details")),
            "results": _serialize_results(session.get("results")),
            "image_intelligence": _serialize_image_intelligence(
                session.get("image_intelligence")
            ),
        }

        s3.put_object(
            Bucket=_bucket(),
            Key=r2_key,
            Body=json.dumps(snapshot, default=str).encode("utf-8"),
            ContentType="application/json",
        )
        logger.info(f"[R2] Session JSON saved — {r2_key}")
        return True

    except Exception as e:
        logger.error(f"[R2] Failed to save session JSON for {session_id}: {e}")
        return False


def load_session_json(session_id: str) -> dict | None:
    """
    Loads and returns session JSON from R2.
    Returns None if not found or expired.
    Called when session is missing from in-memory store.

    R2 key: sessions/{session_id}/session.json
    """
    s3 = _get_s3_client()
    if not s3:
        return None

    r2_key = f"sessions/{session_id}/session.json"

    try:
        response = s3.get_object(Bucket=_bucket(), Key=r2_key)
        data = json.loads(response["Body"].read().decode("utf-8"))

        # Check expiry
        import time
        created_at = data.get("created_at", 0)
        if time.time() - created_at > SESSION_TTL:
            logger.info(f"[R2] Session {session_id} expired — not rehydrating")
            return None

        data["rehydrated"] = True
        logger.info(f"[R2] Session {session_id} rehydrated from R2")
        return data

    except Exception as e:
        logger.info(f"[R2] Session JSON not found for {session_id}: {e}")
        return None


# ---------------------------------------------------------------------------
# Original images — persisted at payment for upsell fulfillment
# ---------------------------------------------------------------------------

def save_original_images(
    session_id: str,
    images: list[tuple[bytes, str]],
) -> bool:
    """
    Saves original uploaded images to R2 at payment time.
    Required for photo editing upsell fulfillment after session expires.
    Returns True on success, False on failure (never raises).

    R2 key: sessions/{session_id}/originals/{filename}
    """
    s3 = _get_s3_client()
    if not s3:
        logger.warning("[R2] Stub mode — skipping original image save")
        return False

    success_count = 0
    for image_bytes, filename in images:
        r2_key = f"sessions/{session_id}/originals/{filename}"
        try:
            s3.put_object(
                Bucket=_bucket(),
                Key=r2_key,
                Body=image_bytes,
                ContentType="image/jpeg",
            )
            success_count += 1
        except Exception as e:
            logger.error(f"[R2] Failed to save original image {filename}: {e}")

    logger.info(
        f"[R2] Saved {success_count}/{len(images)} original images for session {session_id}"
    )
    return success_count == len(images)


def load_original_images(session_id: str) -> list[tuple[bytes, str]]:
    """
    Loads original images from R2 for upsell fulfillment.
    Returns list of (image_bytes, filename) tuples.
    Returns empty list if not found.

    R2 key: sessions/{session_id}/originals/{filename}
    """
    s3 = _get_s3_client()
    if not s3:
        return []

    try:
        prefix = f"sessions/{session_id}/originals/"
        response = s3.list_objects_v2(Bucket=_bucket(), Prefix=prefix)
        objects = response.get("Contents", [])

        images = []
        for obj in objects:
            key = obj["Key"]
            filename = key.replace(prefix, "")
            img_response = s3.get_object(Bucket=_bucket(), Key=key)
            image_bytes = img_response["Body"].read()
            images.append((image_bytes, filename))

        logger.info(f"[R2] Loaded {len(images)} original images for session {session_id}")
        return images

    except Exception as e:
        logger.error(f"[R2] Failed to load original images for {session_id}: {e}")
        return []


# ---------------------------------------------------------------------------
# Enhanced images — saved post-Autoenhance, served in preview grid
# ---------------------------------------------------------------------------

def save_enhanced_images(
    session_id: str,
    images: list[tuple[bytes, str]],
) -> bool:
    """
    Saves enhanced images to R2 after Autoenhance processing completes.
    Uses renamed filenames for SEO value.
    Returns True on success, False on failure (never raises).

    R2 key: sessions/{session_id}/enhanced/{renamed_filename}
    """
    s3 = _get_s3_client()
    if not s3:
        logger.warning("[R2] Stub mode — skipping enhanced image save")
        return False

    success_count = 0
    for image_bytes, filename in images:
        r2_key = f"sessions/{session_id}/enhanced/{filename}"
        try:
            s3.put_object(
                Bucket=_bucket(),
                Key=r2_key,
                Body=image_bytes,
                ContentType="image/jpeg",
            )
            success_count += 1
        except Exception as e:
            logger.error(f"[R2] Failed to save enhanced image {filename}: {e}")

    logger.info(
        f"[R2] Saved {success_count}/{len(images)} enhanced images for session {session_id}"
    )
    return success_count == len(images)


def get_enhanced_image(session_id: str, filename: str) -> bytes | None:
    """
    Retrieves a single enhanced image from R2.
    Returns bytes or None if not found.

    R2 key: sessions/{session_id}/enhanced/{filename}
    """
    s3 = _get_s3_client()
    if not s3:
        return None

    r2_key = f"sessions/{session_id}/enhanced/{filename}"
    try:
        response = s3.get_object(Bucket=_bucket(), Key=r2_key)
        return response["Body"].read()
    except Exception as e:
        logger.info(f"[R2] Enhanced image not found {r2_key}: {e}")
        return None


# ---------------------------------------------------------------------------
# Enhanced photo ZIP — download link in photos delivery email
# ---------------------------------------------------------------------------

async def upload_photos_zip(
    session_id: str,
    images: list[tuple[bytes, str]],
) -> str:
    """
    Builds a ZIP of enhanced images and uploads to R2.
    Returns a presigned download URL valid for 7 days.

    R2 key: sessions/{session_id}/enhanced_photos.zip
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for image_bytes, filename in images:
            zf.writestr(f"enhanced_photos/{filename}", image_bytes)
    zip_buffer.seek(0)
    zip_bytes = zip_buffer.read()

    r2_key = f"sessions/{session_id}/enhanced_photos.zip"

    s3 = _get_s3_client()
    if not s3:
        logger.warning("[R2] Stub mode — returning placeholder URL")
        return f"https://placeholder-r2-url/{r2_key}"

    try:
        s3.put_object(
            Bucket=_bucket(),
            Key=r2_key,
            Body=zip_bytes,
            ContentType="application/zip",
        )

        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": _bucket(), "Key": r2_key},
            ExpiresIn=SESSION_TTL,
        )

        logger.info(f"[R2] Photos ZIP uploaded — {r2_key} ({len(zip_bytes)} bytes)")
        return presigned_url

    except Exception as e:
        logger.error(f"[R2] ZIP upload failed for {r2_key}: {e}")
        raise


# ---------------------------------------------------------------------------
# Serialization helpers — strip non-JSON-serializable objects
# ---------------------------------------------------------------------------

def _serialize_details(details) -> dict | None:
    if not details:
        return None
    try:
        return details.model_dump()
    except Exception:
        return None


def _serialize_results(results: dict | None) -> dict | None:
    if not results:
        return None
    try:
        serializable = {}
        for key, value in results.items():
            if key in ("listing_details",):
                # Skip non-serializable objects
                continue
            try:
                json.dumps(value, default=str)
                serializable[key] = value
            except Exception:
                try:
                    serializable[key] = value.model_dump() if hasattr(value, "model_dump") else str(value)
                except Exception:
                    pass
        return serializable
    except Exception:
        return None


def _serialize_image_intelligence(intelligence) -> dict | None:
    if not intelligence:
        return None
    try:
        return intelligence.model_dump()
    except Exception:
        return None