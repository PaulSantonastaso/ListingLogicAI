import asyncio
from typing import Optional, cast
from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from chains.email_chain import build_email_chain
from models.property_data import EmailCampaign, PropertyDetails, ListingDescriptionOutput, SocialPostOutput
from services.visual_summary_service import build_visual_summary
from services.compliance_service import ComplianceService
from services.listing_mapper_service import map_property_to_listing_details
from services.reso_csv_service import build_reso_csv_string
from models.image_intelligence import ImageIntelligence
from services.social_image_planner_service import build_social_image_plan


async def extract_property_data_service(raw_notes: str, api_key: str) -> PropertyDetails:
    extraction_chain = build_extraction_chain(api_key)
    
    extracted_details = await extraction_chain.ainvoke({"raw_notes": raw_notes})
    
    return cast(PropertyDetails, extracted_details)


async def generate_marketing_assets_service(
    details: PropertyDetails,
    api_key: str,
    email_tone: str = "Professional",
    image_intelligence: Optional[ImageIntelligence] = None,
):
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

    social_posts: list[SocialPostOutput] = []
    social_plan = build_social_image_plan(image_intelligence)

    if social_plan:
        social_tasks = [
            social_chain.ainvoke({
                "property_details": property_details_json,
                "mls_summary": listing_output.mls_summary,
                "visual_summary": visual_summary,
                "platform": slot.platform,
                "slot_name": slot.slot_name,
                "image_id": slot.image_id,
                "image_filename": slot.image_filename,
                "recommended_aspect_ratio": slot.recommended_aspect_ratio,
                "crop_guidance": slot.crop_guidance,
                "room_type": slot.room_type or "",
                "visible_features": ", ".join(slot.visible_features),
            })
            for slot in social_plan
        ]
    else:
        social_tasks = [
            social_chain.ainvoke({
                "property_details": property_details_json,
                "mls_summary": listing_output.mls_summary,
                "visual_summary": visual_summary,
                "platform": "Facebook",
                "slot_name": "fallback_social_post",
                "image_id": "",
                "image_filename": "",
                "recommended_aspect_ratio": "1.91:1",
                "crop_guidance": "No selected image is available. Write a strong property-level post grounded only in the provided listing information.",
                "room_type": "",
                "visible_features": "",
            })
        ]

    email_task = email_chain.ainvoke({
        "mls_summary": listing_output.mls_summary,
        "email_tone": email_tone,
        "visual_summary": visual_summary,
    })

    results = await asyncio.gather(*social_tasks, email_task)
    social_results = results[:-1]
    email_res = results[-1]

    listing_details = map_property_to_listing_details(
        details,
        public_remarks=listing_output.mls_summary,
    )

    reso_csv = build_reso_csv_string(listing_details)

    social_posts = [cast(SocialPostOutput, result) for result in social_results]
    email_output = cast(EmailCampaign, email_res)

    primary_social_post = social_posts[0].social_media_post if social_posts else ""

    compliance_results = await compliance_service.review_assets({
        "mls_summary": listing_output.mls_summary,
        "social_media_post": primary_social_post,
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

    if social_posts:
        social_posts[0].social_media_post = compliance_results["social_media_post"].compliant_text

    return {
        "mls_summary": compliance_results["mls_summary"].compliant_text,
        "social_media_post": social_posts[0].social_media_post if social_posts else "",
        "social_posts": social_posts,
        "social_image_plan": social_plan,
        "email_campaign": EmailCampaign(
            subject=compliance_results["email_subject"].compliant_text,
            body=compliance_results["email_body"].compliant_text,
            preview_text=compliance_results["email_preview_text"].compliant_text,
        ),
        "compliance_results": list(compliance_results.values()),
        "listing_details": listing_details,
        "reso_csv": reso_csv,
    }