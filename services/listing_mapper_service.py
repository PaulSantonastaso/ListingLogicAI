from models.property_data import PropertyDetails
from models.listing_details import (
    ListingDetails,
    AddressDetails,
    PricingDetails,
    BasicPropertyDetails,
    InteriorDetails,
    ExteriorDetails,
    ParkingDetails,
    HoaDetails,
    RemarksDetails,
    PhotoDetails,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_COOLING = "Central Air"
DEFAULT_HEATING = "Central"
DEFAULT_SHOWING_INSTRUCTIONS = (
    "Contact listing agent to schedule. 24-hour notice preferred. "
    "Please remove shoes upon entry."
)

# Flooring keywords to extract from interior_features into the flooring field
FLOORING_KEYWORDS: set[str] = {
    "hardwood floors",
    "hardwood flooring",
    "hardwood",
    "tile floors",
    "tile flooring",
    "tile",
    "vinyl flooring",
    "vinyl",
    "lvp flooring",
    "lvp",
    "luxury vinyl plank",
    "laminate flooring",
    "laminate",
    "carpet",
    "travertine",
    "marble floors",
    "marble flooring",
    "marble",
    "bamboo flooring",
    "bamboo",
    "cork flooring",
    "concrete floors",
    "polished concrete",
    "wood-look flooring",
    "wood look flooring",
    "engineered hardwood",
}

# Fireplace keywords for fireplace_yn derivation
FIREPLACE_KEYWORDS: set[str] = {
    "fireplace",
    "gas fireplace",
    "wood burning fireplace",
    "electric fireplace",
    "double-sided fireplace",
}

# Spa/hot tub keywords for spa_yn derivation
SPA_KEYWORDS: set[str] = {
    "hot tub",
    "spa",
    "in-ground spa",
    "pool spa",
    "jetted tub",
}


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def _normalize_full_bathrooms(value: float | int | None) -> int | None:
    if value is None:
        return None
    whole = int(value)
    fractional = float(value) - whole
    if fractional >= 0.5:
        return whole
    return whole


def _normalize_half_bathrooms(
    bathrooms: float | int | None,
    half_bathrooms: float | int | None,
) -> int | None:
    if half_bathrooms is not None:
        return int(half_bathrooms)
    if bathrooms is None:
        return None
    whole = int(bathrooms)
    fractional = float(bathrooms) - whole
    if fractional >= 0.5:
        return 1
    return 0


def _dedupe(items: list[str] | None) -> list[str]:
    if not items:
        return []
    cleaned = [item.strip() for item in items if item and item.strip()]
    return list(dict.fromkeys(cleaned))


# ---------------------------------------------------------------------------
# Derivation helpers
# ---------------------------------------------------------------------------

def _extract_flooring(interior_features: list[str]) -> list[str]:
    """
    Pull flooring-type strings out of interior_features into a dedicated
    flooring list for the RESO Flooring field.
    """
    flooring = []
    for feature in interior_features:
        if feature.strip().lower() in FLOORING_KEYWORDS:
            flooring.append(feature.strip())
    return _dedupe(flooring)


def _derive_fireplace_yn(interior_features: list[str]) -> bool:
    normalized = {f.strip().lower() for f in interior_features}
    return any(kw in normalized for kw in FIREPLACE_KEYWORDS)


def _derive_spa_yn(pool_features: list[str]) -> bool:
    normalized = {f.strip().lower() for f in pool_features}
    return any(kw in normalized for kw in SPA_KEYWORDS)


def _derive_cooling(cooling: str | None) -> str:
    """
    Use extracted value if present, otherwise apply smart default.
    Never invents data — default is applied at mapping time only.
    """
    return cooling.strip() if cooling and cooling.strip() else DEFAULT_COOLING


def _derive_heating(heating: str | None) -> str:
    return heating.strip() if heating and heating.strip() else DEFAULT_HEATING


# ---------------------------------------------------------------------------
# Main mapper
# ---------------------------------------------------------------------------

def map_property_to_listing_details(
    property_details: PropertyDetails,
    public_remarks: str | None = None,
    photos_count: int | None = None,
) -> ListingDetails:

    bathrooms_full = _normalize_full_bathrooms(property_details.bathrooms)
    bathrooms_half = _normalize_half_bathrooms(
        property_details.bathrooms,
        property_details.half_bathrooms,
    )

    interior_features = _dedupe(property_details.interior_features)
    pool_features = _dedupe(property_details.pool_features)

    fireplace_yn = _derive_fireplace_yn(interior_features)
    fireplaces_total = 1 if fireplace_yn else None
    pool_private_yn = len(pool_features) > 0
    spa_yn = _derive_spa_yn(pool_features)
    flooring = _extract_flooring(interior_features)
    cooling = _derive_cooling(property_details.cooling)
    heating = _derive_heating(property_details.heating)

    return ListingDetails(
        address=AddressDetails(
            full_address=property_details.address,
            city=property_details.city,
            state=property_details.state,
            postal_code=property_details.postal_code,
            community_name=property_details.community_name,
            subdivision_name=property_details.subdivision_name,
        ),
        pricing=PricingDetails(
            list_price=property_details.list_price,
            original_list_price=property_details.list_price,
        ),
        basics=BasicPropertyDetails(
            property_type=property_details.property_type,
            property_subtype=property_details.property_subtype,
            bedrooms_total=property_details.bedrooms,
            bathrooms_full=bathrooms_full,
            bathrooms_half=bathrooms_half,
            living_area_sqft=property_details.square_footage,
            lot_size_sqft=property_details.lot_size_sqft,
            year_built=property_details.year_built,
            stories_total=property_details.stories_total,
            cooling=cooling,
            heating=heating,
            fireplace_yn=fireplace_yn,
            fireplaces_total=fireplaces_total,
            pool_private_yn=pool_private_yn,
            spa_yn=spa_yn,
        ),
        interior=InteriorDetails(
            interior_features=interior_features,
            appliances=_dedupe(property_details.appliances),
            flooring=flooring,
        ),
        exterior=ExteriorDetails(
            exterior_features=_dedupe(property_details.exterior_features),
            pool_features=pool_features,
        ),
        parking=ParkingDetails(
            garage_spaces=property_details.garage_spaces,
            parking_features=_dedupe(property_details.parking_features),
        ),
        hoa_details=HoaDetails(
            hoa=property_details.hoa,
            hoa_fee=property_details.hoa_fee,
            hoa_fee_frequency=property_details.hoa_fee_frequency,
            community_features=_dedupe(property_details.community_features),
        ),
        remarks=RemarksDetails(
            public_remarks=public_remarks,
            showing_instructions=DEFAULT_SHOWING_INSTRUCTIONS,
        ),
        photos=PhotoDetails(
            photos_count=photos_count,
        ),
    )