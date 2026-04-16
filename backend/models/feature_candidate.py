from pydantic import BaseModel, Field
from typing import Literal, Optional


FeatureSource = Literal["notes", "image", "merged", "user"]
ConfidenceLevel = Literal["low", "medium", "high"]


class FeatureCandidate(BaseModel):
    name: str = Field(
        ...,
        description="Feature name as a short noun phrase."
    )
    source: FeatureSource = Field(
        ...,
        description="Where the feature originated."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the feature."
    )
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Bucketed confidence level."
    )
    evidence: Optional[str] = Field(
        default=None,
        description="Optional evidence or explanation for why this feature was included."
    )