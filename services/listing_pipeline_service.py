from typing import cast
from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from models.property_data import PropertyDetails, ListingDescriptionOutput, SocialPostOutput 

def generate_listing_package_service(raw_notes: str, api_key: str):
    # Initialize chains
    extraction_chain = build_extraction_chain(api_key)
    listing_chain = build_listing_description_chain(api_key)
    social_chain = build_social_post_chain(api_key)

    extracted_details = cast(PropertyDetails, extraction_chain.invoke({"raw_notes": raw_notes}))

    property_details_json = extracted_details.model_dump_json(indent=2)

    listing_result = cast(ListingDescriptionOutput, listing_chain.invoke({
        "property_details": property_details_json
    }))

    social_result = cast(SocialPostOutput, social_chain.invoke({
        "property_details": property_details_json,
        "mls_summary": listing_result.mls_summary 
    }))

    return {
        "extracted_details": extracted_details,
        "mls_summary": listing_result.mls_summary,
        "social_media_post": social_result.social_media_post,
    }