from pydantic import BaseModel
from typing import List, Literal


ComplianceStatus = Literal["pass", "revised", "flagged"]


class ComplianceReviewResult(BaseModel):
    asset_type: str
    original_text: str
    compliant_text: str
    status: ComplianceStatus
    issues_found: List[str] = []
    reviewer_notes: str | None = None