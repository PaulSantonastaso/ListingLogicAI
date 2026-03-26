from typing import Optional, List
from pydantic import BaseModel, Field


class AddressDetails(BaseModel):
    full_address: Optional[str] = Field(
        default=None,
        description="Full property address as a single string"
    )
    city: Optional[str] = Field(
        default=None,
        description="City where the property is located"
    )
    state: Optional[str] = Field(
        default=None,
        description="State or region where the property is located"
    )
    postal_code: Optional[str] = Field(
        default=None,
        description="Postal or ZIP code of the property"
    )


class PricingDetails(BaseModel):
    list_price: Optional[int] = Field(
        default=None,
        description="Current listing price in whole dollars"
    )


class BasicPropertyDetails(BaseModel):
    property_type: Optional[str] = Field(
        default=None,
        description="High level property type such as Residential, Condo, Townhouse, Land, or Multi-Family"
    )
    property_subtype: Optional[str] = Field(
        default=None,
        description="More specific property subtype such as Single Family Residence, Townhome, Condo, or Duplex"
    )
    bedrooms_total: Optional[int] = Field(
        default=None,
        description="Total number of bedrooms in the property"
    )
    bathrooms_full: Optional[int] = Field(
        default=None,
        description="Number of full bathrooms in the property"
    )
    bathrooms_half: Optional[int] = Field(
        default=None,
        description="Number of half bathrooms in the property"
    )
    living_area_sqft: Optional[int] = Field(
        default=None,
        description="Total living area in square feet"
    )
    lot_size_sqft: Optional[int] = Field(
        default=None,
        description="Total lot size in square feet"
    )
    year_built: Optional[int] = Field(
        default=None,
        description="Year the property was originally built"
    )
    stories_total: Optional[int] = Field(
        default=None,
        description="Total number of stories or floors in the property"
    )


class InteriorDetails(BaseModel):
    interior_features: List[str] = Field(
        default_factory=list,
        description="Interior features such as open floor plan, vaulted ceilings, or fireplace"
    )
    appliances: List[str] = Field(
        default_factory=list,
        description="Appliances included with the property such as dishwasher, refrigerator, microwave, or range"
    )


class ExteriorDetails(BaseModel):
    exterior_features: List[str] = Field(
        default_factory=list,
        description="Exterior features such as patio, deck, fenced yard, covered porch, or screened enclosure"
    )
    pool_features: List[str] = Field(
        default_factory=list,
        description="Pool-related features such as in-ground pool, heated pool, spa, or screen enclosure"
    )


class ParkingDetails(BaseModel):
    garage_spaces: Optional[int] = Field(
        default=None,
        description="Number of garage parking spaces"
    )
    parking_features: List[str] = Field(
        default_factory=list,
        description="Parking features such as attached garage, driveway, carport, or street parking"
    )


class HoaDetails(BaseModel):
    hoa: Optional[bool] = Field(
        default=None,
        description="Whether the property is part of a Homeowners Association"
    )
    hoa_fee: Optional[float] = Field(
        default=None,
        description="Recurring HOA fee amount"
    )
    hoa_fee_frequency: Optional[str] = Field(
        default=None,
        description="Frequency of the HOA fee such as Monthly, Quarterly, or Annually"
    )
    community_features: List[str] = Field(
        default_factory=list,
        description="Community or association amenities such as clubhouse, community pool, fitness center, or gated entry"
    )


class RemarksDetails(BaseModel):
    public_remarks: Optional[str] = Field(
        default=None,
        description="Public-facing MLS remarks describing the property"
    )


class ListingDetails(BaseModel):
    address: AddressDetails = Field(
        default_factory=AddressDetails,
        description="Normalized address information for the listing"
    )
    pricing: PricingDetails = Field(
        default_factory=PricingDetails,
        description="Pricing information for the listing"
    )
    basics: BasicPropertyDetails = Field(
        default_factory=BasicPropertyDetails,
        description="Core property facts such as beds, baths, square footage, and year built"
    )
    interior: InteriorDetails = Field(
        default_factory=InteriorDetails,
        description="Interior features and appliances"
    )
    exterior: ExteriorDetails = Field(
        default_factory=ExteriorDetails,
        description="Exterior and pool-related features"
    )
    parking: ParkingDetails = Field(
        default_factory=ParkingDetails,
        description="Garage and parking details"
    )
    hoa_details: HoaDetails = Field(
        default_factory=HoaDetails,
        description="HOA and community amenity details"
    )
    remarks: RemarksDetails = Field(
        default_factory=RemarksDetails,
        description="Public remarks and other listing text fields"
    )