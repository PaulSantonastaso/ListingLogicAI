from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyDetails(BaseModel):
    address: Optional[str] = Field(
        default=None,
        description="Full property address or community name"
    )

    bedrooms: Optional[int] = Field(
        default=None,
        description="Number of bedrooms as an integer"
    )

    bathrooms: Optional[float] = Field(
        default=None,
        description="Number of bathrooms as a decimal if needed (e.g., 2.5)"
    )

    list_price: Optional[int] = Field(
        default=None,
        description="Listing price in USD as a number without commas"
    )

    square_footage: Optional[int] = Field(
        default=None,
        description="Square footage of the property in square feet"
    )

    key_features: List[str] = Field(
        default_factory=list,
        description="3-5 short phrases describing standout property features"
    )


class ListingDescriptionOutput(BaseModel):
    mls_summary: str = Field(description="Professional MLS listing description, about 100-150 words")


class SocialPostOutput(BaseModel):
    social_media_post: str = Field(description="Catchy, emoji-friendly social media post with hashtags")