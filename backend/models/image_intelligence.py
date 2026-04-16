from pydantic import BaseModel, Field
from typing import List, Optional


class RankedImage(BaseModel):
    image_id: str
    filename: str

    room_type: Optional[str] = None
    shot_type: Optional[str] = None

    score: float
    score_components: Optional[dict[str, float]] = None

    quality_score: Optional[float] = None
    marketing_worthy: Optional[bool] = None
    
    visible_features: List[str] = Field(default_factory=list)

    reason: str


class WeakImage(BaseModel):
    image_id: str
    filename: str
    reason: str


class ImageHighlight(BaseModel):
    feature: str
    supporting_image_ids: List[str] = Field(default_factory=list)
    reason: Optional[str] = None


class ImageIntelligence(BaseModel):
    ranked_images: List[RankedImage] = Field(default_factory=list)
    weak_images: List[WeakImage] = Field(default_factory=list)
    highlight_images: List[str] = Field(default_factory=list)
    highlights: List[ImageHighlight] = Field(default_factory=list)
    hero_image_id: Optional[str] = Field(
        default=None,
        description="Image ID of the single highest-scoring image across all uploads. Used as the anchor visual for email campaigns."
    )
    summary: Optional[str] = None