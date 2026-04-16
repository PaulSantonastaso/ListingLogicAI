"""
feature_router_service.py

Routes high-confidence image-detected features into the correct structured
fields on PropertyDetails. This is the bridge between image intelligence
and the RESO CSV output.

Routing rules:
- Only features at or above HIGH_CONFIDENCE_THRESHOLD are routed.
- Never overwrite existing values — only append missing items.
- Appliance GROUP phrases (e.g. "stainless steel appliances") are explicitly
  blocked from the appliances field to prevent contaminating RESO data with
  non-enumerable values. They remain useful as key_features for copy only.
- Room type context is used to resolve ambiguous features (e.g. ceiling fan
  in bedroom → interior_features, ceiling fan in patio → exterior_features).
- All normalization is lowercase for deduplication, original casing is preserved
  when appending to PropertyDetails fields.
"""

from models.property_image import ImageFeature, RoomType
from models.property_data import PropertyDetails


HIGH_CONFIDENCE_THRESHOLD = 0.85

# ---------------------------------------------------------------------------
# Appliance routing
# ---------------------------------------------------------------------------

# Individual named appliances that map directly to PropertyDetails.appliances
APPLIANCE_NAMES: set[str] = {
    "dishwasher",
    "disposal",
    "garbage disposal",
    "dryer",
    "washer",
    "washing machine",
    "microwave",
    "range",
    "oven",
    "double oven",
    "refrigerator",
    "french door refrigerator",
    "stainless refrigerator",
    "wine refrigerator",
    "wine cooler",
    "ice maker",
    "cooktop",
    "gas cooktop",
    "electric cooktop",
    "hood",
    "range hood",
    "exhaust hood",
    "freezer",
    "trash compactor",
}

# Group phrases explicitly blocked from the appliances field
APPLIANCE_GROUP_PHRASES: set[str] = {
    "stainless steel appliances",
    "stainless appliances",
    "updated appliances",
    "new appliances",
    "appliances",
    "kitchen appliances",
}

# ---------------------------------------------------------------------------
# Interior feature routing
# ---------------------------------------------------------------------------

INTERIOR_FEATURE_NAMES: set[str] = {
    "fireplace",
    "gas fireplace",
    "wood burning fireplace",
    "electric fireplace",
    "barn door",
    "sliding barn door",
    "tray ceiling",
    "coffered ceiling",
    "vaulted ceiling",
    "cathedral ceiling",
    "open floor plan",
    "open concept",
    "kitchen island",
    "breakfast bar",
    "bar seating",
    "built-ins",
    "built-in shelves",
    "built-in cabinetry",
    "crown molding",
    "wainscoting",
    "shiplap",
    "accent wall",
    "exposed beams",
    "hardwood floors",
    "hardwood flooring",
    "tile floors",
    "tile flooring",
    "vinyl flooring",
    "lvp flooring",
    "laminate flooring",
    "walk-in closet",
    "walk-in pantry",
    "pantry",
    "laundry room",
    "mud room",
    "mudroom",
    "loft",
    "bonus room",
    "flex room",
    "staircase",
    "wood staircase",
    "spiral staircase",
    "iron railing",
    "chandelier",
    "ceiling fan",
    "recessed lighting",
    "smart home",
    "smart lighting",
    "double vanity",
    "dual vanity",
    "walk-in shower",
    "frameless shower",
    "soaking tub",
    "freestanding tub",
    "garden tub",
    "jetted tub",
    "subway tile",
    "tile backsplash",
    "quartz countertops",
    "granite countertops",
    "marble countertops",
    "acacia countertops",
    "butcher block countertops",
    "white cabinetry",
    "shaker cabinets",
    "upgraded cabinetry",
    "soft close cabinets",
    "french doors",
    "sliding glass doors",
    "glass doors to pool",
    "pocket doors",
}

# ---------------------------------------------------------------------------
# Exterior feature routing
# ---------------------------------------------------------------------------

EXTERIOR_FEATURE_NAMES: set[str] = {
    "screened lanai",
    "screened porch",
    "screened enclosure",
    "covered lanai",
    "covered patio",
    "covered porch",
    "wrap around porch",
    "front porch",
    "back porch",
    "deck",
    "wood deck",
    "composite deck",
    "outdoor kitchen",
    "summer kitchen",
    "fire pit",
    "pergola",
    "gazebo",
    "shed",
    "workshop",
    "fenced backyard",
    "fenced yard",
    "privacy fence",
    "vinyl fence",
    "white vinyl fence",
    "wood fence",
    "aluminum fence",
    "irrigation system",
    "sprinkler system",
    "solar panels",
    "outdoor lighting",
    "landscape lighting",
    "mature landscaping",
    "tropical landscaping",
    "fruit trees",
    "outdoor shower",
    "rv parking",
    "boat parking",
}

# ---------------------------------------------------------------------------
# Pool feature routing
# ---------------------------------------------------------------------------

POOL_FEATURE_NAMES: set[str] = {
    "in-ground pool",
    "inground pool",
    "pool",
    "heated pool",
    "salt water pool",
    "saltwater pool",
    "lap pool",
    "hot tub",
    "spa",
    "in-ground spa",
    "pool spa",
    "pool deck",
    "travertine pool deck",
    "paver pool deck",
    "screen enclosure",
    "screened pool enclosure",
    "pool enclosure",
    "pool cage",
    "pool bath",
    "pool bathroom",
    "waterfall feature",
    "grotto",
    "swim shelf",
    "tanning ledge",
    "beach entry",
}

# ---------------------------------------------------------------------------
# Parking feature routing
# ---------------------------------------------------------------------------

PARKING_FEATURE_NAMES: set[str] = {
    "attached garage",
    "detached garage",
    "two car garage",
    "2 car garage",
    "three car garage",
    "3 car garage",
    "oversized garage",
    "tandem garage",
    "carport",
    "driveway",
    "paved driveway",
    "circular driveway",
    "extended driveway",
    "rv pad",
    "rv parking",
    "boat parking",
    "side entry garage",
    "rear entry garage",
}

# ---------------------------------------------------------------------------
# Ambiguous features resolved by room type context
# ---------------------------------------------------------------------------

# Features that belong in interior OR exterior depending on room context
ROOM_CONTEXT_OVERRIDES: dict[str, dict[str, str]] = {
    "ceiling fan": {
        "interior": "interior_features",
        "exterior": "exterior_features",
    },
    "french doors": {
        "interior": "interior_features",
        "exterior": "exterior_features",
    },
    "sliding glass doors": {
        "interior": "interior_features",
        "exterior": "exterior_features",
    },
}

EXTERIOR_ROOM_TYPES: set[str] = {
    "front_exterior",
    "back_exterior",
    "backyard",
    "patio",
    "pool",
}


# ---------------------------------------------------------------------------
# Core routing logic
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    return text.strip().lower()


def _is_exterior_room(room_type: str | None) -> bool:
    return (room_type or "other") in EXTERIOR_ROOM_TYPES


def _resolve_target_field(
    feature_name: str,
    room_type: str | None,
) -> str | None:
    """
    Determine which PropertyDetails field a detected feature belongs in.
    Returns the field name as a string, or None if the feature should not
    be routed to any structured field.
    """
    normalized = _normalize(feature_name)

    # Block appliance group phrases entirely
    if normalized in APPLIANCE_GROUP_PHRASES:
        return None

    # Individual appliances → appliances field
    if normalized in APPLIANCE_NAMES:
        return "appliances"

    # Pool features → pool_features field
    if normalized in POOL_FEATURE_NAMES:
        return "pool_features"

    # Parking features → parking_features field
    if normalized in PARKING_FEATURE_NAMES:
        return "parking_features"

    # Exterior features → exterior_features field
    if normalized in EXTERIOR_FEATURE_NAMES:
        return "exterior_features"

    # Interior features — check room context for ambiguous features first
    if normalized in ROOM_CONTEXT_OVERRIDES:
        context = ROOM_CONTEXT_OVERRIDES[normalized]
        if _is_exterior_room(room_type):
            return context.get("exterior", "exterior_features")
        return context.get("interior", "interior_features")

    if normalized in INTERIOR_FEATURE_NAMES:
        return "interior_features"

    return None


def _already_present(value: str, existing: list[str]) -> bool:
    normalized = _normalize(value)
    return any(_normalize(existing_val) == normalized for existing_val in existing)


def route_image_features_to_structured_fields(
    property_details: PropertyDetails,
    feature: ImageFeature,
    room_type: str | None,
) -> PropertyDetails:
    """
    Route a single high-confidence image feature into the correct
    structured field on PropertyDetails.

    Only appends — never overwrites existing values.
    Returns the mutated PropertyDetails object.
    """
    if feature.confidence < HIGH_CONFIDENCE_THRESHOLD:
        return property_details

    target_field = _resolve_target_field(feature.name, room_type)

    if target_field is None:
        return property_details

    current_list: list[str] = getattr(property_details, target_field, []) or []

    if not _already_present(feature.name, current_list):
        current_list.append(feature.name)
        setattr(property_details, target_field, current_list)

    return property_details