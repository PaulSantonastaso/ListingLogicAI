from pydantic import BaseModel, Field
from typing import List, Literal, Optional


RoomType = Literal[
    "front_exterior",
    "back_exterior",
    "living_room",
    "kitchen",
    "dining_room",
    "bedroom",
    "bathroom",
    "office",
    "backyard",
    "patio",
    "garage",
    "other",
]

ShotType = Literal["wide", "detail", "close_up", "unknown"]
ConfidenceLevel = Literal["low", "medium", "high"]
FeatureSource = Literal["image", "vision"]


class ImageFeature(BaseModel):
    name: str = Field(
        ...,
        description="Observed visible feature in the image, written as a short noun phrase."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence that the feature is clearly visible in the image."
    )
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Bucketed confidence level for the detected feature."
    )
    source: FeatureSource = Field(
        default="image",
        description="Source of the feature detection."
    )


class ImageMetadata(BaseModel):
    image_id: str = Field(
        ...,
        description="Unique identifier for the uploaded image."
    )
    filename: str = Field(
        ...,
        description="Original uploaded filename."
    )
    room_type: RoomType = Field(
        default="other",
        description="Best estimate of the room or property area shown in the image."
    )
    shot_type: ShotType = Field(
        default="unknown",
        description="Approximate framing of the image, such as wide room shot or close-up detail."
    )
    is_interior: Optional[bool] = Field(
        default=None,
        description="Whether the image appears to show an interior space."
    )
    is_exterior: Optional[bool] = Field(
        default=None,
        description="Whether the image appears to show an exterior space."
    )
    quality_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Estimated usefulness of the image for marketing purposes."
    )
    likely_marketing_worthy: Optional[bool] = Field(
        default=None,
        description="Whether the image seems suitable for use in listing marketing."
    )


class PropertyImage(BaseModel):
    image_id: str = Field(
        ...,
        description="Unique identifier for the uploaded image."
    )
    filename: str = Field(
        ...,
        description="Original uploaded filename."
    )
    description: str = Field(
        ...,
        description="Conservative factual description of what is clearly visible in the image."
    )
    visible_features: List[ImageFeature] = Field(
        default_factory=list,
        description="Visible property features detected from the image."
    )
    metadata: ImageMetadata = Field(
        ...,
        description="Structured metadata about the uploaded image."
    )