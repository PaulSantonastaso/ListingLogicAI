"""
neighborhood_chain.py

Generates two neighborhood copy outputs from Places API data.
The LLM handles all curation — no blocklist.

Single Flash Lite call does three things:
  1. Selects the 3-5 most character-defining places from up to 24 candidates
  2. Writes mls_insert — 1-2 sentences for weaving into MLS description
  3. Writes neighborhood_guide — 3-4 sentence standalone paragraph for the ZIP

Uses Gemini Flash Lite for cost efficiency (~$0.002/call).
Grounded strictly in Places API data — no invented details.
Fair Housing compliant — lifestyle and amenity focus only.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class NeighborhoodOutput(BaseModel):
    selected_places: list[str] = Field(
        description=(
            "Names of the 3-5 places selected as most character-defining. "
            "Used for debugging and future transparency features."
        )
    )
    mls_insert: str = Field(
        description=(
            "1-2 sentences describing nearby neighborhood highlights. "
            "Specific place names only. Lifestyle-forward, not a list. "
            "Suitable for weaving naturally into an MLS description. "
            "Empty string if no compelling places available."
        )
    )
    neighborhood_guide: str = Field(
        description=(
            "3-4 sentence neighborhood insight paragraph. "
            "Reads like a local recommending the neighborhood. "
            "Specific, evocative, conversational. Not a bulleted list. "
            "Empty string if no compelling places available."
        )
    )


NEIGHBORHOOD_PROMPT = """You are a real estate copywriter who knows what makes a neighborhood feel premium and desirable.

PROPERTY ADDRESS:
{address}

NEARBY PLACES (from live Google Places data — name, category, rating, review count):
{places_formatted}

YOUR TASK:

STEP 1 — CURATE:
From the list above, select the 3-5 places that best communicate neighborhood character and lifestyle quality.
Prioritize: local coffee shops, bakeries, parks, farmers markets, boutique fitness (yoga, pilates), quality grocers (Whole Foods, Trader Joe's, Fresh Market).
Deprioritize: national fast food chains, big box stores, generic gyms. Use your judgment — a beloved local institution with strong reviews beats a chain every time.

STEP 2 — WRITE mls_insert:
1-2 sentences. Specific place names from your selection. Lifestyle-forward, not a list.
Suitable for weaving naturally into an MLS description.
Example: "Steps from Foxtail Coffee and a short walk to Lake Weston Park — the kind of neighborhood that sells itself once buyers arrive."

STEP 3 — WRITE neighborhood_guide:
3-4 sentences. Reads like a local recommending the area to a friend.
Specific, evocative, conversational. Not a bulleted list.
Example: "Westover Hills sits on Orlando's quiet west side, where tree-lined streets meet genuine neighborhood character. Foxtail Coffee is two blocks north — the kind of place regulars know by name. Lake Weston Park is a five-minute walk for morning runs or weekend afternoons."

RULES:
- Only mention places from the provided list. Do not invent places.
- Do not describe demographics, schools, religious institutions, or who lives there.
- Do not use the words "nestled", "charming", "vibrant", "trendy", or "up-and-coming".
- Use walkable language ("steps from", "a short walk", "nearby") — not drive times or distances in miles.
- If the list contains nothing worth highlighting, return empty strings for mls_insert and neighborhood_guide.
- Fair Housing: lifestyle and amenity focus only. No demographic implications."""


def build_neighborhood_chain(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        google_api_key=api_key,
        temperature=0.5,
    )

    structured_llm = llm.with_structured_output(NeighborhoodOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("user", NEIGHBORHOOD_PROMPT),
    ])

    return prompt | structured_llm


async def generate_neighborhood_copy(
    address: str,
    places_formatted: str,
    api_key: str,
) -> NeighborhoodOutput | None:
    if not places_formatted.strip():
        return None

    try:
        chain = build_neighborhood_chain(api_key).with_config(run_name="Neighborhood Copy")
        result = await chain.ainvoke({
            "address": address,
            "places_formatted": places_formatted,
        })
        return result if isinstance(result, NeighborhoodOutput) else None
    except Exception as e:
        import logging
        logging.getLogger(__name__).info(f"Neighborhood chain failed: {e}")
        print(f"[NEIGHBORHOOD CHAIN ERROR] {e}")  # add this
        return None