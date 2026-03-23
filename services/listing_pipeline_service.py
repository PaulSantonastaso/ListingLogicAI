import asyncio
from typing import cast
from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from chains.email_chain import build_email_chain
from models.property_data import EmailCampaign, PropertyDetails, ListingDescriptionOutput, SocialPostOutput


async def extract_property_data_service(raw_notes: str, api_key: str) -> PropertyDetails:
    extraction_chain = build_extraction_chain(api_key)
    
    extracted_details = await extraction_chain.ainvoke({"raw_notes": raw_notes})
    
    return cast(PropertyDetails, extracted_details)

async def generate_marketing_assets_service(details: PropertyDetails, api_key: str, email_tone: str = "Professional"):
    listing_chain = build_listing_description_chain(api_key)
    social_chain = build_social_post_chain(api_key)
    email_chain = build_email_chain(api_key)

    property_details_json = details.model_dump_json(indent=2)

    listing_result = await listing_chain.ainvoke({
        "property_details": property_details_json
    })
    listing_output = cast(ListingDescriptionOutput, listing_result)

    social_task = social_chain.ainvoke({
        "property_details": property_details_json,
        "mls_summary": listing_output.mls_summary 
    })

    email_task = email_chain.ainvoke({
        "mls_summary": listing_output.mls_summary,
        "email_tone": email_tone
    })

    social_res, email_res = await asyncio.gather(social_task, email_task)

    return {
        "mls_summary": listing_output.mls_summary,
        "social_media_post": cast(SocialPostOutput, social_res).social_media_post,
        "email_campaign": cast(EmailCampaign, email_res)
    }