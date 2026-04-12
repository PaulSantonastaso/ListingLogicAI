"""
image_caption_chain.py

Generates a short marketing caption for a single property image based on
detected room type, visible features, and quality score.

Uses Gemini Flash Lite for cost efficiency — ~$0.00003 per image.
Output is a single caption string, 15-25 words, marketing-forward,
grounded only in detected features.

No hallucination risk — the prompt explicitly forbids inventing features
not present in the input data.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

CAPTION_PROMPT = """You are a real estate marketing copywriter writing a short caption for a single property photo.

PHOTO DETAILS:
Room type: {room_type}
Visible features: {visible_features}
Quality score: {quality_score}
Marketing worthy: {marketing_worthy}

RULES:
- Write exactly ONE caption, 15-25 words.
- Ground the caption only in the provided room type and visible features.
- Do not invent features, finishes, views, or amenities not listed above.
- Make it lifestyle-forward and specific — not generic.
- Never use: stunning, meticulously, dream, nestled, rare find, must-see.
- Never mention the quality score or marketing score in the caption.
- Write as a statement, not a question. No punctuation at the end.
- If visible features are empty, write a simple factual caption based on room type only.

EXAMPLES OF STRONG CAPTIONS:
- "Screened pool and spa with tiled coping and mature landscaping — your private backyard oasis"
- "White shaker cabinetry, dark wood countertops, and stainless steel appliances in an open kitchen layout"
- "First-floor primary suite with barn door entry, tray ceiling, and direct pool access"
- "Living room with wood plank flooring, fireplace, and sliding glass doors to the pool"
- "Front exterior with covered entry, large windows, and manicured landscaping"

Return only the caption text. No labels, no quotes, no extra formatting."""


def build_image_caption_chain(api_key: str):
    """
    Build a simple caption chain using Flash Lite and string output.
    Returns a plain string — no structured output needed for a single field.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=api_key,
        temperature=0.4,
    )

    prompt = ChatPromptTemplate.from_template(CAPTION_PROMPT)
    chain = prompt | llm | StrOutputParser()
    return chain


async def generate_caption_for_image(
    room_type: str,
    visible_features: list[str],
    quality_score: float | None,
    marketing_worthy: bool | None,
    api_key: str,
) -> str:
    """
    Generate a single marketing caption for one image.
    Returns the caption string or a safe fallback if generation fails.
    """
    chain = build_image_caption_chain(api_key)

    features_str = ", ".join(visible_features) if visible_features else "none detected"
    quality_str = f"{quality_score:.2f}" if quality_score is not None else "unknown"
    marketing_str = "yes" if marketing_worthy else "no" if marketing_worthy is False else "unknown"

    try:
        caption = await chain.ainvoke({
            "room_type": room_type.replace("_", " "),
            "visible_features": features_str,
            "quality_score": quality_str,
            "marketing_worthy": marketing_str,
        })
        return caption.strip()
    except Exception:
        # Graceful fallback — never break the pipeline over a caption
        room_label = room_type.replace("_", " ").title()
        return f"{room_label} with {features_str}" if visible_features else room_label