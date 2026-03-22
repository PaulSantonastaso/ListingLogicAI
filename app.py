import asyncio
import streamlit as st
from services.listing_pipeline_service import (
    extract_property_data_service, 
    generate_marketing_assets_service
)
from models.property_data import PropertyDetails

if "extracted_details" not in st.session_state:
    st.session_state.extracted_details = None

if "marketing_results" not in st.session_state:
    st.session_state.marketing_results = None

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
    user_notes = st.text_area(
        "Agent Notes",
        placeholder="Enter property details, upgrades, and neighborhood info here...",
        height=150
    )

    if st.button("Step 1: Extract Details for Review", type="secondary"):
        if not user_notes.strip():
            st.warning("Please enter agent notes.")
        else:
            with st.spinner("AI is extracting facts..."):
                try:
                    # Run just the extraction chain
                    details = asyncio.run(extract_property_data_service(user_notes, api_key))
                    st.session_state.extracted_details = details
                    # Clear old results when starting a new extraction
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

        if st.button("Step 2: Generate Marketing Suite", type="primary"):
            # Manually sync the widget values back to the session state object
            st.session_state.extracted_details.address = edit_address
            st.session_state.extracted_details.list_price = int(edit_price or 0)
            st.session_state.extracted_details.bedrooms = int(edit_beds or 0)
            st.session_state.extracted_details.bathrooms = float(edit_baths or 0.0)
            st.session_state.extracted_details.key_features = [f.strip() for f in edit_features.split(",") if f.strip()]

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

with tab_photo:
    st.info("Photo enhancement is currently in development.")