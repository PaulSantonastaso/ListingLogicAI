import io
import csv

from models.listing_details import ListingDetails


def _join_list(values: list[str]) -> str:
    return ", ".join(v.strip() for v in values if v and v.strip())


def build_reso_csv_row(listing: ListingDetails) -> dict[str, str | int | float | None]:
    return {
        "StreetAddress": listing.address.full_address,
        "City": listing.address.city,
        "StateOrProvince": listing.address.state,
        "PostalCode": listing.address.postal_code,

        "ListPrice": listing.pricing.list_price,

        "PropertyType": listing.basics.property_type,
        "PropertySubType": listing.basics.property_subtype,
        "BedroomsTotal": listing.basics.bedrooms_total,
        "BathroomsFull": listing.basics.bathrooms_full,
        "BathroomsHalf": listing.basics.bathrooms_half,
        "LivingArea": listing.basics.living_area_sqft,
        "LotSizeSquareFeet": listing.basics.lot_size_sqft,
        "YearBuilt": listing.basics.year_built,
        "StoriesTotal": listing.basics.stories_total,

        "InteriorFeatures": _join_list(listing.interior.interior_features),
        "Appliances": _join_list(listing.interior.appliances),

        "ExteriorFeatures": _join_list(listing.exterior.exterior_features),
        "PoolFeatures": _join_list(listing.exterior.pool_features),

        "GarageSpaces": listing.parking.garage_spaces,
        "ParkingFeatures": _join_list(listing.parking.parking_features),

        "AssociationYN": listing.hoa_details.hoa,
        "AssociationFee": listing.hoa_details.hoa_fee,
        "AssociationFeeFrequency": listing.hoa_details.hoa_fee_frequency,
        "AssociationAmenities": _join_list(listing.hoa_details.community_features),

        "PublicRemarks": listing.remarks.public_remarks,
    }


def build_reso_csv_string(listing: ListingDetails) -> str:
    row = build_reso_csv_row(listing)
    output = io.StringIO()

    writer = csv.DictWriter(output, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)

    return output.getvalue()