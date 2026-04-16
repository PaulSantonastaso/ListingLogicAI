from typing import List, Optional

from models.image_intelligence import ImageIntelligence, RankedImage
from models.video_script import VideoShot


# Per-platform shot counts
REEL_SHOT_COUNT = 5
TIKTOK_SHOT_COUNT = 7
YOUTUBE_SHORT_SHOT_COUNT = 9

# Room preference order for the opening shot — hero/exterior first
OPENING_PREFERRED_ROOMS = [
    "front_exterior",
    "back_exterior",
    "living_room",
    "kitchen",
]

# Room preference order for mid-sequence shots
MID_PREFERRED_ROOMS = [
    "kitchen",
    "living_room",
    "primary_bedroom",
    "bedroom",
    "bathroom",
    "dining_room",
    "office",
    "patio",
    "backyard",
]

# Room preference order for closing shot — aspirational/outdoor last
CLOSING_PREFERRED_ROOMS = [
    "backyard",
    "patio",
    "back_exterior",
    "front_exterior",
    "living_room",
]


def _build_shot_direction(image: RankedImage, position: str) -> str:
    """
    Build an actionable shot direction for the agent based on
    room type and position in the sequence (opening, mid, closing).
    """
    room = image.room_type or "space"
    features = ", ".join(image.visible_features[:3]) if image.visible_features else None
    feature_note = f" — highlight {features}" if features else ""

    if position == "opening":
        if room == "front_exterior":
            return f"Start outside. Walk slowly toward the front door to draw the viewer in{feature_note}."
        if room in {"back_exterior", "backyard", "patio"}:
            return f"Open on the outdoor space. Pan slowly across the full area{feature_note}."
        return f"Open wide on the {room.replace('_', ' ')}. Let the space speak first{feature_note}."

    if position == "closing":
        if room in {"backyard", "patio", "back_exterior"}:
            return f"End on the outdoor space. Slow pan, let it breathe{feature_note}."
        if room == "front_exterior":
            return f"Close outside. Pull back slowly from the front of the home{feature_note}."
        return f"Close on the {room.replace('_', ' ')}. End with energy and confidence{feature_note}."

    # Mid sequence
    directions = {
        "kitchen": f"Move through the kitchen. Lead with the island or countertops{feature_note}.",
        "living_room": f"Sweep across the living room. Capture the full layout and light{feature_note}.",
        "dining_room": f"Frame the dining area. Show the full table and any natural light{feature_note}.",
        "bedroom": f"Pan across the bedroom. Keep it wide to show scale{feature_note}.",
        "primary_bedroom": f"Pan across the primary suite. Emphasize size and any standout finishes{feature_note}.",
        "bathroom": f"Show the vanity and shower or tub. Keep the shot clean and tight{feature_note}.",
        "office": f"Frame the office or flex space. Keep it bright and purposeful{feature_note}.",
        "patio": f"Walk through the outdoor living area. Show the full entertaining space{feature_note}.",
        "backyard": f"Pan across the backyard. Capture depth and any standout features{feature_note}.",
    }

    return directions.get(
        room,
        f"Frame the {room.replace('_', ' ')} clearly. Keep the shot wide and well-lit{feature_note}."
    )


def _build_text_only_direction(order: int, total: int) -> str:
    """
    Fallback shot direction when no images are available.
    Guides the agent on what to film based on shot position.
    """
    if order == 1:
        return "Open outside. Start at the curb and walk slowly toward the front door."
    if order == total:
        return "Close on your favorite feature of the home — something that will stick with the viewer."
    positions = {
        2: "Move inside. Open wide on the main living area to establish the layout.",
        3: "Film the kitchen. Lead with the countertops or island — whatever stands out.",
        4: "Show the primary bedroom or a standout interior space.",
        5: "Capture an outdoor space — backyard, patio, or pool if available.",
        6: "Find a detail shot — a fireplace, built-ins, upgraded finishes, or a view.",
        7: "Show the dining area or another lifestyle-forward space.",
        8: "Return outside. Film the back of the property or any outdoor amenity.",
    }
    return positions.get(order, f"Film a compelling feature of the home — shot {order} of {total}.")


def _pick_by_room_preference(
    ranked: List[RankedImage],
    used_ids: set,
    preferred_rooms: List[str],
) -> Optional[RankedImage]:
    for room in preferred_rooms:
        for img in ranked:
            if img.image_id not in used_ids and img.room_type == room:
                return img
    return None


def _pick_next_available(
    ranked: List[RankedImage],
    used_ids: set,
) -> Optional[RankedImage]:
    for img in ranked:
        if img.image_id not in used_ids:
            return img
    return None


def _build_shots_from_images(
    ranked: List[RankedImage],
    shot_count: int,
) -> List[VideoShot]:
    """
    Select images and build an ordered shot list for a given platform.
    Opens on the best exterior/hero, fills mid shots by room preference,
    and closes on the most aspirational available image.
    """
    shots: List[VideoShot] = []
    used_ids: set = set()

    # Opening shot
    opening = _pick_by_room_preference(ranked, used_ids, OPENING_PREFERRED_ROOMS)
    if not opening:
        opening = _pick_next_available(ranked, used_ids)
    if opening:
        used_ids.add(opening.image_id)
        shots.append(VideoShot(
            order=1,
            image_filename=opening.filename,
            room_type=opening.room_type,
            visible_features=opening.visible_features,
            direction=_build_shot_direction(opening, "opening"),
        ))

    # Closing shot — pick now so we can reserve it
    closing_candidate = _pick_by_room_preference(ranked, used_ids, CLOSING_PREFERRED_ROOMS)
    if not closing_candidate:
        closing_candidate = _pick_next_available(ranked, used_ids)
    if closing_candidate:
        used_ids.add(closing_candidate.image_id)

    # Mid shots — fill remaining slots between opening and closing
    mid_count = shot_count - (1 if closing_candidate else 0) - len(shots)
    for _ in range(mid_count):
        mid = _pick_by_room_preference(ranked, used_ids, MID_PREFERRED_ROOMS)
        if not mid:
            mid = _pick_next_available(ranked, used_ids)
        if mid:
            used_ids.add(mid.image_id)
            shots.append(VideoShot(
                order=len(shots) + 1,
                image_filename=mid.filename,
                room_type=mid.room_type,
                visible_features=mid.visible_features,
                direction=_build_shot_direction(mid, "mid"),
            ))

    # Append closing shot last
    if closing_candidate:
        shots.append(VideoShot(
            order=len(shots) + 1,
            image_filename=closing_candidate.filename,
            room_type=closing_candidate.room_type,
            visible_features=closing_candidate.visible_features,
            direction=_build_shot_direction(closing_candidate, "closing"),
        ))

    return shots


def _build_text_only_shots(shot_count: int) -> List[VideoShot]:
    """
    Fallback shot list when no images are available.
    Guides the agent on what to film without referencing specific images.
    """
    return [
        VideoShot(
            order=i,
            image_filename=None,
            room_type=None,
            visible_features=[],
            direction=_build_text_only_direction(i, shot_count),
        )
        for i in range(1, shot_count + 1)
    ]


def build_video_shot_plan(
    image_intelligence: Optional[ImageIntelligence],
) -> dict[str, List[VideoShot]]:
    """
    Returns a dict of per-platform shot lists keyed by platform name.
    Falls back to text-only directions if no image intelligence is available.
    """
    if image_intelligence is not None and len(image_intelligence.ranked_images) > 0:
        ranked = image_intelligence.ranked_images
        return {
            "reel": _build_shots_from_images(ranked, REEL_SHOT_COUNT),
            "tiktok": _build_shots_from_images(ranked, TIKTOK_SHOT_COUNT),
            "youtube_short": _build_shots_from_images(ranked, YOUTUBE_SHORT_SHOT_COUNT),
        }

    return {
        "reel": _build_text_only_shots(REEL_SHOT_COUNT),
        "tiktok": _build_text_only_shots(TIKTOK_SHOT_COUNT),
        "youtube_short": _build_text_only_shots(YOUTUBE_SHORT_SHOT_COUNT),
    }