"""
email_service.py

Sends transactional emails via Resend.
https://resend.com/docs/api-reference/emails/send-email

Two email types:
  1. Listing delivery — sent immediately on payment confirmation
  2. Photo delivery   — sent when Autoenhance.ai completes (Item 13, stubbed)

Environment variables required:
  RESEND_API_KEY   — from resend.com dashboard
  FROM_EMAIL       — verified sending address (e.g. hello@listinglogicai.com)
                     Use onboarding@resend.dev for local dev without domain

Dev behavior:
  If RESEND_API_KEY is not set, logs the email content and returns gracefully.
  Never raises — email failure should never break the payment flow.
"""

import logging
import os

import httpx

from templates.listing_email import (
    build_listing_delivery_html,
    build_listing_delivery_subject,
    build_listing_delivery_text,
)
from templates.photos_email import (
    build_photos_delivery_html,
    build_photos_delivery_subject,
    build_photos_delivery_text,
)

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


def _get_config() -> tuple[str | None, str]:
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    return api_key, from_email


async def _send_email(
    to: str,
    subject: str,
    html: str,
    text: str,
) -> bool:
    """
    Send a single email via Resend API.
    Returns True on success, False on failure.
    Never raises — email errors are logged but don't bubble up.
    """
    api_key, from_email = _get_config()

    if not api_key:
        # Dev mode — log and return gracefully
        logger.info(
            "RESEND_API_KEY not set — skipping email send.\n"
            f"  To: {to}\n"
            f"  Subject: {subject}\n"
            f"  Preview: {text[:200]}..."
        )
        return True

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                RESEND_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": from_email,
                    "to": [to],
                    "subject": subject,
                    "html": html,
                    "text": text,
                },
                timeout=10.0,
            )

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Email sent successfully. Resend ID: {data.get('id')}")
            return True
        else:
            logger.error(
                f"Resend API error {response.status_code}: {response.text}"
            )
            return False

    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return False


async def send_listing_delivery_email(
    to: str,
    session: dict,
    download_token: str,
) -> bool:
    """
    Send the listing delivery email immediately after payment.

    Pulls headline, MLS description, and Just Listed email subject
    directly from session results. Download URL is constructed from
    the session ID and token.

    Args:
        to:             Agent email address (from Stripe checkout)
        session:        Full session dict from _sessions store
        download_token: Generated download token for the ZIP

    Returns:
        True on success, False on failure (never raises)
    """
    if not to:
        logger.warning("send_listing_delivery_email called with no recipient — skipping")
        return False

    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    session_id = session.get("session_id", "")
    download_url = f"{backend_url}/api/download/{session_id}/{download_token}"

    # Pull content from results
    results = session.get("results") or {}
    details = session.get("extracted_details")
    address = details.address if details else None

    headline = results.get("headline")
    mls_summary = results.get("mls_summary", "")
    mls_char_count = len(mls_summary) if mls_summary else 0

    # Just Listed email subject + preview
    campaign = results.get("email_campaign")
    just_listed_subject = None
    just_listed_preview = None
    if campaign and hasattr(campaign, "just_listed"):
        just_listed_subject = campaign.just_listed.subject
        just_listed_preview = campaign.just_listed.preview_text

    subject = build_listing_delivery_subject(address)
    html = build_listing_delivery_html(
        address=address,
        headline=headline,
        mls_description=mls_summary,
        mls_char_count=mls_char_count,
        just_listed_subject=just_listed_subject,
        just_listed_preview=just_listed_preview,
        download_url=download_url,
    )
    text = build_listing_delivery_text(
        address=address,
        headline=headline,
        mls_description=mls_summary,
        mls_char_count=mls_char_count,
        just_listed_subject=just_listed_subject,
        download_url=download_url,
    )

    return await _send_email(to=to, subject=subject, html=html, text=text)


async def send_photos_delivery_email(
    to: str,
    session: dict,
    photo_download_token: str,
    photo_count: int,
) -> bool:
    """
    Send the photo delivery email when Autoenhance.ai completes.
    Stubbed for Item 13 — infrastructure ready.

    Args:
        to:                  Agent email address
        session:             Full session dict
        photo_download_token: Separate download token for the enhanced photo ZIP
        photo_count:         Number of photos that were enhanced

    Returns:
        True on success, False on failure (never raises)
    """
    if not to:
        logger.warning("send_photos_delivery_email called with no recipient — skipping")
        return False

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    session_id = session.get("session_id", "")
    download_url = f"{frontend_url}/api/download-photos/{session_id}/{photo_download_token}"

    details = session.get("extracted_details")
    address = details.address if details else None

    subject = build_photos_delivery_subject(address)
    html = build_photos_delivery_html(
        address=address,
        photo_count=photo_count,
        download_url=download_url,
    )
    text = build_photos_delivery_text(
        address=address,
        photo_count=photo_count,
        download_url=download_url,
    )

    return await _send_email(to=to, subject=subject, html=html, text=text)