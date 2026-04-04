"""
package_builder_service.py

Builds a complete marketing package ZIP in memory from a pipeline results dict.
Returns bytes that can be passed directly to Streamlit's download_button.

No file system writes — everything lives in memory and is garbage collected
after the download is served.
"""

import io
import zipfile
from datetime import datetime


def _format_header(title: str) -> str:
    border = "=" * 60
    return f"{border}\n{title}\n{border}\n\n"


def _format_section(title: str, content: str) -> str:
    border = "-" * 40
    return f"{border}\n{title}\n{border}\n{content}\n\n"


def _build_headline_file(res: dict) -> str:
    lines = [_format_header("LISTING HEADLINE")]
    lines.append(res.get("headline", "No headline generated."))
    lines.append("\n\nUSAGE:")
    lines.append("- Zillow 'What's Special' section")
    lines.append("- Email subject lines")
    lines.append("- Social media captions")
    lines.append("- Open house signage")
    return "\n".join(lines)


def _build_mls_description_file(res: dict) -> str:
    mls = res.get("mls_summary", "No MLS description generated.")
    char_count = len(mls)
    lines = [_format_header("MLS DESCRIPTION")]
    lines.append(mls)
    lines.append(f"\n\n[{char_count} / 950 characters]")
    return "\n".join(lines)


def _build_social_posts_file(res: dict) -> str:
    lines = [_format_header("SOCIAL MEDIA POSTS")]
    social_posts = res.get("social_posts", [])

    if not social_posts:
        lines.append("No social posts generated.")
        return "\n".join(lines)

    for post in social_posts:
        platform = post.platform or "Social"
        slot = (post.slot_name or "post").replace("_", " ").title()
        label = f"{platform} — {slot}"

        details = []
        if post.recommended_aspect_ratio:
            details.append(f"Aspect ratio: {post.recommended_aspect_ratio}")
        if post.image_filename:
            details.append(f"Image: {post.image_filename}")
        if post.room_type:
            details.append(f"Room: {post.room_type.replace('_', ' ').title()}")
        if post.crop_guidance:
            details.append(f"Crop guidance: {post.crop_guidance}")

        detail_str = "\n".join(details)
        content = f"{detail_str}\n\nCAPTION:\n{post.social_media_post}"
        lines.append(_format_section(label, content))

    return "\n".join(lines)


def _build_email_campaign_file(res: dict, email_tone: str = "Professional") -> str:
    lines = [_format_header(f"EMAIL CAMPAIGN — {email_tone.upper()} TONE")]
    lines.append(
        "Fill in [DAYS ON MARKET] and [SOLD PRICE] in the Just Sold email before sending.\n"
        "Fill in [Day] and [Time] in the Open House email before sending.\n"
    )

    campaign = res.get("email_campaign")
    if not campaign:
        lines.append("No email campaign generated.")
        return "\n".join(lines)

    emails = [
        ("EMAIL 1 — JUST LISTED", campaign.just_listed, "Send day 1 the listing goes live."),
        ("EMAIL 2 — OPEN HOUSE INVITATION", campaign.open_house, "Send day 3-5 before the open house."),
        ("EMAIL 3 — WHY THIS HOME", campaign.why_this_home, "Send day 7-10, mid-campaign."),
        ("EMAIL 4 — JUST SOLD", campaign.just_sold, "Send post-close. Fill in placeholders before sending."),
    ]

    for label, email, timing in emails:
        content = (
            f"TIMING: {timing}\n\n"
            f"SUBJECT: {email.subject}\n"
            f"PREVIEW: {email.preview_text}\n\n"
            f"BODY:\n{email.body}"
        )
        lines.append(_format_section(label, content))

    return "\n".join(lines)


def _build_video_scripts_file(res: dict) -> str:
    lines = [_format_header("SHORT FORM VIDEO SCRIPTS")]
    lines.append(
        "Film these scripts with your phone. Follow each shot direction in order.\n"
        "No video editing experience required.\n"
    )

    video_suite = res.get("video_scripts")
    if not video_suite:
        lines.append("No video scripts generated.")
        return "\n".join(lines)

    scripts = [
        ("INSTAGRAM REEL", video_suite.reel),
        ("TIKTOK", video_suite.tiktok),
        ("YOUTUBE SHORT", video_suite.youtube_short),
    ]

    for label, script in scripts:
        shot_lines = []
        for shot in script.shots:
            image_ref = f" [{shot.image_filename}]" if shot.image_filename else ""
            features = ", ".join(shot.visible_features) if shot.visible_features else ""
            feature_str = f" — {features}" if features else ""
            shot_lines.append(
                f"  Shot {shot.order}{image_ref}{feature_str}\n"
                f"  Direction: {shot.direction}"
            )

        content = (
            f"Duration: {script.duration_seconds} seconds\n\n"
            f"HOOK:\n{script.hook}\n\n"
            f"SHOT LIST:\n" + "\n\n".join(shot_lines) + f"\n\n"
            f"VOICEOVER:\n{script.voiceover}\n\n"
            f"CALL TO ACTION:\n{script.cta}"
        )
        lines.append(_format_section(label, content))

    return "\n".join(lines)


def _build_compliance_audit_file(res: dict) -> str:
    lines = [_format_header("FAIR HOUSING COMPLIANCE AUDIT")]
    lines.append(
        "Every asset in your campaign has been reviewed for fair housing compliance.\n"
        "Review any FLAGGED or REVISED items before publishing.\n"
    )

    compliance_results = res.get("compliance_results", [])
    if not compliance_results:
        lines.append("No compliance results available.")
        return "\n".join(lines)

    status_counts = {"pass": 0, "revised": 0, "flagged": 0}
    audit_lines = []

    for review in compliance_results:
        status_icon = {"pass": "✓ PASS", "revised": "~ REVISED", "flagged": "! FLAGGED"}.get(
            review.status, "? UNKNOWN"
        )
        label = review.asset_type.replace("_", " ").upper()
        entry = f"{status_icon} — {label}"

        if review.issues_found:
            entry += "\n  Issues:"
            for issue in review.issues_found:
                entry += f"\n    - {issue}"

        if review.reviewer_notes:
            entry += f"\n  Notes: {review.reviewer_notes}"

        if review.status in status_counts:
            status_counts[review.status] += 1

        audit_lines.append(entry)

    # Summary at top
    total = len(compliance_results)
    summary = (
        f"SUMMARY: {total} assets reviewed — "
        f"{status_counts['pass']} passed, "
        f"{status_counts['revised']} revised, "
        f"{status_counts['flagged']} flagged\n"
    )
    lines.append(summary)
    lines.append("\nDETAILED RESULTS:\n")
    lines.extend(audit_lines)

    return "\n".join(lines)


def build_marketing_package_zip(
    res: dict,
    address: str | None = None,
    email_tone: str = "Professional",
) -> bytes:
    """
    Build a complete marketing package ZIP in memory.

    Args:
        res: The marketing results dict from generate_marketing_assets_service
        address: Property address for the ZIP filename
        email_tone: The tone used for the email campaign

    Returns:
        ZIP file as bytes, ready for Streamlit download_button
    """
    # Build a clean filename from address
    if address:
        safe_address = address.replace(" ", "_").replace("/", "-")[:40]
        zip_filename_prefix = f"{safe_address}_"
    else:
        zip_filename_prefix = ""

    timestamp = datetime.now().strftime("%Y%m%d")

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        folder = f"{zip_filename_prefix}listing_package_{timestamp}/"

        zf.writestr(
            folder + "01_headline.txt",
            _build_headline_file(res)
        )
        zf.writestr(
            folder + "02_mls_description.txt",
            _build_mls_description_file(res)
        )
        zf.writestr(
            folder + "03_mls_import.csv",
            res.get("reso_csv", "")
        )
        zf.writestr(
            folder + "04_social_posts.txt",
            _build_social_posts_file(res)
        )
        zf.writestr(
            folder + "05_email_campaign.txt",
            _build_email_campaign_file(res, email_tone)
        )
        zf.writestr(
            folder + "06_video_scripts.txt",
            _build_video_scripts_file(res)
        )
        zf.writestr(
            folder + "07_compliance_audit.txt",
            _build_compliance_audit_file(res)
        )

    buffer.seek(0)
    return buffer.read()