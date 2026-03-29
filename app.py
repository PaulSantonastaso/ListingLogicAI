import asyncio
import hashlib
import os

import streamlit as st
from dotenv import load_dotenv

from services.listing_pipeline_service import (
    extract_property_data_service,
    generate_marketing_assets_service,
)
from services.image_analysis_service import analyze_property_images
from services.fusion_service import merge_image_features_into_property
from services.image_enhancement_service import enhance_listing_photos
from services.property_normalization_service import normalize_property_details
from services.image_intelligence_service import build_image_intelligence

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ListingLogicAI",
    page_icon="🏠",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state bootstrap
# ---------------------------------------------------------------------------
_session_defaults = {
    "extracted_details": None,
    "marketing_results": None,
    "analyzed_images": None,
    "uploaded_image_fingerprint": None,
    "original_images": None,
    "enhanced_images": None,
    "image_intelligence": None,
}
for key, default in _session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_uploaded_image_fingerprint(uploaded_files) -> str:
    hasher = hashlib.sha256()
    for file in uploaded_files:
        hasher.update(file.name.encode("utf-8"))
        hasher.update(file.getvalue())
    return hasher.hexdigest()


def extract_room_from_evidence(evidence: str | None) -> str:
    if not evidence or "(" not in evidence or ")" not in evidence:
        return "other"
    try:
        return evidence.split("(")[-1].split(")")[0].strip()
    except Exception:
        return "other"


def group_feature_candidates(candidates):
    grouped = {}
    for candidate in candidates:
        room = extract_room_from_evidence(candidate.evidence)
        grouped.setdefault(room, []).append(candidate)
    for room in grouped:
        grouped[room].sort(key=lambda x: x.confidence, reverse=True)
    return grouped


def build_image_lookup(images):
    if not images:
        return {}
    return {filename: image_bytes for image_bytes, filename in images}


def render_social_post_card(post, enhanced_lookup):
    platform_label = post.platform or "Social"
    slot_label = (post.slot_name or "social_post").replace("_", " ").title()
    aspect_ratio = post.recommended_aspect_ratio or "N/A"
    room_type = (post.room_type or "unknown").replace("_", " ").title()
    feature_text = ", ".join(post.visible_features) if post.visible_features else "None listed"

    st.markdown(f"#### {platform_label}")
    st.caption(f"{slot_label} · {aspect_ratio}")

    selected_image = enhanced_lookup.get(post.image_filename or "")
    if selected_image:
        st.image(selected_image, use_container_width=True)
    else:
        st.info("Image preview unavailable.")

    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        st.caption(f"🛋 {room_type}")
    with meta_col2:
        st.caption(f"✨ {feature_text}")

    if getattr(post, "crop_guidance", None):
        st.caption(f"✂️ {post.crop_guidance}")

    st.text_area(
        "Caption",
        value=post.social_media_post,
        height=200,
        key=f"social_post_{post.slot_name}_{post.image_id}",
    )


def render_email_card(label: str, email, key_prefix: str):
    """Render a single campaign email with subject, preview, and body."""
    st.markdown(f"**Subject:** {email.subject}")
    st.caption(f"Preview: {email.preview_text}")
    st.text_area(
        "Body",
        value=email.body,
        height=280,
        key=f"{key_prefix}_body",
    )


def render_video_script_card(script, enhanced_lookup, key_prefix: str):
    """Render a single platform video script with hook, shot list, voiceover, and CTA."""
    st.markdown(f"**⏱ Target Duration:** {script.duration_seconds} seconds")
    st.divider()

    # Hook
    st.markdown("**🎣 Hook**")
    st.caption("Spoken or shown in the first 2-3 seconds — stops the scroll.")
    st.info(script.hook)

    # Shot list
    if script.shots:
        st.markdown("**🎬 Shot List**")
        st.caption("Film these shots in order. Each maps to a specific space in the property.")

        for shot in script.shots:
            with st.container():
                shot_col1, shot_col2 = st.columns([1, 2])

                with shot_col1:
                    image_bytes = enhanced_lookup.get(shot.image_filename or "")
                    if image_bytes:
                        st.image(image_bytes, use_container_width=True)
                        st.caption(
                            (shot.room_type or "").replace("_", " ").title()
                        )
                    else:
                        room_label = (shot.room_type or "No image").replace("_", " ").title()
                        st.markdown(
                            f"<div style='background:#f0f2f6;border-radius:8px;"
                            f"padding:24px;text-align:center;color:#666;'>"
                            f"📷 {room_label}</div>",
                            unsafe_allow_html=True,
                        )

                with shot_col2:
                    st.markdown(f"**Shot {shot.order}**")
                    if shot.visible_features:
                        st.caption("Features: " + ", ".join(shot.visible_features))
                    st.write(f"🎥 {shot.direction}")

                st.markdown("---")

    # Voiceover
    st.markdown("**🎙 Voiceover Script**")
    st.caption("Read this while filming or record it in post.")
    st.text_area(
        "Voiceover",
        value=script.voiceover,
        height=200,
        key=f"{key_prefix}_voiceover",
    )

    # CTA
    st.markdown("**📣 Call to Action**")
    st.success(script.cta)


def render_compliance_badge(review):
    status_icon = {"pass": "✅", "revised": "✏️", "flagged": "⚠️"}.get(review.status, "ℹ️")
    label = review.asset_type.replace("_", " ").title()
    st.markdown(f"**{status_icon} {label}**")
    if review.issues_found:
        for issue in review.issues_found:
            st.caption(f"• {issue}")
    if review.reviewer_notes:
        st.caption(review.reviewer_notes)


# ---------------------------------------------------------------------------
# Guard: API key must be present in env
# ---------------------------------------------------------------------------
if not API_KEY:
    st.error(
        "**GEMINI_API_KEY not found.** Add it to your `.env` file and restart the app.\n\n"
        "```\nGEMINI_API_KEY=your-key-here\n```"
    )
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/home.png", width=48)
    st.title("ListingLogicAI")
    st.caption("AI-powered listing marketing for high-performing agents.")
    st.divider()

    st.subheader("⚙️ Settings")
    email_tone = st.selectbox(
        "Campaign Tone",
        ["Professional", "Luxury", "Casual", "Urgent"],
        index=0,
        help="Sets the voice and style across all 4 campaign emails.",
    )

    st.divider()
    st.caption("📋 Workflow")
    st.markdown(
        """
        1. Upload photos + enter notes  
        2. Review & confirm extracted details  
        3. Generate full marketing suite  
        """
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🏠 ListingLogicAI")
st.markdown("From rough notes to a complete listing campaign — in seconds.")
st.divider()

# ---------------------------------------------------------------------------
# Main tabs
# ---------------------------------------------------------------------------
tab_generator, tab_photos = st.tabs(["📝 Listing Generator", "📸 Photo Enhancer"])

# ===========================================================================
# TAB 1 — LISTING GENERATOR
# ===========================================================================
with tab_generator:

    # --- Input section ---
    input_col, tips_col = st.columns([3, 1])

    with input_col:
        uploaded_images = st.file_uploader(
            "Upload Property Photos",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Upload listing photos. AI Image Intelligence will score and select the best ones for your social posts and video scripts.",
        )

        user_notes = st.text_area(
            "Agent Notes",
            placeholder=(
                "Paste your rough notes here — address, price, beds/baths, "
                "key upgrades, neighborhood highlights, anything you'd tell a buyer..."
            ),
            height=160,
        )

    with tips_col:
        st.markdown("##### 💡 Tips")
        st.caption(
            "The more detail you provide in your notes, the stronger the output. "
            "Include things like recent renovations, standout finishes, community perks, "
            "and what makes this listing unique."
        )

    extract_btn = st.button("Step 1: Extract & Analyze", type="secondary", use_container_width=True)

    if extract_btn:
        if not user_notes.strip():
            st.warning("Please enter agent notes before extracting.")
        else:
            with st.spinner("Extracting property details and analyzing photos..."):
                try:
                    details = asyncio.run(
                        extract_property_data_service(user_notes, API_KEY)
                    )

                    if not uploaded_images:
                        st.session_state.analyzed_images = None
                        st.session_state.original_images = None
                        st.session_state.enhanced_images = None
                        st.session_state.uploaded_image_fingerprint = None
                        st.session_state.image_intelligence = None

                    if uploaded_images:
                        current_fingerprint = build_uploaded_image_fingerprint(uploaded_images)

                        if (
                            st.session_state.analyzed_images is None
                            or st.session_state.uploaded_image_fingerprint != current_fingerprint
                        ):
                            images = [(f.getvalue(), f.name) for f in uploaded_images]
                            st.session_state.original_images = images

                            enhanced_images = enhance_listing_photos(images)
                            st.session_state.enhanced_images = enhanced_images

                            analyzed_images = asyncio.run(
                                analyze_property_images(enhanced_images, API_KEY)
                            )
                            st.session_state.analyzed_images = analyzed_images
                            st.session_state.uploaded_image_fingerprint = current_fingerprint

                        if st.session_state.analyzed_images:
                            st.session_state.image_intelligence = build_image_intelligence(
                                st.session_state.analyzed_images
                            )
                            details = merge_image_features_into_property(
                                details, st.session_state.analyzed_images
                            )
                        else:
                            st.session_state.image_intelligence = None

                    details = normalize_property_details(details)
                    st.session_state.extracted_details = details
                    st.session_state.marketing_results = None

                except Exception as e:
                    st.error(f"Extraction error: {e}")

    # --- HITL: Review & Edit ---
    if st.session_state.extracted_details is not None:
        st.divider()
        st.subheader("🛠 Review & Confirm Property Details")
        st.caption("Verify the extracted details before generating your campaign. Edits here flow into every asset.")

        details = st.session_state.extracted_details

        col1, col2, col3 = st.columns(3)

        with col1:
            edit_address = st.text_input("Street Address", value=details.address or "")
            edit_city = st.text_input("City", value=details.city or "")
            edit_state = st.text_input("State", value=details.state or "")
            edit_postal_code = st.text_input("Postal Code", value=details.postal_code or "")

        with col2:
            edit_community_name = st.text_input("Community Name", value=details.community_name or "")
            edit_subdivision_name = st.text_input("Subdivision Name", value=details.subdivision_name or "")
            edit_price = st.number_input("List Price", value=int(details.list_price or 0))

        with col3:
            edit_beds = st.number_input("Beds", value=int(details.bedrooms or 0))
            edit_baths = st.number_input("Baths", value=float(details.bathrooms or 0))

        edit_features = st.text_area(
            "Key Features (comma separated)",
            value=", ".join(st.session_state.extracted_details.key_features),
        )

        details = st.session_state.extracted_details
        if details.feature_candidates:
            st.markdown("---")
            st.subheader("🔍 Image-Detected Features")
            st.caption("Features detected from your photos. Check any you want included in the campaign.")

            selected_features = []
            grouped_candidates = group_feature_candidates(details.feature_candidates)

            for room, candidates in grouped_candidates.items():
                room_label = room.replace("_", " ").title()
                st.markdown(f"**{room_label}**")

                for candidate in candidates:
                    default_checked = candidate.confidence >= 0.90
                    checked = st.checkbox(
                        f"{candidate.name} (confidence {candidate.confidence:.2f})",
                        value=default_checked,
                        help=candidate.evidence,
                        key=f"feature_{room}_{candidate.name}_{id(candidate)}",
                    )
                    if checked:
                        selected_features.append(candidate.name)

            base_features = [f.strip() for f in edit_features.split(",") if f.strip()]
            edit_features = list(dict.fromkeys(base_features + selected_features))

        # AI Image Intelligence panel
        if st.session_state.image_intelligence:
            intelligence = st.session_state.image_intelligence
            st.markdown("---")
            st.subheader("🧠 AI Image Intelligence")

            intel_col1, intel_col2 = st.columns(2)

            with intel_col1:
                if intelligence.highlight_images:
                    st.markdown("**Selected for Social Posts**")
                    for idx, image_id in enumerate(intelligence.highlight_images, start=1):
                        ranked = next(
                            (img for img in intelligence.ranked_images if img.image_id == image_id),
                            None,
                        )
                        if ranked:
                            st.write(
                                f"{idx}. **{ranked.filename}** "
                                f"({ranked.room_type or 'unknown'}) — {ranked.reason}"
                            )

                if intelligence.hero_image_id:
                    st.markdown("**Hero Image**")
                    hero = next(
                        (img for img in intelligence.ranked_images if img.image_id == intelligence.hero_image_id),
                        None,
                    )
                    if hero:
                        st.write(
                            f"⭐ **{hero.filename}** "
                            f"({hero.room_type or 'unknown'}) — used to anchor email and video content"
                        )

            with intel_col2:
                if intelligence.highlights:
                    st.markdown("**Visual Highlights**")
                    for highlight in intelligence.highlights:
                        st.write(f"- {highlight.feature}")

            if intelligence.weak_images:
                st.warning(f"{len(intelligence.weak_images)} image(s) may be weaker for marketing.")

        # Photo comparison panel
        if details.images:
            st.markdown("---")
            st.subheader("📷 Photo Enhancement Preview")
            original_lookup = build_image_lookup(st.session_state.original_images or [])
            enhanced_lookup = build_image_lookup(st.session_state.enhanced_images or [])

            for img in details.images:
                st.markdown(f"**{img.filename}** — {img.metadata.room_type.replace('_', ' ').title()}")
                photo_col1, photo_col2 = st.columns(2)
                with photo_col1:
                    st.caption("Original")
                    original_bytes = original_lookup.get(img.filename)
                    if original_bytes:
                        st.image(original_bytes, use_container_width=True)
                with photo_col2:
                    st.caption("Enhanced")
                    enhanced_bytes = enhanced_lookup.get(img.filename)
                    if enhanced_bytes:
                        st.image(enhanced_bytes, use_container_width=True)
                if img.visible_features:
                    st.caption("Detected: " + ", ".join([f.name for f in img.visible_features]))
                st.divider()

        # Generate button
        st.markdown("---")
        generate_btn = st.button("Step 2: Generate Marketing Suite", type="primary", use_container_width=True)

        if generate_btn:
            st.session_state.extracted_details.address = edit_address.strip() or None
            st.session_state.extracted_details.city = edit_city.strip() or None
            st.session_state.extracted_details.state = edit_state.strip() or None
            st.session_state.extracted_details.postal_code = edit_postal_code.strip() or None
            st.session_state.extracted_details.community_name = edit_community_name.strip() or None
            st.session_state.extracted_details.subdivision_name = edit_subdivision_name.strip() or None
            st.session_state.extracted_details.list_price = int(edit_price or 0)
            st.session_state.extracted_details.bedrooms = int(edit_beds or 0)
            st.session_state.extracted_details.bathrooms = float(edit_baths or 0.0)

            if isinstance(edit_features, list):
                st.session_state.extracted_details.key_features = [
                    f.strip() for f in edit_features if f.strip()
                ]
            else:
                st.session_state.extracted_details.key_features = [
                    f.strip() for f in edit_features.split(",") if f.strip()
                ]

            with st.spinner("Generating your full listing campaign..."):
                try:
                    results = asyncio.run(
                        generate_marketing_assets_service(
                            st.session_state.extracted_details,
                            API_KEY,
                            email_tone,
                            image_intelligence=st.session_state.image_intelligence,
                        )
                    )
                    st.session_state.marketing_results = results
                except Exception as e:
                    st.error(f"Generation error: {e}")

    # --- Results ---
    if st.session_state.marketing_results:
        res = st.session_state.marketing_results
        campaign = res["email_campaign"]
        video_suite = res.get("video_scripts")
        enhanced_lookup = build_image_lookup(st.session_state.enhanced_images or [])

        st.success("✅ Campaign generated successfully!")
        st.divider()

        # MLS + CSV
        mls_col, csv_col = st.columns([4, 1])
        with mls_col:
            st.subheader("📋 MLS Description")
            st.info(res["mls_summary"])
        with csv_col:
            st.markdown("##### Export")
            if "reso_csv" in res:
                st.download_button(
                    label="⬇ MLS CSV",
                    data=res["reso_csv"],
                    file_name="listing_import.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        st.divider()

        # Social posts
        st.subheader("📣 Social Launch Pack")
        social_posts = res.get("social_posts", [])

        if social_posts:
            social_cols = st.columns(len(social_posts))
            for col, post in zip(social_cols, social_posts):
                with col:
                    render_social_post_card(post, enhanced_lookup)
        else:
            st.info("No social posts were generated.")

        st.divider()

        # Email campaign
        st.subheader(f"📧 Email Campaign — {email_tone} Tone")
        st.caption(
            "Four emails covering the full listing lifecycle. "
            "Fill in the **[DAYS ON MARKET]** and **[SOLD PRICE]** placeholders in the Just Sold email before sending."
        )

        email_tabs = st.tabs([
            "📬 Just Listed",
            "🏡 Open House",
            "💡 Why This Home",
            "🏆 Just Sold",
        ])

        with email_tabs[0]:
            render_email_card("Just Listed", campaign.just_listed, "just_listed")

        with email_tabs[1]:
            render_email_card("Open House", campaign.open_house, "open_house")

        with email_tabs[2]:
            render_email_card("Why This Home", campaign.why_this_home, "why_this_home")

        with email_tabs[3]:
            st.info(
                "✏️ Before sending, replace **[DAYS ON MARKET]** and **[SOLD PRICE]** "
                "with your actual results.",
                icon="📝",
            )
            render_email_card("Just Sold", campaign.just_sold, "just_sold")

        st.divider()

        # Video scripts
        if video_suite:
            st.subheader("🎬 Short Form Video Scripts")
            st.caption(
                "Three platform-native scripts with shot-by-shot directions. "
                "Film with your phone — no video experience required."
            )

            video_tabs = st.tabs([
                "📱 Instagram Reel",
                "🎵 TikTok",
                "▶️ YouTube Short",
            ])

            with video_tabs[0]:
                render_video_script_card(video_suite.reel, enhanced_lookup, "reel")

            with video_tabs[1]:
                render_video_script_card(video_suite.tiktok, enhanced_lookup, "tiktok")

            with video_tabs[2]:
                render_video_script_card(video_suite.youtube_short, enhanced_lookup, "youtube_short")

            st.divider()

        # Compliance review
        if "compliance_results" in res:
            with st.expander("⚖️ Fair Housing Compliance Review", expanded=False):
                st.caption(
                    "Every asset in your campaign has been reviewed for fair housing compliance. "
                    "Flagged or revised items should be reviewed before publishing."
                )
                st.markdown("---")

                compliance_cols = st.columns(3)
                for i, review in enumerate(res["compliance_results"]):
                    with compliance_cols[i % 3]:
                        render_compliance_badge(review)
                        st.markdown("---")

        # Source of truth expander
        with st.expander("📊 Final Data Used (Source of Truth)", expanded=False):
            if st.session_state.extracted_details:
                data = st.session_state.extracted_details
                truth_col1, truth_col2 = st.columns(2)
                with truth_col1:
                    st.write(f"**Address:** {data.address or 'N/A'}")
                    st.write(f"**City:** {data.city or 'N/A'}")
                    st.write(f"**State:** {data.state or 'N/A'}")
                    st.write(f"**Postal Code:** {data.postal_code or 'N/A'}")
                with truth_col2:
                    st.write(f"**Community:** {data.community_name or 'N/A'}")
                    st.write(f"**Subdivision:** {data.subdivision_name or 'N/A'}")
                    price_val = data.list_price
                    st.write(f"**Price:** ${price_val:,}" if price_val else "**Price:** N/A")
                    st.write(f"**Features:** {', '.join(data.key_features or [])}")
                st.markdown("---")
                st.text(res["reso_csv"])
            else:
                st.write("No data extracted yet.")