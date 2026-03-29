import io
import csv

from models.listing_details import ListingDetails


def _join_list(values: list[str]) -> str:
    return ", ".join(v.strip() for v in values if v and v.strip())


def _bool_to_yn(value: bool | None) -> str:
    if value is None:
        return ""
    return "Yes" if value else "No"


def build_reso_csv_row(listing: ListingDetails) -> dict[str, str | int | float | None]:
    return {
        # --- Address ---
        "StreetAddress": listing.address.full_address,
        "City": listing.address.city,
        "StateOrProvince": listing.address.state,
        "PostalCode": listing.address.postal_code,
        "CommunityName": listing.address.community_name,
        "SubdivisionName": listing.address.subdivision_name,

        # --- Pricing ---
        "ListPrice": listing.pricing.list_price,
        "OriginalListPrice": listing.pricing.original_list_price,

        # --- Property Basics ---
        "PropertyType": listing.basics.property_type,
        "PropertySubType": listing.basics.property_subtype,
        "BedroomsTotal": listing.basics.bedrooms_total,
        "BathroomsFull": listing.basics.bathrooms_full,
        "BathroomsHalf": listing.basics.bathrooms_half,
        "LivingArea": listing.basics.living_area_sqft,
        "LotSizeSquareFeet": listing.basics.lot_size_sqft,
        "YearBuilt": listing.basics.year_built,
        "StoriesTotal": listing.basics.stories_total,

        # --- Systems ---
        "Cooling": listing.basics.cooling,
        "Heating": listing.basics.heating,

        # --- Fireplace ---
        "FireplaceYN": _bool_to_yn(listing.basics.fireplace_yn),
        "FireplacesTotal": listing.basics.fireplaces_total,

        # --- Pool & Spa ---
        "PoolPrivateYN": _bool_to_yn(listing.basics.pool_private_yn),
        "SpaYN": _bool_to_yn(listing.basics.spa_yn),

        # --- Interior ---
        "InteriorFeatures": _join_list(listing.interior.interior_features),
        "Appliances": _join_list(listing.interior.appliances),
        "Flooring": _join_list(listing.interior.flooring),

        # --- Exterior ---
        "ExteriorFeatures": _join_list(listing.exterior.exterior_features),
        "PoolFeatures": _join_list(listing.exterior.pool_features),

        # --- Parking ---
        "GarageSpaces": listing.parking.garage_spaces,
        "ParkingFeatures": _join_list(listing.parking.parking_features),

        # --- HOA ---
        "AssociationYN": listing.hoa_details.hoa,
        "AssociationFee": listing.hoa_details.hoa_fee,
        "AssociationFeeFrequency": listing.hoa_details.hoa_fee_frequency,
        "AssociationAmenities": _join_list(listing.hoa_details.community_features),

        # --- Remarks ---
        "PublicRemarks": listing.remarks.public_remarks,
        "ShowingInstructions": listing.remarks.showing_instructions,

        # --- Photos ---
        "PhotosCount": listing.photos.photos_count,
    }


def build_reso_csv_string(listing: ListingDetails) -> str:
    row = build_reso_csv_row(listing)
    output = io.StringIO()

    writer = csv.DictWriter(output, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)

    return output.getvalue()