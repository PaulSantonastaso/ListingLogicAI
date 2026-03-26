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
)


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


def map_property_to_listing_details(
    property_details: PropertyDetails,
    public_remarks: str | None = None,
) -> ListingDetails:
    bathrooms_full = _normalize_full_bathrooms(property_details.bathrooms)
    bathrooms_half = _normalize_half_bathrooms(
        property_details.bathrooms,
        property_details.half_bathrooms,
    )

    return ListingDetails(
        address=AddressDetails(
            full_address=property_details.address,
            city=property_details.city,
            state=property_details.state,
            postal_code=property_details.postal_code,
        ),
        pricing=PricingDetails(
            list_price=property_details.list_price,
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
        ),
        interior=InteriorDetails(
            interior_features=_dedupe(property_details.interior_features),
            appliances=_dedupe(property_details.appliances),
        ),
        exterior=ExteriorDetails(
            exterior_features=_dedupe(property_details.exterior_features),
            pool_features=_dedupe(property_details.pool_features),
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
        ),
    )