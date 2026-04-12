from typing import List
from collections import defaultdict

from models.property_image import PropertyImage
from models.image_intelligence import (
    ImageIntelligence,
    RankedImage,
    WeakImage,
    ImageHighlight,
)

ROOM_WEIGHTS = {
    "front_exterior": 1.0,
    "back_exterior": 0.9,
    "backyard": 0.9,
    "patio": 0.85,
    "pool": 0.95,
    "living_room": 0.85,
    "kitchen": 0.85,
    "dining_room": 0.75,
    "bedroom": 0.7,
    "bathroom": 0.6,
    "office": 0.65,
    "garage": 0.25,
    "other": 0.4,
}

SHOT_WEIGHTS = {
    "wide": 0.15,
    "detail": -0.05,
    "close_up": -0.1,
    "unknown": 0.0,
}

def _score_image(image: PropertyImage) -> float:

    room_weight = ROOM_WEIGHTS.get(image.metadata.room_type, 0.4)

    shot_bonus = SHOT_WEIGHTS.get(image.metadata.shot_type, 0.0)

    quality = image.metadata.quality_score or 0.5

    marketing_bonus = 0.1 if image.metadata.likely_marketing_worthy else -0.1

    feature_bonus = min(len(image.visible_features) * 0.03, 0.15)

    score = (
        room_weight
        + shot_bonus
        + quality * 0.6
        + marketing_bonus
        + feature_bonus
    )

    return round(score, 4)

def _rank_images(images: List[PropertyImage]) -> List[RankedImage]:

    ranked = []

    for img in images:

        score = _score_image(img)

        ranked.append(
            RankedImage(
                image_id=img.image_id,
                filename=img.filename,
                room_type=img.metadata.room_type,
                shot_type=img.metadata.shot_type,
                score=score,
                quality_score=img.metadata.quality_score,
                marketing_worthy=img.metadata.likely_marketing_worthy,
                visible_features=[f.name for f in img.visible_features],
                reason=(
                    img.caption
                    if img.caption
                    else f"{img.metadata.room_type.replace('_', ' ').title()} — {', '.join(f.name for f in img.visible_features[:2])}"
                    if img.visible_features
                    else img.metadata.room_type.replace('_', ' ').title()
                ),
            )
        )

    ranked.sort(key=lambda x: x.score, reverse=True)

    return ranked

def _detect_weak_images(images: List[PropertyImage]) -> List[WeakImage]:

    weak = []

    for img in images:

        if img.metadata.likely_marketing_worthy is False:
            weak.append(
                WeakImage(
                    image_id=img.image_id,
                    filename=img.filename,
                    reason="Image appears unsuitable for marketing.",
                )
            )
            continue

        if img.metadata.quality_score is not None and img.metadata.quality_score < 0.35:
            weak.append(
                WeakImage(
                    image_id=img.image_id,
                    filename=img.filename,
                    reason="Low image quality.",
                )
            )

    return weak

def _extract_highlights(images: List[PropertyImage]) -> List[ImageHighlight]:

    feature_map = defaultdict(list)

    for img in images:
        for feature in img.visible_features:
            feature_map[feature.name].append(img.image_id)

    highlights = []

    for feature, ids in feature_map.items():
        highlights.append(
            ImageHighlight(
                feature=feature,
                supporting_image_ids=ids,
            )
        )

    return highlights[:5]

def _select_highlight_images(ranked: List[RankedImage]) -> List[str]:

    selected = []
    seen_rooms = set()

    for img in ranked:

        if img.room_type not in seen_rooms:
            selected.append(img.image_id)
            seen_rooms.add(img.room_type)

        if len(selected) == 3:
            break

    return selected

def build_image_intelligence(images: List[PropertyImage]) -> ImageIntelligence:

    if not images:
        return ImageIntelligence()

    ranked = _rank_images(images)
    weak = _detect_weak_images(images)
    highlights = _extract_highlights(images)
    highlight_images = _select_highlight_images(ranked)

    # The hero image is the single highest-scoring image after ranking.
    # It anchors the email campaign copy and informs the video shot list.
    hero_image_id = ranked[0].image_id if ranked else None

    return ImageIntelligence(
        ranked_images=ranked,
        weak_images=weak,
        highlight_images=highlight_images,
        hero_image_id=hero_image_id,
        highlights=highlights,
    )