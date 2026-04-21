"""
package_builder_service.py

Builds a complete marketing package ZIP in memory from a pipeline results dict.
Returns bytes that can be passed directly to Streamlit's download_button.

No file system writes — everything lives in memory and is garbage collected
after the download is served.

ZIP contents:
  01_headline.txt
  02_mls_description.txt
  03_listing_data_for_mls.txt   (tap-to-copy field reference — CSV toggled off)
  04_social_posts.txt
  05_email_campaign.txt
  06_compliance_audit.txt
  07_video_scripts.txt          (only included when ENABLE_VIDEO_SCRIPTS is True)
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


def _build_listing_data_file(res: dict) -> str:
    """
    Tap-to-copy field reference for manual MLS entry.
    Replaces the RESO CSV while board-specific validation is pending.
    Organized by category to match the order of most MLS input forms.
    """
    lines = [_format_header("LISTING DATA FOR MLS ENTRY")]
    lines.append(
        "Copy and paste each field into your MLS input form.\n"
        "Field names match standard RESO / MLS terminology.\n"
    )

    listing_details = res.get("listing_details")
    if not listing_details:
        lines.append("No listing data available.")
        return "\n".join(lines)

    ld = listing_details

    def field(label: str, value) -> str:
        if value is None or value == "" or value == 0:
            return f"  {label:<30} —"
        return f"  {label:<30} {value}"

    # --- Property Identification ---
    lines.append(_format_section("PROPERTY IDENTIFICATION", "\n".join([
        field("Street Address", getattr(ld, "unparsed_address", None)),
        field("City", getattr(ld, "city", None)),
        field("State", getattr(ld, "state_or_province", None)),
        field("Postal Code", getattr(ld, "postal_code", None)),
        field("County", getattr(ld, "county_or_parish", None)),
        field("Subdivision", getattr(ld, "subdivision_name", None)),
        field("Community", getattr(ld, "community_features", None)),
        field("MLS Area", getattr(ld, "mls_area_major", None)),
    ])))

    # --- Listing Details ---
    lines.append(_format_section("LISTING DETAILS", "\n".join([
        field("List Price", f"${getattr(ld, 'list_price', None):,}" if getattr(ld, "list_price", None) else None),
        field("Property Type", getattr(ld, "property_type", None)),
        field("Property Sub Type", getattr(ld, "property_sub_type", None)),
        field("Standard Status", getattr(ld, "standard_status", None)),
        field("Listing Agreement", getattr(ld, "listing_agreement", None)),
    ])))

    # --- Structure ---
    lines.append(_format_section("STRUCTURE", "\n".join([
        field("Bedrooms", getattr(ld, "bedrooms_total", None)),
        field("Bathrooms (Full)", getattr(ld, "bathrooms_full", None)),
        field("Bathrooms (Half)", getattr(ld, "bathrooms_half", None)),
        field("Living Area (sqft)", getattr(ld, "living_area", None)),
        field("Lot Size (sqft)", getattr(ld, "lot_size_square_feet", None)),
        field("Stories", getattr(ld, "stories_total", None)),
        field("Year Built", getattr(ld, "year_built", None)),
        field("Garage Spaces", getattr(ld, "garage_spaces", None)),
        field("Carport Spaces", getattr(ld, "carport_spaces", None)),
    ])))

    # --- Interior ---
    lines.append(_format_section("INTERIOR", "\n".join([
        field("Flooring", ", ".join(getattr(ld, "flooring", None) or [])),
        field("Interior Features", ", ".join(getattr(ld, "interior_features", None) or [])),
        field("Appliances", ", ".join(getattr(ld, "appliances", None) or [])),
        field("Fireplace", getattr(ld, "fireplace_yn", None)),
        field("Cooling", ", ".join(getattr(ld, "cooling", None) or [])),
        field("Heating", ", ".join(getattr(ld, "heating", None) or [])),
        field("Laundry Features", ", ".join(getattr(ld, "laundry_features", None) or [])),
    ])))

    # --- Exterior ---
    lines.append(_format_section("EXTERIOR", "\n".join([
        field("Exterior Features", ", ".join(getattr(ld, "exterior_features", None) or [])),
        field("Pool", getattr(ld, "pool_private_yn", None)),
        field("Pool Features", ", ".join(getattr(ld, "pool_features", None) or [])),
        field("Spa", getattr(ld, "spa_yn", None)),
        field("Parking Features", ", ".join(getattr(ld, "parking_features", None) or [])),
        field("Fencing", ", ".join(getattr(ld, "fencing", None) or [])),
        field("Patio Features", ", ".join(getattr(ld, "patio_and_porch_features", None) or [])),
    ])))

    # --- HOA + Financial ---
    lines.append(_format_section("HOA & FINANCIAL", "\n".join([
        field("HOA Y/N", getattr(ld, "association_yn", None)),
        field("HOA Fee", f"${getattr(ld, 'association_fee', None)}" if getattr(ld, "association_fee", None) else None),
        field("HOA Frequency", getattr(ld, "association_fee_frequency", None)),
        field("Tax Annual Amount", f"${getattr(ld, 'tax_annual_amount', None):,}" if getattr(ld, "tax_annual_amount", None) else None),
        field("Tax Year", getattr(ld, "tax_year", None)),
    ])))

    # --- Marketing ---
    lines.append(_format_section("MARKETING", "\n".join([
        field("Photos Count", getattr(ld, "photos_count", None)),
        field("Showing Instructions", getattr(ld, "showing_requirements", None)),
        field("Virtual Tour URL", getattr(ld, "virtual_tour_url_unbranded", None)),
    ])))

    lines.append("=" * 60)
    lines.append("Public Remarks (MLS Description):")
    lines.append("=" * 60)
    lines.append(res.get("mls_summary", ""))

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
            f"SHOT LIST:\n" + "\n\n".join(shot_lines) + "\n\n"
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

def _build_neighborhood_insight_file(res: dict) -> str:
    lines = [_format_header("NEIGHBORHOOD INSIGHT")]
    lines.append(
        "AI-generated neighborhood guide based on live local data.\n"
        "Review before sharing — verify place names are current.\n"
    )
    lines.append(res.get("neighborhood_guide", ""))
    return "\n".join(lines)

def build_marketing_package_zip(
    res: dict,
    address: str | None = None,
    email_tone: str = "Professional",
    rename_result=None,
) -> bytes:
    """
    Build a complete marketing package ZIP in memory.

    Args:
        res:           The marketing results dict from generate_marketing_assets_service
        address:       Property address for the ZIP filename
        email_tone:    The tone used for the email campaign
        rename_result: Optional RenameResult from build_renamed_image_set.
                       When provided, writes photos/curated/ and photos/additional/
                       subfolders into the ZIP.

    Returns:
        ZIP file as bytes, ready for Streamlit download_button
    """
    if address:
        safe_address = address.replace(" ", "_").replace("/", "-")[:40]
        zip_filename_prefix = f"{safe_address}_"
    else:
        zip_filename_prefix = ""

    timestamp = datetime.now().strftime("%Y%m%d")
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        folder = f"{zip_filename_prefix}listing_package_{timestamp}/"

        # --- Marketing copy files ---
        zf.writestr(folder + "01_headline.txt", _build_headline_file(res))
        zf.writestr(folder + "02_mls_description.txt", _build_mls_description_file(res))
        zf.writestr(folder + "03_listing_data_for_mls.txt", _build_listing_data_file(res))
        zf.writestr(folder + "04_social_posts.txt", _build_social_posts_file(res))
        zf.writestr(folder + "05_email_campaign.txt", _build_email_campaign_file(res, email_tone))
        zf.writestr(folder + "06_compliance_audit.txt", _build_compliance_audit_file(res))

        # Video scripts only included when feature is enabled
        if res.get("video_scripts") is not None:
            zf.writestr(folder + "07_video_scripts.txt", _build_video_scripts_file(res))

        if res.get("neighborhood_guide"):
            zf.writestr(folder + "08_neighborhood_insight.txt", _build_neighborhood_insight_file(res))

        # --- Photos subfolders ---
        # photos/curated/   — top CURATED_SET_SIZE images, AI-ranked and renamed
        # photos/additional/ — remaining images outside the curated set
        if rename_result is not None:
            for img in rename_result.curated:
                zf.writestr(
                    folder + f"photos/curated/{img.renamed_filename}",
                    img.image_bytes,
                )
            for img in rename_result.additional:
                zf.writestr(
                    folder + f"photos/additional/{img.renamed_filename}",
                    img.image_bytes,
                )

    buffer.seek(0)
    return buffer.read()