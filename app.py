import streamlit as st
from services.listing_pipeline_service import generate_listing_package_service
from models.property_data import PropertyDetails

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="ListingLogicAI",
    page_icon="🏠",
    layout="wide"
)

# --- 2. SIDEBAR (API KEY & SETTINGS) ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.info("Your key is used only for this session.")
    
    st.divider()
    st.header("Customization")
    # NEW: Tone selection for the email chain
    email_tone = st.selectbox(
        "Email Tone",
        ["Professional", "Luxury", "Casual", "Urgent"],
        index=0,
        help="Select the 'voice' for the lead-gen email campaign."
    )
    

# --- 3. MAIN INTERFACE ---
st.title("🏠 ListingLogicAI")
st.markdown("Transform messy notes into professional multi-channel marketing.")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
    st.stop()

tab_text, tab_photo = st.tabs(["📝 Listing Generator", "📸 Photo Enhancer"])

with tab_text:
    user_notes = st.text_area(
        "Agent Notes",
        placeholder="Enter property details, upgrades, and neighborhood info here...",
        height=150
    )

    if st.button("Generate Marketing Suite", type="primary"):
        if not user_notes.strip():
            st.warning("Please enter agent notes.")
        else:
            with st.spinner("Analyzing data and writing copy..."):
                try:
                    # Pass the email_tone to your service
                    result = generate_listing_package_service(user_notes, api_key, email_tone)
                    
                    # Unpack the results from your service dictionary
                    mls_text = result["mls_summary"]
                    social_text = result["social_media_post"]
                    email_data = result["email_campaign"] # This is your new EmailCampaign object
                    details: PropertyDetails = result["extracted_details"]

                    st.success("Campaign Generated Successfully!")
                    st.divider()

                    # --- ROW 1: MLS & SOCIAL ---
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📋 MLS Description")
                        st.info(mls_text)

                    with col2:
                        st.subheader("📱 Social Media Post")
                        st.success(social_text)

                    # --- ROW 2: LEAD-GEN EMAIL ---
                    st.divider()
                    st.subheader(f"📧 Lead-Gen Email ({email_tone} Tone)")
                    
                    email_col1, email_col2 = st.columns([1, 2])
                    with email_col1:
                        st.markdown(f"**Subject:** {email_data.subject}")
                        st.caption(f"Preview: {email_data.preview_text}")
                    with email_col2:
                        st.text_area("Email Body", value=email_data.body, height=300)

                    # --- ROW 3: DATA VERIFICATION ---
                    with st.expander("📊 Extracted Data Source of Truth"):
                        st.write(f"**Address:** {details.address}")
                        st.write(f"**Price:** ${details.list_price:,}" if details.list_price else "Price: N/A")
                        st.write(f"**Features:** {', '.join(details.key_features)}")
                    
                    st.session_state["features"] = details.key_features

                except Exception as e:
                    st.error(f"Error: {e}")

with tab_photo:
    st.info("Photo enhancement is currently in development.")