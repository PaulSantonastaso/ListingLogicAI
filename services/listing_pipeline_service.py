import asyncio
from typing import cast
from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from chains.email_chain import build_email_chain
from models.property_data import EmailCampaign, PropertyDetails, ListingDescriptionOutput, SocialPostOutput 

async def generate_listing_package_service(raw_notes: str, api_key: str, email_tone: str = "Professional"):
    # Initialize chains
    extraction_chain = build_extraction_chain(api_key)
    listing_chain = build_listing_description_chain(api_key)
    social_chain = build_social_post_chain(api_key)
    email_chain = build_email_chain(api_key)


    extracted_details = cast(PropertyDetails, await extraction_chain.ainvoke({"raw_notes": raw_notes}))

    property_details_json = extracted_details.model_dump_json(indent=2)

    listing_result = cast(ListingDescriptionOutput, await listing_chain.ainvoke({
        "property_details": property_details_json
    }))

    social_task = social_chain.ainvoke({
        "property_details": property_details_json,
        "mls_summary": listing_result.mls_summary 
    })

    email_task = email_chain.ainvoke({
        "mls_summary": listing_result.mls_summary,
        "email_tone": email_tone
    })

    social_res, email_res = await asyncio.gather(social_task, email_task)

    return {
        "extracted_details": extracted_details,
        "mls_summary": listing_result.mls_summary,
        "social_media_post": cast(SocialPostOutput, social_res).social_media_post,
        "email_campaign": cast(EmailCampaign, email_res)
    }