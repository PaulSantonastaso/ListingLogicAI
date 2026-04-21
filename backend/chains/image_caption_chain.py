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

CAPTION_PROMPT = """You are a real estate marketing copywriter. Write one short caption for a single property photo.

PHOTO DETAILS:
Room type: {room_type}
Visible features: {visible_features}
Quality score: {quality_score}
Caption index for this room: {room_caption_index} of {room_caption_total}

CORE RULES:
- Exactly ONE caption, 15-25 words, no punctuation at the end
- Ground every detail in the visible features provided — never invent
- If visible features are empty, write a simple factual caption based on room type only
- Vary your sentence structure — not every caption should follow [material] + [verb phrase] + [result]
- If caption index is greater than 1, your opening word or phrase must be completely different from any previous caption for this room — if caption 1 started with a verb, caption 2 must start with a material or layout observation; if caption 2 started with a material, caption 3 must start with a verb or spatial descriptor. Never repeat an opening word across captions of the same room type.
- Never open with the room type as a label (e.g. not "Kitchen with..." or "Bathroom featuring...")
- Never use: stunning, meticulously, dream, nestled, features, highlights, showcases, boasts, defines this space, soars above
- Never end with a lifestyle coda formula: "for your daily routine", "for your morning routine", "for evening relaxation", "for your [any] routine", "perfect for relaxing"
- Never mention appliances from the sacrificial tier: dishwasher, refrigerator, microwave, garbage disposal, or any standard builder-grade appliance unless it is the only feature available
- Never use: culinary workflow, workflow efficiency, maximize your
- Never repeat an opening word or phrase across any two captions in the same listing — if "Gather" opened one caption, it cannot open another

ROOM-SPECIFIC CREATIVE DIRECTION:
Every caption should answer "what does it feel like to live in this space" — not just describe what is visible.
Sell the moment, not the spec. A reader should be able to picture their life in this room.

KITCHEN: The feeling is energy, capability, and connection. This is where the week gets organized and the weekend gets celebrated.
  Strong: "A 5-burner gas cooktop and double wall ovens anchor a kitchen that means business on Sunday mornings"
  Strong: "Prep, plate, and pivot — the central island connects the kitchen to the living area for effortless hosting"
  Strong: "Light cabinetry and a tile backsplash frame a layout where cooking and conversation happen at the same time"
  Strong: "The peninsula extends the prep space while the island handles overflow — built for the way people actually cook"
  Weak: "Wood-look tile flooring flows through this open floor plan centered by a kitchen island"
  Weak: "Host dinner parties with ease using the gas cooktop" — never use this opener
  Weak: "maximize your culinary workflow" — never use this phrase
  Weak: "Wood-look tile flooring stretches across..." — never lead a kitchen caption with flooring under any circumstances

LIVING_ROOM / GREAT_ROOM: The feeling is ease, light, and the end of a long day. This is where the home exhales.
  Strong: "Oversized windows flood the living area with the kind of natural light that makes you want to stay in"
  Strong: "An open layout, recessed lighting, and sightlines into the kitchen — this room was made for slow Sundays"

PRIMARY_BEDROOM / BEDROOM: The feeling is calm, privacy, and a good night's sleep. Not storage. Not square footage.
  Strong: "Plush carpet and large windows make this bedroom the kind of room you don't want to leave on a Saturday morning"
  Strong: "Built-in shelving and organized hanging rods give this bedroom the quiet order of a boutique hotel"
  Weak: "Plush carpeted flooring meets custom built-in shelving for a highly functional storage solution"

PRIMARY_BATHROOM / BATHROOM: The feeling is a hotel you never have to check out of. Sensory and calm.
  Strong: "Marble-look tile and a glass-enclosed shower turn the morning routine into something worth waking up for"
  Strong: "A soaking tub, double vanity, and floor-to-ceiling tile — this bathroom earns its own line in the listing"
  Weak: "Marble-look tile surrounds the deep soaking tub for your daily routine"
  Banned closing: never end with "for your daily routine", "for your morning routine", "for evening relaxation", "in this space"

BACK_EXTERIOR / PATIO / OUTDOOR: The feeling is the first Friday night of a long weekend. Privacy, air, and no agenda.
  Strong: "Slide the glass doors open to a covered brick patio and fenced backyard built for Friday nights with nowhere to be"
  Strong: "A wooden deck, grassy lawn, and privacy fence — the kind of backyard that makes staying home the easy choice"

FRONT_EXTERIOR: The feeling is arrival. The home makes a promise before you walk in.
  Strong: "Brick and stone meet a gabled roofline — this 2025 build makes a strong first impression before you step inside"
  Strong: "A covered entryway and clean concrete driveway signal that everything inside is just as considered"

POOL / COMMUNITY_AMENITY: The feeling is a resort you live next to. Leisure without the travel.
  Strong: "Lap lanes, a splash pad, and a covered pavilion — the Ladera community pool is the kind of amenity that closes deals"
  Strong: "The community pool and playground are steps away — the kind of perk that makes the HOA fee feel like a bargain"

GARAGE / UTILITY / OTHER: Write a clean, factual caption grounded in what is visible. No lifestyle inflation needed for utility spaces.

Return only the caption text. No labels, no quotes, no extra formatting."""


def build_image_caption_chain(api_key: str):
    """
    Build a simple caption chain using Flash Lite and string output.
    Returns a plain string — no structured output needed for a single field.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        google_api_key=api_key,
        temperature=0.7,
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
    room_caption_index: int = 1,
    room_caption_total: int = 1,
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
            "room_caption_index": room_caption_index,
            "room_caption_total": room_caption_total,
        })
        return caption.strip()
    except Exception:
        # Graceful fallback — never break the pipeline over a caption
        room_label = room_type.replace("_", " ").title()
        return f"{room_label} with {features_str}" if visible_features else room_label