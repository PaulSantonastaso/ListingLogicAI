from pydantic import BaseModel, Field
from typing import Literal, Optional


FeatureSource = Literal["notes", "image", "merged", "user_confirmed"]
ConfidenceLevel = Literal["low", "medium", "high"]


class ExtractedFeature(BaseModel):
    name: str
    source: FeatureSource
    confidence: float = Field(..., ge=0.0, le=1.0)
    confidence_level: ConfidenceLevel
    evidence: Optional[str] = None