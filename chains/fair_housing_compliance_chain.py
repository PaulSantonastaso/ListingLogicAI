from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.compliance import ComplianceStatus


class FairHousingComplianceOutput(BaseModel):
    status: ComplianceStatus
    issues_found: list[str] = Field(
        default_factory=list,
        description="List of potential compliance or advertising issues found in the copy."
    )
    reviewer_notes: str = Field(
        default="",
        description="Short explanation of why the copy passed, was revised, or was flagged."
    )
    compliant_text: str = Field(
        description="Final compliant version of the text. If already compliant, return the original text unchanged."
    )


def build_fair_housing_compliance_chain(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(FairHousingComplianceOutput)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a real estate marketing compliance reviewer.

Review the provided real estate marketing copy for:
1. Potential Fair Housing issues
2. Unsupported or misleading claims
3. Risky language implying buyer preference, limitation, exclusion, or protected-class targeting

Rules:
- Preserve strong marketing quality.
- Prefer factual, property-centered language.
- Do not add new facts.
- If the text is already compliant, return status = "pass".
- If small edits make it compliant, return status = "revised".
- If the text is too risky to safely fix without changing meaning substantially, return status = "flagged".

Avoid risky phrases and ideas such as:
- perfect for families
- ideal for young professionals
- safe neighborhood
- walk to church
- great for retirees
- bachelor pad
- family-friendly
- exclusive community

Focus on the home, property features, layout, finishes, outdoor space, and factual amenities.

Return structured output only.
            """.strip(),
        ),
        (
            "user",
            """
Asset Type: {asset_type}

Copy to Review:
{copy_text}
            """.strip(),
        ),
    ])

    return prompt | structured_llm