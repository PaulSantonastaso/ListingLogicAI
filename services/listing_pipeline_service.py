import asyncio
from typing import Optional, cast

from chains.extraction_chain import build_extraction_chain
from chains.listing_description_chain import build_listing_description_chain
from chains.social_post_chain import build_social_post_chain
from chains.email_chain import build_email_chain, _format_hero_image_context
from chains.video_script_chain import build_video_script_chain, _format_shot_list, _format_hero_image_context as _format_hero_image_context_video
from models.property_data import CampaignEmail, EmailCampaign, PropertyDetails, ListingDescriptionOutput, SocialPostOutput
from models.video_script import VideoScriptSuite
from services.visual_summary_service import build_visual_summary
from services.compliance_service import ComplianceService
from services.listing_mapper_service import map_property_to_listing_details
from services.reso_csv_service import build_reso_csv_string
from models.image_intelligence import ImageIntelligence
from services.social_image_planner_service import build_social_image_plan
from services.video_shot_planner_service import build_video_shot_plan


async def extract_property_data_service(raw_notes: str, api_key: str) -> PropertyDetails:
    extraction_chain = build_extraction_chain(api_key)
    extracted_details = await extraction_chain.ainvoke({"raw_notes": raw_notes})
    return cast(PropertyDetails, extracted_details)


async def generate_marketing_assets_service(
    details: PropertyDetails,
    api_key: str,
    email_tone: str = "Professional",
    image_intelligence: Optional[ImageIntelligence] = None,
    photos_count: Optional[int] = None,
):
    listing_chain = build_listing_description_chain(api_key)
    social_chain = build_social_post_chain(api_key)
    email_chain = build_email_chain(api_key)
    video_chain = build_video_script_chain(api_key)
    compliance_service = ComplianceService(api_key)

    property_details_json = details.model_dump_json(indent=2)
    visual_summary = build_visual_summary(details)

    # --- MLS description runs first — feeds into all downstream chains ---
    listing_result = await listing_chain.ainvoke({
        "property_details": property_details_json,
        "visual_summary": visual_summary,
    })
    listing_output = cast(ListingDescriptionOutput, listing_result)

    # --- Build image-informed plans ---
    social_plan = build_social_image_plan(image_intelligence)
    video_shot_plan = build_video_shot_plan(image_intelligence)

    # --- Hero image context for email and video chains ---
    hero_image_context_email = _format_hero_image_context(image_intelligence)
    hero_image_context_video = _format_hero_image_context_video(image_intelligence)
    shot_list_str = _format_shot_list(video_shot_plan)

    # --- Social tasks ---
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

    # --- Email task ---
    email_task = email_chain.ainvoke({
        "mls_summary": listing_output.mls_summary,
        "email_tone": email_tone,
        "visual_summary": visual_summary,
        "hero_image_context": hero_image_context_email,
    })

    # --- Video task ---
    video_task = video_chain.ainvoke({
        "property_details": property_details_json,
        "mls_summary": listing_output.mls_summary,
        "visual_summary": visual_summary,
        "shot_list": shot_list_str,
        "hero_image_context": hero_image_context_video,
    })

    # --- Run social, email, and video in parallel ---
    results = await asyncio.gather(*social_tasks, email_task, video_task)

    social_posts: list[SocialPostOutput] = [cast(SocialPostOutput, r) for r in results[:-2]]
    email_output = cast(EmailCampaign, results[-2])
    video_output = cast(VideoScriptSuite, results[-1])

    # --- Build compliance asset map ---
    assets: dict[str, str] = {
        "mls_summary": listing_output.mls_summary,
    }

    # All social posts
    for i, post in enumerate(social_posts):
        platform = (post.platform or "social").lower().replace(" ", "_")
        slot = post.slot_name or f"post_{i + 1}"
        assets[f"social_{platform}_{slot}"] = post.social_media_post

    # All 4 campaign emails — subject + body reviewed independently
    assets["email_just_listed_subject"] = email_output.just_listed.subject
    assets["email_just_listed_body"] = email_output.just_listed.body
    assets["email_open_house_subject"] = email_output.open_house.subject
    assets["email_open_house_body"] = email_output.open_house.body
    assets["email_why_this_home_subject"] = email_output.why_this_home.subject
    assets["email_why_this_home_body"] = email_output.why_this_home.body
    assets["email_just_sold_subject"] = email_output.just_sold.subject
    assets["email_just_sold_body"] = email_output.just_sold.body

    # All 3 video scripts — hook + voiceover reviewed independently
    assets["video_reel_hook"] = video_output.reel.hook
    assets["video_reel_voiceover"] = video_output.reel.voiceover
    assets["video_tiktok_hook"] = video_output.tiktok.hook
    assets["video_tiktok_voiceover"] = video_output.tiktok.voiceover
    assets["video_youtube_short_hook"] = video_output.youtube_short.hook
    assets["video_youtube_short_voiceover"] = video_output.youtube_short.voiceover

    # --- Run all compliance checks in parallel ---
    compliance_results = await compliance_service.review_assets(assets)

    # --- Apply compliant text back to outputs ---
    final_mls_summary = compliance_results["mls_summary"].compliant_text

    for i, post in enumerate(social_posts):
        platform = (post.platform or "social").lower().replace(" ", "_")
        slot = post.slot_name or f"post_{i + 1}"
        key = f"social_{platform}_{slot}"
        if key in compliance_results:
            post.social_media_post = compliance_results[key].compliant_text

    compliant_campaign = EmailCampaign(
        just_listed=CampaignEmail(
            subject=compliance_results["email_just_listed_subject"].compliant_text,
            body=compliance_results["email_just_listed_body"].compliant_text,
            preview_text=email_output.just_listed.preview_text,
        ),
        open_house=CampaignEmail(
            subject=compliance_results["email_open_house_subject"].compliant_text,
            body=compliance_results["email_open_house_body"].compliant_text,
            preview_text=email_output.open_house.preview_text,
        ),
        why_this_home=CampaignEmail(
            subject=compliance_results["email_why_this_home_subject"].compliant_text,
            body=compliance_results["email_why_this_home_body"].compliant_text,
            preview_text=email_output.why_this_home.preview_text,
        ),
        just_sold=CampaignEmail(
            subject=compliance_results["email_just_sold_subject"].compliant_text,
            body=compliance_results["email_just_sold_body"].compliant_text,
            preview_text=email_output.just_sold.preview_text,
        ),
    )

    # --- Apply compliant text back to video scripts ---
    video_output.reel.hook = compliance_results["video_reel_hook"].compliant_text
    video_output.reel.voiceover = compliance_results["video_reel_voiceover"].compliant_text
    video_output.tiktok.hook = compliance_results["video_tiktok_hook"].compliant_text
    video_output.tiktok.voiceover = compliance_results["video_tiktok_voiceover"].compliant_text
    video_output.youtube_short.hook = compliance_results["video_youtube_short_hook"].compliant_text
    video_output.youtube_short.voiceover = compliance_results["video_youtube_short_voiceover"].compliant_text

    listing_details = map_property_to_listing_details(
        details,
        public_remarks=final_mls_summary,
        photos_count=photos_count,
    )

    reso_csv = build_reso_csv_string(listing_details)

    return {
        "mls_summary": final_mls_summary,
        "social_media_post": social_posts[0].social_media_post if social_posts else "",
        "social_posts": social_posts,
        "social_image_plan": social_plan,
        "email_campaign": compliant_campaign,
        "video_scripts": video_output,
        "compliance_results": list(compliance_results.values()),
        "listing_details": listing_details,
        "reso_csv": reso_csv,
    }