"""
image_rename_service.py

Takes the ranked image set from ImageIntelligence and the original uploaded
image bytes, and returns two sets of renamed images:

  curated   — top CURATED_SET_SIZE images, goes into photos/curated/ in the ZIP
  additional — remainder, goes into photos/additional/ in the ZIP

Naming convention:
  {rank:02d}_{room_type}_{top_feature}.{ext}
  Hero image always prefixed with 'hero':
  01_hero_front_exterior.jpg
  02_pool_screen-enclosure.jpg
  03_kitchen_white-cabinetry.jpg

No new AI calls — built entirely from existing RankedImage data.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from models.image_intelligence import ImageIntelligence, RankedImage

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CURATED_SET_SIZE = 25       # Top N images go into photos/curated/
MAX_FEATURE_CHARS = 20      # Max chars from top feature in filename
MAX_ROOM_CHARS = 24         # Max chars from room type in filename


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------
@dataclass
class RenamedImage:
    image_id: str
    original_filename: str
    renamed_filename: str
    image_bytes: bytes
    rank: int
    room_type: str
    is_hero: bool
    is_curated: bool


@dataclass
class RenameResult:
    curated: list[RenamedImage] = field(default_factory=list)
    additional: list[RenamedImage] = field(default_factory=list)

    @property
    def all_images(self) -> list[RenamedImage]:
        return self.curated + self.additional


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------

def _sanitize(text: str, max_chars: int) -> str:
    """
    Lowercase, replace spaces/underscores with hyphens, strip non-alphanumeric
    characters (except hyphens), truncate to max_chars, strip trailing hyphens.
    """
    text = text.lower().strip()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    text = text[:max_chars]
    text = text.strip("-")
    return text


def _get_extension(filename: str) -> str:
    """Extract lowercase extension from filename. Defaults to .jpg."""
    if "." in filename:
        return "." + filename.rsplit(".", 1)[-1].lower()
    return ".jpg"


def _build_filename(
    rank: int,
    is_hero: bool,
    room_type: Optional[str],
    visible_features: list[str],
    extension: str,
    used_names: set[str],
) -> str:
    """
    Build a clean ranked filename from image metadata.
    Disambiguates duplicates by appending _b, _c, etc.
    """
    parts = [f"{rank:02d}"]

    if is_hero:
        parts.append("hero")

    if room_type:
        parts.append(_sanitize(room_type, MAX_ROOM_CHARS))

    if visible_features:
        top_feature = _sanitize(visible_features[0], MAX_FEATURE_CHARS)
        if top_feature:
            parts.append(top_feature)

    base = "_".join(parts)
    candidate = f"{base}{extension}"

    # Disambiguate if name already used
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate

    for suffix in "bcdefghijklmnopqrstuvwxyz":
        candidate = f"{base}_{suffix}{extension}"
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate

    # Fallback — append rank again to guarantee uniqueness
    candidate = f"{base}_{rank:04d}{extension}"
    used_names.add(candidate)
    return candidate


# ---------------------------------------------------------------------------
# Main service function
# ---------------------------------------------------------------------------

def build_renamed_image_set(
    image_intelligence: ImageIntelligence,
    original_images: list[tuple[bytes, str]],
) -> RenameResult:
    """
    Join ranked images against original bytes and produce RenameResult.

    Args:
        image_intelligence: Output from build_image_intelligence()
        original_images:    List of (image_bytes, original_filename) tuples
                            from session state

    Returns:
        RenameResult with curated and additional lists, each in rank order
    """
    if not image_intelligence or not image_intelligence.ranked_images:
        return RenameResult()

    # Build lookup: original_filename -> image_bytes
    # Filenames are the join key between ranked images and raw bytes
    bytes_lookup: dict[str, bytes] = {
        filename: img_bytes
        for img_bytes, filename in original_images
    }

    ranked = image_intelligence.ranked_images  # already sorted by score desc
    hero_id = image_intelligence.hero_image_id
    used_names: set[str] = set()

    curated: list[RenamedImage] = []
    additional: list[RenamedImage] = []

    for rank_index, ranked_image in enumerate(ranked, start=1):
        image_bytes = bytes_lookup.get(ranked_image.filename)

        if image_bytes is None:
            # Image in intelligence model but not in uploaded set — skip
            continue

        is_hero = ranked_image.image_id == hero_id
        is_curated = rank_index <= CURATED_SET_SIZE
        extension = _get_extension(ranked_image.filename)

        renamed_filename = _build_filename(
            rank=rank_index,
            is_hero=is_hero,
            room_type=ranked_image.room_type,
            visible_features=ranked_image.visible_features,
            extension=extension,
            used_names=used_names,
        )

        renamed = RenamedImage(
            image_id=ranked_image.image_id,
            original_filename=ranked_image.filename,
            renamed_filename=renamed_filename,
            image_bytes=image_bytes,
            rank=rank_index,
            room_type=ranked_image.room_type or "unknown",
            is_hero=is_hero,
            is_curated=is_curated,
        )

        if is_curated:
            curated.append(renamed)
        else:
            additional.append(renamed)

    return RenameResult(curated=curated, additional=additional)