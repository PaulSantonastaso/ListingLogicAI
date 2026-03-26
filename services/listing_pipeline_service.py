import asyncio
from typing import cast
from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from chains.email_chain import build_email_chain
from models import listing_details
from models.property_data import EmailCampaign, PropertyDetails, ListingDescriptionOutput, SocialPostOutput
from services.visual_summary_service import build_visual_summary
from services.compliance_service import ComplianceService
from services.listing_mapper_service import map_property_to_listing_details
from services.reso_csv_service import build_reso_csv_string


async def extract_property_data_service(raw_notes: str, api_key: str) -> PropertyDetails:
    extraction_chain = build_extraction_chain(api_key)
    
    extracted_details = await extraction_chain.ainvoke({"raw_notes": raw_notes})
    
    return cast(PropertyDetails, extracted_details)


async def generate_marketing_assets_service(details: PropertyDetails, api_key: str, email_tone: str = "Professional"):
    listing_chain = build_listing_description_chain(api_key)
    social_chain = build_social_post_chain(api_key)
    email_chain = build_email_chain(api_key)
    compliance_service = ComplianceService(api_key)

    property_details_json = details.model_dump_json(indent=2)
    visual_summary = build_visual_summary(details)

    listing_result = await listing_chain.ainvoke({
        "property_details": property_details_json,
        "visual_summary": visual_summary
    })
    listing_output = cast(ListingDescriptionOutput, listing_result)

    social_task = social_chain.ainvoke({
        "property_details": property_details_json,
        "mls_summary": listing_output.mls_summary,
        "visual_summary": visual_summary
    })

    email_task = email_chain.ainvoke({
        "mls_summary": listing_output.mls_summary,
        "email_tone": email_tone,
        "visual_summary": visual_summary,
    })

    social_res, email_res = await asyncio.gather(social_task, email_task)

    listing_details = map_property_to_listing_details(
        details,
        public_remarks=listing_output.mls_summary,
    )

    reso_csv = build_reso_csv_string(listing_details)

    social_output = cast(SocialPostOutput, social_res)
    email_output = cast(EmailCampaign, email_res)

    compliance_results = await compliance_service.review_assets({
        "mls_summary": listing_output.mls_summary,
        "social_media_post": social_output.social_media_post,
        "email_subject": email_output.subject,
        "email_body": email_output.body,
        "email_preview_text": email_output.preview_text,
    })

    final_mls_summary = compliance_results["mls_summary"].compliant_text

    listing_details = map_property_to_listing_details(
        details,
        public_remarks=final_mls_summary,
    )

    reso_csv = build_reso_csv_string(listing_details)

    return {
        "mls_summary": compliance_results["mls_summary"].compliant_text,
        "social_media_post": compliance_results["social_media_post"].compliant_text,
        "email_campaign": EmailCampaign(
            subject=compliance_results["email_subject"].compliant_text,
            body=compliance_results["email_body"].compliant_text,
            preview_text=compliance_results["email_preview_text"].compliant_text,
        ),
        "compliance_results": list(compliance_results.values()),
        "listing_details": listing_details,
        "reso_csv": reso_csv,
    }