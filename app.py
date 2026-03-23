import asyncio
import streamlit as st
import hashlib
from services.listing_pipeline_service import (
    extract_property_data_service, 
    generate_marketing_assets_service
)
from models.property_data import PropertyDetails
from services.image_analysis_service import analyze_property_images
from services.fusion_service import merge_image_features_into_property
from services.image_enhancement_service import enhance_listing_photos

def build_uploaded_image_fingerprint(uploaded_files) -> str:
    """
    Build a stable fingerprint for the currently uploaded files.
    """
    hasher = hashlib.sha256()

    for file in uploaded_files:
        file_bytes = file.getvalue()
        hasher.update(file.name.encode("utf-8"))
        hasher.update(file_bytes)

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
        grouped[room].sort(
            key=lambda x: x.confidence,
            reverse=True
        )

    return grouped

def build_image_lookup(images):
    if not images:
        return {}
    return {filename: image_bytes for image_bytes, filename in images}

if "extracted_details" not in st.session_state:
    st.session_state.extracted_details = None

if "marketing_results" not in st.session_state:
    st.session_state.marketing_results = None

if "analyzed_images" not in st.session_state:
    st.session_state.analyzed_images = None

if "uploaded_image_fingerprint" not in st.session_state:
    st.session_state.uploaded_image_fingerprint = None

if "original_images" not in st.session_state:
    st.session_state.original_images = None

if "enhanced_images" not in st.session_state:
    st.session_state.enhanced_images = None

st.set_page_config(
    page_title="ListingLogicAI",
    page_icon="🏠",
    layout="wide"
)

with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.info("Your key is used only for this session.")
    
    st.divider()
    st.header("Customization")

    email_tone = st.selectbox(
        "Email Tone",
        ["Professional", "Luxury", "Casual", "Urgent"],
        index=0,
        help="Select the 'voice' for the lead-gen email campaign."
    )    


st.title("🏠 ListingLogicAI")
st.markdown("Transform messy notes into professional multi-channel marketing.")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
    st.stop()

tab_text, tab_photo = st.tabs(["📝 Listing Generator", "📸 Photo Enhancer"])

with tab_text:
    uploaded_images = st.file_uploader(
        "Upload Property Photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload photos you took at the property to enhance the marketing content."
    )

    user_notes = st.text_area(
        "Agent Notes",
        placeholder="Enter property details, upgrades, and neighborhood info here...",
        height=150
    )

    if st.button("Step 1: Extract Details for Review", type="secondary"):
        if not user_notes.strip():
            st.warning("Please enter agent notes.")
        else:
            with st.spinner("AI is extracting facts and analyzing photos..."):
                try:
                    details = asyncio.run(extract_property_data_service(user_notes, api_key))

                    if uploaded_images:
                        current_fingerprint = build_uploaded_image_fingerprint(uploaded_images)

                        if (
                            st.session_state.analyzed_images is None
                            or st.session_state.uploaded_image_fingerprint != current_fingerprint
                        ):

                            images = []

                            for file in uploaded_images:
                                image_bytes = file.getvalue()
                                images.append((image_bytes, file.name))

                            st.session_state.original_images = images
                            enhanced_images = enhance_listing_photos(images)
                            st.session_state.enhanced_images = enhanced_images
                            # debugging line to check the number of enhanced images
                            st.caption(f"Enhanced {len(enhanced_images)} images")

                            analyzed_images = asyncio.run(
                                analyze_property_images(enhanced_images, api_key)
                            )
                            st.session_state.analyzed_images = analyzed_images
                            st.session_state.uploaded_image_fingerprint = current_fingerprint

                        if st.session_state.analyzed_images:
                            details = merge_image_features_into_property(
                                details,
                                st.session_state.analyzed_images
                            )

                    st.session_state.extracted_details = details
                    st.session_state.marketing_results = None

                except Exception as e:
                    st.error(f"Extraction Error: {e}")

    # Only displays if we have successfully extracted data
    if st.session_state.extracted_details is not None:
        st.divider()
        st.subheader("🛠 Verify & Edit Property Details")
        st.caption("Confirm these details are correct before generating marketing copy.")

        col1, col2 = st.columns(2)
        with col1:
            edit_address = st.text_input("Address", value=st.session_state.extracted_details.address)
            edit_price = st.number_input("List Price", value=int(st.session_state.extracted_details.list_price or 0))
        with col2:
            edit_beds = st.number_input("Beds", value=st.session_state.extracted_details.bedrooms)
            edit_baths = st.number_input("Baths", value=float(st.session_state.extracted_details.bathrooms or 0))
        
        edit_features = st.text_area(
            "Key Features (comma separated)", 
            value=", ".join(st.session_state.extracted_details.key_features)
        )

        details = st.session_state.extracted_details

        if details.feature_candidates:
            st.subheader("🔍 Image-Detected Features")

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
                        key=f"feature_{room}_{candidate.name}_{id(candidate)}"
                    )

                    if checked:
                        selected_features.append(candidate.name)

            base_features = [f.strip() for f in edit_features.split(",") if f.strip()]
            edit_features = list(dict.fromkeys(base_features + selected_features))

        if details.images:
            st.subheader("📷 Uploaded Photos")

            original_lookup = build_image_lookup(st.session_state.original_images or [])
            enhanced_lookup = build_image_lookup(st.session_state.enhanced_images or [])

            for img in details.images:
                st.markdown(f"### {img.filename}")
                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("Original")
                    original_bytes = original_lookup.get(img.filename)
                    if original_bytes:
                        st.image(original_bytes, use_container_width=True)

                with col2:
                    st.caption("Enhanced")
                    enhanced_bytes = enhanced_lookup.get(img.filename)
                    if enhanced_bytes:
                        st.image(enhanced_bytes, use_container_width=True)

                st.caption(img.metadata.room_type.replace("_", " ").title())
                st.write(img.description)

                if img.visible_features:
                    feature_text = ", ".join([f.name for f in img.visible_features])
                    st.write(f"**Detected features:** {feature_text}")

                st.divider()

        if st.button("Step 2: Generate Marketing Suite", type="primary"):
            # Manually sync the widget values back to the session state object
            st.session_state.extracted_details.address = edit_address
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

            with st.spinner("Generating marketing assets from your edits..."):
                try:
                    # Run the Parallel Async marketing chains
                    results = asyncio.run(generate_marketing_assets_service(
                        st.session_state.extracted_details,
                        api_key,
                        email_tone
                    ))
                    st.session_state.marketing_results = results
                except Exception as e:
                    st.error(f"Generation Error: {e}")

    # This block is now outside of any button logic, so the results stay visible
    if st.session_state.marketing_results:
        res = st.session_state.marketing_results
        details = st.session_state.extracted_details
        
        st.success("Campaign Generated Successfully!")
        st.divider()

        col_mls, col_soc = st.columns(2)
        with col_mls:
            st.subheader("📋 MLS Description")
            st.info(res["mls_summary"])

        with col_soc:
            st.subheader("📱 Social Media Post")
            st.success(res["social_media_post"])

        st.divider()
        email_data = res["email_campaign"]
        st.subheader(f"📧 Lead-Gen Email ({email_tone} Tone)")
        
        email_col1, email_col2 = st.columns([1, 2])
        with email_col1:
            st.markdown(f"**Subject:** {email_data.subject}")
            st.caption(f"Preview: {email_data.preview_text}")
        with email_col2:
            st.text_area("Email Body", value=email_data.body, height=300)

        with st.expander("📊 Final Data Used (Source of Truth)"):
            # Always check if the object exists before accessing attributes
            if st.session_state.extracted_details:
                data = st.session_state.extracted_details
                st.write(f"**Address:** {data.address}")
                
                # Use a safe getter for price to avoid formatting NoneType
                price_val = data.list_price
                st.write(f"**Price:** ${price_val:,}" if price_val else "Price: N/A")
                
                # Ensure key_features is a list before joining
                features = data.key_features or []
                st.write(f"**Features:** {', '.join(features)}")
            else:
                st.write("No data extracted yet.")