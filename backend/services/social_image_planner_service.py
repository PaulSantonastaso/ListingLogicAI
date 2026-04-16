from pydantic import BaseModel, Field
from typing import List, Optional

from models.image_intelligence import ImageIntelligence, RankedImage


class PlannedSocialImage(BaseModel):
    platform: str = Field(
        description="Target platform such as Facebook or Instagram"
    )
    slot_name: str = Field(
        description="Planned slot name such as facebook_feed, instagram_post_1, or instagram_post_2"
    )
    image_id: str = Field(
        description="Selected image ID for this social slot"
    )
    image_filename: str = Field(
        description="Filename of the selected image"
    )
    recommended_aspect_ratio: str = Field(
        description="Recommended aspect ratio for this platform slot"
    )
    crop_guidance: str = Field(
        description="Brief crop or framing guidance for the selected image"
    )
    room_type: Optional[str] = Field(
        default=None,
        description="Primary room or scene shown in the selected image"
    )
    visible_features: List[str] = Field(
        default_factory=list,
        description="Key visible features shown in the selected image"
    )


def _build_crop_guidance(image: RankedImage) -> str:
    room_type = image.room_type or "space"

    if room_type == "front_exterior":
        return "Keep the full front elevation centered and avoid tight crops that cut off the roofline, entry, or driveway."
    if room_type in {"back_exterior", "backyard", "patio"}:
        return "Keep the entertaining area centered and avoid cropping out major outdoor features."
    if room_type == "kitchen":
        return "Preserve the full kitchen layout and avoid tight crops that remove cabinetry, island, or countertops."
    if room_type == "pool":
        return "Frame the full pool and spa. Keep the screen enclosure visible to show the full outdoor oasis."
    if room_type == "living_room":
        return "Keep the room wide and balanced so the layout and natural light remain clear."
    if room_type == "dining_room":
        return "Frame the full dining area and preserve the sense of openness."
    if room_type == "bedroom":
        return "Center the room and avoid cropping out windows or major furniture anchors."
    if room_type == "bathroom":
        return "Keep the vanity, shower, or tub visible and avoid awkward tight crops."
    if room_type == "office":
        return "Preserve the work area context and keep the composition clean and balanced."

    return "Use a balanced crop that preserves the main subject and avoids cutting off key features."


def _pick_best_by_room(
    ranked_images: List[RankedImage],
    excluded_image_ids: set[str],
    preferred_room_types: List[str],
) -> Optional[RankedImage]:
    for room_type in preferred_room_types:
        for image in ranked_images:
            if image.image_id in excluded_image_ids:
                continue
            if image.room_type == room_type:
                return image
    return None


def _pick_next_best(
    ranked_images: List[RankedImage],
    excluded_image_ids: set[str],
) -> Optional[RankedImage]:
    for image in ranked_images:
        if image.image_id not in excluded_image_ids:
            return image
    return None


def build_social_image_plan(image_intelligence: Optional[ImageIntelligence]) -> List[PlannedSocialImage]:
    if not image_intelligence or not image_intelligence.ranked_images:
        return []

    ranked_images = image_intelligence.ranked_images
    selected_slots: List[PlannedSocialImage] = []
    used_image_ids: set[str] = set()

    facebook_image = _pick_best_by_room(
        ranked_images,
        excluded_image_ids=used_image_ids,
        preferred_room_types=["front_exterior", "pool", "back_exterior", "backyard", "patio", "living_room", "kitchen"],
    ) or _pick_next_best(ranked_images, excluded_image_ids=used_image_ids)

    if facebook_image:
        used_image_ids.add(facebook_image.image_id)
        selected_slots.append(
            PlannedSocialImage(
                platform="Facebook",
                slot_name="facebook_feed",
                image_id=facebook_image.image_id,
                image_filename=facebook_image.filename,
                recommended_aspect_ratio="1.91:1",
                crop_guidance=_build_crop_guidance(facebook_image),
                room_type=facebook_image.room_type,
                visible_features=facebook_image.visible_features,
            )
        )

    instagram_post_1 = _pick_best_by_room(
        ranked_images,
        excluded_image_ids=used_image_ids,
        preferred_room_types=["kitchen", "living_room", "front_exterior", "back_exterior", "patio", "backyard"],
    ) or _pick_next_best(ranked_images, excluded_image_ids=used_image_ids)

    if instagram_post_1:
        used_image_ids.add(instagram_post_1.image_id)
        selected_slots.append(
            PlannedSocialImage(
                platform="Instagram",
                slot_name="instagram_post_1",
                image_id=instagram_post_1.image_id,
                image_filename=instagram_post_1.filename,
                recommended_aspect_ratio="4:5",
                crop_guidance=_build_crop_guidance(instagram_post_1),
                room_type=instagram_post_1.room_type,
                visible_features=instagram_post_1.visible_features,
            )
        )

    instagram_post_2 = _pick_best_by_room(
        ranked_images,
        excluded_image_ids=used_image_ids,
        preferred_room_types=["backyard", "patio", "living_room", "kitchen", "bedroom", "bathroom"],
    ) or _pick_next_best(ranked_images, excluded_image_ids=used_image_ids)

    if instagram_post_2:
        used_image_ids.add(instagram_post_2.image_id)
        selected_slots.append(
            PlannedSocialImage(
                platform="Instagram",
                slot_name="instagram_post_2",
                image_id=instagram_post_2.image_id,
                image_filename=instagram_post_2.filename,
                recommended_aspect_ratio="4:5",
                crop_guidance=_build_crop_guidance(instagram_post_2),
                room_type=instagram_post_2.room_type,
                visible_features=instagram_post_2.visible_features,
            )
        )

    return selected_slots