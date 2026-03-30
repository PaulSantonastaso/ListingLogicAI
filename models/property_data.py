from pydantic import BaseModel, Field
from typing import List, Optional

from models.property_image import PropertyImage
from models.feature_candidate import FeatureCandidate


class PropertyDetails(BaseModel):
    address: Optional[str] = Field(
        default=None,
        description="Full street address such as '101 Lake Ave'. Do not include community or neighborhood names."
    )

    city: Optional[str] = Field(
        default=None,
        description="Official city or municipality where the property is located. Do not place neighborhood or community names here."
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
        description="Private on-property pool features such as in-ground pool, heated pool, spa, or screened enclosure. Do not include community pool amenities."
    )

    cooling: Optional[str] = Field(
        default=None,
        description="Cooling system type such as Central Air, Mini-Split, or Window Units. Only extract if explicitly stated in the notes."
    )

    heating: Optional[str] = Field(
        default=None,
        description="Heating system type such as Central, Electric, Gas, or Heat Pump. Only extract if explicitly stated in the notes."
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

    community_features: list[str] = Field(
        default_factory=list,
        description="Community or association amenities such as clubhouse, community pool, playground, fitness center, or gated entry. Do not include private property features."
    )

    community_name: Optional[str] = Field(
        default=None,
        description="Neighborhood or master-planned community name such as Lake Nona, SoHo, or Brickell. Do not place this value in the city field."
    )

    subdivision_name: Optional[str] = Field(
        default=None,
        description="Subdivision, residential development section, or condo building name such as Laureate Park or Baldwin Park."
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
    mls_summary: str = Field(
        description=(
            "Professional MLS listing description. Maximum 950 characters including spaces. "
            "Do not exceed this limit under any circumstances."
        )
    )
    headline: str = Field(
        description=(
            "A punchy 8-12 word lifestyle-forward headline for this listing. "
            "Used in Zillow's What's Special section, email subject lines, and social captions. "
            "Should capture the single most compelling thing about this property. "
            "No punctuation at the end. No generic phrases like 'Dream Home' or 'Must See'."
        )
    )


class SocialPostOutput(BaseModel):
    platform: Optional[str] = Field(
        default=None,
        description="Target social platform such as Facebook or Instagram"
    )
    slot_name: Optional[str] = Field(
        default=None,
        description="Planned slot name such as facebook_feed, instagram_post_1, or instagram_post_2"
    )
    image_id: Optional[str] = Field(
        default=None,
        description="ID of the selected image tied to this post"
    )
    image_filename: Optional[str] = Field(
        default=None,
        description="Filename of the selected image tied to this post"
    )
    recommended_aspect_ratio: Optional[str] = Field(
        default=None,
        description="Recommended aspect ratio for the image on this platform, such as 4:5 or 1.91:1"
    )
    crop_guidance: Optional[str] = Field(
        default=None,
        description="Brief guidance on how the image should be cropped or framed for this platform"
    )
    room_type: Optional[str] = Field(
        default=None,
        description="Primary room or scene shown in the selected image"
    )
    visible_features: List[str] = Field(
        default_factory=list,
        description="Key visible features supported by the selected image"
    )
    social_media_post: str = Field(
        description="Platform-specific social media caption tied to the selected image"
    )


class SocialMediaSuiteOutput(BaseModel):
    posts: List[SocialPostOutput] = Field(
        default_factory=list,
        description="Collection of platform-specific social posts, each tied to a selected image"
    )


class CampaignEmail(BaseModel):
    subject: str = Field(description="High-open rate subject line tailored to this email's campaign stage")
    body: str = Field(description="Persuasive email body with a clear, singular CTA appropriate for this campaign stage")
    preview_text: str = Field(description="The 1-sentence snippet seen in the inbox preview")
 
 
class EmailCampaign(BaseModel):
    just_listed: CampaignEmail = Field(
        description="Day 1 email. Creates urgency and exclusivity to drive immediate inquiries from the agent's database."
    )
    open_house: CampaignEmail = Field(
        description="Day 3-5 email. Drives foot traffic to the open house with an RSVP feel and lifestyle-forward copy."
    )
    why_this_home: CampaignEmail = Field(
        description="Day 7-10 email. A slower-burn, educational email that sells the lifestyle and explains why this specific home stands out to hesitant buyers."
    )
    just_sold: CampaignEmail = Field(
        description="Post-close email. Builds the agent's brand by showcasing results. Use [DAYS ON MARKET] and [SOLD PRICE] as placeholders for the agent to fill in before sending."
    )