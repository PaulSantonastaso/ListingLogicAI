from typing import List, Optional
from pydantic import BaseModel, Field


class RankedImage(BaseModel):
    image_id: str = Field(description="Stable image identifier")
    filename: str = Field(description="Original uploaded filename")
    room_type: Optional[str] = Field(
        default=None,
        description="Detected room or property area, such as kitchen, living_room, exterior_front, or pool"
    )
    score: float = Field(
        description="Overall marketing usefulness score for this image"
    )
    quality_score: Optional[float] = Field(
        default=None,
        description="Underlying image quality score if available"
    )
    marketing_worthy: Optional[bool] = Field(
        default=None,
        description="Whether the image appears suitable for marketing use"
    )
    visible_features: List[str] = Field(
        default_factory=list,
        description="Important visual features visible in the image"
    )
    reason: str = Field(
        description="Short explanation for why this image ranked where it did"
    )


class WeakImage(BaseModel):
    image_id: str = Field(description="Stable image identifier")
    filename: str = Field(description="Original uploaded filename")
    reason: str = Field(
        description="Why the image is weak for marketing, such as blurry, dark, redundant, or low-value room type"
    )


class ImageHighlight(BaseModel):
    feature: str = Field(
        description="A marketing-relevant visual feature or theme derived from images"
    )
    supporting_image_ids: List[str] = Field(
        default_factory=list,
        description="Images that support this highlight"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Why this feature matters for marketing"
    )


class ImageIntelligence(BaseModel):
    ranked_images: List[RankedImage] = Field(
        default_factory=list,
        description="Images ranked by overall marketing usefulness"
    )
    weak_images: List[WeakImage] = Field(
        default_factory=list,
        description="Images that may be lower value for marketing"
    )
    highlight_images: List[str] = Field(
        default_factory=list,
        description="Top image IDs that best represent the property's strongest visual selling points"
    )
    highlights: List[ImageHighlight] = Field(
        default_factory=list,
        description="Top visual marketing highlights derived from the image set"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Short summary of the property's strongest visual marketing themes"
    )