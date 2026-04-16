import asyncio
from typing import cast

from chains.fair_housing_compliance_chain import (
    FairHousingComplianceOutput,
    build_fair_housing_compliance_chain,
)
from models.compliance import ComplianceReviewResult


class ComplianceService:
    def __init__(self, api_key: str):
        self.chain = build_fair_housing_compliance_chain(api_key)

    async def review_asset(self, asset_type: str, text: str) -> ComplianceReviewResult:
        if not text or not text.strip():
            return ComplianceReviewResult(
                asset_type=asset_type,
                original_text=text,
                compliant_text=text,
                status="pass",
                issues_found=[],
                reviewer_notes="No content to review.",
            )

        raw_result = await self.chain.ainvoke(
            {
                "asset_type": asset_type,
                "copy_text": text,
            }
        )
        result = cast(FairHousingComplianceOutput, raw_result)

        return ComplianceReviewResult(
            asset_type=asset_type,
            original_text=text,
            compliant_text=result.compliant_text,
            status=result.status,
            issues_found=result.issues_found,
            reviewer_notes=result.reviewer_notes,
        )

    async def review_assets(
        self,
        assets: dict[str, str],
    ) -> dict[str, ComplianceReviewResult]:
        tasks = {
            asset_name: self.review_asset(asset_name, asset_text)
            for asset_name, asset_text in assets.items()
        }

        keys = list(tasks.keys())
        values = await asyncio.gather(*tasks.values())

        return dict(zip(keys, values))