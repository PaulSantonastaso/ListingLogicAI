from pydantic import BaseModel, Field
from typing import List, Optional

from models.property_image import PropertyImage
from models.feature_candidate import FeatureCandidate


class PropertyDetails(BaseModel):
    address: Optional[str] = Field(
        default=None,
        description="Full property address or community name"
    )

    city: Optional[str] = Field(
        default=None,
        description="City where the property is located"
    )

    state: Optional[str] = Field(
        default=None,
        description="State or region of the property"
    )

    postal_code: Optional[str] = Field(
        default=None,
        description="Postal or ZIP code of the property"
    )

    property_type: Optional[str] = Field(
        default=None,
        description="High level property type such as Residential, Condo, Townhouse, Land, or Multi-Family"
    )

    property_subtype: Optional[str] = Field(
        default=None,
        description="More specific property type such as Single Family Residence, Townhome, Condo, Duplex"
    )

    stories_total: Optional[int] = Field(
        default=None,
        description="Total number of stories or floors in the property"
    )

    year_built: Optional[int] = Field(
        default=None,
        description="Year the property was originally built"
    )

    bedrooms: Optional[int] = Field(
        default=None,
        description="Number of bedrooms as an integer"
    )

    bathrooms: Optional[float] = Field(
        default=None,
        description="Number of full bathrooms in the property (not including half bathrooms)"
    )

    half_bathrooms: Optional[float] = Field(
        default=None,
        description="Number of half bathrooms in the property (toilet and sink only)"
    )

    list_price: Optional[int] = Field(
        default=None,
        description="Listing price in USD as a number without commas"
    )

    square_footage: Optional[int] = Field(
        default=None,
        description="Square footage of the property in square feet"
    )

    lot_size_sqft: Optional[int] = Field(
        default=None,
        description="Total lot size in square feet"
    )

    garage_spaces: Optional[int] = Field(
        default=None,
        description="Number of garage parking spaces"
    )

    parking_features: list[str] = Field(
        default_factory=list,
        description="Parking features such as driveway, attached garage, carport, or street parking"
    )

    interior_features: list[str] = Field(
        default_factory=list,
        description="Interior property features such as vaulted ceilings, open floor plan, or fireplace"
    )

    exterior_features: list[str] = Field(
        default_factory=list,
        description="Exterior features such as patio, deck, fenced yard, or covered porch"
    )

    appliances: list[str] = Field(
        default_factory=list,
        description="Appliances included in the property such as dishwasher, refrigerator, microwave, or range"
    )

    pool_features: list[str] = Field(
        default_factory=list,
        description="Pool related features such as in-ground pool, heated pool, screened enclosure"
    )

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
        description="Frequency of HOA fee such as Monthly, Quarterly, or Annually"
    )

    key_features: List[str] = Field(
        default_factory=list,
        description="3-5 short phrases describing standout property features"
    )

    images: List[PropertyImage] = Field(
        default_factory=list,
        description="Property photos uploaded by the agent. Each image includes an AI-generated description, detected visual features, and metadata such as room type and quality score."
    )

    feature_candidates: list[FeatureCandidate] = Field(
        default_factory=list,
        description="Suggested property features with provenance and confidence, derived from notes, images, or merged system logic."
    )


class ListingDescriptionOutput(BaseModel):
    mls_summary: str = Field(description="Professional MLS listing description, about 100-150 words")


class SocialPostOutput(BaseModel):
    social_media_post: str = Field(description="Catchy, emoji-friendly social media post with hashtags")


class EmailCampaign(BaseModel):
    subject: str = Field(description="High-open rate subject line using a 'hook'")
    body: str = Field(description="Persuasive email body with a clear CTA to book a tour")
    preview_text: str = Field(description="The 1-sentence snippet seen in the inbox preview")