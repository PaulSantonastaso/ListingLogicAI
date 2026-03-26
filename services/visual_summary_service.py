from typing import List
from models.property_data import PropertyDetails


ROOM_PRIORITY = {
    "front_exterior": 1,
    "living_room": 2,
    "kitchen": 3,
    "dining_room": 4,
    "primary_bedroom": 5,
    "bedroom": 6,
    "bathroom": 7,
    "office": 8,
    "patio": 9,
    "backyard": 10,
    "pool": 11,
    "back_exterior": 12,
    "garage": 13,
    "other": 99,
}


def _room_priority(room_type: str) -> int:
    return ROOM_PRIORITY.get(room_type, 99)


def build_visual_summary(details: PropertyDetails) -> str:
    """
    Build a concise, marketing-focused visual summary from
    marketing-worthy listing images only.
    """
    if not details.images:
        return ""

    worthy_images = [
        img for img in details.images
        if img.metadata.likely_marketing_worthy is True
    ]

    if not worthy_images:
        return ""

    worthy_images = sorted(
        worthy_images,
        key=lambda img: _room_priority(img.metadata.room_type)
    )

    lines: List[str] = []

    for img in worthy_images:
        room = img.metadata.room_type.replace("_", " ").title()

        features = [f.name for f in img.visible_features][:3]
        feature_text = ", ".join(features)

        if feature_text:
            lines.append(f"{room}: {feature_text}")
        else:
            lines.append(f"{room}: {img.description}")

    return "\n".join(lines)