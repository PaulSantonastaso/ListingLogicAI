import streamlit as st
from services.listing_pipeline_service import generate_listing_package_service
from models.property_data import PropertyDetails

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Listing Pro AI",
    page_icon="🏠",
    layout="wide"
)

# --- 2. SIDEBAR (API KEY) ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Your key is used only for this session.")

# --- 3. MAIN INTERFACE ---
st.title("🏠 Real Estate Marketing Suite")
st.markdown("Transform messy notes into professional listings.")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
    st.stop()

tab_text, tab_photo = st.tabs(["📝 Listing Generator", "📸 Photo Enhancer"])

with tab_text:
    user_notes = st.text_area(
        "Agent Notes",
        placeholder="3 bed, 2 bath, updated kitchen...",
        height=150
    )

    if st.button("Generate Listing Package", type="primary"):
        if not user_notes.strip():
            st.warning("Please enter agent notes.")
        else:
            with st.spinner("Writing listing..."):
                try:
                    # 2. FIX: The service returns a DICT, not a single 'ListingOutput' object
                    result = generate_listing_package_service(user_notes, api_key)
                    
                    # Since it's a dict, use ['key'] or .get('key')
                    mls_text = result["mls_summary"]
                    social_text = result["social_media_post"]
                    details: PropertyDetails = result["extracted_details"]

                    st.success("Listing Generated Successfully!")
                    st.divider()

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("MLS Description")
                        st.info(mls_text)

                    with col2:
                        st.subheader("Social Media Post")
                        st.success(social_text)

                    # 4. Show the extracted data
                    with st.expander("📊 Extracted Property Details"):
                        st.write(f"**Address:** {details.address}")
                        st.write(f"**Price:** ${details.list_price:,}" if details.list_price else "Price: N/A")
                        st.write(f"**Features:** {', '.join(details.key_features)}")
                    
                    st.session_state["features"] = details.key_features

                except Exception as e:
                    st.error(f"Error: {e}")

with tab_photo:
    st.info("Photo enhancement is coming next.")