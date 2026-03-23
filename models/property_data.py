from pydantic import BaseModel, Field
from typing import List, Optional

from models.property_image import PropertyImage
from models.feature_candidate import FeatureCandidate


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